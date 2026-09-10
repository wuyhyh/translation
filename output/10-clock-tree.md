<!-- page: 275 -->

# 10. 时钟树

几乎每个数字电路都需要一种方式来同步其内部电路，或者与其他电路进行同步。时钟是一种产生周期性信号的设备，它是数字电子领域中最普遍的心跳源形式。

然而，同一个时钟信号不能用于为像 STM32 这样的现代微控制器提供的所有组件和外设供电。此外，功耗是一个与特定外设时钟速度直接相关的关键方面。能够选择性地禁用某些 MCU 部分或降低其时钟速度，有助于优化整个设备的功耗。这要求时钟以层次结构组织，使开发人员能够选择不同的速度和时钟源。

本章简要介绍了 STM32 MCU 复杂的时钟分配网络。其目的是为读者提供必要的工具来理解和管理时钟树，并展示 HAL_RCC 模块的主要功能。本章的内容将在专门讨论电源管理的第 19 章中进一步补充。

## 10.1 时钟分配

时钟通常产生占空比为 50% 的方波信号，如图 10.1¹ 所示。

![Image from PDF page 275](../images/page-0275-image-01.png)

图 10.1：占空比为 50% 的典型时钟信号

时钟信号在 VL 和 VH 电压电平之间振荡，对于 STM32 微控制器而言，这两个电平是 VDD 供电电压的一部分。时钟最基本的参数是频率，它表示每秒从 VL 切换到 VH 的次数。频率以赫兹（Hertz）为单位表示。

¹ 重要的是要指出，图 10.1 中代表的方波是“理想”的。时钟源的实际方波具有梯形形式。

<!-- page: 276 -->

大多数 STM32 MCU² 可以交替使用两种不同的时钟源进行时钟驱动：内部 RC 振荡器³（称为高速内部时钟，High Speed Internal，HSI）或外部专用晶振⁴（称为高速外部时钟，High Speed External，HSE）。选择外部晶振而非内部 RC 振荡器有几个原因：

- 与内部 RC 网络相比，外部晶振提供了更高的精度，内部 RC 网络的精度额定为 1%⁵，尤其是在 PCB 工作温度远离 25°C 环境温度时。
- 某些外设，特别是高速外设，只能由以特定频率运行的专用外部晶振驱动。

除了高速振荡器⁶ 外，还可以使用另一个时钟源来偏置低速振荡器，后者可以由外部晶振（称为低速外部时钟，Low Speed External，LSE）或内部专用 RC 振荡器（称为低速内部时钟，Low Speed Internal，LSI）驱动。低速振荡器用于驱动实时时钟（Real Time Clock，RTC）和独立看门狗（Independent Watchdog，IWDT）外设。

高速振荡器的频率并不决定 Cortex-M 内核或其他外设的实际频率。一个复杂的分配网络，也称为时钟树，负责在 STM32 MCU 内部传播时钟信号。通过使用多个可编程锁相环（Phase-Locked Loops，PLL）和预分频器，可以根据需要增加/降低源频率（见图 10.2），具体取决于我们要达到的性能、特定外设或总线的最大速度以及整体全局功耗⁷。

![Image from PDF page 276](../images/page-0276-image-01.png)

图 10.2：如何使用 PLL 和预分频器增加/降低源时钟信号频率

### 10.1.1 STM32 时钟树概览

STM32 MCU 的时钟树可能具有非常复杂的结构。即使在“较简单”的 STM32F0 MCU 中，内部时钟网络也可以拥有多达四个 PLL/预分频级，并且系统时钟多路复用器（也称为系统时钟切换，System Clock Switch，SW）可以由多个备用源供电。

² 存在一些 STM32 MCU，特别是那些引脚数较少的型号，无法由外部时钟源驱动。 ³ https://bit.ly/1TkDnUd ⁴ https://bit.ly/20ymjJx ⁵ 1% 的精度可能看起来是一个不错的折衷方案，特别是考虑到你可以节省 PCB 空间以及专用晶振的成本，而晶振是一种价格不可忽略的设备。然而，对于时间约束应用，1% 可能是一个巨大的偏差。例如，一天由 86,400 秒组成。1% 的误差意味着在最坏情况下，我们可能会损失（或获得）多达 864 秒，这等于 14.4 分钟！如果温度升高，情况可能会变得更糟。这就是为什么如果你打算使用 RTC，必须使用外部低速晶振的原因。然而，存在一种提高此精度的解决方案。稍后会有更多介绍。 ⁶ 在本书中，我们将把高速振荡器称为“抽象”时钟源，它有两个互斥的“具体”源：HSE 或 HSI 振荡器。同样的规则也适用于低速振荡器 ⁷ 请记住，MCU 的功耗与其频率大致呈线性关系。频率越高，消耗的功率越大。

