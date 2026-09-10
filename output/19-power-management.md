<!-- page: 487 -->

# 19. 电源管理

能效是电子行业的一个趋势性话题。即使您没有设计电池供电的设备，通常也必须处理与电源相关的需求。从电源角度来看，设计良好的设备不仅能耗更低，还能简化和最小化其电源部分，从而减少 PCB 的整体尺寸、BOM（物料清单）以及功耗。

通常，我们认为电子板的电源管理完全与其供电阶段有关。在过去二十年中，电源转换一直是热门话题。IC 供应商的研究和开发产生了许多集成器件，能够在众多应用领域中提高整体电源效率，范围从低功耗解决方案到能够供应数千安培电流的高负载电源转换单元。相反，作为嵌入式开发人员，我们在确保固件能够最小化所制造设备的能耗方面承担着巨大的责任。

现代微控制器为开发人员提供了许多用于最小化能耗的工具。Cortex-M 内核也不例外，它们提供了一种“抽象”的电源管理模型，由硅片制造商重新排列以创建自己的电源管理方案。STM32 MCU 正是这种情况：即使在所有 STM32 系列中都涉及电源管理，但在 STM32L 和 STM32U 系列中，它达到了非常复杂的实现，为开发人员提供了可扩展的电源模型，以精确调整所需的能量。这使得设计能够仅由纽扣电池供电运行多年的电子设备成为可能。

在本章中，我们将快速了解 STM32 MCU 中电源管理的实现方式，并分别分析 STM32F 系列、STM32L 系列和 STM32G 系列。我们将首先检查 Cortex-M 内核提供的功能，然后发现 ST 工程师如何对其进行专门化，以在最近的 STM32L5 系列中提供多达十二种不同的电源模式。

## 19.1 基于 Cortex-M 的 MCU 中的电源管理

在我们研究基于 Cortex-M 的微控制器提供的用于以编程方式选择 MCU 电源模式的功能之前，最好先对数字设备中的功耗来源进行一些考量。

首先，设备本身的复杂性会影响能耗。我们的板卡提供的周边设备和功能越多，所需的功率就越大。此外，某些周边设备本质上能耗较高。例如，与其他电子板卡部件相比，TFT 显示屏消耗大量功率。最后，低功耗设计需要仔细选择 BOM 中的所有组件。例如，在实时时钟 (RTC)

<!-- page: 488 -->

在所有条件下（包括睡眠、关机和 VBAT 模式）都保持激活的应用中¹，LSE 的电流消耗在整体系统级应用设计中变得更加关键。

仅关注 MCU，影响功耗的第一个方面是其运行频率：CPU 运行得越快，其消耗就越高。这是一条刻在石头上的定律，所有固件开发人员都必须知道：即使我们使用的 MCU 能够运行到 200MHz，如果我们不需要那么高的速度，那么通过简单地降低时钟频率就可以节省大量能量。这也是 STM32 微控制器拥有复杂时钟分布树的主要原因之一。

这一方面的另一个影响是，主动运行的周边设备越多，MCU 消耗的功率就越大。这意味着设计良好的固件总是立即禁用不再需要的周边设备。例如，如果我们在引导过程中只需要 I²C EEPROM（因为它存储了一些我们在固件生命周期内保留在 RAM 中的配置参数），那么一旦完成，我们就必须禁用 I²C 周边设备²。这就是为什么 STM32 MCU 提供选择性禁用每个周边设备的能力，通过调用 __HAL__RCC_<PPP>_CLK_DISABLE() 来门控其时钟源，其中 <PPP> 是特定的周边设备（例如，__HAL_RCC_DMA1_CLK_DISABLE() 允许门控 DMA1 的时钟，而 __HAL_RCC_DMA1_CLK_ENABLE() 则启用它）。

在谈论微控制器时，最好谈论能效，而不仅仅是它们的功耗。设备的功耗仅谈论它使用多少 mA 或 µA，而能效衡量的是它用有限量的能量能做多少“工作”，例如以 DMIPS/mW 或 CoreMark/mW 的形式。因此我们可以发现，对于 STM32L4 MCU，当它在低功耗运行 (LPRUN) 模式下运行时，达到了最佳的能效折衷，如图 19.8 所示。

最后，MCU 及其周边设备本身的设计会影响整体功耗。这就是为什么 STM32L 微控制器被明确设计为在提供特定子系列最佳性能的同时，提供同类最佳的功耗。例如，STM32L4 MCU 中的一些通信周边设备（LPUART 就是其中之一）允许在 MCU 处于 STOP2 模式³时以 DMA 模式交换数据。

## 19.2 Cortex-M 微控制器如何处理运行模式和睡眠模式

当基于 Cortex-M 的微控制器复位时，其电源模式被设置为运行⁴模式。在此模式下，所需的能量当然由整个微控制器的设计决定，但主要取决于运行频率和激活的外设数量。这里需要特别指出的是，闪存

¹正如我们接下来将发现的，在某些非常“深度”的睡眠模式下，微控制器只能由少数几个外设唤醒，这些外设始终包括 RTC。 ²I²C 外设在以最大时钟速度运行的“旧款” STM32F103 上最多消耗 720µA。对于由市电供电的设备，这似乎不算多，但对于电池供电的设备，其影响是巨大的。 ³在此模式下，STM32L4 微控制器的内核消耗约 1.1µA。 ⁴官方 ARM 文档提到的是活动模式（active mode），这与用于指示内核未运行的睡眠模式相对。然而，由于本书完全关于 STM32 微控制器，且 Cortex-M 微控制器的电源方案取决于特定供应商的实现，因此我们将在本书中使用“运行模式”（run mode）这一术语，这是 ST 用来指示 CPU 正在积极运行的术语。

<!-- page: 489 -->

和 SRAM 存储器都是位于 Cortex-M 内核之外的“外设”。此外，采用先进的闪存预取技术（如 ART™ 加速器）也会影响整体功耗。

在此模式下，开发人员可以通过调节时钟速度和禁用不需要的外设来改变微控制器的能耗方式。这看似显而易见，但重要的是要指出，在许多实际情况下，这是我们能做的最佳电源优化。正如我们将在本章后面看到的，STM32G/L 微控制器将运行模式结构化为多个子模式，在保证大部分功能性和最佳 CPU 性能的同时，提供了对功耗更多的控制。

如果我们知道在给定时间段内不需要处理任何事务，那么 Cortex-M 内核允许我们将其置于睡眠模式，而无需进行忙等待（busy-waits）。在此模式下，内核停止运行，并且只能由来自 EXTI 控制器的“外部事件”（例如连接到 GPIO 的按钮）唤醒。同样，STM32G/L 微控制器扩展了此模式，提供多达八种不同的子模式，我们稍后将看到。

重要的是要强调，Cortex-M 内核进入睡眠模式是“自愿的”：两条不同的 ARM 指令（我们稍后将看到）会暂停 CPU，同时保持其部分事件线处于活动状态。通过触发这些线，CPU 会在给定的唤醒时间内恢复执行，该时间取决于有效的睡眠级别和 Cortex-M 内核类型（M0、M3 等）。

唤醒延迟可以用 CPU 周期来表示（对于“轻量级”睡眠模式），也可以用微秒（µs）来表示（对于深度睡眠模式）。这意味着睡眠模式越深，唤醒时间越长。开发人员需要决定为其特定应用使用哪种睡眠模式：进入然后退出深度低功耗状态所消耗的能量和时间可能会超过任何潜在的功耗节省收益。在可穿戴设备中，能效是最重要的因素，而在某些工业控制应用中，唤醒延迟可能非常关键。

设计低功耗系统也有不同的方法。如今，许多嵌入式系统被设计为中断驱动（interrupt driven）。这意味着当没有请求需要处理时，系统保持在睡眠模式。当中断请求到达时，处理器唤醒并处理它，工作完成后再次回到睡眠模式。或者，如果数据处理请求是周期性的且持续时间恒定，并且数据处理延迟不是问题，你可以以尽可能慢的时钟速度运行系统以减少功耗。哪种方法更好没有明确的答案，因为选择将取决于应用的数据处理要求、所使用的微控制器以及其他因素，如可用的电源类型。

<!-- page: 490 -->

![Image from PDF page 490](../images/page-0490-image-01.png)

图 19.1：固件如何潜在地管理其活动期间的时钟速度和电源模式

图 19.1 展示了一种最小化功耗的可能策略。在微控制器启动过程中，微控制器以最大速度运行，以允许快速完成所有初始化活动。当所有外设配置完成后，时钟速度降低，微控制器进入睡眠模式。在此期间，微控制器由中断唤醒，这些中断可以在较低的 CPU 速度下处理。当需要执行 CPU 密集型操作时，时钟速度可以增加到最大值，完成后再次降低。

那么，何时进入睡眠模式？如前所述，由我们决定将微控制器置于可能的睡眠模式之一的正确时间。如果我们知道微控制器正在等待通过中断通知的异步事件，那么进入睡眠模式而不是进行忙等待可能是正确的时机。让我们考虑一下我们在本书中多次看到的经典闪烁 LED 应用。

```text
...
while(1) {
HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
HAL_Delay(500);
}
```

这段看似无害的代码对我们设备的功耗有巨大影响。即使在那 500ms 内我们没有太多事情要做，我们也在浪费大量电力来检查全局 SysTick 计数值，以查看该时间是否已过。相反，我们可以重新排列该代码，使其大部分时间保持在睡眠模式，并设置一个定时器，在 100ms 后唤醒微控制器。

