<!-- page: 119 -->

# 4. STM32CubeMX 工具

通过几条汇编指令即可配置 8 位微控制器外设的时代已经远去。尽管仍有一群根深蒂固的开发者坚持使用纯汇编代码¹开发嵌入式软件，但在当今的项目开发中，时间是最昂贵的资源，对于 STM32 这样相当复杂的硬件平台，获得尽可能多的帮助至关重要。此外，在现代 32 位 MCU 中，尤其是那些拥有大量 I/O 端口的型号，即使驱动一个简单的 GPIO 也可能需要你在长达一千页的数据手册中翻阅数十页。信不信由你，如果没有 ST HAL 的专门支持，仅仅初始化 STM32H7 上像 DCMI 或 ETH 接口这样的高级外设，真的会令人非常沮丧。最后，要了解 GPIO 的所有可能配置选项，要求你对特定 STM32 型号所支持的所有外设、其特定的引脚布局和配置有完整的概览。幸运的是，ST 提供了一款强大且便捷的工具，使我们无需关注外设配置底层的所有特定实现细节，这就是 STM32CubeMX。

STM32CubeMX² 是每位 STM32 开发者的瑞士军刀，特别是对于 STM32 平台的新手来说，它是一款基础工具。这是一款相当复杂的软件，由 ST 免费分发，既可以作为从 ST 网站下载的独立工具使用，也可以作为 STM32CubeIDE 内部的集成组件使用。

在本章中，我们将了解 CubeMX 的工作原理，以及如何利用它生成的代码从零开始创建可运行的项目。这将使我们能够创建更好的代码，并准备好与 STM32Cube HAL 的其余部分集成。然而，本章不能替代 CubeMX 工具的官方 ST 文档³，该文档长达 350 多页，深入解释了其所有功能。

## 4.1 CubeMX 工具简介

CubeMX 是用于配置我们项目中选定的微控制器的工具。它既用于选择正确的硬件连接，也用于生成配置 ST HAL 所需的代码。

CubeMX 是一个以 MCU 为中心的应用程序。这意味着该工具执行的所有活动都基于：

- STM32 MCU 的系列（F0、F1 等）。

¹ 可能有一天，有人会向他们解释，除了少数特定情况外，现代编译器从 C 语言生成的汇编代码比手工直接编写的汇编代码更好。然而，我们必须说，这些习惯仅限于 PIC12 等超低成本 8 位 MCU。 ² 在本书其余部分，STM32CubeMX 的名称将简化为 CubeMX。 ³ https://bit.ly/3k8HeE2

<!-- page: 120 -->

- 为我们设备选择的封装类型（LQFP48、BGA144 等）。
- 我们项目中需要的硬件外设（USART、SPI 等）。

- 选定的外设如何映射到微控制器引脚。
- MCU 的一般配置（如时钟、电源管理、NVIC 控制器等）

除了与硬件相关的功能外，CubeMX 还能够处理以下软件方面：

- 针对给定 MCU 系列的 ST HAL 管理（CubeF0、CubeF1 等）。
- 配置额外的软件库，称为中间件（Middlewares）库，我们可能在项目中需要它们来驱动特定外设或管理复杂的软件栈（FatFs、LwIP、FreeRTOS 等）。
- 我们将用于构建固件的开发环境（IAR EWARM、Keil MDK- ARM、STM32CubeIDE）⁴。

在 CubeMX 中生成项目本质上是一个两阶段的活动。第一步是通过目标选择向导（Target Selection wizard）选择正确的 STM32 MCU 或开发板。第二步是根据项目需求配置 MCU 和任何所需的中间件库。让我们深入研究这两个阶段。

### 4.1.1 目标选择向导

我们在第 3 章⁵中已经使用 CubeMX 生成了 hello-nucleo，即我们的第一个 STM32 项目。我们看到项目生成从目标选择视图开始。该视图是一个基于选项卡的窗口，有四个主要选项卡（见图 4.1）：MCU/MPU 选择器、板卡选择器、示例选择器和交叉选择器。让我们更深入地分析它们。

⁴ CubeMX 的独立版本不仅可以为官方 STM32CubeIDE 生成项目代码和配置，还可以为其他商业 IDE 生成。然而，在本书中，我们将仅关注在 STM32CubeIDE 内部使用 CubeMX 的相关方面。 ⁵ ch3-hello-nucleo-project

<!-- page: 121 -->

![Image from PDF page 121](../images/page-0121-image-01.jpeg)

图 4.1：CubeMX MCU/MPU 选择器

#### 4.1.1.1 MCU/MPU 选择器

第一个选项卡允许从整个 STM32 产品组合中选择一个微控制器。多个过滤器有助于为用户应用识别正确的微控制器。

- 内核：此过滤器允许仅选择属于选定 Cortex-M 内核（-M0、M4 等）的 MCU。
- 系列（Series）：使用此过滤器，我们可以仅显示属于选定 STM32 系列（F0、F4 等）的 MCU。
- 产品线（Line）：此过滤器允许进一步选择属于子系列（如 Value line 等）的 MCU。
- 封装（Package）：此过滤器允许选择具有所需物理封装（LQFP、WLCSP 等）的所有 MCU。
- 其他（Other）：此部分提供多个过滤器，允许根据预算价格、I/O 数量、FLASH、SRAM 和 EEPROM 内存的尺寸来限制 MCU。
- 外设（Peripheral）：此部分允许仅选择具有所需集成外设的 MCU。

<!-- page: 122 -->