<!-- page: 277 -->

![Image from PDF page 277](../images/page-0277-image-01.png)

表 10.1：本书中用作测试板的 Nucleo 板所搭载 MCU 的 AHB、APB1 和 APB2 总线的最大时钟速度

此外，深入解释每个 STM32 系列的时钟树是一项复杂的任务，这也要求我们将注意力集中在特定的部件号上。这是因为时钟树结构主要受以下关键方面影响：

- 微控制器的 STM32 主系列。例如，所有 STM32F0 MCU 仅提供一个外设总线（APB1），其时钟频率可以达到 Cortex-M 内核的最大频率。其他 STM32 微控制器通常提供两个外设总线，其中只有一个（APB2）可以达到最大 CPU 时钟速度。相反，STM32F7 微控制器中可用的任何外设总线都无法达到最大内核频率⁸，而 STM32G4 MCU 中的 APB1 和 APB2 都可以达到最大内核时钟速度。表 10.1 报告了本书中用作测试板的 Nucleo 板所搭载 MCU 的 AHB、APB1 和 APB2 总线（及相关定时器时钟速度）的最大时钟速度：你可以注意到，对于“旧款” STM32F103，仅使用外部 HSE 振荡器就可以达到最大时钟速度。
- MCU 提供的外设类型和数量。时钟树的复杂性随着可用外设数量的增加而增加。此外，某些外设需要专用的时钟源和速度，这会影响 PLL 级的数量。
- MCU 的销售类型和封装，这决定了所提供外设的有效类型和数量。

即使我们将焦点仅限于搭载在 Nucleo 板上的九个 MCU，这也需要漫长且繁琐的工作，涉及对给定 MCU 实现的所有外设的深入了解。基于这些原因，我们将对 STM32 时钟树进行快速概览，并留给读者责任去深入考虑他们特定的 MCU。此外，正如我们稍后所见，得益于 CubeMX，我们可以从特定的时钟树实现中抽象出来，

⁸ 除了 APB2 总线上的定时器。

<!-- page: 278 -->

除非我们需要处理特定的 PLL 配置以满足性能和电源管理的原因。

![Image from PDF page 278](../images/page-0278-image-01.jpeg)

图 10.3：STM32F030R8 MCU 的时钟树

图 10.3 展示了最简单的 STM32 微控制器之一：STM32F030R8 的时钟树。该图提取自 ST 提供的相关参考手册⁹。对于许多 STM32 平台的新手来说，这张图完全令人费解且难以解读，尤其是当他们也是嵌入式微控制器的新手时。图中用红色标出了最相关的路径：从 HSI 振荡器到 Cortex-M0 内核、AHB 总线和 DMA 的路径。这是我们在此处“使用”的路径，我们一直默默地使用它，而没有过多地处理其可能的配置。让我们介绍

⁹https://bit.ly/1GfS3iC

<!-- page: 279 -->

该路径中最相关的部分。

该路径从内部 8MHz 振荡器开始。如前所述，这是一个由 ST 工厂校准的 RC 振荡器，在 25 °C 环境温度下精度为 1%。HSI 时钟可以直接用于馈送系统时钟切换器（SW）（图 10.3 中用蓝色高亮显示的路径），或者在经过中间预分频器¹⁰将其除以二后，用于馈送 PLL 倍频器。因此，主 PLL 可以将 4MHz 时钟最多乘以 12 倍，以获得 48MHz 的最大系统时钟频率（SYSCLK）。SYSCLK 源可用于馈送 I2C1 外设（作为 HSI 的替代方案）以及另一个中间预分频器，即 AHB 预分频器，后者可用于降低高速时钟（HCLK），而 HCLK 又偏置 AHB 总线、内核和 SysTimer。

### 为什么需要这么多中间 PLL/预分频器级？

![Image from PDF page 279](../images/page-0279-image-01.png)

如前所述，时钟速度决定了整体性能，但也影响 MCU 的总功耗。能够选择性地开启/关闭或降低 MCU 某些部分的时钟速度，使得可以根据实际所需的计算能力来降低功耗。正如我们将在第 19 章中看到的，L0/1/4/5 MCU 引入了更多的 PLL/预分频器级，以让开发人员对 MCU 的整体功耗拥有更多的控制权。结合专门的硬件设计，这使得创建由电池供电的设备成为可能，这些设备可以使用同一块电池运行数年。

时钟树配置是通过一个名为复位和时钟控制（RCC）的专用外设¹¹进行的，该过程本质上由三个步骤组成：

