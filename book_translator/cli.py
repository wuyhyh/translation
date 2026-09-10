from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Iterable, List, Optional

from .benchmark import run_benchmark
from .audit import (
    audit_project, generate_semantic_samples, recover_missing_sources,
    restore_exact_code_blocks,
)
from .chunker import Chunk, load_page_records, make_chunks
from .extractor import extract_pdf, inspect_pdf
from .pipeline import merge_markdown, rebuild_chapter_files
from .progress import ProgressStore
from .repair import queue_repaired_chunks, repair_failed_chunks, write_failed_report
from .status import progress_status
from .translator import check_api, translate_chunks
from .util import contiguous_ranges, parse_page_ranges


DEFAULT_BASE_URL = "http://192.168.1.141:11434/v1"
DEFAULT_MODEL = "qwen3.8:latest"


def _add_runtime_options(parser: argparse.ArgumentParser, chunk_size: bool = True) -> None:
    parser.add_argument("--workers", type=int, choices=(1, 2, 4), default=1, help="有界并发请求数")
    parser.add_argument("--backend", choices=("auto", "openai", "ollama"), default="auto")
    parser.add_argument("--max-retries", type=int, default=3, help="每块失败后的最大重试次数")
    if chunk_size:
        parser.add_argument("--chunk-size", type=int, default=8000, help="目标块上限，建议 8000 或 12000")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="可断点续传的英文技术书 PDF 翻译工具（页码均为 PDF 物理页码）")
    parser.add_argument("--pdf", type=Path, default=Path("MasteringSTM32-2e.pdf"))
    parser.add_argument("--work-dir", type=Path, default=Path("work"))
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    parser.add_argument("--glossary", type=Path, default=Path("glossary.yaml"))
    parser.add_argument("--base-url", default=os.getenv("TRANSLATOR_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--api-key", default=os.getenv("TRANSLATOR_API_KEY", "ollama"))
    parser.add_argument("--model", default=os.getenv("TRANSLATOR_MODEL", DEFAULT_MODEL))
    parser.add_argument("--timeout", type=float, default=600.0)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("inspect", help="判断 PDF 是文本型还是扫描型")
    check = sub.add_parser("check-api", help="检查 thinking 关闭状态和后端")
    check.add_argument("--backend", choices=("auto", "openai", "ollama"), default="auto")

    extract = sub.add_parser("extract", help="按页提取 Markdown 和图片")
    extract.add_argument("--pages", help="例如 32-35,40；省略则提取全书")
    extract.add_argument("--force", action="store_true", help="覆盖已提取页")

    translate = sub.add_parser("translate", help="只翻译指定页码或章节")
    group = translate.add_mutually_exclusive_group(required=True)
    group.add_argument("--pages", help="例如 32-35,40")
    group.add_argument("--chapter", help="章号、英文章名或文件 slug")
    _add_runtime_options(translate)

    all_parser = sub.add_parser("translate-all", help="提取全书并从断点续译")
    _add_runtime_options(all_parser)

    resume = sub.add_parser("resume", help="从 progress.json 的未完成块继续")
    _add_runtime_options(resume)

    retry = sub.add_parser("retry-failed", help="仅重译 failed 块")
    _add_runtime_options(retry)

    repair = sub.add_parser("repair-failed", help="按页、带占位符保护地修复最终 failed 块")
    repair.add_argument("--backend", choices=("auto", "openai", "ollama"), default="ollama")
    repair.add_argument("--max-retries", type=int, default=3)
    repair.add_argument(
        "--redo-repaired", action="store_true",
        help="仅重新排队此前由 failed 修复流程生成的块，用于强化完整性复核",
    )

    failed_report = sub.add_parser("failed-report", help="按 progress.json 最终状态生成失败块报告")
    failed_report.add_argument("--destination", type=Path, default=Path("reports/failed-blocks.md"))

    audit = sub.add_parser("audit", help="执行全书结构、代码和标识符完整性审计")
    audit.add_argument("--destination", type=Path, default=Path("reports/audit-report.md"))
    audit.add_argument("--semantic-destination", type=Path, default=Path("reports/semantic-samples.md"))

    sub.add_parser("restore-code-blocks", help="从源块确定性恢复 fenced code，不调用模型")

    sub.add_parser("status", help="查看完成页数、块数、失败数和 ETA")

    merge = sub.add_parser("merge", help="按文件名合并所有已生成章节")
    merge.add_argument("--destination", type=Path, default=None)

    benchmark = sub.add_parser("benchmark", help="在临时目录测试 1/2/4 并发和 8000/12000 块")
    benchmark.add_argument("--pages", default="106-117", help="10～20 个代表性物理页")
    benchmark.add_argument("--backend", choices=("auto", "openai", "ollama"), default="auto")
    benchmark.add_argument("--results", type=Path, default=Path("benchmarks/latest.json"))
    return parser


def _page_count(pdf: Path) -> int:
    return int(inspect_pdf(pdf)["page_count"])


def _chunk_bounds(size: int) -> tuple[int, int]:
    if size < 4000 or size > 16000:
        raise ValueError("--chunk-size 必须在 4000..16000 之间")
    return max(4000, int(size * 0.6)), size


def _prepare_chunks(
    args: argparse.Namespace, pages: Optional[List[int]] = None,
    chapter: Optional[str] = None,
) -> List[Chunk]:
    records = load_page_records(args.work_dir, pages=pages, chapter=chapter)
    target_min, target_max = _chunk_bounds(args.chunk_size)
    return make_chunks(records, target_min=target_min, target_max=target_max)


def _execute(
    args: argparse.Namespace, chunks: Iterable[Chunk], progress: ProgressStore,
    total_pages: Optional[int] = None, progress_every: int = 0,
    register: bool = False, retire_replaced: bool = True,
) -> int:
    chunks = list(chunks)
    if register:
        progress.register(
            chunks, args.work_dir / "translated", args.work_dir / "chunks",
            retire_replaced=retire_replaced,
        )
    summary = translate_chunks(
        chunks, progress, args.base_url, args.api_key, args.model, args.glossary,
        Path("logs") / "requests-errors.jsonl", timeout=args.timeout,
        temperature=0.1, max_retries=args.max_retries, workers=args.workers,
        backend_name=args.backend, chunk_max=args.chunk_size,
        total_pages=total_pages, progress_every=progress_every,
    )
    written = rebuild_chapter_files(progress, args.output_dir, args.glossary)
    result = summary.as_dict()
    result.pop("chunk_results", None)
    result["chapter_files"] = [str(path) for path in written]
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if summary.failed else 0


def _full_book_chunks(args: argparse.Namespace, progress: ProgressStore) -> List[Chunk]:
    extract_pdf(args.pdf, args.work_dir)
    registered = progress.registered_pages()
    records = [
        record for record in load_page_records(args.work_dir)
        if int(record["page_number"]) not in registered
    ]
    if records:
        target_min, target_max = _chunk_bounds(args.chunk_size)
        chunks = make_chunks(records, target_min=target_min, target_max=target_max)
        progress.register(
            chunks, args.work_dir / "translated", args.work_dir / "chunks",
            retire_replaced=False,
        )
    return progress.load_chunks({"pending", "failed"})


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "inspect":
            print(json.dumps(inspect_pdf(args.pdf), ensure_ascii=False, indent=2))
            return 0
        if args.command == "check-api":
            result = check_api(
                args.base_url, args.api_key, args.model, args.timeout,
                Path("logs") / "requests-errors.jsonl", args.backend,
            )
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        if args.command == "extract":
            pages = parse_page_ranges(args.pages, _page_count(args.pdf)) if args.pages else None
            manifest = extract_pdf(args.pdf, args.work_dir, pages=pages, force=args.force)
            extracted = sorted(int(key) for key in manifest.get("pages", {}))
            print(json.dumps({
                "pdf_type": manifest["inspection"]["pdf_type"],
                "page_count": manifest["inspection"]["page_count"],
                "extracted_pages_in_manifest": contiguous_ranges(extracted),
                "manifest": str(args.work_dir / "manifest.json"),
            }, ensure_ascii=False, indent=2))
            return 0
        if args.command == "translate":
            pages = parse_page_ranges(args.pages, _page_count(args.pdf)) if args.pages else None
            chunks = _prepare_chunks(args, pages=pages, chapter=args.chapter)
            progress = ProgressStore(args.work_dir / "progress.json")
            return _execute(args, chunks, progress, register=True)
        if args.command == "translate-all":
            progress = ProgressStore(args.work_dir / "progress.json")
            chunks = _full_book_chunks(args, progress)
            return _execute(args, chunks, progress, total_pages=_page_count(args.pdf), progress_every=10)
        if args.command == "resume":
            progress = ProgressStore(args.work_dir / "progress.json")
            chunks = progress.load_chunks({"pending", "failed"})
            return _execute(args, chunks, progress, total_pages=_page_count(args.pdf), progress_every=10)
        if args.command == "retry-failed":
            progress = ProgressStore(args.work_dir / "progress.json")
            failed_ids = set(progress.ids_with_status({"failed"}))
            progress.reset_failed()
            chunks = [chunk for chunk in progress.load_chunks({"pending"}) if chunk.chunk_id in failed_ids]
            return _execute(args, chunks, progress, total_pages=_page_count(args.pdf), progress_every=10)
        if args.command == "failed-report":
            progress = ProgressStore(args.work_dir / "progress.json")
            result = write_failed_report(progress, args.destination)
            result["report"] = str(args.destination)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        if args.command == "repair-failed":
            progress = ProgressStore(args.work_dir / "progress.json")
            queued = queue_repaired_chunks(progress) if args.redo_repaired else []
            recovered = recover_missing_sources(progress, args.work_dir)
            summary = repair_failed_chunks(
                progress, args.base_url, args.api_key, args.model, args.glossary,
                Path("reports"), timeout=args.timeout, backend_name=args.backend,
                max_retries=args.max_retries,
            )
            result = summary.__dict__.copy()
            result["recovered_source_files"] = recovered
            result["requeued_repaired_chunks"] = queued
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 1 if summary.remaining_failed else 0
        if args.command == "audit":
            progress = ProgressStore(args.work_dir / "progress.json")
            recovered = recover_missing_sources(progress, args.work_dir)
            total_pages = _page_count(args.pdf)
            result = audit_project(progress, args.work_dir, args.output_dir, total_pages, args.destination)
            repaired_pages = sorted({
                int(page) for item in progress.snapshot()["chunks"].values()
                if item.get("status") == "completed" and item.get("repaired")
                for page in item.get("pages") or []
            })
            semantic = generate_semantic_samples(
                progress, args.work_dir, repaired_pages, args.semantic_destination,
            )
            result["semantic_samples"] = semantic
            result["recovered_source_files"] = recovered
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0 if result["passed"] else 1
        if args.command == "restore-code-blocks":
            progress = ProgressStore(args.work_dir / "progress.json")
            result = restore_exact_code_blocks(progress)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 1 if result["unresolved"] else 0
        if args.command == "status":
            progress = ProgressStore(args.work_dir / "progress.json")
            print(json.dumps(progress_status(progress, _page_count(args.pdf)), ensure_ascii=False, indent=2))
            return 0
        if args.command == "merge":
            destination = args.destination or (args.output_dir / "all-translated.md")
            files = merge_markdown(args.output_dir, destination)
            print(json.dumps({"merged_files": len(files), "destination": str(destination)}, ensure_ascii=False, indent=2))
            return 0
        if args.command == "benchmark":
            pages = parse_page_ranges(args.pages, _page_count(args.pdf))
            report = run_benchmark(
                args.pdf, pages, args.base_url, args.api_key, args.model,
                args.glossary, args.results, args.timeout, args.backend,
            )
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 0
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"请求失败 ({type(exc).__name__}): {str(exc)[:500]}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n已中断；进度已保存，可使用 resume 继续。", file=sys.stderr)
        return 130
    return 0