![Image from PDF page 122](../images/page-0122-image-01.jpeg)

图 4.2：CubeMX 板卡选择器

#### 4.1.1.2 开发板选择器

开发板选择器（Board Selector）选项卡允许在所有官方 ST 开发板中进行筛选（参见图 4.2）。多个筛选器有助于识别正确的开发板。

- 类型（Type）：此筛选器允许将选择范围限制为属于特定系列（如 Nucleo-64、Discovery、Evaluation Board 等）的开发板。
- MCU/MPU 系列（MCU/MPU Series）：使用此筛选器，可以仅显示目标微控制器（MCU）属于所选 STM32 系列（如 F0、F4 等）的开发板。
- 其他（Other）：此部分提供两个筛选器，允许根据预算价格或振荡器频率限制微控制器（根据本作者的观点，这不是一个非常有用的筛选器）。
- 外设（Peripheral）：此部分允许根据所需的集成外设选择开发板。

#### 4.1.1.3 示例选择器

多年来，ST 开发了数千个示例，以展示如何使用 STM32 产品线的单个外设或扩展中间件（Middleware）。示例选择器（Example Selector）选项卡允许在超过 5,000 个示例中进行筛选（参见图 4.3）。多个筛选器有助于识别正确的示例。

- 名称（Name）：此筛选器允许将示例列表限制为具有特定项目名称的示例（每个示例通常可用于多个微控制器和/或开发板）。

<!-- page: 123 -->

- 关键字（Keyword）：此筛选器根据给定的搜索关键字限制示例列表。
- 开发板（Board）：此筛选器选择针对特定目标开发板的所有示例。
- MCU/MPU：此筛选器选择针对特定目标微控制器的所有示例。
- 项目类型（Project Type）：此筛选器允许在应用程序（Application）、演示（Demonstration）和示例（Example）项目之间进行选择；好吧，以我卑微的观点来看，他们在这个字段上只是吹毛求疵。
- 基于驱动程序（Based on driver）：使用此筛选器可以选择那些使用 CubeHAL、CubeHAL-LL 或两者混合制作的示例；稍后会有更多介绍。
- 中间件（Middleware）：此筛选器允许选择所有展示特定中间件库用法的示例。
- MCU/MPU 库（MCU/MPU Library）：此筛选器可能会引起一点误解，因为其用途是选择所有展示如何编程特定外设的示例。
- 开发板支持包库（Board Support Package Library）：许多 STM32 开发套件集成了额外外设，例如 LCD 显示屏、DCMI 摄像头、MEMS 传感器等。为了测试这些额外外设，ST 提供了有用的开发板支持包（简称 BSP）库。当你需要在自定义开发板上驱动类似外设时，这些免费库非常有用。此筛选器允许选择使用特定 BSP 库的示例。

![Image from PDF page 123](../images/page-0123-image-01.jpeg)

图 4.3：CubeMX 示例选择器

<!-- page: 124 -->

#### 4.1.1.4 交叉选择器

如果你习惯使用其他供应商（Microchip、Renesas 等）的微控制器，并且正在考虑将电子开发板移植到 STM32 微控制器，交叉选择器（Cross Selector）部分可能有助于你识别正确的替代方案。然而，在我看来，这个工具在寻找特定 STM32 微控制器的替代方案时工作得很好。如果 STM32 微控制器在市场上缺货（这在当今时代绝非罕见），这可能特别有用。交叉选择器工具（如图 4.4 所示）提供了一个匹配百分比，让你了解建议的替代方案与你当前微控制器的差异程度。然而，请始终手边备好数据手册，并仔细检查即使是非主要规格，例如 GPIO 的物理行为（电压容差、摆率等）。

![Image from PDF page 124](../images/page-0124-image-01.jpeg)

图 4.4：CubeMX 交叉选择器

### 4.1.2 微控制器和中间件配置

一旦项目生成完毕，STM32CubeIDE 会自动打开项目文件夹中名为 <project-name>.ioc 的文件。此文件是 CubeMX 的主项目文件，包含在 CubeMX 中执行的所有配置。基于这些配置，CubeMX 将生成相应的项目结构，包括使用所选外设和中间件组件所需的所有源文件和库。

<!-- page: 125 -->

当打开 .ioc 文件时，CubeMX 会显示设备配置工具（Device Configuration Tool），如图 4.5 所示。

![Image from PDF page 125](../images/page-0125-image-01.jpeg)

图 4.5：CubeMX 设备配置工具视图

在 CubeMX 视图的上部，你可以看到一个上下文菜单，分为浅蓝色和深蓝色。菜单分为四个主要选项卡，每个选项卡都有其专用的视图。让我们简要介绍它们。

#### 4.1.2.1 引脚布局视图与配置

引脚布局与配置（Pinout & Configuration）视图是第一个视图，它又分为几个子部分。右侧包含带有所选外设和 GPIO 的微控制器表示，ST 称之为引脚布局视图（Pinout view）。它允许轻松地在微控制器配置内部导航，是配置微控制器的便捷方式。⁶ 亮绿色的引脚表示已启用。这意味着 CubeMX 将生成必要的代码，根据绑定的外设配置该引脚。例如，考虑图 4.5 中的项目配置，对于引脚 PA5，CubeMX 将生成所需的 C 代码，将其设置为通用输出引脚以驱动 LD2 LED⁷。相反，对于 PA2 引脚，CubeMX 将生成代码将其配置为 USART TX 引脚。

