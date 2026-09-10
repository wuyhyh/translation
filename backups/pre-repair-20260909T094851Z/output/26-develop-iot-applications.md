<!-- page: 763 -->

# 26. 开发物联网应用

在一个互联的世界中，越来越多的设备正在实现连接。汽车、洗衣机和冰箱等家用电器、灯光、百叶窗、恒温器，以及用于环境监测的传感器，都只是如今通过互联网交换消息的设备的少数几个例子。许多观察者一致认为，这就是物联网（Internet of Things, IoT）时代。实际上，很难说物联网是否会代表电子行业的一个新的黄金时代。但可以肯定的是，许多半导体公司正在该领域投入数十亿美元。

物联网是一个模糊的术语。它没有说明通信标准、协议、应用层，甚至系统架构。物联网通信协议和技术的世界是一片丛林。存在数十种标准，尤其是无线通信协议。WiFi、Bluetooth、Zigbee、LoRaWAN，以及 TI 的 SimpliciTI 或 Microchip 的 MiWI 等专有解决方案，还有 5G/4G 移动网络。但即使通信介质也有数十种。例如，在无线通信中，2.4GHz 和 5.8GHz 频率是全球标准，但还有几个区域性和替代频率，例如欧盟的 868MHz（美国的 915MHz）、欧盟和美国部分地区的 434MHz，以及欧盟大部分地区和日本的 169MHz。这些标准中的每一个都有自己关于发射功率、占空比等的规则。每种都有其优缺点。

通信介质和协议的选择也会影响应用架构。例如，支持 WiFi 或以太网的设备只需使用集成 MODEM 的路由器即可连接到互联网。使用专有协议的设备（例如 Zigbee 设备）通常需要中间设备（控制单元），该设备收集消息并通过互联网将其发送到集中式服务器（或现在称为云服务器的集中式服务器）。对于某些“工业”应用，这通常是一个优势（即使在没有互联网的情况下，本地设备也可以继续工作）。对于消费级应用，这通常会阻碍用户采用该解决方案。

如今，有几家芯片制造商提供集成有线和无线连接功能的微控制器。Texas Instruments 在收购 ChipCon 后，开发了几款集成射频前端的 MCU。例如，CC2540 是一款 8051 MCU，带有专用于 Bluetooth 应用的 2.4GHz 射频。CC3200 是一款 Cortex-M4 内核，带有能够根据 WiFi 标准进行通信的 2.4GHz 射频。最近，市场上出现了另一个参与者。Espressif¹ 是一家中国公司，向市场推出了一款双核 Tensilica² LX6 微控制器，运行频率为 240MHz，集成 2.4GHz 射频和 MAC 层（ESP32³）。这些 MCU 在低批量下成本低于 5 美元，在创客群体中很受欢迎。

本章为未实现以太网控制器的 Nucleo-64 板所有者提供解决方案。

¹https://espressif.com/ ²Tensilica 是一家公司，与 ARM 类似，设计 IP 内核，随后由芯片制造商实现。它目前由 Cadence 拥有，Cadence 也是设计 Allegro CAD 的公司。 ³https://bit.ly/2dN52fx

<!-- page: 764 -->

器。提出的解决方案基于 WIZnet⁴ 的 W5500 网络处理器，WIZnet 是一家专门设计此类设备的韩国公司。该公司凭借 W5100 IC 获得了巨大的知名度，该 IC 被用于开发流行的 Arduino Ethernet Shield⁵。我们将看到如何使用 Nucleo 开发集成 Web 服务器的嵌入式应用。然而，在进入这些内容之前，我将简要介绍 ST 为开发物联网应用提供的 CubeHAL 计划。

## 26.1 STM 提供的物联网应用开发解决方案

如前所述，F1/2/4/7 系列的多个 STM32 微控制器提供集成以太网控制器，支持介质无关接口（Media-Independent Interface, MII）及其变体缩减型 MII（Reduced-MII, RMII）。这是一种通信标准，它抽象了给定的物理介质，并允许将以太网控制器的 MAC 层连接到物理控制器芯片，也称为物理层收发器（phyther）。市场上存在多种 LAN 物理层收发器，与芯片的互连完全由底层 MII 协议处理。

然而，专用硬件接口的存在并不能快速构建物联网应用。还需要一个完整的 TCP/IP 协议栈，否则对于单个开发人员来说，处理像 TCP/IP 这样复杂的协议栈是不可能的。ST 不提供自定义解决方案，而是采用了轻量级 IP（Lightweight IP, LwIP）协议栈。LwIP 是一个由 Adam Dunkels 发起，现在由大型社区维护的开源框架。此外，Altera、Xilinx 和 Freescale 等其他几家半导体公司也参与了这个相当复杂的框架的开发。

ST 已将 LwIP 集成到 CubeMX 中，它会自动向项目添加与该框架配合工作所需的所有文件。一旦启用以太网控制器，LwIP 就会显示为可选的中间件组件。ST 积极维护和支持它。

以下是 LwIP 的最相关特性：

- IP（互联网协议，IPv4 和 IPv6），包括通过多个网络接口的数据包转发
- ICMP（互联网控制消息协议），用于网络维护和调试
- IGMP（互联网组管理协议），用于多播流量管理
- MLD（IPv6 的多播监听器发现）

- – 旨在符合 RFC 2710。不支持 MLDv2
- ND（IPv6 的邻居发现和状态无关地址自动配置）

- – 旨在符合 RFC 4861（邻居发现）和 RFC 4862（地址自动配置）
- UDP（用户数据报协议），包括实验性的 UDP-lite 扩展

⁴http://www.wiznet.co.kr/ ⁵http://bit.ly/2dMXhGi

<!-- page: 765 -->

- TCP（传输控制协议），具有拥塞控制、RTT 估计和快速恢复/快速重传
- 用于增强性能的原始/原生套接字 API
- 可选的类 Berkeley 套接字 API
- DNS（域名解析器）

LwIP 还为以下应用协议提供完整实现：

- 支持 SSI 和 CGI 的 HTTP 服务器
- 带有 MIB 编译器的 SNMPv2c 代理（简单网络管理协议）
- SNTP（简单网络时间协议）
- NetBIOS 名称服务响应器
- MDNS（多播 DNS）响应器
- iPerf 服务器实现

由于配备 Nucleo-64 板的 STM32 微控制器缺乏 RMII 接口，我将不会在此详细列出在应用中设置 LwIP 所需的步骤。有关此内容的更多信息，请参阅 CubeHAL 示例。此外，你可以在我的博客上找到一些关于此主题的文章。最后，CubeMXImporter 工具实现了所有必要的逻辑，以将 LwIP 协议栈导入 GNU MCU Eclipse 项目。

当谈到物联网时，无线协议起着重要作用。ST 意识到几个无线标准的关键作用。因此，ST 也带着两个专用的 STM32 系列进入了这个市场领域：STM32WB 和 STM32WL。前者面向 2.4GHz 射频应用，支持 Bluetooth 5.2、Bluetooth Mesh 以及在该频段运行的其他协议，如 Zigbee 3.0。后者，STM32WL 系列，则面向 Sub-Ghz 频谱，范围从 169MHz 到 915MHz。此外，ST 与 Semtech 建立了合作伙伴关系，以开发兼容 Long Range Alliance (LoRa) 的自定义解决方案。得益于这一合作伙伴关系，STM32WL 系列集成了支持 LoRaWANTM 标准化协议的 Semtech LoRa 收发器。ST 提供了一套专用的 Nucleo 板，用于 STM32WL 和 STM32WB 系列的开发。

<!-- page: 766 -->

![Image from PDF page 766](../images/page-0766-image-01.jpeg)

图 26.1：Nucleo-WB55 开发板

## 26.2 W5500 以太网控制器

除了较新的 Nucleo-144 开发板外，其他 Nucleo-64 和 Nucleo-32 开发板均未提供集成以太网控制器的 STM32 微控制器（MCU）。这意味着，如果您希望在 Nucleo-64 上开发物联网（IoT）应用，就需要使用外部扩展板。

WIZnet 是一家韩国公司，其知名度得益于 Arduino 开发板。事实上，其首款以太网控制器 W5100 IC 正是用于创建 Arduino 以太网扩展板的芯片。自 W5100 控制器以来，WIZnet 持续迭代开发了其他类似产品。其中表现最佳的产品之一是 W5500，我们将在本章中对其进行研究。

