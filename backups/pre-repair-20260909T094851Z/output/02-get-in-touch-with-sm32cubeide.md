<!-- page: 92 -->

### 2.1.1 关于 Eclipse 的两句闲话…

Eclipse³ 是一款开源且免费的基于 Java 的集成开发环境（IDE）。尽管存在这一事实（不幸的是，Java 程序往往消耗大量机器资源并导致你的 PC 变慢），Eclipse 仍然是最普及且最完整的开发环境之一。Eclipse 提供多种预配置版本，针对特定用途进行了定制。例如，面向 Java 开发者的 Eclipse IDE 预配置了与 Java 以及该开发平台中使用的各种工具（如 Ant、Maven 等）协同工作的能力。在我们的案例中，STM32CubeIDE 本质上基于面向 C/C++ 开发者的 Eclipse IDE。

Eclipse 被设计为可通过插件进行扩展。Eclipse Marketplace 中有多个可用于嵌入式系统软件开发的插件。我们将在本书中安装并使用其中大部分插件。此外，Eclipse 具有高度的可定制性。我强烈建议你查看其设置，以便根据你的需求和偏好进行适配。

### 2.1.2 …以及 GCC

GNU 编译器集合⁴（GCC）是一套完整且广泛使用的编译器套件。它是唯一能够编译多种编程语言（前端）并生成数十种硬件架构（具有多种变体）代码的开发工具。GCC 是一个真正复杂的软件。它提供了多种工具以完成编译任务。除了编译器本身外，这些工具还包括汇编器、链接器、调试器（即 GNU Debugger - GDB），以及用于二进制文件检查、反汇编和优化的多种工具。此外，GCC 还配备了针对目标架构定制的 C 语言运行时环境。

近年来，多家公司，甚至是在嵌入式领域，都采用了 GCC 作为其官方编译器。例如，NXP 使用 GCC 作为其 LPC 系列 Cortex 微控制器的交叉编译器。

³http://www.eclipse.org ⁴https://gcc.gnu.org/

<!-- page: 93 -->

什么是交叉编译器？

![Image from PDF page 93](../images/page-0093-image-01.png)

我们通常将编译器一词指代为能够为我们 PC 中的处理器生成机器码的工具。编译器仅仅是一个从特定编程语言（在我们的案例中是 C 语言）到低级机器语言（也称为汇编语言）的“语言翻译器”。例如，如果我们在 Intel x86 机器上工作，我们使用编译器从 C 编程语言生成 x86 汇编代码。为了完整性，我们必须指出，如今编译器是一个更复杂的工具，它同时针对特定的目标硬件处理器和我们正在使用的操作系统（例如 Windows 7）。

跨平台编译器是一种能够生成与用于开发应用程序的机器不同的硬件机器机器码的编译器。在我们的案例中，GCC ARM Embedded 编译器在 x86 机器上（使用特定的操作系统，例如 Windows 或 Mac OSX）编译时，为 Cortex-M 处理器生成机器码。

在 ARM 领域，GCC 是最常用的编译器，这主要归因于它被用作 ARM Cortex-A 处理器（装备几乎每个移动设备的 ARM 微控制器）基于 Linux 的操作系统的主要开发工具。ARM 工程师积极维护 GCC 的 ARM GCC 分支。STM32CubeIDE 使用了基于 GCC 的最新工具链之一。最后，请考虑获取关于这套编译器的知识在未来也可能有用：这是一项可以复用于其他嵌入式架构的技能。

## 2.2 下载和安装 STM32CubeIDE

可以从官方 STM 网站⁵免费下载 STM32CubeIDE。唯一的要求是你在 STM 网站注册并提供一个有效的电子邮件地址。

在同一个网页上，你可以找到所有操作系统的安装包。你会找到五个链接，如图 2.1⁶所示。三个链接与 Linux 相关，另外两个分别用于 Windows 和 MacOS：