⁶ 在此上下文中，引脚（pin）和信号（signal）可以互换使用。⁷ 在某些 Nucleo 开发板上，LD2 LED 连接到不同的引脚。例如，在 Nucleo-F302 上，LD2 连接到 PB13 引脚。在配置之前，请查阅你特定开发板的手册。

<!-- page: 126 -->

当相应外设未启用时，引脚显示为橙色。例如，在图 4.6 中，PA2⁸ 和 PA3 引脚已启用，CubeMX 将生成相应的 C 代码来初始化它们，但关联的外设（USART2）未启用，因此不会自动生成用于设置该外设的 USART 相关代码。浅黄色的引脚是电源引脚，其配置无法更改。BOOT 和 RESET 引脚显示为卡其色，其配置无法更改。

![Image from PDF page 126](../images/page-0126-image-01.png)

图 4.6：外设的替代映射

当鼠标指针悬停在微控制器引脚上时，会显示上下文工具提示（参见图 4.7）。例如，引脚 PB3 的上下文工具提示告诉我们，该信号映射到串行线调试（Serial Wire Debug, SWD）接口，并作为串行线输出（Serial Wire Output, SWO）引脚。此外，还显示了引脚编号（本例中为 55）。

![Image from PDF page 126](../images/page-0126-image-02.png)

图 4.7：上下文工具提示有助于理解信号用途

具有较高引脚数量的 STM32 微控制器允许将外设映射到不同的引脚。例如，在 STM32F401xE 微控制器中，SPI2 MOSI 信号可以映射到引脚 PC2 或 PB14。通过 Ctrl+点击引脚，CubeMX 可以轻松显示允许的替代方案。如果存在替代引脚，它会以蓝色显示（仅当引脚不处于复位状态——即已启用时——才显示替代方案）。例如，在图 4.6 中，我们可以看到，如果对 PC2 引脚执行 Ctrl+点击，PB14 信号会以蓝色高亮显示⁹。这在开发板布局期间非常有用。如果无法或不方便将信号布线到该引脚，或者该引脚需要用于其他功能，使用替代引脚可能会简化开发板设计。

⁸ 本节中显示的引脚配置是指 STM32L073RZ 微控制器。⁹ 请注意，在最近的 CubeMX 版本中，Ctrl+点击的行为略有变化。要显示替代引脚，你需要在 Ctrl+点击后按住鼠标，直到替代引脚开始闪烁。第一次做时并不直观。

<!-- page: 127 -->

引脚可能会简化开发板。

![Image from PDF page 127](../images/page-0127-image-01.png)

图 4.8：引脚的替代功能

同样地，大多数微控制器（MCU）引脚可以具有替代功能。点击引脚时会显示一个上下文菜单。这允许我们选择希望为该信号启用的功能。

这种灵活性会导致信号功能之间产生冲突。CubeMX 会尝试自动解决这些冲突，将信号分配给另一个引脚。固定引脚（Pinned signals）是指其功能被锁定到特定引脚的引脚，从而防止 CubeMX 选择替代引脚。当冲突导致某个外设无法使用时，芯片视图（Chip View）中的引脚模式会被禁用，并且该引脚会被标记为橙色。要将输入/输出（I/O）标记为固定，请右键点击引脚并选择“Pin locking”（引脚锁定）选项。

CubeMX 还提供了一个非常便捷的功能：可以为每个单独的 MCU 信号定义自定义标签。通过右键点击一个已启用的引脚，您可以选择“Enter User Label”（输入用户标签）选项。随后会出现一个上下文弹出窗口，如图 4.9 所示。标签的形式可以是 LABEL [Comment]。LABEL 部分将用于在 main.h 文件中生成相应的宏，而 [Comment] 部分只是显示在引脚布局视图（Pinout View）中供开发人员参考的注释。

![Image from PDF page 127](../images/page-0127-image-02.png)

图 4.9：如何为 MCU I/O 添加自定义标签

作为引脚布局视图（Pinout view）的替代视图，系统视图（System view）提供了所有可通过软件配置的组件概览：GPIO、外设、DMA、NVIC、中间件（Middleware）以及额外的软件组件。可点击的按钮允许打开给定组件的配置选项（模式和配置面板）。按钮图标的颜色反映了配置状态。

<!-- page: 128 -->

![Image from PDF page 128](../images/page-0128-image-01.jpeg)

表 4.1：CubeMX 在配置窗格中显示组件列表的方式

在引脚布局与配置视图（Pinout & Configuration view）的左侧，我们有类别列表（在 ST 官方文档中也称为组件列表），既可以按字母顺序显示，也可以按类别显示。默认情况下，它包含目标 MCU 支持的外设和中间件组件列表，这是一种启用/禁用并配置所需外设和软件中间件的便捷方式。从该列表中选择一个条目会打开两个附加面板（模式和配置），允许用户设置其功能模式并配置

<!-- page: 129 -->

将包含在生成代码中的初始化参数。

表 4.1 展示了组件列表视图中使用的图标和颜色方案，以及模式面板中对应的颜色方案。

- 情况 1：表示该外设可用且当前处于禁用状态，其所有可能的模式均可使用。例如，对于 USART 接口，该外设的所有可能模式（异步、同步、IrDA 等）均可用。
- 情况 2：表示该外设因与另一个外设冲突而被禁用。这意味着两个外设使用相同的 GPIO，因此无法同时使用它们。将鼠标悬停在上面会显示涉及冲突的另一个外设。例如，对于 STM32F401RE MCU，不可能同时使用 I2S2 和 SPI2 引脚。
- 情况 3：表示该外设已配置（至少设置了一种模式），且其他所有模式均可用。绿色对勾表示所有参数已正确配置，洋红色叉号表示未正确配置。
- 情况 4：表示该外设未配置（未设置任何模式），且其至少一种模式不可用。
- 情况 5：表示该外设未配置（未设置任何模式），且没有任何模式可用。将鼠标悬停在外设名称上可以显示描述冲突的工具提示。