1. 选择高速振荡器源（HSI 或 HSE），如果使用 HSE，则对其进行适当配置。¹² 2. 如果我们希望以高于高速振荡器提供的频率馈送 SYSCLK，则需要配置主 PLL（提供 PLLCLK 信号）。否则，我们可以跳过此步骤。 3. 配置系统时钟切换器（SW），选择正确的时钟源（HSI、HSE 或 PLLCLK）。然后，我们选择正确的 AHB、APB1 和 APB2（如果可用）预分频器设置，以达到高速时钟（HCLK - 即馈送内核、DMA 和 AHB 总线的时钟）所需的频率，以及高级外设总线 1（APB1）和 APB2（如果可用）总线的频率。

了解 PLL 和预分频器的允许值可能是一场噩梦，尤其是对于更复杂的 STM32 MCU。对于给定的 STM32 微控制器，只有一些组合是有效的，不当的配置可能会损坏 MCU 或至少导致故障

¹⁰预分频器是一种用于降低高频的“电子计数器”。在这种情况下，“/2”预分频器将主 8MHz 频率降低到 4MHz。 ¹¹有时，ST 在其文档中将 RCC 定义为“外设”。有时则不。我不确定它是否真正是一个外设，但我会像 ST 那样定义它。有时。 ¹²在 STM32L0/1/4 MCU 中，SYSCLK 也可以由另一个专用的低功耗时钟源馈送，该源名为 MSI。我们将讨论这个时钟源。

<!-- page: 280 -->

（错误的时钟配置可能导致异常行为、奇怪且不可预测的重置等）。幸运的是，STM32 工程师提供了一个简化工具来简化时钟配置：CubeMX。

#### 10.1.1.1 STM32L/U 系列中的多速度内部 RC 振荡器

时钟源及其分配网络对 MCU 的整体功耗有不可忽略的影响。如果我们需要的 SYSCLK 频率高于或低于内部 HSI 时钟源（对于大多数 STM32 MCU 为 8MHz，对于某些其他型号为 16MHz），我们必须使用 PLL 源复用器和中间预分频器来增加/减少它。不幸的是，这些组件消耗能量，这对电池供电设备可能产生巨大影响。

![Image from PDF page 280](../images/page-0280-image-01.png)

表 10.2：STM32L476 MCU 中时钟源的比较

STM32L/U MCU 明确针对低功耗应用设计，并通过提供一个专用的内部时钟源来解决这一特定问题，该源名为多速度内部（MSI）RC 振荡器。MSI 是一个低功耗 RC 振荡器，具有 ±1%@25°C 的工厂预校准精度，在 0-85°C 范围内可能增加到 ±3%。MSI 的主要特点是它提供多达十二种不同的频率，而无需添加任何外部组件。例如，STM32L476 中的 MSI 提供从 100kHz 到 48MHz 的内部时钟源。MSI 时钟在从复位重启、从待机模式和关机低功耗模式唤醒后用作 SYSCLK。从复位重启后，MSI 频率设置为其默认值（例如，STM32L476 中的默认 MSI 频率为 4MHz）。表 10.2 总结了 STM32L476 MCU 中所有可能时钟源的最相关特性。如您所见，当 MCU 由 MSI 时钟驱动时（不使用 PLL 复用器），可实现最佳的功耗。此外，与 HSI 相比，该时钟源保证了最短的启动时间。有趣的是，稳定 LSE 时钟最多需要两秒钟：如果启动速度对您的应用确实很重要，那么使用一个单独的线程¹³来启动 LSE 是一个值得考虑的选项。

¹³这显然意味着使用 RTOS。我们将在后面的章节中研究这个问题。

<!-- page: 281 -->

除了与低功耗相关的优势外，当 MSI 用作 PLL 源复用器的源时，它提供了一个非常精确的时钟源，该源可用于 USB OTG FS 设备，而无需使用外部专用晶振，同时馈送主 PLL 以让系统以最大速度运行。

### 10.1.2 使用 CubeMX 配置时钟树

我们在第 4 章中已经接触过 CubeMX 的时钟配置视图。现在是时候看看它是如何工作的了。图 10.4 展示了前文所见的同一款 F0 微控制器的时钟树。正如你所见，得益于屏幕上可用的空间更大，分配网络看起来不那么繁琐了。

![Image from PDF page 281](../images/page-0281-image-01.jpeg)

图 10.4：STM32F030R8 微控制器的时钟树在 CubeMX 中的表示方式

在这种情况下，时钟树中最关键的路径也用红色和蓝色高亮显示。这应该能简化与图 10.3 的对比。当创建新项目时，默认情况下 CubeMX 选择 HSI 振荡器作为默认时钟源。如图 10.4 所示，HSI 也被选为系统时钟多路复用器¹⁴（蓝色路径）的默认时钟源。这意味着，对于我们要考虑的这款微控制器，Cortex-M 内核频率将等于 8MHz。