- STM32CubeIDE-Win：此可执行包包含 Windows 的安装程序。
- STM32CubeIDE-Mac：此 ZIP 文件包含带有 Mac OSX 安装程序的 DMG 文件（Apple Disk Image）。
- STM32CubeIDE-DEB：此包包含 Linux Debian 安装包（.deb 包）。这适用于 Linux Debian 发行版及其衍生版本（特别是 Ubuntu）。
- STM32CubeIDE-RPM：此包包含 Linux RedHat 安装包（.rpm 包）。这适用于 Linux RedHat 发行版及其衍生版本（特别是 CentOS）。
- STM32CubeIDE-Lnx：这是一个通用的 Linux tarball，包含 STM32CubeIDE 以及所有必要的工具和库。此包适用于高级 Linux 用户，他们通常知道如何自行安装自定义应用程序。

⁵https://www.st.com/en/development-tools/stm32cubeide.html ⁶在本书中，除非另有要求，所有屏幕截图均基于 Mac OS，因为这是作者用于开发 STM32 应用程序（以及撰写本书）的操作系统。然而，它们也适用于其他操作系统。

<!-- page: 94 -->

在下载部分点击粉色图标“Get Software”，选择适用于你操作系统的 STM32CubeIDE 移植版本。软件下载完成后，请按照下一节中的说明进行操作。

![Image from PDF page 94](../images/page-0094-image-01.jpeg)

图 2.1：官方 STM 网站上的 STM32CubeIDE 下载页面

![Image from PDF page 94](../images/page-0094-image-02.png)

接下来的三段及其子段落几乎相同。它们仅在特定于给定操作系统（Windows、Linux 或 Mac OS）的部分有所不同。因此，请跳转到你感兴趣的段落，并跳过其余部分。

### 2.2.1 Windows - 安装工具链

Windows 安装包包含在一个 ZIP 文件中。下载完成后，解压 ZIP 归档文件并运行其中包含的可执行文件（可执行文件名结构为：st-stm32cubeide_VERSION_x86_64.exe，其中 VERSION 对应 IDE 的最新发布版本）。在安装过程中，Windows 可能会显示一个对话框，内容为：“是否允许此应用对你的设备进行更改？”，并显示信息“已验证的发布者：STMicroelectronics Software AB”。点击“是”以接受并让安装程序继续。

<!-- page: 95 -->

![Image from PDF page 95](../images/page-0095-image-01.jpeg)

图 2.2：Windows 安装程序欢迎页面

几秒钟后，安装程序的“欢迎使用……”页面将出现，如图 2.2 所示。点击“下一步”，阅读许可协议并点击“我同意”以接受协议条款。在下一个对话框中（见图 2.3），可以选择安装位置。建议选择较短的路径，以避免因工作区路径过长而遇到 Windows 的限制。我的建议是保留默认路径（C:\ST\STM32CubeIDE）。

![Image from PDF page 95](../images/page-0095-image-02.jpeg)

图 2.3：选择安装位置对话框

<!-- page: 96 -->

![Image from PDF page 96](../images/page-0096-image-01.png)

独立项目不会存储在该路径内。相反，它们被分组在一个名为“工作区”的首选位置中。这是 Eclipse 存储项目的通用方式，好消息是你可以拥有任意数量的工作区：每个工作区代表一个完全独立的环境，无论是从存储项目的角度来看，还是从 IDE 配置的角度来看。这意味着你可以根据具体需求自定义每个工作区。每个项目、每个已安装的插件、每个 IDE 和工具配置都将局限于该特定工作区。这对初学者也非常有用：弄乱 IDE 配置并破坏一些重要配置的情况并不罕见。如果发生这种情况，你只需丢弃当前工作区并创建一个新的工作区，而不会影响整体系统配置。

选择安装路径后，点击“下一步”。将显示“选择组件”对话框，如图 2.4 所示。除非你对这些选项非常熟悉，否则我的建议是保持所有选项均被勾选。随着本书内容的推进，这些组件的作用将变得更加清晰。点击“安装”按钮并等待操作完成。在此步骤中，安装程序会将 IDE 及所有相关组件复制到所选位置：Java 虚拟机、Eclipse 及其所有插件、GCC 编译器和调试器、用于 ST-LINK 调试器的 Windows 驱动程序。

![Image from PDF page 96](../images/page-0096-image-02.jpeg)

图 2.4：选择组件对话框

安装步骤结束后，点击“完成”。

下一个需要安装的工具是 STM32CubeProgrammer。它是一个软件，用于通过我们 Nucleo 板上的 ST-LINK 接口或专用的 ST-LINK 编程器将固件上传到 MCU。除了下一章之外，我们在书中不会过多使用这个工具。然而，在常见的开发生命周期中，尤其是在小批量生产时，这个工具经常派上用场。因此，我认为熟悉这个工具是合理的。

