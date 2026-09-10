<!-- page: 106 -->

# 3. 你好，Nucleo！

没有哪本编程书不是从经典的“Hello world!”程序开始的。本书也将遵循这一传统。在上一章中，我们配置了用于开发 STM32 嵌入式应用的 STM32CubeIDE。因此，我们现在已经准备好开始编写代码了。

在本章中，我们将创建一个非常基础的程序：一个闪烁的 LED。我们将使用 STM32CubeIDE 在几个步骤内创建一个完整的应用程序，在此阶段，我们不会处理与 ST 硬件抽象层（Hardware Abstraction Layer, HAL）以及 MCU 图形配置器（更常被称为 STM32CubeMX）相关的方面。我意识到，本章中介绍的一些细节一开始可能并不清晰，特别是如果你完全是嵌入式编程的新手。然而，这个第一个示例将帮助我们熟悉开发环境。随后的章节，尤其是下一章，将澄清许多晦涩难懂的内容。因此，我建议你保持耐心，并尽力从以下段落中获取最大的收获。

## 3.1 创建项目

让我们创建第一个项目。我们将创建一个简单应用程序，使 Nucleo 上的 LD2 LED（绿色那个）闪烁。转到 File->New->STM32 Project。根据你当前的 IDE 配置，目标选择向导（Target Selection wizard，如图 3.1 所示）将在稍后出现。

![Image from PDF page 106](../images/page-0106-image-01.png)

第一次运行目标选择向导时，可能需要几秒钟才能显示出来。进度指示器会提示你正在从 ST 的服务器获取 MCU 和开发板的规格。新的 STM32 微控制器或开发套件每月都会发布，该工具的设计方式是不内置完整的部件号列表。因此，请耐心等待，让软件完成操作。

正如我们稍后将要学习的，目标选择向导是一个更复杂的软件的一部分，该软件以前被称为 STM32CubeMX。该工具旨在极大地简化特定 STM32 MCU 硬件外设的配置过程，以及生成驱动这些外设所需的所有库文件。下一章将完全基于对 STM32CubeMX 最相关功能的解释。因此，我们现在不会在此事上花费太多时间。

现在点击“Board Selector”选项卡（在图 3.1 中以浅蓝色高亮显示），展开“Type”菜单并勾选 Nucleo-64 系列开发板。在开发板列表中查找你的特定 Nucleo-64 开发板。

<!-- page: 107 -->

![Image from PDF page 107](../images/page-0107-image-01.jpeg)

图 3.1：目标选择向导 - 步骤 1

![Image from PDF page 107](../images/page-0107-image-02.png)

如第 1 章所述，本书完全基于 Nucleo-64 开发板，且文中的示例已在表 1.18 中列出的开发板上进行了测试。然而，本书的目的是教授 STM32 编程的基础概念。我认为，将本文中的此示例及其他所有示例适配到其他任何开发板（Nucleo-32、Nucleo-144、Discovery 等）应该相对容易。

<!-- page: 108 -->

![Image from PDF page 108](../images/page-0108-image-01.jpeg)

图 3.2：项目向导 - 步骤 2

在列表中选中开发板后，点击“Next”按钮。在相应字段中指定项目名称（在我们的情况下是 hello-nucleo，但你可以自由选择最适合你的名称），并保持所有其他标志为默认配置，如图 3.1 所示。点击“Finish”开始生成项目。STM32CubeIDE 会询问你是否希望以默认模式初始化所有外设，如图 3.3 所示。这是什么意思？

![Image from PDF page 108](../images/page-0108-image-02.jpeg)

图 3.3：项目向导 - 步骤 3

在每个开发板上，目标 MCU（即上传固件的主 MCU）既配备了内部外设（例如，实时时钟 - RTC），又通过单独的 GPIO 引脚连接到多个外部其他设备。例如，在每个 Nucleo-64 开发板上，一个 GPIO 直接连接到标记为 PCB 上 LD2 的绿色 USER LED。要使用这些“默认”外设，我们必须正确配置内部外设和相应的 GPIO。通过回答“是”，我们指示 IDE 自动执行所有必要的配置，以使用 Nucleo-64 开发板的所有内部和外部默认外设。随着我们深入本书，你将学习如何自行配置每个外设。然而，在此阶段，为了保持简单，点击“是”，让 IDE 施展魔法。

