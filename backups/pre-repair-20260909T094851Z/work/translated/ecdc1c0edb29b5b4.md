<!-- page: 711 -->

### 24.1.2 故障异常与故障分析

Cortex-M CPU 提供的故障异常机制对于检测故障源非常有用。在开发生命周期中，出现故障状况是很常见的，尤其是对于 STM32 平台或嵌入式编程的新手而言。

本段简要概述了故障状况的分析方法。它并不旨在取代官方的 ARM 文档或 Joseph Yiu⁷(http://amzn.to/1P5sZwq) 的优秀著作。其主要目标是提供必要的工具和概念，以便在四个故障异常之一被触发时，理解发生了什么错误。此外，正如本章后面将要看到的，STM32CubeIDE 提供了一个专用工具，可以轻松检查与故障相关的异常和寄存器，以查找可能的故障根源。

Cortex-M3/4/7 内核提供了几个用于故障分析的寄存器。它们可以被故障处理程序代码使用，但在大多数情况下，它们是在调试会话中使用的。表 24.2 列出了可用于故障分析的可用寄存器。

表 24.2：故障状态和地址信息寄存器

CMSIS 符号 寄存器名称 描述

SCB->CFSR 可配置故障状态寄存器 (Configurable Fault Status Register) 提供关于可配置异常（MemFault、BusFault、UsageFault）的状态信息 SCB->HFSR 硬故障状态 (Status for HardFault) 提供关于硬故障（HardFault）异常的状态信息 SCB->DFSR 调试故障状态寄存器 (Debug Fault Status Register) 提供关于调试监视器（Debug Monitor）异常的状态信息 SCB->MMFAR 内存管理故障地址寄存器 (MemManage Fault Address Register) 如果可用，显示触发内存管理（MemManage）故障的地址 SCB->BFAR 总线故障地址寄存器 (BusFault Address Register) 如果可用，显示触发总线故障（BusFault）故障的地址

SCB->CFSR 是可配置故障状态寄存器，它提供那些可以可选启用的异常（MemFault、BusFault、UsageFault）的信息。它进一步分为三个子寄存器，如图 24.6 所示。我们将在相关的子段落中提供它们的完整描述。

![Image from PDF page 711](../images/page-0711-image-01.png)

图 24.6：SCB->CFSR 如何进一步划分为三个子寄存器

⁷http://amzn.to/1P5sZwq

<!-- page: 712 -->

#### 24.1.2.1 内存管理异常

此异常可能由于违反 MPU 配置定义的访问规则而触发。例如，当尝试以写模式访问被定义为只读的区域时，就会触发此异常。此异常仅在 Cortex-M3/4/7 内核中可用，并且必须启用。一旦启用，SCB->MFSR 寄存器（对应于 SCB->CFSR 寄存器的第一个字节）中的各个位可以取表 24.3 中报告的值。SCB->MFSR 寄存器在复位时被设置为 0x0，其值保持为高电平，直到向该寄存器写入 1。通过检查各个位的值，我们可以推导出更多关于故障原因的信息。例如，如果 DACCVIOL 位被置位，则对受保护内存位置的访问导致了该异常。在这种情况下，MMARVALID 位被置位，寄存器 SCB->MMFAR 包含产生故障的目标内存位置。要查看此异常的工作情况，请尝试执行 MPU 单元段落中提供的示例。

表 24.3：内存管理故障状态寄存器 (SCB->MFSR)

位 名称 描述 7 MMARVALID 指示 SCB->MMFAR 寄存器的内容有效 6 RESERVED 保留 5 MLSPERR 浮点延迟堆栈错误（仅在 Cortex-M4F 内核上可用） 4 MSTKERR 堆栈错误 3 MUNSTKERR 出栈错误 2 RESERVED 保留 1 DACCVIOL 数据访问违规 0 IACCVIOL 指令访问违规

#### 24.1.2.2 总线故障异常

此异常主要是由于对 SRAM 内存或程序内存的错误访问而触发的。总线故障异常的两个最常见来源是指向非法 SRAM 内存区域的错误指针和错误的函数指针。此外，总线故障也可能发生在异常处理序列的堆栈和出栈过程中：

- 如果总线错误发生在异常入口序列的堆栈压入过程中，则称为堆栈错误（stacking error）。
- 如果总线错误发生在异常出口序列的堆栈弹出过程中，则称为出栈错误（unstacking error）。

通常，堆栈错误表示堆栈溢出：堆栈空间耗尽，这导致对无效 SRAM 位置的访问，从而引发总线故障。异常系统触发故障异常，但 CPU 无法将保存的内核寄存器压入已满的堆栈。这导致堆栈错误，进而触发硬故障（Hard Fault）。通过访问 SCB->BFSR，我们可以看到位 15 和位 12 都被置位。SCB->BFAR 的内容因此有效，我们可以看到它包含等于 0x1fff bff8 的值。这是 STM32 MCU 中一个无效的 SRAM 位置，因此我们可以很容易地推导出发生了堆栈溢出。

<!-- page: 713 -->

表 24.4 显示了 SCB->BFSR 寄存器中各个位的含义。

表 24.4：总线故障状态寄存器 (SCB->BFSR)

位 名称 描述 15 BFARVALID 指示 SCB->BFAR 寄存器的内容有效 14 RESERVED 保留 13 LSPERR 浮点延迟堆栈错误（仅在 Cortex-M4F 内核上可用） 12 STKERR 堆栈错误 11 UNSTKERR 出栈错误 10 IMPRECISERR 不精确数据访问错误 9 PRECISERR 精确数据访问错误 8 IBUSERR 指令访问错误

总线故障可以分为：

- 精确总线故障（Precise bus faults）：故障异常在内存访问指令执行时立即发生。
- 不精确总线故障（Imprecise bus faults）：故障异常在内存访问指令执行后的一段时间发生。

总线故障变得不精确的原因是由于处理器总线接口中存在写缓冲区。当处理器向可缓冲地址写入数据时，即使传输需要几个时钟周期才能完成，处理器也可以继续执行下一条指令。当发生不精确数据访问错误时，SCB->BFAR 寄存器无效。为了推导故障源，我们需要反汇编 C 源代码，并识别在逻辑上先于堆栈中 PC 所指向的那条指令的汇编指令。