¹⁴系统时钟多路复用器即图 10.3 中看到的系统时钟切换器（SW）

<!-- page: 282 -->

CubeMX 还向我们提示了两件事：在此微控制器中，高速时钟（HCLK）和 APB1 总线的最大频率等于 48MHz（蓝色标签）。要提高 CPU 内核频率，我们首先需要选择 PLLCLK 作为系统时钟切换器的源时钟，然后选择合适的 PLL 倍频系数。然而，CubeMX 提供了一种快速完成此操作的方法：你只需在 HCLK 字段中输入“48”并按下回车键。CubeMX 将自动调整设置，选择正确的时钟树路径（图 10.4 中的红色路径）。

如果你的开发板依赖外部 HSE/LSE 晶振，你必须在 RCC 外设中启用它，然后才能将其用作相应振荡器的主要时钟源（我们稍后将会逐步介绍如何执行此步骤）。一旦外部振荡器被启用，就可以指定其频率（在标有“输入频率”的蓝色框内），并配置主 PLL 以实现所需的 SYSCLK 速度（参见图 10.5）。否则，外部振荡器的输入频率可以直接用作系统时钟切换器的源时钟。

![Image from PDF page 282](../images/page-0282-image-01.jpeg)

图 10.5：使用 RCC 外设启用 HSE 振荡器后，CubeMX 允许选择该振荡器

我们需要相应地配置 RCC 外设以启用外部时钟源。这可以通过 CubeMX 中的引脚布局视图完成，如图 10.6 所示。

![Image from PDF page 282](../images/page-0282-image-02.png)

图 10.6：RCC 外设提供的配置选项

对于 HSE 和 LSE 振荡器，CubeMX 提供三种配置选项：

- Disable（禁用）：外部振荡器不可用/未使用，并使用相应的内部振荡器。
- Crystal/Ceramic Resonator（晶振/陶瓷谐振器）：使用外部晶振/陶瓷谐振器，并从中导出相应的主频率。这意味着使用 RCC_OSC_IN 和 RCC_OSC_OUT 引脚来连接 HSE，并且相应的信号 I/O 不可用于其他用途（如果我们使用的是外部低速晶振，则也使用相应的 RCC_OSC32_IN 和 RCC_OSC32_OUT I/O）。

<!-- page: 283 -->

- BYPASS Clock Source（旁路时钟源）：使用外部时钟源。该时钟源由另一个活动设备生成。这意味着 RCC_OSC_OUT 保持未使用状态，并且可以将其用作常规 GPIO。在几乎所有来自 ST 的开发板（包括 Nucleo 系列）中，ST-LINK 接口的 Master Clock Output (MCO) 引脚被用作目标 STM32 微控制器的外部时钟源。启用此选项允许将 ST-LINK MCO 用作 HSE。

RCC 外设还允许启用 Master Clock Output (MCO)，这是一个可用于为另一个外部设备提供时钟的引脚，从而为该其他 IC 节省外部晶振。一旦启用 MCO，就可以使用时钟配置视图选择其时钟源，如图 10.7 所示。

![Image from PDF page 283](../images/page-0283-image-01.jpeg)

图 10.7：如何为 MCO 引脚选择时钟源

### 10.1.3 Nucleo 开发板中的时钟源选项

Nucleo-64 开发板为时钟源提供了多种替代方案。然而，早期的 Nucleo-64 开发板与基于不同板级布局和较新的 ST-LINK v3 调试器的较新开发板之间存在显著区别。

要了解你拥有的是哪个版本的 Nucleo-64，检查开发板版本号很重要。早期版本基于 MB1136 设计。较新的版本基于 MB1367 设计。此信息通常报告在 PCB 上（在较旧的 Nucleo 上使用背面的标签），如图 10.8 所示。

![Image from PDF page 283](../images/page-0283-image-02.jpeg)

图 10.8：Nucleo-64 PCB 版本号

<!-- page: 284 -->

#### 10.1.3.1 Nucleo-64 rev. MB1136（旧版，配备 ST-LINK V2.1）的时钟源

##### 10.1.3.1.1 OSC 时钟供电

配置对应外部高速时钟 external highspeed clock (HSE) 的引脚有四种方式：

- 来自 ST-LINK 的 MCO：使用 ST-LINK 微控制器的 MCO 输出作为输入时钟。该频率不可更改，固定为 8 MHz，并连接到目标 STM32 微控制器的 PF0/PD0/PH0-OSC_IN。需要以下配置：

- – SB55 OFF – SB16 和 SB50 ON – 移除 R35 和 R37
- 板载 HSE 振荡器，来自 X3 晶振（未提供）：关于典型频率及其电容和电阻，请参阅 STM32 微控制器数据手册。关于 STM32 微控制器的振荡器设计指南，请参阅 AN2867。需要以下配置：