<!-- page: 130 -->

#### 4.1.2.2 时钟配置视图

![Image from PDF page 130](../images/page-0130-image-01.png)

图 4.10：CubeMX 时钟视图

时钟配置视图（Clock Configuration view）是进行所有与时钟管理相关的配置的面板。在这里，我们可以设置主内核和外设的时钟。所有时钟源和 PLL 的配置都以图形方式呈现（见图 4.10）。用户第一次看到此视图时，可能会被大量的配置选项所困惑。然而，经过一点练习，这是处理 STM32 时钟配置（与 8 位 MCU 相比相当复杂）的最简单方式。

如果您的板级设计需要高速时钟（HSE）、低速时钟（LSE）或两者都需要外部源，您必须首先在引脚布局视图（Pinout view）的系统内核（System Core）-> RCC 部分中启用它，如图 4.11 所示。

<!-- page: 131 -->

![Image from PDF page 131](../images/page-0131-image-01.jpeg)

图 4.11：在 CubeMX 中启用 HSE 和 LSE

完成此操作后，您将能够在时钟视图中更改时钟源。

时钟树配置将在第 10 章中探讨。为了避免在此阶段产生混淆，请保持所有参数为 CubeMX 自动配置的状态。

超频

![Image from PDF page 131](../images/page-0131-image-02.png)

一种常见的黑客做法是超频 MCU 内核，通过更改 PLL 配置使其以更高的频率运行。作者强烈不鼓励这种做法，因为这不仅可能会严重损坏微控制器，还可能导致难以调试的异常行为。

除非您绝对确定自己在做什么，否则请勿更改任何设置。

<!-- page: 132 -->

### 4.1.3 项目管理器

![Image from PDF page 132](../images/page-0132-image-01.png)

图 4.12：项目管理器视图

项目管理器视图包含与工作区、工具链、源代码生成以及所使用的硬件抽象层（HAL）库类型相关的项目级配置。该视图进一步分为三个部分：

- 项目（Project）：此部分包含通用项目设置，例如项目名称、文件系统中的项目位置、工具链以及 CubeHAL 库的版本。
- 代码生成器（Code Generator）：此部分包含与 CubeMX 代码生成相关的附加选项，例如 HAL *.c/h 文件如何包含在项目中、当对项目设置应用新的更改时如何保持模板文件结构等。
- 高级设置（Advanced Settings）：此部分包含更多高级项目选项，主要与用于生成特定外设初始化代码的 CubeHAL 类型有关。可以在 CubeHAL 和更优化的 Cube-LL 库之间进行选择。同时，可以选择不为某些外设或中间件组件生成代码，以便程序员决定添加自己的代码。

<!-- page: 133 -->

什么是 Cube 底层 API？

随着 STCube 计划的推出，ST 完全重新设计了 STM32 系列的 SDK，引入了硬件抽象层（HAL）库，并将旧的标准外设库（SPL）弃之不用。尽管 SPL 在 ST 社区中非常流行，但它缺乏许多与较新且功能更强大的 STM32 微控制器相关的特性。然而，多年来 HAL 库受到了大量批评，一方面是因为它在最初几年存在太多错误，另一方面——也是更重要的一点——是因为它并不是嵌入式应用开发中代码优化良好的典范。

CubeHAL 确实是一个性能不佳的库，但这有一个简单的原因：它被设计为抽象化，以简化同一系列微控制器之间以及不同 STM32 系列微控制器之间用户代码的移植。这导致该库充满了 if 和 then 语句，并且在针对非常具体的微控制器工作时包含大量不必要的代码。但这是为了简化开发流程——以及更重要的是——为了采用如 STM32 产品组合这样复杂的微控制器架构所必须付出的代价。HAL API 分为两类：通用 API，为所有 STM32 系列提供通用和通用的功能；以及扩展 API，包含针对特定系列或部件号的具体和定制功能。HAL 驱动程序包含一套完整的即用型 API，简化了用户应用的实现。HAL 驱动程序是面向功能的，而不是面向 IP 的。例如，定时器 API 根据 IP 功能分为几个类别，如基本定时器、捕获和脉冲宽度调制（PWM）。HAL 驱动层通过检查所有函数的输入值来实现运行时故障检测。这种动态检查增强了固件的健壮性。

近年来，ST 通过引入 Cube 底层（简称 LL）驱动程序集来回应关于库性能的强烈批评。顾名思义，LL 库旨在高度优化，将处理特定 STM32 系列和特定部件号（P/N）非常具体特性的责任留给程序员。LL 驱动程序基于 STM32 外设的可用功能提供硬件服务。这些服务准确反映了硬件能力，并提供必须按照产品线参考手册中描述的编程模型调用的原子操作。因此，LL 服务不基于独立进程，也不需要任何额外的内存资源来保存其状态、计数器或数据指针。所有操作都是通过更改关联外设寄存器的内容来执行的。与 HAL 不同，对于优化访问不是关键特性的外设，或者需要大量软件配置和/或复杂上层堆栈（如 USB）的外设，不提供 LL API。基于 LL 的代码本质上是一系列 C 宏，这些宏将展开为一系列语句，从性能角度来看，分支和不可预测语句的使用非常有限。