你可以从 ST 官方页面⁷下载 STM32CubeProgrammer（下载链接位于页面底部的“获取软件”部分）。下载完成后，解压

⁷http://bit.ly/2CK4aFa

<!-- page: 97 -->

.zip 包。你将找到 SetupSTM32CubeProgrammer-2.9.0.exe 文件。运行它并按照安装说明操作。

工具链的安装现已完成，如果你是 Eclipse IDE 的完全新手，可以跳转到 STM32CubeIDE 概述段落。

### 2.2.2 Linux - 安装工具链

整个安装过程将假设满足以下要求：

- 一台运行最新 Linux-64 位版本的 PC：

- – Ubuntu Linux 20.04 LTS Desktop 或更高版本 – Fedora 29 或更高版本
- 足够的硬件资源（建议至少拥有 4Gb 内存和硬盘上 20Gb 的可用空间）；这些说明应能轻松适配其他 Linux 发行版。

安装程序以不同的捆绑包形式提供，以适应各种 Linux 发行版。捆绑包的命名为 st-stm32cubeide_VERSION_ARCHITECTURE.PACKAGE，其中：

- VERSION 是实际的产品版本和构建日期（例如：1.0.0_2026_20190221_1309）
- ARCHITECTURE 是运行 STM32CubeIDE 的目标主机计算机的架构（例如：amd64）
- PACKAGE 是要安装的 Linux 包类型。支持的包包括：

– rpm_bundle.sh 用于 Fedora/CentOS – deb_bundle.sh 用于 Ubuntu/Debian – .sh 用于通用 Linux

请按以下步骤操作：

1. 在主机计算机上使用命令控制台导航到安装文件所在的位置。 2. 在控制台窗口中输入以下命令：

```text
1
$ sudo sh ./st-stm32cubeide_VERSION_ARCHITECHURE.PACKAGE
```

其中 VERSION、ARCHITECTURE 和 PACKAGE 必须根据所选的 Linux 包进行输入。

3. 按照控制台窗口中提供的进一步说明操作。

下一个需要安装的工具是 STM32CubeProgrammer。它是一个软件，用于通过我们 Nucleo 板上的 ST-LINK 接口或专用的 ST-LINK 编程器将固件上传到 MCU。除了下一章之外，我们在书中不会过多使用这个工具。然而，在常见的开发生命周期中，尤其是在小批量生产时，这个工具经常派上用场。因此，我认为熟悉这个工具是合理的。

要在 Linux 上执行 STM32CubeProgrammer，要求你的机器上已安装某些包。所需的包是：

<!-- page: 98 -->

```text
• libusb-1.0.0-dev
```

该包的安装方式因具体的 Linux 发行版而异。在 Ubuntu 中，可以在终端提示符下使用以下命令进行安装：

```text
$ sudo apt-get install libusb libusb-1.0.0-dev
```

你可以从 ST 官方页面⁸下载 STM32CubeProgrammer（下载链接位于页面底部的“获取软件”部分）。下载完成后，解压 .zip 包。你将找到 SetupSTM32CubeProgrammer-2.9.0.linux 文件。运行它并按照安装说明操作。

如果你是 Eclipse IDE 的完全新手，可以跳转到 STM32CubeIDE 概述段落。

### 2.2.3 Mac - 安装工具链

MacOS 安装包包含在一个 ZIP 文件中。下载完成后，解压 ZIP 归档文件并运行其中的 DMG 文件（文件名结构为：ststm32cubeide_VERSION_x86_64.dmg，其中 VERSION 对应 IDE 的最新发布版本）。双击 DMG 文件以让 MacOS 挂载 Apple 磁盘映像。随后会出现许可协议对话框，如图 2.5 所示。

![Image from PDF page 98](../images/page-0098-image-01.jpeg)

图 2.5：许可协议对话框

阅读许可协议并点击“同意”以接受协议条款并继续软件安装。随后会出现安装页面，如图 2.6 所示。在将大型 IDE 图标拖入应用程序文件夹之前，重要的是先安装 ST-LINK 服务器包。因此，点击“Install me 1st”图标（MacOS 中代表软件包的经典图标）并按照安装说明进行操作。

