<!-- page: 703 -->

# 24. 高级调试技术

在第 5 章中，我们开始分析用于调试目标微控制器上运行的固件的基本工具和技术。我们研究了一些重要的 Eclipse
功能，例如断点和单步调试，这些功能有助于理解代码中出了什么问题。然而，这些技术可能不足以调试实际应用。问题可能以多种方式出现，为了更好调试我们的嵌入式应用程序，通常需要专用且往往昂贵的硬件工具。

本章旨在向读者介绍基于 Cortex-M 的微控制器提供的一些高级调试功能。最后，我们将展示 Cortex-M
异常的作用，并说明如何解码内核寄存器，这些寄存器可以提供关于异常源头的有用信息。本章还简要介绍了在 Cortex-M3/4/7 MCU
中实现的串行线查看器（Serial Wire Viewer）功能，这是一种独特的 ARM 技术，允许使用外部调试工具对 MCU 活动进行实时跟踪。

本章不仅限于底层调试技术。我们还将实际查看 STM32CubeIDE 工具链提供的其他一些功能，例如实时表达式（Live Expressions）和 SFR
视图，并分析 CubeHAL 提供的功能，以改进错误管理并优化调试过程。
> **提示**
>
> 在理想情况下，本章应紧跟在第 5 章之后。这里报告的信息对于在早期接触 STM32
> 平台时进行高效调试非常重要。不幸的是，要掌握本章中阐述的概念，需要先学习其他几个主题，才能深入理解这里展示的技术和工具。作为一般规则，作者建议在阅读本章之前，至少阅读第
> 7、20 和 21 章。

## 24.1 理解 Cortex-M 故障相关异常

在这段漫长旅程的开始，我们看到基于 Cortex-M
的微控制器实现了许多系统相关的异常。其中一些是故障相关的，即当正常执行流程中发生错误时触发这些异常。通过为这些故障相关异常实现适当的中断处理程序，我们可以消除故障根源。这在调试期间极其有用，因为它有助于我们将问题与应用程序的其余部分隔离开来。然而，正确的故障处理即使在“生产”固件中也有用：一旦检测到故障，我们可以尝试在重置板卡之前将设备置于安全状态。

Cortex-M3/4/7 内核为程序员提供了四种故障相关异常（见表 7.1）：

<!-- page: 704 -->

- 内存管理故障（Memory Management Fault）
- 总线故障（Bus Fault）
- 使用故障（Usage Fault）
- 硬故障（Hard Fault）

前三种异常在特定故障发生时触发，并且仅在 Cortex-M3/4/7 内核中可用。最后一种，即硬故障异常，是即使在 Cortex-M0/0+
内核中也唯一可用的异常。它也被称为通用故障异常，因为它不能被禁用，并且当其他故障相关异常被禁用时，它充当特定故障条件的收集器。

当引发故障异常时，我们可以通过分析某些“系统寄存器”的内容来尝试推导故障原因。此外，对堆栈跟踪的简单分析至少可以在大多数故障原因中引导我们找到故障条件的根源¹。

什么情况下会产生系统故障？回答这个显而易见的问题并不简单。故障的最常见来源是固件中的错误，尤其是在开发阶段。访问无效的内存位置（通常是由于指针损坏）是故障条件最常见的来源。无效或实现不当的向量表是另一个常见的故障来源。堆栈溢出是另一个相当频繁的故障条件，特别是在运行实时操作系统的低成本
STM32 MCU 中。

有时，故障的起源与软件无关，而可能由外部因素引起，例如：

- 糟糕的 PCB 设计和布局（这比你想象的更常见）。
- 不稳定或质量差的电源（在劣质设计中相当常见）。
- 电气噪声（对于在嘈杂环境中运行的设备尤其如此）。
- 电磁干扰（EMI）或静电放电（ESD）。
- 极端运行环境（例如，温度、湿度等）。
- 某些组件损坏（例如，Flash/EEPROM 器件、晶振、电解电容）。
- 辐射。

诊断上述棘手的故障条件确实很难。这些是任何硬件开发人员都不希望遇到的情况，并且超出了本书的范围。在这里，我们将只关注软件相关的故障以及识别它们的方法。然而，在开始分析触发四种故障相关异常的原因之前，从软件角度分析异常生成的方式是根本性的。这对于识别（或至少尝试识别）导致故障异常的代码非常重要。

¹显然，如果没有实时操作系统内核感知调试，如果我们正在使用实时操作系统，堆栈跟踪很可能会提供误导性的信息。

<!-- page: 705 -->

### 24.1.1 Cortex-M 异常入口序列与 ARM 调用约定

对于高级语言程序员²来说，调用一个例程似乎是一件显而易见的事情。我们只需写下要调用的函数名称，并传递给定数量的参数。就这样结束了。然而，从处理器的角度来看，底层发生的事情需要被规定到最细微的细节，并且必须同时符合处理器架构和编程语言语义。因此，在描述将新例程压入堆栈的过程时，通常会提到调用约定（calling
convention）。

ARM 架构过程调用标准（AAPCS）精确定义了基于 ARM 架构的调用约定。在第 1 章中，我们已经看到，基于 Cortex-M
的微控制器提供了多个内核寄存器，为了方便起见，这些寄存器再次在图 24.1 中展示。并非所有这些内核寄存器在所有 Cortex-M
内核中都可用：例如，FPU 寄存器 S0-S31 仅在启用并使用 FPU 单元时，才在 Cortex-M4F 和 Cortex-M7 内核中可用。

<p align="center"><img src="../images/page-0705-image-01.jpeg" alt="Image from PDF page 705"></p>

<p align="center">图 24.1：Cortex-M CPU 内核寄存器</p>

某些内核寄存器承担特殊角色，因为它们用于处理器运行。R13 是堆栈指针（Stack Pointer，SP），即 SRAM 中指向最近压入栈的条目基址的指针（因此在
STM32 中类似于 `0x2000 XXXX`）。该条目代表给定函数的局部内存区域；在全降序堆栈中，SP 与堆栈的最低地址重合。R14 是链接寄存器（Link
Register，LR），即 Flash³ 中（因此在 STM32 中类似于 `0x0800X XXXX`）调用栈上给定函数的调用指令之后那条指令的地址。

²作为 C 程序员，无论你是否相信，我们都是“高级语言程序员”。³这并不完全正确，因为 CPU 也可以执行放置在 SRAM
以及其他外部存储器中的代码。但在这里将其视为真值是合理的。

<!-- page: 706 -->

R15 是程序计数器（Program Counter，PC），即包含当前汇编指令在 Flash 存储器中地址的寄存器。

R0-R3 寄存器在 ARM 调用约定中扮演着另一个重要角色。它们用于存储传递给被调用函数的前四个参数（从现在开始，我们将使用术语
callee 来表示被调用函数，使用 caller
来表示调用其他函数的函数）。如果被调用函数使用最多四个参数，那么前四个通用寄存器包含这些参数的内容。显然，这里我们假设参数是字对齐的（四字节对齐）。相反，如果我们的函数接受超过四个参数，或者它们的总大小超过十六字节，那么我们需要在被调用函数的堆栈上分配足够的空间来存储其他参数，然后再将控制权传递给被调用函数。这种对
R0-R3 寄存器的使用允许加速调用过程并减少使用的 SRAM 量。最后，R0-R1
寄存器也用于存储函数的返回值。因此，一个好的规则是尽可能将参数数量限制在最多四个。如果不可能，那么你应该尝试将最常访问的参数放在
R0-R3 中（即，将它们定义为前四个函数参数），以便最小化被调用函数中的堆栈访问。

由于一些通用寄存器扮演特定角色，作为被调用函数，我们不能自由地修改它们的内容，但必须遵守以下约定：

- 被调用函数可以自由修改寄存器 R0、R1、R2 和 R3。
    - 这意味着调用方在将控制权传递给被调用函数之前，需要保存它们的内容（如果它们被用于存储对调用方相关的数据）。
- 除非 R0、R1、R2 和 R3 扮演参数的角色，否则被调用函数不能假设它们的内容。
- 被调用函数可以自由修改 LR 寄存器，但在离开函数时需要进入函数时的值（因此该值需要存储在被调用函数的堆栈帧中）。
- 只要在被调用函数离开时恢复其值，被调用函数就可以修改所有剩余的寄存器。这包括 SP 和寄存器
  R4-R11。这意味着，在调用一个函数后，我们必须假设（仅）寄存器 R0-R3、R12 和 LR 已被覆盖。
- 函数不应假设当前程序状态寄存器（CPSR）的内容。
- 如果 FPU 被启用并使用，被调用函数可以自由修改 S0-S15 寄存器，这些寄存器必须由调用方在调用被调用函数之前保存（连同 FPSCR
  寄存器）。相反，被调用函数需要在更改 S16-S31 寄存器的内容之前保存其内容。
- R12 是一个特殊的“暂存寄存器”，由链接器用于执行动态链接。在像 Cortex-M 这样的真正嵌入式微控制器中不太有用，但根据
  AAPCS⁴，它是一个必须由调用方保存的寄存器。

因此，总结一下，从调用方的角度来看，在调用另一个例程之前，我们需要保存以下寄存器的内容：R0-R3、R12、R14、CPSR（如果 FPU 被启用，还包括
S0-S15 和 FPSCR）。这些寄存器在图 24.1 中以红色突出显示。

⁴重要的是要强调，相同的 ARM 调用约定也适用于基于 Cortex-A 的微处理器，它们具有处理与 Linux 和 Windows 等高级操作系统进行动态链接的所有功能。

<!-- page: 707 -->

作为高级语言程序员，我们不需要关心这些规则。确保遵守 AAPCS 规则是编译器的任务。在第 7 章中，我们看到 Cortex-M
内核的一个显著特性是能够使用常规 C 函数作为异常处理程序。这意味着异常处理程序像常规 C 例程一样被“压入”主堆栈。但这意味着，为了允许
C 函数用作异常处理程序，异常机制需要遵守 AAPCS 调用约定的要求，因此需要在异常入口时自动保存图 24.1
中那些“红色”寄存器，并在异常退出时恢复它们，这一切都在处理器的控制下进行。这样，当返回到被中断的程序时，所有寄存器都将具有与中断入口序列开始时相同的值。

此外，由于异常对应于主程序流的打断，并且它可以在任何时候触发，我们需要保存 PC 的内容，否则在异常退出时我们没有办法返回到主流程。在常规函数调用中，PC
的值由分支指令存储在 LR 寄存器中。相反，当异常触发时，返回地址（PC）的值不存储在 LR 中（异常机制在异常入口时在 LR 中放置一个特殊的
EXC_RETURN 代码，用于异常返回 - 我们稍后会分析它），并且返回地址的值也需要由异常序列保存。

因此，在基于 Cortex-M 的微控制器上，在异常处理序列期间总共需要保存八个寄存器：

<p align="center"><img src="../images/page-0707-image-01.png" alt="Image from PDF page 0707"></p>

<p align="center">图 24.2：CPU 在异常入口时如何堆叠内核寄存器</p>

- R0-R3
- R12
- SP

<!-- page: 708 -->

- LR
- CPSR

此外，如果使用 FPU，则需要保存 S0-S15 和 FPSCR 寄存器。