本书不会涵盖与 LL 库相关的主题。这需要一种完全不同的文本方法，并强烈专注于少数几个 STM32 部件号。本书旨在具有通用性，并提供最相关特性的概述，以开始设计强大且复杂的电子板。如果你需要控制特定外设的每一个方面以达到最优化的代码，那么 LL 库就是你所需要的。但是，首先，我建议你先使用 CubeHAL 开始设计固件，然后再进入下一步，除非你是一位非常有经验的固件开发人员。

<!-- page: 134 -->

### 4.1.4 工具视图

工具视图包含其他相关的配置面板，其中一些面板仅在更高级的 STM32 微控制器（如 STM32MP1 系列）上可用。相反，对于所有 STM32 微控制器，都可用功耗计算器（PCC）。这是 CubeMX 的一项功能，给定一个微控制器、一个电池模型和一个用户定义的电源序列，它可以估算以下参数：

- 平均功耗。
- 电池寿命。
- 平均 DMIPS。

可以通过专用界面添加用户定义的电池。对于每个步骤，用户可以选择 VBUS 作为可能的电源，而不是电池。这将影响电池寿命的估算。如果在不同的电压级别下有功耗测量数据，CubeMX 还会提供电压值的选择。

PCC 视图将在后续章节中进行分析。

![Image from PDF page 134](../images/page-0134-image-01.png)

图 4.13：CubeMX 工具视图

<!-- page: 135 -->

## 4.2 理解项目结构

一旦完成了 MCU、其外设和中间件组件的配置，我们就可以使用 CubeMX 为我们生成 C 项目骨架。代码生成可以通过两种方式启动：

```text
• 通过保存 CubeMX 项目（.ioc 文件）并让 CubeMX 自动执行生成；
• 通过转到 Project->Generate Code 菜单（当 .ioc 文件在主透视图中被选中时），或者通过点击 Eclipse 工具栏上对应的图标（见表 2.1）。
```

CubeMX 将生成所有必要的文件，并按照图 4.14 所示的结构进行排列。

起初，你可能会被所有这些复杂性所困惑，特别是如果你是嵌入式编程或此类复杂架构的新手¹⁰。但请不要担心：在后续章节中，我们将处理这些自动生成的源文件中包含的所有细节。然而，为了开始编程而不必担心不理解相关主题，最好我们先快速浏览一下主要的项目文件夹及其包含的文件。图 4.14 是这次快速浏览的良好参考。

```text
Binaries
```

此文件夹包含编译器在构建过程结束时生成的最终二进制文件。它是一个可执行和可链接格式（ELF）文件，这是基于 Linux 的操作系统中典型的对象文件。该文件夹是 Eclipse CDT 项目组织的一部分，其内容是冗余的：相同的二进制文件也包含在 Debug 文件夹中。Includes

此文件夹扮演两个角色。它是编译器所有包含路径（即 GCC 查找 C 包含文件（.h）的文件系统上的所有目录）的图形表示。但它也是一个添加对其他包含文件的额外引用的地方，而无需处理编译器特定的参数和包含路径。有关此主题的更多信息，请参阅 Eclipse CDT 文档。Core

此文件夹包含所有特定于应用程序的文件。此文件夹及其子文件夹中的文件特定于 CubeMX 中的项目设置和 MCU 配置。Core 文件夹应包含开发应用程序所需的所有其他文件，但 Eclipse 足够智能，允许你根据需要将这些文件重新排列到不同的文件夹中。但为此需要付出很高的代价：如果你更改了 Core 文件夹结构，当你引入对 CubeMX 项目的任何修改时，你将无法更新源代码。因此，我的建议是在项目的早期阶段保持其原样。Core 文件夹中的一些文件在项目中扮演非常特殊的角色。让我们来分析它们。

¹⁰嗯……使用 STM32H7 开始学习嵌入式编程从来都不是一个好主意 ;-P。

<!-- page: 136 -->

![Image from PDF page 136](../images/page-0136-image-01.jpeg)

图 4.14：CubeMX 项目的典型结构

```text
Core/Inc/main.h
```

此文件是 main.c 的配套头文件。除了其他内容外，它还包含使用 CubeMX 与各个外设关联的所有标签的宏声明。Core/Inc/stm32XXxx_hal_conf.h

这是将 HAL 配置转换为 C 代码的文件，使用多个宏定义。这些宏用于“指示” HAL 关于启用的 MCU 功能。你会发现很多被注释掉的宏，如下所示。

<!-- page: 137 -->

```text
Filename: Core/Inc/stm32XXxx_hal_conf.h
55
#define HAL_UART_MODULE_ENABLED
56
/*#define HAL_USART_MODULE_ENABLED
*/
57
/*#define HAL_IRDA_MODULE_ENABLED
*/
58
/*#define HAL_SMARTCARD_MODULE_ENABLED
*/
59
/*#define HAL_SMBUS_MODULE_ENABLED
*/
60
/*#define HAL_WWDG_MODULE_ENABLED
*/
61
/*#define HAL_PCD_MODULE_ENABLED
*/
62
#define HAL_GPIO_MODULE_ENABLED
63
#define HAL_EXTI_MODULE_ENABLED
64
#define HAL_DMA_MODULE_ENABLED
65
#define HAL_I2C_MODULE_ENABLED
66
#define HAL_RCC_MODULE_ENABLED
67
#define HAL_FLASH_MODULE_ENABLED
68
#define HAL_PWR_MODULE_ENABLED
69
#define HAL_CORTEX_MODULE_ENABLED
```

