<!-- page: 56 -->

### 1.3.1 F0

![Image from PDF page 56](../images/page-0056-image-01.png)

Table 1.4: STM32F0 features

The STM32F0 series is the most cost-effective line of MCU from the STM32 portfolio. It is designed to have a street price able to compete with some 8/16-bit MCUs from other vendors, offering a more advanced and powerful platform. The most important features of this series are:

- Core:

- – ARM Cortex-M0 core at a maximum clock rate of 48 MHz. – Cortex-M0 options include the SysTick Timer.
- Memory:

- – Static RAM from 4 to 32 KB. – Flash from 16 to 256 KB. – Each chip has a factory-programmed 96-bit unique device identifier number.
- Peripherals:

– Each F0-series device features a range of peripherals which vary from line to line (see Table 1.4 for a quick overview).

<!-- page: 57 -->

- Oscillator source consists of internal RC (8 MHz, 40 kHz), optional external HSE (4 to 32 MHz), LSE (32.768 to 1000 kHz).
- IC packages: LQFP, TSSOP20¹⁵, UFBGA, UFQFPN, WLCSP (see Table 1.4 for more about this).
- Operating voltage range is 2.0V to 3.6V with the possibility to go down to 1.8V ±8%.

### 1.3.2 F1

![Image from PDF page 57](../images/page-0057-image-01.png)

Table 1.5: STM32F1 features

The STM32F1 series was the first ARM based MCU from ST. Introduced in the market in 2007, it is still the most widespread MCU from the STM32 portfolio. Plenty of development boards are available on the market, produced by ST and other vendors, and you will find tons of examples on the web for F1 microcontrollers. If you are new to the STM32 world, probably the F1 line is the best choice to start working with to learn this platform. The F1-series has evolved over time by increasing speed, size of internal memory, variety of peripherals. There are five F1 lines: Connectivity (STM32F105/107), Performance (STM32F103), USB Access (STM32F102), Access (STM32F101), Value (STM32F100). The most important features of this series are:

- Core:

- – ARM Cortex-M3 core at a maximum clock rate ranging from 24 to 72 MHz.
- Memory:

– Static RAM from 4 to 96 KB. – Flash from 16 to 256 KB. – Each chip has a factory-programmed 96-bit unique device identifier number.

¹⁵F0/G0/L0 are the only STM32 families that provides this convenient package.

<!-- page: 58 -->

- Peripherals:

- – Each F1-series device features a range of peripherals which vary from line to line (see Table 1.5 for a quick overview).
- Oscillator source consists of internal RC (8 MHz, 40 kHz), optional external HSE (4-24MHz(F100), 4-16MHz(F101/2/3), 3-25MHz (F105/7), LSE (32.768 - 1000 kHz) ).
- IC packages: LFBGA, LQFP, UFBGA, UFQFPN, WLCSP (see Table 1.5 for more about this).
- Operating voltage range is 2.0V to 3.6V
- Multiple connectivity options, including Ethernet, CAN and USB 2.0 OTG.

### 1.3.3 F2

![Image from PDF page 58](../images/page-0058-image-01.png)

Table 1.6: STM32F2 features

The STM32F2 series of STM32 microcontrollers is the cost-effective solution in the High-performance segment. It is the most recent and fastest Cortex-M3 based MCU in the STM32 portfolio, with exclusive ARTTM Accelerator from ST. The F2 is pin-to-pin compatible with the STM32 F4series.

The most important features of this series are:

- Core:

- – ARM Cortex-M3 core at a maximum clock rate of 120 MHz.
- Memory:

– Static RAM from 64 to 128 KB.

- * 4 KB battery-backed, 80 bytes battery-backed with tamper-detection erase. – Flash from 128 to 1024 KB. – Each chip has a factory-programmed 96-bit unique device identifier number.
- Peripherals:

- – Each F2-series device features a range of peripherals which vary from line to line (see Table 1.6 for a quick overview).
- Oscillators consist of internal RC (16 MHz, 32 kHz), optional external HSE (1 to 26 MHz), LSE (32.768 to 1000 kHz).
- IC packages: BGA, LQFP, UFBGA, WLCSP (see Table 1.6 for more about this).
- Operating voltage range is 1.8V to 3.6V.

<!-- page: 59 -->

### 1.3.4 F3

![Image from PDF page 59](../images/page-0059-image-01.png)

Table 1.7: STM32F3 features

The STM32F3 it is based on the ARM Cortex-M4F core and it is one of the two families dedicated to mixed-signal application. It is designed to be almost pin-to-pin compatible with the STM32 F1series, even if it does not offer the same variety of peripherals. STM32F3 was the MCU chosen by the developers of the BB-8 droid¹⁶ toy by Sphero¹⁷.

The distinguishing feature for this series is the presence of integrated analog peripherals leading to cost reduction at application level and simplifying application design, including:

- Ultra-fast comparators (25 ns).
- Op-amp with programmable gain.
- 12-bit DACs.
- Ultra-fast 12-bit ADCs with 5 MSPS (Million Samples Per Second) per channel (up to 18 MSPS in Interleaved mode).
- Precise 16-bit sigma-delta ADCs (21 channels).
- 144 MHz Advanced 16-bit pulse-width modulation timer (resolution < 7 ns) for control applications; high resolution timer (217 picoseconds), self-compensated vs power supply and temperature drift.

Another interesting feature of this series is the presence of a Core Coupled Memory (CCM), a specific memory architecture which couples some regions of memory to the CPU core, allowing 0-wait states.

¹⁶http://cnet.co/1M2NyJS ¹⁷http://www.sphero.com/

<!-- page: 60 -->

This can be used to boost time-critical routines, improving performance by up to 40%. For example, OS routines for context switching can be stored in this area to speed up RTOS activities. The most important features of this series are:

![Image from PDF page 60](../images/page-0060-image-01.png)

Figure 1.14: The BB-8 droid made with an STM32F3 MCU

- Core:

- – ARM Cortex-M4F core at a maximum clock rate of 72 MHz.
- Memory:

– Static RAM from 16 to 80 KB general-purpose with hardware parity check.

- * 64 / 128 bytes battery-backed with tamper-detection erase. – Up to 8 KB Core Coupled Memory (CCM) with hardware parity check. – Flash from 32 to 512 KB. – Each chip has a factory-programmed 96-bit unique device identifier number.
- Peripherals:

- – Each F3-series device features a range of peripherals which vary from line to line (see Table 1.7 for a quick overview).
- Oscillators consist of internal RC (8 MHz, 40 kHz), optional external HSE (4 to 32 MHz), LSE (32.768 to 1000 kHz).
- IC packages: LQFP, UFBGA, UFQFPN, WLCSP (see Table 1.7 for more about this). Operating voltage range is 1.8V ±8%. to 3.6V.

<!-- page: 61 -->