处理器将这些寄存器存储在哪里？显然，它们被存储在堆栈⁵上，位于异常处理程序堆栈帧的起始位置。这个过程被称为压栈（stacking），图
24.2 清晰地展示了这一过程。请注意，在图 24.2 中，内核寄存器的颜色比图 24.1
中使用的颜色更浅。这是因为需要强调，处理器在进入异常序列之前，会将内核寄存器的内容存储在这些位置。当异常触发时，内核寄存器的内容会被更新为与异常上下文相关的数据（例如，PC
将指向异常处理程序的第一条指令，或者 SP 将指向压栈后的内核寄存器之上的 MSP 顶部）。

保存的内核寄存器内容对于评估是什么导致了故障异常可能很有用。例如，如果由于访问无效的内存位置（可能是由于指针损坏）而触发了故障异常，通过检查这些寄存器，我们可以尝试理解非法内存访问发生的位置。因此，问题是：作为高级语言程序员，我们是否有办法访问这些值？当然有！我们只需要一点汇编编程知识。

假设我们想在 EXTI15_10_IRQHandler () 被调用时访问压栈寄存器的内容（这是当 PC13 引脚——连接到 Nucleo 开发板上的蓝色按钮——在大多数
STM32 微控制器上配置为中断模式时调用的 ISR）。我们可以按以下方式定义该 ISR：

```c
 1  void EXTI15_10_IRQHandler(void) {
 2      asm volatile(
 3          " tst lr,#4        \n"
 4          " ite eq           \n"
 5          " mrseq r0,msp     \n"
 6          " mrsne r0,psp     \n"
 7          " mov r1,lr        \n"
 8          " ldr r2,=EXTI15_10_IRQHandler_C \n"
 9          " bx r2"
10      );
11  }
12
13  EXTI15_10_IRQHandler (uint32_t *core_registers, uint32_t lr) {
14      /* core_registers points to the R0-R3, R13, SP and CPSR
15         registers, while the lr argument contains the content
16         of the LR register just before the exception entrance */
17      ....
18  }
```

⁵这里的情况稍微复杂一些。根据实时操作系统（RTOS）的使用情况，可能同时存在“多个”堆栈：主堆栈（Main
Stack）或特定于单个线程的堆栈，称为进程堆栈（Process Stack）。此主题超出了本书的范围。有关更多信息，请参阅 Joseph Yiu 关于
Cortex-M 架构的优秀书籍（http://amzn.to/1P5sZwq）。

<!-- page: 709 -->

上述汇编代码可能看起来难以理解，但它并不是什么黑魔法。`tst` 指令执行 LR 寄存器（当前寄存器，而非存储在堆栈上的那个）的内容与字面量
4 之间的按位比较。如果它们匹配（即 LR 寄存器的第三位被置为 1），则异常进入时使用的是 PSP 堆栈。否则，MSP
是当前使用的堆栈。执行此检查的原因很快就会变得清晰。在这里先接受这一事实。

第 7 行的指令做了一件简单的事情（这是关键部分）：当前 LR 寄存器的内容被放入 R1 寄存器，并调用函数 EXTI15_10_IRQHandler_C ()
（注意末尾的 _C）。这个函数接受两个参数：core_registers 和 lr。根据 AAPCS 规范，core_registers 将与寄存器 R0⁶ 对应，而 lr 将与
R1 的内容对应。当进入异常处理程序时，R0 与当前堆栈（MSP 或 PSP）上存储内核寄存器的起始地址一致。

<p align="center"><img src="../images/page-0709-image-01.png" alt="Image from PDF page 709"></p>

<p align="center">图 24.3：当前 R0-R1 寄存器如何指向压栈寄存器和实际的 LR 寄存器</p>

图 24.3 清楚地解释了这一点。如您所见，`core_registers` 对应于 R0 寄存器，该寄存器保存已压栈寄存器的基地址。`lr` 对应于 R1
寄存器；第 7 行的汇编指令将实际 LR 寄存器的内容写入该寄存器。因此，我们可以从 `EXTI15_10_IRQHandler_C()`
例程中访问已压栈寄存器，并分析其内容，后文将看到这一点。

⁶请注意，core_registers 参数是一个指针，因此 R0 寄存器将包含内核寄存器被保存的内存位置（一个 32 位整数）。

<!-- page: 710 -->

#### 24.1.1.1 如何解释异常进入时 LR 寄存器的内容

在基于 Cortex-M 的处理器中，异常返回机制是使用一个称为 EXC_RETURN 的特殊返回地址触发的。该值在异常进入时生成，并存储在链接寄存器（LR）中。当使用允许的功能返回指令将此值写入
PC 时，它会触发异常返回序列。

EXC_RETURN 地址不对应于实际的 Flash 地址。它可以取六个值，如表 24.1 所列。

**表 24.1：EXC_RETURN 的可能值及其解释**

| EXC_RETURN    | 返回模式     | 返回堆栈 | 启用 FPU | 描述                         |
|---------------|--------------|----------|----------|------------------------------|
| `0xFFFF FFF1` | 0（Handler） | MSP      | 否       | 返回处理程序模式（使用 MSP） |
| `0xFFFF FFF9` | 1（Thread）  | MSP      | 否       | 返回线程模式（使用 MSP）     |
| `0xFFFF FFFD` | 1（Thread）  | PSP      | 否       | 返回线程模式（使用 PSP）     |
| `0xFFFF FFE1` | 0（Handler） | MSP      | 是       | 返回处理程序模式（使用 MSP） |
| `0xFFFF FFE9` | 1（Thread）  | MSP      | 是       | 返回线程模式（使用 MSP）     |
| `0xFFFF FFED` | 1（Thread）  | PSP      | 是       | 返回线程模式（使用 PSP）     |

例如，如果在进入异常之前 CPU 正在运行“常规代码”（即 CPU 处于线程模式），如果使用的堆栈是 MSP，并且 FPU 单元被禁用，那么 LR
寄存器包含的值是 0xFFFF FFF9。相反，如果当前异常进入时 CPU 正在处理另一个异常（可能是一个中断）（即 CPU 处于处理程序模式），那么
LR 寄存器的内容是 0xFFFF FFF1。

正是由于 EXC_RETURN 机制，普通的 C 函数可以被用作异常处理程序，而无需编写任何汇编代码。这与其他微控制器架构不同，后者需要编译器（或开发人员）进行额外的工作来处理异常处理程序的压栈/出栈。

<p align="center"><img src="../images/page-0710-image-01.png" alt="Image from PDF page 710"></p>

<p align="center">图 24.5：EXC_RETURN 值是如何被解释的</p>

图 24.5 展示了 EXC_RETURN 值的完整结构。如您所见，第三位指示故障条件触发时所使用的堆栈。这清楚地解释了之前汇编代码中使用
`tst` 指令检测所用堆栈的原因。

<!-- page: 711 -->

### 24.1.2 故障异常与故障分析

Cortex-M CPU 提供的故障异常机制对于检测故障源非常有用。在开发生命周期中，出现故障状况是很常见的，尤其是对于 STM32
平台或嵌入式编程的新手而言。