⁸http://bit.ly/2CK4aFa

<!-- page: 99 -->

![Image from PDF page 99](../images/page-0099-image-01.png)

MacOS 会阻止你安装该软件，因为它来自不受信任的网站，而非官方 App Store。不过，我假设你对 MacOS 足够熟悉，能够通过进入 MacOS 系统偏好设置 -> 安全性与隐私设置来绕过此限制。或者，你可以通过在 MacOS 终端中运行以下命令来完全禁用 MacOS Gatekeeper（该组件负责强制代码签名，并在最近的 MacOS 版本中允许运行之前验证下载的应用程序）：

```text
$ sudo spctl --master-disable
```

完成后，你可以安全地将 IDE 图标拖入应用程序文件夹，并等待操作完成。

![Image from PDF page 99](../images/page-0099-image-02.jpeg)

图 2.6：安装页面对话框

<!-- page: 100 -->

请仔细阅读！

![Image from PDF page 100](../images/page-0100-image-01.png)

MacOS 用户在首次启动应用程序时经常无法运行 STM32CubeIDE。此时会显示以下系统警告：

![Image from PDF page 100](../images/page-0100-image-02.jpeg)

不幸的是，此错误是由于错误的扩展属性权限造成的，这主要与 MacOS X 的新路径有关，这正推动 MacOS 向某种更高级的 iOS 发展。诚实地说，作为一个非常资深且高级的 MacOS 用户，我看不到这种转变有任何好处。然而，好消息是你可以通过打开 MacOS 终端并在提示符下执行以下命令轻松解决此问题：

```text
$ xattr -c /Applications/STM32CubeIDE.app
```

这应该能修复该问题，并且你应该能够运行 STM32CubeIDE。

下一个要安装的工具是 STM32CubeProgrammer。它是一个软件，用于通过我们 Nucleo 的 ST-LINK 接口或专用的 ST-LINK 编程器将固件上传到 MCU。除了下一章之外，我们在书中不会太多使用这个工具。然而，这个工具在常见的开发生命周期中经常派上用场，特别是对于小批量生产。因此，我认为熟悉这个工具是合理的。

你可以从 ST 官方页面⁹下载 STM32CubeProgrammer（下载链接位于页面底部的“获取软件”部分）。下载完成后，解压 .zip 包。你会找到 SetupSTM32CubeProgrammer-2.9.0.app 文件。运行它并按照安装说明进行操作。

工具链安装已完成，如果你是 Eclipse IDE 的新手，可以跳转到下一段。

## 2.3 STM32CubeIDE 概述

现在我们已经完成了工具链的安装，我们可以初步查看其主要界面和功能。

⁹http://bit.ly/2CK4aFa

<!-- page: 101 -->

当你启动 Eclipse 时，系统会要求你指定一个工作区目录，如图 2.7 所示。你可以自由地将此文件夹指向硬盘上的任何位置。

![Image from PDF page 101](../images/page-0101-image-01.jpeg)

图 2.7：Eclipse 工作区选择对话框

工作区是磁盘上的一个目录，Eclipse 平台以及所有已安装的插件在此存储偏好设置、配置和临时信息。后续的 Eclipse 调用将使用此存储来恢复之前的状态。顾名思义，它是你的“工作空间”。它定义了你在 Eclipse 会话期间的关注区域。除了 IDE 配置参数外，工作区也是属于给定工作区的所有项目的仓库。

拥有多个工作区主要是程序员的个人选择，他们可以根据个人需求组织项目和 IDE 配置。如果你不打算拥有多个工作区，可以勾选“Use this as the default and do not ask again”（使用此作为默认值且不再询问）标志。Eclipse 将在启动时自动打开该工作区。

![Image from PDF page 101](../images/page-0101-image-02.png)

任何时候，如果你改变主意并想切换到新的工作区，你可以通过点击 File->Switch workspace->Other…（文件->切换工作区->其他…）来覆盖默认配置。图 2.7 中的对话框将再次出现，你将能够选择不同的工作区。

设置好默认工作区位置后，点击 Launch（启动）按钮，并等待 Eclipse 完全启动。

当你启动 STM32CubeIDE 时，如果你是 Eclipse 的新手，可能会对其界面感到有些困惑。图 2.8 显示了 Eclipse 首次启动时的外观。