STM32CubeIDE 将开始生成新项目。如果这是你第一次为你的 Nucleo 开发板的 STM32 系列（即 STM32F0、STM32F4 等）创建项目，IDE 需要下载相应的 Cube 固件包（例如，如果你的开发板是 Nucleo-F401RE，则需要下载 STM32F4 系列的 stm32cube_fw_f4_v1XXX.zip 包）。

<!-- page: 109 -->

这些包包含几个相关组件：

- 给定 STM32 系列的完整 HAL：硬件抽象层（Hardware Abstraction Layer, HAL）是一组允许驱动微控制器外设和内核功能而无需处理特定 MCU 细节的库。本书完全基于 STM32CubeHAL，我们将学习关于这个相当复杂的库的许多内容。
- 额外的中间件包：一些 STM32 MCU 集成了高级外设，需要使用额外的库（由 ST 或第三方开发）。例如，要编程某些 STM32 MCU 中集成的 USB 控制器，必须使用 ST 免费提供的完整 USB 协议栈。每个 Cube 固件包都附带一组中间件库，我们将在本书的第三部分分析其中几个。
- 开发板的示例项目：ST 为其开发板提供了许多完整且可运行的示例。每个示例都旨在展示如何使用开发板的特定功能。每个 Cube 固件包集成了多个示例，你可以通过点击目标选择向导中的“Example Selector”选项卡（见图 3.1）来浏览完整的示例列表。

![Image from PDF page 109](../images/page-0109-image-01.jpeg)

图 3.4：Cube 固件包下载对话框

根据 STM32 系列的不同，Cube 固件包的大小可能相当大。基本规则是，STM32 系列越强大，相应的 Cube 固件就越大。因此，请耐心等待完整的下载，如特定对话框所示（见图 3.4）。

## 3.2 向生成的代码中添加有用的内容

图 3.5 展示了项目生成后在 STM32CubeIDE 中显示的内容。项目资源管理器（Project Explorer）视图显示了项目结构。这是一级文件夹的内容（从上到下）¹：

```text
Includes
```

此文件夹显示了所有属于 GCC 包含文件夹（Include Folders）² 的文件夹。

¹我们不会在此处描述所有生成的文件和文件夹。这只是一个简要介绍。在后续章节中，我们将有机会更好地分析它们。现在不要在上面花太多时间。 ²每个 C/C++ 编译器都需要知道在哪里查找包含文件（以 .h 结尾的文件）。这些文件夹被称为包含文件夹（或更准确地说是包含路径），并且必须使用 -I 参数向 GCC 指定其路径。然而，Eclipse 可以自动为我们完成此操作，并且包含文件夹在视觉上显示了 GCC 将查找包含文件的搜索路径。

<!-- page: 110 -->

```text
Core
```

此 Eclipse 文件夹包含生成的项目，由构成我们应用程序的几个 .c 文件组成。其中一个文件是 src/main.c，其中包含我们稍后将进行定制的 int main(void) 例程。Drivers

此 Eclipse 文件夹通常包含许多相关库的头文件和源文件（例如，ST CubeHAL 和 CMSIS 包）。我们将在下一章中更深入地了解它们。hello-nucleo.ioc

此文件是在设备配置工具（Device Configuration Tool）视图中图形化显示的 STM32CubeMX 项目（项目生成后的默认主视图，如图 3.5 所示）。我们将在下一章中深入分析 STM32CubeMX 的界面和功能。

![Image from PDF page 110](../images/page-0110-image-01.jpeg)

图 3.5：完整项目生成后的 STM32CubeIDE 界面

我们现在准备好开始处理真正的核心应用程序了。IDE 生成的项目自动包含构建自洽应用程序所需的所有代码。为了让 LD2 LED 闪烁，我们只需要在 main() 函数中添加两行代码，该函数是我们自定义应用程序的入口点³。因此，在项目资源管理器窗格中，展开 Core->Src 文件夹并双击 main.c 文件。转到大约第 66 行，在那里你可以找到 main() 函数的定义。在这里你可以找到

³经验丰富的 STM32 程序员知道，说 main() 函数是 STM32 应用程序的入口点是不恰当的。固件的执行开始得早得多，从调用一些重要的设置例程开始，这些例程为固件创建执行环境。然而，从应用程序的角度来看，其起点在 main() 函数内部。后续章节将详细展示 STM32 微控制器的引导过程。

