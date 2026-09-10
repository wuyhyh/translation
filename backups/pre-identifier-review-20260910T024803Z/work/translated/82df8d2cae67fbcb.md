<!-- page: 567 -->

为了完全避免对非易失性存储器（Non-Volatile Memory, NVM）的意外写入，所有 STM32 微控制器（microcontroller）中的闪存（flash memory）均受写保护，并且存在一个特定的解锁序列以禁用该保护：在选项字节（Option Bytes）区域中提供了两个专用的密钥寄存器（register），通过向其中写入特定值即可禁用闪存写保护。在某些 STM32 微控制器中，必须针对每个扇区单独禁用写保护。根据 STM32 系列的不同，写访问可以是 8 位、16 位、32 位或 64 位。

为了保护知识产权，闪存可以针对来自调试接口的外部访问进行读保护（显然，Cortex-M 内核和 DMA 控制器的读访问仍然是允许的）。这可以防止其他恶意用户保存闪存内容以进行反汇编或在假冒设备上复制⁴。我们稍后将分析此主题。

根据 STM32 系列的不同，闪存可以并行执行多个编程/擦除操作，从而允许一次写入更多字节。要并行执行编程操作，必须满足特定条件。通常，需要达到特定的 VDD 电压才能实现最大并行度。请务必查阅您的微控制器的参考手册以了解更多信息。

## 21.2 HAL_FLASH 模块

正如之前所述，与其他所有 STM32 外设一样，闪存也提供了多个用于操作其设置的寄存器。HAL_FLASH 模块以及相关的 HAL_FLASHEx

³STM32L 系列中的许多 STM32 微控制器提供了专用的真实 EEPROM 存储器，类似于其他低成本 8 位微控制器（例如 ATMEL AVR 微控制器）。⁴然而，请记住，存在一些公司能够使用先进的硬件技术绕过读保护（这通常涉及使用激光重写选项字节区域内的读保护位——这并不便宜，但这是可能的 ;-) ）

<!-- page: 568 -->

模块，允许轻松擦除和重新编程 NVM 存储器，而无需过多关注其实现细节。接下来的小节将介绍这些模块中最相关的函数。

### 21.2.1 闪存解锁

闪存默认处于写保护状态，以防止由电气干扰或程序故障引起的意外写入。要启用写模式，必须执行一系列操作，且这些操作因特定的 STM32 系列而异。为了完成此任务，CubeHAL 提供了以下函数：

```text
HAL_StatusTypeDef HAL_FLASH_Unlock(void);
```

该函数允许我们完全忽略特定的闪存架构。一旦禁用了闪存的写/擦除保护，我们就可以执行擦除或写入操作。解锁操作的逆过程通过以下函数执行：

```text
HAL_StatusTypeDef HAL_FLASH_Lock(void);
```

系统复位时会自动设置写保护。然而，强烈建议在完成所有写入操作后显式地重新锁定存储器。这可以防止因固件故障或电源不稳定导致的任何意外写入。

### 21.2.2 闪存擦除

在更改闪存位置的内容之前，我们需要将其位重置为默认值（根据 NOR 闪存类型不同，默认为“0”或“1”）。这是通过以扇区/页为粒度执行的擦除操作完成的。或者，可以执行整个存储块的批量擦除：这意味着在提供两个存储块的 STM32 微控制器上，我们可以一次批量擦除每个存储块。

在大多数 STM32 微控制器中，擦除操作后，闪存块（扇区或页）中的各个单元被设置为“1”，只有两个明显的例外：STM32L0 和 STM32L1 微控制器，它们的默认值反而是“0”。

CubeHAL 提供了两种执行闪存擦除操作的方法：轮询模式和中断模式下的闪存擦除。

函数：

```text
HAL_StatusTypeDef HAL_FLASHEx_Erase(FLASH_EraseInitTypeDef *pEraseInit,
uint32_t *SectorError);
```

<!-- page: 569 -->

