<!-- page: 22 -->

# How to Integrate This Book?

This book does not aim to be a full-comprehensive guide to STM32 microcontrollers but is essentially a guide to developing applications using the official ST HAL. It is strongly suggested to integrate it with a book about the ARM Cortex-M architecture, and the series by Joseph Yiu¹ is the best source for every Cortex-M developer.

¹http://amzn.to/1P5sZwq

<!-- page: 23 -->

## How Is the Book Organized?

The book is divided in twenty-eight chapters, and they cover the following topics.

Chapter 1 gives a brief and preliminary introduction to the STM32 platform. It presents the main aspects of these microcontrollers, introducing the reader to the ARM Cortex-M architecture. Moreover, the key features of each STM32 subfamily (L0, F1, etc.) are briefly explained. The chapter also introduces the development board used throughout this book as testing board for the presented topics: the Nucleo.

Chapter 2 shows how to setup the STM32CubeIDE to start developing STM32 applications. The chapter is divided in three different branches, each one explaining the tool-chain setup process for the Windows, Linux and Mac OS X platforms.

Chapter 3 is dedicated to showing how to build the first application for the STM32 Nucleo development board. This is a really simple application, a blinking led, which is with no doubt the Hello World application of hardware.

Chapter 4 is about the STM32CubeMX tool, our main companion every time we need to start a new application based on an STM32 MCUs. The chapter gives a hands-on presentation of the tool, explaining its characteristics and how to configure the MCU peripherals according to the features we need.

Chapter 5 introduces the reader to debugging, showing a brief view of STM32CubeIDE’s debugging capabilities. Finally, the reader is introduced to an important topic: I/O retargeting.

Chapter 6 gives a quick overview of the ST CubeHAL, explaining how peripherals are mapped inside the HAL using handlers to the peripheral memory mapped region. Next, it presents the HAL_GPIO libraries and all the configuration options offered by STM32 GPIOs.

Chapter 7 explains the mechanisms underlying the NVIC controller: the hardware unit integrated in every STM32 MCU which is responsible for the management of exceptions and interrupts. The HAL_NVIC module is introduced extensively, and the differences between Cortex-M0/0+ and Cortex- M3/4/7 are highlighted.

Chapter 8 gives a practical introduction to the HAL_UART module used to program the UART interfaces provided by all STM32 microcontrollers. Moreover, a quick introduction to the difference between UART and USART interfaces is given. Two ways to exchange data between devices using a UART are presented: polling and interrupt oriented modes. Finally we present in a practical way how to use the integrated VCP of every Nucleo board, and how to retarget the printf()/scanf() functions using the Nucleo’s UART.

Chapter 9 talks about the DMA controller, showing the differences between several STM32 families like the more powerful and recent DMAMUX available in STM32L4+/L5/Gx/H7 families. A more detailed overview of the internals of an STM32 MCU is presented, describing the relations between the Cortex-M core, DMA controllers and slave peripherals. Moreover, it shows how to use the HAL_- DMA module in both polling and interrupt modes. Finally, a performance analysis of memory-tomemory transfers is presented.

<!-- page: 24 -->

Chapter 10 introduces the clock tree of an STM32 microcontroller, showing main functional blocks and how to configure them using the HAL_RCC module. Moreover, the CubeMX Clock configuration view is presented, explaining how to change its settings to generate the right clock configuration.

Chapter 11 is a walkthrough into timers, one of the most advanced and highly customizable peripherals implemented in every STM32 microcontroller. The chapter will guide the reader stepby-step through this subject, introducing the most fundamental concepts of basic, general purpose and advanced timers. Moreover, several advanced usage modes (master/slave, external trigger, input capture, output compare, PWM, etc.) are illustrated with practical examples.

Chapter 12 provides an overview of the Analog To Digital (ADC) peripheral. It introduces the reader to the concepts underlying SAR ADCs and then it explains how to program this useful peripheral using the designated CubeHAL module. Moreover, this chapter provides a practical example that shows how to use a hardware timer to drive ADC conversions in DMA mode.

Chapter 13 briefly introduces the Digital To Analog (DAC) peripheral. It provides the most fundamental concepts underlying R-2R DACs and how to program this useful peripheral using the designated CubeHAL module. This chapter also shows an example detailing how to use a hardware timer to drive DAC conversions in DMA mode.

Chapter 14 is dedicated to the I²C bus. The chapter starts introducing the essentials of the I²C protocol, and then it shows the most relevant routines from the CubeHAL to use this peripheral. Moreover, a complete example that explains how to develop I²C slave applications is also shown.

Chapter 15 is dedicated to the SPI bus. The chapter starts introducing the essentials of the SPI specification, and then it shows the most relevant routines from the CubeHAL to use this fundamental peripheral.

Chapter 16 talks about the CRC peripheral, briefly introducing the math behind its calculation, and it shows the related CubeHAL module used to program it.

Chapter 17 is about IWDT and WWDT timers, and it briefly introduces their role and how to use the related CubeHAL modules to program them.

Chapter 18 talks about the RTC peripheral and its main functionalities. The most relevant CubeHAL routines to program the RTC are also shown.

Chapter 19 introduces the reader to the power management capabilities offered by STM32F and STM32L microcontrollers. It starts showing how Cortex-M cores handle low-power modes, introducing WFI and WFE instructions. Then it explains how these modes are implemented in STM32 MCUs. The corresponding HAL_PWR module is also described.

Chapter 20 analyzes the activities involved during the compilation and linking processes, which define the memory layout of an STM32 application. A bare-bone application is shown, and a complete and working linker script is designed from scratch, showing how to organize the STM32 memory space. Moreover, the usage of CCM RAM is presented, as well as other important Cortex-M functionalities like the vector table relocation.

Chapter 21 introduces to the internal flash memory, and its related controller, available in all STM32 microcontrollers. It illustrates how to configure and program this peripheral, showing the

<!-- page: 25 -->

related CubeHAL routines. Moreover, a walk-through of the STM32F7 bus and memory organization introduces the reader to the architecture of these high-performing MCUs.

Chapter 22 describes the operations performed by STM32 microcontrollers at startup. The whole booting process is described, and some advanced techniques (like the vector table relocation in Cortex-M0 microcontrollers) are explained. Moreover, a custom and secure bootloader is shown, which can upgrade the on-board firmware through the USART peripheral. The bootloader uses the AES algorithm to encrypt the firmware.

Chapter 23 is dedicated to the FreeRTOS Real-Time Operating System. It introduces the reader to the most relevant concepts underlying an RTOS and shows how to use the main FreeRTOS functionalities (like threads, semaphores, mutexes, and so on) using the CMSIS-RTOS v2 layer developed by ST on top of the FreeRTOS API. Moreover, some advanced techniques, like the tickless mode in low-power design and the handling of concurrency with C stdlib are shown.