<!-- page: 111 -->

四个例程⁴ 的调用：

- HAL_Init()：此函数初始化 CubeHAL 框架。它负责 MCU 的最初初始化。我们将在书中稍后分析此函数。
- SystemClock_Config()：此函数起着真正关键的作用，因为它配置 MCU 以使用可能的时钟源之一工作。STM32 MCU 提供了使用几种不同时钟源的可能性。这是一个高级主题，我们将在第 10 章中深入探讨。
- MX_GPIO_Init()：此函数根据在 STM32CubeMX 中完成的图形化配置初始化 I/O 引脚。在我们的情况下，它将配置与 LD2 LED 关联的 GPIO 引脚。关于这些主题的更多信息见第 6 章。
- MX_USART2_UART_Init()：此函数初始化 UART2 外设，该外设在所有 Nucleo 板上都连接到 ST-LINK 接口。关于此主题的更多信息见第 8 章。

紧接着这四个初始化例程的调用之后，你可以找到一个 while 循环，这是一个无限循环，所有固件活动都在其中发生。在这里你可以添加两个函数调用，如下所示在第 101-102 行。

```text
Filename: src/main.c
66
int main(void)
67
{
68
/* USER CODE BEGIN 1 */
```

69

```text
70
/* USER CODE END 1 */
```

71

```text
72
/* MCU Configuration--------------------------------------------------------*/
```

73

```text
74
/* Reset of all peripherals, Initializes the Flash interface and the Systick. */
75
HAL_Init();
```

76

```text
77
/* USER CODE BEGIN Init */
```

78

```text
79
/* USER CODE END Init */
```

80

```text
81
/* Configure the system clock */
82
SystemClock_Config();
```

83

```text
84
/* USER CODE BEGIN SysInit */
```

85

```text
86
/* USER CODE END SysInit */
```

87

```text
88
/* Initialize all configured peripherals */
89
MX_GPIO_Init();
```

⁴根据你的开发板，特别是如果你没有使用 Nucleo-64，你可能会发现 main() 函数内部调用了额外的例程。这意味着你的开发板提供了比标准 Nucleo-64 板更多的外设（请记住，当 STM32CubeIDE 询问我们是否要自动初始化所有外设时，我们回答了“是”。因此，如果你的 main() 与这里显示的略有不同，请不要太在意。

<!-- page: 112 -->

```text
90
MX_USART2_UART_Init();
91
/* USER CODE BEGIN 2 */
```

92

```text
93
/* USER CODE END 2 */
```

94

```text
95
/* Infinite loop */
96
/* USER CODE BEGIN WHILE */
97
while (1)
98
{
99
/* USER CODE END WHILE */
100
/* USER CODE BEGIN 3 */
101
HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
102
HAL_Delay(500);
103
}
104
/* USER CODE END 3 */
```

你会注意到，由 CubeMX 生成的代码充满了这些注释区域：

![Image from PDF page 112](../images/page-0112-image-01.png)

```text
/* USER CODE BEGIN 1 */
...
/* USER CODE END 1 */
```

这些注释是做什么用的？CubeMX 的设计使得如果你更改硬件配置，你可以重新生成项目代码而不会丢失你添加的代码片段。将你的代码放在这些“受保护区域”内应该能保证你不会丢失你的工作。然而，我必须承认，有时 CubeMX 可能会把生成的文件搞得一团糟，用户代码会丢失。因此，我建议始终生成另一个独立的项目，并将更改的代码复制粘贴到应用程序文件中。这也让你完全控制你的代码。

代码应该是自解释的。HAL_GPIO_TogglePin() 函数简单地反转连接到 LD2 LED 的 PIN 的逻辑状态（这对应于所有 Nucleo-64 板上 GPIO 端口 A 的 PIN 5），而 HAL_Delay() 函数只是一个持续 500ms 的忙等待自旋：因此 LD2 将以 1HZ 的频率闪烁。

<!-- page: 113 -->

![Image from PDF page 113](../images/page-0113-image-01.png)

我们如何知道 LED 连接到哪个引脚？ST 提供了 Nucleo 板的原理图⁵。原理图是使用 Altium Designer CAD 制作的，这是一种在专业世界中使用的相当昂贵的软件。然而，幸运的是，ST 提供了一个包含原理图的方便 PDF。查看第 4 页，我们可以看到 LED 连接到 PA5 引脚⁶，如图 3.6 所示。