让其他软件组件决定何时将微控制器置于睡眠模式可以代表另一种方法。正如我们将在第 23 章中发现的，实时操作系统可以被编程为在无事可做时自动将微控制器置于睡眠模式⁵。

⁵我们将在该章中发现，一种可能的策略是在空闲线程被调度时将微控制器置于睡眠模式。空闲线程是当所有其他线程都“不可运行”时由实时操作系统执行的那个线程。这显然意味着微控制器没有相关的事情要做，可以安全地将其置于睡眠模式。

<!-- page: 491 -->

### 19.2.1 进入/退出睡眠模式

正如上一段所述，CPU 仅基于自愿原则进入睡眠模式，通过使用特定的 ARM 汇编指令实现。这意味着，作为程序员，我们对我们所制造设备的功耗承担全部责任⁶。

基于 Cortex-M 的微控制器（MCU）提供两条指令将 MCU 置于睡眠模式：WFI 和 WFE。等待中断（Wait For Interrupt, WFI）指令也被称为无条件睡眠指令。当 CPU 执行该指令时，它会立即停止内核执行。CPU 仅在中断请求（取决于中断优先级和有效的睡眠级别，稍后详述）或调试事件的情况下才会恢复。如果在 MCU 执行 WFI 指令时有中断处于挂起状态，它会进入睡眠模式并立即再次唤醒。

等待事件（Wait For Event, WFE）是另一条允许将 MCU 置于睡眠模式的指令。它与 WFI 的不同之处在于，它在停止内核之前会检查特定事件寄存器⁷的状态：如果该寄存器被置位，WFE 会清除它并且不停止 CPU，继续执行程序执行（这允许我们在需要时处理挂起的事件）。否则，它会停止 MCU，直到该事件寄存器再次被置位。

但事件和中断之间的确切区别是什么？在 STM32 世界（以及更广泛的 Cortex-M 世界）中，事件是一个令人困惑的来源。与我们在第 7 章中学会处理的中断相比，它们看起来像是某种无形的东西。在我们澄清“事件”一词的含义之前，我们需要更好地解释 EXTI 控制器在 STM32 MCU 中的作用。扩展中断和事件控制器（Extended Interrupts and Events Controller, EXTI）是 MCU 内部的一个硬件组件，它管理外部和内部异步中断/事件，并向 CPU/NVIC 控制器生成事件请求，向电源控制器生成唤醒请求（参见图 19.2）。EXTI 允许管理多条事件线，这些线可以将 MCU 从某些睡眠模式中唤醒（并非所有事件都能唤醒 MCU）。这些线是可配置的或直接的，因此在 MCU 内部是硬连线的：

- 线是可配置的：可以独立选择活动边沿，并且状态标志指示中断源。可配置线用于 I/O 外部中断和少数外设（稍后详述）。
- 线是直接的且硬连线的：它们由某些外设用于生成从停止模式唤醒的事件或中断。状态标志由外设本身提供。例如，RTC 可用于生成唤醒 MCU 的事件。

⁶显然，我们谈论的是 MCU 内核和所有集成外设的功耗。整个板的功耗由其他因素决定，这里不予讨论。⁷该寄存器位于内核内部，用户无法访问。

<!-- page: 492 -->

![Image from PDF page 492](../images/page-0492-image-01.jpeg)

图 19.2：如何使用事件唤醒内核

关于 EXTI 和 NVIC 控制器，另一个需要澄清的重要方面是，每条线都可以独立地屏蔽中断或事件生成。例如，在第 6 章中我们看到，GPIO 可以配置为工作在 GPIO_MODE_EVT_* 模式下，这与 GPIO_MODE_IT_* 模式不同：在前一种情况下，当 I/O 被触发时，它不会生成 IRQ 请求，而是会设置事件标志。如果 MCU 使用 WFE 指令进入了低功耗模式，这将导致 MCU 唤醒。

因此，WFE 指令检查是否有事件挂起，因此也被称为条件睡眠指令。该事件寄存器可以由以下情况设置：

- 异常进入和退出；
- 当 SEV-On-Pend 功能启用时，当中断挂起状态从 0 变为 1 时，事件寄存器可以被设置（稍后详述）；
- 外设设置其专用事件线（这是外设特定的）；
- 执行 SEV（Send Event）指令；
- 调试事件（例如，停止请求）。

在第 7 章中我们看到，在 Cortex-M3/4/7/33 内核中，我们可以暂时屏蔽那些优先级低于 BASEPRI 寄存器中设定值的中断的执行。然而，如果这些中断触发，它们仍然处于使能状态并被标记为挂起。我们可以通过设置 SCR->SEVONPEND 位来配置 MCU，以便在中断挂起时设置事件寄存器。顾名思义，该寄存器将在“中断挂起时设置事件寄存器”。这意味着，如果处理器被 WFE 指令置于睡眠模式，CPU 会立即唤醒，我们可以最终处理挂起的中断。相反，WFI 指令永远不会唤醒内核。Cube HAL 提供了两个方便的函数，HAL_PWR_EnableSEVOnPend() 和 HAL_PWR_DisableSEVOnPend()，以执行此设置。

<!-- page: 493 -->

相反，如果通过设置 PRIMASK 寄存器来屏蔽中断，挂起的中断可以唤醒处理器，无论使用哪种睡眠指令（WFI 或 WFE）：这一特性允许软件通过门控时钟来关闭 MCU 的某些部分，并且软件可以在唤醒后、执行 ISR 之前将其重新打开。

因此，总结一下，WFI 和 WFE 具有相同的以下行为：

- 在使能的且优先级高于当前级别的中断/异常请求时唤醒⁸；
- 可以被调试事件唤醒；
- 可用于产生睡眠和深度睡眠模式（稍后详述）。

相反，WFI 和 WFE 因以下原因而不同：

- 如果内部事件寄存器被置位，执行 WFE 不会进入睡眠模式，而执行 WFI 总是导致睡眠；
- 如果设置了 SEVONPEND，被禁用或屏蔽的中断的新挂起可以从 WFE 唤醒处理器；
- WFE 可以被外部事件唤醒；
- 当设置了 PRIMASK 时，WFI 可以被使能的中断唤醒。

#### 19.2.1.1 退出时休眠 (Sleep-On-Exit)

退出时休眠 (Sleep-On-Exit) 功能对于中断驱动的应用非常有用，在这些应用中，除了初始化阶段外，所有操作都在中断处理程序中执行。这是一个可编程功能，可以通过设置 SCB->SCR 寄存器中的位来启用或禁用。当启用时，Cortex-M 内核在退出异常/中断处理程序时会自动进入休眠模式（其行为与 WFI 指令相同）。应在初始化阶段结束时启用退出时休眠 (Sleep-On-Exit) 功能。否则，如果在初始化阶段期间发生中断事件，而此时退出时休眠 (Sleep-On-Exit) 功能已启用，即使初始化阶段尚未完成，处理器也会进入休眠状态。

CubeHAL 提供了两个便捷的例程来启用/禁用此模式：HAL_PWR_EnableSleepOnExit() 和 HAL_PWR_DisableSleepOnExit()。

### 19.2.2 基于 Cortex-M 的微控制器中的休眠模式

到目前为止，我们广泛地讨论了休眠模式。这主要是因为 ARM 定义的电源管理方案被芯片供应商进一步专门化，例如 ST 在其产品中就是这样做的。基于 Cortex-M 的微控制器在架构上支持两种休眠模式：普通休眠和深度休眠。正如我们将在本章后面发现的那样，STM32F 微控制器将它们称为休眠 (sleep) 和停止 (stop) 模式

⁸基于优先级禁用中断仅适用于基于 Cortex-M3/4/7 的微控制器。

<!-- page: 494 -->

并添加了一种更深的模式，称为待机 (standby) 模式。STM32L 系列进一步将这些两个“主要”操作模式细分为多个子模式。

普通休眠和深度休眠模式都是通过之前看到的 WFI 和 WFE 指令达到的。唯一的区别是，深度休眠模式是通过将 PWR->SCR 寄存器中的 SLEEPDEEP 位设置为 1 来实现的。然而，我们不需要处理这些细节，因为 CubeHAL 被设计为抽象这些细节。

通常，STM32 微控制器被设计为在休眠模式下仅关闭 CPU 时钟，而对其他时钟或模拟时钟源没有影响（这意味着所有启用的外设保持活动状态）。而在停止模式下，属于 1.8V（对于较新的 STM32 微控制器为 1.2V）域时钟的所有外设都会被关闭，而 VDD 域保持开启⁹，除了 HSI 和 HSE 振荡器会被关闭。在待机模式下，1.8V 域和 VDD 域都会被关闭。然而，在下一段中我们将深入探讨这些主题。

## 19.3 STM32F 微控制器中的电源管理

迄今为止说明的概念适用于所有 STM32 微控制器。然而，STM32 产品组合分为几个分支：STM32F、STM32G、STM32L、STM32U 系列（不考虑本书未涵盖的 STM32W 系列）。STM32G/L/U 面向低功耗应用，并提供更多的操作模式以最小化功耗。

我们将首先分析如何管理 STM32F 微控制器中的电源模式。然而，重要的是要强调，正如这个庞大产品组合中其他功能经常发生的情况一样，某些 STM32 系列，甚至某些特定的部件号，具有与大多数 STM32F 微控制器处理电源管理方式不同的特定特性。因此，请始终手边备有您正在考虑的微控制器的参考手册。