## 它们用于在编译时有选择地包含 HAL 模块。当你需要某个模块时，如果对应的 .c/.h 文件已经包含在项目中，你只需取消相应宏的注释即可。在本书的其余部分，我们将有机会看到在此文件中定义的所有其他宏。

```text
Core/Inc/stm32XXxx_it.h and Core/Src/stm32XXxx_it.c
```

## 这两个文件是我们项目的另一个基本组成部分。所有由 CubeMX 生成的中断服务例程 (ISR) 都存储在这里。鉴于我们选择的 CubeMX 配置，该文件包含几个函数的定义。考虑到第 3 章¹¹中的 hello-nucleo 项目，只有一个有用的函数：void SysTick_Handler(void)。该函数是 SysTick 定时器的 ISR，即当 SysTick 定时器达到 0 时调用的例程。但是，这个 ISR 是在哪里被调用的？

```text
Filename: Core/Src/stm32XXxx_it.c
123
/**
124
* @brief This function handles System tick timer.
125
*/
126
void SysTick_Handler(void)
127
{
128
/* USER CODE BEGIN SysTick_IRQn 0 */
129
130
/* USER CODE END SysTick_IRQn 0 */
131
HAL_IncTick();
132
/* USER CODE BEGIN SysTick_IRQn 1 */
133
134
/* USER CODE END SysTick_IRQn 1 */
135
}
```

¹¹ch3-hello-nucleo-project

<!-- page: 138 -->

## 回答这个问题让我们有机会开始处理 Cortex-M 处理器最有趣的功能之一：嵌套向量中断控制器 (NVIC)。第 1 章中的表 1.1 展示了 Cortex-M 的异常类型。如果你还记得，我们说过在 Cortex-M CPU 中，中断是异常的一种特殊类型。Cortex-M 将 SysTick_Handler 定义为 NVIC 向量数组中的第十五个异常。但是这个数组是在哪里定义的？在 Core/Startup 文件夹中，有一个用汇编语言编写的特殊文件，称为启动文件 (startup file)。打开此文件，我们可以看到 Cortex 处理器的最小向量表，如下所示：

```text
Filename: Core/Startup/startup_stmXXxx.s
116
/******************************************************************************
117
* The minimal vector table for a Cortex M4. Note that the proper constructs
118
* must be placed on this to ensure that it ends up at physical address
119
* 0x0000.0000.
120
*******************************************************************************/
121
.section
.isr_vector,"a",%progbits
122
.type
g_pfnVectors, %object
123
.size
g_pfnVectors, .-g_pfnVectors
124
125
126
g_pfnVectors:
127
.word
_estack
128
.word
Reset_Handler
129
130
.word
NMI_Handler
131
.word
HardFault_Handler
132
.word
MemManage_Handler
133
.word
BusFault_Handler
134
.word
UsageFault_Handler
135
.word
0
136
.word
0
137
.word
0
138
.word
0
139
.word
SVC_Handler
140
.word
DebugMon_Handler
141
.word
0
142
.word
PendSV_Handler
143
.word
SysTick_Handler
144
145
/* External Interrupts */
```

## 第 145 行将 SysTick_Handler() 定义为 SysTick 定时器的 ISR。

<!-- page: 139 -->

![Image from PDF page 139](../images/page-0139-image-01.png)

请注意，启动文件在不同的 ST HAL 之间会有细微的修改。这里报告的行号可能与你的 MCU 的启动文件略有不同。此外，MemManage Fault、Bus Fault、Usage Fault 和 Debug Monitor 异常在基于 Cortex-M0/0+ 的处理器中不可用（因此相应的向量条目是 RESERVED - 参见第 1 章中的表 1.1）。然而，NVIC 中的前十五个异常对于所有基于 Cortex-M0/0+ 的处理器和所有基于 Cortex-M3/4/7 的 MCU 都是相同的。

```text
Core/Src/stm32XXxx_hal_msp.c
```

这是另一个需要分析的重要文件。首先，重要的是澄清“MSP”的含义。它代表 MCU Support Package（MCU 支持包），它定义了用于根据用户配置（引脚分配、时钟使能、DMA 和中断的使用）配置片上外设的所有初始化函数。让我们通过一个例子深入解释这一点。一个外设基本上由两部分组成：外设本身（例如，SPI2 接口）和与该外设关联的硬件引脚。

![Image from PDF page 139](../images/page-0139-image-02.png)

图 4.15：MSP 文件与 HAL 之间的关系

ST HAL 的设计使得 HAL 的 SPI 模块是通用的，并且与特定的 I/O 设置抽象分离，这些设置可能因 MCU 封装和用户定义的硬件配置而异。因此，ST 开发人员将“填充”HAL 这一部分的责任留给了用户，使用一种回调例程来配置外设所需的代码，并且这些代码位于 Core/Src/stm32XXxx_hal_msp.c 文件中（见图 4.15）。

让我们打开它。在这里我们可以找到函数 void HAL_UART_MspInit() 的定义：

<!-- page: 140 -->

```text
Filename: Core/Src/stm32XXxx_hal_msp.c
86
void HAL_UART_MspInit(UART_HandleTypeDef* huart)
87
{
88
GPIO_InitTypeDef GPIO_InitStruct = {0};
89
if(huart->Instance==USART2) {
90
/* USER CODE BEGIN USART2_MspInit 0 */
```