![Image from PDF page 113](../images/page-0113-image-02.jpeg)

图 3.6：LD2 连接到 PA5

PA5 是 GPIOA 端口 PIN5 的缩写，这是在 STM32 世界中指示 GPIO 的标准方式。最后，STM32CubeMX 自动定义宏 LD2_GPIO_Port 和 LD2_Pin，以便它们的展开对应于 GPIOA 端口和 PIN5。

### 现在我们可以编译项目了。转到菜单 Project->Build Project。过一会儿，我们应该会在输出控制台⁷中看到类似以下内容。

```text
arm-none-eabi-size
hello-nucleo.elf
arm-none-eabi-objdump -h -S
hello-nucleo.elf
> "hello-nucleo.list"
arm-none-eabi-objcopy
-O binary
hello-nucleo.elf
"hello-nucleo.bin"
text
data
bss
dec
hex
filename
8224
20
1636
9880
2698
hello-nucleo.elf
Finished building: default.size.stdout
Finished building: hello-nucleo.bin
Finished building: hello-nucleo.list
15:22:52 Build Finished. 0 errors, 0 warnings. (took 5s.769ms)
```

⁵http://bit.ly/1FAVXSw ⁶除了 Nucleo-F302RB 之外，其 LD2 连接到 PB13 端口。稍后会有更多介绍。⁷每个二进制段（text、bss 等）所需的字节数可能与你的不同。这是因为不同 STM32 系列之间的 HAL 存在差异，以及编译器优化级别不同所致。请不要关注这些细节，稍后它们会变得清晰得多。

<!-- page: 114 -->

## 3.3 将 Nucleo 连接到 PC

一旦我们编译了测试项目，就可以使用连接到 micro-USB 端口（在图 3.7 中称为 VCP）的 USB 线将 Nucleo 板连接到你的计算机。你应该至少能看到两个 LED 亮起。

仔细阅读

![Image from PDF page 114](../images/page-0114-image-01.png)

请确保 USB 端口能够为板卡提供足够的电力。强烈建议使用能够提供至少 500mAh 的 USB 端口或自供电的外部集线器。

![Image from PDF page 114](../images/page-0114-image-02.jpeg)

图 3.7：Nucleo 板及其主要接口

第一个是 LD1 LED，在图 3.7 中标记为 ST-LINK LED。它是一个红/绿 LED，用于指示 ST-LINK 的活动状态：一旦板卡连接到计算机，该 LED 为绿色；在调试会话期间或向 MCU 上传固件时，它会交替闪烁绿色和红色。

另一个在板卡连接到计算机时会点亮的 LED 是 LD3，在图 3.7 中标记为 POWER LED。它是一个红色 LED，当 USB 端口完成枚举时点亮，即 ST-LINK 接口被计算机操作系统正确识别为 USB 外设。板卡上的目标 MCU 仅在该 LED 点亮时才通电（这意味着 ST-LINK 接口还负责管理目标 MCU 的供电）。

最后，如果你还没有用自定义固件刷写你的板卡，你会看到 LD2 LED，即图 3.7 中标记为 USER LED 的绿色 LED，也在闪烁：这是因为 ST 预加载了

<!-- page: 115 -->

一个使 LD2 LED 闪烁的固件。你可以通过按下图 3.7 中标记为 USER BTN 的开关（蓝色那个）来改变闪烁频率。

我们稍后会将板载固件替换为我们之前制作的那个。在继续这一步之前，重要的是要确保我们 Nucleo 板上的 ST-LINK 调试器配备了最新的 ST-LINK 2.1 固件。

### 3.3.1 ST-LINK 固件升级

警告

![Image from PDF page 115](../images/page-0115-image-01.png)

请仔细阅读本段。不要跳过这一步！

我购买了几块 Nucleo 板，发现所有板卡通常都带有相当旧的 ST-LINK 固件。为了使用最新的 STM32CubeIDE，固件必须至少更新到 V2J37.x 版本。

升级过程可以很容易地通过 STM32CubeIDE 完成。使用 USB 线连接你的 Nucleo 板，然后转到 Help->ST-LINK Upgrade。ST-LINK Upgrade 程序会出现，如图 3.8 所示。

![Image from PDF page 115](../images/page-0115-image-02.jpeg)

图 3.8：ST-LINK Upgrade 程序