### 19.3.1 电源

图 19.3 显示了 STM32F 微控制器的电源¹⁰。如前所述，即使我们习惯于仅通过一个电源为微控制器供电（更多相关内容见第 27 章），微控制器内部有一个电源分配网络，定义了多个电压域，用于为具有相同供电特性的外设供电。例如，VDDA 域包括那些需要独立（过滤更好）电源的模拟外设，通过 VDDA 引脚供电。

⁹正如我们将很快发现的，STM32 微控制器可以由 2.0V 到 3.6V 的可变电压源供电（其中一些允许低至 1.62V 供电）。该电压源也称为 VDD 域，微控制器内部所有由该电源供电的组件都被认为是 VDD 域的一部分。然而，微控制器内部内核和其他一些外设由专用的 1.8V（在某些 STM32L 微控制器中甚至为 1.0V）内部电压调节器供电。这定义了 1.8V 域或 VCORE 域。低压内部调节器可以独立关闭。稍后会有更多介绍。 ¹⁰重要的是要指出，图 19.3 中的图表只是一个示意图。某些 STM32F 微控制器，特别是那些提供 TFT-LCD 控制器或其他通信接口（如以太网）的微控制器，引入了其他电源域。同样，引脚数较少的 STM32 微控制器（特别是引脚数少于 32 个的那些）具有简化的电源分配网络。然而，这里说明的概念仍然有效。

<!-- page: 495 -->

![Image from PDF page 495](../images/page-0495-image-01.jpeg)

图 19.3：STM32F 微控制器中的电源

VDD 和 VDD18 域是最相关的域。VDD 域由外部电源供电，而 VDD18 域由微控制器内部的电压调节器供电。该调节器可以配置为工作在低功耗模式，我们将在下文看到。为了在 VDD 关闭时保持备份寄存器¹¹的内容并为 RTC 功能供电，VBAT 引脚可以连接到由电池或其他源提供的可选待机电压。VBAT 引脚为 RTC 单元、LSE 振荡器以及用于从深度休眠模式唤醒微控制器的一个或两个引脚供电，允许 RTC 在主电源关闭时继续运行。因此，VBAT 电源被称为为 RTC 域供电。切换到 VBAT 供电由嵌入在复位块中的掉电复位 (Power Down Reset, PDR) 控制。

### 19.3.2 电源模式

在本章的第一部分中，我们已经了解到 Cortex-M 微控制器（MCU）提供三种主要的电源模式：运行（run）、睡眠（sleep）和深度睡眠（deep sleep）。现在正是时候来看看 ST 工程师如何在 STM32F 系列微控制器中重新安排这些模式了。表 19.1 总结了这些模式，并展示了硬件抽象层（HAL）提供的三个主要功能，用于将微控制器置于相应的电源模式。我们将在后面更深入地分析它们。

¹¹备份寄存器（Backup registers）是一个专用的内存区域，典型大小为 4Kb，由不同的电源供电，通常连接到电池或超级电容器。这用于存储易失性数据，即使微控制器断电（无论是整个设备关闭还是微控制器进入待机模式），这些数据仍然保持有效。

<!-- page: 496 -->

![Image from PDF page 496](../images/page-0496-image-01.png)

表 19.1：STM32F 系列微控制器支持的三种电源模式

#### 19.3.2.1 运行模式

默认情况下，在上电或系统复位后，STM32F 系列微控制器被置于运行模式。这是一种完全活跃的模式，即使执行轻微任务也会消耗大量功率。运行模式和睡眠模式的功耗都取决于工作频率¹²。

图 19.4¹³ 展示了一些最新 STM32F4 系列微控制器的功耗水平。

在运行模式下，主稳压器向 1.8-1.2V 域（CPU 内核、存储器和数字外设）提供全功率。在此模式下，稳压器输出电压（根据具体的 STM32F 系列微控制器，约为 1.8-1.2V）可以通过软件调整为不同的电压值（稍后会有更多介绍）。一些较新的 STM32F4 系列微控制器提供两种运行模式：

- 正常模式（Normal mode）：CPU 和内核逻辑在给定的电压缩放（scale 1、scale 2 或 scale 3）下以最大频率运行。
- 超驱动模式（Over-drive mode）：此模式允许 CPU 和内核逻辑在电压缩放 scale 1 和 scale 2 下以高于正常模式的频率运行。稍后会有更多关于此模式的介绍。