<!-- page: 102 -->

![Image from PDF page 102](../images/page-0102-image-01.png)

图 2.8：Eclipse 首次启动后的界面

Eclipse 是一个多视图 IDE，其组织方式使得所有功能都显示在一个窗口中，但用户可以自由地根据自己的需求安排界面。当 Eclipse 启动时，会显示一个欢迎屏幕。该欢迎选项卡的内容称为视图（view）。

![Image from PDF page 102](../images/page-0102-image-02.jpeg)

图 2.9：通过点击 X 关闭欢迎视图。

要关闭欢迎视图，请点击交叉图标，如图 2.9 所示。一旦欢迎视图消失，C/C++ 透视图（perspective）就会出现，如图 2.10 所示。

<!-- page: 103 -->

![Image from PDF page 103](../images/page-0103-image-01.jpeg)

图 2.10：Eclipse 中的 C/C++ 透视图（稍后加载了 main.c 文件）

如果你想要重新显示欢迎视图，请点击主工具栏上红圈标出的图标，如下图所示。

![Image from PDF page 103](../images/page-0103-image-02.png)

![Image from PDF page 103](../images/page-0103-image-03.jpeg)

在 Eclipse 中，透视图（perspective）是一种以与透视图功能相关的方式排列视图的方法。C/C++ 透视图专门用于编码，它展示了与源代码编辑及其编译相关的所有方面。它分为四个视图。

左侧名为 Project Explorer（项目资源管理器）的视图显示了工作区内的所有项目。居中的视图，也是最大的一个，是 C/C++ 编辑器。每个源文件显示为一个选项卡，可以同时打开多个选项卡。

Eclipse 窗口底部的视图专门用于与编译相关的多种活动，它们被细分为选项卡。例如，Console（控制台）选项卡显示编译器的输出；

<!-- page: 104 -->

Problems（问题）选项卡以方便检查的方式组织来自编译器的所有消息；Search（搜索）选项卡包含搜索结果。

右侧的视图包含其他几个选项卡。例如，Outline（大纲）选项卡显示每个源文件中包含的符号（函数、变量等），允许在文件内容中快速导航。

还有其他可用的视图（以及许多由自定义插件提供的视图）。用户可以通过进入 Window->Show View->Other… 菜单来查看它们。其中一些将在后续章节中进行分析。

![Image from PDF page 104](../images/page-0104-image-01.png)

有时，某个视图会被“最小化”，看起来像是从 IDE 中消失了。对于刚接触 Eclipse 的用户来说，这可能会让人困惑，不知道它去了哪里。例如，查看图 2.11 时，似乎 Project Explorer 视图已经消失，但它只是被最小化了，你可以点击红色圆圈标记的图标来恢复它。然而，有时视图确实已被关闭。这种情况发生在该视图中只有一个活动标签页且我们将其关闭时。在这种情况下，你可以进入 Window->Show View->Other… 菜单重新启用该视图。

![Image from PDF page 104](../images/page-0104-image-02.jpeg)

图 2.11：最小化的 Project Explorer 视图

要在不同的透视（Perspective）之间切换，你可以使用 Eclipse 右上角提供的专用工具栏（见图 2.12）。

![Image from PDF page 104](../images/page-0104-image-03.jpeg)

图 2.12：透视切换工具栏

默认情况下，另一个可用的透视是 Debug（调试），我们将在后面更详细地介绍。你可以通过进入 Window->Perspective->Open Perspective->Other… 菜单来启用其他透视。

<!-- page: 105 -->

![Image from PDF page 105](../images/page-0105-image-01.png)

从 Eclipse 4.6（又称 Neon）开始，透视切换工具栏默认不再显示透视名称，仅显示与透视关联的图标。这往往会令初学者感到困惑。你可以右键点击工具栏并选择 Show Text 选项，以在图标附近显示透视名称，如下所示。

![Image from PDF page 105](../images/page-0105-image-02.jpeg)

Eclipse IDE 设计有一个主工具栏，其内容会根据主透视视图中选定的文件类型进行自适应调整。表 2.1 解释了工具栏中最常见且相关的图标。

![Image from PDF page 105](../images/page-0105-image-03.png)

表 2.1：Eclipse 主工具栏图标

随着本书主题的深入，我们将有机会看到 Eclipse 的其他功能。
