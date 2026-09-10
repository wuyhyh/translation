<!-- page: 711 -->

### 24.1.2 Fault Exceptions and Faults Analysis

The fault exception mechanism provided by Cortex-M CPU is useful to detect sources of faults. During the development lifecycle, it is common to have fault conditions, especially if you are new to the STM32 platform or the embedded programming.

This paragraph shows a brief overview of the analysis of fault conditions. It does not aim to replace the official ARM documentation or the excellent work from Joseph Yiu⁷(http://amzn.to/1P5sZwq). Its main goal is to provide the necessary tools and concepts to understanding what’s going wrong when one of the four fault exceptions is raised. Moreover, as we will see later in the chapter, STM32CubeIDE provides a dedicated tool to easily inspect fault-related exceptions and registers to find for the possible fault origin.

Cortex-M3/4/7 cores provide several registers that are used for fault analysis. They may be used by the fault handler code, but in most cases, they are used during a debug session. Table 24.2 lists the available registers useful to fault analysis.

Table 24.2: Registers for fault status and address information

CMSIS Symbol Register name Description

SCB->CFSR Configurable Fault Status Register Provides status information about configurable exceptions (MemFault, BusFault, UsageFault) SCB->HFSR Status for HardFault Provides status information for the HardFault exception SCB->DFSR Debug Fault Status Register Provides status information for the Debug Monitor exception SCB->MMFAR MemManage Fault Address Register If available, shows the address that triggered the MemManage fault SCB->BFAR BusFault Address Register If available, shows the address that triggered the BusFault fault

SCB->CFSR is the Configurable Fault Status Register and it provides information for those exceptions that can be optionally enabled (MemFault, BusFault, UsageFault). It is in turn dived in three subregisters, as shown in Figure 24.6. We are going to provide a complete description of them in the related sub-paragraphs.

![Image from PDF page 711](../images/page-0711-image-01.png)

Figure 24.6: How the SCB->CFSR is further divided in three sub-registers

⁷http://amzn.to/1P5sZwq

<!-- page: 712 -->

#### 24.1.2.1 Memory Management Exception

This exception can be triggered due to a violation of access rules defined by the MPU configuration. For example, it is triggered when trying to access in write mode to a region defined as read only. This exception is available only in Cortex-M3/4/7 cores and it must be enabled. Once enabled, individual bits of the SCB->MFSR register (which corresponds to the first byte of the SCB->CFSR register) can assume the values reported in Table 24.3. The SCB->MFSR register is set to 0x0 upon reset, and its values stay high until a value of 1 is written to the register. By inspecting individual bit values, we can derive more information about the fault cause. For example, if the DACCVIOL bit is set, then an access to a protected memory location caused the exception. In this case the MMARVALID bit is set, the register SCB->MMFAR contains the destination memory location that generated the fault. To see this exception at work, try to execute the example provided in the paragraph about the MPU unit.

Table 24.3: MemManage Fault Status Register (SCB->MFSR)

Bit Name Description 7 MMARVALID Indicates that the content of SCB->MMFAR register is valid 6 RESERVED RESERVED 5 MLSPERR Floating point lazy stacking error (available on Cortex-M4F cores only) 4 MSTKERR Stacking error 3 MUNSTKERR Unstacking error 2 RESERVED RESERVED 1 DACCVIOL Data access violation 0 IACCVIOL Instruction access violation

#### 24.1.2.2 Bus Fault Exception

This exception is mostly raised due to wrong access either to SRAM memory or program memory. The two more frequent sources of Bus Fault exception are a wrong pointer to an illegal SRAM memory region and a bad function pointer. In addition, the bus fault can also occur during stacking and unstacking of the exception handling sequence:

- If the bus error occurred during stack pushing in the exception entrance sequence, it is called a stacking error.
- If the bus error occurred during stack popping in the exception exit sequence, it is called an unstacking error.

Usually, a stacking error indicates a stack overflow: the stack runs out of space and this causes Bus Fault due to an access to an invalid SRAM location. The exception system triggers the fault exception, but the CPU cannot push saved core register on the full stack. This causes a stacking error, which in turn triggers a Hard Fault. By accessing to the SCB->BFSR we can see that both bits 15 and 12 are set. The content of the SCB->BFAR is so valid, and we can see that it contains something equal to 0x1fff bff8. This is an invalid SRAM location in STM32 MCU, and so we can easily derive that a stack overflow happened.

<!-- page: 713 -->

Table 24.4 shows the meaning of individual bits in the SCB->BFSR register.

Table 24.4: Bus Fault Status Register (SCB->BFSR)

Bit Name Description 15 BFARVALID Indicates that the content of SCB->BFAR register is valid 14 RESERVED RESERVED 13 LSPERR Floating point lazy stacking error (available on Cortex-M4F cores only) 12 STKERR Stacking error 11 UNSTKERR Unstacking error 10 IMPRECISERR Imprecise data access error 9 PRECISERR Precise data access error 8 IBUSERR Instruction access error

Bus faults can be classified as:

- Precise bus faults: the fault exceptions happened immediately when the memory access instruction is executed.
- Imprecise bus faults: the fault exceptions happened sometime after the memory access instruction is executed.

The reason for a bus fault to become imprecise is due to the presence of write buffers in the processor bus interface. When the processor writes data to a bufferable address, the processor can proceed to execute the next instruction even if the transfer takes several clock cycles to complete. When an imprecise data access error takes place, the SCB->BFAR register is invalid. To derive the source of fault we need to disassemble the C source code and to identify the assembly instruction that logically precedes the one pointed by the stacked PC.
