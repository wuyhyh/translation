# PDF 技术书翻译工具

这是一个面向个人学习的、可断点续传的英文技术书 PDF 翻译项目。它使用 PyMuPDF 按物理页提取文本和图片，可使用 OpenAI Python SDK 或 Ollama 原生 `/api/chat` 调用本地模型。

> `translate` 必须显式给出 `--pages` 或 `--chapter`；只有明确运行 `translate-all` 才会规划并续译全书。所有命令中的页码都是 PDF 阅读器显示的从 1 开始的物理页码，不是书页上印刷的页码。

## Windows 11 + WSL Ubuntu 安装

1. 在 Windows 中启用 WSL2 并安装 Ubuntu，然后在 Ubuntu 终端安装 Python 支持：

   ```bash
   sudo apt update
   sudo apt install -y python3 python3-venv python3-pip
   ```

2. 把项目和 PDF 放在 WSL 文件系统中（例如 `~/translation`）。大 PDF 放在 `/mnt/c/...` 也能使用，但通常更慢。

3. 在项目目录创建并启用虚拟环境：

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

4. 确认 WSL 能访问模型服务。如果 Windows 主机防火墙拦截 11434 端口，需要允许局域网访问。默认配置为：

   - Base URL: `http://192.168.1.141:11434/v1`
   - API Key: `ollama`
   - Model: `qwen3.8:latest`
   - temperature: `0.1`
   - timeout: `600` 秒
   - 推荐后端: `ollama`（原生 `/api/chat`，可真正关闭 thinking）
   - 推荐并发数: `1`
   - 推荐块尺寸: `8000`

可通过环境变量 `TRANSLATOR_BASE_URL`、`TRANSLATOR_API_KEY`、`TRANSLATOR_MODEL` 覆盖前三项，也可在命令行用同名全局选项覆盖。全局选项必须放在子命令之前。

## 建议工作流

先判定 PDF 类型：

```bash
python translate.py inspect
```

程序会在全书均匀抽样页面。如果判定为扫描型，`extract` 会明确报告需要 OCR 并停止，不会静默产生空文件。

检查 API 和 thinking 状态。`auto` 会先测试 OpenAI 兼容端点的 `extra_body={"think": false, "keep_alive": -1}`；如果响应仍含 reasoning，则切换到原生 Ollama 后端：

```bash
python translate.py check-api --backend auto
```

只提取少量样例页：

```bash
python translate.py extract --pages 32-35
```

提取整本 PDF（只提取，不调用模型）：

```bash
python translate.py extract
```

只翻译指定页：

```bash
python translate.py translate --pages 32-35 --backend ollama --workers 1 --chunk-size 8000
```

只翻译已提取的指定章节，可使用章号、英文章名或文件名 slug：

```bash
python translate.py translate --chapter 1 --backend ollama --workers 1 --chunk-size 8000
python translate.py translate --chapter introduction-to-stm32-mcu-portfolio --backend ollama --workers 1 --chunk-size 8000
```

首次启动全书翻译或从全书断点继续。该命令先补齐尚未提取的页面，只为尚未登记的页面规划块，已有完成块不会重新翻译：

```bash
python translate.py translate-all --backend ollama --workers 1 --chunk-size 8000
```

从已经登记的中断块继续，不重新提取或重切块：

```bash
python translate.py resume --backend ollama --workers 1 --chunk-size 8000
```

只重试最终状态为 `failed` 的块：

```bash
python translate.py retry-failed --backend ollama --workers 1 --chunk-size 8000
```

查看完成页数、块数、重试数、最近速度和预计完成时间：

```bash
python translate.py status
```

合并已生成的章节：

```bash
python translate.py merge
```

在隔离的系统临时目录中，用同一组 10～20 页比较 8000/12000 字符块和 1/2/4 并发：

```bash
python translate.py benchmark --pages 106-117 --results benchmarks/latest.json
```

临时译文、临时进度和临时图片会在基准结束后删除，只保留 JSON 报告，不会污染正式 `work/progress.json`、`output/` 或 `images/`。

运行测试：

```bash
python -m pytest -q
```

## 文件与断点

- `glossary.yaml`：统一术语和不可翻译标识符。翻译前可按需增补。
- `work/manifest.json`：PDF 类型、目录、页文件和图片元数据。
- `work/pages/page-XXXX.md`：带 `<!-- page: X -->` 的提取结果。
- `images/`：以英文、数字和短横线命名的提取图片。
- `work/progress.json`：每个块的 SHA-256、状态、顺序、重试次数、token、页码、耗时和输入/输出文件。
- `work/chunks/`：登记后固定不变的源块；`resume` 直接读取这里，避免修改块尺寸后断点漂移。
- `work/translated/`：按块保存的译文，用于恢复和重建章节。
- `output/NN-english-slug.md`：按章节生成的译文。
- `logs/requests-errors.jsonl`：请求错误的结构化日志；不保存完整提示词和原文。

默认分块上限为 8000 个英文字符，仅在标题、段落、完整代码块或完整表格边界切分；单个不可分割单元不会被拦腰切断。若服务以 `length` 截断，程序会沿相同安全边界自动缩小请求并重试。`--workers` 支持 1、2、4，共享 HTTP 连接池，在途任务上限为 `2 × workers`。

每个块通过页码、标题层级、代码围栏、图片路径和异常标记校验后，立即原子写入独立输出，再在线程锁内原子更新 `progress.json`。HTTP 429、500、502、503、超时以及格式校验错误最多自动重试 3 次，采用 1、2、4 秒指数退避；单块最终失败不会阻塞其他块。全书模式每新增完成至少 10 页打印一次页数、百分比、近期速度、ETA 和块统计。

2026-09-09 对 PDF 物理页 106～117 的实测结果保存在 `benchmarks/latest.json`。Ollama 服务表现为近似串行，推荐使用 `--backend ollama --workers 1 --chunk-size 8000`，避免增加共享服务器负载而没有实际吞吐收益。

## 质量限制

PDF 的视觉排版不等于语义结构。多栏、页眉页脚、图注、数学式和某些嵌入字体可能需要人工校对。建议始终先试译 3～5 页，检查标题、代码、图片顺序和术语后，再扩大范围。