- – SB54 和 SB55 OFF – 焊接 R35 和 R37 – 焊接 C33 和 C34 – SB16 和 SB50 OFF
- 来自外部 PF0/PD0/PH0 的振荡器：通过 CN7 连接器的第 29 引脚从外部振荡器引入。需要以下配置：

- – SB55 ON – SB50 OFF – 移除 R35 和 R37
- 未使用 HSE：PF0/PD0/PH1 和 PF1/PD1/PH1 用作 GPIO，而非时钟。需要以下配置：

– SB54 和 SB55 ON – SB16 和 SB50 (MCO) OFF – 移除 R35 和 R37

根据 NUCLEO 板硬件版本的不同，HSE 引脚有两种可能的默认配置。PCB 底部贴纸上标有板版本 MB1136 C-01/02/03。

- 板标记 MB1136 C-01 对应配置为未使用 HSE 的板。
- 板标记 MB1136 C-02（或更高版本）对应配置为使用 STLINK MCO 作为时钟输入的板。

<!-- page: 285 -->

请仔细阅读

![Image from PDF page 285](../images/page-0285-image-01.png)

对于 Nucleo-L476RG，ST-LINK MCO 输出未连接到 OSCIN，以降低低功耗模式下的功耗。因此，除非按照前述描述在 X3 焊盘上安装外部晶振，否则 Nucleo-L476RG 中的 HSE 无法使用。

##### 10.1.3.1.2 OSC 32kHz 时钟供电

配置对应低速时钟 (LSE) 的引脚有三种方式：

- 板载振荡器：X2 晶振。关于 STM32 微控制器的振荡器设计指南，请参阅 AN2867¹⁵。
- 来自外部 PC14 的振荡器：通过 CN7 连接器的第 25 引脚从外部振荡器引入。需要以下配置：

- – SB48 和 SB49 ON – 移除 R34 和 R36
- 未使用 LSE：PC14 和 PC15 用作 GPIO，而非低速时钟。需要以下配置：

– SB48 和 SB49 ON – 移除 R34 和 R36

根据 NUCLEO 板硬件版本的不同，LSE 有两种可能的默认配置。PCB 底部贴纸上标有板版本 MB1136 C-01/02/03。

- 板标记 MB1136 C-01 对应配置为未使用 LSE 的板。
- 板标记 MB1136 C-02（或更高版本）对应配置为使用板载 32kHz 振荡器的板。
- 板标记 MB1136 C-03（或更高版本）对应使用新 LSE 晶振 (ABS25) 并更新了 C26、C31 和 C32 数值的板。

请仔细阅读

![Image from PDF page 285](../images/page-0285-image-02.png)

所有发布版本等于 MB1136 C-02 的 Nucleo 板在阻尼电阻 R34、R36 以及电容 C26、C31 和 C32 的数值上存在严重问题。此问题导致 LSE 无法正确启动。

¹⁵https://bit.ly/2WbvHgS

<!-- page: 286 -->

#### 10.1.3.2 Nucleo-64 rev. MB1367（新版，配备 ST-LINK v3）的时钟源

##### 10.1.3.2.1 OSC 时钟供电

配置对应外部高速时钟 external highspeed clock (HSE) 的引脚有四种方式：

- 来自 ST-LINK 的 MCO：使用 ST-LINK 的 MCO 输出作为输入时钟。该频率不可更改，固定为 8 MHz 或 8.33MHz¹⁶，并连接到 STM32 微控制器的 PF0-OSC_IN。配置必须为：

- – SB27 ON – SB25 和 SB26 OFF – SB24 和 SB28 OFF
- 板载 HSE 振荡器，来自 X3 晶振（默认）：关于典型频率及其电容和电阻，请参阅 STM32 微控制器数据手册以及 STM8S、STM8A 和 STM32 微控制器的振荡器设计指南应用笔记 (AN2867¹⁷)。建议使用具有以下特性的晶振：24 MHz，6 pF 负载电容，20 ppm。配置必须为：

- – SB25 和 SB26 ON – SB24 和 SB28 OFF – SB27 OFF – 使用 6.8 pF 电容焊接 C56 和 C59
- 来自外部 PF0 的振荡器：通过 CN7 连接器的第 29 引脚从外部振荡器引入。配置必须为：

- – SB28 ON – SB24 OFF – SB25 和 SB26 OFF – SB27 OFF
- 未使用 HSE：PF0 和 PF1 用作 GPIO，而非时钟。配置必须为：

– SB24 和 SB28 ON – SB27 OFF – SB25 和 SB26 OFF