本段简要概述了故障状况的分析方法。它并不旨在取代官方的 ARM 文档或 Joseph Yiu⁷ (http://amzn.to/1P5sZwq)
的优秀著作。其主要目标是提供必要的工具和概念，以便在四个故障异常之一被触发时，理解发生了什么错误。此外，正如本章后面将要看到的，STM32CubeIDE
提供了一个专用工具，可以轻松检查与故障相关的异常和寄存器，以查找可能的故障根源。

Cortex-M3/4/7 内核提供了几个用于故障分析的寄存器。它们可以被故障处理程序代码使用，但在大多数情况下，它们是在调试会话中使用的。表
24.2 列出了可用于故障分析的可用寄存器。

**表 24.2：故障状态和地址信息寄存器**

| CMSIS 符号   | 寄存器名称                                                 | 描述                                                         |
|--------------|------------------------------------------------------------|--------------------------------------------------------------|
| `SCB->CFSR`  | 可配置故障状态寄存器（Configurable Fault Status Register） | 提供可配置异常（MemFault、BusFault、UsageFault）的状态信息。 |
| `SCB->HFSR`  | 硬故障状态寄存器（HardFault Status Register）              | 提供硬故障（HardFault）异常的状态信息。                      |
| `SCB->DFSR`  | 调试故障状态寄存器（Debug Fault Status Register）          | 提供调试监视器（Debug Monitor）异常的状态信息。              |
| `SCB->MMFAR` | 内存管理故障地址寄存器（MemManage Fault Address Register） | 如果有效，显示触发内存管理故障（MemManage Fault）的地址。    |
| `SCB->BFAR`  | 总线故障地址寄存器（BusFault Address Register）            | 如果有效，显示触发总线故障（BusFault）的地址。               |

SCB->CFSR 是可配置故障状态寄存器，它提供那些可以可选启用的异常（MemFault、BusFault、UsageFault）的信息。它进一步分为三个子寄存器，如图
24.6 所示。我们将在相关的子段落中提供它们的完整描述。

<p align="center"><img src="../images/page-0711-image-01.png" alt="Image from PDF page 711"></p>

<p align="center">图 24.6：SCB->CFSR 如何进一步划分为三个子寄存器</p>

⁷http://amzn.to/1P5sZwq

<!-- page: 712 -->

#### 24.1.2.1 内存管理异常

此异常可能因违反 MPU 配置所定义的访问规则而触发。例如，尝试以写模式访问被定义为只读的区域时，就会触发此异常。该异常仅在
Cortex-M3/4/7 内核中可用，并且必须显式启用。启用后，`SCB->MFSR` 寄存器（对应于 `SCB->CFSR` 寄存器的第一个字节）中的各位可取表
24.3 所列的值。`SCB->MFSR` 寄存器复位时为 `0x0`；各状态位一旦置位，会保持置位，直到向该寄存器写入
1。通过检查各位的值，我们可以获得更多关于故障原因的信息。例如，若 `DACCVIOL` 位被置位，则对受保护内存位置的访问导致了该异常。在这种情况下，
`MMARVALID` 位被置位，`SCB->MMFAR` 寄存器包含发生故障的目标内存位置。要查看此异常的工作方式，请尝试执行 MPU 单元部分给出的示例。

**表 24.3：内存管理故障状态寄存器（`SCB->MFSR`）**

| 位 | 名称      | 描述                                         |
|----|-----------|----------------------------------------------|
| 7  | MMARVALID | 指示 `SCB->MMFAR` 寄存器的内容有效。         |
| 6  | RESERVED  | 保留。                                       |
| 5  | MLSPERR   | 浮点延迟压栈错误（仅 Cortex-M4F 内核可用）。 |
| 4  | MSTKERR   | 压栈错误。                                   |
| 3  | MUNSTKERR | 出栈错误。                                   |
| 2  | RESERVED  | 保留。                                       |
| 1  | DACCVIOL  | 数据访问违规。                               |
| 0  | IACCVIOL  | 指令访问违规。                               |

#### 24.1.2.2 总线故障异常

此异常主要是由于对 SRAM 内存或程序内存的错误访问而触发的。总线故障异常的两个最常见来源是指向非法 SRAM
内存区域的错误指针和错误的函数指针。此外，总线故障也可能发生在异常处理序列的堆栈和出栈过程中：

- 如果总线错误发生在异常入口序列的压栈过程中，则称为压栈错误（stacking error）。
- 如果总线错误发生在异常出口序列的堆栈弹出过程中，则称为出栈错误（unstacking error）。

通常，堆栈错误表示堆栈溢出：堆栈空间耗尽，这导致对无效 SRAM 位置的访问，从而引发总线故障。异常系统触发故障异常，但 CPU
无法将保存的内核寄存器压入已满的堆栈。这导致堆栈错误，进而触发硬故障（Hard Fault）。通过访问 SCB->BFSR，我们可以看到位 15 和位
12 都被置位。SCB->BFAR 的内容因此有效，我们可以看到它包含等于 0x1fff bff8 的值。这是 STM32 MCU 中一个无效的 SRAM
位置，因此我们可以很容易地推导出发生了堆栈溢出。

<!-- page: 713 -->

表 24.4 显示了 `SCB->BFSR` 寄存器中各位的含义。

**表 24.4：总线故障状态寄存器（`SCB->BFSR`）**

| 位 | 名称        | 描述                                         |
|----|-------------|----------------------------------------------|
| 15 | BFARVALID   | 指示 `SCB->BFAR` 寄存器的内容有效。          |
| 14 | RESERVED    | 保留。                                       |
| 13 | LSPERR      | 浮点延迟压栈错误（仅 Cortex-M4F 内核可用）。 |
| 12 | STKERR      | 压栈错误。                                   |
| 11 | UNSTKERR    | 出栈错误。                                   |
| 10 | IMPRECISERR | 不精确数据访问错误。                         |
| 9  | PRECISERR   | 精确数据访问错误。                           |
| 8  | IBUSERR     | 指令访问错误。                               |

总线故障可以分为：

- 精确总线故障（Precise bus faults）：故障异常在内存访问指令执行时立即发生。
- 不精确总线故障（Imprecise bus faults）：故障异常在内存访问指令执行后的一段时间发生。

总线故障变得不精确的原因是由于处理器总线接口中存在写缓冲区。当处理器向可缓冲地址写入数据时，即使传输需要几个时钟周期才能完成，处理器也可以继续执行下一条指令。当发生不精确数据访问错误时，SCB->
BFAR 寄存器无效。为了推导故障源，我们需要反汇编 C 源代码，并识别在逻辑上先于堆栈中 PC 所指向的那条指令的汇编指令。

#### 24.1.2.3 用法故障异常（Usage Fault Exception）

此异常可能由多种因素引发。在开发 STM32 应用程序时，最常见的原因包括：

- 执行未定义指令（包括在浮点单元被禁用的情况下尝试执行浮点指令）。这通常发生在拥有无效函数指针时，该指针指向一个有效的内存位置（这种情况常发生在某些函数位于
  SRAM 中时），但所指位置的内容并不对应于 ARM 汇编指令。
- 在异常返回序列期间出现无效的 EXC_RETURN 代码。例如，尝试在仍有其他异常处于活动状态（当前正在处理的异常除外）的情况下返回线程模式
  (Thread Mode)。
- 使用多重加载或多重存储指令（包括加载双字和存储双字指令）时发生非对齐内存访问。

<!-- page: 714 -->

- 当 SVC 的优先级级别等于或低于当前级别时，执行 SVC 指令。这种情况可能发生在系统异常的 FreeRTOS 配置出现严重问题时（通常
  SysTick 中断 (IRQ) 没有设置为最低优先级）。

在进行相应配置后，还可以针对以下情况生成用法故障：

- 除以零。
- 所有非对齐内存访问。

表 24.5 展示了 `SCB->UFSR` 寄存器中各位的含义。

**表 24.5：用法故障状态寄存器（`SCB->UFSR`）**

| 位    | 名称       | 描述                                                       |
|-------|------------|------------------------------------------------------------|
| 31–26 | RESERVED   | 保留。                                                     |
| 25    | DIVBYZERO  | 指示除以零错误（仅在启用时才能置位）。                     |
| 24    | UNALIGNED  | 指示发生非对齐访问错误。                                   |
| 23–20 | RESERVED   | 保留。                                                     |
| 19    | NOCP       | 在 Cortex-M4F 浮点单元不可用或未启用时，尝试执行浮点指令。 |
| 18    | INVPC      | 尝试使用 EXC_RETURN 值中的错误值进行异常返回。             |
| 17    | INVSTATE   | 尝试切换到无效状态（例如从 ARM 切换到 Thumb）。            |
| 16    | UNDEFINSTR | 尝试执行未定义指令。                                       |

默认情况下，基于 Cortex-M 的微控制器 (MCU) 在将数字除以零时返回值为 0。如果需要捕获除以零错误，则可以通过设置 SCB->CCR
寄存器中的 DIV_0_TRP 位来启用此错误条件：

```c
SCB->CCR |= SCB_CCR_DIV_0_TRP_Msk;
```

非对齐内存访问的情况也类似：

```c
SCB->CCR |= SCB_CCR_UNALIGN_TRP_Msk;
```

#### 24.1.2.4 硬故障异常（Hard Fault Exception）

如果未启用前述可配置异常，此异常通常由这些异常升级而来。此外，硬故障（HardFault）还可能由以下原因触发：

- 在获取向量表期间接收到总线错误。这发生是因为向量表无效（大多数情况下是我们忘记包含由 STM 提供的汇编文件）。
- 在连接调试器的情况下执行断点指令 (asm ("BKPT #0");)。

表 24.6 展示了 `SCB->HFSR` 寄存器中各位的含义。

<!-- page: 715 -->

**表 24.6：硬故障状态寄存器（`SCB->HFSR`）**

| 位   | 名称     | 描述                                                                                                                                |
|------|----------|-------------------------------------------------------------------------------------------------------------------------------------|
| 31   | DEBUGEVT | 指示硬故障由调试事件触发。                                                                                                          |
| 30   | FORCED   | 指示硬故障由禁用状态下升级的可配置故障异常引起。此时需要检查 `SCB->MFSR`、`SCB->BFSR` 和 `SCB->UFSR` 寄存器的内容，以推导故障原因。 |
| 29–2 | RESERVED | 保留。                                                                                                                              |
| 1    | VECTBL   | 指示硬故障由取向量表失败引起。                                                                                                      |
| 0    | RESERVED | 保留。                                                                                                                              |

#### 24.1.2.5 安全故障异常（Secure Fault Exception）

安全故障异常（SecureFault）仅在 Cortex-M33 内核中可用。该异常由执行的各种安全检查触发。例如，从非安全代码跳转到未标记为有效入口点的安全代码地址时，就会触发该异常。通常，固件将
SecureFault 视为终止条件：要么停止系统，要么重启系统。必须仔细审查对 SecureFault
的任何其他处理，以确保不会无意中引入安全漏洞。安全故障始终针对安全状态；安全状态是系统复位后的默认内核状态。这意味着
SecureFault 异常默认启用。

安全故障状态寄存器（SFSR）提供有关安全相关故障的信息。由于本书不涵盖 Cortex-M33 内核，因此不会在此深入讨论。更多信息请参阅官方
STM 文档⁸。

#### 24.1.2.6 启用可选错误处理器

内存管理故障（Memory Fault）、总线故障（Bus Fault）和用法故障（Usage Fault）默认均处于禁用状态。`HAL_NVIC_EnableIRQ()` 或
`NVIC_EnableIRQ()` 都无法启用这些异常；必须设置 `SCB->SHCSR` 寄存器的第 16、17 和 18 位。要启用内存管理故障异常，请使用以下指令：

```c
SCB->SHCSR |= SCB_SHCSR_MEMFAULTENA_Msk; //Set bit 16
```

要启用总线故障异常，请使用以下指令：

```c
SCB->SHCSR |= SCB_SHCSR_BUSFAULTENA_Msk; //Set bit 17
```

要启用用法故障异常，请使用以下指令：

⁸https://bit.ly/3o8mkJw

<!-- page: 716 -->

```c
SCB->SHCSR |= SCB_SHCSR_USGFAULTENA_Msk; //Set bit 18
```

一旦启用其中任何一个异常，我们就可以像其他可配置异常一样，使用 HAL_NVIC_SetPriority () 来配置其优先级。

#### 24.1.2.7 基于 Cortex-M0/0+ 处理器的故障分析

Cortex-M0/0+ 内核不提供内存管理故障（Memory Fault）、总线故障（Bus Fault）和用法故障（Usage Fault）异常，相应的状态寄存器也不可用。这意味着我们不具备
Cortex-M3/4/7 内核所提供的同等诊断能力。

分析已压栈寄存器（stacked registers）是我们可用于诊断故障原因的唯一相关技术。Joseph Yiu 在 ARM
官方论坛上的这篇回答⁹提供了更多有用的细节。其他技术，例如用哨兵值（sentinel value）填充 SRAM 以检测堆栈溢出，可能有助于您定位代码中的故障根源。

## 24.2 STM32CubeIDE 高级调试功能

在第 5 章中，我们开始分析 STM32CubeIDE 工具链提供的调试功能。我们已经熟悉了断点插入和单步调试等最基本的功能。现在是时候查看官方
STM 开发环境中集成的其他调试功能了。

此处展示的所有功能均可通过调试（Debugging）透视图访问。

### 24.2.1 表达式和实时表达式

表达式（Expressions）视图功能强大，可在调试期间访问内存地址、变量和其他数据结构的内容。此外，它还能够执行函数调用，从而评估给定例程的结果。必须通过“窗口 ->
显示视图 -> 表达式”（Window -> Show View -> Expressions）显式启用表达式视图。

⁹http://bit.ly/2deDjUB

<!-- page: 717 -->

<p align="center"><img src="../images/page-0717-image-01.jpeg" alt="Image from PDF page 717"></p>

<p align="center">图 24.7：调试透视图中的表达式视图</p>

图 24.7 展示了若干表达式示例。`pxCurrentTCB` 是 FreeRTOS 中准备停止的任务的当前线程控制块（Thread Control Block，TCB）。如图
24.7 所示，只需在表达式视图中输入变量名，即可访问它在代码中定义位置的内容。还可以使用 `variable@len` 表达式将 C 指针显示为数组，其中
`variable` 为指针名称，`len` 为数组中显示的数据量。

图 24.7 还展示了如何调用函数（本例为 `HAL_GetTick()`
）并取得其结果¹⁰。表达式还可包含算术运算。最后，表达式视图也能访问单个内存位置的内容，并将其转换为指定数据类型（右键单击表达式行即可将变量转换为其他数据类型）。

近期 Eclipse CDT 版本中的表达式视图接受增强表达式（enhanced
expressions）。增强表达式是一种轻松编写表达式模式的方法，该模式会自动扩展为更大的子表达式子集。可以使用四种类型的增强表达式：

- 模式匹配局部变量
- 模式匹配寄存器
- 模式匹配数组元素
- 表达式组

例如，模式 “= *” 允许显示当前堆栈帧中的所有局部变量，而模式 “=$*” 显示内核寄存器。有关增强表达式的更多信息，请参阅 Eclipse
CDT 文档¹¹。

实时表达式（Live Expressions）视图是 STM32CubeIDE
的一个独特视图，其工作方式与表达式视图非常相似，不同之处在于所有表达式都在调试执行期间实时采样。采样速度由被采样的表达式数量决定。被采样的表达式数量增加会导致采样率变慢。

¹⁰显然，该函数必须包含在二进制映像中，即它必须是固件代码中使用的函数。 ¹¹https://bit.ly/2cRC6ra

<!-- page: 718 -->

#### 24.2.1.1 内存监视器

STM32CubeIDE 允许访问整个 4GB 地址空间的内容。您可以使用内存（Memory）视图访问内存位置的内容。要显示该视图，请前往 Window->
Show View->Memory。内存视图允许您监视和修改 MCU 内存。地址空间以所谓的内存监视器（memory monitors）列表形式呈现。每个监视器代表由称为基地址（base
address）的位置指定的内存段。

<p align="center"><img src="../images/page-0718-image-01.jpeg" alt="Image from PDF page 718"></p>

<p align="center">图 24.8：内存监视器视图</p>

显示该视图后，您可以单击图 24.8 中显示的绿色加号，向监视器视图添加新的内存位置。下一步是选择一个“渲染器”（renderer），即显示内存位置内容的方式。您可以选择以下选项：

- 浮点数（Floating Point）
- 传统（Traditional）
- 十六进制（Hexadecimal）
- ASCII
- 有符号和无符号整数（Signed and unsigned integer）

您还可以为同一内存位置添加更多渲染器。最后，您可以通过右键单击内存单元格来配置内存视图的多个选项（单元格大小、字节序、内存格式等）。

<p align="center"><img src="../images/page-0718-image-02.jpeg" alt="Image from PDF page 718"></p>

<p align="center">图 24.9：使用十六进制和传统渲染器显示的内存位置</p>

<!-- page: 719 -->

### 24.2.2 观察点 (Watchpoints)

每个基于 Cortex-M 的处理器都提供一定数量的断点 (breakpoints) 和观察点 (watchpoints)（参见表
24.7）。断点用于在特定指令处中断执行，而观察点用于在访问特定数据位置时中断执行。任何数据或外设地址都可以被标记为被监视变量，对该地址的访问会生成一个调试事件，从而暂停程序执行。观察点还可以用于仅在特定表达式匹配时暂停执行。

**表 24.7：Cortex-M 内核中可用的断点/观察点**

| Cortex-M  | 断点 | 观察点 |
|-----------|-----:|-------:|
| M0/0+     |    4 |      2 |
| M3/4/7/33 |    6 |      4 |

在 Eclipse CDT 工具链 中有几种添加观察点的方法。例如，您可以在“变量”视图中右键单击一个变量，然后选择“添加观察点 (C/C++)
”条目。同样，也可以在“表达式”视图和“内存监视器”视图中，通过右键单击内存位置来执行此操作。

<p align="center"><img src="../images/page-0719-image-01.jpeg" alt="Image from PDF page 719"></p>

<p align="center">图 24.10：观察点配置视图</p>

单击“添加观察点 (C/C++)”条目后，将出现观察点配置视图，如图 24.10 所示。在这里，我们可以设置从第一个字 (word) 开始要监视的内存量（Range
字段）。此外，我们可以指定是否希望在该内存位置以读 (Read) 或写 (Write) 模式被访问时暂停执行。Enable
字段允许启用/禁用观察点。最后，Condition 字段允许指定一个条件。观察点列在“断点”视图中。

<!-- page: 720 -->

### 24.2.3 指令单步模式 (Instruction Stepping Mode)

指令单步模式是一种调试模式，允许对给定 C 指令“底层”的 ARM 汇编指令进行逐步调试。

<p align="center"><img src="../images/page-0720-image-01.jpeg" alt="Image from PDF page 720"></p>

<p align="center">图 24.11：Eclipse 工具栏上的指令单步模式图标</p>

通过单击 Eclipse 主工具栏上的相关图标来启用指令单步模式，如图 24.11 所示。启用后，将出现反汇编 (Disassembly) 视图，如图
24.12 所示。Eclipse 将自动显示与当前 C 指令对应的 ARM 汇编指令。

> **仔细阅读**
>
> 指令单步模式会显著减慢调试过程，因为 CPU 会在每条汇编指令处暂停。如果您无法理解为什么调试如此缓慢，那么您可能忘记了反汇编视图处于活动状态。

<p align="center"><img src="../images/page-0720-image-03.jpeg" alt="Image from PDF page 720"></p>

<p align="center">图 24.12：反汇编视图</p>

### 24.2.4 SFR 视图

特殊功能寄存器（Special Function Registers，SFR）视图（如图 24.13 所示）允许访问 Cortex-M 内核寄存器，以及特定 STM32
器件的所有专用寄存器。双击寄存器值或相应位域的表示，即可修改寄存器内容。调试项目时，寄存器和位域会填入从目标读取的值。

SFR
视图顶部包含搜索字段，用于筛选外设、寄存器和位域等可见节点。输入文本后，只显示包含该文本的节点。视图底部的信息窗格显示所选行的详细信息。对于寄存器和位域，这包括 [Access]
与 [Read action] 信息。[Access] 包含以下详情：

<!-- page: 721 -->

- RO（只读）
- WO（只写）
- RW（读写）
- W1（写一次）
- RW1（读/写一次）

工具栏按钮位于 SFR 视图右上角。工具栏中的 [RD] 按钮用于强制读取所选寄存器；即使该寄存器或其中的某些位域在 SVD 文件中设置了
`ReadAction` 属性，按下该按钮仍会读取该寄存器。通过 [RD]
按钮读取寄存器时，视图中所有其他可见寄存器也会重新读取，以反映寄存器的全部更新。读取寄存器前必须暂停程序。基数格式按钮（[X16]、[X10]、[X2]
）用于更改寄存器的显示基数。

<p align="center"><img src="../images/page-0721-image-01.jpeg" alt="Image from PDF page 721"></p>

<p align="center">图 24.13：调试透视图中的寄存器视图</p>

### 24.2.5 故障分析器 (Fault Analyzer)

STM32CubeIDE 提供了一个用于简化调试过程的工具：故障分析器（见图 24.14）。故障分析器会解释从 Cortex-M
故障相关异常和寄存器中提取的信息，以识别导致故障的条件。发生故障时，

<!-- page: 722 -->

调试器会显示发生故障的代码行。该视图显示故障状态的原因。故障分为硬故障（Hard Fault）、总线故障（Bus Fault）、用法故障（Usage
Fault）和内存管理故障（Memory Fault）。

为了进一步协助故障分析，异常堆栈帧可视化选项提供了崩溃时 MCU 寄存器值的快照。如果未显示，可以通过转到 Window->Show View->
Fault Analyzer 在调试器透视图中启用故障分析器视图。

故障分析器视图的右上部分包含一个工具栏（参见图 24.14 中的红框）：

- 第一个工具栏按钮（左侧）使用堆栈中 PC 和 LR 寄存器的信息，以及被调试 ELF 文件中的符号信息，在故障位置的返回地址处打开编辑器。
- 第二个工具栏按钮（中间）使用堆栈中 PC 和 LR 寄存器的信息，以及被调试 ELF 文件中的符号信息，在故障位置的返回地址处打开反汇编视图。
- 第三个工具栏按钮（右侧）选择使用编辑器或反汇编视图打开故障位置时采用 PC 还是 LR 寄存器。

<p align="center"><img src="../images/page-0722-image-01.jpeg" alt="Image from PDF page 722"></p>

<p align="center">图 24.14：故障分析器视图</p>

<!-- page: 723 -->

#### 24.2.5.1 在没有 IDE 支持的情况下追踪故障相关寄存器

经常会出现这种情况：目标设备在非调试会话期间发生故障，而调试探针并未连接到设备。在这种不利情况下，了解故障状态和已压栈寄存器（stacked
registers）的状态会非常有帮助。

我们可以为故障相关异常（硬故障、内存管理故障、总线故障和用法故障）定义处理程序，以便通过首选输出方式（UART、USB、ITM
等）轻松打印已压栈寄存器，具体方法如下。故障相关寄存器在 Cortex-M0/0+（ARMv6-M 架构）与 Cortex-M3/4/7（Cortex-M7 使用 ARMv7-M
和 ARMv7E-M）之间存在差异，因此分别进行说明。

**Cortex-M0/0+ – ARMv6-M**

转储过程使用了前文讨论 Cortex-M 内核在异常触发时执行压栈操作所采用的相同技术。通过重新定义系统调用
`int _write(int file, char *ptr, int len)`，我们可以将输出重定向到所需的物理介质。

```c
 1  typedef struct {
 2      uint32_t r0;
 3      uint32_t r1;
 4      uint32_t r2;
 5      uint32_t r3;
 6      uint32_t r12;
 7      uint32_t lr;
 8      uint32_t pc;
 9      uint32_t psr;
10  } ExceptionStackFrame;
11
12  void dumpExceptionStack (ExceptionStackFrame* frame, uint32_t lr) {
13      printf ("Stack frame:\r\n");
14      printf (" R0 =  %08X\r\n", frame->r0);
15      printf (" R1 =  %08X\r\n", frame->r1);
16      printf (" R2 =  %08X\r\n", frame->r2);
17      printf (" R3 =  %08X\r\n", frame->r3);
18      printf (" R12 = %08X\r\n", frame->r12);
19      printf (" LR =  %08X\r\n", frame->lr);
20      printf (" PC =  %08X\r\n", frame->pc);
21      printf (" PSR = %08X\r\n", frame->psr);
22      printf ("Misc\r\n");
23      printf (" LR/EXC_RETURN= %08X\r\n", lr);
24  }
25
26  void HardFault_Handler (void) {
27      asm volatile(
28          " movs r0,#4       \r\n"
29          " mov r1,lr        \r\n"
30          " tst r0,r1        \r\n"
31          " beq 1f           \r\n"
32          " mrs r0,psp       \r\n"
33          " b   2f           \r\n"
34          "1:                \r\n"
35          " mrs r0,msp       \r\n"
36          "2:"
37          " mov r1,lr        \r\n"
38          " ldr r2,=HardFault_Handler_C \r\n"
39          " bx r2"
40
41      : /* Outputs */
42      : /* Inputs */
43      : /* Clobbers */
44      );
45  }
46
47  void HardFault_Handler_C (ExceptionStackFrame* frame __attribute__((unused)),
48                            uint32_t lr __attribute__((unused))) {
49      printf ("[HardFault]\r\n");
50      dumpExceptionStack (frame, lr);
51
52  #if defined(DEBUG)
53      __DEBUG_BKPT();
54  #endif
55      while (1);
56  }
```

**Cortex-M3/4/7 – ARMv7-M/ARMv7E-M**

转储过程使用了前文讨论 Cortex-M 内核在异常触发时执行压栈操作时所采用的相同技术。通过重新定义系统调用
`int _write(int file, char *ptr, int len)`，我们可以将输出重定向到所需的物理介质。

```c
 1  typedef struct {
 2      uint32_t r0;
 3      uint32_t r1;
 4      uint32_t r2;
 5      uint32_t r3;
 6      uint32_t r12;
 7      uint32_t lr;
 8      uint32_t pc;
 9      uint32_t psr;
10  #if defined(__ARM_ARCH_7EM__)
11      uint32_t s[16];
12  #endif
13  } ExceptionStackFrame;
14
15  void dumpExceptionStack (ExceptionStackFrame* frame, uint32_t cfsr,
16                           uint32_t mmfar, uint32_t bfar, uint32_t lr) {
17      printf ("Stack frame:\r\n");
18      printf (" R0 =  %08X\r\n", frame->r0);
19      printf (" R1 =  %08X\r\n", frame->r1);
20      printf (" R2 =  %08X\r\n", frame->r2);
21      printf (" R3 =  %08X\r\n", frame->r3);
22      printf (" R12 = %08X\r\n", frame->r12);
23      printf (" LR =  %08X\r\n", frame->lr);
24      printf (" PC =  %08X\r\n", frame->pc);
25      printf (" PSR = %08X\r\n", frame->psr);
26      printf ("FSR/FAR:\r\n");
27      printf (" CFSR =  %08X\r\n", cfsr);
28      printf (" HFSR =  %08X\r\n", SCB->HFSR);
29      printf (" DFSR =  %08X\r\n", SCB->DFSR);
30      printf (" AFSR =  %08X\r\n", SCB->AFSR);
31
32      if (cfsr & (1UL << 7)) {
33          printf (" MMFAR = %08X\r\n", mmfar);
34      }
35      if (cfsr & (1UL << 15)) {
36          printf (" BFAR =  %08X\r\n", bfar);
37      }
38      printf ("Misc\r\n");
39      printf (" LR/EXC_RETURN= %08X\r\n", lr);
40  }
41
42  void HardFault_Handler (void) {
43      asm volatile(
44          " tst lr,#4        \r\n"
45          " ite eq           \r\n"
46          " mrseq r0,msp     \r\n"
47          " mrsne r0,psp     \r\n"
48          " mov r1,lr        \r\n"
49          " ldr r2,=HardFault_Handler_C \r\n"
50          " bx r2"
51
52      : /* Outputs */
53      : /* Inputs */
54      : /* Clobbers */
55      );
56  }
57
58  void HardFault_Handler_C (ExceptionStackFrame* frame __attribute__((unused)),
59                            uint32_t lr __attribute__((unused))) {
60      uint32_t mmfar = SCB->MMFAR; // MemManage Fault Address
61      uint32_t bfar = SCB->BFAR;   // Bus Fault Address
62      uint32_t cfsr = SCB->CFSR;   // Configurable Fault Status Registers
63
64      printf ("[HardFault]\r\n");
65      dumpExceptionStack (frame, cfsr, mmfar, bfar, lr);
66
67  #if defined(DEBUG)
68      __DEBUG_BKPT();
69  #endif
70      while (1);
71  }
```

### 24.2.6 构建分析器 (Build Analyzer)

构建分析器功能详细解释二进制 ELF 文件中的程序信息，并在“窗口 -> 显示视图 -> 构建分析器”中提供的专用视图中呈现这些信息。如果在与
ELF 文件相同的文件夹中找到与 ELF 文件同名的 .map 文件，则也会使用 .map 文件中的信息，从而可以呈现更多的信息。

构建分析器视图对于优化或简化程序非常有用。该视图包含两个选项卡：内存区域 (Memory Regions) 和内存详细信息 (Memory Details)：

<p align="center"><img src="../images/page-0726-image-01.jpeg" alt="Image from PDF page 726"></p>

<p align="center">图 24.15：构建分析器视图中的内存区域选项卡</p>

- 如果 ELF 文件包含相应的 .map 文件，内存区域选项卡将填充数据。当 .map
  文件可用时，此选项卡可视为内存区域的摘要，包含区域名称、起始地址和大小等信息。大小信息还包括区域的总大小、空闲和已使用部分，以及使用百分比。
- 内存详细信息选项卡（见图 24.16）包含基于 ELF
  文件的详细程序信息。不同的链接器节名称以地址和大小信息呈现。每个节都可以展开和折叠。当展开一个节时，会列出该节中的函数/数据。每个呈现的函数/数据都包含地址和大小信息。

<!-- page: 727 -->

<p align="center"><img src="../images/page-0727-image-01.jpeg" alt="Image from PDF page 727"></p>

<p align="center">图 24.16：构建分析器视图中的内存详细信息选项卡</p>

可以通过点击列名来更改内存详细信息选项卡中列的排序顺序。通过在搜索字段中输入字符串，可以过滤内存详细信息选项卡中的信息。该视图提供了一个便捷的功能。可以通过在视图中选择内存详细信息选项卡中的多行来计算这些行大小的总和。所选内容的总和显示在视图中的名称列上方，如图
24.16 所示。可以通过选择要复制的行并输入 Ctrl+C（或在 Mac 上输入 CMD+C），将内存详细信息选项卡中的数据以 CSV 格式复制到其他应用程序。

### 24.2.7 静态堆栈分析器 (Static Stack Analyzer)

静态堆栈分析器功能根据已构建的程序计算堆栈使用情况。它详细分析由 GCC 从给定的 .c 文件生成的每个 .su 文件以及 ELF
文件，并在视图中呈现结果信息。可以通过前往“窗口 -> 显示视图 -> 静态堆栈分析器”来启用该视图。该视图包含两个选项卡：列表
(List) 和调用图 (Call Graph) 选项卡。

<p align="center"><img src="../images/page-0727-image-02.jpeg" alt="Image from PDF page 727"></p>

<p align="center">图 24.17：静态堆栈分析器视图中的列表选项卡</p>

- 列表选项卡（见图 24.17）包含所选程序中所有函数的列表。使用“隐藏死代码”选择项来启用或禁用死代码函数（即因运行时未使用而被链接器丢弃的函数）的列表显示。如果使用，过滤字段将限制显示为包含其字符的匹配函数。

<!-- page: 728 -->

- 调用图选项卡（见图 24.18）以树视图形式包含详细的程序信息。程序中每个未被其他函数调用的函数都显示在顶层。可以展开树以查看被调用的函数。只有
  ELF 文件中可用的函数才能在该选项卡中可见。当使用时，“搜索…”按钮会触发显示与搜索字段中字符匹配的函数。根据复选框“区分大小写”的选择，搜索可以是区分大小写或不区分大小写。函数名称左侧的小图标（在“函数”列中）表示以下含义：

- 绿色圆点：该函数使用静态堆栈分配（固定堆栈）。
- 蓝色方块：该函数使用动态堆栈分配（取决于运行时）。
- `010` 图标：堆栈信息未知时使用；库函数或汇编函数可能出现这种情况。
- 圆圈中的三个箭头：函数递归调用时，在调用图选项卡中使用。

<p align="center"><img src="../images/page-0728-image-01.jpeg" alt="Image from PDF page 728"></p>

<p align="center">图 24.18：静态堆栈分析器视图中的调用图选项卡</p>

## 24.3 串行线查看器（Serial Wire Viewer，SWV）跟踪

基于 Cortex-M 的微控制器在同一芯片中集成了多种调试与跟踪技术。JTAG 和 SWD 是两种互补规范，可将外部调试器连接到目标微控制器；同一接口也可实现跟踪功能。跟踪可实时导出
CPU 执行期间的内部活动，是一种使用 JTAG 端口 5 个信号的实时硬件调试方式。嵌入式跟踪宏单元（Embedded Trace
Macrocell，ETM）技术实现了这种跟踪，但需要更快、更先进的调试器。ETM 跟踪是一种不会影响微控制器性能的“嗅探”技术。

<!-- page: 729 -->

> **提示：JTAG 与 SWD 接口的区别**
>
> 初学者往往会对这两种调试标准感到困惑，而 STM32 微控制器同时支持二者。联合测试行动组（Joint Test Action
> Group，JTAG）是一项定义信号特性和数据协议的标准。它基于五个信号，另加两根用于检测目标 VDD 电压和 GND 的导线。JTAG
> 可将外部调试探针连接到微控制器，是电子行业广泛采用的标准。
>
> 串行线调试（Serial Wire Debug，SWD）是一种替代的 ARM 专有两针电气接口，使用相同的 JTAG 协议。SWD 使调试器成为另一个 AMBA
> 总线主设备，可访问系统内存、外设或调试寄存器。数据速率最高可达 50 MHz 时的 4 Mbytes/s。SWD 还具有内置错误检测功能。在具备 SWD
> 功能的 JTAG 器件上，TMS 和 TCK 分别用作 SWDIO 和 SWCLK 信号，从而提供双模式编程器。另有一根名为串行线输出（Serial Wire
> Output，SWO）的可选信号线，可与主机应用程序交换数据和消息，对微控制器性能影响很小。稍后将分析此功能。

仪器跟踪宏单元（Instrumentation Trace Macrocell，ITM）是一种要求较低的跟踪技术，可通过名为串行线输出（Serial Wire
Output，SWO）的专用 I/O 信号，经由 SWD 发送由软件生成的调试消息。SWO 引脚与调试探针交换数据所使用的协议称为串行线查看器（Serial
Wire Viewer，SWV）。基于 Cortex-M0/0+ 的微控制器不支持 SWV。

与其他用于“调试”的外设（如 UART）或其他技术（如 ARM 半主机）相比，SWV 快得多。其通信速率与微控制器的速度成正比，因此可以限制数据交换对固件性能的影响。显然，SWO
I/O 运行得越快，对调试器的速度要求也越高。

SWV 提供以下类型的目标信息：

- 数据读取和写入的事件通知。
- 异常进入和退出的事件通知。
- 事件计数器。
- 时间戳和 CPU 周期信息，可用于程序统计剖析。

面向 Cortex-M3/4/7 内核的 CMSIS-Core 包提供了处理 SWV 协议所需的配套代码。例如，`ITM_SendChar()` 例程允许通过 SWO
引脚发送一个字符。这样我们便可重新定义 `_write()` 系统调用，将 `printf()` 例程的输出重定向到 SWV 控制台。SWV 协议定义了 32
个不同的刺激端口：端口是 SWV 消息的“标签”，可选择性地启用或禁用消息。将不同类型的数据写入不同 SWV
通道，调试器便可采用不同方式解释或可视化各通道的数据。默认刺激端口为 0。

STM32CubeIDE 提供了一整套丰富的工具和视图，以充分利用 SWV 技术所提供的所有调试可能性。使用这些调试工具完全是可选的，但对于大型且复杂的项目而言，使用它们是必不可少的。

<!-- page: 730 -->

### 24.3.1 启用 SWV 调试

要在 STM32CubeIDE 中调试并使用串行线查看器（Serial Wire Viewer, SWV），调试探针和 GDB 服务器都必须支持
SWV。在本文本中使用的典型开发环境中，这一点始终成立，因为集成的 ST-LINK 接口（无论是 V2.1 还是 V3）和 ST-LINK GDB 服务器都支持
SWV。显然，当使用 SWV 时，目标微控制器必须配置为正确启用 SWD，如图 24.19¹² 所示。

<p align="center"><img src="../images/page-0730-image-01.jpeg" alt="Image from PDF page 730"></p>

<p align="center">图 24.19：支持 SWD 的 MCU 引脚配置</p>

要使用 SWV，需要相应配置调试配置（Debug Configuration），如图 24.20 所示。为正确解码通过 SWO 端口发送的字节，主机调试器需要知道
CPU 内核频率；该值通过“核心时钟（MHz）”（Core Clock (MHz)）字段指定。默认情况下，STM32CubeIDE 将此值设置为所选 STM32 MCU
的默认时钟配置。例如，CubeMX 默认将 STM32F401RE MCU 的时钟频率设置为 84
MHz。如果不确定实际运行频率，可在调试会话期间使用“表达式”（Expressions）视图检查全局变量 `SystemCoreClock` 的内容，如图 24.21
所示。

> **注意**
>
> 若固件在运行时动态更改内核时钟，使用 SWD 接口时必须了解当前内核时钟频率。这是初次使用 SWV 时常见的困惑来源之一。

另一个重要的配置是 SWO 时钟频率。默认情况下，STM32CubeIDE 将其设置为给定配置内核时钟下的最大切换频率。这有助于减少由 SWV
接口引入的开销：通过 SWD 端口发送的字节需要以特定频率交换，这可能会影响整体固件性能。然而，ST-LINK V2.1 提供的最大 SWD 频率高达
4MHz，而较新的 ST-LINK V3 则高达 24MHz。如果您使用的是运行较低 SWD 频率的调试适配器，则可以通过指定探针的最大值来限制 SWO
时钟。

¹²默认情况下，CubeMX 将 PA14 引脚（对应串行线调试时钟，Serial Wire Debug Clock）显示为 TCK，将 PA13 引脚（对应串行线调试
I/O，Serial Wire Debug I/O）显示为 TMS。这些缩写源自 JTAG 规范，如前所述，该规范使用 4+1 个引脚来建立与目标 MCU
的调试连接。这些引脚是：测试数据输入（Test Data In, TDI）、测试数据输出（Test Data Out, TDO）、测试时钟（Test Clock,
TCK）、测试模式选择（Test Mode Select, TMS）以及测试复位（Test Reset, TRST）- 可选。

<!-- page: 731 -->

<p align="center"><img src="../images/page-0731-image-01.jpeg" alt="Image from PDF page 731"></p>

<p align="center">图 24.20：如何在 STM32CubeIDE 中启用 SWD</p>

<p align="center"><img src="../images/page-0731-image-02.jpeg" alt="Image from PDF page 731"></p>

<p align="center">图 24.21：如何使用调试表达式推导运行中的内核时钟频率</p>

### 24.3.2 配置 SWV

在调试配置中启用 SWV 后，还必须配置若干相关的全局设置，以确定要跟踪的信息类型。可从“窗口 -> 显示视图 -> SWV”中的任一 SWV
视图访问 SWV 设置，如图 24.22 所示。例如，图 24.23 展示了 SWV 跟踪日志视图：该视图左上角包含主 SWV 工具栏；单击“设置”图标即可访问
SWV 设置，如图 24.24 所示。下面介绍最相关的设置字段。

<p align="center"><img src="../images/page-0731-image-03.jpeg" alt="Image from PDF page 731"></p>

<p align="center">图 24.22：如何启用其中一个 SWV 视图</p>

<!-- page: 732 -->

<p align="center"><img src="../images/page-0732-image-01.jpeg" alt="Image from PDF page 732"></p>

<p align="center">图 24.23：如何访问 SWV 设置</p>

- 时钟设置（Clock Settings）：这些字段被禁用，仅显示在调试会话的调试配置（Debug
  Configurations）中使用和配置的值。如果需要更改这些值，请关闭调试会话并打开调试配置以进行修改。

- 跟踪事件（Trace Events）：可以跟踪以下事件。
    - **CPI**（每条指令的周期数，Cycles per instruction）：一条指令使用第一个周期之后，每多使用一个周期，内部计数器就加 1。DWT
      CPI 计数器最多计至 256，随后复位为 0；每次复位时都会发送一个数据包。它是处理器性能的一个指标，用于计算每秒指令数。值越低，性能越好。
    - **SLEEP**（睡眠周期）：CPU 处于睡眠模式的周期数，在 DWT 睡眠计数寄存器（DWT Sleep count register）中计数。CPU 每处于睡眠模式
      256 个周期，就会发送一个数据包。这可用于调试功耗或等待外部设备。
    - **FOLD**（折叠指令）：用于计算被折叠（移除）的指令数量。每 256 条占用零周期的折叠指令会接收一个事件，在 DWT 折叠计数寄存器（DWT
      Fold count register）中计数。分支折叠技术会在预测到大多数分支时，将分支指令完全从送入执行流水线的指令流中移除；它可显著提高分支性能，使分支的
      CPI 低于 1。
    - **EXC**（异常开销）：DWT 异常计数寄存器（DWT Exception count register）记录用于异常开销的 CPU
      周期数，包括压栈和返回，但不包括执行异常处理代码的时间。计数器溢出时会发送一个事件，可用于计算程序实际的异常处理成本。
    - **LSU**（加载/存储单元周期）：DWT LSU 计数寄存器（DWT LSU count register）计算处理器处理 LSU
      操作在第一个周期之后额外使用的总周期数。计数器溢出时会发送一个事件；通过该测量可跟踪内存操作所耗费的时间。
    - **EXETRC**（异常跟踪）：每当发生异常时，都会发送异常入口、异常出口和异常返回事件。可以在 SWV

<!-- page: 733 -->

    异常跟踪日志（Exception Trace Log）视图中监控这些事件。从该视图可以跳转到相应异常的处理程序代码。

<p align="center"><img src="../images/page-0733-image-01.jpeg" alt="Image from PDF page 733"></p>

<p align="center">图 24.24：SWV 设置对话框</p>

- PC 采样（PC Sampling）：启用此功能后，将以某个周期间隔开始采样程序计数器（Program Counter）。由于 SWO
  引脚带宽有限，不建议采样过快。尝试调整“分辨率（周期/采样）”（Resolution (cycles/sample)）设置，以便能够足够频繁地采样。采样的结果用于
  SWV 统计剖析（Statistical Profiling）视图等。
- 时间戳（Timestamps）：必须启用以了解事件发生的时间。预分频器（Prescaler）应仅作为最后手段更改，以减少溢出数据包。时间戳设置与
  SWV 数据跟踪时间线图（Data Trace Timeline Graph）一起使用，我们稍后会看到。
- 数据跟踪（Data Trace）：可以跟踪多达四个不同的 C 变量符号，或内存中的固定数值区域。为此，启用一个比较器并输入要跟踪的变量名称或内存地址。被跟踪变量的值可以在数据跟踪（Data
  Trace）和数据跟踪时间线图（Data Trace Timeline Graph）视图中显示。更多细节稍后介绍。
- ITM 刺激端口（ITM Stimulus Ports）：有 32 个可用的 ITM 端口（消息标签），应用程序可以使用它们。例如，可以使用 CMSIS 函数
  ITM_SendChar () 向给定端口发送字符。来自 ITM 端口的数据包显示在 SWV ITM 数据控制台（ITM Data Console）视图中。更多细节稍后介绍。

### 24.3.3 SWV 视图

STM32CubeIDE 提供了六个专用视图来利用 SWV 功能。我们现在将逐一解释它们。要在任何视图中启用 SWV
跟踪，需要切换该视图工具栏上的“开始/停止跟踪”按钮（红色按钮），如图 24.23 所示。请注意，对 SWV 设置对话框的任何更改，都将在 SWV
停止并重新启动后影响 SWV 跟踪。

<!-- page: 734 -->

#### 24.3.3.1 SWV 跟踪日志

SWV 跟踪日志视图（如图 24.23 所示）以电子表格形式列出所有传入的 SWV 数据包。可以通过选择要复制的行并输入 Ctrl+C（或在 Mac
上输入 CMD+C），将该视图中的数据以 CSV 格式复制到其他应用程序中。SWV 跟踪日志视图中的列信息描述见表 24.8。

<p align="center"><img src="../images/page-0734-image-01.jpeg" alt="Image from PDF page 734"></p>

<p align="center">表 24.8：SWV 跟踪日志视图的列描述</p>

#### 24.3.3.2 SWV 异常跟踪日志

SWV 异常跟踪日志视图（如图 24.25 所示）由两个选项卡组成。

数据选项卡 第一个选项卡类似于 SWV
跟踪日志视图，但仅限于异常事件。它还提供了关于事件类型的附加信息。数据可以复制并粘贴到其他应用程序中。每一行都链接到对应异常处理程序的代码。双击事件可在编辑器视图中打开对应的中断处理程序源代码。SWV
异常跟踪日志 – 数据选项卡中的列信息描述见表 24.9。

<p align="center"><img src="../images/page-0734-image-02.jpeg" alt="Image from PDF page 734"></p>

<p align="center">图 24.25：SWV 异常跟踪日志视图</p>

<!-- page: 735 -->

<p align="center"><img src="../images/page-0735-image-01.jpeg" alt="Image from PDF page 735"></p>

<p align="center">表 24.9：SWV 异常跟踪日志数据选项卡的列描述</p>

统计选项卡 第二个选项卡显示关于异常事件的统计信息。这些信息在优化代码时可能极具价值。其中包含指向编辑器中异常处理程序源代码的超链接。SWV
异常跟踪日志 – 统计选项卡中的列信息描述见表 24.10。

<p align="center"><img src="../images/page-0735-image-02.jpeg" alt="Image from PDF page 735"></p>

<p align="center">表 24.10：SWV 异常跟踪日志统计选项卡的列描述</p>

#### 24.3.3.3 SWV 数据跟踪

SWV 数据跟踪视图（见图 24.26）可跟踪内存中最多四个不同的符号或区域。例如，可以通过名称引用全局变量。数据可以在读、写和读/写操作上进行跟踪。SWV
设置对话框中可用四个比较器。例如，在图 24.24 中，程序中的两个全局变量 SystemCoreClock 和 uwTick（全局 HAL
滴答计数器）在读写访问时被跟踪。生成的输出可以仅包含数据值，也可以包含跟踪读写内存位置时访问的指令的 PC 值。SWV 数据跟踪仅能跟踪整数值。

<!-- page: 736 -->

<p align="center"><img src="../images/page-0736-image-01.jpeg" alt="Image from PDF page 736"></p>

<p align="center">图 24.26：SWV 数据跟踪视图</p>

#### 24.3.3.4 SWV 数据跟踪时间线图表

SWV 数据跟踪时间线图表视图包含一个图形显示，展示变量值随时间的分布情况。它适用于 SWV 数据跟踪中的变量或内存区域。图 24.27
显示了 sin ()/cos () 函数的绘图。与 SWV 数据跟踪一样，时间线图表只能绘制整数值。

SWV 数据跟踪时间线图表具有以下功能：

- 通过点击相机工具栏按钮，可以将图表保存为 JPEG 图像文件。
- 图表默认显示秒为单位的时间，但可以通过点击时钟工具栏按钮更改为周期数。
- 通过点击 Y 轴工具栏按钮，可以调整 Y 轴以最佳适配。
- 通过点击 [+] 和 [–] 工具栏按钮进行放大和缩小。
- 调试运行时，缩放范围受限。调试暂停时，可查看缩放详情。

<p align="center"><img src="../images/page-0736-image-02.jpeg" alt="Image from PDF page 736"></p>

<p align="center">图 24.27：SWV 数据跟踪时间线图表视图</p>

<!-- page: 737 -->

#### 24.3.3.5 SWV ITM 数据控制台

SWV ITM 数据控制台（见图 24.28）是 SWV 工具集中最有用的功能，尤其适用于目标设备没有专用 UART 端口可用于打印消息的情形。SWV
ITM 数据控制台输出来自目标应用程序的可读文本。通常通过 `printf()` 实现，并将输出重定向到 ITM 通道 0；其他 ITM
通道也可以拥有各自的控制台视图。

要使用 SWV ITM 数据控制台视图，首先需要在串行线查看器设置对话框中启用 32 个 ITM 端口中的一个或多个（见图 24.24）。来自 ITM
端口的数据包会显示在 SWV ITM 数据控制台视图中。应用程序可使用 CMSIS 函数 `ITM_SendChar()` 向端口 0 发送字符；也可以在
`Core/Src/syscalls.c` 中正确重写 `_write()` 系统调用，将 `printf()` 函数重定向为使用 `ITM_SendChar()`，如下所示：

```c
#include "stm32fXXxx.h"
...
int _write(int file, char *ptr, int len) {
    for (int DataIdx = 0; DataIdx < len; DataIdx++)
        ITM_SendChar(*ptr++);
    return len;
}
```

CMSIS API 没有提供方便的函数来向其他刺激端口发送字符。然而，可以通过定义以下函数轻松实现：

```c
#include "stm32fXXxx.h"
...
__STATIC_INLINE uint32_t ITM_SendCharToPort (uint32_t ch, uint8_t port)
{
    if (((ITM->TCR & ITM_TCR_ITMENA_Msk) != 0UL) &&     /* ITM enabled */
        ((ITM->TER & (1UL << port)      ) != 0UL)) {    /* ITM Port #n enabled */
        while (ITM->PORT[port].u32 == 0UL) {
            __NOP();
        }
        ITM->PORT[port].u8 = (uint8_t)ch;
    }
    return (ch);
}
```

可以通过按工具栏上的绿色 [+] 按钮，在 SWV ITM 数据控制台中打开新的端口选项卡（用于其他刺激端口）。

<!-- page: 738 -->

<p align="center"><img src="../images/page-0738-image-01.jpeg" alt="Image from PDF page 738"></p>

<p align="center">图 24.28：SWV ITM 数据控制台视图</p>

#### 24.3.3.6 SWV 统计剖析

SWV 统计剖析（参见图
24.29）视图显示基于程序计数器（PC）采样的统计数据。它展示了在各个函数中花费的执行时间。这在优化代码时非常有用。数据可以复制并粘贴到其他应用程序中。当调试暂停时，该视图会更新。要启用剖析，请遵循以下步骤：

1. 配置 SWV 以发送程序计数器样本，如图 24.24 所示，通过启用 PC 采样标志和时间戳。根据给定的分辨率（周期/样本），SWV 将程序计数器值报告给
   STM32CubeIDE。将分辨率（周期/样本）设置为高值以避免接口溢出。
2. 通过选择“窗口”->“显示视图”->“SWV 统计剖析”来打开 SWV 统计剖析视图。由于尚未收集数据，该视图为空。
3. 按下 SWV 视图工具栏上的红色“开始/停止跟踪”按钮，以将配置发送到开发板。
4. 恢复程序调试。当代码在目标系统中执行时，STM32CubeIDE 开始通过 SWV 收集关于函数使用的统计数据。
5. 暂停（挂起）调试。视图显示收集到的数据。调试会话时间越长，收集的统计数据越多。

<p align="center"><img src="../images/page-0738-image-02.jpeg" alt="Image from PDF page 738"></p>

<p align="center">图 24.29：SWV 统计剖析视图</p>

<!-- page: 739 -->

<p align="center"><img src="../images/page-0739-image-01.jpeg" alt="Image from PDF page 739"></p>

<p align="center">表 24.11：SWV 统计剖析视图的列描述</p>

## 24.4 来自 CubeHAL 的调试辅助

CubeHAL 通过检查所有 HAL API 的输入值实现运行时故障检测。运行时检查由 `assert_param()` 宏实现；该宏用于所有带输入参数的
CubeHAL 函数，可验证输入值是否处于该参数允许的取值范围内。

要启用运行时检查，需要在项目级别定义 `USE_FULL_ASSERT` 宏（可在项目设置中定义，也可取消 `stm32XXxx_hal_conf.h`
文件中该宏定义的注释）。CubeMX 会在 `main.c` 文件中生成名为 `assert_failed()` 的函数，其定义如下：

```c
void assert_failed(uint8_t* file, uint32_t line);
```

如果断言条件不满足，`assert_param()` 宏会自动调用该函数，并将文件名和该条件不满足处的确切代码行号传给它。

`assert_failed()` 函数的实现留给用户。一个简单实现是调用 `bkpt` ARM 指令设置软件断点：

```c
void assert_failed(uint8_t* file, uint32_t line) {
    asm("BKPT #0");
}
```

在开发阶段启用 `USE_FULL_ASSERT` 宏有助于理解 CubeHAL 出现的问题，尤其适合 CubeHAL 新手。

## 24.5 外部调试器

严肃的项目需要严肃的工具，这一点在电子设计中尤为明显。如果您没有跳过基础章节而读到本书这一部分，就已经了解 ST-LINK
调试接口的局限性。

<!-- page: 740 -->

<p align="center"><img src="../images/page-0740-image-01.jpeg" alt="Image from PDF page 740"></p>

<p align="center">图 24.30：SEGGER J-Link Ultra+ 调试探针</p>

SEGGER 是一家德国公司，专门设计用于 ARM Cortex 系列（包括 Cortex-M/R/A 微处理器以及其他现代微控制器，如 PIC32 和瑞萨 RX
系列）的外部调试探针。SEGGER J-Links（参见图 24.30）是当今最广泛使用的调试探针系列，它们通常作为其他供应商的 OEM 版本出售（IAR
和 Keil 的调试探针只不过是 J-Link 而已）。

J-Link 调试器提供的最相关特性包括：

- 高达 3 MByte/s 的下载速度。
- 兼容所有流行的工具链，包括 STM32CubeIDE。
- 支持在闪存中设置无限数量的软件断点。
- 允许通过 FMC 控制器在 Cortex-M 系统的外部闪存中设置断点。
- 跨平台支持（Microsoft Windows、Linux、Mac OS X）。
- 支持多个应用程序并发访问 CPU。
- 支持多核调试。
- 包含远程服务器。允许通过 TCP/IP 远程使用 J-Link。
- 软件附带免费的 GDB 服务器，允许使用 J-Link 与所有基于 GDB 的调试解决方案配合使用。
- 提供生产级闪存编程软件（J-Flash）。
- 调试器独立的闪存下载（内部闪存、CFI 闪存、SPIFI 闪存）。
- 支持 CPU/MCU 内部跟踪缓冲区（ETB、MTB 等）。

<!-- page: 741 -->

- 支持 ETM 跟踪（J-Trace Cortex-M、J-Trace ARM）。
- 宽目标电压范围：1.2V - 3.3V，5V 容忍。
- 支持多种目标接口（JTAG、SWD、FINE、SPD 等）。

J-Link 探针从 EDU 版（价格约为 60 美元）到 J-Trace PRO 版（价格约为 1,100 美元）不等。如果您是学生或预算有限的爱好者，EDU
版值得购买，因为它支持专业 J-Link 探针提供的所有相关特性。如果您是专业人士，作者认为 Ultra+ 是不错的选择。

然而，对于 STM 开发板（Nucleo、Discovery、Eval）的用户，还有一个出色且完全免费的替代方案：2016 年 4 月，SEGGER 发布了 ST-LINK
V2/V2.1¹³ 接口的固件升级，可将其转换为兼容 J-Link 的调试探针。下载¹⁴专用软件工具¹⁵后，您的 ST-LINK 会转换为兼容 J-Link OB
的接口，从而可以使用 SEGGER¹⁶ 最重要的软件工具。此外，您也可以轻松将接口还原为 ST-LINK。如果在将 ST-LINK V2 调试器切换为
J-Link OB 时遇到问题，请遵循该博客文章¹⁷中的说明。

在使用 SEGGER 调试探针进行调试时，无需使用 ST-LINK GDB Server，因为 SEGGER 提供了自己的兼容 GDB 服务器，名为
JLinkGDBServer。这是选择这些工具的基本原因之一，因为 JLinkGDBServer 是 ST-LINK 的更快、更可靠的替代方案，同时还是跨平台的。将
ST-LINK 接口升级为兼容 J-Link 接口的说明清楚地列在 SEGGER 网站上。我们不会在这里重复它们。相反，我们现在将分析如何使用
J-Link 调试探针与 GNU MCU Eclipse 工具链配合使用。

无需安装 SEGGER 软件工具即可开始使用 SEGGER 调试探针，因为 `JLinkGDBServer` 已集成在 STM32CubeIDE 中。要在 STM32CubeIDE
中使用 J-LINK，需要在“调试配置”中选择相应的调试探针。

## 24.6 同时调试两块 Nucleo 开发板

我们可能需要同时调试两个基于 STM32 的设备。这种情况并不少见，尤其是在处理通信协议时。STM32CubeIDE 允许我们在同一台计算机上调试两块或更多开发板。

要启动两个 ST-LINK GDB Server 实例，需要创建两个独立的调试配置，每块开发板对应一个配置。在每个配置中，需要设置两个基本参数：ST-LINK
接口的序列号（S/N）和 GDB Server 端口号（见图 24.31）。对于 GDB Server 端口，选择两个或更多不同的端口号（例如 61234

¹³ 在撰写本章时（2 月 2022），SEGGER 尚未提供将 ST-LINK V3 调试适配器转换为 SEGGER J-LINK
的工具。¹⁴ https://www.segger.com/jlink-st-link.html ¹⁵ 不幸的是，在撰写本章时，升级工具仅适用于 Windows 操作系统。¹⁶
请注意，此“免费”升级至 ST-LINK 接口的许可证禁止您将其用于调试自定义和商业设备。请查看 SEGGER
网站以获取完整的限制列表。¹⁷ https://bit.ly/3ostIQ6

<!-- page: 742 -->

和 61235）即可。要获取 ST-LINK 的 S/N，只需单击 ST-LINK S/N 字段旁的扫描按钮；STM32CubeIDE 会列出连接到 PC 的每块开发板的序列号。

假设使用两块不同的开发板/微控制器：HW_A 和 HW_B。当两个项目的调试配置都已设置，且每块开发板均关联到特定探针时，应先分别测试和调试两块开发板。确认正常后，即可按以下步骤同时调试两个目标：

1. 开始调试 HW_A。
2. HW_A 的调试会话开始时，STM32CubeIDE 会自动切换到调试视图。
3. 切换到 C/C++ 视图。
4. 选择 HW_B 的项目并开始调试；调试视图会再次打开。
5. 调试视图中会有两个应用程序节点，每个项目各一个。更改所选节点时，相关编辑器、变量视图及其他视图会更新，以显示与所选项目关联的信息。

<p align="center"><img src="../images/page-0742-image-01.jpeg" alt="Image from PDF page 742"></p>

<p align="center">图 24.31：同时使用两个 ST-LINK 时如何配置调试配置字段</p>

## 24.7 ARM 半主机（Semihosting）

ARM 半主机是 Cortex-M 平台的一项独特功能，对测试和调试极其有用。它是一种允许目标板卡“交换消息”的机制：从

<!-- page: 743 -->

嵌入式固件到运行调试器的主机计算机。在 Cortex-M0/0+ 内核中，由于 ITM 接口不可用，该机制可在无法使用任一集成 UART 的情况下启用
`printf()` 和 `scanf()` 功能。然而，ARM 半主机的用途并不限于打印消息；半主机还可访问其他主机 PC I/O 功能，例如终端和文件。当需要在目标板与主机
PC 之间传输大量数据时，后一项功能极其有用。

半主机需要额外的运行时库代码，并且可在 Cortex-M 架构上以多种方式实现。不过，首选方式是使用 `bkpt` ARM
汇编指令，后文将会说明。下一节将简要介绍如何配置 STM32CubeIDE 项目以在代码中使用半主机，从而能在 OpenOCD 控制台上打印消息。

### 24.7.1 在项目中启用半主机

要在 STM32CubeIDE 中使用半主机功能，需要在项目中做一些更新。此外，还需要一个支持半主机功能的调试器。本文指导如何在配合
OpenOCD、ST-LINK 和 STM32 器件时启用半主机功能。请注意，ST-LINK GDB 服务器不支持半主机功能，因此我们将配置调试设置以运行
OpenOCD。

要启用半主机功能，请按照以下步骤操作：

1. 将 `Core/Src/syscalls.c` 从编译中排除（或将其完全删除）。在“项目资源管理器”窗格中右键单击该文件，然后选择“资源配置 ->
   从构建中排除…”。
2. 在 `Core/Src/main.c` 开头添加以下两行，以包含 `<stdio.h>` 并声明 `initialise_monitor_handles()`；随后在 `main()` 函数开头调用
   `initialise_monitor_handles()`。

```c
1  #include <stdio.h>
2  extern void initialise_monitor_handles(void);
3  ...
4  int main(void) {
5      /* USER CODE BEGIN 1 */
6      initialise_monitor_handles();
```

3. 更新 GCC 链接器项目配置，将 `rdimon` 库添加到链接库中，如图 24.32 所示。

<!-- page: 744 -->

<p align="center"><img src="../images/page-0744-image-01.jpeg" alt="Image from PDF page 744"></p>

<p align="center">图 24.32：配置项目以链接 rdimon 库</p>

4. 在“其他”中更新 GCC 链接器项目配置，添加 `-specs=rdimon.specs` 标志，如图 24.33 所示。

<p align="center"><img src="../images/page-0744-image-02.jpeg" alt="Image from PDF page 744"></p>

<p align="center">图 24.33：配置项目以添加 `rdimon.specs` 标志</p>

5. 在调试探针字段中选择 ST-LINK (OpenOCD)，以配置当前调试配置；随后在“调试配置 - 启动”选项卡中添加
   `monitor arm semihosting enable` 初始化命令，如图 24.34 所示。调试控制台视图用于半主机

<!-- page: 745 -->

输入/输出，如图 24.35 所示。

<p align="center"><img src="../images/page-0745-image-01.jpeg" alt="Image from PDF page 745"></p>

<p align="center">图 24.34：配置调试设置以通过 OpenOCD 启用半主机模式</p>

<p align="center"><img src="../images/page-0745-image-02.jpeg" alt="Image from PDF page 745"></p>

<p align="center">图 24.35：在调试控制台视图中使用半主机模式输出的消息</p>

> **仔细阅读**
>
> OpenOCD 的半主机模式实现要求每个字符串在显示到 OpenOCD 控制台之前都必须以换行符（`\n`
> ）结尾。这是非常常见的错误，初次使用时往往会令人沮丧。切勿忘记在传递给 `printf()` 例程的每个字符串末尾添加 `\n`。

### 24.7.2 半主机（Semihosting）的缺点

半主机（Semihosting）是一项出色的功能，但也有几个缺点。首先，它仅在调试会话期间有效；若不在 GDB 控制下运行，固件会完全挂起。例如，在
Nucleo 开发板上下载使用半主机的示例后终止调试会话，再按下 RESET 按钮复位开发板，就会发现固件已挂起。这是因为固件卡在
`printf()` 例程中（下一节将详细说明原因）。这是相当常见的问题，每个初学者开始使用 STM32 平台时都可能遇到。

<!-- page: 746 -->

另一个需要牢记的重要方面是，半主机（Semihosting）会显著影响固件性能。每次半主机调用都要消耗若干 CPU
周期，并影响整体性能。此外，这种成本不可预测，因为它涉及 MCU 执行流之外的活动（下一节将详细说明）。

### 24.7.3 理解半主机（Semihosting）的工作原理

半主机（Semihosting）功能有多种实现方式，其中之一是使用软件断点。ARM Cortex-M 提供两类断点：硬件断点（HBP）和软件断点（SBP）。

HBP 通过对断点单元（Break Point Unit，每个 Cortex-M 内核内部的硬件单元）进行编程来设置；该单元监控内核总线，以检测从特定内存位置取指。可使用连接到调试接口的外部物理编程器，在
RAM 或 ROM 的任意位置设置 HBP。对于 Nucleo 开发板，集成 ST-LINK 编程器连接到 MCU 调试接口，并由 OpenOCD 管理。图 24.36
展示了外部调试器与 MCU 内部调试单元之间的关系。

<p align="center"><img src="../images/page-0746-image-01.png" alt="Image from PDF page 746"></p>

<p align="center">图 24.36：Cortex-M 微控制器中的调试组件</p>

SBP 的实现方法是在待检查代码之前立即加入一条特殊的 `bkpt` 指令。当内核执行断点指令时，会被强制进入调试状态。调试器发现 MCU
已停止后，便开始调试 MCU。`bkpt` 指令接受一个 8 位立即数操作码，可用于指定特定的中断条件。如果希望停止固件执行并将控制权交给调试器，以下指令即可实现：

```c
asm("bkpt #0")
```

这种技术用于实现软件条件断点。例如，假设存在需要检查的异常故障条件，则可能有如下代码：

<!-- page: 747 -->

```c
if(cond == 0) {
    ...
} else if(cond > 0) {
    ...
} else { /* Abnormal state, let us debug it */
    asm("bkpt #0");
}
```

在上述代码中，如果 `cond` 变量取负值，MCU 将停止，控制权转交给 GDB，从而可以检查调用栈和当前栈帧。

半主机（Semihosting）使用特殊的立即数操作码 `0xAB` 实现。也就是说，以下指令：

```c
asm("bkpt #0xAB")
```

会使 MCU 停止；但这次 OpenOCD 会识别该特殊操作码，并将其解释为半主机（Semihosting）操作。按约定，`r0` 寄存器包含操作类型（
`_write()`、`_read()` 等），`r1` 寄存器包含指向存放函数参数的内存区域的指针。例如，若要在主机 PC 控制台上写入以空字符结尾的字符串，可编写以下汇编指令：

```c
char msg[] = "Hello World!\r\n";
asm (
    "mov r0, 0x4 \n"       /* OPCODE for WRITE0 */
    "mov r1, %[addr] \n"   /* Address of string to transfer to OpenOCD */
    "bkpt #0xAB"
    :
    : [addr] "r" (msg)      /* Pass the reference to the msg string */
);
```

这里利用 GCC `asm()` 函数的功能，传递包含字符串 `"Hello World!\r\n"` 的 `msg` 缓冲区指针。

表 24.12 总结了支持的半主机（Semihosting）操作。请注意，OpenOCD 目前并不支持所有这些操作。

现在您可以理解为什么如果调试器不活动，半主机（Semihosting）会导致 MCU 卡住。bkpt 指令会停止 MCU
执行，并且如果不使用外部调试器（或进行硬件重置），就没有办法恢复它。此外，每次发出 bkpt 指令时，内部 MCU
活动都会暂停，直到控制权传递给调试器。在此期间，重要的异步事件（如由外设生成的中断）可能会丢失。这段时间间隔完全不可预测，并且取决于许多因素（硬件接口的速度、当前主机
PC 的负载、ST-LINK 固件的速度等，等等）。

<!-- page: 748 -->

**表 24.12：半主机（Semihosting）操作摘要（续下页）**

| 半主机操作      | 立即数操作码 | 描述                                                                                                         |
|-----------------|--------------|--------------------------------------------------------------------------------------------------------------|
| EnterSVC        | `0x17`       | 将处理器设置为 Supervisor 模式，并通过设置新 CPSR 中的两个中断屏蔽位来禁用所有中断。                         |
| ReportException | `0x18`       | 应用程序可调用此 SVC，直接向调试器报告异常。最常见用途是使用 `ADP_Stopped_ApplicationExit` 报告执行已完成。  |
| SYS_CLOSE       | `0x02`       | 关闭主机系统上的文件。句柄必须引用使用 `SYS_OPEN` 打开的文件。                                               |
| SYS_CLOCK       | `0x10`       | 返回自执行开始以来的百分之一秒数。                                                                           |
| SYS_ELAPSED     | `0x30`       | 返回自执行开始以来经过的目标滴答数。使用 `SYS_TICKFREQ` 确定滴答频率。                                       |
| SYS_ERRNO       | `0x13`       | 返回与半主机 SVC 的主机实现相关的 C 库 `errno` 变量值。                                                      |
| SYS_FLEN        | `0x0C`       | 返回指定文件的长度。                                                                                         |
| SYS_GET_CMDLINE | `0x15`       | 返回用于调用可执行文件的命令行，即 `argc` 和 `argv`。                                                        |
| SYS_HEAPINFO    | `0x16`       | 返回系统栈和堆参数；返回值通常由 C 库在初始化期间使用。                                                      |
| SYS_ISERROR     | `0x08`       | 确定另一个半主机调用的返回码是否表示错误状态。此调用传入一个包含待检查错误代码的参数块。                     |
| SYS_ISTTY       | `0x09`       | 检查文件是否连接到交互式设备。                                                                               |
| SYS_OPEN        | `0x01`       | 打开主机系统上的文件。文件路径可相对于主机进程的当前目录指定，也可按照主机操作系统的路径约定指定为绝对路径。 |
| SYS_READ        | `0x06`       | 将文件内容读入缓冲区。                                                                                       |
| SYS_READC       | `0x07`       | 从控制台读取一个字节。                                                                                       |
| SYS_REMOVE      | `0x0E`       | 删除主机文件系统上的指定文件。                                                                               |
| SYS_RENAME      | `0x0F`       | 重命名指定文件。                                                                                             |
| SYS_SEEK        | `0x0A`       | 使用从文件开头指定的偏移量，在文件中查找指定位置。假定文件是字节数组，偏移量以字节为单位。                   |
| SYS_SYSTEM      | `0x12`       | 将命令传给主机命令行解释器，可执行 `dir`、`ls` 或 `pwd` 等系统命令。终端 I/O 位于主机上，对目标不可见。      |
| SYS_TICKFREQ    | `0x31`       | 返回滴答频率。                                                                                               |

<!-- page: 749 -->

**表 24.12：半主机（Semihosting）操作摘要（续）**

| 半主机操作 | 立即数操作码 | 描述                                                                                    |
|------------|--------------|-----------------------------------------------------------------------------------------|
| SYS_TIME   | `0x11`       | 返回自 1970 年 1 月 1 日 00:00 起经过的秒数。                                           |
| SYS_TMPNAM | `0x0D`       | 返回由系统文件标识符标识的文件的临时名称。                                              |
| SYS_WRITE  | `0x05`       | 将缓冲区内容写入指定文件的当前位置。当前 OpenOCD 实现期望缓冲区以换行符（`\n`）结尾。   |
| SYS_WRITEC | `0x03`       | 将 R1 指向的字符字节写入调试通道。在 ARM 调试器下执行时，字符显示在主机调试器控制台上。 |
| SYS_WRITE0 | `0x04`       | 将空终止字符串写入调试通道。在 ARM 调试器下执行时，字符显示在主机调试器控制台上。       |
