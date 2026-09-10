# Translation integrity audit

- Generated: 2026-09-10T02:44:38+00:00
- Overall: **FAIL**
- Active chunks: 301
- Physical pages: 910

| Check | Result | Summary |
|---|---|---|
| All source chunks have successful translations | PASS | sources=301/301, outputs=301/301 |
| Final failed count is zero | PASS | failed=0 |
| Physical page coverage | PASS | covered=910/910; explicit blank/anomaly pages=6 |
| Page marker order | PASS | issues=0 |
| Markdown heading count and levels | PASS | issues=0 |
| Image references and files | PASS | issues=0 |
| Code fences paired | PASS | issues=0 |
| Code block contents exact | PASS | issues=0 |
| Technical identifiers preserved | FAIL | issues=22 |
| No reasoning or prompt leakage | PASS | issues=0 |
| No abnormal duplicate paragraphs | PASS | issues=0 |
| No obvious truncation | PASS | issues=0 |
| Extraction anomaly markers inventoried | PASS | markers=6 |
| No long untranslated English body | PASS | issues=0 |

## Details

### All source chunks have successful translations

- No issues found.

### Final failed count is zero

- No issues found.

### Physical page coverage

- No issues found.

### Page marker order

- No issues found.

### Markdown heading count and levels

- No issues found.

### Image references and files

- No issues found.

### Code fences paired

- No issues found.

### Code block contents exact

- No issues found.

### Technical identifiers preserved

- ed78e7d0fc278832 path: /pc
- b3228e67eddf8ea4 path: C:\ST\STM32CubeIDE
- ecad685e479c3d6c path: /scanf
- 9f5579b959ba6ce1 path: main.c, stm32XXxx_hal_msp.c
- 9f5579b959ba6ce1 function: HAL_UART_MspInit, MX_USART2_UART_Init
- c3502a05909a09f2 path: /HAL_UART_Receive_DMA
- adff42768a02cda5 path: /AHB-prescaler
- 57507d61be6f493b register: HAL_ADC
- 57507d61be6f493b macro: HAL_ADC
- 57507d61be6f493b function: MX_ADC1_Init
- 0f207c72b98db88c register: ADC_OVR_DATA_OVERWRITTEN
- 0f207c72b98db88c macro: ADC_OVR_DATA_OVERWRITTEN
- 0f207c72b98db88c function: HAL_ADC_Stop_DMA
- 63fed76c30799c51 path: /VREF
- 229665c4449dd792 path: /Power
- fb4255c914e69555 function: aes_enc_dec
- 1d323e27d9522c68 path: portable/GCC/ARM_CMO, portmarco.h
- 1d323e27d9522c68 register: ARM_CMO
- 1d323e27d9522c68 macro: ARM_CMO
- 2b2a9435c7429fb5 path: /vPortFree
- c0e024d8bbe95fb7 function: UART_IRQ_Hanler
- f45a462b5c5e4144 path: /Dlines

### No reasoning or prompt leakage

- No issues found.

### No abnormal duplicate paragraphs

- No issues found.

### No obvious truncation

- No issues found.

### Extraction anomaly markers inventoried

- 9cd8dd3df2d875dc: [原文提取异常，第1页]
- 33d43fd09190affa: [原文提取异常，第31页]
- bea57f79df33eb9f: [原文提取异常，第159页]
- 64f189dc94cbd576: [原文提取异常，第486页]
- 76f1cc2ee1abd995: [原文提取异常，第830页]
- 55edb2e2dbb32c80: [原文提取异常，第890页]

### No long untranslated English body

- No issues found.
