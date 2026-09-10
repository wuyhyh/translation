<!-- page: 293 -->

# 11. 定时器

嵌入式设备基于时间执行某些活动。对于非常简单且不精确的延时，忙等待循环（busy loop）可以完成任务，但使用 CPU 内核来执行与时间相关的活动从来都不是明智的解决方案。因此，所有微控制器都提供了专用的硬件外设：定时器。定时器不仅是时基发生器，还提供多种附加功能，用于与 Cortex-M 内核以及 MCU 内部和外部的其他外设进行交互。

根据所使用的系列和封装，STM32 微控制器实现了可变数量的定时器，每个定时器具有特定的特性。某些型号最多可提供 14 个独立的定时器。与其他外设不同，定时器在所有 STM32 系列中几乎具有相同的实现方式，并被归入九个不同的类别。其中最重要的是：基本定时器、通用定时器和高级定时器。

STM32 定时器是一种功能强大的外设，提供广泛的定制选项。此外，其中一些功能特定于应用领域。深入探讨这一主题需要一本完全独立的书籍（你需要考虑到，通常典型的 STM32 数据手册中超过 250 页的内容都专门用于定时器）。本章无疑是本书中最长的章节之一，旨在梳理 STM32 MCU 中基本定时器和通用定时器最相关的概念，并参考用于编程它们的 CubeHAL 模块。

## 11.1 定时器简介

定时器是一个自由运行的计数器，其计数频率是其源时钟的一个分数。可以使用每个定时器专用的预分频器来降低计数速度¹。根据定时器类型，它可以由内部时钟（派生自其所连接的总线）、外部时钟源或用作“主”定时器的另一个定时器进行时钟驱动。

通常，定时器从零计数到给定值，该值不能高于其分辨率的最大无符号值（例如，16 位定时器在计数器达到 65535 时溢出），但它也可以反向计数，以及以我们将在下文看到的其他方式计数。

STM32 微控制器中最先进的定时器具有多种功能：

- 它们可以用作时基发生器（这是所有 STM32 定时器的共同功能）。
- 它们可以用于测量外部事件的频率（输入捕获模式）。
- 用于控制输出波形，或指示一段时间已过（输出比较模式）。

¹这并不完全正确，但在这里将其视为正确是可以接受的。

<!-- page: 294 -->

- 单脉冲模式（OPM）是输入捕获模式和输出比较模式的一个特例。它允许计数器在响应刺激时启动，并在可编程延时后生成长度可编程的脉冲。
- 在每个通道上独立地生成边沿对齐模式或中心对齐模式的 PWM 信号（PWM 模式）。

– 在某些 STM32 MCU 中（特别是 STM32F3 和较新的 STM32L4 系列），某些定时器可以生成具有可编程延时和相位偏移的中心对齐 PWM 信号。

根据定时器类型，当发生以下事件时，定时器可以生成中断或直接存储器访问（direct memory access, DMA）请求：

- 更新事件

- – 计数器上溢/下溢 – 计数器初始化 – 其他
- 触发

- – 计数器启动/停止 – 计数器初始化 – 其他
- 输入捕获/输出比较

### 11.1.1 STM32 MCU 中的定时器类别

STM32 定时器主要可分为九个类别。让我们简要查看每一个类别。

- 基本定时器：该类别的定时器是 STM32 MCU 中最简单的定时器形式。它们是用作时基发生器的 16 位定时器，没有输出/输入引脚。基本定时器还用于为 DAC 外设提供数据，因为其更新事件可以触发 DAC 的 DMA 请求（因此，它们通常存在于至少提供一个 DAC 的 STM32 MCU 中）。基本定时器也可以用作其他定时器的“主”定时器。
- 通用定时器：它们是 16/32 位定时器（取决于 STM32 系列），提供了现代嵌入式微控制器定时器预期实现的经典功能。它们用于任何应用中的输出比较（定时和延时生成）、单脉冲模式、输入捕获（用于外部信号频率测量）、传感器接口（编码器、霍尔传感器）等。显然，通用定时器可以像基本定时器一样用作时基发生器。该类别的定时器提供四个可编程输入/输出通道。

– 1 通道/2 通道：它们是通用定时器的两个子组，仅提供一个/两个输入/输出通道。

<!-- page: 295 -->

- – 带一个互补输出的 1 通道/2 通道：与前面的类型相同，但在一个通道上具有死区时间发生器。这使得能够拥有与高级定时器时基独立的互补信号。
- 高级定时器：这些定时器是 STM32 MCU 中最完整的定时器。除了通用定时器的功能外，它们还包括与电机控制和数字电源转换应用相关的多种功能：具有死区时间插入的三个互补信号、紧急停机输入。
- 高分辨率定时器：高分辨率定时器（HRTIM1）是由 STM32F3/G4 系列（这些系列专门用于电机控制和电源转换）和 STM32H7 系列中的某些微控制器提供的特殊定时器。它允许生成具有高精度定时的数字信号，例如 PWM 或相位偏移脉冲。它由 6 个子定时器组成，1 个主定时器和 5 个从定时器，总共 10 个高分辨率输出，可以成对耦合以插入死区时间。它还具有 5 个故障输入用于保护目的，以及 10 个输入用于处理外部事件，如电流限制、零电压或零电流切换。HRTIM1 定时器由以核心速度时钟的数字内核（digital kernel）后接延迟线组成。具有闭环控制的延迟线保证了无论电压、温度或芯片间制造工艺偏差如何，都能达到 217ps 的分辨率。在所有工作模式下（可变占空比、可变频率和恒定导通时间），10 个输出均可用高分辨率。本书不会涵盖 HRTIM1 定时器。ST 提供了一份撰写良好的应用笔记 AN4539²，涵盖了 HRTIM 定时器的所有方面。
- 低功耗定时器：该组定时器专门针对低功耗应用设计。得益于其多样的时钟源，这些定时器能够在所有电源模式下保持运行（待机模式除外）。鉴于这种即使在没有内部时钟源的情况下也能运行的能力，低功耗定时器可以用作“脉冲计数器”，这在某些应用中很有用。它们还具有从低功耗模式唤醒系统的能力。

²https://bit.ly/2YjCdmM

<!-- page: 296 -->

![Image from PDF page 296](../images/page-0296-image-01.png)

表 11.1：每个定时器类别的最相关特性

表 11.1³ 总结了每个定时器类别需要牢记的最相关特性。

### 11.1.2 STM32 系列中定时器的有效可用性

并非所有类型的定时器都存在于所有 STM32 微控制器中。这主要取决于 STM32 系列、销售类型以及所使用的封装。表 11.2 总结了所有 STM32 家族中 22 个定时器的分布情况。星号表示该定时器并非在该系列的所有微控制器中都可用。