¹⁶默认情况下，ST-LINK v3 配置为 MCO 时钟频率为 HSI/2，在 STM32F723IEK6 中对应 16MHz/2 = 8MHz。从 STLinkUpgrade 3.3.7 开始，可以配置 ST-LINK v3 固件，使 MCO 由 HSE/3 驱动，对应 25MHz/3 = 8.33MHz。与内部 HSI（修剪至 1%）相比，此方案提供了更好的时钟精度。如果切换到 8.33 MHz，目标应用程序必须相应更新：必须在 PLL 配置中应用系数 ×(24/25)，以保持后级时钟树不变（例如，如果 PLLN = 400，则设置 PLLN = 384）。此外，通常在 stm32xxx_hal_conf.h 中定义的 HSE_VALUE 常量必须更改为值 8333333。更多信息请参阅 RN0093。 ¹⁷https://bit.ly/2WbvHgS

<!-- page: 287 -->

##### 10.1.3.2.2 OSC 32kHz 时钟源

配置对应低速时钟 (LSE) 引脚有三种方式：

- 板载振荡器（默认）：X2 晶振。请参阅《STM8S、STM8A 和 STM32 微控制器振荡器设计指南》应用笔记 (AN2867¹⁸)。建议使用具有以下特性的晶振：32.768 kHz，6 pF 负载电容，20 ppm。配置必须为：

- – SB30 和 SB31 开启 – SB29 和 SB32 关闭
- 来自外部 PC14 的振荡器：通过 CN7 连接器的第 25 引脚从外部振荡器引入。配置必须为：

- – SB29 和 SB32 开启 – SB30 和 SB31 关闭
- 不使用 LSE：PC14 和 PC15 用作 GPIO，而不是低速时钟。配置必须为：

– SB29 和 SB32 开启 – SB30 和 SB31 关闭

## 10.2 HAL_RCC 模块概述

到目前为止，我们已经了解到复位和时钟控制 (RCC) 外设负责配置 STM32 MCU 的整个时钟树。HAL_RCC 模块包含 CubeHAL 中对应的描述符和例程，用于抽象特定的 RCC 实现。然而，该模块的实际实现不可避免地反映了特定 STM32 系列和部件号时钟树的特殊性。正如我们对其他 HAL 模块所做的那样，深入探讨此模块超出了本书的范围。这将要求我们跟踪多个 STM32 微控制器之间的太多差异。因此，我们现在将简要概述其主要功能以及时钟树配置过程中涉及的步骤。

配置时钟树最相关的 C 结构体是 RCC_OscInitTypeDef 和 RCC_ClkInitTypeDef。前者用于配置 RCC 内部/外部振荡器源 (HSE, HSI, LSE, LSI)，以及如果 MCU 提供的话，一些额外的时钟源。例如，F0 系列的一些 STM32 MCU (STM32F07x, STM32F0x2 和 STM32F09x) 除了提供 USB 2.0 支持外，还提供一个内部专用且出厂校准的、运行在 48MHz 的高速振荡器，用于偏置 USB 外设。如果是这种情况，RCC_OscInitTypeDef 结构体也用于配置这些额外的时钟源。RCC_OscInitTypeDef 结构体还有一个字段，它是 RCC_PLLInitTypeDef 结构体的实例，用于配置用于提高源时钟速度的主 PLL。它反映了主 PLL 的硬件结构，并且可以根据 STM32 系列由多个字段组成（在 STM32F2/4/7 MCU 中，它可能具有相当复杂的结构）。

¹⁸https://bit.ly/2WbvHgS

<!-- page: 288 -->

相反，RCC_ClkInitTypeDef 结构体用于配置系统时钟切换 (SWCLK)、AHB 总线以及 APB1/2 总线的源时钟。

CubeMX 旨在为我们的 MCU 生成正确的时钟树代码初始化。所有必要的代码都打包在 SystemClock_Config() 例程中，我们在之前生成的项目中已经遇到过它。例如，以下 SystemClock_Config() 实现反映了运行在 48MHz 的 STM32F030R8 MCU 的时钟树配置：

```text
1
void SystemClock_Config(void) {
2
RCC_OscInitTypeDef RCC_OscInitStruct;
3
RCC_ClkInitTypeDef RCC_ClkInitStruct;
```

4

```text
5
RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
6
RCC_OscInitStruct.HSIState = RCC_HSI_ON;
7
RCC_OscInitStruct.HSICalibrationValue = 16;
8
RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
9
RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
10
RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL12;
11
RCC_OscInitStruct.PLL.PREDIV = RCC_PREDIV_DIV1;
12
HAL_RCC_OscConfig(&RCC_OscInitStruct);
```

13

```text
14
RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_SYSCLK;
15
RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
16
RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
17
RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
18
HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_1);
```

19

```text
20
HAL_SYSTICK_Config(HAL_RCC_GetHCLKFreq()/1000);
```