91

```text
92
/* USER CODE END USART2_MspInit 0 */
93
/* Peripheral clock enable */
94
__HAL_RCC_USART2_CLK_ENABLE();
```

95

```text
96
__HAL_RCC_GPIOA_CLK_ENABLE();
97
/**USART2 GPIO Configuration
98
PA2
------> USART2_TX
99
PA3
------> USART2_RX
100
*/
101
GPIO_InitStruct.Pin = USART_TX_Pin|USART_RX_Pin;
102
GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
103
GPIO_InitStruct.Pull = GPIO_NOPULL;
104
GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
105
GPIO_InitStruct.Alternate = GPIO_AF4_USART2;
106
HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
107
}
108
}
```

如你所见，HAL_UART_MspInit() 负责实际配置与 USART 外设关联的引脚对（即 PA2 和 PA3）。图 4.16 展示了函数 HAL_UART_MspInit() 的调用层次结构：如你所见，它由通用 HAL 函数 HAL_UART_Init() 调用，而后者又在 main.c 中由函数 MX_USART2_UART_Init() 调用。

![Image from PDF page 140](../images/page-0140-image-01.jpeg)

图 4.16：函数 HAL_UART_MspInit() 的调用层次结构

我们要分析的最后一个文件是 Core/Src/main.c。它基本上包含四个例程：System-Clock_Config(void)、MX_GPIO_Init(void)、MX_USART2_UART_Init(void) 和 int main(void)。第一个函数用于初始化内核和外设时钟。它的解释超出了本章的范围，但如果你对此事不陌生，其代码并不那么复杂，易于理解。MX_GPIO_Init(void) 是配置连接到 LD2 引脚和 B1 引脚（连接到 Nucleo 板上的蓝色开关）的 GPIO 的函数。第 6 章将深入解释这个问题。

### 最后，我们有 main(void) 函数，如下所示。

<!-- page: 141 -->

```text
Filename: Core/Src/main.c
66
int main(void) {
67
/* MCU Configuration--------------------------------------------------------*/
```

68

```text
69
/* Reset of all peripherals, Initializes the Flash interface and the Systick. */
70
HAL_Init();
```

71

```text
72
/* Configure the system clock */
73
SystemClock_Config();
```

74

```text
75
/* Initialize all configured peripherals */
76
MX_GPIO_Init();
77
MX_USART2_UART_Init();
```

78

```text
79
/* Infinite loop */
80
while (1)
81
{
82
HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
83
HAL_Delay(500);
84
}
85
}
```

代码本身具有自解释性。首先，通过调用函数 HAL_Init() 来初始化 HAL。然后，初始化时钟、GPIO 和 USART2。最后，应用程序进入一个无限循环：这就是我们放置代码的地方。

外设初始化与去初始化

![Image from PDF page 141](../images/page-0141-image-01.png)

如果你查看文件 Core/Src/stm32XXxx_hal_msp.c，可以找到函数 HAL_UART_MspDeInit() 的定义。与 HAL_UART_MspInit() 函数类似，HAL_UART_MspDeInit() 是由 HAL 函数 HAL_UART_DeInit() 调用的。良好的编程实践是，当不再使用某个外设时，始终对其进行去初始化。对于大多数外设，去初始化过程包括将关联的 GPIO 设置为高阻抗状态（以避免任何形式的电源泄漏），并通过关闭其时钟源来停止任何外设的活动。CubeHAL 的设计旨在正确处理外设的去初始化。

为了保持简单，在本书中展示的大多数示例中，你不会找到适当的去初始化过程。但请记住，在嵌入式编程中，你能控制的越多，出现非预期行为的风险就越小。

```text
Core/Src/syscalls.c
```

ARM GCC，以及由此衍生的整个 STM32 开发环境，依赖于嵌入式系统标准 C 运行时库的一个精简版本（newlib 库）：即所谓的

<!-- page: 142 -->

newlib nano。每次我们为 STM32 微控制器编译固件时，newlib nano 的一部分会与 CubeHAL 和我们的源代码链接在一起。newlib nano 提供了在嵌入式应用程序中使用一些传统 C 库函数的可能性。例如，即使我们的开发板没有提供屏幕或键盘，也完全可以使用经典的 printf()/scanf() I/O 操作函数。然而，newlib nano 的一些函数依赖于更“底层”的例程（称为系统调用或 syscalls），这些例程知道如何处理非常具体的硬件特性。文件 Core/Src/syscalls.c 包含这些例程的虚拟实现：如果没有它们，链接过程将会失败。在后续章节中，我们将看到如何自定义某些 syscalls 以实现更强大和高级的调试功能。我们将分析几种建立开发板与我们主机 PC 之间通信的替代方法，包括使用 Instrumentation Trace Macrocell (ITM)、所谓的 ARM Semihosting 或简单的 UART 通信。Core/Src/sysmem.c

与 syscalls.c 文件类似，此文件包含 _sbrk() 例程的一个完全可用的实现。在基于 UNIX 的环境中，此例程是一个系统调用，用于控制分配给进程数据段（即堆）的内存量。在第 20 章中，我们将深入研究典型 STM32 应用的内存布局。这将使我们理解 _sbrk() 例程背后的逻辑以及如何根据我们的需求对其进行自定义。Drivers