³该表改编自 ST 的应用笔记 AN4013(http://bit.ly/1WAewd6)，这是一份专门介绍 STM32 定时器的文档，建议在本章阅读期间随时备查。

<!-- page: 297 -->

![Image from PDF page 297](../images/page-0297-image-01.png)

表 11.2：每个 STM32 系列实现了哪些定时器

### 关于表 11.2，有几点需要特别指出：

- 对于特定的定时器（例如 TIM1、TIM8 等），其实现方式（功能、寄存器数量和类型、生成的中断、DMA 请求、外设互连⁴等）在所有 STM32 微控制器中都是相同的⁵。这保证了为使用特定定时器而编写的固件可以移植到拥有相同定时器的其他微控制器或 STM32 系列上。
- 某个属于特定家族微控制器中定时器的实际存在与否，取决于销售类型和所使用的封装（引脚更多的封装可能会提供该家族实现的所有定时器

⁴术语“外设互连”指的是某些外设能够“触发”其他外设，或触发其部分 DMA 请求的能力（例如，TIM6 的更新事件可以触发 DAC1 的转换）。有关此主题的更多信息，请参阅第 13 章。⁵如本章开头所述，STM32 定时器是唯一在所有 STM32 家族中共享相同实现的外设。这几乎完全正确，除了 TIM2 和 TIM5 定时器，它们在大多数 STM32 微控制器中具有 32 位分辨率，而在一些早期 STM32 微控制器中为 16 位分辨率。此外，某些特定功能在不同 STM32 系列之间（尤其是较旧的 STM32F1 微控制器与较新的 STM32 微控制器之间）的实现可能略有不同。在计划使用某些定时器提供的专用功能之前，请务必查阅您微控制器的数据手册。

<!-- page: 298 -->

- 该家族）。
- 该表是从 AN4013⁶ 中提取、扩展并重新排列的。我仔细核对了该表中报告的数值，发现了一些未更新的内容。然而，我并不完全确定它是否忠实地反映了整个 STM32 产品组合的实际实现⁷（要确保这些数值的准确性，我需要检查超过 1500 个微控制器）。因此，我留了一些单元格为空，以便如果您发现错误，可以最终添加数值⁸。

表 11.3 报告了本书中考虑的九个 Nucleo 板所配备的微控制器实现的所有定时器列表。表 11.3 中报告的几点内容值得强调：

- STM32F401RE 和 STM32F103RB 不提供基本定时器。
- “最大时钟速度”列报告了给定 STM32 微控制器中所有定时器的最大时钟速度。这意味着定时器的最大时钟速度取决于其连接的总线。请务必查阅数据手册以确定定时器连接到哪条总线（参见数据手册中的外设映射部分），并使用 CubeMX 时钟配置视图来确定配置的总线速度。
- STM32G474RE 微控制器于 2021 年初推向市场，实现了 STM32L 和 STM32F3 系列特有的两个功能：低功耗定时器和高分辨率定时器。

在处理定时器时，采取务实的方法非常重要。否则，很容易迷失在其设置和相应的 HAL 例程中（HAL_TIM 和 HAL_TIM_EX 模块是 CubeHAL 中最复杂的模块之一）。因此，我们将开始研究如何使用基本定时器，其功能也是更高级 STM32 定时器的通用功能。

⁶https://bit.ly/1WAewd6 ⁷该表整理于 2021 年 9 月。STM32 微控制器几乎每天都在演进，因此当您阅读本章时，某些内容可能已经发生变化。⁸并最终给我发一封电子邮件，以便我可以在本书的后续版本中更正该表 :-)

<!-- page: 299 -->

![Image from PDF page 299](../images/page-0299-image-01.png)

表 11.3：配备九个 Nucleo 板的每个 STM32 微控制器实现了哪些定时器

## 11.2 基本定时器

基本定时器 TIM6、TIM7 和 TIM18⁹ 是 STM32 产品组合中可用的最简单的定时器。尽管并非所有 STM32 微控制器都提供它们，但需要强调的是，STM32 定时器的设计使得更高级的定时器以相同的方式实现了功能较弱的定时器的相同功能，如图 11.1 所示。这意味着完全可以使用通用定时器以与基本定时器相同的方式工作。CubeHAL 也反映了这种硬件实现：对所有定时器执行的基本操作都是使用 HAL_TIM_Base_XXX 函数完成的。

通过使用 C 结构体 TIM_HandleTypeDef 的实例来引用单个定时器，其定义如下：

⁹TIM18 基本定时器仅在 STM32F37x 微控制器中可用。

<!-- page: 300 -->

```text
typedef struct {
TIM_TypeDef
*Instance;
/* 指向定时器描述符的指针
*/
TIM_Base_InitTypeDef
Init;
/* TIM 时间基准所需参数 */
HAL_TIM_ActiveChannel
Channel;
/* 活动通道
*/
DMA_HandleTypeDef
*hdma[7];
/* DMA 句柄数组
*/
HAL_LockTypeDef
Lock;
/* 锁定对象
*/
__IO HAL_TIM_StateTypeDef
State;
/* TIM 操作状态
*/
} TIM_HandleTypeDef;
```

![Image from PDF page 300](../images/page-0300-image-01.png)

图 11.1：三大类定时器之间的关系

让我们更深入地看看这个结构体中最重要的字段。

- Instance：是指向我们要使用的 TIM 描述符的指针。例如，TIM6 是大多数 STM32 微控制器中可用的基本定时器之一。
- Init：是 C 结构体 TIM_Base_InitTypeDef 的一个实例，用于配置基本定时器的功能。我们稍后会深入研究它。
- Channel：指示那些提供一个或多个输入/输出通道的定时器中活动通道的数量（基本定时器不属于这种情况）。它可以取枚举 HAL_TIM_ActiveChannel 中的一个或多个值，我们将在下一段中研究其用法。
- *hdma[7]：这是一个数组，包含指向与定时器关联的 DMA 请求的 DMA_HandleTypeDef 描述符的指针。如后文所述，一个定时器最多可以生成七个 DMA 请求。
- State：这是 HAL 内部用于跟踪定时器状态的字段。

所有定时器配置活动都是使用 C 结构体 TIM_Base_InitTypeDef 的实例完成的，其定义如下：

<!-- page: 301 -->

```text
typedef struct {
uint32_t Prescaler;
/* 指定用于分频 TIM 时钟的分频器值。 */
uint32_t CounterMode;
/* 指定计数器模式。
*/
uint32_t Period;
/* 指定要在下一次更新事件时加载到活动
自动重载寄存器中的周期值。
*/
uint32_t ClockDivision; /* 指定时钟分频。
*/
uint32_t RepetitionCounter; /* 指定重复计数器值。
*/
} TIM_Base_InitTypeDef;
```

- 预分频器（Prescaler）：它将定时器时钟除以 1 到 65535 之间的一个因子（这意味着预分频器寄存器具有 16 位分辨率）。例如，如果定时器所连接的总线运行频率为 48MHz，那么将预分频器值设置为 48 会将计数频率降低到 1MHz。
- 计数模式（CounterMode）：它定义了定时器的计数方向，可以取表 11.4 中的任一值。某些计数模式仅在通用定时器和高级定时器中可用。对于基本定时器，仅定义了 TIM_COUNTERMODE_UP。
- 周期（Period）：设置定时器计数器在重新开始计数前的最大值。对于 16 位定时器，该值可以从 0x1 到 0xFFFF（65535）；对于将 TIM2 和 TIM5 实现为 32 位定时器的微控制器（MCU），该值可以从 0x1 到 0xFFFF FFFF。如果 Period 设置为 0x0，定时器将不会启动。
- 时钟分割（ClockDivision）：此位域指示内部定时器时钟频率与 ETRx 和 TIx 引脚上数字滤波器使用的采样时钟之间的分割比。请注意，它与馈送定时器的时钟频率无关。这是 STM32 初学者常见的混淆点。ClockDivision 可以取表 11.5 中的一个值，并且仅在通用定时器和高级定时器中可用。我们将在本章稍后研究定时器输入引脚上的数字滤波器。此字段也被死区发生器使用（本书未描述该功能）。
- 重复计数器（RepetitionCounter）：每个定时器都有一个特定的更新寄存器，用于跟踪定时器的溢出/下溢状态。如我们接下来将看到的，这也可以生成特定的中断请求（IRQ）。RepetitionCounter 指定在更新寄存器被置位并引发相应事件（如果已启用）之前，定时器溢出/下溢的次数。RepetitionCounter 仅在高级定时器中可用。

表 11.4：定时器可用的计数模式

计数模式 描述

TIM_COUNTERMODE_UP 定时器从零计数到 Period 值（该值不能高于定时器分辨率 - 16/32 位），然后生成溢出事件。 TIM_COUNTERMODE_DOWN 定时器从 Period 值向下计数到零，然后生成下溢事件。 TIM_COUNTERMODE_CENTERALIGNED1 在中心对齐模式下，计数器从 0 计数到 Period 值 – 1，生成溢出事件，然后从 Period 值向下计数到 1 并生成计数器下溢事件。然后它从 0 重新开始计数。当计数器向下计数时，配置为输出模式的通道的输出比较中断标志被置位。

<!-- page: 302 -->

表 11.4：定时器可用的计数模式

计数模式 描述

TIM_COUNTERMODE_CENTERALIGNED2 与 TIM_COUNTERMODE_CENTERALIGNED1 相同，但当计数器向上计数时，配置为输出模式的通道的输出比较中断标志被置位。 TIM_COUNTERMODE_CENTERALIGNED3 与 TIM_COUNTERMODE_CENTERALIGNED1 相同，但当计数器向上和向下计数时，配置为输出模式的通道的输出比较中断标志被置位。

表 11.5：通用定时器和高级定时器可用的 ClockDivision 模式

时钟分割模式 描述

TIM_CLOCKDIVISION_DIV1 在 ETRx 和 TIx 引脚上计算输入信号的 1 个采样 TIM_CLOCKDIVISION_DIV2 在 ETRx 和 TIx 引脚上计算输入信号的 2 个采样 TIM_CLOCKDIVISION_DIV4 在 ETRx 和 TIx 引脚上计算输入信号的 4 个采样

### 11.2.1 在中断模式下使用定时器

在查看完整示例之前，最好总结一下我们目前所见的内容。一个基本定时器：

- 是一个自由运行的计数器，它从 0 计数到 TIM_Base_InitTypeDef 初始化结构中 Period¹⁰ 字段指定的值，该值可以取最大值 0xFFFF（对于 32 位定时器为 0xFFFF FFFF）；
- 计数频率取决于定时器所连接总线的速度，可以通过在初始化结构中设置 Prescaler 寄存器将其降低多达 65536 倍；
- 当定时器达到 Period 值时，它会溢出，并置位更新事件（UEV）标志¹¹；定时器自动从初始值（对于基本定时器始终为零）重新开始计数¹²。

Period 和 Prescaler 寄存器决定了定时器频率，即溢出所需的时间（或者，如果你愿意，生成更新事件的频率），根据以下简单公式：

UpdateEvent = Timerclock (Prescaler + 1)(Period + 1) [1]

¹⁰Period 用于填充定时器的自动重载寄存器（ARR）。我不知道为什么 ST 工程师决定这样命名，因为 ARR 是所有 ST 数据手册中使用的寄存器名称。这可能会导致很多混淆，特别是当你刚开始接触 CubeHAL 时，但遗憾的是我们无能为力。 ¹¹更新事件（UEV）被锁存到预分频器时钟，并在下一个时钟边沿自动清除。不要将 UEV 与更新中断标志（UIF）混淆，后者必须像其他所有中断请求（IRQ）一样手动清除。只有当相应的中断被启用时，UIF 才会被置位。正如我们将在第 19 章中发现的，UEV 事件，就像为其他外设设置的所有事件标志一样，允许微控制器在使用 WFE 指令进入低功耗模式时唤醒。 ¹²这是与其他微控制器架构（特别是 8 位架构）的一个重要区别，在这些架构中，定时器需要手动“重新装填”才能重新开始计数。

<!-- page: 303 -->

例如，假设在一个 STM32F072 微控制器中，一个定时器连接到 APB1 总线，HCLK 设置为 48MHz，Prescaler 值等于 47999，Period 值等于 499。那么定时器将在每以下时间溢出一次：

UpdateEvent = 48.000.000 (47999 + 1)(499 + 1) = 2Hz = 1

2s = 0.5s

以下代码旨在 Nucleo-F072RB 上运行，展示了一个使用 TIM6¹³ 的完整示例。该示例不过是经典的 LED 闪烁，但这次我们使用基本定时器来计算延迟。

```text
Filename: Core/Src/main-ex1.c
5
TIM_HandleTypeDef htim6;
```

6

```text
7
int main(void) {
8
HAL_Init();
```

9

```text
10
Nucleo_BSP_Init();
```

11

```text
12
htim6.Instance = TIM6;
13
htim6.Init.Prescaler = 47999; //48MHz/48000 = 1000Hz
14
htim6.Init.Period = 499;
//1000HZ / 500 = 2Hz = 0.5s
```

15

```text
16
__HAL_RCC_TIM6_CLK_ENABLE();
```

17

```text
18
HAL_NVIC_SetPriority(TIM6_DAC_IRQn, 0, 0);
19
HAL_NVIC_EnableIRQ(TIM6_DAC_IRQn);
```

20

```text
21
HAL_TIM_Base_Init(&htim6);
22
HAL_TIM_Base_Start_IT(&htim6);
```

23

```text
24
while (1);
25
}
```

第 [12:14] 行使用之前计算的 Prescaler 和 Period 值配置 TIM6。然后通过使用第 19 行的宏启用定时器外设。其中断请求（IRQ）也是如此。定时器在第 21 行进行配置，并使用 HAL_TIM_Base_Start_IT() 函数以中断模式启动¹⁴。其余代码与之前看到的类似。

当定时器溢出时，TIM6_DAC_IRQHandler() 中断服务例程（ISR）触发，然后调用 HAL_TIM_IRQHandler()。硬件抽象层（HAL）会自动为我们处理所有必要的操作以正确管理更新事件，并调用 HAL_TIM_PeriodElapsedCallback() 回调函数来通知我们定时器已经溢出。

¹³配备 F401 和 F103 STM32 微控制器的 Nucleo 板用户会发现一个使用通用定时器的略有不同的示例。然而，概念保持不变。 ¹⁴初学者犯的一个非常常见的错误是忘记启动定时器，即忘记使用 CubeHAL 提供的 HAL_TIM_xxx_Start 函数之一。

<!-- page: 304 -->

![Image from PDF page 304](../images/page-0304-image-01.png)

HAL_TIM_IRQHandler() 例程的性能

对于运行速度极快的定时器，HAL_TIM_IRQHandler() 函数会带来不可忽视的开销。该函数被设计用于检查多达九个不同的中断状态标志，这需要执行多条 ARM 汇编指令才能完成任务。如果你需要在最短的时间内处理中断，最好自行处理 IRQ。再次强调，HAL（硬件抽象层）旨在向用户抽象大量细节，但它引入了性能惩罚，这是每个嵌入式开发人员都应知晓的。

如何为预分频器（Prescaler）和周期（Period）字段选择数值？

![Image from PDF page 304](../images/page-0304-image-02.png)

首先请注意，并非所有预分频器和周期值的组合都能导致定时器时钟频率的整数分频。例如，对于一个以 48MHz 运行的定时器，如果周期设置为 65535，定时器频率将降低至 732,4218 Hz。作者习惯于通过为预分频器值设置一个整数分频器来划分定时器的主频率（例如，对于 48MHz 的定时器，预分频器设为 47999——请记住，根据公式 [1]，频率计算时预分频器和周期值都需要加 1），然后调整周期值以达到所需的频率。MikroElektronica 提供了一个不错的工具¹⁵，可以根据特定的 STM32 微控制器和 HCLK 频率自动计算这些值。不幸的是，在撰写本章时，该工具生成的代码并不支持 CubeHAL。

#### 11.2.1.1 高级定时器中的时基生成

到目前为止，我们已经看到定时器的所有基本功能都是通过 TIM_Base_InitTypeDef 结构体的一个实例来配置的。该结构体包含一个名为 RepetitionCounter 的字段，用于进一步增加两个连续更新事件之间的周期：定时器将计数指定次数后才会设置事件并引发相应的中断。RepetitionCounter 仅在高级定时器中可用，这使得计算更新事件频率的公式变为：

UpdateEvent = Timerclock (Prescaler + 1)(Period + 1)(RepetitionCounter + 1)

将 RepetitionCounter 保持为零（默认行为），我们就获得了与基本定时器相同的工作模式。

### 11.2.2 以轮询模式使用定时器

CubeHAL 提供了三种使用定时器的方式：轮询、中断和直接存储器访问（DMA）模式。因此，HAL 提供了三个不同的函数来启动定时器：HAL_TIM_Base_Start()、HAL_TIM_Base_Start_IT() 和 HAL_TIM_Base_Start_DMA()。轮询模式背后的理念是定时器

¹⁵http://www.mikroe.com/timer-calculator/

<!-- page: 305 -->

计数器寄存器 (TIMx->CNT) 被连续访问以检查特定值。但在轮询定时器时必须小心。例如，在网上经常发现如下代码：

```text
...
while (1) {
if(__HAL_TIM_GET_COUNTER(&tim) == value)
...
```

这种轮询定时器的方式是完全错误的，即使它在某些示例中看似有效。为什么？

定时器独立于 Cortex-M 内核运行。定时器可以高速计数，最高可达 CPU 内核相同的时钟频率。但是，检查定时器计数器是否相等（即检查它是否等于给定值）需要多条 ARM 汇编指令，而这些指令又需要多个时钟周期。没有保证 CPU 访问计数器寄存器的时间恰好是它达到配置值的时间（这种情况仅在定时器运行非常慢时发生）。更好的方法是检查定时器当前计数值是否等于或大于给定值，或者检查 UIF 标志状态¹⁶：在最坏的情况下，我们可能会有时间测量上的偏移，但我们完全不会丢失事件（除非定时器运行得非常快，并且由于中断被屏蔽——即 UIF 标志在手动清除或 HAL 自动清除之前仍然被置位——我们丢失了后续事件）。

```text
...
while (1) {
if(__HAL_TIM_GET_FLAG(&tim) == TIM_FLAG_UPDATE) {
//Clear the IRQ flag otherwise we lose other events
__HAL_TIM_CLEAR_IT(htim, TIM_IT_UPDATE);
...
```

话虽如此，定时器是异步外设，管理溢出/下溢事件的正确方式是使用中断。除非定时器运行得非常快，以至于在几微秒（甚至纳秒）后生成中断会完全淹没微控制器，阻止其处理其他指令¹⁷，否则没有理由不使用中断模式来使用定时器。

### 11.2.3 以 DMA 模式使用定时器

定时器通常被编程为以 DMA 模式工作，特别是当它们用于触发其他外设时。这种模式保证定时器执行的操作是确定性的，并且具有尽可能小的延迟，尤其是当它们运行速度很快时。此外，Cortex-M 内核从定时器管理中解放出来

¹⁶然而，这要求定时器以中断模式启用，使用 HAL_TIM_Base_Start_IT() 函数。 ¹⁷请记住，即使 Cortex-M 微控制器中的异常处理具有确定性延迟（Cortex-M3/4/7/33 内核在 12 个 CPU 周期内响应中断，而 Cortex-M0 在 15 个周期内，Cortex-M0+ 在 16 个周期内），它也有不可忽视的成本，在“低速”微控制器中需要几纳秒（例如，对于以 48MHz 运行的 STM32F072 微控制器，中断服务大约需要 300ns）。此成本必须加上之前看到的 HAL 在中断管理期间引入的开销。

<!-- page: 306 -->

，这通常涉及处理频繁的 ISR（中断服务程序），可能会使 CPU 拥塞。最后，在某些高级模式下，如输出 PWM 模式，如果不使用 DMA 模式，几乎不可能达到给定的开关频率。

基于这些原因，定时器提供多达七个 DMA 请求，如表 11.6 所列。基本定时器仅实现 TIM_DMA_UPDATE 请求，因为它们没有输入/输出 I/O。然而，在希望基于时间执行 DMA 传输的情况下，利用 TIMx_UP 请求是有用的。

表 11.6：DMA 请求（其中大多数仅在通用定时器和高级定时器中可用）

定时器 DMA 请求 描述

TIM_DMA_UPDATE 更新请求（在 UEV 事件时生成） TIM_DMA_CC1 捕获/比较 1 DMA 请求 TIM_DMA_CC2 捕获/比较 2 DMA 请求 TIM_DMA_CC3 捕获/比较 3 DMA 请求 TIM_DMA_CC4 捕获/比较 4 DMA 请求 TIM_DMA_COM 换相请求 TIM_DMA_TRIGGER 触发请求

以下示例是闪烁 LED 应用的另一种变体，但这次我们使用以 DMA 模式运行的定时器来开启/关闭 LED。这里我们将使用 TIM6 定时器，编程为每 500ms 溢出一次：当这种情况发生时，定时器生成 TIM6_UP 请求（在 STM32F072 微控制器中，该请求绑定到 DMA1 的第三个通道），并且缓冲区的下一个元素以 DMA 循环模式传输到 GPIOA->ODR 寄存器，这导致 LD2 无限期地闪烁。

仔细阅读

![Image from PDF page 306](../images/page-0306-image-01.png)

在 STM32F2/F4/F7/L1/L4 系列中，只有 DMA2 对总线矩阵具有完全访问权限。这意味着只有那些请求绑定到此 DMA 控制器的定时器才能用于执行涉及其他外设的传输（内部和外部易失性存储器除外）。因此，对于基于 F2/F4/L1/L4 微控制器的 Nucleo 板，此示例使用 TIM1 作为时基生成器。

```text
Filename: Core/Src/main-ex2.c
8
int main(void) {
9
uint8_t data[] = {0xFF, 0x0};
```

10

```text
11
HAL_Init();
```

12

```text
13
Nucleo_BSP_Init();
```

14

```text
15
htim6.Instance = TIM6;
16
htim6.Init.Prescaler = 47999; //48MHz/48000 = 1000Hz
17
htim6.Init.Period = 499;
//1000HZ / 500 = 2Hz = 0.5s
```

<!-- page: 307 -->

18

```text
19
__HAL_RCC_TIM6_CLK_ENABLE();
```

20

```text
21
HAL_TIM_Base_Init(&htim6);
```

22

```text
23
hdma_tim6_up.Instance = DMA1_Channel3;
24
hdma_tim6_up.Init.Direction = DMA_MEMORY_TO_PERIPH;
25
hdma_tim6_up.Init.PeriphInc = DMA_PINC_DISABLE;
26
hdma_tim6_up.Init.MemInc = DMA_MINC_ENABLE;
27
hdma_tim6_up.Init.PeriphDataAlignment = DMA_PDATAALIGN_BYTE;
28
hdma_tim6_up.Init.MemDataAlignment = DMA_MDATAALIGN_BYTE;
29
hdma_tim6_up.Init.Mode = DMA_CIRCULAR;
30
hdma_tim6_up.Init.Priority = DMA_PRIORITY_LOW;
31
HAL_DMA_Init(&hdma_tim6_up);
```

32

```text
33
HAL_TIM_Base_Start(&htim6);
34
HAL_DMA_Start(&hdma_tim6_up, (uint32_t)data, (uint32_t)&GPIOA->ODR, 2);
35
__HAL_TIM_ENABLE_DMA(&htim6, TIM_DMA_UPDATE);
```

36

```text
37
while (1);
38
}
```

## 第 [26:33] 行配置了 DMA1_Channel3 的 DMA_HandleTypeDef，使其工作在循环模式。随后，第 37 行启动 DMA 传输，使得每当生成 TIM6_UP 请求（即定时器溢出）时，data 缓冲区的内容就会被传输到 GPIOA->ODR 寄存器中。这导致 LD2 LED 闪烁。请注意，这里没有使用 HAL_TIM_Base_Start_DMA() 函数。为什么不用？

## 查看 HAL_TIM_Base_Start_DMA() 例程的实现，可以看到 ST 工程师将其定义为从内存缓冲区传输到 TIM6->ARR，这对应于 Period（周期）。

```text
HAL_TIM_Base_Start_DMA(TIM_HandleTypeDef *htim, uint32_t *pData, uint16_t Length) {
...
/* Enable the DMA channel */
HAL_DMA_Start_IT(htim->hdma[TIM_DMA_ID_UPDATE], (uint32_t)pData,
(uint32_t)&htim->Instance->ARR, Length);
/* Enable the TIM Update DMA request */
__HAL_TIM_ENABLE_DMA(htim, TIM_DMA_UPDATE);
...
```

## 基本上，我们只能使用 HAL_TIM_Base_Start_DMA() 来在每次定时器溢出时更改定时器的 Period（周期）。因此，我们需要自行配置 DMA 以执行此传输。

## 在下一章中，我们将看到一个更有用的应用，展示如何在 DMA 模式下使用定时器来定期执行 ADC 转换。

<!-- page: 308 -->

### 11.2.4 停止定时器

CubeHAL 提供了三个用于停止运行中定时器的函数：HAL_TIM_Base_Stop()、HAL_TIM_Base_Stop_IT() 和 HAL_TIM_Base_Stop_DMA()。我们根据所使用的定时器模式选择其中一个（例如，如果我们在中断模式下启动了定时器，则需要使用 HAL_TIM_Base_Stop_IT() 例程来停止它）。每个函数都旨在正确地禁用 IRQ（中断请求）和 DMA 配置。

### 11.2.5 使用 CubeMX 配置基本定时器

CubeMX 可以将配置基本定时器所需的工作量降至最低。一旦通过勾选 Activated 标志启用定时器，就可以从 Configuration 视图中进行配置。定时器配置视图允许设置 Prescaler（预分频器）和 Period（周期）寄存器的值，如图 11.2 所示。CubeMX 将在 MX_TIMx_Init() 函数内生成所有必要的初始化代码。此外，始终在同一个配置对话框中，可以启用与定时器相关的 IRQ（中断请求）和 DMA 请求。

![Image from PDF page 308](../images/page-0308-image-01.jpeg)

图 11.2：CubeMX 允许轻松生成配置定时器所需的代码

## 11.3 通用定时器

大多数 STM32 定时器都是通用定时器。与之前介绍的基本定时器不同，它们提供了更多的交互能力，这得益于多达四个独立通道，可用于测量输入信号、基于时间输出信号以及生成脉宽调制 (PWM) 信号。然而，通用定时器提供了许多其他功能，我们将在本章的这一部分逐步发现。

<!-- page: 309 -->

### 11.3.1 具有外部时钟源的时间基准发生器

图 11.3 显示了通用定时器¹⁸ 的框图。图中的某些部分已被屏蔽：我们将在后面更深入地研究它们。红色高亮显示的路径用于在 APB 时钟被选为源时为定时器供电：内部时钟 CK_INT 馈送到 Prescaler (PSC)，后者进而决定 Counter Register (CNT) 增加/减小的速度。该计数器与自动重载寄存器（其中填充了 TIM_Base_InitTypeDef.Period 字段的值）的内容进行比较。当它们匹配时，生成 UEV 事件，如果已启用，则触发相应的 IRQ（中断请求）。

![Image from PDF page 309](../images/page-0309-image-01.jpeg)

图 11.3：通用定时器的结构

查看图 11.3，我们可以看到定时器可以从其他源接收“刺激”。这些可以分为两个主要组：

- 时钟源，用于为定时器提供时钟。它们可以来自连接到 MCU 引脚的外部源，或来自内部连接到 MCU 的其他定时器。请记住

¹⁸该图改编自 ST 的 RM0368(https://bit.ly/1Kq3SoE) 参考手册中找到的图。

<!-- page: 310 -->

- 定时器没有时钟源就无法工作，因为时钟源用于递增计数器寄存器。
- 触发源，用于将定时器与连接到 MCU 引脚的外部源或内部连接的其他定时器同步。例如，可以配置定时器，使其在外部事件触发时开始计数。在这种情况下，定时器由另一个时钟源（可以是 APBx 总线或连接到 ETR2 引脚的外部时钟源）提供时钟，并由另一个设备控制（即，何时开始计数等）。

根据定时器类型及其实际实现，定时器可以从以下来源获取时钟：

- 由 RCC 提供的内部 TIMx_CLK（在第 11.2 节中介绍）
- 内部触发输入 0 到 3

- – ITR0、ITR1、ITR2 和 ITR3，使用另一个定时器（主）作为此定时器（从）的预分频器（在第 11.3.1.2 节中介绍）
- 外部输入通道引脚（在第 11.3.1.2 节中介绍）

- – 引脚 1：TI1FP1 或 TI1F_ED – 引脚 2：TI2FP2
- 外部 ETR 引脚：

– ETR1 引脚（在第 11.3.1.2 节中介绍） – ETR2 引脚（在第 11.3.1.1 节中介绍）

相反，定时器可以从以下来源触发：

- 内部触发输入 0 到 3

- – ITR0、ITR1、ITR2 和 ITR3，使用另一个定时器作为主定时器（在第 11.3.2 节中介绍）
- 外部输入通道引脚（在第 11.3.2 节中介绍）

- – 引脚 1：TI1FP1 或 TI1F_ED – 引脚 2：TI2FP2
- 外部 ETR1 引脚

让我们通过分析实际示例来研究这些从外部源为定时器提供时钟/触发的方式。

<!-- page: 311 -->

#### 11.3.1.1 外部时钟模式 2

通用定时器（General purpose timers）具有从外部源获取时钟的能力，这使它们可以设置为两种不同的模式：外部时钟源模式 1 和 外部时钟源模式 2。第一种模式仅在定时器配置为从模式（slave mode）时可用。我们将在下一段中研究这种模式。

相反，第二种模式仅通过使用外部时钟源即可激活。这允许使用更精确和专用的源，并最终进一步降低计数频率。事实上，当选择外部时钟源模式 2 时，计算更新事件频率的公式变为：

UpdateEvent = EXTclock (EXTclockPrescaler)(Prescaler + 1)(Period + 1)(RepetitionCounter + 1) [2]

其中 EXTclock 是外部源的频率，EXTclockPrescaler 是一个源频率分频器，其取值可以为 1、2、4 和 8。

可以使用函数 HAL_TIM_ConfigClockSource() 和结构体 TIM_ClockConfigTypeDef 的一个实例来选择通用定时器的时钟源，该结构体定义如下：

```text
typedef struct {
uint32_t ClockSource;
/* TIM clock sources
*/
uint32_t ClockPolarity;
/* TIM clock polarity
*/
uint32_t ClockPrescaler;
/* TIM clock prescaler */
uint32_t ClockFilter;
/* TIM clock filter */
} TIM_ClockConfigTypeDef;
```

- ClockSource：指定用于驱动定时器的时钟信号的源。它可以取表 11.7 中的值。默认情况下，选择 TIM_CLOCKSOURCE_INTERNAL 模式。
- ClockPolarity：指示用于驱动定时器的时钟信号的极性。它可以取表 11.8 中的值。默认情况下，选择 TIM_CLOCKPOLARITY_RISING 模式。
- ClockPrescaler：指定外部时钟源的分频器。它可以取表 11.9 中的值。默认情况下，选择 TIM_CLOCKPRESCALER_DIV1 值。
- ClockFilter：这个 4 位字段定义了用于采样外部时钟信号的频率以及应用于该信号的数字滤波器的长度。数字滤波器由一个事件计数器组成，需要 N 个连续事件来验证输出上的转换。关于 fDT S（死区信号）是如何计算的，请参阅您的 MCU 数据手册。默认情况下，滤波器被禁用。

<!-- page: 312 -->

表 11.7：通用定时器和高级定时器可用的时钟源模式

时钟源模式 描述

TIM_CLOCKSOURCE_INTERNAL 定时器由其所连接的 APBx 总线提供时钟。 TIM_CLOCKSOURCE_ETRMODE1 此模式称为外部时钟模式 1¹⁹，当定时器配置为从模式时可用。定时器可以由连接到 ITR0、ITR1、ITR2、ITR3、TI1FP1、TI2FP2 或 ETR1 引脚的内部/外部源提供时钟。 TIM_CLOCKSOURCE_ETRMODE2 此模式称为外部时钟模式 2。定时器可以由连接到 ETR2 引脚的外部源提供时钟。

表 11.8：通用定时器和高级定时器可用的外部时钟极性模式

外部时钟极性模式 描述

TIM_CLOCKPOLARITY_RISING 定时器在外部时钟源的上升沿同步。 TIM_CLOCKPOLARITY_FALLING 定时器在外部时钟源的下降沿同步。 TIM_CLOCKPOLARITY_BOTHEDGE 定时器在外部时钟源的上升沿和下降沿同步（这将增加采样频率）。

表 11.9：通用定时器和高级定时器可用的外部时钟分频器模式

外部时钟分频器模式 描述

TIM_CLOCKPRESCALER_DIV1 不使用分频器 TIM_CLOCKPRESCALER_DIV2 每 2 个事件执行一次捕获 TIM_CLOCKPRESCALER_DIV4 每 4 个事件执行一次捕获 TIM_CLOCKPRESCALER_DIV8 每 8 个事件执行一次捕获

让我们构建一个示例，展示如何为 TIM3 定时器使用外部时钟源。该示例包括将主时钟输出（MCO）引脚路由到 TIM3_ETR2 引脚，对于提供此定时器的所有 Nucleo 板，这对应于 PD2 引脚。使用 Morpho 连接器可以轻松完成此操作，如图 11.4 所示（针对 Nucleo-F072RB）（对于您的 Nucleo，请使用 CubeMX 工具识别 MCO 引脚以及附录 C 中对应的引脚图）。

¹⁹在 ST 文档中，这些模式也被称为外部触发模式 1 和 2（ETR1 和 ETR2）。

<!-- page: 313 -->

![Image from PDF page 313](../images/page-0313-image-01.jpeg)

图 11.4：如何在 Nucleo-F072RB 板上将 MCO 引脚路由到 TIM3_ETR 引脚

## MCO 引脚已启用并连接到 HSI 时钟源。以下代码显示了示例中最相关的部分。

```text
Filename: Core/Src/main-ex3.c
23
void MX_TIM3_Init(void) {
24
TIM_ClockConfigTypeDef sClockSourceConfig;
```

25

```text
26
htim3.Instance = TIM3;
27
htim3.Init.Prescaler = 999;
28
htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
29
htim3.Init.Period = 3999;
30
htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
31
htim3.Init.RepetitionCounter = 0;
32
HAL_TIM_Base_Init(&htim3);
```

33

```text
34
sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_ETRMODE2;
35
sClockSourceConfig.ClockPolarity = TIM_CLOCKPOLARITY_NONINVERTED;
36
sClockSourceConfig.ClockPrescaler = TIM_CLOCKPRESCALER_DIV1;
37
sClockSourceConfig.ClockFilter = 0;
38
HAL_TIM_ConfigClockSource(&htim3, &sClockSourceConfig);
```

39

```text
40
HAL_NVIC_SetPriority(TIM3_IRQn, 0, 0);
41
HAL_NVIC_EnableIRQ(TIM3_IRQn);
42
}
```

43

```text
44
void HAL_TIM_Base_MspInit(TIM_HandleTypeDef* htim_base) {
45
GPIO_InitTypeDef GPIO_InitStruct;
46
if(htim_base->Instance==TIM3)
{
47
/* Peripheral clock enable */
```

<!-- page: 314 -->

```text
48
__HAL_RCC_TIM3_CLK_ENABLE();
49
__HAL_RCC_GPIOD_CLK_ENABLE();
```

50

```text
51
/**TIM3 GPIO Configuration
52
PD2
------> TIM3_ETR
53
*/
54
GPIO_InitStruct.Pin = GPIO_PIN_2;
55
GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
56
GPIO_InitStruct.Pull = GPIO_NOPULL;
57
GPIO_InitStruct.Speed = GPIO_SPEED_LOW;
58
HAL_GPIO_Init(GPIOD, &GPIO_InitStruct);
59
}
60
}
```

第 [27:33] 行配置 TIM3 定时器，将其分频器设置为 999，周期设置为 3999。第 [34:38] 行为 TIM3 配置外部时钟源。由于 HSI 振荡器运行在 8MHz²⁰，使用公式 [2] 我们可以计算 UEV 频率，其等于：

UpdateEvent = 8.000.000 (1)(999 + 1)(3999 + 1)(0 + 1) = 2Hz = 0.5s

最后，第 [48:58] 行启用 TIM3 并将 PD2 引脚（对应于 TIM3_ETR2 引脚）配置为输入源。

仔细阅读

![Image from PDF page 314](../images/page-0314-image-01.png)

重要的是要指出，在使用 __GPIOD_CLK_ENABLE() 宏启用 GPIO 端口 D 之前，我们不能将其用作 TIM3 的时钟源。同样适用于 TIM3，它通过 __TIM3_CLK_ENABLE() 启用：这是因为外部时钟并不直接馈送到分频器，而是首先通过专用逻辑块与 APBx 时钟进行同步。

#### 11.3.1.2 外部时钟模式 1

STM32 的通用定时器和高级定时器可以被配置为工作在主模式或从模式²¹。当被配置为从模式时，定时器可以由内部 ITR0、ITR1、ITR2 和 ITR3 线、连接到 ETR1 引脚的外部时钟，或连接到 TI1FP1 和 TI2FP2 源的其他时钟源驱动，这些源对应于通道 1 和通道 2 的输入引脚。这种工作模式被称为外部时钟模式 1。

²⁰此 HSI 频率与 STM32F072RB 相关。在其他 STM32 微控制器中，HSI 速度为 16MHz。请查阅您的微控制器数据手册，并相应地调整计算。²¹正如我们接下来将看到的，定时器可以被配置为同时工作在主模式和从模式。

<!-- page: 315 -->

![Image from PDF page 315](../images/page-0315-image-01.png)

对于所有 STM32 平台的新手来说，外部时钟模式 1 和 2 是相当令人困惑的。这两种模式都是使用外部时钟源为定时器提供时钟的方式，但第一种是通过将定时器配置为从模式来实现的（这确实是一种“触发”形式），而第二种是通过简单地选择不同的时钟源获得的。我不知道这种术语的起源，以及这种区分的实际效果是什么。然而，重要的是在此指出，将定时器配置为 ETR1 或 ETR2 模式的方式是完全不同的，我们将在下一个例子中看到。

查看图 11.16，我们可以看到 TI1FP1 和 TI2FP2 输入只不过是定时器在应用输入滤波器后的 TI1 和 TI2 输入通道。

![Image from PDF page 315](../images/page-0315-image-02.png)

要配置定时器为从模式，我们使用函数 HAL_TIM_SlaveConfigSynchro() 和 struct TIM_SlaveConfigTypeDef 的一个实例，其定义如下：

```text
typedef struct {
uint32_t
SlaveMode;
/* 从模式选择 */
uint32_t
InputTrigger;
/* 输入触发源 */
uint32_t
TriggerPolarity;
/* 输入触发极性 */
uint32_t
TriggerPrescaler; /* 输入触发预分频器 */
uint32_t
TriggerFilter;
/* 输入触发滤波器 */
} TIM_SlaveConfigTypeDef;
```

- SlaveMode：当定时器被配置为从模式时，它可以由多个源进行时钟/触发。此字段可以取表 11.10 中的值。本段讨论的是 TIM_SLAVEMODE_EXTERNAL1 模式。
- InputTrigger：定义触发/时钟配置为从模式的定时器的源。它可以取表 11.11 中的值。
- TriggerPolarity：指示触发/时钟源的极性。它可以取表 11.12 中的值。
- TriggerPrescaler：指定外部时钟源的预分频器。它可以取表 11.13 中的值。默认情况下，选择 TIM_TRIGGERPRESCALER_DIV1 值。
- TriggerFilter：此 4 位字段定义了用于采样连接到输入引脚的外部时钟/触发信号的频率，以及应用于该信号的数字滤波器的长度。数字滤波器由一个事件计数器组成，其中需要 N 个连续事件来验证输出上的转换。关于如何计算 fDT S（死区信号），请参阅您的微控制器数据手册。默认情况下，滤波器被禁用。

<!-- page: 316 -->

表 11.10：通用定时器和高级定时器可用的从模式

从模式 工作 描述

TIM_SLAVEMODE_DISABLE 禁用 从模式被禁用（默认值） TIM_SLAVEMODE_RESET 触发 所选触发输入 (TRGI) 的上升沿重新初始化计数器并生成寄存器的更新 TIM_SLAVEMODE_GATED 触发 当触发输入 (TRGI) 为高电平时，计数器时钟被启用。一旦触发变为低电平，计数器停止（但不会被重置）。计数器的启动和停止都受控制 TIM_SLAVEMODE_TRIGGER 触发 计数器在 TRGI 的上升沿启动（但不会被重置）。仅计数器的启动受控制 TIM_SLAVEMODE_EXTERNAL1 时钟 所选 TRGI 的上升沿对计数器进行时钟 TIM_SLAVEMODE_COMBINED_RESETTRIGGER²² 触发 所选触发输入 (TRGI) 的上升沿重新初始化计数器，生成寄存器的更新并启动计数器

表 11.11：工作在从模式的定时器可用的触发/时钟源

触发/时钟源 描述

TIM_TS_ITR0 触发/时钟源是 ITR0 线（内部连接到主定时器） TIM_TS_ITR1 触发/时钟源是 ITR1 线（内部连接到主定时器） TIM_TS_ITR2 触发/时钟源是 ITR2 线（内部连接到主定时器） TIM_TS_ITR3 触发/时钟源是 ITR3 线（内部连接到主定时器） TIM_TS_TI1F_ED 触发/时钟源是 TIM_TS_TI1F_ED 线 TIM_TS_TI1FP1 触发/时钟源是 TIM_TS_TI1FP1 线，对应于通道 1 TIM_TS_TI2FP2 触发/时钟源是 TIM_TS_TI2FP2 线，对应于通道 2 TIM_TS_ETRF 触发/时钟源是 ETR1 引脚 TIM_TS_NONE 无外部时钟/触发源

表 11.12：工作在从模式的定时器可用的触发/时钟极性模式

触发/时钟极性模式 描述

TIM_TRIGGERPOLARITY_INVERTED 当外部时钟源是 ETR1 时使用。ETR1 非反相，高电平或上升沿有效 TIM_TRIGGERPOLARITY_NONINVERTED 当外部时钟源是 ETR1 时使用。ETR1 反相，低电平或下降沿有效 TIM_TRIGGERPOLARITY_RISING TIxFPx 或 TI1_ED 触发源的极性。定时器在外部触发源的上升沿同步 ²²此模式仅在部分 STM32F3 微控制器中可用。

<!-- page: 317 -->

表 11.12：工作在从模式的定时器可用的触发/时钟极性模式

触发/时钟极性模式 描述

TIM_TRIGGERPOLARITY_FALLING TIxFPx 或 TI1_ED 触发源的极性。定时器在外部触发源的下降沿同步 TIM_TRIGGERPOLARITY_BOTHEDGE TIxFPx 或 TI1_ED 触发源的极性。定时器在外部触发源的上升沿和下降沿同步（这将增加采样频率）

表 11.13：工作在从模式的定时器可用的触发/时钟预分频器模式

外部时钟预分频器模式 描述

TIM_TRIGGERPRESCALER_DIV1 不使用预分频器 TIM_TRIGGERPRESCALER_DIV2 每 2 个事件执行一次捕获 TIM_TRIGGERPRESCALER_DIV4 每 4 个事件执行一次捕获 TIM_TRIGGERPRESCALER_DIV8 每 8 个事件执行一次捕获

当选择外部时钟源模式 1 时，计算更新事件频率的公式变为：

UpdateEvent = TRGIclock (Prescaler + 1)(Period + 1)(RepetitionCounter + 1) [3]

其中 TRGIclock 是连接到 ETR1 引脚的时钟源的频率，连接到内部线 ITR0..ITR3 的内部/外部触发时钟源的频率，或连接到外部通道 TI1FP1..T2FP2 的信号频率。

因此，让我们回顾一下到目前为止看到的内容：

- 当定时器仅工作在主模式²³时，可以通过将此源连接到 ETR2 引脚来由外部源进行时钟；
- 如果定时器工作在从模式，则它可以由连接到 ETR1 引脚的信号、连接到内部线 ITR0…ITR2 的任何触发源（因此，时钟源只能是另一个定时器）或连接到定时器通道 TI1 和 TI2 的输入信号进行时钟，如果激活了输入滤波级，则变为 TI1FP1 和 TI2FP2。

让我们构建另一个示例，展示如何使用外部时钟源为 TIM3 定时器提供时钟。该示例包括将主时钟输出 (MCO) 引脚路由到 TI2FP2 引脚（即 TIM3 定时器的第二个通道），在 Nucleo-F072RB 中对应于 PA7 引脚。使用 Morpho 连接器可以轻松完成此操作，如图 11.5 所示（对于您的 Nucleo，请使用 CubeMX 工具来识别 MCO 和 TI2FP2 引脚）。

²³ 正如我们稍后将会发现的，定时器的主从模式并非排他性的：一个定时器可以被配置为同时作为主定时器和从定时器工作。

<!-- page: 318 -->

![Image from PDF page 318](../images/page-0318-image-01.jpeg)

图 11.5：如何在 Nucleo-F072RB 开发板上将 MCO 引脚路由到 TI2FP2 引脚

## MCO 引脚已启用并连接到 HSI 时钟源，如前一个示例所示。以下代码展示了该示例中最相关的部分。

```text
Filename: Core/Src/main-ex4.c
24
void MX_TIM3_Init(void) {
25
TIM_SlaveConfigTypeDef sSlaveConfig;
```

26

```text
27
htim3.Instance = TIM3;
28
htim3.Init.Prescaler = 999;
29
htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
30
htim3.Init.Period = 3999;
31
htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
32
HAL_TIM_Base_Init(&htim3);
```

33

```text
34
sSlaveConfig.SlaveMode = TIM_SLAVEMODE_EXTERNAL1;
35
sSlaveConfig.InputTrigger = TIM_TS_TI2FP2;
36
sSlaveConfig.TriggerPolarity = TIM_TRIGGERPOLARITY_RISING;
37
sSlaveConfig.TriggerFilter = 0;
38
HAL_TIM_SlaveConfigSynchro(&htim3, &sSlaveConfig);
```

39

```text
40
HAL_NVIC_SetPriority(TIM3_IRQn, 0, 0);
41
HAL_NVIC_EnableIRQ(TIM3_IRQn);
42
}
```

43

```text
44
void HAL_TIM_Base_MspInit(TIM_HandleTypeDef* htim_base) {
45
GPIO_InitTypeDef GPIO_InitStruct;
46
if(htim_base->Instance==TIM3)
{
47
/* Peripheral clock enable */
48
__HAL_RCC_TIM3_CLK_ENABLE();
```

<!-- page: 319 -->

```text
49
__HAL_RCC_GPIOA_CLK_ENABLE();
```

50

```text
51
/**TIM3 GPIO Configuration
52
PA7
------> TIM3_CH2
53
*/
54
GPIO_InitStruct.Pin = GPIO_PIN_7;
55
GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
56
GPIO_InitStruct.Pull = GPIO_NOPULL;
57
GPIO_InitStruct.Speed = GPIO_SPEED_LOW;
58
GPIO_InitStruct.Alternate = GPIO_AF1_TIM3;
59
HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
60
}
```

第 [34:38] 行将 TIM3 配置为从模式。输入触发源被设置为 TI2FP2，定时器同步于输入信号的上升沿。最后，第 [54:59] 行将 PA7 配置为 TIM3 第二通道的输入引脚。

#### 11.3.1.3 使用 CubeMX 配置通用定时器的源时钟

配置通用定时器的时钟源可能是一场噩梦，尤其对于 STM32 平台的新手而言。CubeMX 可以简化这一过程，尽管这需要很好地理解主从模式以及 ETR1 和 ETR2 模式。

要将定时器配置为外部时钟模式 2，只需从配置面板中选择 ETR2 作为时钟源即可，如图 11.6 所示。

![Image from PDF page 319](../images/page-0319-image-01.jpeg)

图 11.6：如何从 IP 面板中选择 ETR2 模式

选择时钟源后，可以从配置中设置外部时钟滤波器、极性和预分频器，如图 11.7 所示。

<!-- page: 320 -->

![Image from PDF page 320](../images/page-0320-image-01.jpeg)

图 11.7：如何配置工作在 ETR2 模式的定时器

要将定时器配置为外部时钟模式 1，我们需要从从模式条目中选择该模式，然后选择触发源（在这种情况下，它是定时器的时钟源），如图 11.8 所示。

![Image from PDF page 320](../images/page-0320-image-02.jpeg)

图 11.8：如何从 IP 树面板中选择 ETR1 模式

选择时钟源后，可以从定时器配置对话框中设置其他配置参数（此处未显示）。

### 11.3.2 主从同步模式

一旦定时器以主模式运行，它就可以通过一条专用的输出线（称为触发输出 TRGO²⁴）向配置为从模式的另一个定时器提供信号，该输出线连接到内部专用线 ITR0、ITR1、ITR2 和 ITR3。主定时器既可以提供时钟源（因此充当一级预分频器——这就是我们在上一段中研究的内容），也可以触发从定时器。

这些内部触发（ITR）线（ITR0、ITR1、ITR2 和 ITR3）正是芯片内部的，每条线都在两个定义的定时器之间硬连线。例如，在 STM32F072 微控制器中，TIM1

²⁴ 一些 STM32 微控制器，特别是 STM32F3 系列，提供两条独立的触发线，分别命名为 TRGO1 和 TRGO2。本书未展示这种情况。

<!-- page: 321 -->

的 TRGO 线连接到 TIM2 定时器的 ITR0 线，如图 11.9 所示。

![Image from PDF page 321](../images/page-0321-image-01.png)

图 11.9：TIM1 可以通过 ITR0 线向 TIM2 定时器提供信号

配置为从模式的定时器也可以同时作为另一个定时器的主定时器，从而允许创建复杂的定时器网络。例如，图 11.10 展示了定时器如何级联连接，而图 11.11 展示了定时器如何通过主从模式的组合形成层次结构。请注意，TIM1、TIM2 和 TIM3 通过同一条 ITR0 线内部互连。这使得可以根据同一事件（复位、使能、更新等）同步多个定时器。

![Image from PDF page 321](../images/page-0321-image-02.png)

图 11.10：主从模式的组合允许将定时器配置为级联

<!-- page: 322 -->

![Image from PDF page 322](../images/page-0322-image-01.png)

图 11.11：主从模式的组合允许将定时器配置为层次结构

要配置定时器为主模式，我们使用函数 HAL_TIMEx_MasterConfigSynchronization() 和结构体 TIM_MasterConfigTypeDef 的一个实例，其定义如下：

```text
typedef struct {
uint32_t
MasterOutputTrigger;
/* Trigger output (TRGO) selection */
uint32_t
MasterSlaveMode;
/* Master/slave mode selection */
} TIM_MasterConfigTypeDef;
```

- MasterOutputTrigger：指定 TRGO 输出的行为，其取值来自表 11.14。
- MasterSlaveMode：用于启用/禁用定时器的主从模式。它可以取值为 TIM_MASTERSLAVEMODE_ENABLE 或 TIM_MASTERSLAVEMODE_DISABLE。

表 11.14：工作在从模式的定时器可用的触发/时钟源

定时器主模式选择 描述

TIM_TRGO_RESET 当 TIMx->EGR 寄存器中的 UG 位被置位时，生成 TRGO 信号。更多细节见第 11.3.3 节 TIM_TRGO_ENABLE 当主定时器被使能时，生成 TRGO 信号。这有助于同时启动多个定时器，或控制从定时器被使能的时间窗口 TIM_TRGO_UPDATE 选择更新事件作为触发输出（TRGO）。例如，主定时器可以用作从定时器的预分频器（我们在第 11.3.1.2 节中研究过这种模式） TIM_TRGO_OC1 一旦发生捕获或比较匹配，触发输出发送一个正脉冲

<!-- page: 323 -->

表 11.14：工作在从模式的定时器可用的触发/时钟源

定时器主模式选择 描述

TIM_TRGO_OC1REF 一旦在通道 1 上发生捕获或比较匹配，触发输出发送一个正脉冲 TIM_TRGO_OC2REF 一旦在通道 2 上发生捕获或比较匹配，触发输出发送一个正脉冲 TIM_TRGO_OC3REF 一旦在通道 3 上发生捕获或比较匹配，触发输出发送一个正脉冲 TIM_TRGO_OC4REF 一旦在通道 4 上发生捕获或比较匹配，触发输出发送一个正脉冲

让我们看一个示例，展示如何配置 TIM1 和 TIM3 为级联模式，其中 TIM1 作为 TIM3 定时器的主定时器。TIM1 通过 ITR0 线用作 TIM3 的时钟源。此外，TIM1 被配置为在其 TI1FP1 线上发生外部事件时开始计数，在 Nucleo-F072 上这对应于 PA8 引脚：当 PA8 引脚变高时，TIM1 开始计数，然后通过 ITR0 线向 TIM3 定时器提供信号。

```text
Filename: Core/Src/main-ex5.c
12
int main(void) {
13
HAL_Init();
```

14

```text
15
Nucleo_BSP_Init();
16
MX_TIM1_Init();
17
MX_TIM3_Init();
```

18

```text
19
HAL_TIM_Base_Start_IT(&htim3);
```

20

```text
21
while (1);
22
}
```

23

```text
24
void MX_TIM1_Init(void) {
25
TIM_ClockConfigTypeDef sClockSourceConfig;
26
TIM_MasterConfigTypeDef sMasterConfig;
27
TIM_SlaveConfigTypeDef sSlaveConfig;
```

28

```text
29
htim1.Instance = TIM1;
30
htim1.Init.Prescaler = 47999;
31
htim1.Init.CounterMode = TIM_COUNTERMODE_UP;
32
htim1.Init.Period = 249;
33
htim1.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
34
htim1.Init.RepetitionCounter = 0;
35
HAL_TIM_Base_Init(&htim1);
```

36

```text
37
sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
38
HAL_TIM_ConfigClockSource(&htim1, &sClockSourceConfig);
```

39

<!-- page: 324 -->

```text
40
sSlaveConfig.SlaveMode = TIM_SLAVEMODE_TRIGGER;
41
sSlaveConfig.InputTrigger = TIM_TS_TI1FP1;
42
sSlaveConfig.TriggerPolarity = TIM_TRIGGERPOLARITY_RISING;
43
sSlaveConfig.TriggerFilter = 15;
44
HAL_TIM_SlaveConfigSynchron(&htim1, &sSlaveConfig);
```

45

```text
46
sMasterConfig.MasterOutputTrigger = TIM_TRGO_UPDATE;
47
sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_ENABLE;
48
HAL_TIMEx_MasterConfigSynchronization(&htim1, &sMasterConfig);
49
}
```

50

```text
51
void MX_TIM3_Init(void) {
52
TIM_SlaveConfigTypeDef sSlaveConfig;
```

53

```text
54
htim3.Instance = TIM3;
55
htim3.Init.Prescaler = 0;
56
htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
57
htim3.Init.Period = 1;
58
htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
59
HAL_TIM_Base_Init(&htim3);
```

60

```text
61
sSlaveConfig.SlaveMode = TIM_SLAVEMODE_EXTERNAL1;
62
sSlaveConfig.InputTrigger = TIM_TS_ITR0;
63
HAL_TIM_SlaveConfigSynchro(&htim3, &sSlaveConfig);
```

64

```text
65
HAL_NVIC_SetPriority(TIM3_IRQn, 0, 0);
66
HAL_NVIC_EnableIRQ(TIM3_IRQn);
67
}
```

68

```text
69
void HAL_TIM_Base_MspInit(TIM_HandleTypeDef* htim_base) {
70
GPIO_InitTypeDef GPIO_InitStruct;
71
if(htim_base->Instance==TIM3) {
72
__HAL_RCC_TIM3_CLK_ENABLE();
73
}
```

74

```text
75
if(htim_base->Instance==TIM1) {
76
__HAL_RCC_TIM1_CLK_ENABLE();
```

77

```text
78
GPIO_InitStruct.Pin = GPIO_PIN_8;
79
GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
80
GPIO_InitStruct.Pull = GPIO_PULLDOWN;
81
GPIO_InitStruct.Speed = GPIO_SPEED_LOW;
82
GPIO_InitStruct.Alternate = GPIO_AF2_TIM1;
83
HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
84
}
85
}
```

<!-- page: 325 -->

第 [29:38] 行配置 TIM1 以内部 APB1 总线作为时钟源。第 [40:44] 行将 TIM1 配置为从模式，使其在 TI1FP1 线变高时（即被触发时）开始计数。PA8 GPIO 在第 [74:79] 行中相应地进行了配置（被配置为 GPIO_AF2_TIM1）。请注意，第 76 行激活了内部下拉电阻：这可以防止浮空输入意外触发定时器。出于同样的原因，第 43 行将 TriggerFilter 设置为最大级别（如果你尝试将其设置为零，你会发现即使只是触摸连接到 PA8 引脚的导线，也很容易意外触发定时器）。

第 [46:48] 行配置 TIM1 同时工作在主模式。每当产生更新事件时，定时器都会触发其内部线（该线连接到 TIM3 的 ITR0 线）。最后，第 [61:63] 行将 TIM3 配置为外部时钟模式 1，选择 ITR0 线作为源时钟。

![Image from PDF page 325](../images/page-0325-image-01.png)

注意，为了使 LD2 LED 每 500ms（2Hz）闪烁一次，TIM1 的周期被设置为 249²⁵，这导致 TIM1 的更新频率为 4Hz。这是必需的，因为根据公式 [3]，我们有：

UpdateEvent = 4Hz (0 + 1)(1 + 1)(0 + 1) = 2Hz = 0.5s

请记住，Period 字段不能设置为零。

要触发 TIM1，你需要将 PA8 引脚连接到 +3V3 电源。图 11.12 展示了如何在 Nucleo-F072 上进行连接。

最后，请注意，我们没有为 TIM1 定时器调用 HAL_TIM_Base_Start() 函数（参见 main() 例程），因为定时器是在通道 1 上生成的触发事件时启动的（即，当我们把 PA8 引脚连接到 +3V3 电源时）。

²⁵显然，该预分频器值是针对运行在 48MHz 的 STM32F072RB 微控制器而言的。对于你的 Nucleo，请查阅书中的示例以获取正确的预分频器设置。

<!-- page: 326 -->

![Image from PDF page 326](../images/page-0326-image-01.jpeg)

图 11.12：如何在 Nucleo-F072R8 板上将 TI2FP2 引脚连接到 AVDD 引脚

#### 11.3.2.1 启用触发相关中断

当定时器工作在从模式时，如果已启用，每次指定的触发事件发生时，定时器中断（IRQ）都会被触发。例如，当主时钟因更新事件而触发时，从定时器的 IRQ 会被触发，我们可以通过定义回调函数来获知此事：

```text
void HAL_TIM_TriggerCallback(TIM_HandleTypeDef *htim) {
...
}
```

默认情况下，HAL_TIM_Base_Start_IT() 不会启用这种类型中断。我们必须使用函数 HAL_TIM_SlaveConfigSynchron_IT()，而不是函数 HAL_TIM_SlaveConfigSynchron()。显然，必须定义相应的定时器 ISR，并且必须从中调用函数 HAL_TIM_IRQHandler()。

#### 11.3.2.2 使用 CubeMX 配置主/从同步

要从 CubeMX 配置定时器为从模式，只需从 IP 面板树（从模式组合框）中选择所需的触发模式（复位模式、门控模式、触发模式），然后选择触发源，如图 11.13 所示。请记住，配置为从模式且未工作在外部时钟模式 1 的定时器，必须由内部时钟或 ETR2 时钟源提供时钟。

<!-- page: 327 -->

![Image from PDF page 327](../images/page-0327-image-01.jpeg)

图 11.13：如何配置定时器为从模式

相反，要启用主模式，我们需要从定时器配置视图中选择该模式，如图 11.14 所示。选择主模式后，即可选择 TRGO 源事件。

![Image from PDF page 327](../images/page-0327-image-02.jpeg)

图 11.14：如何配置定时器为主模式

### 11.3.3 通过软件生成定时器相关事件

定时器通常在满足特定条件时生成事件。例如，当计数器寄存器 (CNT) 与周期值匹配时，它们会生成更新事件 (UEV)。然而，我们可以通过软件强制定时器生成特定事件。每个定时器都提供一个专用寄存器，名为事件生成器 (EGR)。该寄存器中的某些位用于触发定时器相关事件。例如，第一个位名为更新生成器 (UG)，当置位时允许生成 UEV 事件。一旦事件生成，该位会自动清零。

要通过软件生成事件，HAL 提供了以下函数：

<!-- page: 328 -->

```text
HAL_StatusTypeDef HAL_TIM_GenerateEvent(TIM_HandleTypeDef *htim, uint32_t EventSource);
```

该函数接受指向定时器句柄的指针以及要生成的事件。EventSource 参数可以取表 11.15 中的一个值。

表 11.15：软件可触发的事件

事件源 描述

TIM_EVENTSOURCE_UPDATE 定时器更新事件源 TIM_EVENTSOURCE_CC1 定时器捕获比较 1 事件源 TIM_EVENTSOURCE_CC2 定时器捕获比较 2 事件源 TIM_EVENTSOURCE_CC3 定时器捕获比较 3 事件源 TIM_EVENTSOURCE_CC4 定时器捕获比较 4 事件源 TIM_EVENTSOURCE_COM 定时器 COM 事件源 TIM_EVENTSOURCE_TRIGGER 定时器触发事件源 TIM_EVENTSOURCE_BREAK 定时器断路事件源

TIM_EVENTSOURCE_UPDATE 扮演两个重要角色。第一个与定时器运行时周期寄存器（即 TIMx->ARR 寄存器）的更新方式有关。默认情况下，除非定时器配置不同，否则当生成 TIM_EVENTSOURCE_UPDATE 事件时，ARR 寄存器的内容会被传输到内部影子寄存器。稍后会有更多介绍。

当配置为主模式的定时器的 TRGO 输出设置为 TIM_TRGO_RESET 模式时，TIM_EVENTSOURCE_UPDATE 事件也很有用：在这种情况下，只有使用 TIMx->EGR 寄存器生成 TIM_EVENTSOURCE_UPDATE 事件（即置位 UG 位）时，从定时器才会被触发。

以下代码展示了软件事件生成是如何工作的（该示例基于 STM32F401RE 微控制器）。TIM3 和 TIM4 是两个分别配置为主模式和从模式的定时器。TIM4 配置为工作在 ETR1 模式（即由主定时器提供时钟）。TIM3 配置为当 TIM3->EGR 寄存器的 UG 位置位时触发 TRGO 输出（该输出内部连接到 ITR2 线）。最后，我们在 main() 例程中每 200ms 手动生成一次 UEV 事件。

```text
int main(void) {
...
while (1) {
HAL_TIM_GenerateEvent(&htim3, TIM_EVENTSOURCE_UPDATE);
HAL_Delay(200);
}
...
}
void MX_TIM3_Init(void){
TIM_ClockConfigTypeDef sClockSourceConfig;
TIM_MasterConfigTypeDef sMasterConfig;
```

<!-- page: 329 -->

```text
htim3.Instance = TIM3;
htim3.Init.Prescaler = 65535;
htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
htim3.Init.Period = 120;
htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
HAL_TIM_Base_Init(&htim3);
sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
HAL_TIM_ConfigClockSource(&htim3, &sClockSourceConfig);
sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_ENABLE;
HAL_TIMEx_MasterConfigSynchronization(&htim3, &sMasterConfig);
}
void MX_TIM4_Init(void) {
TIM_SlaveConfigTypeDef sSlaveConfig;
htim4.Instance = TIM4;
htim4.Init.Prescaler = 0;
htim4.Init.CounterMode = TIM_COUNTERMODE_UP;
htim4.Init.Period = 1;
htim4.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
HAL_TIM_Base_Init(&htim4);
sSlaveConfig.SlaveMode = TIM_SLAVEMODE_EXTERNAL1;
sSlaveConfig.InputTrigger = TIM_TS_ITR2;
HAL_TIM_SlaveConfigSynchro_IT(&htim4, &sSlaveConfig);
}
```

### 11.3.4 计数模式

## 在本章开头，我们看到基本定时器从零计数到给定的周期值。通用定时器和高级定时器可以以其他不同的方式计数，如表 11.4 所示。图 11.15 展示了三种主要的计数模式。

## 当定时器以 TIM_COUNTERMODE_DOWN 模式计数时，它从 Period 值开始向下计数至零：当计数器到达终点时，会触发定时器中断（IRQ）并置位 UIF 标志（即生成更新事件，并由 HAL 调用 HAL_TIM_PeriodElapsedCallback()）。

<!-- page: 330 -->

![Image from PDF page 330](../images/page-0330-image-01.png)

图 11.15：通用定时器的三种主要计数模式

相反，当定时器以 TIM_COUNTERMODE_CENTERALIGNED 模式计数时，它从零开始向上计数至 Period 值：这会导致触发定时器中断（IRQ）并置位 UIF 标志（即生成更新事件，并由 HAL 调用 HAL_TIM_PeriodElapsedCallback()）。随后，定时器开始向下计数至零，并生成另一个更新事件（以及相应的中断）。

### 11.3.5 输入捕获模式

通用定时器并非设计用作时基发生器。尽管完全可以使用它们来完成此任务，但也可以使用其他定时器（如基本定时器和 SysTick 定时器）来执行此任务。通用定时器提供了更高级的功能，可用于驱动其他重要的时间相关活动。

图 11.16 展示了通用定时器中²⁶ 输入通道的结构。如图所示，每个输入都连接到一个边沿检测器，该检测器还配备了一个用于对输入信号进行“去抖动”的滤波器。边沿检测器的输出进入一个源多路复用器（IC1、IC2 等）。如果某个 I/O 被分配给另一个外设，这允许“重映射”输入通道。最后，一个专用的预分频器允许“降低”输入信号的频率，以便在无法降低定时器运行频率的情况下（我们稍后会看到）使其与定时器运行频率匹配。

²⁶ 某些通用定时器（例如 TIM14）具有较少的输入通道，因此其输入级结构较为简化。请参阅您 MCU 的参考手册以了解您将要使用的定时器的确切结构。

<!-- page: 331 -->

![Image from PDF page 331](../images/page-0331-image-01.jpeg)

图 11.16：通用定时器中输入通道的结构

通用定时器和高级定时器提供的输入捕获模式允许计算施加到这些定时器提供的 4 个通道中每一个的外部信号的频率。并且捕获是对每个通道独立进行的。

![Image from PDF page 331](../images/page-0331-image-02.png)

图 11.17：外部信号馈入定时器其中一个通道的捕获过程

图 11.17 展示了捕获过程的工作原理。TIMx 是一个定时器，配置为以给定的 TIMx_CLK 时钟频率²⁷ 工作。这意味着它每 1 T IMx_CLK 秒将 TIMx_CNT 寄存器递增一次，直到达到 Period 值。假设我们将一个方波信号施加到定时器的一个通道上，并假设我们配置定时器在输入信号的每个上升沿触发

²⁷ 定时器时钟频率与定时器的工作方式（在此情况下为输入捕获模式）无关。如前几段所述，定时器时钟取决于总线频率或外部时钟源以及相关的预分频器设置。

<!-- page: 332 -->

输入信号，那么 TIMx_CCRx²⁸ 寄存器将在检测到每次转换时更新为 TIMx_CNT 寄存器的内容。当这种情况发生时，定时器将生成相应的中断或 DMA 请求，从而允许跟踪计数器的值。

要获取外部信号的周期，需要两次连续的捕获。周期是通过减去这两个值（CNT0（图 11.17 中的值 4）和 CNT1（图 11.17 中的值 20））并使用以下公式计算的：

)−1 [4]

Period = Capture · ( TIMx_CLK (Prescaler + 1)(CHP rescaler)(PolarityIndex)

其中：

Capture = CNT1 −CNT0 如果 CNT0 < CNT1 Capture = (TIMx_Period −CNT0) + CNT1 如果 CNT0 > CNT1

CHP rescaler 是可以应用于输入通道的进一步预分频器，PolarityIndex 在通道配置为在输入信号的上升沿或下降沿触发时等于 1，或者在采样两个边沿时等于 2。

另一个相关条件是 UEV 频率应低于采样信号频率。为什么这很重要是显而易见的：如果定时器运行速度比采样信号快，那么它将在能够采样信号边沿之前溢出（即 Period 计数器耗尽）（见图 11.18）。因此，通常建议将 Period 值设置为最大值，并增加 Prescaler 因子以降低计数频率。

![Image from PDF page 332](../images/page-0332-image-01.png)

图 11.18：如果定时器运行速度比采样信号快，则会在检测到两个上升沿之前溢出

要配置输入通道，我们使用函数 HAL_TIM_IC_ConfigChannel() 和 C 结构体 TIM_IC_InitTypeDef 的一个实例，其定义如下：

²⁸ CCR 是 Capture Compare Register（捕获比较寄存器）的缩写，x 是通道号。

<!-- page: 333 -->

```text
typedef struct {
uint32_t ICPolarity;
/* Specifies the active edge of the input signal. */
uint32_t ICSelection;
/* Specifies the input. */
uint32_t ICPrescaler;
/* Specifies the Input Capture Prescaler. */
uint32_t ICFilter;
/* Specifies the input capture filter. */
} TIM_IC_InitTypeDef;
```

- ICPolarity：指定输入信号的极性，其值可取自表 11.16。
- ICSelection：指定定时器使用的输入。其值可取自表 11.17。可以选择性地将输入通道重映射到不同的输入源，即 (IC1,IC2) 映射到 (TI2,TI1)，(IC3,IC4) 映射到 (TI4,TI3)。通常这用于区分上升沿捕获和下降沿捕获，适用于 Ton 与 Toff 不同的信号。也可以从名为 TRC 的同一内部通道进行捕获，该通道连接到 ITR0..ITR3 源。
- ICPrescaler：配置给定输入的预分频级。其值可取自表 11.18。
- ICFilter：此 4 位字段定义了用于采样连接到 TIMx_CHx 引脚的外部时钟信号的频率，以及应用于该信号的数字滤波器的长度。它有助于对输入信号进行去抖动。有关更多信息，请参阅您 MCU 的数据手册。

表 11.16：可用的输入捕获极性

输入捕获极性模式 描述

TIM_ICPOLARITY_RISING 捕获外部信号的上升沿 TIM_ICPOLARITY_FALLING 捕获外部信号的下降沿 TIM_ICPOLARITY_BOTHEDGE 外部信号的上升沿和下降沿确定捕获周期（这将增加采样信号的频率）

表 11.17：可用的输入捕获选择模式

输入捕获选择模式 描述

TIM_ICSELECTION_DIRECTTI 选择 TIM 输入 1、2、3 或 4 分别连接到 IC1、IC2、IC3 或 IC4 TIM_ICSELECTION_INDIRECTTI 选择 TIM 输入 1、2、3 或 4 分别连接到 IC2、IC1、IC4 或 IC3。 TIM_ICSELECTION_TRC 选择 TIM 输入 1、2、3 或 4 连接到 TRC（图 11.3 中的触发线 - 图 11.16 中高亮显示为红色的 TRC 输入）

<!-- page: 334 -->

表 11.18：可用的输入预分频模式

### 输入捕获预分频模式说明

TIM_ICPSC_DIV1 不使用预分频 TIM_ICPSC_DIV2 每 2 个事件捕获一次 TIM_ICPSC_DIV4 每 4 个事件捕获一次 TIM_ICPSC_DIV8 每 8 个事件捕获一次

## 现在是时候来看一个实际示例了。我们将重新排列本章的示例 2，以便通过 TIM3 定时器的通道 1 对 PA5 引脚（连接到 LD2 LED 的那个引脚）的开关频率进行采样（在 STM32F072 微控制器中，该引脚与 PA6 引脚重合）。我们将通道 1 配置为输入捕获引脚，并将其配置为直接存储器访问（DMA）模式，以便在检测到输入信号的上升沿时，触发 TIM_DMA_ID_CC1 请求，自动填充一个临时缓冲区，该缓冲区存储 TIM3_CNT 寄存器的值。

## 在分析 main() 函数之前，最好先看一下 TIM3 的初始化例程。

```text
Filename: Core/Src/main-ex6.c
59
/* TIM3 init function */
60
void MX_TIM3_Init(void) {
61
TIM_IC_InitTypeDef sConfigIC;
```

62

```text
63
htim3.Instance = TIM3;
64
htim3.Init.Prescaler = 999;
65
htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
66
htim3.Init.Period = 65535;
67
htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
68
HAL_TIM_IC_Init(&htim3);
```

69

```text
70
sConfigIC.ICPolarity = TIM_INPUTCHANNELPOLARITY_RISING;
71
sConfigIC.ICSelection = TIM_ICSELECTION_DIRECTTI;
72
sConfigIC.ICPrescaler = TIM_ICPSC_DIV1;
73
sConfigIC.ICFilter = 0;
74
HAL_TIM_IC_ConfigChannel(&htim3, &sConfigIC, TIM_CHANNEL_1);
75
}
```

76

```text
77
void HAL_TIM_IC_MspInit(TIM_HandleTypeDef* htim_ic) {
78
GPIO_InitTypeDef GPIO_InitStruct;
79
if (htim_ic->Instance == TIM3) {
80
/* Peripheral clock enable */
81
__HAL_RCC_TIM3_CLK_ENABLE();
```

82

```text
83
/**TIM3 GPIO Configuration
84
PA6
------> TIM3_CH1
85
*/
86
GPIO_InitStruct.Pin = GPIO_PIN_6;
87
GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
```

<!-- page: 335 -->

```text
88
GPIO_InitStruct.Pull = GPIO_NOPULL;
89
GPIO_InitStruct.Speed = GPIO_SPEED_LOW;
90
GPIO_InitStruct.Alternate = GPIO_AF1_TIM3;
91
HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
```

92

```text
93
/* Peripheral DMA init*/
94
hdma_tim3_ch1_trig.Instance = DMA1_Channel4;
95
hdma_tim3_ch1_trig.Init.Direction = DMA_PERIPH_TO_MEMORY;
96
hdma_tim3_ch1_trig.Init.PeriphInc = DMA_PINC_DISABLE;
97
hdma_tim3_ch1_trig.Init.MemInc = DMA_MINC_ENABLE;
98
hdma_tim3_ch1_trig.Init.PeriphDataAlignment = DMA_PDATAALIGN_HALFWORD;
99
hdma_tim3_ch1_trig.Init.MemDataAlignment = DMA_MDATAALIGN_HALFWORD;
100
hdma_tim3_ch1_trig.Init.Mode = DMA_NORMAL;
101
hdma_tim3_ch1_trig.Init.Priority = DMA_PRIORITY_LOW;
102
HAL_DMA_Init(&hdma_tim3_ch1_trig);
103
104
/* Several peripheral DMA handle pointers point to the same DMA handle.
105
Be aware that there is only one channel to perform all the requested DMAs. */
106
__HAL_LINKDMA(htim_ic, hdma[TIM_DMA_ID_CC1], hdma_tim3_ch1_trig);
107
}
108
}
```

![Image from PDF page 335](../images/page-0335-image-01.png)

图 11.19：如何在 Nucleo-F072RB 中连接 PA5 和 PA6 引脚

## MX_TIM3_Init() 配置 TIM3 定时器，使其以约 0.732Hz 的频率运行。随后，第一个通道被配置为在输入信号的每个上升沿触发捕获事件（TIM_DMA_ID_CC1）。然后，HAL_TIM_IC_MspInit() 配置硬件部分（连接到 TIM3 通道 1 的 PA6 引脚）以及用于配置 TIM_DMA_ID_CC1

<!-- page: 336 -->

## 请求的 DMA 描述符。

![Image from PDF page 336](../images/page-0336-image-01.png)

这里有两点需要注意。首先，DMA 被配置为外设和内存数据对齐均设置为执行 16 位传输，因为定时器计数器寄存器是 16 位宽的。在 TIM2 和 TIM5 定时器具有 32 位宽计数器寄存器的微控制器中，您需要设置 DMA 以执行字对齐传输。其次，由于我们在第 69 行使用了 HAL_TIM_IC_Init()，HAL 被设计为调用 HAL_TIM_IC_MspInit() 函数来执行底层初始化，而不是调用 HAL_TIM_Base_MspInit()。

```text
Filename: Core/Src/main-ex6.c
20
uint8_t
odrVals[] = { 0x0, 0xFF };
21
uint16_t captures[2];
22
volatile uint8_t
captureDone = 0;
```

23

```text
24
int main(void) {
25
uint16_t diffCapture = 0;
26
char msg[30];
```

27

```text
28
HAL_Init();
```

29

```text
30
Nucleo_BSP_Init();
31
MX_DMA_Init();
```

32

```text
33
MX_TIM3_Init();
34
MX_TIM6_Init();
```

35

```text
36
HAL_DMA_Start(&hdma_tim6_up, (uint32_t) odrVals, (uint32_t) &GPIOA->ODR, 2);
37
__HAL_TIM_ENABLE_DMA(&htim6, TIM_DMA_UPDATE);
38
HAL_TIM_Base_Start(&htim6);
```

39

```text
40
HAL_TIM_IC_Start_DMA(&htim3, TIM_CHANNEL_1, (uint32_t*) captures, 2);
```

41

```text
42
while (1) {
43
if (captureDone != 0) {
44
if (captures[1] >= captures[0])
45
diffCapture = captures[1] - captures[0];
46
else
47
diffCapture = (htim3.Instance->ARR - captures[0]) + captures[1];
```

48

```text
49
frequency = HAL_RCC_GetPCLK1Freq() / (htim3.Instance->PSC + 1);
50
frequency = (float) frequency / diffCapture;
```

51

```text
52
sprintf(msg, "Input frequency: %.3f\r\n", frequency);
53
HAL_UART_Transmit(&huart2, (uint8_t*) msg, strlen(msg), HAL_MAX_DELAY);
54
while (1);
```

<!-- page: 337 -->

```text
55
}
56
}
57
}
```

应用程序中最相关的部分是 main() 函数。我们首先使用 MX_TIM6_Init() 函数初始化 TIM6 定时器（它被配置为以 40Hz 运行——这意味着 PA5 引脚每 50ms = 20Hz 被置为高电平），然后按照本章前面所述，以 DMA 模式启动它。接着，我们启动 TIM3，并使用 HAL_TIM_IC_Start_DMA() 函数（第 40 行）在第一个通道上启用 DMA 模式。captures 数组用于存储在该通道上获取的两个连续捕获值。

第 [42:53] 行是我们计算外部信号频率的部分。当两个捕获完成时，全局变量 captureDone 会被 HAL_TIM_IC_CaptureCallback() 回调函数（此处未显示）设置为 1，该函数在捕获过程结束时被调用。当这种情况发生时，我们使用公式 [4] 计算采样信号的频率。

为了使示例正常工作，您需要按照图 11.19 所示连接 PA5 和 PA6 引脚。请务必检查您的 Nucleo 开发板上这些引脚是否路由到 Morpho 连接器的相应位置。

#### 11.3.5.1 使用 CubeMX 配置输入捕获模式

借助 CubeMX，配置通用定时器的输入通道以进入输入捕获模式变得轻而易举。为了将一个通道绑定到对应的输入（即 IC1 绑定到 TI1），您需要为期望的通道选择“输入捕获直接模式”（Input capture direct mode），如图 11.20 所示。

![Image from PDF page 337](../images/page-0337-image-01.jpeg)

图 11.20：如何启用通道的输入捕获模式

相反，为了将一对中的另一个通道（(IC1,IC2) 或 (IC3,IC4)）映射到相同的输入（即对于 (IC1,IC2) 对，映射到 TI1 或 TI2），您可以启用该对中的另一个通道为“输入捕获间接模式”（Input capture indirect mode），如图 11.21 所示。最后，从 TIMx 配置视图（此处未展示）中，可以配置其他输入捕获参数（如通道极性、滤波器设置等）。

<!-- page: 338 -->

![Image from PDF page 338](../images/page-0338-image-01.jpeg)

图 11.21：如何启用通道的输入捕获间接模式

### 11.3.6 输出比较模式

到目前为止，我们使用了两种技术来控制 GPIO 电平，一种使用中断，另一种使用 DMA。它们都利用更新事件（UEV event）的产生来切换配置为输出引脚的 GPIO。输出比较（Output Compare）是通用定时器和高级定时器提供的一种模式，它允许在通道比较寄存器（TIMx_CCRx）与定时器计数器寄存器（TIMx_CNT）匹配时控制输出通道的状态。

程序员可以使用六种²⁹输出比较模式：

- 输出比较计时³⁰：输出比较寄存器（CCRx）与计数器（CNT）之间的比较对输出没有影响。此模式用于生成计时基准。
- 输出比较激活：匹配时将通道输出设置为激活电平。当计数器（CNT）与捕获/比较寄存器（CCRx）匹配时，通道输出被强制置高。
- 输出比较非激活：匹配时将通道设置为非激活电平。当计数器（CNT）与捕获/比较寄存器（CCRx）匹配时，通道输出被强制置低。
- 输出比较翻转：当计数器（CNT）与捕获/比较寄存器（CCRx）匹配时，通道输出发生翻转。
- 输出比较强制激活/非激活：无论计数器值如何，通道输出被强制置高（激活模式）或置低（非激活模式）。

定时器的每个通道都通过函数 HAL_TIM_OC_ConfigChannel() 和 C 结构体 TIM_OC_InitTypeDef 的一个实例配置为输出比较模式，其定义如下：

²⁹输出比较模式实际上有八种，但其中两种与 PWM 输出相关，将在下一段中分析。³⁰此模式在 CubeMX 中被称为冻结模式（Frozen mode）。

<!-- page: 339 -->

```text
typedef struct {
uint32_t OCMode;
/* Specifies the TIM mode. */
uint32_t Pulse;
/* Specifies the pulse value to be loaded
into the Capture Compare Register. */
uint32_t OCPolarity;
/* Specifies the output polarity. */
uint32_t OCNPolarity;
/* Specifies the complementary output polarity.*/
uint32_t OCFastMode;
/* Specifies the Fast mode state. */
uint32_t OCIdleState;
/* Specifies the TIM Output Compare pin state during Idle state.*/
uint32_t OCNIdleState; /* Specifies the complementary
TIM Output Compare pin
state during Idle state. */
} TIM_OC_InitTypeDef;
```

- OCMode：指定输出比较模式，其值可取自表 11.19。
- Pulse：该字段的内容将存储在 CCRx 寄存器中，并确定何时触发输出。请确保定时器周期设置为 Pulse 字段的倍数，否则请准备好相应处理整数除法的余数。
- OCPolarity：定义当 CCRx 寄存器与 CNT 寄存器匹配时的输出通道极性。其值可取自表 11.20。
- OCNPolarity：定义互补输出极性。这是仅在 TIM1 和 TIM8 高级定时器中可用的模式，允许在额外的专用通道上生成互补信号（即当 CH1 为高电平时 CH1n 为低电平，反之亦然）。此功能特别针对电机控制应用设计，本书中不予详细描述。其值可取自表 11.21。
- OCFastMode：指定快速模式状态。此参数仅在 PWM1 和 PWM2 模式下有效，可取值为 TIM_OCFAST_DISABLE 和 TIM_OCFAST_ENABLE。
- OCIdleState：指定定时器空闲状态期间通道输出比较引脚的状态。可取值为 TIM_OCIDLESTATE_SET 和 TIM_OCIDLESTATE_RESET。此参数仅在 TIM1 和 TIM8 高级定时器中可用。
- OCNIdleState：指定定时器空闲状态期间互补通道输出比较引脚的状态。可取值为 TIM_OCNIDLESTATE_SET 和 TIM_OCNIDLESTATE_RESET。此参数仅在 TIM1 和 TIM8 高级定时器中可用。

表 11.19：可用的输出比较模式

输出比较模式 描述

TIM_OCMODE_TIMING 输出比较寄存器（CCRx）与计数器（CNT）之间的比较对输出没有影响（又称冻结模式） TIM_OCMODE_ACTIVE 匹配时将通道输出设置为激活电平 TIM_OCMODE_INACTIVE 匹配时将通道设置为非激活电平 TIM_OCMODE_TOGGLE 当计数器（CNT）与捕获/比较寄存器（CCRx）匹配时，通道输出发生翻转 TIM_OCMODE_PWM1 PWM 模式 1 - 见下一段 TIM_OCMODE_PWM2 PWM 模式 2 - 见下一段 TIM_OCMODE_FORCED_ACTIVE 无论计数器值如何，通道输出被强制置高 TIM_OCMODE_FORCED_INACTIVE 无论计数器值如何，通道输出被强制置低

<!-- page: 340 -->

表 11.20：可用的输出比较极性模式

输出比较极性模式 描述

TIM_OCPOLARITY_HIGH 当 CCRx 和 CNT 寄存器匹配时，输出通道被置高 TIM_OCPOLARITY_LOW 当 CCRx 和 CNT 寄存器匹配时，输出通道被置低

表 11.21：可用的互补输出比较极性模式

互补输出比较极性模式 描述

TIM_OCNPOLARITY_HIGH 当 CCRx 和 CNT 寄存器匹配时，互补输出通道被置高 TIM_OCNPOLARITY_LOW 当 CCRx 和 CNT 寄存器匹配时，互补输出通道被置低

当 CCRx 寄存器与定时器 CNT 计数器匹配，且通道被配置为工作在输出比较模式时，会生成一个特定的中断（如果已启用）。这使得可以独立控制每个通道的切换频率，并最终实现通道间的相位偏移。通道频率可以使用以下公式计算：

CHx_Update = TIMx_CLK

CCRx [5]

其中：

TIMx_CLK 是定时器的工作频率，CCRx 是用于配置通道的 TIM_OnePulse_InitTypeDef 结构体中的 Pulse 值。这意味着，给定一个通道频率，我们可以按以下方式计算 Pulse 值：

Pulse = TIMx_CLK

CHx_Update [6]

显然，重要的是要强调，定时器频率必须设置得使通过 [6] 计算出的 Pulse 值小于定时器的 Period 值（CCRx 值不能高于 TIM->ARR 值，该值对应于定时器的 Period）。

以下示例展示了如何生成两个输出方波信号，一个运行在 25kHz，另一个运行在 50kHz。它使用 TIM3 定时器的通道 1 和通道 2（分别绑定到 OC1 和 OC2），并设计用于在 Nucleo-F072RB 上运行。

<!-- page: 341 -->

```text
Filename: Core/Src/main-ex7.c
17
volatile uint16_t CH1_FREQ = 0;
18
volatile uint16_t CH2_FREQ = 0;
```

19

```text
20
int main(void) {
21
HAL_Init();
```

22

```text
23
Nucleo_BSP_Init();
24
MX_TIM3_Init();
```

25

```text
26
HAL_TIM_OC_Start_IT(&htim3, TIM_CHANNEL_1);
27
HAL_TIM_OC_Start_IT(&htim3, TIM_CHANNEL_2);
```

28

```text
29
while (1);
30
}
```

31

```text
32
/* TIM3 init function */
33
void MX_TIM3_Init(void) {
34
TIM_OC_InitTypeDef sConfigOC;
```

35

```text
36
htim3.Instance = TIM3;
37
htim3.Init.Prescaler = 2;
38
htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
39
htim3.Init.Period = 63999;
40
htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
41
HAL_TIM_OC_Init(&htim3);
```

42

```text
43
CH1_FREQ = computePulse(&htim3, 25000); /* 25kHZ switching frequency */
44
CH2_FREQ = computePulse(&htim3, 50000); /* 50kHZ switching frequency */
```

45

```text
46
sConfigOC.OCMode = TIM_OCMODE_TOGGLE;
47
sConfigOC.Pulse = 0;
48
sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
49
sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
50
HAL_TIM_OC_ConfigChannel(&htim3, &sConfigOC, TIM_CHANNEL_1);
```

51

```text
52
sConfigOC.Pulse = 0;
53
HAL_TIM_OC_ConfigChannel(&htim3, &sConfigOC, TIM_CHANNEL_2);
54
}
```

## 第 [48:59] 行将通道 1 和通道 2 配置为输出比较通道。两者均配置为翻转模式（即，每当 CCRx 寄存器与 CNT 定时器寄存器匹配时，GPIO 的状态就会反转）。TIM3 被配置为以 16MHz 运行，因此，使用公式 [6] 的函数 computePulse() 将分别返回 640 和 320，以使通道的切换频率分别等于 50kHz 和 100kHz。然而，上述代码仍不足以以该频率驱动 GPIO。在这里，我们配置通道，使得它们

<!-- page: 342 -->

## 每当定时器 CNT 寄存器等于通道 1 的 640 和通道 2 的 320 时，其输出就会翻转。但这意味着切换频率等于：

16.000.000

# 65535 + 1 = 244Hz

## 并且两个通道之间只有 10µs 的相位偏移，如图 11.22 所示。该 65535 值对应于定时器的 Period（周期）值，即定时器 CNT 寄存器达到的最大值。

![Image from PDF page 342](../images/page-0342-image-01.jpeg)

图 11.22：通道 1 和通道 2 之间的翻转偏移

## 为了达到期望的切换频率³¹，我们需要在 TIM3 CNT 寄存器每 640 和 320 个计数时翻转输出。为此，我们可以定义以下回调例程：

```text
Filename: Core/Src/main-ex7.c
56
void HAL_TIM_OC_DelayElapsedCallback(TIM_HandleTypeDef *htim) {
57
uint32_t pulse;
58
uint16_t arr = __HAL_TIM_GET_AUTORELOAD(htim);
```

59

```text
60
/* TIMx_CH1 toggling with frequency = 50KHz */
61
if(htim->Channel == HAL_TIM_ACTIVE_CHANNEL_1) {
62
pulse = HAL_TIM_ReadCapturedValue(htim, TIM_CHANNEL_1);
63
/* Set the Capture Compare Register value */
64
if((pulse + CH1_FREQ) < arr)
65
__HAL_TIM_SET_COMPARE(htim, TIM_CHANNEL_1, (pulse + CH1_FREQ));
66
else
67
__HAL_TIM_SET_COMPARE(htim, TIM_CHANNEL_1, (pulse + CH1_FREQ) - arr);
68
}
```

69

```text
70
/* TIMx_CH2 toggling with frequency = 100KHz */
71
if(htim->Channel == HAL_TIM_ACTIVE_CHANNEL_2) {
72
pulse = HAL_TIM_ReadCapturedValue(htim, TIM_CHANNEL_2);
73
/* Set the Capture Compare Register value */
74
if((pulse + CH2_FREQ) < arr)
```

³¹请确保 GPIO 速度已配置，使得允许的最大切换频率与期望的定时器切换频率处于同一数量级。

<!-- page: 343 -->

```text
75
__HAL_TIM_SET_COMPARE(htim, TIM_CHANNEL_2, (pulse + CH2_FREQ));
76
else
77
__HAL_TIM_SET_COMPARE(htim, TIM_CHANNEL_2, (pulse + CH2_FREQ) - arr);
78
}
79
}
```

HAL_TIM_OC_DelayElapsedCallback() 由 HAL 在通道 CCRx 寄存器与定时器计数器匹配时自动调用。因此，我们可以将通道 1 的 Pulse（即 CCRx 寄存器）增加 CH1_FREQ，将通道 2 的 Pulse 增加 CH2_FREQ。这将导致相应通道以期望的频率切换，如图 11.23 所示。

![Image from PDF page 343](../images/page-0343-image-01.jpeg)

图 11.23：通道 2 被配置为以通道 1 两倍的速度切换

使用 DMA 模式和预初始化的向量也可以获得相同的结果，该向量最终可以使用 const 修饰符存储在闪存中：

```text
const uint16_t ch1IV[] = {320, 640, 960, ...};
...
HAL_TIM_OC_Start_DMA(&htim3, TIM_CHANNEL_1, (uint32_t)ch1IV, sizeof(ch1IV));
```

#### 11.3.6.1 使用 CubeMX 配置输出比较模式

在 CubeMX 中配置输出比较模式的过程与配置输入捕获模式的过程相同。第一步是为期望的通道选择 Output compare CHx（输出比较 CHx）模式，如图 11.20 所示。接下来，从 TIMx 配置视图（此处未显示）中，可以配置其他输出比较参数（输出模式、通道极性等）。

### 11.3.7 脉宽生成

迄今为止生成的方波都有一个共同特征：它们的 TON 周期等于 TOFF 周期。因此，它们也被称为具有 50% 的占空比。占空比是指在一个周期（例如 1s）内信号处于活动状态的百分比。作为公式，占空比表示为：

<!-- page: 344 -->

D = TON Period × 100% [8]

其中 D 是占空比，TON 是信号处于活动状态的时间。因此，50% 的占空比意味着信号 50% 的时间处于开启状态，50% 的时间处于关闭状态。占空比并不说明持续时间有多长。对于 50% 占空比，“开启时间”可以是几分之一秒、一天，甚至一周，具体取决于周期的长度。脉宽是给定实际周期时 TON 的持续时间。例如，假设周期为 1s，20% 的占空比会产生 200ms 的脉宽。

![Image from PDF page 344](../images/page-0344-image-01.png)

图 11.24：三种不同的占空比 - 50%、20% 和 80%

图 11.24 显示了三种不同的占空比：50%、20% 和 80%。

脉宽调制（PWM）是一种用于在给定时间段内（或者，如果你愿意，在给定频率下）生成具有不同占空比的多个脉冲的技术。PWM 在数字电子学中有很多应用，但它们都可以归为两大类：

- 控制输出电压（从而控制电流）；
- 对消息（即数字电子学中的一系列字节³²）进行编码（即调制）到载波（以给定频率运行）上。

这两类可以扩展为 PWM 技术的多种实际用途。将注意力集中在输出电压的控制上，我们可以找到几种应用：

- 生成从 0V 到 VDD 范围的输出电压（即 I/O 允许的最大电压，在 STM32 中为 3.3V）；

³²然而，请记住，作为调制技术的 PWM 并不局限于数字电子学，它起源于“模拟时代”，当时用于将音频波调制到载波频率上。

<!-- page: 345 -->

- LED 调光；
- 电机控制；
- 电源转换；
- 生成以给定频率运行的输出波形（正弦波、三角波、方波等）；
- 声音输出；

通过适当的输出滤波，通常涉及使用低通滤波器，PWM 可以复制 DAC 的行为，即使 MCU 不提供 DAC。通过改变输出引脚的占空比，可以按比例调节输出电压。放大器可以根据需要增加/减小电压范围，并且还可以使用功率晶体管控制大电流和负载。

使用函数 HAL_TIM_PWM_ConfigChannel() 和上一段中看到的 C 结构体 TIM_OC_InitTypeDef 的实例来配置定时器通道为 PWM 模式。TIM_OC_InitTypeDef.Pulse 字段定义占空比，其范围从 0 到定时器的 Period 字段。Period 越长，调节范围越宽。这意味着我们可以微调输出电压。

![Image from PDF page 345](../images/page-0345-image-01.png)

周期（Period）的选择——它与定时器时钟（内部、外部等）共同决定了输出信号的频率——绝非可以随意决定的细节。这取决于具体的应用领域，并且可能对整体电磁干扰（EMI）发射产生严重影响。此外，某些使用脉宽调制（PWM）技术控制的设备在特定频率下可能会发出可听噪声。例如，电动机在处于人耳听觉范围内的频率下受控时，可能会发出令人不悦的嗡嗡声。另一个与此关联不大但成因相似的例子是开关电源中功率电感器发出的噪声。这些电源利用 PWM 的底层概念来调节输出电压，进而调节电流。有时，输出噪声是不可避免的，需要使用清漆等产品来减轻问题。而在其他情况下，正确的频率源自“自然限制”：以接近 100Hz 的频率调节 LED 的亮度，通常足以避免可见的光闪烁。

有两种可用的 PWM 模式：PWM 模式 1 和 PWM 模式 2。两者都可以通过字段 `TIM_OC_InitTypeDef.OCMode` 进行配置，使用值 `TIM_OCMODE_PWM1` 和 `TIM_OCMODE_PWM2`。让我们来看看它们的区别。

- PWM 模式 1：在向上计数时，只要 Period < Pulse，通道即为活动状态，否则为非活动状态。在向下计数时，只要 Period > Pulse，通道即为非活动状态，否则为活动状态。
- PWM 模式 2：在向上计数时，只要 Period < Pulse，通道 1 即为非活动状态，否则为活动状态。在向下计数时，只要 Period > Pulse，通道 1 即为活动状态，否则为非活动状态。

以下示例展示了 PWM 技术的一个典型应用：LED 调光。该示例设计用于在 Nucleo-F401RE 上运行，并使 LD2 LED³³ 进行淡入/淡出效果。

³³不幸的是，并非所有 Nucleo 开发板都将 LD2 LED 连接到定时器通道（这取决于 LQFP-64 STM32 微控制器的引脚布局是否完全兼容这一事实）。只有七款开发板具备此功能。拥有其他 Nucleo 开发板的用户需要使用外部 LED 重新调整该示例。

<!-- page: 346 -->

```text
Filename: Core/Src/main-ex8.c
11
int main(void) {
12
HAL_Init();
```

13

```text
14
Nucleo_BSP_Init();
15
MX_TIM2_Init();
```

16

```text
17
HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_1);
```

18

```text
19
uint16_t dutyCycle = HAL_TIM_ReadCapturedValue(&htim2, TIM_CHANNEL_1);
```

20

```text
21
while(1) {
22
while(dutyCycle < __HAL_TIM_GET_AUTORELOAD(&htim2)) {
23
__HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_1, ++dutyCycle);
24
HAL_Delay(1);
25
}
```

26

```text
27
while(dutyCycle > 0) {
28
__HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_1, --dutyCycle);
29
HAL_Delay(1);
30
}
31
}
32
}
```

33

```text
34
/* TIM3 init function */
35
void MX_TIM2_Init(void) {
36
TIM_OC_InitTypeDef sConfigOC;
```

37

```text
38
htim2.Instance = TIM2;
39
htim2.Init.Prescaler = 499;
40
htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
41
htim2.Init.Period = 999;
42
htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
43
HAL_TIM_PWM_Init(&htim2);
```

44

```text
45
sConfigOC.OCMode = TIM_OCMODE_PWM1;
46
sConfigOC.Pulse = 0;
47
sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
48
sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
49
HAL_TIM_PWM_ConfigChannel(&htim2, &sConfigOC, TIM_CHANNEL_1);
50
}
```

## 第 [45:49] 行将定时器 TIM2 的第一个通道配置为工作在 PWM 模式 1。占空比（duty cycle）的范围将从 0 到 999，这对应于 Period 的值。这意味着，如果输出经过良好滤波（且 PCB 布局良好），我们可以以约 0.0033V 的步长调节输出电压。这接近于 10 位 DAC 的性能。

<!-- page: 347 -->

第 [21:32] 行是实现淡入/淡出效果的地方。第一个循环每 1ms 将 Pulse 的值（对应于捕获比较寄存器 1 (CCR1)）递增，直到达到 Period 的值（对应于自动重载寄存器 (ARR)）。这意味着在不到 1 秒的时间内，LED 将达到全亮。第二个循环以相同的方式递减 Pulse 字段，直到其达到零。

![Image from PDF page 347](../images/page-0347-image-01.png)

定时器的更新频率设置为 84MHz³⁴/(499+1)(999+1)=168Hz。通过将 Prescaler 设置为 249 并将 Period 设置为 1999，也可以获得相同的频率。但是淡入/淡出效果会发生变化。为什么会这样？如果你无法解释其中的差异，我强烈建议先休息一下，然后自己动手做实验。

#### 11.3.7.1 使用 PWM 生成正弦波

使用 PWM 技术生成的输出方波可以通过滤波生成平滑信号，即峰峰值电压（Vpp）降低的模拟信号。电阻-电容（RC）低通滤波器（参见图 11.25）可以截止所有频率高于给定阈值的交流信号。RC 低通滤波器的一般经验法则是：截止频率越低，Vpp³⁵ 越低。RC 低通滤波器利用了电容的一个重要特性：能够阻断直流电流同时允许交流电流通过：给定由电阻-电容网络形成的 R/C 时间常数，滤波器会将频率高于 RC 常数的交流信号短路到地，从而允许信号的直流分量和较低频率的交流电压通过。

![Image from PDF page 347](../images/page-0347-image-02.png)

图 11.25：使用电阻和电容实现的典型低通滤波器

虽然这个电路非常简单，但为 R（电阻）和 C（电容）选择合适的值包含一些设计决策：我们可以容忍多少纹波，以及滤波器需要多快响应。这两个参数是相互排斥的。在大多数滤波器中，我们希望拥有完美的滤波器——一个让所有低于截止频率的频率通过且没有电压纹波的滤波器。不幸的是，这种理想滤波器并不存在：为了将纹波降低到零，我们必须选择一个非常大的滤波器，这会导致输出稳定所需的时间很长。虽然这对于连续且固定的电压可能是可以接受的，但如果我们试图从 PWM 信号生成复杂的波形，这对输出信号的质量会有严重影响。

³⁴当从 APB1 总线时钟驱动时，STM32F401RE MCU 中定时器的最大频率为 84MHz。 ³⁵在处理用于平滑输出波形的滤波器时，考虑对输出电压的影响比考虑滤波器的频率响应更为方便。然而，滤波器传递函数下的数学超出了本书的范围。如果有兴趣，这个在线计算器(https://bit.ly/22breq2)允许根据 VIN、PWM 频率以及 R 和 C 的值来评估 Vpp 输出。

<!-- page: 348 -->

一阶 RC 低通滤波器的截止频率 (fc) 由以下公式表示：

fc = 1 2πRC [9]

图 11.26 展示了低通滤波器对频率为 100Hz 的 PWM 信号的影响。在这里，我们选择了 1K 电阻和 10µF 电容。这意味着截止频率等于：

fc = 1 2π103 × 10−5 ≈15.9Hz

![Image from PDF page 348](../images/page-0348-image-01.jpeg)

图 11.26：截止频率等于 15.9Hz 的低通滤波器的影响

图 11.27 展示了使用 4300K 电阻和 10µF 电容的低通滤波器的影响。这意味着截止频率等于：

fc = 1 2π(4.3 × 103) × 10−5 ≈3.7Hz

如你所见，第二个滤波器允许 Vpp 约为 160mV，这对于许多应用来说是一个可以接受的电压差。

![Image from PDF page 348](../images/page-0348-image-02.jpeg)

图 11.27：截止频率等于 3.7Hz 的低通滤波器的影响

通过改变输出电压（这意味着我们改变占空比），我们可以生成任意的输出波形，其频率是 PWM 周期的一部分。这里的基本思想

<!-- page: 349 -->

其方法是将我们想要的波形（例如正弦波）划分为 “x” 个分段。对于每个分段，我们都有一个 PWM 周期。TON 时间（即占空比）直接对应该分段中波形的幅度，该幅度使用 sin() 函数计算得出。

![Image from PDF page 349](../images/page-0349-image-01.png)

图 11.28：如何使用多个 PWM 信号近似正弦波

考虑图 11.28 中所示的示意图。这里正弦波被划分为 10 个步骤。因此，我们需要 10 个按正弦方式递增/递减的不同 PWM 脉冲。占空比为 0% 的 PWM 脉冲代表最小幅度（0V），占空比为 100% 的脉冲代表最大幅度（3.3V）。由于我们的 PWM 脉冲电压在 0V 到 3.3V 之间摆动，我们的正弦波也将在 0V 到 3.3V 之间摆动。

正弦波完成一个周期需要 360 度。因此，对于 10 个分段，我们需要以 36 度为步长增加角度。这被称为角度步长率（Angle Step Rate）或角度分辨率。我们可以增加分段的数量以获得更精确的波形。但随着分段的增加，我们也需要增加分辨率，这意味着我们必须增加用于生成 PWM 信号的定时器的频率（定时器运行得越快，周期越小）。

通常，200 个分段是输出波形的良好近似。这意味着，如果我们想生成一个 50Hz 的正弦波，我们需要以 50Hz*200 = 10kHz 的频率运行定时器。脉冲周期将等于 200（步骤数 - 这意味着我们将输出电压变化 3.3V/200=0.016V），因此预分频器（Prescaler）值将为（假设 STM32F072 MCU 以 48MHz 运行）：

Prescaler = 48MHz 50Hz × 200divisions × 200Pulse = 24

以下示例展示了如何在以 48MHz 运行的 STM32F072MCU 上生成 50Hz 纯正弦波。

<!-- page: 350 -->

```text
Filename: Core/Src/main-ex9.c
14
#define PI
3.14159
15
#define ASR
1.8 //360 / 200 = 1.8
```

16

```text
17
int main(void) {
18
uint16_t IV[200];
19
float angle;
```

20

```text
21
HAL_Init();
```

22

```text
23
Nucleo_BSP_Init();
24
MX_TIM3_Init();
```

25

```text
26
for (uint8_t i = 0; i < 200; i++) {
27
angle = ASR*(float)i;
28
IV[i] = (uint16_t) rint(100 + 99*sinf(angle*(PI/180)));
29
}
```

30

```text
31
HAL_TIM_PWM_Start_DMA(&htim3, TIM_CHANNEL_1, (uint32_t *)IV, 200);
```

32

```text
33
while (1);
34
}
```

35

```text
36
/* TIM3 init function */
37
void MX_TIM3_Init(void) {
38
TIM_OC_InitTypeDef sConfigOC;
```

39

```text
40
htim3.Instance = TIM3;
41
htim3.Init.Prescaler = 23;
42
htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
43
htim3.Init.Period = 199;
44
htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV4;
45
HAL_TIM_PWM_Init(&htim3);
```

46

```text
47
sConfigOC.OCMode = TIM_OCMODE_PWM1;
48
sConfigOC.Pulse = 0;
49
sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
50
sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
51
HAL_TIM_PWM_ConfigChannel(&htim3, &sConfigOC, TIM_CHANNEL_1);
```

52

```text
53
hdma_tim3_ch1_trig.Instance = DMA1_Channel4;
54
hdma_tim3_ch1_trig.Init.Direction = DMA_MEMORY_TO_PERIPH;
55
hdma_tim3_ch1_trig.Init.PeriphInc = DMA_PINC_DISABLE;
56
hdma_tim3_ch1_trig.Init.MemInc = DMA_MINC_ENABLE;
57
hdma_tim3_ch1_trig.Init.PeriphDataAlignment = DMA_PDATAALIGN_HALFWORD;
58
hdma_tim3_ch1_trig.Init.MemDataAlignment = DMA_MDATAALIGN_HALFWORD;
59
hdma_tim3_ch1_trig.Init.Mode = DMA_CIRCULAR;
```

<!-- page: 351 -->

```text
60
hdma_tim3_ch1_trig.Init.Priority = DMA_PRIORITY_LOW;
61
HAL_DMA_Init(&hdma_tim3_ch1_trig);
```

62

```text
63
/* Several peripheral DMA handle pointers point to the same DMA handle.
64
Be aware that there is only one channel to perform all the requested DMAs. */
65
__HAL_LINKDMA(&htim3, hdma[TIM_DMA_ID_CC1], hdma_tim3_ch1_trig);
66
__HAL_LINKDMA(&htim3, hdma[TIM_DMA_ID_TRIGGER], hdma_tim3_ch1_trig);
67
}
```

最相关的部分由第 [26:29] 行表示。这些代码行用于生成初始化向量（Initialization Vector, IV），即包含用于生成正弦波的脉冲值（对应输出电压电平）的向量。C 语言中的 sinf() 返回给定角度（以弧度表示）的正弦值。因此，我们需要使用以下公式将以度表示的角度转换为弧度：

Radians = π 180° × Degrees

然而，在我们的情况下，我们将正弦波周期划分为 200 个步骤（即，我们将圆周划分为 200 个步骤），因此我们需要计算每个步骤的弧度值。但由于正弦函数在 180° 到 360° 之间的角度给出负值（见图 11.29），我们需要对其进行缩放，因为 PWM 输出值不能为负。

![Image from PDF page 351](../images/page-0351-image-01.jpeg)

图 11.29：正弦函数在 180° 到 360° 之间取的值

一旦生成了 IV 向量，我们就可以启动 DMA 模式下的 PWM。DMA1_Channel4 被配置为以循环模式工作，因此它会根据 IV 中包含的脉冲值自动设置 TIMx_CCRx 寄存器的值。使用 DMA 模式下的定时器是生成任意函数而不引入延迟并影响 Cortex-M 内核的最佳方式。然而，通常 IV 是硬编码在程序中的，使用自动存储在闪存中的 const 数组。你可以找到几个在线工具来完成此操作，例如这里提供的工具³⁶。

³⁶https://bit.ly/1QPfm4k

<!-- page: 352 -->

![Image from PDF page 352](../images/page-0352-image-01.jpeg)

图 11.30：定时器如何允许使用 PWM 近似 50Hz 正弦波

图 11.30 显示了 TIM3 通道 1 的输出：如你所见，使用适当的滤波级³⁷，很容易生成纯 50Hz 正弦波。

#### 11.3.7.2 使用 CubeMX 配置 PWM 模式

一旦掌握了 PWM 生成的基本概念，在 CubeMX 中配置 PWM 模式的过程就很直接了。第一步是为所需通道选择 PWM Generation CHx 模式，如图 11.20 所示。接下来，从 TIMx 配置视图（此处未显示）中，可以配置其他 PWM 设置（PWM 模式 1 或 2、通道极性，等等）。

### 11.3.8 单脉冲模式

单脉冲模式（One Pulse Mode, OPM）是通用定时器和高级定时器提供的输入捕获模式和输出比较模式的混合。它允许计数器在响应刺激信号时启动，并在可编程延迟后生成具有可编程持续时间（PWM）的脉冲。

OPM 是一种专门设计用于与定时器的通道 1 和通道 2 一起工作的模式。我们可以使用以下函数决定这两个通道中哪一个是输出，哪一个是输入：

```text
HAL_TIM_OnePulse_ConfigChannel(TIM_HandleTypeDef *htim, TIM_OnePulse_InitTypeDef* sConfig,
uint32_t OutputChannel,
uint32_t InputChannel);
```

两个通道都使用 C 结构体 TIM_OnePulse_InitTypeDef 的实例进行配置，其定义如下：

³⁷这里，我使用了一个 100ohm 电阻和一个 10µF 电容，它们给出了约 159Hz 的截止频率和等于 0.08V 的 Vpp。

<!-- page: 353 -->

```text
typedef struct {
uint32_t Pulse;
/* Specifies the pulse value to be loaded into the CCRx register.*/
/* Output channel configuration */
uint32_t OCMode;
/* Specifies the TIM mode. */
uint32_t OCPolarity;
/* Specifies the output polarity. */
uint32_t OCNPolarity;
/* Specifies the complementary output polarity. */
uint32_t OCIdleState;
/* Specifies the TIM Output Compare pin state during Idle state.*/
uint32_t OCNIdleState; /* Specifies the TIM Output Compare pin state during Idle state.*/
/* Input channel configuration */
uint32_t ICPolarity;
/* Specifies the active edge of the input signal. */
uint32_t ICSelection;
/* Specifies the input. */
uint32_t ICFilter;
/* Specifies the input capture filter. */
} TIM_OnePulse_InitTypeDef;
```

该结构体在逻辑上分为两部分：一部分与输入通道的配置相关，另一部分与输出相关。我们不会深入讨论结构体字段的细节，因为它们与我们之前讨论输入捕获和输出比较模式时所见到的类似。

需要理解的一个重要方面是定时器计算延迟和脉冲持续时间的方式。延迟根据以下公式计算：

Delay = Pulse ( T IMx_CLK

```text
Prescaler+1 )
[10]
```

而脉冲的持续时间（即占空比）用以下公式计算：

```text
Duration = Period - Pulse
```

( T IMx_CLK

```text
Prescaler+1 )
[11]
```

这意味着，一旦输入通道检测到触发事件，定时器就开始计数，当 CNT 寄存器达到 CCRx 寄存器（Pulse）时，它生成输出信号，该信号持续直到 CNT 寄存器达到 ARR 寄存器（Period），即 Period - Pulse。

OPM 可以设置为单次触发（single shoot）或重复模式。这是通过使用以下函数完成的：

```text
HAL_TIM_OnePulse_Init(TIM_HandleTypeDef *htim, uint32_t OnePulseMode);
```

该函数接受指向定时器句柄的指针以及符号常量 TIM_OPMODE_SINGLE 以将 OPM 配置为单次触发，或 TIM_OPMODE_REPETITIVE 以启用重复模式。

以下示例展示了如何在 STM32F072 MCU 中配置 TIM3 以 OPM 模式运行。

<!-- page: 354 -->

```text
Filename: Core/Src/main-ex10.c
12
int main(void) {
13
HAL_Init();
```

14

```text
15
Nucleo_BSP_Init();
16
MX_TIM3_Init();
```

17

```text
18
HAL_TIM_OnePulse_Start(&htim3, TIM_CHANNEL_1);
```

19

```text
20
while (1);
21
}
```

22

```text
23
/* TIM3 init function */
24
void MX_TIM3_Init(void) {
25
TIM_OnePulse_InitTypeDef sConfig;
```

26

```text
27
htim3.Instance = TIM3;
28
htim3.Init.Prescaler = 47;
29
htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
30
htim3.Init.Period = 65535;
31
HAL_TIM_OnePulse_Init(&htim3, TIM_OPMODE_SINGLE);
```

32

```text
33
/* Configure the Channel 1 */
34
sConfig.OCMode = TIM_OCMODE_PWM1;
35
sConfig.OCPolarity = TIM_OCPOLARITY_LOW;
36
sConfig.Pulse = 19999;
```

37

```text
38
/* Configure the Channel 2 */
39
sConfig.ICPolarity = TIM_ICPOLARITY_RISING;
40
sConfig.ICSelection = TIM_ICSELECTION_DIRECTTI;
41
sConfig.ICFilter = 0;
```

42

```text
43
HAL_TIM_OnePulse_ConfigChannel(&htim3, &sConfig, TIM_CHANNEL_1, TIM_CHANNEL_2);
44
}
```

## 第 [34:36] 行将输出通道配置为 PWM 模式 1，而第 [39:41] 行配置输入通道。第 43 行的 HAL_TIM_OnePulse_ConfigChannel() 配置这两个通道，将通道 1 设置为输出，通道 2 设置为输入。最后，HAL_TIM_OnePulse_Start()（在第 18 行调用）以 OPM 模式启动定时器。通过在 Nucleo-F072RB 上对 PA7 引脚施加偏置，定时器将在 20ms 的延迟后启动，并生成约 45ms 的 PWM，如图 11.31 所示。

<!-- page: 355 -->

![Image from PDF page 355](../images/page-0355-image-01.jpeg)

图 11.31：单脉冲模式如何工作

以单脉冲模式运行的定时器的输出通道甚至可以配置为 PWM 以外的其他模式。

#### 11.3.8.1 使用 CubeMX 配置 OPM 模式

若要使用 CubeMX 启用 OPM 模式，第一步是独立配置通道 1 和通道 2，然后选中“单脉冲模式”（One Pulse Mode）复选框，如图 11.32 所示。接下来，从 TIMx 配置视图（此处未显示）中，可以配置其他通道的设置。

![Image from PDF page 355](../images/page-0355-image-02.jpeg)

图 11.32：如何在定时器中启用单脉冲模式

### 11.3.9 编码器模式

旋转编码器具有广泛的应用范围。它们用于测量旋转物体的速度以及角位置。它们可用于测量电机的转速（RPM）和方向，控制伺服电机以及步进电机等。旋转编码器有几种类型：光学式、机械式和磁式。

增量式编码器是一种在检测到运动时提供周期性输出的旋转编码器类型。机械式类型需要去抖动，通常用作“数字电位器”。

<!-- page: 356 -->

大多数现代家用和车载音响使用机械式旋转编码器进行音量控制。由于成本低廉且能够提供易于解释以提供运动相关信息（如速度）的信号，增量式旋转编码器是所有旋转编码器中使用最广泛的。

![Image from PDF page 356](../images/page-0356-image-01.png)

图 11.33：正交编码器在 A 和 B 通道上发出的方波

它们使用两个称为 A 和 B 的输出，这些输出被称为正交输出，因为它们的相位相差 90 度，如图 11.33 所示。电机的方向取决于相位 A 是否领先于相位 B，或者相位 B 是否领先于相位 A。可选的第三个通道，即索引脉冲，每转发生一次，用作测量绝对位置的参考。检测旋转编码器方向和位置的方法有多种。通过将 A 和 B 引脚连接到两个 MCU 的 I/O，可以检测信号何时变为高电平（HIGH）和低电平（LOW）。这可以手动完成（使用中断来捕获通道状态变化的时刻），也可以使用定时器：其通道可以配置为输入捕获模式，并将捕获值进行比较以计算编码器的方向和速度。

STM32 通用定时器提供了一种读取旋转编码器的便捷方式：这种模式确实被称为编码器模式，它极大地简化了捕获过程。当定时器配置为编码器模式时，定时器计数器寄存器（TIMx_CNT）会在输入通道的边沿处递增/递减。

<!-- page: 357 -->

![Image from PDF page 357](../images/page-0357-image-01.png)

图 11.34：编码器模式下的定时器如何计算编码器速度和方向

有两种可用的捕获模式：X2 和 X4。在 X2 模式下，CNT 寄存器仅在其中一个通道（T1 或 T2）的每个边沿处递增/递减。在 X4 模式下，CNT 寄存器在两个通道的每个边沿处更新：这将捕获频率加倍。运动方向会自动推导出来，并通过 TIMx_DIR 寄存器提供给程序员，如图 11.34 所示。通过定期比较计数器寄存器的值，可以推导出 RPM 数，前提是已知编码器每转发出的脉冲数。

增量式机械编码器通常由于输出噪声需要去抖动。通常使用比较器作为这些设备的滤波级，特别是当它们用于接口电机和其他噪声设备时。在某些条件下，STM32 定时器的输入滤波级可用于过滤 A 和 B 通道，从而减少 BOM 组件的数量。

编码器模式仅在 TI1 和 TI2 通道上可用，并通过使用函数 HAL_TIM_Encoder_Init() 和 C 结构体 TIM_Encoder_InitTypeDef 的一个实例来激活，其定义如下。

<!-- page: 358 -->

```text
typedef struct {
/* T1 channel */
uint32_t EncoderMode;
/* Specifies the active edge of the input signal. */
uint32_t IC1Polarity;
/* Specifies the active edge of the input signal. */
uint32_t IC1Selection;
/* Specifies the input. */
uint32_t IC1Prescaler;
/* Specifies the Input capture prescaler. */
uint32_t IC1Filter;
/* Specifies the input capture filter. */
/* T2 channel */
uint32_t IC2Polarity;
/* Specifies the active edge of the input signal. */
uint32_t IC2Selection;
/* Specifies the input. */
uint32_t IC2Prescaler;
/* Specifies the Input capture prescaler. */
uint32_t IC2Filter;
/* Specifies the input capture filter. */
} TIM_Encoder_InitTypeDef;
```

我们在前面的段落中已经遇到了 TIM_Encoder_InitTypeDef 的大多数字段。唯一值得注意的是 EncoderMode，它可以取值 TIM_ENCODERMODE_TI1 或 TIM_ENCODERMODE_TI2 以在两个通道之一上设置 X2 编码器模式，以及取值 TIM_ENCODERMODE_TI12 以设置 X4 模式，从而使 TIMx_CNT 寄存器在 TI1 和 TI2 通道的每个边沿处更新。

以下示例旨在 Nucleo-F072RB 上运行，通过使用 TIM1 的输出比较模式来模拟增量式编码器。TIM1 的 OC1 和 OC2（PA8, PA9）通道通过 morpho 连接器路由到 TIM3 的 TI1 和 TI2 通道（PA6, PA7），并配置为生成两个具有相同周期但相位偏移的方波信号。然后 TIM3 被配置为编码器模式。SysTick 定时器用于生成时基：每 1 秒，计算脉冲数以及编码器方向。然后推导出 RPM 数，假设编码器每转生成 4 个脉冲。最后，通过按下 USER 按钮可以改变相位 A 和 B 之间的相位偏移：这将反转编码器的旋转方向。

```text
Filename: Core/Src/main-ex11.c
22
#define PULSES_PER_REVOLUTION 4
```

23

```text
24
int main(void) {
25
HAL_Init();
```

26

```text
27
Nucleo_BSP_Init();
28
MX_TIM1_Init();
29
MX_TIM3_Init();
```

30

```text
31
HAL_TIM_Encoder_Start(&htim3, TIM_CHANNEL_ALL);
32
HAL_TIM_OC_Start(&htim1, TIM_CHANNEL_1);
33
HAL_TIM_OC_Start(&htim1, TIM_CHANNEL_2);
```

34

```text
35
cnt1 = __HAL_TIM_GET_COUNTER(&htim3);
36
tick = HAL_GetTick();
```

<!-- page: 359 -->

37

```text
38
while (1) {
39
if (HAL_GetTick() - tick > 1000L) {
40
cnt2 = __HAL_TIM_GET_COUNTER(&htim3);
41
if (__HAL_TIM_IS_TIM_COUNTING_DOWN(&htim3)) {
42
if (cnt2 < cnt1) /* Check for counter underflow */
43
diff = cnt1 - cnt2;
44
else
45
diff = (65535 - cnt2) + cnt1;
46
} else {
47
if (cnt2 > cnt1) /* Check for counter overflow */
48
diff = cnt2 - cnt1;
49
else
50
diff = (65535 - cnt1) + cnt2;
51
}
```

52

```text
53
sprintf(msg, "Difference: %d\r\n", diff);
54
HAL_UART_Transmit(&huart2, (uint8_t*) msg, strlen(msg), HAL_MAX_DELAY);
```

55

```text
56
speed = ((diff / PULSES_PER_REVOLUTION) / 60);
```

57

```text
58
/* If the first three bits of SMCR register are set to 0x3
59
* then the timer is set in X4 mode (TIM_ENCODERMODE_TI12)
60
* and we need to divide the pulses counter by two, because
61
* they include the pulses for both the channels */
62
if ((TIM3->SMCR & 0x3) == 0x3)
63
speed /= 2;
```

64

```text
65
sprintf(msg, "Speed: %d RPM\r\n", speed);
66
HAL_UART_Transmit(&huart2, (uint8_t*) msg, strlen(msg), HAL_MAX_DELAY);
```

67

```text
68
dir = __HAL_TIM_IS_TIM_COUNTING_DOWN(&htim3);
69
sprintf(msg, "Direction: %d\r\n", dir);
70
HAL_UART_Transmit(&huart2, (uint8_t*) msg, strlen(msg), HAL_MAX_DELAY);
```

71

```text
72
tick = HAL_GetTick();
73
cnt1 = __HAL_TIM_GET_COUNTER(&htim3);
74
}
```

75

```text
76
if (HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_13) == GPIO_PIN_RESET) {
77
/* Invert rotation by swapping CH1 and CH2 CCR value */
78
tim1_ch1_pulse = __HAL_TIM_GET_COMPARE(&htim1, TIM_CHANNEL_1);
79
tim1_ch2_pulse = __HAL_TIM_GET_COMPARE(&htim1, TIM_CHANNEL_2);
```

80

```text
81
__HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_1, tim1_ch2_pulse);
82
__HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_2, tim1_ch1_pulse);
83
}
```

<!-- page: 360 -->

```text
84
}
85
}
```

86

```text
87
/* TIM1 初始化函数 */
88
void MX_TIM1_Init(void) {
89
TIM_OC_InitTypeDef sConfigOC;
```

90

```text
91
htim1.Instance = TIM1;
92
htim1.Init.Prescaler = 9;
93
htim1.Init.CounterMode = TIM_COUNTERMODE_UP;
94
htim1.Init.Period = 999;
95
HAL_TIM_Base_Init(&htim1);
```

96

```text
97
sConfigOC.OCMode = TIM_OCMODE_TOGGLE;
98
sConfigOC.Pulse = 499;
99
sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
100
sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
101
sConfigOC.OCIdleState = TIM_OCIDLESTATE_RESET;
102
sConfigOC.OCNPolarity = TIM_OCNPOLARITY_HIGH;
103
sConfigOC.OCNIdleState = TIM_OCNIDLESTATE_RESET;
104
HAL_TIM_OC_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_1);
105
106
sConfigOC.Pulse = 999; /* 相位 B 偏移 90° */
107
HAL_TIM_OC_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_2);
108
}
109
110
/* TIM3 初始化函数 */
111
void MX_TIM3_Init(void) {
112
TIM_Encoder_InitTypeDef sEncoderConfig;
113
114
htim3.Instance = TIM3;
115
htim3.Init.Prescaler = 0;
116
htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
117
htim3.Init.Period = 65535;
118
119
sEncoderConfig.EncoderMode = TIM_ENCODERMODE_TI12;
120
121
sEncoderConfig.IC1Polarity = TIM_ICPOLARITY_RISING;
122
sEncoderConfig.IC1Selection = TIM_ICSELECTION_DIRECTTI;
123
sEncoderConfig.IC1Prescaler = TIM_ICPSC_DIV1;
124
sEncoderConfig.IC1Filter = 0;
125
126
sEncoderConfig.IC2Polarity = TIM_ICPOLARITY_RISING;
127
sEncoderConfig.IC2Selection = TIM_ICSELECTION_DIRECTTI;
128
sEncoderConfig.IC2Prescaler = TIM_ICPSC_DIV1;
129
sEncoderConfig.IC2Filter = 0;
130
```

<!-- page: 361 -->

```text
131
HAL_TIM_Encoder_Init(&htim3, &sEncoderConfig);
132
}
```

函数 MX_TIM1_Init() 配置 TIM1 定时器，使其 OC1 和 OC2 通道工作在输出比较模式，每约 20μs 触发一次输出。通过设置两个不同的 Pulse 值（第 84 行和第 92 行），这两个输出在相位上相互偏移。MX_TIM3_Init() 函数将 TIM3 配置为编码器 X4 模式（TIM_ENCODERMODE_TI12）。

main() 函数的设计如下：SysTimer 被配置为每 1ms 生成一个滴答（tick），每当 SysTimer 计数达到 1000 个滴答时，将计数器寄存器（cnt2）的当前内容与保存的值（cnt1）进行比较：根据编码器方向（向上或向下）计算差值，并计算速度。代码还需要检测计数器可能发生的溢出/下溢，并相应地计算差值。另外请注意，由于我们每秒执行一次比较，必须配置 TIM1，使得通道 A 和 B 生成的脉冲总和每秒小于 65535。为此，我们将 TIM1 的 Prescaler 设置为 9 以减慢其速度。最后，当按下 Nucleo 用户按钮时，第 [76:83] 行会反转 A 和 B 之间的相位偏移（即 TIM1 定时器的 OC1 和 OC2 通道）。

#### 11.3.9.1 使用 CubeMX 配置编码器模式

若要使用 CubeMX 启用编码器模式，第一步是从 Combined Channels 组合框中启用此模式，如图 11.35 所示。接下来，在 TIMx 配置视图（此处未显示）中，可以配置其他通道的设置。

![Image from PDF page 361](../images/page-0361-image-01.jpeg)

图 11.35：如何在定时器中启用编码器模式

### 11.3.10 通用定时器和高级定时器中的其他功能

迄今为止介绍的功能代表了定时器最常见的用法。然而，STM32 的通用定时器和高级定时器还提供了其他重要功能，这些功能在某些特定的

<!-- page: 362 -->

应用领域中非常有用。我们现在将简要概述这些附加功能。由于这些功能共享前几段中其他应用示例中找到的共同概念，我们将不会深入探讨这些主题的详细信息（特别是因为如果没有专用硬件，很难安排示例）。

#### 11.3.10.1 霍尔传感器模式

在有刷直流电机中，电刷通过物理连接线圈来控制换向，并在正确的时刻进行连接。在无刷直流（BLDC）电机中，换向由电子电路控制，使用 PWM。电子电路可以具有位置传感器输入，提供关于何时进行换向的信息，或者使用线圈中产生的反电动势（BEF）。位置传感器最常用于启动扭矩变化很大或需要高初始扭矩的应用中。位置传感器也常用于电机用于定位的应用中。

霍尔效应传感器，或简称霍尔传感器，主要用于计算三相 BLDC 电机的位置（每个相位一个传感器）。STM32 通用定时器可以被编程为工作在霍尔传感器模式。通过将前三个输入设置为异或（XOR）模式，可以自动检测转子的位置。

这是通过使用高级控制定时器（TIM1）生成 PWM 信号来驱动电机，并使用另一个定时器（例如 TIM3）作为“接口定时器”来实现的。该接口定时器捕获通过异或门连接到 TI1 输入通道的三个定时器输入引脚（CC1、CC2、CC3）（参见图 11.16）。TIM3 处于从模式，配置为复位模式；从输入为 TI1F_ED³⁸。因此，每当三个输入之一切换时，计数器从 0 重新开始计数。这创建了一个由霍尔输入的任何变化触发的时间基准。

在“接口定时器”（TIM3）上，捕获/比较通道 1 被配置为捕获模式，捕获信号为 TRC（参见图 11.16 - TRC 以红色高亮显示）。捕获的值对应于输入之间两次变化之间的时间间隔，提供了关于电机速度的信息。“接口定时器”可以用作输出模式，生成一个脉冲，该脉冲改变高级控制定时器（TIM1）的通道配置（通过触发 COM 事件）。TIM1 定时器用于生成 PWM 信号以驱动电机。为此，接口定时器通道必须被编程，以便在编程延迟后生成一个正脉冲（在输出比较或 PWM 模式下）。该脉冲通过 TRGO 输出发送到高级定时器（TIM1）。

#### 11.3.10.2 三相 PWM 组合模式及其他电机控制相关功能

ST32F3 系列是专门用于高级电源转换和电机控制的系列。部分 STM32F3 微控制器，特别是 STM32F30x 和 STM32F3x8，能够使用单个可编程信号（该信号在脉冲中间进行 AND 操作）生成 1 到 3 个中心对齐的 PWM 信号。此外，它们还可以生成多达 3 个互补输出，并插入死区时间。这些

³⁸ED 是 Edge Detector（边沿检测器）的缩写，它是一种内部滤波定时器输入，当 XOR 的三个输入中仅有一个为 HIGH 时启用。

<!-- page: 363 -->

功能，加上之前提到的霍尔传感器模式，使得构建适用于电机控制的电子设备成为可能。有关此功能的更多信息，请参阅 ST 发布的 AN4013³⁹。

#### 11.3.10.3 刹车输入与定时器寄存器锁定

刹车输入（Break input）是电机控制应用中的紧急输入。刹车功能保护由高级定时器生成的 PWM 信号驱动的功率开关。刹车输入通常连接到功率级和三相逆变器的故障输出。当被激活时，刹车电路会关闭 TIM 输出，并将其强制置于预定义的安全状态。

此外，高级定时器通过编程 BDTR 寄存器中的 LOCK 位，为其寄存器提供渐进式保护。共有三个锁定级别可供选择，可选择性地锁定所有定时器寄存器。有关更多信息，请参阅您所用微控制器的参考手册。

#### 11.3.10.4 自动重载寄存器的预加载

我们在图 11.16 中遗留了一个未加注释的细节。ARR 寄存器在图形表示中带有阴影。这是因为它是预加载的，即对 ARR 寄存器的写入或读取操作访问的是预加载寄存器。预加载寄存器的内容会永久地，或者在每次 UEV 事件时（当且仅当 TIMx->CR1 寄存器中的自动重载预加载位（APRE）被使能时），传输到影子寄存器（即定时器内部实际包含待匹配计数值的寄存器）。如果是这种情况，可以通过设置 TIMx->EGR 寄存器中相应的位来生成 UEV 事件：这将导致预加载寄存器的内容传输到影子寄存器，并且定时器将采用新值。显然，如果您停止定时器，您可以自由更改 ARR 寄存器的内容。

这是一个需要澄清的重要方面。当定时器停止时，我们可以使用 TIM_Base_InitTypeDef.Period 结构体来配置 ARR 寄存器：Period 字段的内容由 HAL_TIM_Base_Init() 函数传输到 TIMx->ARR 寄存器。这将导致生成 UEV 事件，并且如果已使能，相应的 IRQ 将被触发。值得注意的是，即使定时器是外设复位后首次配置，这种情况也会发生。让我们考虑以下代码：

```text
htim6.Instance = TIM6;
htim6.Init.Prescaler = 47999; //48MHz/48000 = 1kHz
htim6.Init.Period = 4999;
//1kHz / 5000 = 5s
htim6.Init.CounterMode = TIM_COUNTERMODE_UP;
__HAL_RCC_TIM6_CLK_ENABLE();
HAL_NVIC_SetPriority(TIM6_IRQn, 0, 0);
HAL_NVIC_EnableIRQ(TIM6_IRQn);
HAL_TIM_Base_Init(&htim6);
HAL_TIM_Base_Start_IT(&htim6);
```

³⁹https://bit.ly/1WAewd6

<!-- page: 364 -->

上述代码配置 TIM6 定时器，使其在 5 秒后到期。然而，如果您将该代码重新排列到一个完整的示例中，您会发现 IRQ 在调用 HAL_TIM_Base_Start_IT() 函数后几乎立即触发。这是因为 HAL_TIM_Base_Init() 例程生成了一个 UEV 事件，以将 TIM6->ARR 寄存器的内容传输到内部影子寄存器。这导致 UIF 标志被置位，并且当 HAL_TIM_Base_Start_IT() 使能 IRQ 时，IRQ 被触发。

我们可以通过设置 TIMx->CR1 寄存器中的 URS 位来绕过此行为：这将导致 UEV 事件仅在计数器达到溢出/下溢时生成。

可以通过设置 TIMx->CR1 控制寄存器中的 TIM_CR1_ARPE 位来配置定时器，使 ARR 寄存器被缓冲。这将导致影子寄存器的内容自动更新。不幸的是，HAL 似乎没有提供明确的宏来执行此操作，我们需要在底层访问定时器寄存器：

```text
TIM3->CR1 |= TIM_CR1_ARPE;
//Enable preloading
TIM3->CR1 &= ~TIM_CR1_ARPE; //Disable preloading
```

预加载在使用输出比较模式且启用多个输出通道（每个通道具有自己的捕获值）的定时器时特别有用，此时我们必须确保对 CCRx 寄存器的任何更改同时发生。如果我们使用定时器进行电机控制或电源转换，这一点尤为重要。启用预加载功能可保证 CCRx 寄存器的新设置在定时器计数器的下一次溢出/下溢时生效。

### 11.3.11 调试与定时器

在调试会话期间，当执行因硬件或软件断点而暂停时，默认情况下定时器不会停止。有时，在调试期间停止定时器是有用的，特别是当定时器用于驱动外部设备时。

STM32 定时器可以选择性地配置为在内核因断点而暂停时停止。HAL 宏 `__HAL_DBGMCU_FREEZE_TIMx()`（其中 x 对应定时器编号）启用定时器的此工作模式。此外，具有互补输出的定时器的输出将被禁用并强制处于非活动状态。对于定时器控制电源开关或电动机的应用，此功能极其有用。它可以防止功率级因过流而损坏，或防止在命中断点时电动机处于不受控制的状态。

宏 `__HAL_DBGMCU_UNFREEZE_TIMx()` 恢复默认行为（即定时器在断点期间不停止）。

![Image from PDF page 364](../images/page-0364-image-01.png)

请注意，在调用 `__HAL_DBGMCU_FREEZE_TIMx()` 宏之前，必须通过调用 `__HAL_RCC_DBGMCU_CLK_- ENABLE()` 宏来启用 MCU 调试组件（DBGMCU）。

<!-- page: 365 -->

## 11.4 SysTick 定时器

SysTick 是 Cortex-M 内核内部的一个特殊定时器，由所有 STM32 微控制器提供。它主要用作 CubeHAL 和实时操作系统（real-time operating system，RTOS，如果使用）的时间基准生成器。关于 SysTick 定时器最重要的一点是，如果将其用作 HAL 的时间基准生成器，必须将其配置为每 1ms 生成一次异常：异常处理程序将递增系统滴答计数器（一个全局的、32 位宽且静态的变量），可以通过调用 `HAL_GetTick()` 例程来访问该计数器。

SysTick 是一个 24 位递减计数器，由 AHB 总线时钟驱动（即，它具有与高速时钟 - HCLK 相同的频率）。其时钟速度最终可以使用以下函数除以 8：

```text
void HAL_SYSTICK_CLKSourceConfig(uint32_t CLKSource);
which accepts the parameters SYSTICK_CLKSOURCE_HCLK and SYSTICK_CLKSOURCE_HCLK_DIV8.
```

SysTick 的更新频率由 SysTick 计数器的起始值决定，该值使用以下函数进行配置：

```text
uint32_t HAL_SYSTICK_Config(uint32_t TicksNumb);
```

要配置 SysTick 定时器使其每 1ms 生成一次更新事件，并假设它以与 AHB 总线相同的速度时钟驱动，只需以以下方式调用 `HAL_SYSTICK_Config()` 即可：

```text
HAL_SYSTICK_Config(HAL_RCC_GetHCLKFreq()/1000);
```

`HAL_SYSTICK_Config()` 例程还负责启用定时器及其 `SysTick_IRQn` 异常⁴⁰。异常的优先级可以在编译时通过设置 `include/stm32XXxx_hal_conf.h` 文件中的 `TICK_INT_- PRIORITY` 符号常量来配置，或者如第 7 章所示，通过调用 `HAL_- NVIC_SetPriority()` 来配置 `SysTick_IRQn` 异常的优先级。

当 SysTick 定时器达到零时，会引发 `SysTick_IRQn` 异常，并调用相应的处理程序。CubeMX 已经为我们提供了正确的函数体，其定义如下：

```text
void SysTick_Handler(void) {
HAL_IncTick();
HAL_SYSTICK_IRQHandler();
}
```

⁴⁰请记住，`SysTick_IRQn` 是一个异常而不是中断，尽管通常将其称为中断。这意味着我们不能使用 `HAL_NVIC_EnableIRQ()` 函数来启用它。

<!-- page: 366 -->

`HAL_IncTick()` 自动递增全局 SysTick 计数器，而 `HAL_SYSTICK_- IRQHandler()` 仅包含对 `HAL_SYSTICK_Callback()` 例程的调用，这是一个可选实现的回调，用于在定时器下溢时通知我们。

### 仔细阅读

![Image from PDF page 366](../images/page-0366-image-01.png)

避免在 `HAL_SYSTICK_Callback()` 例程中使用缓慢的代码，否则可能会影响时间基准生成。这可能导致依赖精确 1ms 时间基准生成的一些 HAL 模块出现不可预测的行为。

此外，使用 `HAL_Delay()` 时必须小心。该函数基于 SysTick 计数器提供精确的延迟（以毫秒为单位）。这意味着如果从外设 ISR 进程中调用 `HAL_Delay()`，则 SysTick 中断必须具有比外设中断更高的优先级（数值更低）。否则，调用者 ISR 进程将被阻塞（因为全局滴答计数器永远不会递增）。

要暂停系统时间基准生成，可以使用 `HAL_SuspendTick()` 例程，而要恢复它则使用 `HAL_ResumeTick()`。

### 11.4.1 使用另一个定时器作为系统时间基准源

SysTick 定时器只有一个主要应用：作为 HAL 或可选 RTOS 的时间基准生成器。由于 SysTick 时钟无法轻松预分频到更灵活的计数频率，因此不适合用作常规定时器。然而，它有一个重要的限制，我们将在第 23 章中更好地分析：它不适合用于某些 RTOS 为低功耗应用提供的无滴答（tickless）模式。因此，有时使用另一个定时器（可能是 LPTIM）作为系统时间基准生成器很重要。最后，正如我们将在第 23 章中发现的那样，当使用 RTOS 时，将 HAL 和 RTOS 的时间基准源分开是方便的。

CubeMX 允许轻松使用另一个定时器代替 SysTick。要执行此操作，请进入引脚布局（Pinout）视图，然后从类别窗格中打开 RCC 条目并选择时间基准源，如图 11.36 所示。

<!-- page: 367 -->

![Image from PDF page 367](../images/page-0367-image-01.jpeg)

图 11.36：如何选择另一个定时器作为系统时间基准源

CubeMX 将生成一个名为 `stm32XXxx_hal_timebase_TIM.c` 的附加文件，其中包含 `HAL_InitTick()`（包含初始化定时器所需的所有代码，使其每 1ms 溢出一次）、`HAL_SuspendTick()` 和 `HAL_ResumeTick()` 的定义，以及 `HAL_TIM_PeriodElapsedCallback()` 的定义，其中包含对 `HAL_IncTick()` 例程的调用。这种对 HAL 例程的“覆盖”之所以可能，是因为这些函数在 HAL 源文件中被定义为 `__weak`。

## 11.5 案例研究：如何使用 STM32 微控制器精确测量微秒

有时，特别是在处理未由外设硬件实现的通信协议时，我们需要精确测量从 1 微秒到几微秒不等的延迟。这引出了另一个更普遍的问题：如何在 STM32 微控制器中精确测量微秒？

实现这一目标有几种方法，但有些方法在不同微控制器和时钟配置之间更准确，而另一些方法则更具通用性。

让我们考虑 STM32F4 系列的一个成员：STM32F401RE。这款微控制器在使用内部 RC 时钟时，最高运行频率可达 84MHz。这意味着每 1µs，时钟会循环 84 次。因此，我们需要一种方法来计数 84 个时钟周期，以确认 1µs 已经流逝（我假设您可以容忍内部 RC 时钟 1% 的精度误差）。

有时，我们会发现类似以下的延迟例程：

<!-- page: 368 -->

```text
void delay1US() {
#define CLOCK_CYCLES_PER_INSTRUCTION
X
#define CLOCK_FREQ
Y
//IN MHZ (e.g., 16 for 16 MHZ)
volatile int cycleCount = CLOCK_FREQ / CLOCK_CYCLE_PER_INSTRUCTION;
while (cycleCount--);
}
```

但是，如何确定计算 `while(cycleCount--)` 指令的一个步骤需要多少个时钟周期呢？不幸的是，给出答案并不简单。让我们假设 `cycleCount` 等于 1。通过一些测试（我稍后会解释我是如何进行的），在禁用编译器优化（GCC 的 -O0 选项）的情况下，我们可以看到在这种情况下，整个 C 指令需要 24 个周期来执行。这是如何可能的呢？您必须明白，我们的 C 语句被展开为几条汇编指令，如果我们反汇编固件二进制文件，就可以看到这一点：

```text
...
while(counter--);
800183e:
f89d 3003
ldrb.w
r3, [sp, #3]
8001842:
b2db
uxtb
r3, r3
8001844:
1e5a
subs
r2, r3, #1
8001846:
b2d2
uxtb
r2, r2
8001848:
f88d 2003
strb.w
r2, [sp, #3]
800184c:
2b00
cmp
r3, #0
800184e:
d1f6
bne.n
800183e <delay1US+0x3e>
```

此外，另一个延迟来源与从内部 MCU 闪存中获取指令有关（这与“低成本”STM32 微控制器和更强大的微控制器（如带有 ART 加速器的 STM32F4 和 STM32F7，该加速器旨在将闪存访问延迟降至零）有很大不同）。因此，该指令具有 24 个周期的“基本成本”。如果 `cycleCount` 等于 2，需要多少个周期？在这种情况下，MCU 需要 33 个周期，即额外增加 9 个周期。这意味着，如果我们想要自旋 84 个周期，`cycleCount` 必须等于 (84-24)/9，约为 7。因此，我们可以以更通用的方式编写延迟函数：

```text
void delayUS(uint32_t us) {
volatile uint32_t counter = 7*us;
while(counter--);
}
```

使用以下代码测试此函数：

<!-- page: 369 -->

```text
while(1) {
delayUS(1);
GPIOA->ODR = 0x0;
delayUS(1);
GPIOA->ODR = 0x20;
}
```

我们可以使用连接到 PA5 引脚的示波器来检查，确认我们获得了所需的延迟：

![Image from PDF page 369](../images/page-0369-image-01.jpeg)

这种延迟 1µs 的方法是否一致？不幸的是，答案是否定的。首先，它仅在此特定微控制器（STM32F401RE）以全速（84MHz）运行时才有效。如果我们决定使用不同的时钟速度，我们需要通过测试重新调整它。其次，它受编译器优化的影响（我们很快就会看到），以及某些 STM32 微控制器中 D-Bus 和 I-Bus 上的 CPU 内部缓存（这些缓存最终可以通过在 include/stm32XXxx_hal_conf.h 文件中设置 PREFETCH_ENABLE, INSTRUCTION_CACHE_ENABLE, DATA_CACHE_ENABLE 来禁用）。

让我们为“大小”启用 GCC 优化（-Os）。我们得到什么结果？在这种情况下，`delayUS()` 函数仅花费 72 个 CPU 周期，即约 850ns。示波器证实了这一点：

![Image from PDF page 369](../images/page-0369-image-02.jpeg)

如果我们启用最大速度优化（-O3）会发生什么？在这种情况下，我们只有 64 个 CPU 周期，即我们的 `delayUS()` 仅持续约 750ns。然而，这个问题可以使用特定的 GCC pragma 指令来解决：

<!-- page: 370 -->

```text
#pragma GCC push_options
#pragma GCC optimize ("O0")
void delayUS(uint32_t us) {
volatile uint32_t counter = 7*us;
while(counter--);
}
#pragma GCC pop_options
```

然而，如果我们想要使用较低的 CPU 频率，或者想要将代码移植到不同的 STM32 微控制器，我们仍然需要重新进行测试，并经验性地推导出周期数。

![Image from PDF page 370](../images/page-0370-image-01.png)

但是，请记住，CPU 频率越低，精确延迟 1µs 就越困难，因为给定指令的周期数是固定的，但在相同的时间单位内可用的周期数更少。

那么，如果我们更改硬件设置，如何在不进行测试的情况下获得精确的 1µs 延迟？

一种可能的答案是通过设置一个每 1µs 溢出一次的定时器（只需将其 Period 设置为外设总线速度（以 MHz 为单位）——例如，对于 STM32F401RE，我们需要将 Period 设置为 (84 - 1)），并且我们可以递增一个全局变量来跟踪已流逝的微秒数。这与 SysTick 定时器用于生成 HAL 时间基准的方式相同。

然而，这种方法不切实际，特别是对于低速 STM32 微控制器。每 1µs 生成一次中断（对于以全速运行的 STM32F0 微控制器，这意味着每 48 个 CPU 周期一次）会使 MCU 拥塞，降低整体的多任务处理程度。此外，中断管理具有不可忽略的成本（从 12 到 16 个周期），这将影响 1µs 时间基准的生成。同样，轮询定时器以获取其计数器的值也不切实际：大量时间将花费在检查计数器与起始值的比较上，并且定时器溢出/下溢的处理将影响时间基准的生成。

一种更稳健的解决方案来自之前的测试。我是如何测量 CPU 周期的？Cortex-M3/4/7 处理器可以有一个可选的调试单元，称为数据观察点和跟踪（DWT），它为处理器提供观察点、数据跟踪和系统分析。该单元的一个寄存器是 CYCCNT，它计算 CPU 执行的周期数。因此，我们可以使用这个特殊单元来计数 MCU 在执行指令期间执行的周期数。

<!-- page: 371 -->

```text
uint32_t cycles = 0;
/* DWT struct is defined inside the core_cm4.h file */
DWT->CTRL |= 1 ; // enable the counter
DWT->CYCCNT = 0; // reset the counter
delayUS(1);
cycles = DWT->CYCCNT;
cycles--; /* We subtract the cycle used to transfer
CYCCNT content to cycles variable */
```

## 使用 DWT，我们可以以这种方式构建一个更通用的 delayUS() 例程：

```text
#pragma GCC push_options
#pragma GCC optimize ("O3")
void delayUS_DWT(uint32_t us) {
volatile uint32_t cycles = (SystemCoreClock/1000000L)*us;
volatile uint32_t start = DWT->CYCCNT;
do
{
} while(DWT->CYCCNT - start < cycles);
}
#pragma GCC pop_options
```

## 这个函数的精度如何？如果你对 1µs 的最佳分辨率感兴趣，这个函数帮不了你，示波器显示如下。

![Image from PDF page 371](../images/page-0371-image-01.jpeg)

## 当设置较高的编译器优化级别时，可获得最佳性能。如图所示，对于期望的 1µs 延迟，该函数给出的延迟约为 1.22µs（慢了 22%）。然而，如果我们需要自旋 10µs，我们获得的实际延迟为 10.5µs（慢了 5%），这更接近我们的期望。

<!-- page: 372 -->

![Image from PDF page 372](../images/page-0372-image-01.jpeg)

从 100µs 的延迟开始，误差完全可以忽略不计。

为什么这个函数不够精确？要理解为什么这个函数比另一个函数精度低，你必须明白我们使用了一系列指令来检查自函数启动以来已经过去了多少个周期（即 while 条件）。这些指令消耗 CPU 周期，既用于用 CYCCNT 寄存器的内容更新内部 CPU 寄存器，也用于执行比较和分支。然而，这个函数的优势在于它自动检测 CPU 速度，并且开箱即用，特别是在处理速度更快的处理器上时。

如果你想要完全控制编译器优化，可以使用以下完全用汇编编写的宏来达到最佳的 1µs 延迟：

```text
#define delayUS_ASM(us) do {
\
asm volatile ("MOV R0,%[loops]\n
\
1: \n
\
SUB R0, #1\n
\
CMP R0, #0\n
\
BNE 1b \t"
\
: : [loops] "r" (16*us) : "memory" \
);
\
} while(0)
```

这是编写 while(counter--) 函数最优化的一种方式。通过示波器测试，我发现当微控制器在 84MHZ 下执行此循环 16 次时，可以获得 1µs 的延迟。然而，如果你的处理器速度较低，必须重新调整此宏，并且请记住，由于它是一个宏，每次使用它时都会“展开”，从而导致固件尺寸增加。
