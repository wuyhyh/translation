<!-- page: 567 -->

To completely avoid unwanted writings in the Non-Volatile Memory (NVM), the flash memory in all STM32 MCUs is write protected, and there exists a specific unlocking sequence to follow to disable it: two dedicated key registers are provided in the Option Bytes region, which allow to disable flash writing protection by issuing a specific value inside them. In some STM32 MCUs the write protection must be individually disabled for each sector. Depending on the STM32 family, the write access is performed by 8-, 16-, 32- or 64-bit.

To protect the intellectual property, the flash memory can be read-protected against external access from debug interface (clearly, the read access is still permitted from the Cortex-M core and DMA controllers). This avoids other malicious users can save the content of flash memory to disassemble or replicate it on counterfeit devices⁴. We will analyze this topic later.

Depending on the STM32 family, the flash memory can perform several program/erase operations in parallel, allowing to write more bytes at once. Particular conditions must be met to carry out program operations in parallels. Usually, a given VDD voltage is required to reach the maximum parallelism. Always consult the reference manual of your MCU to discover more about this.

## 21.2 The HAL_FLASH Module

Like all other STM32 peripherals, even the flash memory provides several registers used to manipulate its settings, as said before. The HAL_FLASH module, together with the related HAL_FLASHEx

³Several STM32 MCUs from the STM32L-series provide a dedicated and true EEPROM memory, like in other low-cost 8-bit microcontrollers (for example, ATMEL AVR microcontrollers). ⁴However, keep in mind that there exists companies able to bypass read-protection using advanced hardware techniques (this usually involves the usage of lasers that overwrite the read-protection bits inside the Option Bytes region - it is not inexpensive, but it is possible ;-) )

<!-- page: 568 -->

module, allows to easily erase and reprogram the NVM memory without dealing too much with its implementation details. The next subparagraphs introduce the most relevant functions from those modules.

### 21.2.1 Flash Memory Unlocking

The flash memory is write-protected by default, to prevent accidental writings caused by electrical disturbances or program malfunctions. To enable write mode a sequence of operations must be performed, and this is specific of the given STM32 family. To accomplish this task, the CubeHAL provides the function:

```text
HAL_StatusTypeDef HAL_FLASH_Unlock(void);
```

which allows us to completely ignore the specific flash memory architecture. Once the flash memory write/erase protection is disabled, we can perform an erase or write operation. The reverse of the unlock procedure is performed by using the function:

```text
HAL_StatusTypeDef HAL_FLASH_Lock(void);
```

The write protection is automatically set upon a system reset. However, it is strongly suggested to explicitly re-lock the memory when all writing operations are completed. This prevents any accidental writing caused by firmware malfunction or power instability.

### 21.2.2 Flash Memory Erasing

Before we can change the content of a flash memory location, we need to reset its bits to the default value (“0” or “1” depending on the NOR-flash type). This is performed by an erase operation on sector/page granularity. Alternatively, a mass erase of the whole bank can be performed: this means that on those STM32 MCUs providing two banks we can mass erase each bank at a time.

In the majority of STM32 microcontrollers, the individual cells of a flash memory block (sector or page) are set to “1” after an erase operation, with just two notably exceptions: STM32L0 and STM32L1 microcontrollers, whose default value is instead “0”.

The CubeHAL provides two ways to perform a flash erase operation: flash erasing in polling and interrupt mode.

The function:

```text
HAL_StatusTypeDef HAL_FLASHEx_Erase(FLASH_EraseInitTypeDef *pEraseInit,
uint32_t *SectorError);
```

<!-- page: 569 -->

allows to perform a flash erasing in polling mode. It accepts a pointer to an instance of the FLASH_EraseInitTypeDef struct, that we are going to see in a while, and a pointer to variable (SectorError) which returns the id of faulty sectors/pages in case of error during the erasing procedure (for example, if the erasing procedure fails on the 4th page, the SectorError parameter will contain the value 3).

The FLASH_EraseInitTypeDef struct differs a lot between each STM32 family. For this reason, take a look at the stm32XXxx_hal_flash_ex.h file of the CubeHAL for your MCU. Here, we are going to consider the implementation found in CubeHALs for the most performing STM32 MCU like the F2/F4/F7 ones.

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

- TypeErase: specifies if we are performing a mass erase of the whole bank or a sector/page erasing. It can assume the values FLASH_TYPEERASE_SECTORS or FLASH_TYPEERASE_MASSERASE.
- Banks: this parameter, which is available only in those STM32-series providing a multi-bank internal flash memory, specifies the bank involved in a mass-erase. It can assume the values FLASH_BANK_1, FLASH_BANK_2 or FLASH_BANK_BOTH to delete both the banks.
- Sector(Page): this field refers to the sector id involved in a sector-based erasing. It can assume the value FLASH_SECTOR_0, FLASH_SECTOR_1 and so on (the maximum number of sectors depends on the specific microcontroller). In those STM32 MCUs providing a flash memory with page granularity, this fields is replaced by the first address of the page involved in an erasing procedure. Consult the CubeHAL source code for more about this.
- NbSectors(NbPages): the number of sectors (pages) that will be erased starting from the specified Sector.
- VoltageRange: even if we are erasing a whole sector (or page), the erasing procedure cycles over a subset of it (usually two bytes). More performing STM32 MCUs allows to erase multiple bytes at once. This feature is called flash parallelism and it is related to the MCU operating voltage: the higher is VDD, the more bytes are erased at a time⁵. This field can assume a value from Table 21.3. However, always consult the reference manual for your MCU for more about this.

⁵STM32L4-series provides a similar feature named fast program/erase mode. It is related to both the VDD and the clock speed. It allows to erase/program the flash on a double word granularity. Consult the reference manual for your MCU for more about this.

<!-- page: 570 -->

Table 21.3: Program/erase parallelism depending on the voltage range

VoltageRange Voltage range Parallelism

FLASH_VOLTAGE_RANGE_1 1.7 - 2.1 V 8 bits at a time FLASH_VOLTAGE_RANGE_2 2.1 - 2.4 V 16 bits at a time FLASH_VOLTAGE_RANGE_3 2.4 - 3.6 V 32 bits at a time FLASH_VOLTAGE_RANGE_4 2.7 - 3.6 V with External VPP 64 bits at a time

The HAL_FLASHEx_Erase() is a blocking function: it will wait until the erasing procedure has been completed. This may be a quite “long” procedure, depending on the STM32 family, the HCLK speed, the number of sector/pages involved in the erasing and the VDD voltage in those STM32 MCU providing program/erase parallelism. To avoid blocking the firmware activities during this procedure, the HAL provides the function:

```text
HAL_StatusTypeDef HAL_FLASHEx_Erase_IT(FLASH_EraseInitTypeDef *pEraseInit,
uint32_t *SectorError);
```