21

```text
22
HAL_SYSTICK_CLKSourceConfig(SYSTICK_CLKSOURCE_HCLK);
```

23

```text
24
/* SysTick_IRQn interrupt configuration */
25
HAL_NVIC_SetPriority(SysTick_IRQn, 0, 0);
26
}
```

第 [5:12] 行选择 HSI 作为源振荡器并启用主 PLL，通过 PLL 多路复用器将 HSI 设置为其时钟源。然后时钟频率被提高十二倍（设置 PLLMUL 字段）。第 [14:18] 行设置 SYSCLK 频率。选择 PLLCLK 作为时钟源（第 15 行）。同样，选择 SYSCLK 频率作为 AHB 总线的源，并选择相同的 HCLK 频率 (RCC_HCLK_DIV1) 作为 APB1 总线的源。其他代码行设置了 SysTick 定时器，这是 Cortex-M 内核中可用的一个特殊定时器，用于同步一些内部 HAL 活动（或者如我们将在第 23 章中看到的，用于驱动 RTOS 的调度器）。HAL 基于 SysTick 定时器每 1ms 生成一个中断的约定。由于我们将 SysTick 时钟配置为以 48MHz 的最大内核频率运行（这意味着 SYSCLK 每秒执行 48,000,000 个时钟周期），我们可以设置 SysTick 定时器，使其

<!-- page: 289 -->

每 48,000,000 周期/1000ms = 48,000 个时钟周期生成一个中断¹⁹。

### 10.2.1 在运行时计算时钟频率

有时了解 CPU 内核的运行速度至关重要。如果我们的固件被设计为始终以既定频率运行，我们可以轻松地在固件中使用符号常量硬编码该值。然而，这始终是一种糟糕的编程风格，并且如果我们要动态管理 CPU 频率，则完全不适用。CubeHAL 提供了一个可用于计算 SYSCLK 频率的函数：HAL_RCC_GetSysClockFreq()²⁰。然而，必须特别小心地处理此函数。让我们看看原因。

HAL_RCC_GetSysClockFreq() 并不返回真实的 SYSCLK 频率（在没有已知且精确的外部参考的情况下，它永远无法以可靠的方式做到这一点），而是基于以下算法得出结果：

- 如果 SYSCLK 源是 HSI 振荡器，则返回基于 HSI_VALUE 宏的值；
- 如果 SYSCLK 源是 HSE 振荡器，则返回基于 HSE_VALUE 宏的值；
- 如果 SYSCLK 源是 PLLCLK，则根据特定 STM32 MCU 实现，返回基于 HSI_VALUE/HSE_VALUE 乘以 PLL 因子的值。

HSI_VALUE 和 HSE_VALUE 宏定义在 stm32xxx_hal_conf.h 文件中，它们是硬编码的值。HSI_VALUE 由 ST 在芯片设计期间定义，我们可以信任对应宏的值（除了 1% 的精度误差）。相反，如果我们使用外部振荡器作为 HSE 源，我们必须为 HSE_VALUE 宏提供实际值，否则 HAL_RCC_GetSysClockFreq() 函数返回的值将是错误的²¹。这也影响 SysTick 定时器的滴答频率（即生成定时器中断所需的时间）。

我们还可以使用 SystemCoreClock CMSIS 全局变量来获取内核频率。

![Image from PDF page 289](../images/page-0289-image-01.png)

仔细阅读

如果我们决定手动操作时钟树配置而不使用 CubeHAL 例程，我们必须记住，每次更改 SYSCLK 频率时，都需要调用 CMSIS 函数 SystemCoreClockUpdate()，否则某些 CMSIS 例程可能会给出错误结果。此函数由 HAL_RCC_ClockConfig() 例程自动为我们调用。

¹⁹ 如我们将在下一章所见，定时器是一个自由计数器模块，即在每个时钟周期从 0 计数到给定值的设备。请注意，为了完整性，SysTick 定时器是一个 24 位递减计数器定时器，即它从配置的最大值（在我们的情况下为 48.000）递减到零，然后自动重新开始。定时器的源时钟决定了该定时器计数的速度。由于这里我们指定 SysTick 定时器的时钟源是 HCLK（第 22 行），因此计数器每 1ms 达到零。 ²⁰ 请注意，Cortex-M 内核不是由 SYSCLK 频率驱动的，而是由 HCLK 频率驱动的，后者可能会被 AHB 预分频器降低。因此，总结一下，内核频率等于 HAL_RCC_GetSysClockFreq()/AHB-预分频器。 ²¹ HAL_RCC_GetSysClockFreq() 被定义为返回一个 uint32_t。这意味着对于 HSE 振荡器的小数值，它可能会返回错误结果。

<!-- page: 290 -->

### 10.2.2 启用主时钟输出