点击 Refresh device list：连接的板卡应被识别为 ST-LINK/V2-1。点击 Open in update mode。ST-LINK Upgrade 将显示你的 Nucleo 固件是否需要更新（指出不同的版本，如图 3.8 所示）。如果需要，点击 Upgrade 按钮并等待固件更新完成。

<!-- page: 116 -->

ST-LINK 固件升级错误

![Image from PDF page 116](../images/page-0116-image-01.png)

当你点击 Open in update mode 按钮时，上述过程可能会失败。STLinkUpgrade 工具可能会显示错误信息 Error connecting to device ST-LINK/V2- 1 (error 0x1); check the USB connection and refresh device list，即使板卡已正确连接到 PC。这通常是由于板卡供电不足造成的。尝试使用自供电 USB 集线器或使用另一个 USB 端口。在最近的 iMac 上，如果通过集成 USB 端口的 Apple 键盘连接板卡，这种错误相当常见。

## 3.4 使用 STM32CubeProgrammer 刷写 Nucleo

我们在第 2 章中安装了 STM32CubeProgrammer，现在我们将使用它。启动程序并使用 USB 线将你的 Nucleo 连接到 PC。点击图 3.9 中用红圈圈出的刷新按钮。一旦 STM32CubeProgrammer 识别了板卡，其序列号将出现在 Serial number 框中，如图 3.9 所示。

![Image from PDF page 116](../images/page-0116-image-02.jpeg)

图 3.9：STM32CubeProgrammer 工具显示的 ST-LINK 接口序列号

仔细阅读

![Image from PDF page 116](../images/page-0116-image-03.png)

如果显示的是标签 “Old ST-LINK Firmware” 而不是 ST-LINK 接口的序列号，那么你需要将 ST-LINK 固件更新到最新版本。点击 ST-LINK Configuration 窗格底部的 Firmware upgrade 按钮，并按照上一段中报告的相同说明进行操作。

一旦识别了 ST-LINK 板卡，点击 Connect 按钮。过一会儿，你将看到闪存的内容，如图 3.10 所示。好的，让我们最终将示例固件上传到板卡。点击 Erase & programming 图标（左侧第二个绿色图标）。然后，点击 File programming 中的 Browse 按钮。进入你的 Eclipse 工作区目录（默认情况下，在 Windows 中路径为 %HOMEPATH%\STM32CubeIDE\workspace_1.X.0，在 Linux 和 Mac OS 中为 ∼/STM32CubeIDE7workspace_- 1.X.0，其中 1.X.0 对应你的 STM32CubeIDE 的确切版本）。然后进入 hello_nucleo\Debug 子文件夹，选择名为 hello_nucleo.elf 的文件。勾选 Verify programming 和 Run after programming 标志，然后点击 Start Programming 按钮开始刷写。刷写过程结束后，你的 Nucleo 绿色 LED 将开始闪烁。

<!-- page: 117 -->

### 恭喜：欢迎来到 STM32 世界 ;-)

![Image from PDF page 117](../images/page-0117-image-01.jpeg)

图 3.10：连接到 Nucleo 开发板时的 STM32CubeProgrammer 界面

<!-- page: 118 -->

Eclipse 插曲

Eclipse 允许我们在源代码中轻松导航，而无需手动在源文件之间跳转以查找函数定义的位置。例如，假设我们想查看函数 MX_GPIO_Init() 的代码实现。要跳转到其定义处，请高亮显示该函数调用，右键单击并选择“Open declaration entry”，如下面的图像所示。

![Image from PDF page 118](../images/page-0118-image-01.jpeg)

或者，您可以按住 Ctrl 键（在 MacOS 上为 CMD⌘）同时单击给定的符号。此外，在符号导航过程中，可以使用 Eclipse 工具栏上的两个专用按钮在已打开的源文件之间进行导航，如下所示。

![Image from PDF page 118](../images/page-0118-image-02.jpeg)

Eclipse 的另一个有趣功能是能够展开复杂的宏。例如，右键单击一个宏并选择“Explore macro expansion”条目。随后将出现如下上下文窗口。

![Image from PDF page 118](../images/page-0118-image-03.png)

有时，Eclipse 会使其索引文件混乱，导致无法在源代码中进行导航。为了解决这个问题，您可以前往 Project->C/C++ Index->Rebuild 菜单，强制 Eclipse 重建其索引。