W5500 是一款单片式以太网控制器，集成了 LAN 物理层（PHY）。此外，它还是一个完整的网络处理器，内置硬连线 TCP/IP 协议栈。该芯片旨在通过高速 SPI 接口（该接口最高支持 80MHz 工作频率）与主机微控制器交换数据。该芯片的主要特性如下：

- 支持 TCP、UDP、ICMP、IPv4、ARP、IGMP、PPPoE
- 支持同时使用 8 个独立套接字（socket）
- 支持掉电模式（Power down mode）
- 支持基于 UDP 的局域网唤醒（Wake on LAN）
- 支持高速串行外设接口（SPI MODE 0, 3），最高达 80MHz
- 内部 32Kbytes 存储器用于发送/接收缓冲区

<!-- page: 767 -->

- 嵌入式 10BaseT/100BaseTX 以太网 PHY
- 支持自动协商（全双工和半双工，10 和 100 速率）
- 3.3V 工作电压，具备 5V I/O 信号容限
- LED 输出指示（全/半双工、链路、速率、活动状态）
- 48 引脚 LQFP 无铅封装（7x7mm，0.5mm 间距）

![Image from PDF page 767](../images/page-0767-image-01.jpeg)

图 26.2：由 STM32F0 微控制器（左侧）和 W5500 IC（右侧）组成的定制设备

W5500 IC 易于嵌入到定制设计中。只需一个晶振、少量无源元件和一个 LAN 变压器即可使其工作。该芯片还集成了为 LAN 变压器供电所需的充电泵。我在几个定制设计中成功使用了该芯片。由于整个 TCP/IP 协议栈都包含在网络处理器内部，该芯片甚至可以配合低成本 STM32F0 微控制器使用。此外，对于小批量生产，使用这种芯片配合低成本 STM32 微控制器，比使用带有集成以太网和外部专用 LAN 物理层的高性能微控制器更为方便。图 26.2 展示了作者制作的一个定制设计，其中使用 STM32F030 微控制器来驱动 W5500 IC。静态网页存储在外部 SPI FLASH 存储器中。

WIZnet 开发了一款兼容 Arduino 的扩展板（见图 26.3），即使配合 Nucleo 开发板也能开箱即用。该扩展板还集成了 MicroSD 卡读卡器，该读卡器连接在 W5500 IC 的同一 SPI 端口上。这使得可以将网页和其他静态内容（图像、CSS、JavaScript 文件等）存储在外部 SD 卡上。

<!-- page: 768 -->

![Image from PDF page 768](../images/page-0768-image-01.jpeg)

图 26.3：WIZnet 的 W5500 以太网扩展板

像 W5500 及类似的网络处理器以简单的方式工作。该芯片提供多达八个套接字⁶。每个套接字都有一组关联的寄存器。通过修改这些寄存器的内容，可以驱动套接字（打开连接、将其置于监听模式、发送/接收数据等）。为了通过套接字传输数据，W5500 提供内部 32KB 缓冲区空间，该空间可以在八个套接字之间自由划分，我们稍后会看到这一点。通过向该缓冲区写入/从中读取，您可以与另一端点交换数据。这意味着，从微控制器的角度来看，驱动这些 IC 仅仅是通过 SPI 接口交换字节的问题。然而，处理套接字的所有内部状态可能很困难，尤其是对于这类 IC 的新手而言。我开发了一个用于驱动 W5100 的库，我可以确认这项活动非常耗时。此外，不幸的是，所有 W5X00 IC（5100、5200、5300 和 5500）都有一些“棘手”且文档记录不佳的 bug，难以解决。

⁶在网络中，套接字是对复杂 TCP/IP 协议栈的抽象。它只是一个句柄，允许将字节流从一台机器发送到另一台机器，而无需处理复杂的底层协议（除非您需要执行高级操作）。

<!-- page: 769 -->

![Image from PDF page 769](../images/page-0769-image-01.png)

图 26.4：ioLibrary_Driver 库的架构

WIZnet 大约七年前为这一系列芯片发布了一个专用库。它名为 ioLibrary_Driver，可在 GitHub⁷ 上获取。该库的架构如图 26.4 所示。该库基本上由两层组成。一层称为 Ethernet（以太网），包含用于建立对等节点之间连接的原始操作。文件 Ethernet/socket.c 包含所有与套接字管理相关的例程。套接字 API 类似于 BSD 套接字 API，尽管并不完全兼容。相同的 Ethernet 层包含针对每个 WIZnet 芯片的低层驱动程序。例如，文件 Ethernet/w5500.c 包含驱动 W5500 芯片所需的所有逻辑。最后，文件 Ethernet/wizchip_conf.h 包含用于配置该库的宏（稍后会有更多介绍）。

Internet（互联网）层构建在 Ethernet 层之上，是多种互联网协议和服务的集合：

- DHCP 客户端
- DNS 客户端
- FTP 客户端和服务器
- SNMP 代理/陷阱
- SNTP 客户端
- TFTP 客户端
- HTTP 服务器

用户应用程序可以使用上述一个或多个协议，或直接访问 Ethernet 层来构建自定义应用程序。

⁷https://github.com/Wiznet/ioLibrary_Driver

<!-- page: 770 -->

### 26.2.1 如何使用 W5500 扩展板和 ioLibrary_Driver 模块

如前所述，W5500 与本书中使用的全部九块 Nucleo 开发板都能无缝配合。图 26.5⁸ 展示了该扩展板的引脚定义。SPI 接口被路由至 D13、D12 和 D11 引脚，这些引脚对应于 SPI1 外设的相同引脚（Nucleo-F302R8 开发板除外，在该板上这些引脚对应于 SPI2 外设）。W5500 的从设备选择（Slave Select, SS）引脚对应于 Arduino D10 引脚，而 SD 卡的 SS 引脚对应于 Arduino D4 引脚。

![Image from PDF page 770](../images/page-0770-image-01.jpeg)

图 26.5：W5500 扩展板的引脚定义