如前所述，根据所使用的 IC 封装，STM32 MCU 允许将时钟信号路由到一个或两个输出 I/O，称为主时钟输出（Master Clock Output，MCO）。这是通过使用以下函数实现的：

```text
void HAL_RCC_MCOConfig(uint32_t RCC_MCOx, uint32_t RCC_MCOSource, uint32_t RCC_MCODiv);
```

例如，要在 STM32F401RE MCU（对应 PA8 引脚）中将 PLLCLK 路由到 MCO1 引脚，我们必须以以下方式调用上述函数：

```text
HAL_RCC_MCOConfig(RCC_MCO1, RCC_MCO1SOURCE_PLLCLK, RCC_MCODIV_1);
```

### 仔细阅读

![Image from PDF page 290](../images/page-0290-image-01.png)

请注意，当配置 MCO 引脚为输出 GPIO 时，其速度（即压摆率）会影响输出时钟的质量。此外，对于较高的时钟频率，必须以以下方式启用补偿单元：

```text
HAL_EnableCompensationCell();
```

有关此功能的更多信息，请参阅您的 MCU 数据手册。

### 10.2.3 启用时钟安全系统

时钟安全系统（Clock Security System，CSS）是 RCC 外设的一个功能，用于检测外部 HSE 的故障。CSS 在某些关键应用中是一个重要功能，在这些应用中，HSE 的故障可能会导致用户受伤。其重要性由以下事实证明：故障检测是通过 NMI 异常通知的，这是一种无法禁用的 Cortex-M 异常。

当检测到 HSE 故障时，MCU 自动切换到 HSI 时钟，该时钟被选为 SYSCLK 时钟的源。因此，如果需要更高的内核频率，我们需要在 NMI 异常处理程序中进行适当的初始化。

要启用 CSS，我们使用 HAL_RCC_EnableCSS() 例程，并需要以以下方式²²定义 NMI 异常的处理程序：

```text
void NMI_Handler(void) {
HAL_RCC_NMI_IRQHandler();
}
```

捕获 HSE 时钟故障的正确方法是定义回调：

²² 无需启用 NMI 异常，因为它会自动启用，且无法禁用。

<!-- page: 291 -->

```text
void HAL_RCC_CSSCallback(void) {
//Catch the HSE failure and take proper actions
}
```

## 10.3 HSI 校准

我们在之前看到的 SystemClock_Config() 例程中保留了一行未注释的代码：第 7 行的指令。它用于对 HSI 振荡器进行微调校准。但它具体做了什么？

如前所述，由于制造工艺的差异，内部 RC 振荡器的频率可能因芯片而异。因此，ST 对 HSI 振荡器进行了出厂校准，使其在室温下具有 1% 的精度。复位后，出厂校准值会自动加载到 RCC 配置寄存器 (RCC_CR) 的第二个字节 (HSICAL) 中（图 10.9 展示了 STM32F401RE²³ 中该寄存器的实现）。

![Image from PDF page 291](../images/page-0291-image-01.jpeg)

图 10.9：STM32F401RE 微控制器中的 RCC_CR 寄存器

内部 RC 振荡器的频率可以进行微调，以在更宽的温度和电源电压范围内实现更高的精度。修剪位 (trimming bits) 用于此目的。五个修剪位 RCC_CR->HSITRIM[4:0] 用于微调。默认的修剪值为 16。修剪值的增加/减少会导致 HSI 频率的增加/减少。HSI 振荡器以 HSI 时钟速度的 0.5% 为步长进行微调：

- 写入 17 到 31 范围内的修剪值会增加 HSI 频率。
- 写入 0 到 15 范围内的修剪值会降低 HSI 频率。
- 写入等于 16 的修剪值会使 HSI 频率保持其默认值。

可以使用以下程序对 HSI 进行校准：

1. 设置内部高速 RC 振荡器系统时钟；
2. 测量每个修剪值下的内部 RC 振荡器频率；
3. 计算每个修剪值的频率误差（根据已知的参考值）；

²³该图取自 ST 的 RM0368 应用笔记 (https://bit.ly/1Kq3SoE)。

<!-- page: 292 -->

4. 最后，将修剪位设置为最优值（对应最低的频率误差）。

内部振荡器频率不是直接测量的，而是通过与典型值比较使用定时器计数的时钟脉冲数计算得出的。为此，必须有一个非常精确的参考频率，例如由外部 32.768 kHz 晶振提供的 LSE 频率，或市电的 50 Hz/60 Hz。

ST 提供了多个应用笔记，更详细地描述了此过程（例如，AN4067²⁴ 是关于 STM32F0 系列的校准过程）。请参阅这些文档以获取更多信息。

²⁴https://bit.ly/1R8kEbf