¹²请记住，在睡眠模式下，只有 CPU 时钟被关闭，而其他外设保持活跃。因此，HCLK 时钟源的速度继续影响整体功耗。 ¹³该图取自 ST AN4365(https://bit.ly/1XzmF2o) 应用笔记。

<!-- page:497 -->

![Image from PDF page 497](../images/page-0497-image-01.jpeg)

图 19.4：一些 STM32F4 系列微控制器的功耗

##### 19.3.2.1.1 STM32F4/F7 系列微控制器中的动态电压缩放

直流电路使用的功率由电路的电流和电压决定。这意味着我们可以通过降低电压来减少电路所需的功率。STM32F4/F7 系列提供了一项名为动态电压缩放（Dynamic Voltage Scaling, DVS）的智能供电技术，这是 STM32L 系列特有的。DVS 背后的理念是，许多嵌入式系统并不总是需要系统的完整处理能力，因为并非所有子系统始终处于活跃状态。在这种情况下，系统可以保持活跃模式，而处理器不必以最大工作频率运行。当较低频率足够时，可以降低提供给处理器的电压。通过这种电源管理，我们可以在监控处理器输入电压以响应系统性能需求的同时，减少电池消耗的功率。

这包括在根据处理需求降低时钟频率时，缩放 STM32F4 系列稳压器输出电压，该电压为 1.2V 域（内核、存储器和数字外设）供电。STM32F4/F7 系列提供三种电压缩放级别（scale 1、scale 2 和 scale 3）。给定电压缩放级别下可实现的最大内核频率由具体的 STM32 微控制器决定。例如，STM32F401 仅提供两种电压缩放级别，scale 2 和 scale 3，分别允许内核运行至 84MHz 和 60MHz。为了控制电压缩放，CubeHAL 提供了以下函数：

```text
HAL_StatusTypeDef HAL_PWREx_ControlVoltageScaling(uint32_t VoltageScaling);
```

该函数接受符号常量 PWR_REGULATOR_VOLTAGE_SCALE1、PWR_REGULATOR_VOLTAGE_SCALE2 和 PWR_REGULATOR_VOLTAGE_SCALE3。只有当系统时钟多路复用器（System Clock Multiplexer）的源时钟是 HSI 或 HSE 时，才能更改电压缩放级别。因此，要增加/减少电压缩放级别，您可以遵循以下程序：

<!-- page: 498 -->

- 使用 HAL_RCC_ClockConfig() 将 HSI 或 HSE 设置为系统时钟频率。
- 调用 HAL_RCC_OscConfig() 来配置 PLL。
- 调用 HAL_PWREx_ConfigVoltageScaling() API 来调整电压缩放级别。
- 使用 HAL_RCC_ClockConfig() 设置新的系统时钟频率。

有关此主题的更多信息，请参阅 AN4365¹⁴。

##### 19.3.2.1.2 STM32F4/F7 系列微控制器中的超驱动/欠驱动模式

STM32F4 系列中的某些微控制器以及所有 STM32F7 系列微控制器提供两种甚至多种子运行模式。这些模式被称为超驱动（over-drive）和欠驱动（under-drive）。前者通过某种“超频”方式增加内核频率。建议当应用程序未运行关键任务且系统时钟源为 HSI 或 HSE 时进入超驱动模式。这些功能在希望临时增加/减少微控制器时钟速度而不重新配置时钟树时非常有用，因为重新配置时钟树通常会引入不可忽略的开销。HAL 提供了两个方便的函数 HAL_PWREx_EnableOverDrive() 和 HAL_PWREx_DisableOverDrive() 来执行此操作。

欠驱动模式与超驱动模式相反，通过降低 CPU 频率并禁用某些外设来实现。在此模式下，可以将内部电压稳压器置于低功耗模式。在某些 STM32F4/F7 系列微控制器中，即使在停止模式（stop mode）下也可用欠驱动模式。

#### 19.3.2.2 睡眠模式

通过执行 WFI 或 WFE 指令进入睡眠模式。在睡眠模式下，所有 I/O 引脚保持与运行模式相同的状态。然而，我们无需关心汇编指令，因为 CubeHAL 提供了以下函数：

```text
void HAL_PWR_EnterSLEEPMode(uint32_t Regulator, uint8_t SLEEPEntry);
```

第一个参数 Regulator 对于所有 STM32F 系列在睡眠模式下均无意义，保留该参数是为了与 STM32L 系列保持兼容。第二个参数 SLEEPEntry 可以取值为 PWR_SLEEPENTRY_WFI 或 PWR_SLEEPENTRY_WFE：顾名思义，前者执行 WFI 指令，后者执行 WFE 指令。

![Image from PDF page 498](../images/page-0498-image-01.png)

如果您查看 HAL_PWR_EnterSLEEPMode() 函数，会发现如果传入参数 PWR_SLEEPENTRY_WFE，它会连续执行两条 WFE 指令。这导致 HAL_PWR_EnterSLEEPMode() 以与传入参数 PWR_SLEEPENTRY_WFI 相同的方式进入睡眠模式（连续调用两次 WFE 会导致：如果事件寄存器已置位，则第一条 WFE 指令将其清除，第二条指令使 MCU 进入睡眠模式）。我不知道 ST 为何采用这种方法。如果您希望完全控制 MCU 进入低功耗模式的方式，则需要根据您的需要重新调整该函数的内容。显然，MCU 将遵循 WFE 指令的退出条件从睡眠模式退出。

¹⁴https://bit.ly/1XzmF2o

<!-- page: 499 -->

如果使用 WFI 指令进入睡眠模式，任何由嵌套向量中断控制器 (NVIC) 确认的外设中断都可以将器件从睡眠模式唤醒。如果使用 WFE 指令进入睡眠模式，一旦发生事件，MCU 即退出睡眠模式。唤醒事件可以由以下任一方式产生：

- 在外设控制寄存器中使能中断，但在 NVIC 中未使能，并在系统控制寄存器 (System Control Register) 中使能 SEVONPEND 位 - 当 MCU 从 WFE 恢复时，必须清除外设中断挂起位和外设 NVIC IRQ 通道挂起位（位于 NVIC 中断清除挂起寄存器中）；
- 或者将外部或内部 EXTI 线配置为事件模式 - 当 CPU 从 WFE 恢复时，无需清除外设中断挂起位或 NVIC IRQ 通道挂起位，因为对应于事件线的挂起位未被置位。

此模式提供最短的唤醒时间，因为在中断进入/退出过程中没有浪费时间。

#### 19.3.2.3 停止模式

停止模式基于 Cortex-M 深度睡眠模式并结合外设时钟门控。在停止模式下，1.8V 域中的所有时钟停止，PLL、HSI 和 HSE 振荡器被禁用。SRAM 和寄存器内容得以保留。在停止模式下，所有 I/O 引脚保持与运行模式相同的状态。电压调节器可配置为正常模式或低功耗模式。为使 MCU 进入停止模式，HAL 提供了以下函数：

```text
void HAL_PWR_EnterSTOPMode(uint32_t Regulator, uint8_t STOPEntry);
```

其中，Regulator 参数接受值 PWR_MAINREGULATOR_ON 以保持内部电压调节器开启，或接受值 PWR_LOWPOWERREGULATOR_ON 将其置于低功耗模式。参数 STOPEntry 可以取值为 PWR_STOPENTRY_WFI 或 PWR_STOPENTRY_WFE。

要进入停止模式，所有 EXTI 线挂起位、所有外设中断挂起位以及 RTC 闹钟标志必须被复位。否则，停止模式进入过程将被忽略，程序执行将继续。如果应用程序需要在进入停止模式之前禁用外部高速振荡器 (HSE)，则必须先将系统时钟源切换到 HSI，然后清除 HSEON 位。否则，如果在进入停止模式之前 HSEON 位保持为 1，则必须启用安全系统 (CSS) 功能以检测任何外部振荡器（外部时钟）故障，并避免在进入停止模式时发生故障。

任何配置为中断或事件模式的 EXTI 线都会强制 CPU 退出停止模式，具体取决于它是使用 WFI 还是 WFE 指令进入低功耗模式的。由于在进入停止模式之前 HSE 和 PLL 均被禁用，因此当退出此低功耗模式时，MCU 源时钟被设置为 HSI。这意味着我们的代码必须根据所需的 SYSCLK 速度重新配置时钟树。

<!-- page: 500 -->

#### 19.3.2.4 待机模式

待机模式可实现最低的功耗。它基于 Cortex-M 深度睡眠模式，且电压调节器被禁用。因此，1.8-1.2V 域断电。PLL 多路复用器、HSI 和 HSE 振荡器也关闭。SRAM 和寄存器内容丢失，待机电路中的寄存器除外。为使 MCU 进入待机模式，HAL 提供了以下函数：

```text
void HAL_PWR_EnterSTANDBYMode(void);
```

当发生外部复位 (NRST 引脚)、IWDG 复位、任一已使能的 WKUPx 引脚上的上升沿或 RTC 事件时，微控制器退出待机模式。从待机模式唤醒后，除电源控制/状态寄存器 (PWR->CSR) 外，所有寄存器均被复位。从待机模式唤醒后，程序执行以与复位后相同的方式重新开始（启动引脚采样、选项字节加载、获取复位向量等）。使用宏：

```text
__HAL_PWR_GET_FLAG(PWR_FLAG_SB);
```

我们可以检查 MCU 是否因退出待机模式而正在复位。由于在进入停止模式之前 HSE 和 PLL 均被禁用，因此当退出此低功耗模式时，MCU 源时钟被设置为 HSI。这意味着我们的代码必须根据所需的 SYSCLK 速度重新配置时钟树。

仔细阅读

![Image from PDF page 500](../images/page-0500-image-01.png)

某些 STM32 MCU 存在硬件缺陷，导致无法进入或退出待机模式。在进入此模式之前必须满足特定条件。请查阅您 MCU 的勘误表以获取更多信息（如果适用）。

#### 19.3.2.5 低功耗模式示例

以下示例旨在 Nucleo-F072RB¹⁵ 上运行，展示了低功耗模式的工作方式。

¹⁵ 对于其他 Nucleo 开发板，请参阅本书中的示例。

<!-- page: 501 -->

```text
Filename: Core/Src/main-ex1.c
14
int main(void) {
15
char msg[30];
```

16

```text
17
HAL_Init();
18
Nucleo_BSP_Init();
```

19

```text
20
/* Before we can access to every register of the PWR peripheral we must enable it */
21
__HAL_RCC_PWR_CLK_ENABLE();
```

22

```text
23
while (1) {
24
if(__HAL_PWR_GET_FLAG(PWR_FLAG_SB)) {
25
/* If standby flag set in PWR->CSR, then the reset is generated from
26
* the exit of the standby mode */
27
sprintf(msg, "RESET after STANDBY mode\r\n");
28
HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), HAL_MAX_DELAY);
29
/* We have to explicitly clear the flag */
30
__HAL_PWR_CLEAR_FLAG(PWR_FLAG_WU|PWR_FLAG_SB);
31
}
```

32

```text
33
sprintf(msg, "MCU in run mode\r\n");
34
HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), HAL_MAX_DELAY);
35
while(HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_13) == GPIO_PIN_SET) {
36
HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
37
HAL_Delay(100);
38
}
```

39

```text
40
HAL_Delay(200);
```

41

```text
42
sprintf(msg, "Entering in SLEEP mode\r\n");
43
HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), HAL_MAX_DELAY);
```

44

```text
45
SleepMode();
```

46

```text
47
sprintf(msg, "Exiting from SLEEP mode\r\n");
48
HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), HAL_MAX_DELAY);
```

49

```text
50
while(HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_13) == GPIO_PIN_SET);
51
HAL_Delay(200);
```

52

```text
53
sprintf(msg, "Entering in STOP mode\r\n");
54
HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), HAL_MAX_DELAY);
```

55

```text
56
StopMode();
```

57

```text
58
sprintf(msg, "Exiting from STOP mode\r\n");
59
HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), HAL_MAX_DELAY);
```

<!-- page: 502 -->

60

```text
61
while(HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_13) == GPIO_PIN_SET);
62
HAL_Delay(200);
```

63

```text
64
sprintf(msg, "Entering in STANDBY mode\r\n");
65
HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), HAL_MAX_DELAY);
```

66

```text
67
StandbyMode();
```

68

```text
69
while(1); //Never arrives here, since MCU is reset when exiting from STANDBY
70
}
71
}
```

72

73

```text
74
void SleepMode(void)
75
{
76
GPIO_InitTypeDef GPIO_InitStruct;
```

77

```text
78
/* Disable all GPIOs to reduce power */
79
MX_GPIO_Deinit();
```

80

```text
81
/* Configure User push-button as external interrupt generator */
82
__HAL_RCC_GPIOC_CLK_ENABLE();
83
GPIO_InitStruct.Pin = B1_Pin;
84
GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
85
GPIO_InitStruct.Pull = GPIO_NOPULL;
86
HAL_GPIO_Init(B1_GPIO_Port, &GPIO_InitStruct);
```

87

```text
88
HAL_UART_DeInit(&huart2);
```

89

```text
90
/* Suspend Tick increment to prevent wakeup by Systick interrupt.
91
Otherwise the Systick interrupt will wake up the device within 1ms (HAL time base) */
92
HAL_SuspendTick();
```

93

```text
94
__HAL_RCC_PWR_CLK_ENABLE();
95
/* Request to enter SLEEP mode */
96
HAL_PWR_EnterSLEEPMode(0, PWR_SLEEPENTRY_WFI);
```

97

```text
98
/* Resume Tick interrupt if disabled prior to sleep mode entry*/
99
HAL_ResumeTick();
100
101
/* Reinitialize GPIOs */
102
MX_GPIO_Init();
103
104
/* Reinitialize UART2 */
105
MX_USART2_UART_Init();
106
}
```

<!-- page: 503 -->

第 21 行的宏 __HAL_RCC_PWR_CLK_ENABLE() 启用了 PWR 外设：在执行任何与电源管理相关的操作之前，我们需要启用 PWR 外设，即使我们只是检查 PWR->CSR 寄存器中是否设置了待机标志。这是许多初学者在电源管理中遇到麻烦的一个来源。第 [24:31] 行检查是否设置了待机标志：如果是，这意味着 MCU 在退出待机模式后发生了复位。第 [33:38] 行代表运行模式：LD2 LED 会闪烁，直到我们按下连接到 PC13 引脚的 Nucleo USER 按钮。main() 中剩余的代码只是在每次按下 USER 按钮时循环遍历三种低功耗模式。第 [74:106] 行定义了 SleepMode() 函数，用于将 MCU 置于睡眠模式。所有 GPIO 都被配置为模拟模式，以减少未使用 IO 上的电流消耗（特别是那些可能成为漏电源的引脚）。相应的外设时钟被关闭，除了 GPIOC 外设：PC13 GPIO 用于从低功耗模式恢复。同样的情况也适用于 UART2 接口和 SysTick 定时器，后者被停止以防止 MCU 在 1ms 后退出低功耗模式。第 96 行对 HAL_PWR_EnterSLEEPMode() 函数的调用将 MCU 置于睡眠模式，直到按下 USER 按钮时唤醒（因为我们将相应的 IRQ 配置为导致 WFI 指令退出低功耗模式，所以 MCU 会唤醒）。此处未显示的 StopMode() 函数与 SleepMode() 几乎相同，除了它调用 HAL_PWR_EnterSTOPMode() 函数将 MCU 置于停止模式，并且再次调用 Nucleo_BSP_Init() 函数，该函数进而调用 SystemClock_Config() 函数以恢复时钟到原始设置，从而允许 USART2 正常工作。

```text
Filename: Core/Src/main-ex1.c
149
void StandbyMode(void) {
150
MX_GPIO_Deinit();
151
152
/* This procedure come from the STM32F030 Errata sheet*/
153
__HAL_RCC_PWR_CLK_ENABLE();
154
155
HAL_PWR_DisableWakeUpPin(PWR_WAKEUP_PIN1);
156
157
/* Clear PWR wake up Flag */
158
__HAL_PWR_CLEAR_FLAG(PWR_FLAG_WU);
159
160
/* Enable WKUP pin */
161
HAL_PWR_EnableWakeUpPin(PWR_WAKEUP_PIN1);
162
163
/* Enter STANDBY mode */
164
HAL_PWR_EnterSTANDBYMode();
165
}
```

最后，第 [144:160] 行定义了 StandbyMode() 函数。在这里，我们遵循 STM32F072 勘误表中描述的过程，因为该系列受一个硬件缺陷影响，导致 CPU 无法进入待机模式：我们必须首先禁用 PWR_WAKEUP_PIN1 引脚，然后清除 PWR->CSR 外设中的唤醒标志，并重新启用唤醒引脚，在 STM32F072 MCU 中，该引脚与 PA0 引脚重合。

<!-- page: 504 -->

![Image from PDF page 504](../images/page-0504-image-01.png)

STM32 MCU 通常有两个唤醒引脚，分别命名为 PWR_WAKEUP_PIN1 和 PWR_WAKEUP_PIN2。对于许多采用 LQFP64 封装的 STM32 MCU，第二个唤醒引脚与 PC13 重合，而在所有 Nucleo 开发板（除了连接到 PB13 引脚的 Nucleo-F302）中，PC13 都连接到 USER 按钮。然而，在我们的示例中不能使用 PWR_WAKEUP_PIN2，因为该引脚在 PCB 上被电阻拉高。当我们将唤醒引脚与待机模式结合使用时，我们并没有使用相应的 GPIO 外设（该外设允许我们配置引脚输入模式），因为在进入待机模式之前它已经断电：唤醒引脚由 PWR 外设直接处理，如果这两个引脚中的任何一个变高，PWR 外设就会复位 MCU。因此，在示例中我们使用 PWR_WAKEUP_PIN1 引脚，在 STM32F072 MCU 中，该引脚对应于 PA0 引脚。

![Image from PDF page 504](../images/page-0504-image-02.jpeg)

图 19.5：如何在 Nucleo 开发板上测量 MCU 的功耗

Nucleo 开发板允许使用 IDD 引脚排针测量 MCU 的电流消耗。在开始测量之前，您应该按照图 19.5 所示建立与开发板的连接，方法是移除 IDD 跳线帽并连接电流表电缆。确保电流表设置为 mA 量程。这样，您就可以看到每种电源模式下的功耗。

![Image from PDF page 504](../images/page-0504-image-03.png)

### 19.3.3 针对 STM32F1 微控制器的重要警告

在开发相关章节中 FreeRTOS 无滴答（tickless）模式的示例时，我遇到了 STM32F103 MCU 在使用 CubeF1 HAL 中的 `HAL_PWR_EnterSTOPMode()` 例程进入停止模式（stop mode）时的一种棘手行为。具体而言，遇到的问题与

<!-- page: 505 -->

## MCU 使用 WFI 指令进入该低功耗模式后，从该模式退出有关。在这种特定场景下，MCU 能够正确进入停止模式，但当其中断唤醒时，会立即产生一个 Hard Fault 异常。我得出结论，ST 的开发人员在进入 Cortex-M3 处理器的低功耗模式时，并未遵循 ARM 的建议，正如此处所述¹⁶。

## 以这种方式修改 HAL 例程解决了该问题：

```text
1
void HAL_PWR_EnterSTOPMode(uint32_t Regulator, uint8_t STOPEntry) {
2
/* Check the parameters */
3
assert_param(IS_PWR_REGULATOR(Regulator));
4
assert_param(IS_PWR_STOP_ENTRY(STOPEntry));
```

5

```text
6
/* Clear PDDS bit in PWR register to specify entering in STOP mode when CPU enter in Deepsle\
7
ep */
8
CLEAR_BIT(PWR->CR,
PWR_CR_PDDS);
```

9

```text
10
/* Select the voltage regulator mode by setting LPDS bit in PWR register according to Regula\
11
tor parameter value */
12
MODIFY_REG(PWR->CR, PWR_CR_LPDS, Regulator);
```

13

```text
14
/* Set SLEEPDEEP bit of Cortex System Control Register */
15
SET_BIT(SCB->SCR, ((uint32_t)SCB_SCR_SLEEPDEEP_Msk));
```

16

```text
17
/* Select Stop mode entry --------------------------------------------------*/
18
if(STOPEntry == PWR_STOPENTRY_WFI)
19
{
20
/* Request Wait For Interrupt */
21
__DSB(); //Added by me
22
__WFI();
23
__ISB(); //Added by me
24
}
25
else
26
{
27
/* Request Wait For Event */
28
__SEV();
29
PWR_OverloadWfe(); /* WFE redefine locally */
30
PWR_OverloadWfe(); /* WFE redefine locally */
31
}
32
/* Reset SLEEPDEEP bit of Cortex System Control Register */
33
CLEAR_BIT(SCB->SCR, ((uint32_t)SCB_SCR_SLEEPDEEP_Msk));
34
}
```

## 该更改仅在于在 WFI 指令之前和之后各添加了一条内存屏障指令，如第 21 行和第 23 行所示。

¹⁶https://bit.ly/3oN7rO5

<!-- page: 506 -->

![Image from PDF page 506](../images/page-0506-image-01.png)

## 19.4 STM32L/G 微控制器的电源管理

STM32L 系列是一个专为低功耗应用定制的广泛 MCU 产品组合。它分为五个主要系列：L0、L1、L4 以及较新的 L4+ 和 L5。这些微控制器比 STM32F 系列提供更多电源模式，能够精确调节 CPU 内核和集成外设消耗的能源。此外，它们提供了特定的低功耗外设（如 LPUART 或 LPTIM 定时器）。在最近的 STM32L5 MCU 中，还集成了开关模式电源（Switched Mode Power Supply, SMPS）降压转换器，减少了外部组件的数量并提高了整体效率。最后，一些最近的 STM32L MCU 提供了为连接到 VBAT 引脚的外部超级电容充电的可能性¹⁷。所有这些特性使得 STM32L MCU 非常适合电池供电设备。

近年来，STM32 产品阵容发生了很大变化，存在不属于低功耗系列但实现了类似功能的 STM32 MCU。STM32G 系列就是这种情况，它在某些 STM32G4 MCU 中提供多达十一种不同的电源模式，且整体电源效率远优于早期的 STM32L1 微控制器。

在本章的这一部分，我们将分析 STM32L/G MCU 提供的最重要的电源管理相关特性，主要关注 STM32L4 系列。

### 19.4.1 电源

图 19.6 展示了 STM32L4 微控制器的电源。如您所见，为了允许精确调节外设消耗的功率，与 STM32F 系列相比，这些 MCU 提供了更多的电压域。

¹⁷ST 在其数据手册中声称 VBAT 引脚可以为电池充电。虽然这在理论上是可能的，但请注意，集成的“充电器”不过是一个连接到 VDD 的限流电阻。这意味着该充电器没有实现任何必要的充电算法，以避免损坏现代电池（如 LiPo 或 NIMH 电池）。因此，除非您决定通过在固件中实现适当的充电策略来构建自己的电池充电器，否则请注意，存在许多专门用于此用途的 IC，成本仅几美分，尤其是如果您关注中国行业的话。

<!-- page: 507 -->

![Image from PDF page 507](../images/page-0507-image-01.jpeg)

图 19.6：STM32L4 微控制器中的电源

即使在这些系列中，VDD 域也是最重要的。它用于为其他电压域供电，例如 VDDIO1 域（用于为大多数 MCU 引脚供电）以及用于为 VCORE 域供电的内部电压调节器。这可以通过软件编程为三种不同的功率范围（scale 1、scale 2 和 scale 3），以根据系统的最大工作频率优化功耗（得益于前面提到的电压缩放技术）。值得注意的是，对于提供 GPIOG 外设的 MCU（即采用高引脚数封装的 MCU），VDDIO2 域用于独立地为 GPIOG 外设供电。该域与 USB 域一起，可以通过 HAL 提供的专用函数（`HAL_PWREx_EnableVddIO2()`、`HAL_PWREx_EnableVddUSB()` 等）选择性启用/禁用。

为了在 VDD 关闭时保持备份寄存器的内容并为 RTC 功能供电，VBAT 引脚可以连接到由电池或其他电源提供的可选备用电压。VBAT 引脚为 RTC 单元、LSE 振荡器以及一个或两个用于从深度睡眠模式唤醒 MCU 的引脚供电，允许 RTC 在主电源关闭时继续运行。因此，VBAT 电源被称为为 RTC 域供电。切换到 VBAT 供电由 PDR 控制。VLCD 引脚用于控制 LCD 的对比度。

<!-- page: 508 -->

### 19.4.2 电源模式

除了允许降低 MCU 中每个组件功耗的专用设计外，STM32L MCU 还向用户提供多达十二种不同的电源模式，如图 19.7 所示。对于前三种电源模式，每 MHz 的功耗值是 CPU 从闪存（flash）和从 SRAM 执行指令时的功耗平均值¹⁸。前三种电源模式基于 Cortex-M 运行模式（run mode），而接下来的五种模式基于睡眠模式（sleep mode）。最后，所有其他低功耗模式都依赖于 Cortex-M 深度睡眠模式（deep sleep mode）。

表 19.2 总结了十种电源模式，并展示了由硬件抽象层（HAL）提供的用于将 MCU 置于相应电源模式的功能。我们将在后文中更深入地分析它们。请注意，并非所有 STM32L/G MCU 都支持所有这些电源模式。在设计固件中的电源转换之前，请务必查阅您的数据手册对应的参考手册。

![Image from PDF page 508](../images/page-0508-image-01.png)

图 19.7：STM32L5 微控制器支持的十二种电源模式

#### 19.4.2.1 运行模式

默认情况下，在上电或系统复位后，STM32L MCU 被置于运行模式。默认时钟源设置为 MSI，这是一种我们在第 10 章中遇到的功耗优化时钟源。STM32L 微控制器为开发人员提供了更精细的调整能力，允许在此模式下降低功耗。如果我们不需要太多的计算能力，那么我们可以保留 MSI 作为主时钟源，从而避免由 PLL 多路复用器引入的功耗。通过将时钟速度降低到 24-26MHz，我们可以配置动态电压

¹⁸图 19.7 中报告的功耗值指的是集成 SMPS 的 STM32L562 系列。

<!-- page: 509 -->

缩放（DVS）等级 2，这在较新的 STM32L MCU 中会将 VCORE 域降低到 1.0V。这种模式也被称为运行范围 2（run range 2），并且可以通过禁用闪存来进一步降低整体功耗。

![Image from PDF page 509](../images/page-0509-image-01.png)

如前所述，在 STM32L/G MCU 以及某些较新的 STM32F4 MCU（如 STM32F446）中，即使在运行模式下也可以禁用闪存。CubeHAL 函数 HAL_- FLASHEx_EnableRunPowerDown() 会自动为我们执行此操作，而 HAL_FLASHEx_DisableRunPowerDown() 例程则重新启用闪存。唯一的条件是，该函数以及所有在闪存关闭时使用的其他例程（包括中断向量）必须放置在 SRAM 中，否则一旦闪存断电，就会立即发生总线错误（Bus Fault）。通过创建自定义链接器脚本可以轻松实现这一点，我们将在第 20 章中看到。因此，ST 工程师将这些例程收集在一个名为 stm32XXxx_hal_flash_ramfunc.c 的单独文件中。

![Image from PDF page 509](../images/page-0509-image-02.jpeg)

表 19.2：STM32L5 MCU 支持的十二种电源模式中的十种

为了进一步降低系统处于运行模式时的能耗，可以将内部电压调节器配置为低功耗模式。在此模式下，系统频率不应超过 2 MHz。HAL_PWREx_EnableLowPowerRunMode() 函数会自动为我们执行此操作。在此模式下，我们最终可以禁用闪存，以进一步降低整体功耗。

<!-- page: 510 -->

从能效角度来看，低功耗运行模式代表了 STM32L MCU 的最佳折衷方案，如图 19.8¹⁹ 所示。如您所见，启用 ART 加速器会增加性能，但也会降低动态功耗。最佳功耗通常是在指令缓存（Instruction Cache）开启、数据缓存（Data Cache）开启且预取缓冲区（Prefetch Buffer）关闭时达到的，因为这种配置减少了闪存访问次数。较小的闪存动态功耗使得每次固件需要访问闪存时都能保持较小的功耗。SRAM1 和 SRAM2 的功耗相当相似，但当 SRAM2 未重映射到地址 0 时，由于其 0 等待状态访问特性，SRAM2 比 SRAM1 更具能效。

![Image from PDF page 510](../images/page-0510-image-01.jpeg)

图 19.8：STM32L4 系列中的功耗优化与频率关系

#### 19.4.2.2 睡眠模式

睡眠模式允许使用所有外设，同时提供最快的唤醒时间。在这些模式下，CPU 停止运行，并且每个外设时钟都可以通过软件配置，在睡眠模式和低功耗睡眠模式期间被门控开启（ON）或关闭（OFF）。这些模式通过执行汇编指令 WFI 或 WFE 进入。为了将 MCU 置于两种睡眠模式之一，CubeHAL 提供了以下函数：

```text
void HAL_PWR_EnterSLEEPMode(uint32_t Regulator, uint8_t SLEEPEntry);
```

第一个参数 Regulator 可以接受值 PWR_MAINREGULATOR_ON 和 PWR_LOWPOWERREG- ULATOR_ON：前者将 MCU 置于睡眠模式，后者置于低功耗睡眠模式。第二个参数 SLEEPEntry 可以取值 PWR_SLEEPENTRY_WFI 或 PWR_SLEEPENTRY_WFE：顾名思义，前者执行 WFI 指令，后者执行 WFE 指令。

¹⁹图 19.8 取自此 ST 官方文档(https://bit.ly/3FwfEfA)。ST 还提供了一份关于 STM32L4 MCU 功耗优化的有用应用笔记，即 AN4746(https://bit.ly/3FAKKCy)。

<!-- page: 511 -->

仔细阅读

![Image from PDF page 511](../images/page-0511-image-01.png)

请注意，对于 STM32L MCU，在此电源模式下系统频率不应超过 MSI 范围 1 的值。有关电压调节器和外设工作条件的更多详细信息，请参阅产品数据手册。

如果使用 WFI 指令进入睡眠模式，任何由 NVIC 确认的外设中断都可以将设备从睡眠模式中唤醒。如果使用 WFE 指令进入睡眠模式，一旦发生事件，MCU 就会退出睡眠模式。唤醒事件可以由以下情况生成：

- 在外设控制寄存器中启用中断，但在 NVIC 中未启用，并在系统控制寄存器（System Control Register）中启用 SEVONPEND 位 - 当 MCU 从 WFE 恢复时，必须清除外设中断挂起位和外设 NVIC IRQ 通道挂起位（在 NVIC 中断清除挂起寄存器中）；
- 或者将外部或内部 EXTI 线配置为事件模式 - 当 CPU 从 WFE 恢复时，由于对应于事件线的挂起位未被设置，因此不需要清除外设中断挂起位或 NVIC IRQ 通道挂起位。

退出低功耗睡眠模式后，MCU 会自动被置于低功耗运行模式。

##### 19.4.2.2.1 批量采集模式

批量采集模式（Batch Acquisition Mode, BAM）是一种隐式且优化的数据传输模式。在睡眠模式下，仅配置所需的通信外设（例如 I²C）、一个直接存储器访问（DMA）以及 SRAM 的时钟使能。闪存（Flash）存储器进入掉电模式，并且在睡眠模式下闪存时钟被门控关闭。微控制器（MCU）可以进入睡眠模式或低功耗睡眠模式。请注意，即使在低功耗睡眠模式下，I²C 时钟也可以设置为 16 MHz，从而支持 1 MHz 快速模式加（fast-mode plus）。USART 和 LPUART 时钟也可以基于 HSI 振荡器。BAM 的典型应用是传感器集线器。

#### 19.4.2.3 停止模式

STM32L/G 微控制器可提供多达 2 种不同的停止模式，分别命名为 stop1 和 stop2。停止模式基于 Cortex-M 深度睡眠模式并结合外设时钟门控实现。电压调节器可配置为正常²⁰或低功耗模式。在 stop1 模式下，VCORE 域中的所有时钟均停止；PLL、MSI、HSI16 和 HSE 振荡器被禁用。具有唤醒能力的某些外设（I²C、USART 和 LPUART）可以开启 HSI16 以接收帧，并在接收帧后关闭 HSI16，如果该帧不是唤醒帧。在这种情况下，HSI16 时钟仅传播到请求它的外设。SRAM1、SRAM2 和寄存器内容得以保留。在 stop1 模式下，多个外设可以正常工作：PVD、LCD 控制器，

²⁰HAL 将此模式称为 stop0，并通过调用 HAL_PWREx_EnterSTOP0Mode() 函数实现。

<!-- page: 512 -->

数模转换器、运算放大器、比较器、独立看门狗、LPTIM 定时器（如果可用）、I²C、UART 和 LPUART。stop2 与 stop1 模式的区别在于，仅以下外设可用：PVD、LCD 控制器、比较器、独立看门狗、LPTIM1、I2C3 和 LPUART。

BOR 在 stop1 和 stop2 模式下始终可用。当使用高于 VBOR0 的阈值时，功耗会增加。

要将微控制器置于停止模式，HAL 提供了以下函数：

```text
void HAL_PWREx_EnterSTOPxMode(uint8_t STOPEntry);
```

其中 ‘x’ 根据停止模式等于 0、1 或 2。参数 STOPEntry 可以取值为 PWR_STOPENTRY_WFI 或 PWR_STOPENTRY_WFE。为了与其他 HAL 兼容，也可以使用 HAL_PWR_EnterSTOPMode()。

要进入停止模式，必须复位所有 EXTI 线挂起位、所有外设中断挂起位以及 RTC 闹钟标志。否则，停止模式进入过程将被忽略，程序执行将继续。可以从运行模式和低功耗运行模式进入 stop1 模式，但不能从低功耗运行模式进入 stop2 模式。

任何配置为中断或事件模式的 EXTI 线都会强制 CPU 退出停止模式，具体取决于它是使用 WFI 还是 WFE 指令进入低功耗模式的。由于在进入停止模式之前 HSE 和 PLL 均被禁用，因此当退出此低功耗模式时，微控制器的源时钟被设置为 HSI。这意味着我们的代码必须根据所需的 SYSCLK 速度重新配置时钟树。

#### 19.4.2.4 待机模式

STM32L/G 微控制器提供两种待机模式，它们基于 Cortex-M 深度睡眠模式。待机模式是最低功耗模式，在此模式下可保留 32 Kbytes 的 SRAM2，支持从 VDD 到 VBAT 的自动切换，并且 I/O 电平可以通过独立的上拉和下拉电路进行配置。默认情况下，电压调节器处于掉电模式，SRAM 和外设寄存器内容丢失。128 字节的备份寄存器始终保留。超低功耗 BOR 始终开启，以确保无论 VDD 斜率如何都能安全复位。

要将微控制器置于待机模式，HAL 提供了以下函数：

```text
void HAL_PWR_EnterSTANDBYMode(void);
```

如果我们希望保留 32 Kbytes 的 SRAM2，则可以调用以下函数：

```text
void HAL_PWREx_EnableSRAM2ContentRetention(void);
```

<!-- page: 513 -->

```text
before we call the HAL_PWR_EnterSTANDBYMode();
```

在 STM32L 微控制器中，每个 I/O 都可以通过调用 HAL 函数 HAL_PWREx_EnablePullUpPullDownConfig() 配置为带或不带上拉或下拉电阻。这允许在待机模式下控制外部组件的输入状态。有关此主题的更多信息，请参阅您的微控制器参考手册。

当发生外部复位（NRST 引脚）、IWDG 复位、任一已使能的 WKUPx 引脚上的上升沿或 RTC 事件时，微控制器退出待机模式。从待机模式唤醒后，除电源控制/状态寄存器（PWR->CSR）外，所有寄存器均被复位。从待机模式唤醒后，程序执行以与复位后相同的方式重新开始（启动引脚采样、选项字节加载、获取复位向量等）。使用宏：

```text
__HAL_PWR_GET_FLAG(PWR_FLAG_SB);
```

我们可以检查微控制器是否因退出待机模式而复位。由于在进入停止模式之前 HSE 和 PLL 均被禁用，因此当退出此低功耗模式时，微控制器的源时钟被设置为 HSI。这意味着我们的代码必须根据所需的 SYSCLK 速度重新配置时钟树。

#### 19.4.2.5 关机模式

关机模式是功耗最低的模式，在 RTC 关闭的情况下，STM32L5 微控制器在 1.8 V 电压下仅消耗 3.4 nA。此模式与待机模式类似，但不具备任何电源监控功能：在此模式下，欠压复位（BOR）被禁用，且不支持切换到 VBAT。LSI 不可用，因此独立看门狗也不可用。当器件退出关机模式时，会产生欠压复位（Brown-Out Reset）：除备份域中的寄存器外，所有寄存器均被复位，并在引脚上产生复位信号。128 字节的备份寄存器在关机模式下得以保留。退出关机模式时，唤醒时钟为 4 MHz 的 MSI。

要进入关机模式，HAL 提供了以下函数：

```text
void HAL_PWREx_EnterSHUTDOWNMode(void);
```

当发生外部复位（NRST 引脚）、任一已使能的 WKUPx 引脚出现上升沿或 RTC 事件时，微控制器将退出关机模式。从待机模式唤醒后，所有寄存器均被复位，包括电源控制/状态寄存器（PWR->CSR）。从关机模式唤醒后，程序执行将以与复位后相同的方式重新开始（采样启动引脚、加载选项字节、获取复位向量等）。

### 19.4.3 电源模式转换

STM32L/G 微控制器提供了多种电源模式。然而，需要注意的是，从给定的模式出发，并非可以到达所有电源模式，电源模式转换是受限的。

<!-- page: 514 -->

图 19.9 展示了 STM32L4 微控制器中有效的电源模式转换。如图所示，从运行模式可以访问除低功耗睡眠模式外的所有低功耗模式。要进入低功耗睡眠模式，必须先切换到低功耗运行模式，然后在调节器处于低功耗状态时执行 WFI 或 WFE 指令。另一方面，当退出低功耗睡眠模式时，STM32L4 处于低功耗运行模式。当器件处于低功耗运行模式时，可以进入除睡眠模式和 stop2 模式外的所有低功耗模式。Stop2 模式只能从运行模式进入。如果器件从低功耗运行模式进入 Stop1 模式，它将退出至低功耗运行模式。如果器件从低功耗运行模式进入待机模式或关机模式，它将退出至运行模式。

![Image from PDF page 514](../images/page-0514-image-01.jpeg)

图 19.9：STM32L4 微控制器中允许的电源模式转换

### 19.4.4 低功耗外设

几乎所有较新的 STM32 系列（如 STM32L、STM32G、STM32H 以及最新的 STM32U）都提供了专用的低功耗外设。这里简要介绍这些外设。

#### 19.4.4.1 LPUART

低功耗 UART（LPUART）是一种允许双向 UART 通信且功耗有限的 UART。仅需 32.768 kHz 的 LSE 时钟即可支持高达 9600 波特率的 UART 通信。当 LPUART 由不同于 LSE 时钟的时钟源驱动时，可以达到更高的波特率。即使微控制器处于停止模式，LPUART 也可以以极低的能耗等待传入的 UART 帧。LPUART 包含所有必要的硬件支持，以便以最小功耗实现异步串行通信。它支持半双工单线通信和调制解调器操作（CTS/RTS）。它还支持多处理器通信。即使在 stop 2 模式下，也可以使用直接存储器访问（DMA）进行数据传输/接收。

要编程 LPUART 外设，我们使用 HAL_UART 模块中的相同函数。

<!-- page: 515 -->

#### 19.4.4.2 LPTIM

低功耗定时器（LPTIM）是一款 16 位定时器，受益于功耗降低方面的最新发展。得益于其多样的时钟源，无论选择何种电源模式，LPTIM 都能保持运行，这与在停止模式下不运行的标准 STM32 定时器不同。鉴于其即使在没有内部时钟源的情况下也能运行的能力，LPTIM 可用作脉冲计数器，这在某些应用中非常有用。此外，LPTIM 从低功耗模式唤醒系统的能力使其非常适合实现具有极低功耗的超时功能。在第 23 章关于 FreeRTOS 的内容中，我们将使用 LPTIM 定时器作为无滴答空闲模式（tickless idle mode）的时间基准源。LPTIM 引入了一种灵活的时钟方案，在最小化功耗的同时提供所需的功能和性能。

LPTIM 外设的相关特性如下：

- 16 位向上计数器
- 3 位预分频器，具有 8 种可能的分频系数（1, 2, 4, 8, 16, 32, 64, 128）
- 可选时钟源

- – 内部时钟源：LSE、LSI、HSI16 或 APB 时钟 – 通过 ULPTIM 输入的外部时钟源（在无 LP 振荡器运行时工作，用于脉冲计数器应用）
- 16 位周期寄存器
- 16 位比较寄存器
- 连续/单次模式
- 可选软件/硬件输入触发
- 可配置输出：脉冲、PWM
- 可配置 I/O 极性
- 编码器模式

要编程 LPTIM 定时器，我们使用专用的 HAL_LPTIM 模块。

#### 19.4.4.3 LPGPIO

ST 在 2021 年第三季度推出了一款面向超低功耗应用的新 STM32 系列：STM32U。STM32U5 系列提供基于 Cortex-M33 的高级省电微控制器，旨在满足智能应用（包括可穿戴设备、个人医疗设备、家庭自动化和工业传感器）最严苛的功耗/性能要求。在撰写本章时，市场上尚未提供开发板，且 STM32U5 的 CubeHAL 也未发布。

与 STM32L/G 系列相比，STM32U5 系列提供了新的低功耗外设。低功耗 GPIO (LPGPIO) 允许在停止模式（低至 Stop 2 模式）下进行 I/O 控制，并使用直接存储器访问 (DMA) 进行存储器到存储器的传输。LPGPIO 设计用于与 GPIO 配合使用。

LPGPIO 的主要特性可总结如下：

<!-- page: 516 -->

- 在低至 Stop 2 模式的低功耗模式下控制 16 个 I/O。
- 安全的时钟和复位管理。
- 从输出数据寄存器 (LPGPIO_ODR) 输出数据。
- 向输入数据寄存器 (LPGPIO_IDR) 输入数据。
- 位设置和复位寄存器 (LPGPIO_BSRR)，用于对 LPGPIO_ODR 进行按位写访问。
- TrustZone 安全支持。

#### 19.4.4.4 LPDMA

STM32U 系列提供即使在 Stop 3 模式下也能工作的 DMA，允许在内核 (Cortex-M core) 停止时进行存储器与外设之间的传输。此外，LPDMA 能够执行外设到外设的传输，并在睡眠和停止模式下进行自主数据传输。

## 19.5 电源监控器

大多数 STM32 微控制器提供两个电源监控器：BOR 和 PVD。欠压复位 (Brownout Reset, BOR) 是一个单元，它在电源电压达到指定的 VBOR 阈值之前保持微控制器处于复位状态。VBOR 通过器件选项字节进行配置。默认情况下，BOR 处于关闭状态。用户可以选择三到五个可编程的 VBOR 阈值级别。有关 BOR 特性的完整详细信息，请参阅器件数据手册中的“电气特性”部分。不提供 BOR 单元的 STM32 器件通常具有一个名为上电复位 (Power on Reset, POR)/掉电复位 (Power Down Reset, PDR) 的类似单元，它们执行与 BOR 单元相同的功能，但具有固定的、出厂配置的电压阈值。

固件可以通过使用可编程电压检测器 (Programmable Voltage Detector, PVD) 主动监控电源。PVD 允许配置要监控的电压，如果该 VDD 高于或低于给定级别，则电源控制/状态寄存器 (PWR->CSR) 中相应的位会被置位。如果配置得当，MCU 可以通过 EXTI 控制器生成专用的中断请求 (IRQ)。对于具有此功能的 MCU，HAL 提供 HAL_PWR_EnablePVD()/HAL_PWR_DisablePVD() 函数来启用/禁用 PVD，并提供 HAL_PWR_ConfigPVD() 函数来配置电压级别。更多信息，请参阅 CubeHAL 的 HAL_PWREx 模块。

BOR/POR/PDR 和 PVD 都主动监控 VDD，并将其与给定的阈值级别进行比较。最近的 STM32L 微控制器提供四个外设电压监控 (Peripheral Voltage Monitoring, PVM)，用于监控其他外设电源域。四个 PVMx 中的每一个都是固定阈值 VPVMx 与所选电源之间的比较器。表 19.3 总结了 PVMx 的特性，包括监控的电源域和电压级别。每个 PVM 输出都连接到一个 EXTI 线，如果通过 EXTI 寄存器启用，则可以生成中断。在具有 PVM 支持的 STM32 MCU 中，此 IRQ 与 PVD 共享。当独立电源降至 PVMx 阈值以下和/或升至 PVMx 阈值以上时，根据 EXTI 线上升/下降沿配置，会生成 PVMx 输出中断。每个 PVM 可以在 Stop 0、Stop 1 和 Stop 2 模式下保持活动状态，并且 PVM 中断可以从任何停止模式中唤醒。

<!-- page: 517 -->

表 19.3：PVMx 特性

PVM 电源 PVM 阈值 EXTI 线 PVM1 VDDUSB VPVM1 (约 1.2 V) 35 PVM2 VDDIO2 VPVM2 (约 0.9 V) 36 PVM3 VDDA VPVM3 (约 1.65 V) 37 PVM4 VDDA VPVM4 (约 1.8 V) 38

要配置 PVM，CubeHAL 提供 HAL_PWREx_ConfigPVM() 例程，而要选择性启用/禁用其中一个 PVMx，则提供 HAL_PWREx_EnablePVMx()/HAL_PWREx_DisablePVMx()。更多信息，请参阅 CubeL5 文档。

## 19.6 低功耗模式下的调试

默认情况下，如果应用程序在使用调试功能时将 MCU 置于睡眠、停止和待机模式，调试连接将丢失。这是因为 Cortex-M 内核不再有时钟。然而，通过设置 MCU 调试组件 (DBGMCU) 的 DBGMCU_CR 寄存器中的某些配置位，即使大量使用低功耗模式，也可以调试软件。

CubeHAL 提供方便的函数来启用/禁用低功耗模式下的调试模式。函数 HAL_DBGMCU_EnableDBGSleepMode() 用于在睡眠模式期间启用调试²¹；函数 HAL_DBGMCU_EnableDBGStopMode() 和 HAL_DBGMCU_EnableDBGStandbyMode() 分别允许在停止和待机模式期间使用调试接口。

重要的是要注意，如果我们想在低功耗模式下调试 MCU，我们还必须保持对应于 SWDIO/SWO/SWCLK 引脚的 GPIO 外设开启。在所有 Nucleo 板上，这些引脚与 PA13、PA14 和 PB3 重合。

请注意，在启用低功耗模式下的 MCU 调试之前，必须通过调用 __HAL_RCC_DBGMCU_CLK_ENABLE() 宏来启用 DBGMCU 接口。

![Image from PDF page 517](../images/page-0517-image-01.png)

## 19.7 使用 CubeMX 功耗计算器

手动估算微控制器的功耗可能是一场噩梦，尤其是在启用了多个外设且在不同电源模式下存在多种转换状态的情况下。即使 MCU 数据手册提供了所有必要信息，要确定确切的功耗水平仍然很困难。

²¹在 STM32F0 微控制器中，睡眠模式下的调试不可用，因此 HAL 未提供相应的 HAL 函数。

<!-- page: 518 -->

CubeMX 提供了一个名为功耗计算器（Power Consumption Calculator, PCC）的便捷工具，它允许我们构建电源序列并对 MCU 功耗进行估算。

![Image from PDF page 518](../images/page-0518-image-01.jpeg)

图 19.10：功耗计算器主视图

图 19.10 展示了 PCC 的主视图。要使用它，我们首先必须选择 Vdd 电源源，否则该工具不允许我们在电源序列中创建步骤。下一个可选步骤是选择用于在主电源缺失时为 MCU 供电的电池。这对于评估电池寿命非常有用。我们可以从一系列知名电池中选择，或者添加自定义电池。

通过点击绿色的“New Step”（新步骤），我们可以添加序列中的一个步骤。在这里，我们可以指定电源模式（运行、睡眠等）、存储器配置（Flash 启用/禁用、ART 启用/禁用等）以及电源电压水平。从同一个对话框中，我们还可以选择 CPU 频率、步骤持续时间以及启用的外设。

使用此工具，我们可以确定微控制器需要多少功耗。在 STM32L/G MCU 中，还可以启用“Transitions Checker”（转换检查器），它允许识别无效的转换状态（例如，我们不能从运行模式直接切换到低功耗睡眠模式，而不经过低功耗运行模式）。有关 PCC 视图的更多信息，请参阅 ST 的 UM1718²²。

²²https://bit.ly/3k8HeE2

<!-- page: 519 -->

## 19.8 案例研究：在低功耗模式下使用看门狗定时器

IWDG 和 WWDG 定时器一旦启动就无法停止。WWDG 定时器会一直计数直到停止模式，而 IWDG 定时器由于由 LSI 振荡器提供时钟，即使在关机模式下也能工作。这意味着看门狗定时器会阻止 MCU 长时间停留在低功耗模式下。

如果您的应用程序需要同时使用看门狗定时器和低功耗模式，则需要遵循以下技巧，该技巧基于 SRAM 存储器内容在连续复位后得以保留这一事实（显然，它无法在电源开启复位后保留）。因此，为了在保持低功耗模式的同时跟踪由看门狗定时器引起的复位，您可以使用一个变量来跟踪这一事实（例如，在进入低功耗模式之前，将 uint32_t 变量的内容设置为特殊的“密钥”值）。一旦 MCU 复位，您可以检查该变量的内容，如果该变量已相应配置，则可以避免启动看门狗定时器。

然而，我们需要一个“安全”的位置来存储此变量，否则它很可能会被启动例程覆盖。因此，最好的做法是减少 mem.ld 文件中 SRAM 区域的大小，并将此哨兵变量放置在 SRAM 存储器的末尾，通常主堆栈（main stack）就在那里开始：

```text
volatile uint32_t *lpGuard = (0x20000000 + SRAM_SIZE);
```

例如，假设有一个具有 8KB SRAM 的 STM32F030R8 MCU，并且假设我们在 mem.ld 文件中以如下方式定义 SRAM 区域：

```text
MEMORY {
FLASH (rx)
: ORIGIN = 0x08000000, LENGTH = 64K
SRAM (xrw)
: ORIGIN = 0x20000000, LENGTH = 8K - 4
}
```

那么宏 SRAM_SIZE 将等于 0x2000-4 = 0x1FFC。lpGuard 变量的内容将放置在地址 0x2000 1FFC 处。

我知道这些概念可能看起来完全晦涩难懂。一旦您阅读了下一章关于 STM32 应用程序内存布局的内容，许多事情将会得到澄清。
