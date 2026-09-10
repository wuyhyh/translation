# Technical identifier review

- Review date: 2026-09-10
- Source audit: `reports/audit-report.md` (22 issue rows)
- Pre-review backup: `backups/pre-identifier-review-20260910T024803Z`
- Classification totals: **A=6, B=4, C=12, D=0**

Definitions:

- **A** — the translation omitted, rewrote, or damaged a technical identifier.
- **B** — the English source/PDF itself contains a spelling or extraction anomaly.
- **C** — validator false positive; the translation is correct.
- **D** — unresolved and requires human judgment.

## Findings

| # | PDF page | Chunk | Source identifier/context | Translation counterpart before review | Class | Evidence | Modified | Result |
|---:|---:|---|---|---|:---:|---|:---:|---|
| 1 | 55 | `ed78e7d0fc278832` | `/pc` in `1$/pc` | `1 美元/件` | C | `/pc` means “per piece”; it is neither an absolute path nor an identifier. | No | Path grammar no longer treats an arbitrary single slash component as a path. |
| 2 | 95 | `b3228e67eddf8ea4` | `C:\ST\STM32CubeIDE` | `C:\ST\STM32CubeIDE` | C | The path is preserved character-for-character. The old Windows-path regex consumed adjacent Chinese punctuation. | No | Windows paths now stop at the final ASCII path character. |
| 3 | 155, 157 | `ecad685e479c3d6c` | `/scanf` inside `printf()/scanf()` | `` `printf()`/`scanf()` `` | C | Both function names are preserved. The slash is an operator between calls, not a filesystem root. | No | Single arbitrary slash components are excluded from path matching. |
| 4 | 217 | `9f5579b959ba6ce1` | `main.c`, `stm32XXxx_hal_msp.c` | The complete source paragraph was absent. | A | The source paragraph between the CubeMX configuration paragraph and footnote 9 was missing from the translation. | Yes | Restored the one missing paragraph; both filenames are present exactly. |
| 5 | 217 | `9f5579b959ba6ce1` | `HAL_UART_MspInit`, `MX_USART2_UART_Init` | The complete source paragraph was absent. | A | Same omitted paragraph as item 4. | Yes | Restored the paragraph with `HAL_UART_MspInit()` and `MX_USART2_UART_Init()` unchanged. |
| 6 | 262 | `c3502a05909a09f2` | `/HAL_UART_Receive_DMA` inside `HAL_UART_Trasmit_DMA()/HAL_UART_Receive_DMA()` | `` `HAL_UART_Trasmit_DMA()`/`HAL_UART_Receive_DMA()` `` | C | The function is present exactly; the slash separates two calls. | No | The slash expression is no longer classified as a path. |
| 7 | 289 | `adff42768a02cda5` | `/AHB-prescaler` in a division expression | `HAL_RCC_GetSysClockFreq()/AHB-预分频器` | C | “AHB prescaler” is prose in a frequency formula, not a filesystem path. Translating “prescaler” is correct. | No | The slash expression is no longer classified as a path. |
| 8 | 391 | `57507d61be6f493b` | `HAL_ADC` (register-pattern report) | `¹²HAL_ADC 模块` | C | `HAL_ADC` is present exactly. Unicode superscript `²` defeated the old `\b` boundary. | No | Register matching now uses explicit ASCII identifier boundaries. |
| 9 | 391 | `57507d61be6f493b` | `HAL_ADC` (macro-pattern report) | `¹²HAL_ADC 模块` | C | Same boundary false positive as item 8. | No | Macro matching now uses explicit ASCII identifier boundaries. |
| 10 | 393 | `57507d61be6f493b` | `MX_ADC1_Init()` | `MX_ADC1()` | A | The `_Init` suffix was genuinely lost in prose; fenced code still contained the correct symbol. | Yes | Replaced only the prose occurrence with `MX_ADC1_Init()`. |
| 11 | 396 | `0f207c72b98db88c` | normalized `ADC_OVR_DATA_OVERWRITTEN`; extracted as `ADC_OVR_DATA_- OVERWRITTEN` | `ADC_OVR_DATA_-OVERWRITTEN` | A | PDF line wrapping split the macro, and the translation retained the damaged split rather than reconstructing the identifier. | Yes | Replaced with exact `ADC_OVR_DATA_OVERWRITTEN`. |
| 12 | 396 | `0f207c72b98db88c` | same token, macro-pattern report | `ADC_OVR_DATA_-OVERWRITTEN` | A | Same damaged identifier as item 11, reported by the macro check as well. | Yes | Exact macro is now preserved. |
| 13 | 395 | `0f207c72b98db88c` | `HAL_ADC_Stop_DMA()` | `HAL_ADC_Stop_DMA在…` | A | Parentheses and token boundary were lost; the adjacent `HAL_ADC_Start_DMA()` was also left in extracted split form. | Yes | Corrected the single sentence to contain `HAL_ADC_Stop_DMA()` and `HAL_ADC_Start_DMA()` exactly. |
| 14 | 404 | `63fed76c30799c51` | `/VREF` in `0V /VREF logic levels` | `0V / VREF 逻辑电平` | C | This is mathematical notation for two logic levels, not a path. `VREF` is preserved. | No | The slash expression is excluded from path matching. |
| 15 | 516 | `229665c4449dd792` | `/Power` in `POR)/Power Down Reset` | `POR)/掉电复位 (Power Down Reset, PDR)` | C | The slash joins two reset names; it is not a path, and the English term is retained in parentheses. | No | The slash expression is excluded from path matching. |
| 16 | 607 | `fb4255c914e69555` | `aes_enc_dec()` | `¹⁸aes_enc_dec()` | C | The function is present exactly. The preceding Unicode superscript defeated the old word boundary. | No | Function matching now uses explicit ASCII identifier boundaries. |
| 17 | 622 | `1d323e27d9522c68` | `portable/GCC/ARM_CMO`, `portmarco.h` | `portable/GCC/ARM_CM0`, `portmacro.h` | B | Physical PDF page 622 (printed page 592) visibly spells these as `ARM_CMO` and `portmarco.h`; both are book typos. The diagram also shows `ARM_CMO`. | No | Added exact chunk-and-token equivalences to the standard FreeRTOS names. |
| 18 | 622 | `1d323e27d9522c68` | `ARM_CMO` (register-pattern report) | `ARM_CM0` | B | Same PDF typo as item 17; Cortex-M0 uses digit zero. | No | Exact equivalence applies only to this chunk and token. |
| 19 | 622 | `1d323e27d9522c68` | `ARM_CMO` (macro-pattern report) | `ARM_CM0` | B | Same PDF typo as items 17–18. | No | Exact equivalence applies only to this chunk and token. |
| 20 | 652 | `2b2a9435c7429fb5` | `/vPortFree` inside `pvPortMalloc()/vPortFree()` | `` `pvPortMalloc()`/`vPortFree()` `` | C | Both functions are present exactly; the slash separates alternatives/calls. | No | The slash expression is no longer classified as a path. |
| 21 | 672 | `c0e024d8bbe95fb7` | extracted `UART_IRQ_- Hanler()` | `UART_IRQ_Handler()` | B | Physical PDF page 672 (printed page 642) visibly contains a line-wrapped `UART_IRQ_- Hanler()` typo. The corrected handler name is technically valid. | No | Added an exact equivalence for this chunk and misspelled source token. |
| 22 | 801–803 | `f45a462b5c5e4144` | synthetic `/Dlines` produced from `D+/D- lines` | `D+/D- 线` | C | `D+` and `D-` are USB signal names. Source line-wrap normalization combined `D- lines`, after which the old path regex misread the slash expression. | No | The path matcher now requires a real rooted/multi-component path shape. |

## Changes made

Translation changes were restricted to:

- `work/translated/9f5579b959ba6ce1.md` — restored one omitted prose paragraph on physical page 217.
- `work/translated/57507d61be6f493b.md` — restored `_Init` in one prose occurrence on physical page 393.
- `work/translated/0f207c72b98db88c.md` — repaired three identifiers in prose on physical pages 395–396.

No fenced code block, image reference, page marker, or Markdown heading was changed. The audit rule changes retain the identifier check and consist only of:

- ASCII-aware token boundaries next to Chinese text and superscript footnote markers;
- path shapes that distinguish filesystem paths from slash-separated calls, formulas, units, and USB signals;
- four exact equivalences keyed by chunk and source token for PDF-confirmed book typos.