⁸该图取自 WIZnet 网站 (https://bit.ly/2dxjblH)。

<!-- page: 771 -->

![Image from PDF page 771](../images/page-0771-image-01.png)

观察图 26.5，可以看到 D2 引脚起着重要作用。W5500 IC 被设计为可选地在发生与网络接口（例如 IP 冲突等）或单个套接字（例如连接建立、数据接收等）相关的多个事件时，将 INTn 引脚拉低。此功能允许将对应的微控制器（MCU）引脚配置为 GPIO_MODE_IT_FALLING，以便当 IC 将 INTn 引脚拉低时触发相应的中断请求（IRQ）。这使得编写异步应用程序成为可能，特别是当您将 ioLibrary_Driver 与实时操作系统（RTOS）结合使用时（例如，中断服务程序（ISR）可以使用信号量唤醒一个休眠的线程，该线程随后开始执行与套接字相关的操作）。

![Image from PDF page 771](../images/page-0771-image-02.jpeg)

图 26.6：要启用 INTn 引脚，需要短接 1-2 焊盘

请注意，在 W5500 扩展板上，D2 引脚并未连接到 W5500 的 INTn 引脚。要启用它，您需要按照图 26.6 所示，在焊盘 1-2 之间焊接一个 0603 封装的 0Ω 电阻器（使用焊锡滴进行连接也是足够的）。

<!-- page: 772 -->

#### 26.2.1.1 配置 SPI 接口

一旦建立了硬件连接，我们就可以将注意力集中在软件部分。将 ioLibrary_Driver 模块导入现有的 Eclipse 项目非常简单。首先，您需要将整个库拖放到 Eclipse 项目的根目录中。然后，您需要将以下路径添加到项目设置中的包含路径（Include paths）列表中：

```text
• "../ioLibrary_Driver/Ethernet"
• "../ioLibrary_Driver/Internet"
```

最后，您需要通过设置 ioLibrary_Driver/Ethernet/wizchip_conf.h 文件中的宏 _WIZCHIP_ 来指定确切的 W5XXX 芯片类型。

<!-- page: 773 -->

ioLibrary_Driver 模块被设计为与特定的微控制器（MCU）和用于操作 SPI 接口的例程相抽象。它可以与 STM32、AVR、Microchip MCU 等一起使用。因此，我们需要一种方式来将其与用于编程 SPI 外设的 HAL_SPI 模块进行接口连接。

作为该库的用户，我们需要提供 6 个回调例程，以实现驱动 SPI 所需的所有逻辑。这些例程如下：

- void cs_sel()：每当库需要选择（拉低）连接到 W5500 SS 引脚的引脚时，库会调用此回调。
- void cs_desel()：每当库需要取消选择（拉高）连接到 W5500 SS 引脚的引脚时，库会调用此回调。
- uint8_t spi_rb()：当需要从 SPI 接口读取一个字节时，调用此例程。
- void spi_wb(uint8_t b)：当需要通过 SPI 接口发送一个字节时，调用此例程。
- void spi_rb_burst(uint8_t *buf, uint16_t len)：当需要通过 SPI 读取超过三个字节时，调用此可选回调。这允许我们实现以直接存储器访问（DMA）模式处理 SPI 的回调，从而加快传输速度（此模式也称为突发模式）。
- void spi_wb_burst(uint8_t *buf, uint16_t len)：当需要通过 SPI 发送超过三个字节时，调用此可选回调。这允许我们实现以 DMA 模式处理 SPI 的回调。

假设 SPI 接口已相应配置，我们可以简单地按以下方式实现这些回调：

```text
void cs_sel() {
HAL_GPIO_WritePin(W5500_CS_GPIO_Port, W5500_CS_Pin, GPIO_PIN_RESET); //CS LOW
}
void cs_desel() {
HAL_GPIO_WritePin(W5500_CS_GPIO_Port, W5500_CS_Pin, GPIO_PIN_SET); //CS HIGH
}
uint8_t spi_rb(void) {
uint8_t rbuf;
HAL_SPI_Receive(&hspi1, &rbuf, 1, HAL_MAX_DELAY);
return rbuf;
}
void spi_wb(uint8_t b) {
HAL_SPI_Transmit(&hspi1, &b, 1, HAL_MAX_DELAY);
}
```

```text
void spi_rb_burst(uint8_t *buf, uint16_t len) {
HAL_SPI_Receive_DMA(&hspi1, buf, len);
while(HAL_SPI_GetState(&hspi1) == HAL_SPI_STATE_BUSY_RX);
}
void spi_wb_burst(uint8_t *buf, uint16_t len) {
HAL_SPI_Transmit_DMA(&hspi1, buf, len);
while(HAL_SPI_GetState(&hspi1) == HAL_SPI_STATE_BUSY_TX);
}
```

一旦我们定义了与硬件相关的函数，就必须将它们“传递”给 ioLibrary。可以使用以下例程来完成这项工作：

```text
...
reg_wizchip_cs_cbfunc(cs_sel, cs_desel);
reg_wizchip_spi_cbfunc(spi_rb, spi_wb);
reg_wizchip_spiburst_cbfunc(spi_rb_burst, spi_wb_burst);
```

完成。通过这几行代码，我们已成功将 ioLibrary_Driver 库与 CubeHAL 集成。

#### 26.2.1.2 配置套接字缓冲区和网络接口

现在，我们终于准备好开始使用 W5500 IC 了。第一步是通过一个定义明确的流程来初始化 W5500 芯片。在配置好回调函数后，需要调用的第一个函数是：

```text
int8_t wizchip_init(uint8_t* txsize, uint8_t* rxsize);
```

该例程执行两项任务：重置 W5500 IC（这是强制要求的步骤）以及配置每个独立套接字的 TX 和 RX 缓冲区大小。所有 W5X00 IC 都有两个内部公共内存区域，分别专用于 TX 和 RX 缓冲区。在 W5500 芯片中，这两个区域每个宽度为 16KB。这两个区域必须进一步在我们要使用的套接字之间进行划分。默认配置将这两个区域的 2KB 分配给八个套接字中的每一个。但是，例如，如果我们的应用程序只需要四个套接字，那么我们可以将 RX 和 TX 缓冲区划分为四份。或者，如果一个套接字需要更多的空间来与对等端交换数据，那么我们可以只给这一个套接字分配更多空间，并减少其他套接字的空间。

我们可以通过向 `wizchip_init()` 例程传递两个数组来指定 TX 和 RX 缓冲区的分配，每个数组包含八个值。唯一的要求是这些值的总和不得超过 16。例如，如果我们要在应用程序中仅使用两个套接字，我们可以按以下方式定义配置数组：

<!-- page: 774 -->

```text
uint8_t bufSize[] = {12, 4, 0, 0, 0, 0, 0, 0};
wizchip_init(bufSize, bufSize);
```

上述代码简单地将 12KB 的 TX 和 RX 缓冲区分配给第一个套接字，并将剩余的 4KB 分配给第二个套接字。显然，只要尊重 16KB 的总大小，我们可以自由安排 TX 和 RX 缓冲区。

一旦芯片初始化完成，我们就可以使用以下函数来配置网络接口：

```text
void wizchip_setnetinfo(wiz_NetInfo* pnetinfo);
```

其中，用于向库传递网络配置参数的 `wiz_NetInfo` 结构体定义如下：

```text
typedef struct wiz_NetInfo_t {
uint8_t mac[6];
/* 源 MAC 地址 */
uint8_t ip[4];
/* 源 IP 地址 */
uint8_t sn[4];
/* 子网掩码 */
uint8_t gw[4];
/* 网关 IP 地址（可选） */
uint8_t dns[4];
/* DNS 服务器 IP 地址（可选） */
dhcp_mode dhcp;
/* 1 - 静态，2 - DHCP（可选） */
} wiz_NetInfo;
```

这里我不详细解释这些字段，因为它们不言自明。例如，为了配置 W5500 使其能够连接到 192.168.1.0/24 子网，我们可以按以下方式操作：

```text
wiz_NetInfo netInfo = {.mac
= {0x00, 0x08, 0xdc, 0xab, 0xcd, 0xef}, // MAC 地址
.ip
= {192, 168, 1, 192},
// IP 地址
.sn
= {255, 255, 255, 0},
// 子网掩码
.gw
= {192, 168, 1, 1}};
// 网关地址
wizchip_setnetinfo(&netInfo);
```

![Image from PDF page 774](../images/page-0774-image-01.png)

请注意，在这个例子中我们使用的是任意的 MAC 地址。这种操作在私有和测试环境中是被允许的，但如果你计划销售基于 W5500 的产品，则是完全禁止的。在这种情况下，你必须从 IEEE 购买有效的 MAC 地址池（地址池从 4096 个地址的批次开始，价格约为 800 美元⁹）。或者，Microchip 销售预编程的 IC¹⁰，具有有效的 IEEE EUI-48 和 EUI-64 MAC 地址（它们的工作方式类似于 I²C EEPROM）。对于小批量生产，它们是购买自定义 MAC 地址的良好替代方案。

⁹https://bit.ly/34HObty ¹⁰https://bit.ly/2dKLLhA

<!-- page: 775 -->

### 26.2.2 套接字 API

ioLibrary_Driver 模块提供了一组用于操作套接字的 API，其风格类似于 BSD 套接字 API。即使它与 BSD API 不兼容，如果你已经使用过 BSD API，那么开始使用它将会非常容易。

要初始化一个新的套接字，我们可以使用以下函数：

```text
int8_t socket(uint8_t sn, uint8_t protocol, uint16_t port, uint8_t flag);
```

其中：

- `sn`：对应套接字编号，如果你使用的是提供 8 个套接字的 W5500 IC，它可以是 0 到 7 之间的值。
- `protocol`：此参数定义套接字的协议类型。W5500 能够处理三种协议类型：TCP、UDP 和 RAW 套接字¹¹。因此，此参数可以取 `Sn_MR_TCP`、`Sn_MR_UDP` 和 `Sn_MR_MACRAW` 中的一个值。
- `port`：指定与套接字关联的端口号。
- `flag`：它是表 26.1 中列出的附加配置参数的组合（逻辑或）。

成功时，`socket()` 函数返回 `sn` 值，否则它可能返回 `SOCKERR_SOCKNUM` 以指示错误的套接字编号，`SOCKERR_SOCKMODE` 以指示错误的协议，或 `SOCKERR_SOCKFLAG` 以指示无效的 flag 参数。

表 26.1：套接字标志值

模式 | 描述
---|---
SF_IO_NONBLOCK | 将套接字配置为非阻塞模式
SF_ETHER_OWN | W5500 只能接收广播包或发送给它自己的包。此参数仅适用于 RAW 套接字
SF_IGMP_VER2 | 当套接字协议为 UDP 且也指定了 SF_MULTI_ENABLE 模式时，启用 IGMP 版本 2
SF_MULTI_ENABLE | 当套接字协议为 UDP 时，启用多播模式
SF_TCP_NODELAY | 配置 TCP 套接字，使得一旦从远程对等端接收到数据包，就立即发送 ACK 包
SF_BROAD_BLOCK | 当套接字协议为 UDP 或 RAW 时，防止套接字接收广播包
SF_MULTI_BLOCK | 当套接字协议为 RAW 时，防止套接字接收广播包
SF_IPv6_BLOCK | 当套接字协议为 RAW 时，防止套接字接收 IPv6 包
SF_UNI_BLOCK | 当套接字协议为 UDP 时，防止套接字接收单播包

要关闭套接字并取消其配置，我们使用以下函数：

¹¹RAW 套接字是一种允许直接使用 IP 协议交换数据包，而不使用任何特定于协议的传输层（即 TCP 或 UDP）的套接字。

<!-- page: 776 -->

```text
int8_t close(int8_t sn);
```

**仔细阅读**

![Image from PDF page 776](../images/page-0776-image-01.png)

请注意，如果你正在使用 C 标准库中的 I/O 函数，那么由于 C 标准库 `close()` 函数的签名（设计为接受并返回 `int` 类型），此函数将会崩溃。这将产生大量的编译器错误。不幸的是，WIZnet 团队选择了一个不幸的名称和签名。你可以通过修改库，以另一种方式声明 `close()` 函数来绕过这个问题：

```text
int close(int sn);
```

W5500 套接字具有定义明确的状态，检索该状态以更好地理解连接状态可能很有用。宏：

```text
getSn_SR(sn);
```

自动从其寄存器中检索套接字状态。W5500 IC 的可能状态值列于表 26.2 中。

表 26.2：套接字状态值

状态 | 描述
---|---
SOCK_CLOSED | 已关闭
SOCK_INIT | 初始化状态
SOCK_LISTEN | 监听
SOCK_ESTABLISHED | 连接已建立
SOCK_CLOSE_WAIT | 关闭状态
SOCK_UDP | UDP 套接字
SOCK_SYNSENT | 已向远程对等端发送连接请求包（SYN）
SOCK_SYNRECV | 已从远程对等端接收连接请求包（SYN）
SOCK_FIN_WAIT | 已开始套接字关闭过程
SOCK_CLOSING | 正在关闭套接字
SOCK_TIME_WAIT | 等待套接字关闭
SOCK_LAST_ACK | 套接字仍然打开，但远程对等端已关闭连接

#### 26.2.2.1 在 TCP 模式下处理套接字

一旦配置好套接字协议和模式，我们就可以开始与远程对等方（客户端应用程序）建立连接，或者将套接字置于监听模式以接受来自远程对等方（服务器应用程序）的连接。

要与远程对等方建立连接，我们使用以下函数：

<!-- page: 777 -->

```text
int8_t connect(uint8_t sn, uint8_t * addr, uint16_t port);
```

- sn：对应于使用 socket() 函数配置的套接字。
- addr：它是一个由四个字节组成的数组，对应于远程对等方的 IPv4 地址。
- port：它是远程对等方的端口号。

成功时，connect() 函数返回 SOCK_OK 值。否则，存在一系列可能的错误值。请查看 socket.h 文件。

当与远程对等方的连接建立后，我们可以使用以下函数发送一系列字节：

```text
int32_t send(uint8_t sn, uint8_t * buf, uint16_t len);
```

其中 buf 是长度为 len 的字节数组。

相反，要从远程对等方接收字节数组，我们使用以下函数：

```text
int32_t recv(uint8_t sn, uint8_t * buf, uint16_t len);
```

要与远程对等方断开连接，我们可以使用以下函数：

```text
int8_t disconnect(uint8_t sn);
```

如果我们要创建服务器应用程序，一旦使用 socket() 函数配置好套接字，我们就可以使用以下函数将其置于监听模式：

```text
int8_t listen(uint8_t sn);
```

一旦连接建立，我们可以使用 recv() 和 send() 函数接收和发送数据。

#### 26.2.2.2 在 UDP 模式下处理套接字

UDP 是一种无连接协议，因此我们不需要显式创建连接即可开始与远程对等方交换字节。

当套接字处于 UDP 模式时，要向远程对等方发送字节数组，我们使用以下函数：

```text
int32_t sendto(uint8_t sn, uint8_t * buf, uint16_t len, uint8_t * addr, uint16_t port);
```

而从远程对等方接收字节，我们使用以下函数：

<!-- page: 778 -->

```text
int32_t recvfrom(uint8_t sn, uint8_t * buf, uint16_t len, uint8_t * addr, uint16_t *port);
```

### 26.2.3 将 I/O 重定向到 TCP/IP 套接字

在第 5 章中，我们了解了如何将 C 终端 I/O 函数（如 printf() 和 scanf()）重定向到 UART 接口。在开发物联网（IoT）应用程序期间，将 I/O 重定向到网络套接字非常有用，这样我们可以通过网络连接调试设备。如果设备不在我们的直接控制之下，这一点尤其有用。

### 使用 W5500 IC 及其相关的套接字库，此操作很容易实现。RetargetInit() 函数可以重写为以下形式：

```text
Filename: Core/Src/retarget-tcp.c
13
#ifdef RETARGET_TCP
```

14

```text
15
#define STDIN_FILENO
0
16
#define STDOUT_FILENO 1
17
#define STDERR_FILENO 2
```

18

```text
19
#ifndef RETARGET_PORT
20
#define RETARGET_PORT 5000
21
#endif
```

22

```text
23
int8_t gSock = -1;
```

24

```text
25
uint8_t RetargetInit(int8_t sn) {
26
gSock = sn;
```

27

```text
28
/* Disable I/O buffering for STDOUT stream, so that
29
* chars are sent out as soon as they are printed. */
30
setvbuf(stdout, NULL, _IONBF, 0);
```

31

```text
32
/* Open 'sn' socket in TCP mode with a port number equal
33
* to the value of RETARGET_PORT macro */
34
if(socket(sn, Sn_MR_TCP, RETARGET_PORT, 0) == sn) {
35
if(listen(sn) == SOCK_OK)
36
return 1;
37
}
38
return 0;
39
}
```

代码不言自明。RetargetInit() 函数接受一个套接字编号，对于 W5500 IC，其范围从 0 到 7。该函数随后配置套接字并将其置于监听模式。_write() 函数可以重新排列为以下形式：

<!-- page: 779 -->

```text
Filename: Core/Src/retarget-tcp.c
49
int _write(int fd, char* ptr, int len) {
50
int sentlen = 0;
51
int buflen = len;
```

52

```text
53
if(getSn_SR(gSock) == SOCK_ESTABLISHED) {
54
if (fd == STDOUT_FILENO || fd == STDERR_FILENO) {
55
while(1) {
56
sentlen = send(gSock, (void*) ptr, buflen);
57
if (sentlen == buflen)
58
return len;
59
else if (sentlen > 0 && sentlen < buflen) {
60
buflen -= sentlen;
61
ptr += (len - buflen);
62
}
63
else if (sentlen < 0)
64
return EIO;
65
}
66
}
67
} else if(getSn_SR(gSock) != SOCK_LISTEN) {
68
/* Remote peer close the connection? */
69
close(gSock);
70
RetargetInit(gSock);
71
}
```

72

```text
73
errno = EBADF;
74
return -1;
75
}
```

该函数首先检查套接字状态是否等于 SOCK_ESTABLISHED：这意味着远程对等方已与我们设备建立了连接。相反，如果套接字不处于监听模式（第 67 行），则可能是远程对等方关闭了连接：因此我们需要通过调用 RetargetInit() 函数再次将套接字配置为监听模式。如果远程对等方已建立连接，我们就可以开始通过 TCP/IP 连接发送 ptr 缓冲区。

_read() 函数与 _write() 函数几乎相同。完整源代码请参阅本书示例。要使用此模块，我们只需在项目级别定义宏 RETARGET_TCP，并最终移除宏 OS_USE_SEMIHOSTING。

要开始与设备建立连接，Linux 和 MacOS 用户可以使用 telnet 命令，而 Windows 用户可以使用如 putty 这样的终端仿真程序。

### 26.2.4 构建 HTTP 服务器

Internet/httpServer 模块提供了一个基于以太网层构建的完整 HTTP 服务器实现。该模块允许您在几个步骤内设置一个 HTTP 服务器，特别是当您需要仅提供静态内容（即不需要动态处理数据的简单网页）时。

<!-- page: 780 -->

函数

```text
void httpServer_init(uint8_t * tx_buf, uint8_t * rx_buf, uint8_t cnt, uint8_t * socklist);
```

用于配置 HTTP 模块。它接受两个指针 tx_buf 和 rx_buf，指向用于存储 HTTP 服务器交换数据的两个内存缓冲区。这些数组需要有足够的空间来存储 HTTP 头部。事实上，当访问网页时，浏览器需要与 Web 服务器交换由 HTTP 协议定义的若干“底层”消息。这些消息会消耗数百字节，因此 tx_buf 和 rx_buf 缓冲区的最小可行大小均为 1024 字节¹²。cnt 参数告知 HTTP 模块可以使用多少个 W5500 套接字，而 socklist 参数用于传递可用套接字的确切列表。

例如，以下代码片段通过传递两个大小均为 1024 字节的缓冲区以及一个包含用于处理 HTTP 请求的套接字列表的数组来初始化 HTTP 服务器：

```text
#define DATA_BUF_SIZE 1024
#define MAX_HTTPSOCK 5
uint8_t RX_BUF[DATA_BUF_SIZE], TX_BUF[DATA_BUF_SIZE];
uint8_t socknumlist[] = {0, 1, 2, 3, 4};
...
httpServer_init(TX_BUF, RX_BUF, MAX_HTTPSOCK, socknumlist);
...
```

一旦从网络角度配置好 HTTP 服务器，我们就需要让它了解要提供的内容（HTML 页面、图像等）。有两种方法可以实现这一点：一种适用于小型且有限的应用程序，另一种适用于更复杂和结构化的 Web 应用程序。

通过使用函数：

```text
void reg_httpServer_webContent(uint8_t * content_name, uint8_t * content);
```

我们可以将给定的资源（例如文件 index.html）与一个字节数组关联起来，以便通过套接字将其发送到浏览器。content_name 参数对应资源名称，而 content 参数对应包含构成该资源的字节的数组。

¹² 由于 HTTP 库能够将整个 HTTP 流拆分为较小的块，因此可以减小这两个缓冲区的大小，但这会增加传输时间。

<!-- page: 781 -->

![Image from PDF page 781](../images/page-0781-image-01.png)

为什么 HTTP 服务器需要比一个空闲套接字更多的资源来完成其活动？这是一个在开发基于 Web 的嵌入式应用时必须牢记的基本概念，因此我们将对此稍作说明。

现代基于 Web 的应用程序非常复杂。通常，一个网站由多个资源组成：

- 包含 Web 应用程序实际内容的 HTML 页面；
- 装饰 HTML 内容并在某些情况下构成网页内容一部分的图像。
- 配置页面渲染及其功能的 CSS 和 Javascript 文件。

当 Web 浏览器访问网站时，它开始加载主 HTML 页面（如果未指定，则对应于 index.html 文件）。该页面几乎立即被解析（一些浏览器在接收到最初几个字节时就可以开始解析页面），如果其中包含对其他 Web 资源的引用，浏览器会几乎并行地开始加载它们。这种对网站资源的并发访问意味着浏览器会向 HTTP 服务器打开多个套接字（HTTP 协议是无状态的，它规定对于每个 Web 资源，必须向服务器执行单独的请求）。对于像 Apache 或 NGIX 这样设计用于在强大机器上运行的真正 Web 服务器来说，这并不构成问题。这些服务器应用程序被设计为能够处理甚至数千个并发连接。此外，强大的底层硬件允许在几毫秒内提供内容，具体取决于连接速度。套接字在不到一秒的时间内就会打开和关闭。

对于运行在真正嵌入式平台上的 Web 服务器，对同时资源的访问是一个必须仔细表征的问题。每个套接字都会消耗若干硬件资源，而对于 WIZnet 设备，套接字的最大数量是有限的。这意味着我们不能随意安排应用程序，一些现代框架（如 Bootstrap、Angular JS 等）在用于嵌入式设备时往往需要重新调整（有时我们甚至必须完全避免使用它们）。

例如，要发送一个简单的 HTML 页面，我们可以编写以下代码：

```text
const char webpage[] = "<html>
<head>
<title>Simple Web Page</title>
</head>
<body>
<h1>Hello World!</h1>
</body>";
reg_httpServer_webContent((uint8_t*)"index.html", webpage);
...
```

这种方法有几个陷阱。首先，网页嵌入在固件代码中。这意味着 HTML 内容会增加到固件本身中，从而增加整个二进制映像的大小。

<!-- page: 782 -->

其次，每次我们更改 Web 内容时，都需要重新编译整个二进制映像。对于大型和结构化的 Web 应用程序，这种方法是不切实际的。

第二种方法是指令 HTTP 模块从内存设备中查找并获取静态内容。例如，我们可以修改其代码，使其从闪存中加载 Web 资源。这就是我们在下一个示例中要做的事情，我们将使用 FatFs 库来检索存储在外部 SD 卡上的 Web 内容。

当 HTTP 服务器正确配置后，我们可以开始处理来自远程对等方的请求。默认情况下，此操作通过调用以下函数以轮询模式执行：

```text
void httpServer_run(uint8_t seqnum);
```

此函数接受对应于存储在传递给 httpServer_init() 函数的 socklist 参数中的套接字 ID 的索引。对于每个已注册的套接字，此函数检查相应套接字的状态，并根据给定的套接字状态执行 HTTP 状态机。例如，如果传入的套接字已打开并处于监听模式，httpServer_init() 函数会检查远程对等方是否已建立连接。整个 HTTP 协议和状态机由 HTTP 模块处理，除非我们需要对其进行高级操作，否则无需了解实现细节。

最后，HTTP 模块使用一些基于通用时间基准单位（tick）的内部延迟。函数：

```text
httpServer_time_handler();
```

必须从一个配置为每 1ms 触发一次的定时器中调用（Systick ISR 是调用该函数的合适位置）。

#### 26.2.4.1 基于 Web 的示波器

![Image from PDF page 782](../images/page-0782-image-01.png)

由于大多数配备在九块 Nucleo 开发板上的 STM32 微控制器（MCU）硬件资源有限，本示例仅在 STM32F401RE、STM32F411RE 和 STM32F446RE 微控制器上进行了测试。

我们现在将回顾一个更完整的示例，展示如何使用 W5500 IC 和 ioLibrary_Driver¹³ 模块来构建复杂且结构化的应用程序。在本示例中，我们将使用多个 STM32 外设来构建一种基于 Web 的示波器，如图 26.7 所示。通过将信号源连接到 ADC 外设的一个输入端，我们只需使用通用浏览器访问 Web 控制台，即可看到对应的波形。展示该示波器工作原理的视频可在此处查看¹⁴。

¹³ 随本章示例提供的 ioLibrary_Driver 并非 WIZnet 提供的官方库。作者对 HTTP 模块进行了多项修改，以提高其可靠性、性能和灵活性。例如，此修改版本能够使用 FatFs 模块提供存储在 SD 卡上的内容，或使用 ARM 半托管（semihosting）提供开发者 PC 上的内容。 ¹⁴https://youtu.be/fjtLQJDJ_04

<!-- page: 783 -->

![Image from PDF page 783](../images/page-0783-image-01.jpeg)

图 26.7：基于 Web 的示波器界面

该示例使用几种流行且现代的 Web 框架来构建用户界面：Bootstrap¹⁵、jQuery¹⁶ 和 D3js¹⁷。这些框架的介绍超出了本书的范围，并假定读者熟悉最常见和现代的 Web 开发技术。

应用程序分为两个主要部分：一个“底层”部分，负责从选定的 ADC 输入（默认为 IN0）进行模数转换；另一部分使用 ioLibrary_Driver 模块处理 HTTP 请求。假定所有 Web 资源都放置在 SD 卡上，并通过 FatFs 模块和作者开发的 SPI 兼容驱动程序进行访问。然而，为了简化开发过程，该应用程序还能够使用 ARM 半托管调用和常规 C 标准库函数从开发者 PC 提供内容。

以下代码片段与 main() 函数相关。为了获取随时间变化的信号（例如 50Hz 正弦波），我们需要以固定间隔执行 ADC 转换。因此，我们使用 TIM2 定时器¹⁸ 来驱动 ADC1 外设，该外设被配置为以 DMA 循环模式工作：这样定时器将连续触发转换。ADC 以 DMA 模式启动（第 145 行），转换后的值存储在 _adcConv 数组中。在第 140 行实例化的 adcSem 信号量将用于控制对 _adcConv 数组的访问，该数组保存 ADC 转换后的值。其作用将在后文进一步解释。

¹⁵http://getbootstrap.com/ ¹⁶https://jquery.com/ ¹⁷https://d3js.org/ ¹⁸ 此处展示的源代码与 Nucleo-F401RE 开发板相关。

<!-- page: 784 -->

```text
Filename: src/ch25/main-ex2.c
135
int main(void) {
136
HAL_Init();
137
Nucleo_BSP_Init();
138
139
osSemaphoreDef(adcSem);
140
adcSemID = osSemaphoreCreate(osSemaphore(adcSem), 1);
141
142
MX_ADC1_Init();
143
MX_TIM2_Init();
144
HAL_TIM_Base_Start(&htim2);
145
HAL_ADC_Start_DMA(&hadc1, (uint32_t*)_adcConv, 200);
146
147
MX_SPI1_Init();
148
149
#if defined(_USE_SDCARD_) && !defined(OS_USE_SEMIHOSTING)
150
SD_SPI_Configure(SD_CS_GPIO_Port, SD_CS_Pin, &hspi1);
151
MX_FATFS_Init();
152
153
if(f_mount(&diskHandle, "0:", 1) != FR_OK) {
154
#ifdef DEBUG
155
asm("BKPT #0");
156
#else
157
while(1) {
158
HAL_Delay(500);
159
HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
160
}
161
#endif //#ifdef DEBUG
162
}
163
164
#ifdef OS_USE_TRACE_ITM
/* Prints the SD content over the ITM port */
TCHAR buff[256];
strcpy(buff, (char*)L"/");
scan_files(buff);
169
#endif //#ifdef OS_USE_TRACE_ITM
170
171
#endif //#if defined(_USE_SDCARD_) && !defined(OS_USE_SEMIHOSTING)
172
173
osThreadDef(w5500, SetupW5500Thread, osPriorityNormal, 0, 512);
174
osThreadCreate(osThread(w5500), NULL);
175
176
osKernelStart();
177
/* Never coming here, but just in case... */
178
while(1);
179
}
```

<!-- page: 785 -->

如果全局宏 _USE_SDCARD_ 已设置，且未使用 ARM 半托管（即全局宏 OS_USE_SEMIHOSTING 未设置），则意味着 Web 资源（HTML 文件、图像和 CSS/JS 脚本文件）存储在插入 W5500 扩展板卡座中的 MicroSD 卡上。因此，FatFs 库被初始化（第 [150:151] 行），并挂载第一个分区（第 153 行）。此外，如果我们使用能够读取 ITM 刺激的调试器，我们将通过调用 scan_files() 例程（已在第 25 章中展示）在 SWV 控制台上打印 SD 卡的内容。

### 最后启动 SetupW5500Thread() 线程，该线程负责配置 W5500 IC 并处理传入的 HTTP 请求。其代码很简单，如下所示。

```text
Filename: src/ch25/main-ex2.c
181
void SetupW5500Thread(void const *argument) {
182
UNUSED(argument);
183
184
/* 配置 W5500 模块 */
185
IO_LIBRARY_Init();
186
187
/* 配置 HTTP 服务器 */
188
httpServer_init(TX_BUF, RX_BUF, MAX_HTTPSOCK, socknumlist);
189
reg_httpServer_cbfunc(NVIC_SystemReset, NULL);
190
191
/* 开始处理套接字 */
192
while(1) {
193
for(uint8_t i = 0; i < MAX_HTTPSOCK; i++)
194
httpServer_run(i);
195
/* 我们仅延迟 1ms，以便执行具有相同
196
* 或较低优先级的其他线程 */
197
osDelay(1);
198
}
199
}
```

该线程通过调用函数 IO_LIBRARY_Init()（如下所示）开始配置 W5500 IC 和 ioLibrary_Driver 库。接下来，配置 HTTP 服务器（第 188 行），并在无限循环中为分配给 HTTP 服务器的每个套接字调用 httpServer_run() 函数。

```text
Filename: src/ch25/main-ex2.c
79
void IO_LIBRARY_Init(void) {
80
uint8_t runApplication = 0, dhcpRetry = 0, phyLink = 0, bufSize[] = {2, 2, 2, 2, 2};
81
wiz_NetInfo netInfo;
```

82

```text
83
reg_wizchip_cs_cbfunc(cs_sel, cs_desel);
84
reg_wizchip_spi_cbfunc(spi_rb, spi_wb);
85
reg_wizchip_spiburst_cbfunc(spi_rb_burst, spi_wb_burst);
86
reg_wizchip_cris_cbfunc(vPortEnterCritical, vPortExitCritical);
```

87

```text
88
wizchip_init(bufSize, bufSize);
```

<!-- page: 786 -->

89

```text
90
ReadNetCfgFromFile(&netInfo);
```

91

```text
92
/* 等待以太网电缆插入 */
93
do {
94
ctlwizchip(CW_GET_PHYLINK, (void*) &phyLink);
95
osDelay(10);
96
} while(phyLink == PHY_LINK_OFF);
```

97

```text
98
if(netInfo.dhcp == NETINFO_DHCP) { /* DHCP 模式 */
99
DHCP_init(DHCP_SOCK, RX_BUF);
100
101
while(!runApplication) {
102
switch(DHCP_run()) {
103
case DHCP_IP_LEASED:
104
case DHCP_IP_ASSIGN:
105
case DHCP_IP_CHANGED:
106
getIPfromDHCP(netInfo.ip);
107
getGWfromDHCP(netInfo.gw);
108
getSNfromDHCP(netInfo.sn);
109
getDNSfromDHCP(netInfo.dns);
110
runApplication = 1;
111
break;
112
case DHCP_FAILED:
113
dhcpRetry++;
114
if(dhcpRetry > MAX_DHCP_RETRY)
115
{
116
netInfo.dhcp = NETINFO_STATIC;
117
DHCP_stop();
// 如果重启，重新调用 DHCP_init()
118
#ifdef _MAIN_DEBUG_
119
printf(">> DHCP %d Failed\r\n", my_dhcp_retry);
120
Net_Conf();
121
Display_Net_Conf();
// 将静态网络信息打印到串口
122
#endif
123
dhcpRetry = 0;
124
asm("BKPT #0");
125
}
126
break;
127
default:
128
break;
129
}
130
}
131
}
132
wizchip_setnetinfo(&netInfo);
133
}
```

## IO_LIBRARY_Init() 函数负责正确配置 W5500 IC。它首先

<!-- page: 787 -->

配置用于通过 SPI 总线交换数据的函数（第 [83:88] 行，如本章第一个示例所示）。接下来，在第 90 行，使用函数 ReadNetCfgFromFile() 从存储在 SD 卡中的文件检索网络配置。该文件名为 net.cfg，且必须具有以下结构：

```text
1
NODHCP
2
0:11:22:33:44:55
3
192.168.1.165
4
255.255.255.0
5
192.168.1.1
6
8.8.8.8
```

第一行可以取值（NODHCP 和 DHCP），指示网络 IP 是静态配置还是动态配置。第二行对应 MAC 地址，接下来的四行分别对应设备 IP、子网掩码、网络网关和主 DNS。通过读取此文件的内容，网络接口会自动配置。用户可以通过专用网页修改网络参数，如图 26.8 所示。

一旦从配置文件检索到网络设置，IO_LIBRARY_Init() 函数将进入无限循环，直到 LAN 电缆插入 RJ45 端口（第 [93:96] 行）。当这种情况发生时，如果网络接口配置为 DHCP 模式，该函数将启动 DHCP 发现过程。最后，在第 132 行，使用存储在 net.cfg 文件中的设置或从同一网络上的 DHCP 服务器检索到的设置来配置网络接口。

![Image from PDF page 787](../images/page-0787-image-01.jpeg)

图 26.8：用于设置网络设置的网页

应用程序的其余部分基本上由 HTTP 服务器组成。当套接字与远程对等方建立连接时，httpServer_run() 例程会调用 http_process_handler() 函数，该函数负责处理传入的 HTTP 请求。

<!-- page: 788 -->

## 该函数开始分析请求的 HTTP 方法（GET、POST、PUT 等）。这里我们关注 GET 方法的处理方式。

```text
Filename: Middlewares/ioLibrary_Driver/Internet/httpServer/httpServer.c
531
case METHOD_GET :
532
get_http_uri_name(p_http_request->URI, uri_buf);
533
uri_name = uri_buf;
534
535
// 如果 URI 是 "/"，则响应 index.html
536
if (!strcmp((char *)uri_name, "/")) strcpy((char *)uri_name, INITIAL_WEBPAGE);
537
if (!strcmp((char *)uri_name, "m")) strcpy((char *)uri_name, M_INITIAL_WEBPAGE);
538
if (!strcmp((char *)uri_name, "mobile")) strcpy((char *)uri_name, MOBILE_INITIAL_WEBPAGE);
539
// 检查请求的文件类型（包括 HTML、TEXT、GIF、JPEG 等）
540
find_http_uri_type(&p_http_request->TYPE, uri_name);
541
542
#ifdef _HTTPSERVER_DEBUG_
543
printf("\r\n> HTTPSocket[%d] : HTTP Method GET\r\n", s);
544
printf("> HTTPSocket[%d] : Request Type = %d\r\n", s, p_http_request->TYPE);
545
printf("> HTTPSocket[%d] : Request URI = %s\r\n", s, uri_name);
546
#endif
547
548
if(p_http_request->TYPE == PTYPE_CGI)
549
{
550
content_found = http_get_cgi_handler(uri_name, pHTTP_TX, &file_len);
551
if(content_found && (file_len <= (DATA_BUF_SIZE-(strlen(RES_CGIHEAD_OK)+8))))
552
{
553
send_http_response_cgi(s, http_response, pHTTP_TX, (uint16_t)file_len);
554
}
555
else
556
{
557
send_http_response_header(s, PTYPE_CGI, 0, STATUS_NOT_FOUND);
558
}
559
}
560
else
561
{
562
// 查找用于 Web 内容的用户注册索引
563
if(find_userReg_webContent(uri_buf, &content_num, &file_len))
564
{
565
content_found = 1; // 在代码闪存中找到 Web 内容
566
content_addr = (uint32_t)content_num;
567
HTTPSock_Status[get_seqnum].storage_type = CODEFLASH;
568
}
569
// 非 CGI 请求，请求的是 'SD 卡' 或 '数据闪存' 中的 Web 内容
570
#if defined(_USE_SDCARD_) && !defined(OS_USE_SEMIHOSTING)
571
#ifdef _HTTPSERVER_DEBUG_
572
printf("\r\n> HTTPSocket[%d] : Searching the requested content\r\n", s);
573
#endif
```

<!-- page: 789 -->

```text
574
if((fr = f_open(&HTTPSock_Status[get_seqnum].fs, (const char *)uri_name, FA_READ)) == 0)
575
{
576
content_found = 1; // 文件打开成功
577
578
file_len = f_size(&HTTPSock_Status[get_seqnum].fs);
579
HTTPSock_Status[get_seqnum].file_len = file_len;
580
strcpy(HTTPSock_Status[get_seqnum].file_name, uri_name);
581
HTTPSock_Status[get_seqnum].storage_type = SDCARD;
582
}
583
#elif defined(OS_USE_SEMIHOSTING)
584
// 非 CGI 请求，通过 ARM Semihosting 检索 Web 内容
585
char *base_path = OS_BASE_FS_PATH;
586
char *path;
587
588
path = malloc(sizeof(char)*strlen(base_path)+strlen(uri_name));
589
strcpy(path, base_path);
590
strcpy(path+strlen(base_path), uri_name);
591
592
HTTPSock_Status[get_seqnum].fs = fopen((const char *)path,"r");
593
if(HTTPSock_Status[get_seqnum].fs != NULL) {
594
content_found = 1; // 文件打开成功
595
596
fseek(HTTPSock_Status[get_seqnum].fs, 0L, SEEK_END);
597
file_len = ftell(HTTPSock_Status[get_seqnum].fs);
598
HTTPSock_Status[get_seqnum].file_len = file_len;
599
fseek(HTTPSock_Status[get_seqnum].fs, 0L, SEEK_SET);
600
strcpy(HTTPSock_Status[get_seqnum].file_name, uri_name);
601
HTTPSock_Status[get_seqnum].storage_type = SDCARD;
602
}
603
}
```

## 第 532 行的 get_http_uri_name() 函数获取客户端应用程序请求的 URL。如果该 URL 仅等于 "/"，则表示浏览器正在请求默认 URL，这对应于 index.html 文件。第 541 行对 find_http_uri_type() 函数的调用确定与所请求 URL 关联的 Content-Type（内容类型）。Content-Type 是根据文件扩展名推导出来的。例如，以 .gif 结尾的文件的 Content-Type 被设置为 PTYPE_GIF。

## 如果 Content-Type 是 CGI¹⁹（第 549 行），则调用 http_get_cgi_handler() 函数来确定动态内容的生成。我们稍后将会分析该函数的结构。对于所有其他已注册的 Content-Type（请查看 find_http_uri_type() 的实现以获取完整列表），http_process_handler() 函数开始查找所请求的资源（第 561 行）。首先，该函数检查内容是否已通过 reg_httpServer_webContent() 函数注册。如果是，则内容会自动从闪存中

¹⁹通用网关接口（Common Gateway Interface, CGI）是一种标准化协议，用于接口“服务器应用程序”，以动态处理来自客户端的请求。历史上，CGI 被引入以动态生成 Web 内容。如今，这种 Web 应用程序中的服务器处理方式已被大量使用动态且更强大的脚本语言（如 PHP、Python 和 Ruby）构建的 Web 框架所取代。

<!-- page: 790 -->

## 内存中检索并发送到浏览器。如果内容未存储在 MCU 闪存中，且设置了 _USE_SDCARD_ 宏，则该函数检查所请求的内容是否存储在 MicroSD 卡内（第 [575:584] 行）。使用 FatFs API 来访问所请求的文件。相反，如果启用了 ARM 半托管（semihosting），则使用标准 C 例程从开发人员的 PC 上检索文件（第 [586:605] 行）。

## http_get_cgi_handler() 函数负责生成 Web 应用程序的动态内容（例如，由 ADC 外设采样的数据）。该函数的编码方式是请求访问 /adc.cgi 和 /network.cgi 动态页面。让我们从第二个页面开始。

```text
Filename: Middlewares/ioLibrary_Driver/Internet/httpServer/httpUtil.c
22
extern ADC_HandleTypeDef hadc1;
23
extern uint16_t adcConv[100], _adcConv[200];
24
extern TIM_HandleTypeDef htim2;
25
extern osSemaphoreId adcSemID;
```

26

```text
27
uint8_t http_get_cgi_handler(uint8_t * uri_name, uint8_t * buf, uint32_t * file_len)
28
{
29
uint8_t ret = HTTP_FAILED;
30
uint16_t len = 0;
```

31

```text
32
if(strcmp((const char*)uri_name, "adc.cgi") == 0) {
33
char *pbuf = (char*)buf;
```

34

```text
35
/* Compute the current TIM2 frequency */
36
uint32_t freq = HAL_RCC_GetPCLK2Freq() / (((htim2.Init.Prescaler + 1) *
37
(htim2.Init.Period + 1)));
38
pbuf += sprintf(pbuf, "{\"f\":%lu,\"d\":[", freq);
```

39

```text
40
/* Wait until the HAL_ADC_ConvCpltCallback() or
41
HAL_ADC_HalfConvCpltCallback() finish */
42
osSemaphoreWait(adcSemID, osWaitForever);
43
for(uint8_t i = 0; i < 100; i++)
44
pbuf += sprintf(pbuf, "%.2f,", adcConv[i]*0.805);
45
osSemaphoreRelease(adcSemID);
```

46

```text
47
sprintf(--pbuf, "]}");
48
*file_len = strlen((char*)buf);
```

49

```text
50
return HTTP_OK;
```

51

```text
52
} else if(strcmp((const char*)uri_name, "network.cgi") == 0) {
53
wiz_NetInfo ni;
54
wizchip_getnetinfo(&ni);
55
sprintf((char*)buf, "{\"ip\":\"%d.%d.%d.%d\","
56
"\"nm\":\"%d.%d.%d.%d\","
57
"\"gw\":\"%d.%d.%d.%d\","
```

<!-- page: 791 -->

```text
58
"\"dns\":\"%d.%d.%d.%d\","
59
"\"dhcp\":\"%d\"}", ni.ip[0], ni.ip[1], ni.ip[2], ni.ip[3],
60
ni.sn[0], ni.sn[1], ni.sn[2], ni.sn[3],
61
ni.gw[0], ni.gw[1], ni.gw[2], ni.gw[3],
62
ni.dns[0], ni.dns[1], ni.dns[2], ni.dns[3],
63
ni.dhcp);
64
*file_len = strlen((char*)buf);
65
return HTTP_OK;
66
}
```

67

```text
68
if(ret) *file_len = len;
```

network.cgi 页面执行一个简单的操作：它将当前的网络设置返回给 /network.html 页面，后者进而向 /network.cgi 页面发起 AJAX 调用。为了确保所有读者都理解这一点，假设您的 Nucleo 可以通过 IP 地址 192.168.1.165 访问，那么在您的 Web 浏览器中访问 URL http://192.168.1.165/network.cgi²⁰ 将得到以下结果：

```text
{"ip":"192.168.1.165","nm":"255.255.255.0","gw":"192.168.1.1","dns":"8.8.8.8","dhcp":"1"}
```

这对应于以 JSON 格式返回的网络设置。当浏览器访问 /adc.cgi 动态页面时，应用程序以 JSON 格式返回当前的 TIM2 频率和 ADC 采样数据。第 [32:52] 行负责此操作。http_get_cgi_handler() 函数从第 36 行开始推导定时器频率。Web 应用程序将使用此信息在图表上绘制数据。第 [42:45] 行代表了该函数的“棘手部分”。

ADC 转换以 DMA 循环模式执行。转换自行持续进行，且此操作由 TIM2 定时器驱动。如果定时器运行速度很快，访问 _adcConv[] 数组可能会导致竞态条件：在 http_get_cgi_handler() 于第 44 行将其转换为字符串时，其内容可能会被修改。应用程序的组织方式如下：当调用 HAL_ADC_ConvHalfCpltCallback() 和 HAL_ADC_ConvCpltCallback() 例程时，_adcConv[] 数组内容的一半会被复制到 adcConv[] 数组中，如下所示。

```text
Filename: src/ch25/main-ex2.c
259
void HAL_ADC_ConvHalfCpltCallback(ADC_HandleTypeDef* hadc) {
260
UNUSED(hadc);
261
262
if(osSemaphoreWait(adcSemID, 0) == osOK) {
263
memcpy(adcConv, _adcConv, sizeof(uint16_t)*100);
264
osSemaphoreRelease(adcSemID);
265
}
266
}
267
```

²⁰http://192.168.1.165/network.cgi

<!-- page: 792 -->

```text
268
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc) {
269
UNUSED(hadc);
270
271
if(osSemaphoreWait(adcSemID, 0) == osOK) {
272
memcpy(adcConv, _adcConv+100, sizeof(uint16_t)*100);
273
osSemaphoreRelease(adcSemID);
274
}
275
}
```

## 当 HAL_ADC_ConvHalfCpltCallback() 函数被调用时，_adcConv[] 数组中已存储了一百个值：因此我们将前半部分复制到大小为 100 的 adcConv[] 数组中。当另一个回调被调用时，我们复制后半部分。在这两个回调例程复制 _adcConv[] 数组的内容之前，它们会尝试获取信号量 adcSem。如果可用，它们执行复制；否则，这意味着 http_get_cgi_handler() 已经获取了该信号量，并且正在对 adcConv[] 数组进行转换。此方案防止了竞态条件的产生，尽管它不是最快的方案。

## 函数 http_get_cgi_handler() 处理所有针对 CGI 脚本的 GET 请求。类似地，函数 http_post_cgi_handler() 处理所有针对 CGI 脚本的 POST 请求。

```text
Filename: Middlewares/ioLibrary_Driver/Internet/httpServer/httpUtil.c
72
uint8_t http_post_cgi_handler(uint8_t * uri_name, st_http_request * p_http_request, uint8_t * \
73
buf, uint32_t * file_len)
74
{
75
uint8_t ret = HTTP_OK;
76
uint16_t len = 0;
77
uint8_t *param = p_http_request->URI;
```

78

```text
79
if(strcmp((const char *)uri_name, "sf.cgi") == 0) {
80
param = get_http_param_value((char*)p_http_request->URI, "f");
81
if(param != p_http_request->URI) {
82
/* 用户希望更改 ADC 采样频率。因此我们停止转换 */
83
HAL_ADC_Stop_DMA(&hadc1);
84
HAL_TIM_Base_Stop(&htim2);
```

85

```text
86
/* 获取当前的 TIM2 频率 */
87
uint32_t cfreq = HAL_RCC_GetPCLK2Freq() / (((htim2.Init.Prescaler + 1) *
88
(htim2.Init.Period + 1))), nfreq = 0;
```

89

```text
90
if(*param == '1')
91
nfreq = cfreq * 2;
92
else
93
nfreq = cfreq / 2;
```

94

```text
95
htim2.Init.Prescaler = 0;
96
htim2.Init.Period = 1;
```

<!-- page: 793 -->

```text
97
/* 我们循环直到达到所需的频率。在低于 30Hz 的频率下，
98
此算法效率极低 */
99
while(1) {
100
cfreq = HAL_RCC_GetPCLK2Freq() / (((htim2.Init.Prescaler + 1) *
101
(htim2.Init.Period + 1)));
102
if (nfreq < cfreq) {
103
if(++htim2.Init.Period == 0) {
104
htim2.Init.Prescaler++;
105
htim2.Init.Period++;
106
}
107
} else {
108
break;
109
}
110
}
111
HAL_TIM_Base_Init(&htim2);
112
HAL_TIM_Base_Start(&htim2);
113
HAL_ADC_Start_DMA(&hadc1, (uint32_t*)_adcConv, 200);
114
115
sprintf((char*)buf, "OK");
116
len = strlen((char*)buf);
117
}
118
119
}
120
else if(strcmp((const char *)uri_name, "network.cgi") == 0) {
121
wiz_NetInfo netInfo;
122
wizchip_getnetinfo(&netInfo);
123
124
param = get_http_param_value((char*)p_http_request->URI, "dhcp");
125
if(param != 0) {
126
netInfo.dhcp = NETINFO_DHCP;
127
} else {
128
netInfo.dhcp = NETINFO_STATIC;
129
130
param = get_http_param_value((char*)p_http_request->URI, "ip");
131
if(param != 0)
132
inet_addr_((u_char*)param, netInfo.ip);
133
else
134
return HTTP_FAILED;
135
136
param = get_http_param_value((char*)p_http_request->URI, "sn");
137
if(param != 0)
138
inet_addr_((u_char*)param, netInfo.sn);
139
else
140
return HTTP_FAILED;
141
142
param = get_http_param_value((char*)p_http_request->URI, "gw");
143
if(param != 0)
```

<!-- page: 794 -->

```text
144
inet_addr_((u_char*)param, netInfo.gw);
145
else
146
return HTTP_FAILED;
147
148
param = get_http_param_value((char*)p_http_request->URI, "dns");
149
if(param != 0)
150
inet_addr_((u_char*)param, netInfo.dns);
151
else
152
return HTTP_FAILED;
153
}
154
if(!WriteNetCfgInFile(&netInfo))
155
sprintf((char*)buf, "FAILED");
156
else
157
sprintf((char*)buf, "OK");
158
159
/* 更改网络参数 */
160
wizchip_setnetinfo(&netInfo);
161
len = strlen((char*)buf);
162
}
163
164
if(ret) *file_len = len;
```

该函数被编码为服务于两个动态页面：/sf.cgi 和 /network.cgi。后者处理当用户更改网络设置时对 HTML 表单的处理（参见 network.html 文件）。而 /sf.cgi 页面则处理 TIM2 频率的更改。当用户点击“放大/缩小”图标时，浏览器向 /sf.cgi 页面发起请求，通过传递值 1 来增加频率，传递 0 来降低频率。

我们示例应用程序的其余部分全部涉及 HTML、CSS 和 JavaScript。文件 index.html 和 network.html 包含使用 D3js 库绘制图表以及显示和更改网络设置所需的所有代码。

要使用此示例，您可以简单地将 src/ch25/webpages 子目录的内容复制到 SD 卡上。或者，您可以在 PC 文件系统中将宏 OS_BASE_FS_PATH 设置为指向 src/ch25/webpages 的完整路径后，使用 ARM 半主机功能。例如，如果您在 Windows 上，OS_BASE_FS_PATH 可以设置为 C:/STM32Toolchain/projects/nucleof401RE/src/ch25/webpages 路径。