此文件夹包含 CMSIS-CORE 包和 CubeHAL 库。关于 HAL，默认情况下，CubeMX 只会将使用设备配置工具启用的外设所需的文件放入此文件夹及其子文件夹中。相反，CMSIS-CORE 包实现了 Cortex-M 设备的基本运行时系统，并允许用户通过方便的 C 宏访问处理器内核和设备外设。具体而言，它定义了：

- 用于 Cortex-M 处理器寄存器的 HAL，具有 SysTick、NVIC、系统控制块寄存器、MPU 寄存器、FPU 寄存器和内核访问函数的标准化定义。
- 系统异常名称，以便在接口系统异常时避免兼容性问题。
- 组织头文件的方法，使学习新的 Cortex-M 微控制器产品变得容易，并提高软件可移植性。这包括针对特定设备中断的命名约定。
- 供每个 MCU 厂商使用的系统初始化方法。例如，标准化的 SystemInit() 函数对于在设备启动时配置时钟系统至关重要。
- 用于生成标准 C 函数不支持的 CPU 指令的内在函数。
- 一个名为 SystemCoreClock 的全局变量，用于轻松确定系统时钟频率。

CMSIS-CORE 包中最相关的子文件夹是 CMSIS/Include。它包含几个 core_<cpu>.h 文件（其中 <cpu> 被替换为 cm0、cm3 等）。这些文件定义了内核外设，并提供了访问内核寄存器（SysTick、NVIC、ITM、DWT 等）的辅助函数。这些文件对于所有基于 Cortex-M 的 MCU 都是通用的。

<!-- page: 143 -->

```text
Debug
```

此文件夹包含由 Eclipse 和 GCC 编译器生成的所有中间文件（可重定位文件、映射文件等），以获取最终的 ELF 或其他二进制格式的二进制文件。名称 Debug 来自活动的构建配置的名称。构建配置是所有现代 IDE 都支持的功能。它允许在同一个项目内拥有多个项目配置。每个 Eclipse 项目至少有两个构建配置：Debug 和 Release。前者用于生成适合调试的二进制文件。后者用于生成用于生产的优化固件。如果需要，可以安全地完全删除此文件夹。STM32XXxx_FLASH.ld 和 STM32XXxx_RAM.ld

这些文件（_RAM.ld 可能不存在于为某些 STM32 MCU 生成的项目中）是描述我们应用内存布局的链接器脚本。它们定义了 FLASH 和 RAM 内存的数量，并且更重要的是，它们定义了这些内存在运行时如何组织。在第 20 章中，我们将深入研究典型 STM32 应用的内存布局。这将使我们理解这些文件的内容以及如何根据我们的需求对其进行自定义。

## 4.3 下载本书源代码示例

本书中展示的所有示例均可从其 GitHub 仓库下载：http://github.com/cnoviello/mastering-stm32-2nd¹²。

示例按每个 Nucleo 型号进行了划分，如图 4.17 所示。您可以使用 git 命令克隆整个仓库：

```text
$ git clone https://github.com/cnoviello/mastering-stm32-2nd.git
```

或者，您可以按照此链接¹³仅下载仓库内容作为 .zip 包。该仓库分为九个子文件夹，每个文件夹对应本书中用于构建示例的一个 Nucleo 开发板。现在，您需要将适用于您的 Nucleo 的所有 Eclipse 项目导入到 Eclipse 工作区中。

打开 Eclipse 并切换到新的工作区。转到 File->Import…。将出现导入对话框。选择 General->Existing Project into Workspace 条目，然后单击 Next 按钮。现在，通过单击 Browse 按钮浏览到包含您的 Nucleo 示例项目的文件夹。一旦选中主文件夹，将显示其中包含的项目列表。勾选您感兴趣的所有项目，并勾选 Search for nested projects 和 Copy projects into workspace 条目，如图 4.18 所示，然后单击 Finish 按钮。

¹²http://github.com/cnoviello/mastering-stm32-2nd ¹³https://github.com/cnoviello/mastering-stm32-2nd/archive/refs/heads/main.zip

<!-- page: 144 -->

![Image from PDF page 144](../images/page-0144-image-01.jpeg)

图 4.17：包含所有本书示例的 GitHub 仓库内容

![Image from PDF page 144](../images/page-0144-image-02.jpeg)

图 4.18：Eclipse 项目导入向导

### 现在您可以在 Project Explorer 窗格中看到所有已导入的项目。

<!-- page: 145 -->

每个项目都与特定章节相关，该章节中展示的所有示例都位于同一个项目中。要在不同示例之间切换，请选择相应的 Build Configuration，如图 4.19 所示。

![Image from PDF page 145](../images/page-0145-image-01.jpeg)

图 4.19：如何切换到不同的项目配置以选择其他章节的示例

## 4.4 STM32Cube 软件包管理

STM32CubeIDE 允许直接从 IDE 中管理 CubeHAL 软件包和额外的 Cube 扩展包。转到 Help->Manage Embedded Software Packages 可以启动嵌入式软件包管理器，如图 4.20 所示。此工具还允许通过指定本地 ZIP 文件或远程 URL 来手动安装软件包。

```text
请注意，所有 Cube 软件包都位于 Windows 上的 C:\Users\{USERNAME}\STM32Cube\Repository 文件夹
或 MacOS 和 Linux 上的 ∼/STM32Cube/Repository 目录中。请控制此文件夹的内容，因为它可能会占用大量硬盘空间。
```

<!-- page: 146 -->

![Image from PDF page 146](../images/page-0146-image-01.jpeg)

图 4.20：嵌入式软件包管理器
