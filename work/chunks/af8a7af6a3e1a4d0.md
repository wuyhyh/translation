<!-- page: 175 -->

- memory access to an invalid location raised the Hard Fault exceptions if the Bus Fault one is not enabled).
- Memory Management Fault¹: it occurs when executing code attempts to access an illegal location or violates a rule of the Memory Protection Unit (MPU). More about this in Chapter 20.
- Bus Fault¹: it occurs when AHB interface receives an error response from a bus slave (also called prefetch abort if it is an instruction fetch, or data abort if it is a data access). Can also be caused by other illegal accesses (e.g., an access to a non-existent SRAM memory location).
- Usage Fault¹: it occurs when there is a program error such as an illegal instruction, alignment problem, or attempt to access a non-existent co-processor.
- SVCCall: this is not a fault condition, and it is raised when the Supervisor Call (SVC) instructions is called. This is used by Real Time Operating Systems to execute instructions in privileged state (a task needing to execute privileged operations executes the SVC instruction, and the OS performs the requested operations - this is the same behavior of a system call in other OSes).
- Debug Monitor¹: this exception is raised when a software debug event occurs while the processor core is in Monitor Debug-Mode. It is also used as exception for debug events like breakpoints and watchpoints when software-based debug solution is used.
- PendSV: this is another exception related to RTOS. Unlike the SVCall exception, which is executed immediately after an SVC instruction is executed, the PendSV can be delayed. This allows the RTOS to complete tasks with higher priorities.
- SysTick: this exception is also usually related to RTOS activities. Every RTOS needs a timer to periodically interrupt the execution of current code and to switch to another task. All STM32 microcontrollers provide a SysTick timer, internal to the Cortex-M core. Even if every other timer may be used to schedule system activities, the presence of a dedicated timer ensures portability among all STM32 families (due to optimization reasons related to the internal die of the MCU, not all timers could be available as external peripheral). Moreover, even if we aren’t using an RTOS in our firmware, it is important to keep in mind that the ST CubeHAL uses the SysTick timer to perform internal time-related activities (and it assumes that the SysTick timer is configured to generate an interrupt every 1ms).

The remaining exceptions that can be defined for a given MCU are related to IRQ handling. Cortex- M0/0+ cores allow up to 32 external interrupts, Cortex-M3/4/7 cores allow silicon manufacturers to define up to 240 interrupts while Cortex-M33 cores up to 480 IRQ lines.

Where can we find the list of usable interrupts for a given STM32 microcontrollers? The datasheet of that MCU is certainly the main source about available interrupts. However, we can simply refer to the vector table provided by ST in its HAL. This table is defined inside the startup file for our MCU, the assembly file ending with .s inside the Core/Startup folder of our project (for example, for an STM32F446RET MCU the file name is startup_stm32f446retx.s). Opening that file, we can find the whole vector table for that MCU, starting about at line 128 (see example in Chapter 4).

¹This exception is not available in Cortex-M0/0+ based microcontrollers.

<!-- page: 176 -->

![Image from PDF page 176](../images/page-0176-image-01.jpeg)

Table 7.1: Cortex-M exception types

Even if the vector table contains the addresses of the handler routines (it is, in fact, an indirect table), the Cortex-M core needs a way to find the vector table in memory. By convention, the vector table starts at the hardware address 0x0000 0000 in all Cortex-M based processors. If our firmware is designed so that the vector table resides in the internal flash memory (a quite common scenario), then the vector table will be placed starting from the 0x0800 0000 address in all STM32 MCUs. However, in Chapter 1 we saw that the 0x0800 0000 address is automatically aliased

<!-- page: 177 -->

to 0x0000 0000 when the CPU boots up².

Figure 7.2 shows how the vector table is organized in memory. The first entry of this array is the address of the Main Stack Pointer (MSP) inside the SRAM. Usually, this address corresponds to the end of the SRAM, that is its base address + its size (more about memory layout of an STM32 application in Chapter 20). Starting from the second entry of this table, we can find all exceptions and interrupts handler. This means that the vector table has a length equal to 48 for Cortex-M0/0+ based microcontrollers and a length equal to 256 for Cortex-M3/4/7.

![Image from PDF page 177](../images/page-0177-image-01.png)

Figure 7.2: The minimal layout of the vector table in an STM32 MCU based on a Cortex-M3/4/7 core

It is important to clarify some things about the vector table.

1. The name of the exception handlers is just a convention, and you are totally free to rename them if you like a different one. They are just symbols (like variables and functions inside a program). However, keep in mind that the CubeMX software is designed to generate ISR with those names, which are an ST convention. So, you have to rename the ISR name too. 2. As said before, the vector table must be placed at the beginning of the flash memory, where the processor expects to find it. This is a GCC Linker job that places the vector table at the beginning of the flash data during the generation of the absolute file, which is the binary file

²Apart from the Cortex-M0, the rest of Cortex-M cores allow to relocate the position in memory of the vector table. Moreover, it is possible to force the MCU to boot up from different memories than the internal flash one. These are advanced topics that will be covered in Chapter 20 about memory layout and another one dedicated to booting process. To avoid confusion in unexperienced readers it is best to consider the vector table position fixed and bound to the 0x0000 0000 address.

<!-- page: 178 -->

we upload to the flash. In Chapter 20 we will study the content of STM32XXxx_FLASH.ld file, which contains the directives to instruct GNU LD about this.