允许以轮询模式执行闪存擦除。它接受一个指向 FLASH_EraseInitTypeDef 结构体实例的指针（我们稍后会看到），以及一个指向变量（SectorError）的指针，该变量在擦除过程中发生错误时返回故障扇区/页的 ID（例如，如果擦除过程在第 4 页失败，SectorError 参数将包含值 3）。

FLASH_EraseInitTypeDef 结构体在不同 STM32 系列之间差异很大。因此，请查看您的微控制器的 CubeHAL 中的 stm32XXxx_hal_flash_ex.h 文件。在这里，我们将考虑在性能最高的 STM32 微控制器（如 F2/F4/F7）的 CubeHAL 中找到的实现。

```text
typedef struct {
uint32_t TypeErase;
/* Mass erase or sector Erase */
uint32_t Banks;
/* Select banks to erase when Mass erase is enabled */
uint32_t Sector;
/* Initial FLASH sector to erase when Mass erase is disabled */
uint32_t NbSectors;
/* Number of sectors to be erased */
uint32_t VoltageRange;/* The device voltage range which defines the erase parallelism */
} FLASH_EraseInitTypeDef;
```

- TypeErase：指定是执行整个存储块的批量擦除还是扇区/页擦除。它可以取 FLASH_TYPEERASE_SECTORS 或 FLASH_TYPEERASE_MASSERASE 的值。
- Banks：此参数仅在提供多存储块内部闪存存储器的 STM32 系列中可用，指定批量擦除中涉及的存储块。它可以取 FLASH_BANK_1、FLASH_BANK_2 或 FLASH_BANK_BOTH 的值以删除两个存储块。
- Sector(Page)：此字段指扇区擦除中涉及的扇区 ID。它可以取 FLASH_SECTOR_0、FLASH_SECTOR_1 等值（最大扇区数取决于特定的微控制器）。在提供页粒度闪存存储器的 STM32 微控制器中，此字段被替换为擦除过程中涉及的页的首地址。有关此功能的更多信息，请查阅 CubeHAL 源代码。
- NbSectors(NbPages)：从指定的 Sector 开始将被擦除的扇区（页）数量。
- VoltageRange：即使我们擦除整个扇区（或页），擦除过程也是针对其子集（通常是两个字节）循环进行的。性能更高的 STM32 微控制器允许一次擦除多个字节。此功能称为闪存并行性，它与微控制器的工作电压有关：VDD 越高，一次擦除的字节数越多⁵。此字段可以取表 21.3 中的值。然而，有关此功能的更多信息，请务必查阅您的微控制器的参考手册。

⁵STM32L4 系列提供了一种名为快速编程/擦除模式的类似功能。它与 VDD 和时钟速度都有关。它允许以双字粒度擦除/编程闪存。有关此功能的更多信息，请查阅您的微控制器的参考手册。

<!-- page: 570 -->

表 21.3：根据电压范围确定的编程/擦除并行度

VoltageRange 电压范围 并行度

FLASH_VOLTAGE_RANGE_1 1.7 - 2.1 V 一次 8 位 FLASH_VOLTAGE_RANGE_2 2.1 - 2.4 V 一次 16 位 FLASH_VOLTAGE_RANGE_3 2.4 - 3.6 V 一次 32 位 FLASH_VOLTAGE_RANGE_4 2.7 - 3.6 V 带外部 VPP 一次 64 位

HAL_FLASHEx_Erase() 是一个阻塞函数：它将等待直到擦除过程完成。根据 STM32 系列、HCLK 速度、擦除中涉及的扇区/页数量以及提供编程/擦除并行性的 STM32 微控制器的 VDD 电压，这可能是一个相当“长”的过程。为了避免在此过程中阻塞固件活动，HAL 提供了以下函数：

```text
HAL_StatusTypeDef HAL_FLASHEx_Erase_IT(FLASH_EraseInitTypeDef *pEraseInit,
uint32_t *SectorError);
```
