<!-- page: 84 -->

## 1.4 Nucleo 开发板

任何关于电子设备的实用文本都需要一块开发板（也称为套件）才能开始工作。在 STM32 领域中，最广泛使用的开发板是 STM32 Discovery。ST 已经开发了 48 种不同的 Discovery 开发板，用于测试 STM32 微控制器（microcontroller）及其功能。

![Image from PDF page 84](../images/page-0084-image-02.jpeg)

图 1.17：ST 于 2015 年推出的 STM32L0538 Discovery 套件

例如，STM32L0538DISCOVERY 开发板（图 1.17）允许测试 STM32L053 微控制器（MCU）以及电子纸显示屏。您可以在互联网上找到大量涵盖 Discovery 系列开发板的教程。

²⁰http://apple.co/Uf20WR ²¹http://bit.ly/1Pvo8EV

<!-- page: 85 -->

ST 在 2015 年推出了一系列全新的开发板：Nucleo。Nucleo 系列分为三个主要组别：Nucleo-32、Nucleo-64 和 Nucleo-144（见图 1.18）。每个组别的名称源自所使用的微控制器（MCU）封装类型：Nucleo-32 使用 LQFP-32 封装的 STM32；Nucleo-64 使用 LQFP-64 封装；Nucleo-144 使用 LQFP-144 封装。Nucleo-64 是首个推向市场的系列，目前共有 32 种不同的开发板，每块板都配备特定的 STM32 微控制器（microcontroller）。Nucleo-144 于 2016 年 1 月推出，是首个配备强大 STM32F746 的低成本套件。它还提供了以太网物理层收发器²²和 LAN 端口。由于 Nucleo-64 是最完整的系列，本书将仅涵盖 Nucleo-64 系列中最相关的开发板（完整列表见表 1.21）。在本书的其余部分，我们将简单地用术语“Nucleo”来指代 Nucleo-64。

Nucleo 由两部分组成，如图 1.19 所示。带有 mini-USB 连接器的部分是一个集成的 ST-LINK 2.1 调试器，用于将固件上传到目标微控制器（MCU）并进行单步调试。ST-LINK 接口还提供虚拟 COM 端口（VCP），可用于与主机 PC 交换数据和消息。Nucleo 开发板的一个关键特性是，ST-LINK 接口可以轻松地从板子的其余部分分离出来（图 1.19 中的两个红色剪刀图标指示了断开位置）。这样，它可以作为独立的 ST-LINK 编程器使用（独立的 ST-LINK 编程器价格约为 25 美元）。然而，ST-LINK 提供了一个可选的 SWD 接口，可以通过移除标有 ST-LINK 的两个跳线帽，在不将 ST-LINK 接口从 Nucleo 上拆下的情况下（正如在 Discovery 开发板上已经发生的那样）用于编程另一块板子。板子的其余部分包含目标微控制器（MCU）（我们将用于开发应用程序的微控制器）、一个 RESET 按钮（黑色）、一个用户可编程的轻触按钮（蓝色）和一个 LED。板子上还有一个用于安装外部高速晶振（HSE）的焊盘。所有较新的 Nucleo 开发板都已提供低速晶振。最后，板子上有几个引脚排针，我们稍后会详细介绍。

![Image from PDF page 85](../images/page-0085-image-01.jpeg)

图 1.18：一块 Nucleo 开发板

ST 推出这款新套件是为了吸引来自 Arduino 世界的人们。事实上，Nucleo 开发板提供了引脚排针，以接受 Arduino 扩展板，这些扩展板是专门为扩展 Arduino

²²以太网物理层收发器（也称为以太网 PHY）是一种将局域网（LAN）网络中交换的消息转换为电信号的设备。

<!-- page: 86 -->

UNO 及其他所有 Arduino 开发板而构建的。图 1.20²³ 显示了与 Arduino 兼容连接器相关的 STM32 外设和 GPIO。

![Image from PDF page 86](../images/page-0086-image-01.jpeg)

图 1.19：Nucleo 开发板的相关部分

诚实地说，与 Discovery 开发板相比，Nucleo 开发板还有其他有趣的优点。首先，ST 以极具竞争力的价格出售它们（可能是出于上述原因）。一块 Nucleo 的价格在 10 到 15 美元之间，具体取决于购买地点，如果您考虑到使用这种架构可以做的事情，您必须同意与 Arduino DUE 开发板（同样配备 Microchip 的 32 位 ARM 处理器）相比，它的价格确实偏低。另一个有趣的特性是，Nucleo 开发板被设计为彼此引脚兼容。这意味着您可以为 STM32Nucleo-F103RB 开发板（配备流行的 STM32F103 微控制器）开发固件，如果需要更多的计算能力，稍后可以将其适配到更强大的 Nucleo（例如 STM32Nucleo-F401RE）。

²³图 1.20 和 22 取自 mbed.org 网站，并指代 Nucleo-F401RE 开发板。请参阅附录 C 以获取您的 Nucleo 开发板的正确引脚定义。

<!-- page: 87 -->

![Image from PDF page 87](../images/page-0087-image-01.jpeg)

图 1.20：与 Arduino 排针相关的外设和 GPIO

除了 Arduino 兼容的引脚排针外，Nucleo 还提供了自己的扩展连接器。它们是两个 2x19、间距为 2.54mm 的公头引脚排针。它们被称为 Morpho 连接器，是访问大多数微控制器（MCU）引脚的便捷方式。图 1.21 显示了与 Morpho 连接器相关的 STM32 外设和 GPIO。

![Image from PDF page 87](../images/page-0087-image-02.jpeg)

图 1.21：与 Morpho 排针相关的外设和 GPIO

ST 正在发布多种适用于 Nucleo 的扩展板，这些扩展板与 Arduino UNO 或 ST Morpho 排针兼容。例如，图 1.22 显示了一块带有 X-NUCLEO-IHM07M1 扩展板的 Nucleo-F302R8 开发板，该扩展板是一个配备 ST L6230 DMOS 驱动器的电机控制

<!-- page: 88 -->
