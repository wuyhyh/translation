<!-- page: 763 -->

# 26. 开发物联网应用

在这个互联的世界里，越来越多的设备接入了网络。汽车、洗衣机和冰箱等家用电器、灯具、百叶窗、恒温器，以及用于环境监测的传感器，都是如今通过互联网交换消息的设备。许多人认为，我们正处于物联网（Internet of Things，IoT）时代。很难断言物联网是否会为电子行业带来一个新的黄金时代，但可以肯定的是，许多半导体公司正在这一领域投入数十亿美元。

物联网是一个含义宽泛的术语，并未说明通信标准、协议、应用层，甚至系统架构。物联网通信协议和技术种类繁多，纷繁复杂。仅无线通信协议就有数十种标准，例如 Wi-Fi、Bluetooth、Zigbee、LoRaWAN、TI 的 SimpliciTI 和 Microchip 的 MiWi 等专有方案，以及 5G/4G 移动网络。通信频段也有很多种。例如，2.4GHz 和 5.8GHz 是全球通用的无线通信频段；此外还有一些区域性或可选频段，如欧盟的 868MHz（美国为 915MHz）、欧盟和美国部分地区使用的 434MHz，以及欧盟大部分地区和日本使用的 169MHz。每种标准都有自己的发射功率、占空比等限制，也各有优缺点。

通信介质和协议的选择也会影响应用架构。例如，支持 Wi-Fi 或以太网的设备只需通过集成调制解调器的路由器即可连接到互联网。使用专有协议的设备（例如 Zigbee 设备）通常需要中间设备（控制单元），由它收集消息并通过互联网发送到集中式服务器（如今通常称为云服务器）。对于某些“工业”应用，这通常是一个优势（即使没有互联网连接，本地设备也可以继续工作）；但对于消费级应用，这通常会阻碍用户采用该解决方案。

如今，多家芯片制造商推出了集成有线或无线连接功能的微控制器。Texas Instruments 收购 ChipCon 后，开发了多款集成射频前端的 MCU。例如，CC2540 是一款采用 8051 内核、集成 2.4GHz 射频的 MCU，面向 Bluetooth 应用；CC3200 则采用 Cortex-M4 内核，集成了可按 Wi-Fi 标准通信的 2.4GHz 射频。最近，市场上又出现了一家厂商：Espressif¹ 是一家中国公司，推出了 ESP32³——一款运行频率为 240MHz、集成 2.4GHz 射频和 MAC 层的双核 Tensilica² LX6 微控制器。这些 MCU 小批量采购时价格不到 5 美元，因此在创客群体中颇受欢迎。

本章为未配备以太网控制器的 Nucleo-64 开发板用户提供一种解决方案：使用 WIZnet⁴ 的 W5500 网络处理器。WIZnet 是一家专门设计此类器件的韩国公司。该公司凭借 W5100 IC 获得了广泛知名度；这款 IC 曾用于开发广受欢迎的 Arduino Ethernet Shield⁵。我们将介绍如何使用 Nucleo 开发带有集成 Web 服务器的嵌入式应用。在此之前，先简要介绍 ST 基于 CubeHAL 提供的物联网应用开发方案。

¹ https://espressif.com/  
² Tensilica 是一家类似 ARM 的公司，负责设计 IP 内核，再由芯片制造商将其实现为芯片。Tensilica 目前归 Cadence 所有；Cadence 也开发 Allegro CAD。  
³ https://bit.ly/2dN52fx

<!-- page: 764 -->

## 26.1 ST 提供的物联网应用开发解决方案

如前所述，STM32F1/F2/F4/F7 系列中的多款微控制器集成了以太网控制器，支持介质无关接口（Media-Independent Interface，MII）及其变体精简型介质无关接口（Reduced MII，RMII）。这类接口屏蔽了具体物理介质的差异，使以太网控制器的 MAC 层能够连接到物理层收发器（PHY）芯片。市场上有多种 LAN PHY 芯片，MAC 与 PHY 之间的通信由底层 MII 协议处理。

然而，仅有专用硬件接口还不足以快速构建物联网应用；还需要完整的 TCP/IP 协议栈。对于单个开发者而言，从头处理如此复杂的协议栈几乎不可能。ST 没有自行开发协议栈，而是采用了轻量级 IP（Lightweight IP，LwIP）。LwIP 是由 Adam Dunkels 发起、现由大型社区维护的开源框架。Altera、Xilinx 和 Freescale 等多家半导体公司也参与了这一复杂框架的开发。

ST 已将 LwIP 集成到 CubeMX 中；启用以太网控制器后，CubeMX 会自动向项目添加使用该框架所需的文件，并将 LwIP 列为可选中间件。ST 会持续维护和支持该框架。

以下是 LwIP 的最相关特性：

- IP（互联网协议，IPv4 和 IPv6），包括通过多个网络接口的数据包转发
- ICMP（互联网控制消息协议），用于网络维护和调试
- IGMP（互联网组管理协议），用于组播流量管理
- MLD（IPv6 组播侦听发现）
  - 旨在符合 RFC 2710；不支持 MLDv2。
- ND（IPv6 邻居发现和无状态地址自动配置）
  - 旨在符合 RFC 4861（邻居发现）和 RFC 4862（地址自动配置）。
- UDP（用户数据报协议），包括实验性的 UDP-lite 扩展

⁴ http://www.wiznet.co.kr/  
⁵ http://bit.ly/2dMXhGi

<!-- page: 765 -->

- TCP（传输控制协议），具有拥塞控制、RTT 估计和快速恢复/快速重传
- 用于提升性能的原始套接字 API
- 可选的类 Berkeley 套接字 API
- DNS（域名解析器）

LwIP 还为以下应用协议提供完整实现：

- 支持 SSI 和 CGI 的 HTTP 服务器
- 带有 MIB 编译器的 SNMPv2c 代理（简单网络管理协议）
- SNTP（简单网络时间协议）
- NetBIOS 名称服务响应器
- mDNS（组播 DNS）响应器
- iPerf 服务器实现

由于配备 Nucleo-64 板的 STM32 微控制器缺乏 RMII 接口，我将不会在此详细列出在应用中设置 LwIP 所需的步骤。有关此内容的更多信息，请参阅 CubeHAL 示例。此外，你可以在我的博客上找到一些关于此主题的文章。最后，CubeMXImporter 工具实现了所有必要的逻辑，以将 LwIP 协议栈导入 GNU MCU Eclipse 项目。

无线协议在物联网中起着重要作用。ST 注意到多种无线标准的重要性，并以两个专用 STM32 系列进入这一市场：STM32WB 和 STM32WL。前者面向 2.4 GHz 射频应用，支持 Bluetooth 5.2、Bluetooth Mesh 以及该频段内的其他协议，例如 Zigbee 3.0。后者 STM32WL 系列则面向 Sub-GHz 频段，覆盖 169 MHz 至 915 MHz。此外，ST 与 Semtech 建立了合作伙伴关系，以开发兼容 LoRa（Long Range Alliance）技术的定制解决方案。得益于这一合作，STM32WL 系列集成了支持 LoRaWAN™ 协议的 Semtech LoRa 收发器。ST 还提供了专用 Nucleo 开发板，用于 STM32WL 和 STM32WB 系列。

<!-- page: 766 -->

<p align="center"><img src="../images/page-0766-image-01.jpeg" alt="图 26.1：Nucleo-WB55 开发板"></p>

<p align="center">图 26.1：Nucleo-WB55 开发板</p>

## 26.2 W5500 以太网控制器

除了较新的 Nucleo-144 开发板外，其他 Nucleo-64 和 Nucleo-32 开发板均未提供集成以太网控制器的 STM32 微控制器（MCU）。这意味着，如果您希望在 Nucleo-64 上开发物联网（IoT）应用，就需要使用外部扩展板。

WIZnet 是一家韩国公司，其知名度得益于 Arduino 开发板。事实上，其首款以太网控制器 W5100 IC 正是用于创建 Arduino 以太网扩展板的芯片。自 W5100 控制器以来，WIZnet 持续迭代开发了其他类似产品。其中表现最佳的产品之一是 W5500，我们将在本章中对其进行研究。

W5500 是一款单片式以太网控制器，集成了 LAN 物理层（PHY）。此外，它还是一个完整的网络处理器，内置由硬件实现的 TCP/IP 协议栈。该芯片通过高速 SPI 接口与主机微控制器交换数据，SPI 最高支持 80MHz。其主要特性如下：

- 支持 TCP、UDP、ICMP、IPv4、ARP、IGMP、PPPoE
- 支持同时使用 8 个独立套接字（socket）
- 支持掉电模式（Power down mode）
- 支持基于 UDP 的局域网唤醒（Wake on LAN）
- 支持高速串行外设接口（SPI MODE 0, 3），最高达 80MHz
- 内部 32 KB 存储器用作 TX/RX 缓冲区

<!-- page: 767 -->

- 嵌入式 10BaseT/100BaseTX 以太网 PHY
- 支持自动协商（全双工和半双工，10 和 100 速率）
- 3.3V 工作电压，具备 5V I/O 信号容限
- LED 输出指示（全/半双工、链路、速率、活动状态）
- 48 引脚 LQFP 无铅封装（7x7mm，0.5mm 间距）

<p align="center"><img src="../images/page-0767-image-01.jpeg" alt="图 26.2：由 STM32F0 微控制器（左侧）和 W5500 IC（右侧）组成的定制设备"></p>

<p align="center">图 26.2：由 STM32F0 微控制器（左侧）和 W5500 IC（右侧）组成的定制设备</p>

W5500 IC 易于集成到定制设计中。它只需一个晶振、少量无源元件和一个 LAN 隔离变压器即可工作；芯片还集成了驱动该变压器所需的电荷泵。我曾在多个定制设计中成功使用这款芯片。由于整个 TCP/IP 协议栈都集成在网络处理器中，W5500 甚至可以与低成本 STM32F0 微控制器配合使用。此外，对于小批量生产，与采用集成以太网控制器并外接专用 LAN PHY 的高性能微控制器相比，使用 W5500 配合低成本 STM32 微控制器通常更方便。图 26.2 展示了作者制作的一种定制设计：由 STM32F030 微控制器驱动 W5500 IC，静态网页存储在外部 SPI Flash 存储器中。

WIZnet 开发了一款兼容 Arduino 的扩展板（见图 26.3），配合 Nucleo 开发板即可开箱使用。该扩展板还集成了 MicroSD 卡读卡器，并与 W5500 IC 共用同一个 SPI 端口。因此，网页及其他静态内容（图像、CSS、JavaScript 文件等）可以存储在外部 SD 卡上。

<!-- page: 768 -->

<p align="center"><img src="../images/page-0768-image-01.jpeg" alt="图 26.3：WIZnet 的 W5500 以太网扩展板"></p>

<p align="center">图 26.3：WIZnet 的 W5500 以太网扩展板</p>

W5500 等网络处理器的工作方式很直接。该芯片最多提供 8 个套接字⁶，每个套接字都有一组对应的寄存器。修改这些寄存器即可控制套接字，例如打开连接、切换到监听状态以及发送或接收数据。W5500 内置 32KB 缓冲区用于套接字数据，这部分空间可以在 8 个套接字之间灵活分配，后文会进一步介绍。读写该缓冲区即可与通信对端交换数据。因此，从 MCU 的角度看，驱动这类 IC 归根结底就是通过 SPI 接口交换字节。不过，管理套接字的所有内部状态并不容易，尤其对初次接触这类 IC 的开发者而言。我曾为 W5100 编写过驱动库，深知这项工作非常耗时。此外，所有 W5X00 系列 IC（5100、5200、5300 和 5500）都存在一些棘手且文档记录不充分的缺陷，处理起来并不容易。

⁶在网络中，套接字是对复杂 TCP/IP 协议栈的抽象。它只是一个句柄，使设备能够在两台主机之间发送字节流，而不必处理复杂的底层协议（除非需要执行高级操作）。

<!-- page: 769 -->

<p align="center"><img src="../images/page-0769-image-01.png" alt="图 26.4：ioLibrary_Driver 库的架构"></p>

<p align="center">图 26.4：ioLibrary_Driver 库的架构</p>

WIZnet 大约七年前为这一系列芯片发布了专用库 ioLibrary_Driver，可从 GitHub⁷ 获取。该库的架构如图 26.4 所示，主要分为两层。其中一层名为 Ethernet（以太网），包含用于建立对等连接的基本操作。`Ethernet/socket.c` 文件包含套接字管理例程。该层的套接字 API 类似 BSD 套接字 API，但并非完全兼容。Ethernet 层还包含适用于各款 WIZnet 芯片的底层驱动程序；例如，`Ethernet/w5500.c` 包含驱动 W5500 所需的逻辑。最后，`Ethernet/wizchip_conf.h` 定义了配置该库所需的宏，稍后将进一步介绍。

Internet（互联网）层构建在 Ethernet 层之上，是多种互联网协议和服务的集合：

- DHCP 客户端
- DNS 客户端
- FTP 客户端和服务器
- SNMP 代理/陷阱
- SNTP 客户端
- TFTP 客户端
- HTTP 服务器

用户应用程序可以使用上述一个或多个协议，或直接访问 Ethernet 层来构建自定义应用程序。

⁷ https://github.com/Wiznet/ioLibrary_Driver

<!-- page: 770 -->

### 26.2.1 如何使用 W5500 扩展板和 ioLibrary_Driver 模块

如前所述，W5500 与本书中使用的全部九块 Nucleo 开发板都能无缝配合。图 26.5⁸ 展示了该扩展板的引脚定义。SPI 接口被路由至 D13、D12 和 D11 引脚，这些引脚对应于 SPI1 外设的相同引脚（Nucleo-F302R8 开发板除外，在该板上这些引脚对应于 SPI2 外设）。W5500 的从设备选择（Slave Select, SS）引脚对应于 Arduino D10 引脚，而 SD 卡的 SS 引脚对应于 Arduino D4 引脚。

<p align="center"><img src="../images/page-0770-image-01.jpeg" alt="图 26.5：W5500 扩展板的引脚定义"></p>

<p align="center">图 26.5：W5500 扩展板的引脚定义</p>

⁸该图取自 WIZnet 网站 (https://bit.ly/2dxjblH)。

<!-- page: 771 -->

> **说明：** 图 26.5 中的 D2 引脚起着重要作用。W5500 IC 可以配置为在网络接口（例如发生 IP 地址冲突）或某个套接字（例如连接建立、收到数据）发生事件时，将 INTn 引脚拉低。这样，可以将对应的 MCU 引脚配置为 `GPIO_MODE_IT_FALLING`，使 IC 拉低 INTn 时触发相应的中断请求（IRQ），从而编写异步应用程序。尤其是在将 ioLibrary_Driver 与实时操作系统（RTOS）配合使用时，中断服务例程（ISR）可以通过信号量唤醒休眠线程，由该线程执行套接字操作。

<p align="center"><img src="../images/page-0771-image-02.jpeg" alt="图 26.6：启用 INTn 引脚时需短接 1–2 号焊盘"></p>

<p align="center">图 26.6：启用 INTn 引脚时需短接 1–2 号焊盘</p>

请注意，W5500 扩展板上的 D2 引脚默认未连接到 W5500 的 INTn 引脚。若要启用该功能，如图 26.6 所示，需要在 1–2 号焊盘之间焊接一只 0603 封装、阻值为 0Ω 的电阻；用焊锡桥接这两个焊盘也可以。

<!-- page: 772 -->

#### 26.2.1.1 配置 SPI 接口

建立硬件连接后，接下来配置软件。将 ioLibrary_Driver 模块导入现有 Eclipse 项目很简单：先将整个库复制到项目根目录，再把以下路径添加到项目设置的包含路径（Include paths）列表中：

```text
"../ioLibrary_Driver/Ethernet"
"../ioLibrary_Driver/Internet"
```

最后，在 `ioLibrary_Driver/Ethernet/wizchip_conf.h` 文件中设置 `_WIZCHIP_` 宏，以指定具体的 W5XXX 芯片型号。

<!-- page: 773 -->

ioLibrary_Driver 模块与具体 MCU 及 SPI 操作例程解耦，因此可用于 STM32、AVR、Microchip MCU 等平台。我们需要提供适配函数，将该模块连接到用于操作 SPI 外设的 `HAL_SPI` 接口。

作为该库的使用者，我们需要提供 6 个回调函数，实现驱动 SPI 所需的逻辑：

- `void cs_sel()`：库需要选中 W5500 的 SS 引脚（将其拉低）时调用。
- `void cs_desel()`：库需要取消选中 W5500 的 SS 引脚（将其拉高）时调用。
- `uint8_t spi_rb()`：需要从 SPI 接口读取一个字节时调用。
- `void spi_wb(uint8_t b)`：需要通过 SPI 接口发送一个字节时调用。
- `void spi_rb_burst(uint8_t *buf, uint16_t len)`：需要通过 SPI 读取多个（超过 3 个）字节时调用的可选回调。可在此回调中使用 DMA 操作 SPI，以提高传输速度；这种方式也称为突发模式（burst mode）。
- `void spi_wb_burst(uint8_t *buf, uint16_t len)`：需要通过 SPI 发送多个（超过 3 个）字节时调用的可选回调，也可在其中使用 DMA 操作 SPI。

假设 SPI 接口已正确配置，这些回调可以实现如下：

```c
void cs_sel() {
  HAL_GPIO_WritePin(W5500_CS_GPIO_Port, W5500_CS_Pin, GPIO_PIN_RESET); // CS LOW
}

void cs_desel() {
  HAL_GPIO_WritePin(W5500_CS_GPIO_Port, W5500_CS_Pin, GPIO_PIN_SET); // CS HIGH
}

uint8_t spi_rb(void) {
  uint8_t rbuf;
  HAL_SPI_Receive(&hspi1, &rbuf, 1, HAL_MAX_DELAY);
  return rbuf;
}

void spi_wb(uint8_t b) {
  HAL_SPI_Transmit(&hspi1, &b, 1, HAL_MAX_DELAY);
}

void spi_rb_burst(uint8_t *buf, uint16_t len) {
  HAL_SPI_Receive_DMA(&hspi1, buf, len);
  while(HAL_SPI_GetState(&hspi1) == HAL_SPI_STATE_BUSY_RX);
}

void spi_wb_burst(uint8_t *buf, uint16_t len) {
  HAL_SPI_Transmit_DMA(&hspi1, buf, len);
  while(HAL_SPI_GetState(&hspi1) == HAL_SPI_STATE_BUSY_TX);
}
```

定义好与硬件相关的函数后，还要将它们注册到 ioLibrary 中。可以调用以下函数完成注册：

```c
...
reg_wizchip_cs_cbfunc(cs_sel, cs_desel);
reg_wizchip_spi_cbfunc(spi_rb, spi_wb);
reg_wizchip_spiburst_cbfunc(spi_rb_burst, spi_wb_burst);
```

至此，只需这几行代码，就完成了 ioLibrary_Driver 与 CubeHAL 的集成。

#### 26.2.1.2 配置套接字缓冲区和网络接口

现在可以开始使用 W5500 IC。首先要按照明确的流程初始化 W5500 芯片。配置好回调函数后，首先调用：

```c
int8_t wizchip_init(uint8_t* txsize, uint8_t* rxsize);
```

该函数执行两项操作：重置 W5500 IC（必需步骤），并配置每个套接字的 TX 和 RX 缓冲区大小。所有 W5X00 IC 都有两个内部共享存储区，分别用于 TX 和 RX 缓冲区；W5500 中每个存储区的容量为 16KB。这两个存储区需要在要使用的套接字之间分配。默认情况下，每个存储区会为 8 个套接字各分配 2KB。例如，如果应用程序只需要 4 个套接字，就可以将 TX 和 RX 缓冲区分别分成 4 份；如果某个套接字需要更多空间与对端交换数据，也可以为它分配更多空间，同时减少其他套接字的份额。

向 `wizchip_init()` 传入两个数组即可指定 TX 和 RX 缓冲区的分配方式，每个数组包含 8 个值。各值之和不得超过 16。比如，若应用程序只使用两个套接字，可按如下方式定义配置数组：

<!-- page: 774 -->

```c
uint8_t bufSize[] = {12, 4, 0, 0, 0, 0, 0, 0};
wizchip_init(bufSize, bufSize);
```

上面的代码为第一个套接字分配 12KB 的 TX 和 RX 缓冲区，为第二个套接字分配剩余的 4KB。只要总容量不超过 16KB，就可以灵活分配 TX 和 RX 缓冲区。

芯片初始化后，可以调用以下函数配置网络接口：

```c
void wizchip_setnetinfo(wiz_NetInfo* pnetinfo);
```

用于向库传递网络配置参数的 `wiz_NetInfo` 结构体定义如下：

```c
typedef struct wiz_NetInfo_t {
  uint8_t mac[6];  /* Source Mac Address */
  uint8_t ip[4];   /* Source IP Address */
  uint8_t sn[4];   /* Subnet Mask */
  uint8_t gw[4];   /* Gateway IP Address (optional) */
  uint8_t dns[4];  /* DNS server IP Address (optional) */
  dhcp_mode dhcp;  /* 1 - Static, 2 - DHCP (optional) */
} wiz_NetInfo;
```

这里不再逐一解释这些字段。例如，要将 W5500 配置为连接到 `192.168.1.0/24` 子网，可以这样设置：

```c
wiz_NetInfo netInfo = {.mac = {0x00, 0x08, 0xdc, 0xab, 0xcd, 0xef}, // Mac address
                       .ip  = {192, 168, 1, 192},                   // IP address
                       .sn  = {255, 255, 255, 0},                   // Subnet mask
                       .gw  = {192, 168, 1, 1}};                    // Gateway address
wizchip_setnetinfo(&netInfo);
```

> **注意：** 此处使用的是任意 MAC 地址。在私有网络和测试环境中这样做没有问题；但如果要销售基于 W5500 的产品，则不能使用任意地址，而必须向 IEEE 购买有效的 MAC 地址块（每块包含 4096 个地址，起价约 800 美元⁹）。另一种选择是购买 Microchip 预编程的 IC¹⁰；这些 IC 带有有效的 IEEE EUI-48 或 EUI-64 MAC 地址，工作方式类似于 I²C EEPROM。对于小批量生产，这通常比购买自定义 MAC 地址更合适。

⁹ https://bit.ly/34HObty  
¹⁰ https://bit.ly/2dKLLhA

<!-- page: 775 -->

### 26.2.2 套接字 API

ioLibrary_Driver 模块提供了一组用于操作套接字的 API，其设计风格类似 BSD 套接字 API。虽然它并不完全兼容 BSD API，但熟悉 BSD API 的开发者会很容易上手。

要初始化一个新的套接字，我们可以使用以下函数：

```c
int8_t socket(uint8_t sn, uint8_t protocol, uint16_t port, uint8_t flag);
```

其中：

- `sn`：套接字编号。对于提供 8 个套接字的 W5500 IC，该值范围为 0–7。
- `protocol`：套接字使用的协议类型。W5500 支持 TCP、UDP 和 RAW（原始）套接字¹¹，因此该参数可以取 `Sn_MR_TCP`、`Sn_MR_UDP` 或 `Sn_MR_MACRAW`。
- `port`：与套接字关联的端口号。
- `flag`：表 26.1 所列附加配置标志的组合（按位或）。

成功时，`socket()` 返回 `sn`；失败时，可能返回 `SOCKERR_SOCKNUM`（套接字编号无效）、`SOCKERR_SOCKMODE`（协议类型无效）或 `SOCKERR_SOCKFLAG`（标志参数无效）。

<p align="center">表 26.1：套接字标志值</p>

模式 | 描述
---|---
SF_IO_NONBLOCK | 将套接字配置为非阻塞模式
SF_ETHER_OWN | W5500 只能接收广播包或发送给它自己的包。此参数仅适用于 RAW 套接字
SF_IGMP_VER2 | 当套接字协议为 UDP，且同时指定了 SF_MULTI_ENABLE 标志时，启用 IGMP 版本 2
SF_MULTI_ENABLE | 当套接字协议为 UDP 时，启用组播模式
SF_TCP_NODELAY | 配置 TCP 套接字，使其在从通信对端收到数据后立即发送 ACK
SF_BROAD_BLOCK | 当套接字协议为 UDP 或 RAW 时，防止套接字接收广播包
SF_MULTI_BLOCK | 当套接字协议为 RAW 时，防止套接字接收广播包
SF_IPv6_BLOCK | 当套接字协议为 RAW 时，防止套接字接收 IPv6 包
SF_UNI_BLOCK | 当套接字协议为 UDP 时，防止套接字接收单播包

要关闭套接字并取消其配置，可调用：

¹¹RAW 套接字是一种允许直接使用 IP 协议交换数据包，而不使用任何特定于协议的传输层（即 TCP 或 UDP）的套接字。

<!-- page: 776 -->

```c
int8_t close(int8_t sn);
```

**仔细阅读**

> 如果同时使用 C 标准库中的 I/O 函数，这个 `close()` 声明会与标准库中参数和返回值均为 `int` 的 `close()` 函数冲突，导致大量编译错误。WIZnet 为该函数选择了容易冲突的名称和签名。可以修改库中的声明来规避此问题：

```c
int close(int sn);
```

W5500 套接字具有明确的状态。读取套接字状态有助于判断连接情况。宏：

```c
getSn_SR(sn);
```

自动从其寄存器中检索套接字状态。W5500 IC 的可能状态值列于表 26.2 中。

<p align="center">表 26.2：套接字状态值</p>

状态 | 描述
---|---
SOCK_CLOSED | 已关闭
SOCK_INIT | 初始化状态
SOCK_LISTEN | 监听
SOCK_ESTABLISHED | 连接已建立
SOCK_CLOSE_WAIT | 等待关闭
SOCK_UDP | UDP 套接字
SOCK_SYNSENT | 已向通信对端发送连接请求（SYN）
SOCK_SYNRECV | 已从通信对端收到连接请求（SYN）
SOCK_FIN_WAIT | 已开始套接字关闭过程
SOCK_CLOSING | 正在关闭套接字
SOCK_TIME_WAIT | 等待套接字关闭
SOCK_LAST_ACK | 套接字仍处于打开状态，但通信对端已关闭连接

#### 26.2.2.1 在 TCP 模式下处理套接字

配置好套接字的协议和模式后，可以主动连接通信对端（客户端场景），也可以将套接字设为监听状态，等待通信对端连接（服务器场景）。

要与通信对端建立连接，可使用以下函数：

<!-- page: 777 -->

```c
int8_t connect(uint8_t sn, uint8_t * addr, uint16_t port);
```

- `sn`：由 `socket()` 函数配置的套接字编号。
- `addr`：包含通信对端 IPv4 地址的 4 字节数组。
- `port`：通信对端的端口号。

成功时，`connect()` 返回 `SOCK_OK`；否则会返回相应的错误码，详见 `socket.h`。

与通信对端建立连接后，可使用以下函数发送字节序列：

```c
int32_t send(uint8_t sn, uint8_t * buf, uint16_t len);
```

其中，`buf` 指向长度为 `len` 字节的数组。

相应地，要从通信对端接收字节数组，可使用以下函数：

```c
int32_t recv(uint8_t sn, uint8_t * buf, uint16_t len);
```

要与通信对端断开连接，可使用以下函数：

```c
int8_t disconnect(uint8_t sn);
```

如果我们要创建服务器应用程序，一旦使用 socket() 函数配置好套接字，我们就可以使用以下函数将其置于监听模式：

```c
int8_t listen(uint8_t sn);
```

连接建立后，可以使用 `recv()` 和 `send()` 函数接收和发送数据。

#### 26.2.2.2 在 UDP 模式下处理套接字

UDP 是无连接协议，因此无需显式建立连接即可开始与通信对端交换数据。

套接字处于 UDP 模式时，要向通信对端发送字节数组，可使用以下函数：

```c
int32_t sendto(uint8_t sn, uint8_t * buf, uint16_t len, uint8_t * addr, uint16_t port);
```

要从通信对端接收字节，可使用以下函数：

<!-- page: 778 -->

```c
int32_t recvfrom(uint8_t sn, uint8_t * buf, uint16_t len, uint8_t * addr, uint16_t *port);
```

### 26.2.3 将 I/O 重定向到 TCP/IP 套接字

第 5 章介绍了如何将 `printf()`、`scanf()` 等 C 标准 I/O 函数重定向到 UART 接口。在开发物联网应用时，将 I/O 重定向到网络套接字也很有用，这样便可通过网络连接调试设备；当设备不在我们身边时，这一点尤其方便。

使用 W5500 IC 及其套接字库即可轻松实现这一功能。`RetargetInit()` 函数可以改写如下：

**Filename:** `Core/Src/retarget-tcp.c`

```c
 13 #ifdef RETARGET_TCP
 14
 15 #define STDIN_FILENO  0
 16 #define STDOUT_FILENO 1
 17 #define STDERR_FILENO 2
 18
 19 #ifndef RETARGET_PORT
 20 #define RETARGET_PORT 5000
 21 #endif
 22
 23 int8_t gSock = -1;
 24
 25 uint8_t RetargetInit(int8_t sn) {
 26   gSock = sn;
 27
 28   /* Disable I/O buffering for STDOUT stream, so that
 29    * chars are sent out as soon as they are printed. */
 30   setvbuf(stdout, NULL, _IONBF, 0);
 31
 32   /* Open 'sn' socket in TCP mode with a port number equal
 33    * to the value of RETARGET_PORT macro */
 34   if(socket(sn, Sn_MR_TCP, RETARGET_PORT, 0) == sn) {
 35     if(listen(sn) == SOCK_OK)
 36       return 1;
 37   }
 38   return 0;
 39 }
```

代码本身已经说明了其用途。`RetargetInit()` 接收套接字编号；对于 W5500 IC，该编号范围为 0–7。函数会配置此套接字并将其置于监听状态。`_write()` 函数可以改写如下：

<!-- page: 779 -->

**Filename:** `Core/Src/retarget-tcp.c`

```c
 49 int _write(int fd, char* ptr, int len) {
 50   int sentlen = 0;
 51   int buflen = len;
 52
 53   if(getSn_SR(gSock) == SOCK_ESTABLISHED) {
 54     if (fd == STDOUT_FILENO || fd == STDERR_FILENO) {
 55       while(1) {
 56         sentlen = send(gSock, (void*) ptr, buflen);
 57         if (sentlen == buflen)
 58           return len;
 59         else if (sentlen > 0 && sentlen < buflen) {
 60           buflen -= sentlen;
 61           ptr += (len - buflen);
 62         }
 63         else if (sentlen < 0)
 64           return EIO;
 65       }
 66     }
 67   } else if(getSn_SR(gSock) != SOCK_LISTEN) {
 68     /* Remote peer close the connection? */
 69     close(gSock);
 70     RetargetInit(gSock);
 71   }
 72
 73   errno = EBADF;
 74   return -1;
 75 }
```

该函数先检查套接字是否处于 `SOCK_ESTABLISHED` 状态，即通信对端已与设备建立连接。如果套接字不处于监听状态（第 67 行），则可能是通信对端已关闭连接；此时需要调用 `RetargetInit()`，重新将套接字配置为监听状态。连接建立后，函数即可通过 TCP/IP 连接发送 `ptr` 缓冲区中的数据。

`_read()` 函数与 `_write()` 函数几乎相同。完整源代码请参阅本书示例。要使用此模块，只需在项目级别定义 `RETARGET_TCP` 宏，并移除 `OS_USE_SEMIHOSTING` 宏。

要与设备建立连接，Linux 和 macOS 用户可以使用 `telnet` 命令；Windows 用户则可以使用 PuTTY 等终端仿真程序。

### 26.2.4 构建 HTTP 服务器

Internet/httpServer 模块提供了一个基于以太网层构建的完整 HTTP 服务器实现。该模块允许您在几个步骤内设置一个 HTTP 服务器，特别是当您需要仅提供静态内容（即不需要动态处理数据的简单网页）时。

<!-- page: 780 -->

HTTP 模块可通过以下函数进行初始化：

```c
void httpServer_init(uint8_t * tx_buf, uint8_t * rx_buf, uint8_t cnt, uint8_t * socklist);
```

该函数接收 `tx_buf` 和 `rx_buf` 两个指针，分别指向用于存放 HTTP 通信数据的缓冲区。这些缓冲区必须足够大，以容纳 HTTP 头部。浏览器访问网页时，需要与 Web 服务器交换若干 HTTP 协议消息，这些消息可能占用数百字节。因此，建议 `tx_buf` 和 `rx_buf` 的容量至少为 1024 字节¹²。参数 `cnt` 指定 HTTP 模块可使用的 W5500 套接字数量，`socklist` 则提供可用套接字的具体编号列表。

例如，以下代码片段通过传递两个大小均为 1024 字节的缓冲区以及一个包含用于处理 HTTP 请求的套接字列表的数组来初始化 HTTP 服务器：

```c
#define DATA_BUF_SIZE 1024
#define MAX_HTTPSOCK 5
uint8_t RX_BUF[DATA_BUF_SIZE], TX_BUF[DATA_BUF_SIZE];
uint8_t socknumlist[] = {0, 1, 2, 3, 4};
...
httpServer_init(TX_BUF, RX_BUF, MAX_HTTPSOCK, socknumlist);
...
```

完成 HTTP 服务器的网络配置后，还需要指定要提供的内容（HTML 页面、图像等）。可以采用两种方式：一种适合小型、简单的应用，另一种适用于更复杂、结构更完整的 Web 应用。

可以使用以下函数：

```c
void reg_httpServer_webContent(uint8_t * content_name, uint8_t * content);
```

将指定资源（例如 `index.html` 文件）与字节数组关联起来，服务器便可通过套接字将其发送给浏览器。`content_name` 是资源名称，`content` 指向包含该资源内容的字节数组。

¹² 由于 HTTP 库能够将整个 HTTP 流拆分为较小的块，因此可以减小这两个缓冲区的大小，但这会增加传输时间。

<!-- page: 781 -->

> **说明：** 为什么 HTTP 服务器需要的不只是一个空闲套接字？这是开发基于 Web 的嵌入式应用时必须牢记的基本概念，下面稍作说明。

现代 Web 应用通常比较复杂，一个网站一般由多种资源组成：

- HTML 页面，包含 Web 应用的实际内容；
- 图像，用于装饰 HTML 内容，有时也是网页内容的一部分；
- CSS 和 JavaScript 文件，用于配置页面的渲染方式和功能。

浏览器访问网站时，首先加载主 HTML 页面；若未指定页面，通常就是 `index.html`。浏览器几乎会立即开始解析页面（有些浏览器收到最初几个字节后便开始解析）。如果页面引用了其他 Web 资源，浏览器也会几乎并行地加载它们。由于这种并发访问，浏览器会与 HTTP 服务器建立多个套接字连接。HTTP 是无状态协议，每个 Web 资源都需要单独向服务器请求。对于 Apache 或 NGINX 这类运行在高性能机器上的 Web 服务器，这通常不是问题：它们能够处理数千个并发连接，强大的硬件也能根据连接速度在几毫秒内提供内容，因此套接字通常不到一秒便会打开并关闭。

对于运行在真正的嵌入式平台上的 Web 服务器，并发访问多个资源则必须仔细评估。每个套接字都会占用硬件资源，而 WIZnet 器件可用的套接字数量有限。因此，应用不能随意设计；Bootstrap、AngularJS 等现代框架用于嵌入式设备时往往需要调整，有时甚至必须完全避免使用。

例如，要发送一个简单的 HTML 页面，我们可以编写以下代码：

```c
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

这种方法有几个缺点。首先，网页嵌入在固件代码中，HTML 内容会增大固件本身，也就增大了整个二进制映像。

<!-- page: 782 -->

其次，每次修改 Web 内容时，都必须重新编译整个二进制映像。对于大型、结构复杂的 Web 应用，这种做法并不实际。

第二种方法是让 HTTP 模块从存储设备中查找并读取静态内容。例如，可以修改模块代码，使其从闪存加载 Web 资源。下一个示例将使用 FatFs 库读取存储在外部 SD 卡上的 Web 内容。

正确配置 HTTP 服务器后，就可以处理来自通信对端的请求。默认情况下，通过调用以下函数以轮询方式处理：

```c
void httpServer_run(uint8_t seqnum);
```

该函数接收一个索引，对应于传给 `httpServer_init()` 的 `socklist` 参数中保存的套接字编号。对于每个已注册的套接字，它都会检查套接字状态，并据此运行 HTTP 状态机。例如，如果某个套接字已打开并处于监听状态，HTTP 模块就会检查通信对端是否已建立连接。HTTP 模块负责处理整个 HTTP 协议和状态机；除非需要执行高级操作，否则无需了解其实现细节。

此外，HTTP 模块内部使用以 tick（系统节拍）为单位的延时。以下函数：

```c
httpServer_time_handler();
```

必须由周期配置为 1ms 的定时器调用；在 SysTick 的中断服务例程（ISR）中调用它是合适的做法。

#### 26.2.4.1 基于 Web 的示波器

> **提示：** 九块 Nucleo 开发板所搭载的大多数 STM32 微控制器（MCU）硬件资源有限，因此本示例仅在 STM32F401RE、STM32F411RE 和 STM32F446RE 上经过测试。

下面通过一个更完整的示例，介绍如何使用 W5500 IC 和 ioLibrary_Driver¹³ 模块构建结构较为完整的应用。在本例中，我们将使用多个 STM32 外设构建一个基于 Web 的示波器，如图 26.7 所示。将信号源连接到 ADC 外设的一个输入端后，只需用普通浏览器访问 Web 控制台，即可查看对应波形。此处¹⁴提供了该示波器的演示视频。

¹³ 本章示例附带的 ioLibrary_Driver 并非 WIZnet 官方库。作者对 HTTP 模块进行了多项修改，以提升其可靠性、性能和灵活性。例如，该修改版可以通过 FatFs 模块提供存储在 SD 卡上的内容，也可以通过 ARM 半主机（semihosting）从开发者的 PC 提供内容。  
¹⁴ https://youtu.be/fjtLQJDJ_04

<!-- page: 783 -->

<p align="center"><img src="../images/page-0783-image-01.jpeg" alt="图 26.7：基于 Web 的示波器界面"></p>

<p align="center">图 26.7：基于 Web 的示波器界面</p>

该示例使用 Bootstrap¹⁵、jQuery¹⁶ 和 D3.js¹⁷ 等流行的现代 Web 框架构建用户界面。本书不介绍这些框架，假定读者熟悉常见的现代 Web 开发技术。

应用程序由两部分组成：一部分负责对选定的 ADC 输入（默认为 IN0）进行模数转换；另一部分使用 ioLibrary_Driver 模块处理 HTTP 请求。这里假定所有 Web 资源都存储在 SD 卡上，并通过 FatFs 模块和作者编写的 SPI 兼容驱动程序访问。为简化开发，该应用也可以通过 ARM 半主机调用和常规 C 标准库函数，从开发者的 PC 提供内容。

以下代码片段展示了 `main()` 函数。若要获取随时间变化的信号（例如 50Hz 正弦波），就需要以固定间隔执行 ADC 转换。因此，使用 TIM2 定时器¹⁸驱动 ADC1 外设，并将 ADC1 配置为 DMA 循环模式，使定时器能够持续触发转换。ADC 以 DMA 模式启动（第 145 行），转换结果存入 `_adcConv` 数组。第 140 行创建的 `adcSem` 信号量用于控制对该数组的访问；其作用将在后文说明。

¹⁵http://getbootstrap.com/ ¹⁶https://jquery.com/ ¹⁷https://d3js.org/ ¹⁸ 此处展示的源代码与 Nucleo-F401RE 开发板相关。

<!-- page: 784 -->

**Filename:** `src/ch25/main-ex2.c`

```c
135 int main(void) {
136   HAL_Init();
137   Nucleo_BSP_Init();
138
139   osSemaphoreDef(adcSem);
140   adcSemID = osSemaphoreCreate(osSemaphore(adcSem), 1);
141
142   MX_ADC1_Init();
143   MX_TIM2_Init();
144   HAL_TIM_Base_Start(&htim2);
145   HAL_ADC_Start_DMA(&hadc1, (uint32_t*)_adcConv, 200);
146
147   MX_SPI1_Init();
148
149 #if defined(_USE_SDCARD_) && !defined(OS_USE_SEMIHOSTING)
150   SD_SPI_Configure(SD_CS_GPIO_Port, SD_CS_Pin, &hspi1);
151   MX_FATFS_Init();
152
153   if(f_mount(&diskHandle, "0:", 1) != FR_OK) {
154 #ifdef DEBUG
155     asm("BKPT #0");
156 #else
157     while(1) {
158       HAL_Delay(500);
159       HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
160     }
161 #endif //#ifdef DEBUG
162   }
163
164 #ifdef OS_USE_TRACE_ITM
165   /* Prints the SD content over the ITM port */
166   TCHAR buff[256];
167   strcpy(buff, (char*)L"/");
168   scan_files(buff);
169 #endif //#ifdef OS_USE_TRACE_ITM
170
171 #endif //#if defined(_USE_SDCARD_) && !defined(OS_USE_SEMIHOSTING)
172
173   osThreadDef(w5500, SetupW5500Thread, osPriorityNormal, 0, 512);
174   osThreadCreate(osThread(w5500), NULL);
175
176   osKernelStart();
177   /* Never coming here, but just in case... */
178   while(1);
179 }
```

<!-- page: 785 -->

如果设置了全局宏 `_USE_SDCARD_`，且未启用 ARM 半主机（即未设置全局宏 `OS_USE_SEMIHOSTING`），Web 资源（HTML 文件、图像以及 CSS/JS 脚本文件）就会存储在插入 W5500 扩展板卡槽的 MicroSD 卡上。此时会初始化 FatFs 库（第 150–151 行）并挂载第一个分区（第 153 行）。如果调试器支持读取 ITM 激励端口（stimulus port），还可以调用 `scan_files()`（第 25 章已介绍）在 SWV 控制台中列出 SD 卡内容。

最后，启动 `SetupW5500Thread()` 线程来配置 W5500 IC 并处理传入的 HTTP 请求。该线程的代码如下：

**Filename:** `src/ch25/main-ex2.c`

```c
181 void SetupW5500Thread(void const *argument) {
182   UNUSED(argument);
183
184   /* Configure the W5500 module */
185   IO_LIBRARY_Init();
186
187   /* Configure the HTTP server */
188   httpServer_init(TX_BUF, RX_BUF, MAX_HTTPSOCK, socknumlist);
189   reg_httpServer_cbfunc(NVIC_SystemReset, NULL);
190
191   /* Start processing sockets */
192   while(1) {
193     for(uint8_t i = 0; i < MAX_HTTPSOCK; i++)
194       httpServer_run(i);
195     /* We just delay for 1ms so that other threads with the same
196      * or lower priority can be executed */
197     osDelay(1);
198   }
199 }
```

该线程首先调用 `IO_LIBRARY_Init()`（如下所示）配置 W5500 IC 和 ioLibrary_Driver 库，随后配置 HTTP 服务器（第 188 行），并在无限循环中为分配给 HTTP 服务器的每个套接字调用 `httpServer_run()`。

**Filename:** `src/ch25/main-ex2.c`

```c
 79 void IO_LIBRARY_Init(void) {
 80   uint8_t runApplication = 0, dhcpRetry = 0, phyLink = 0, bufSize[] = {2, 2, 2, 2, 2};
 81   wiz_NetInfo netInfo;
 82
 83   reg_wizchip_cs_cbfunc(cs_sel, cs_desel);
 84   reg_wizchip_spi_cbfunc(spi_rb, spi_wb);
 85   reg_wizchip_spiburst_cbfunc(spi_rb_burst, spi_wb_burst);
 86   reg_wizchip_cris_cbfunc(vPortEnterCritical, vPortExitCritical);
 87
 88   wizchip_init(bufSize, bufSize);
 89
 90   ReadNetCfgFromFile(&netInfo);
 91
 92   /* Wait until the ETH cable is plugged in */
 93   do {
 94     ctlwizchip(CW_GET_PHYLINK, (void*) &phyLink);
 95     osDelay(10);
 96   } while(phyLink == PHY_LINK_OFF);
 97
 98   if(netInfo.dhcp == NETINFO_DHCP) { /* DHCP Mode */
 99     DHCP_init(DHCP_SOCK, RX_BUF);
100
101     while(!runApplication) {
102       switch(DHCP_run()) {
103       case DHCP_IP_LEASED:
104       case DHCP_IP_ASSIGN:
105       case DHCP_IP_CHANGED:
106         getIPfromDHCP(netInfo.ip);
107         getGWfromDHCP(netInfo.gw);
108         getSNfromDHCP(netInfo.sn);
109         getDNSfromDHCP(netInfo.dns);
110         runApplication = 1;
111         break;
112       case DHCP_FAILED:
113         dhcpRetry++;
114         if(dhcpRetry > MAX_DHCP_RETRY)
115         {
116           netInfo.dhcp = NETINFO_STATIC;
117           DHCP_stop();        // if restart, recall DHCP_init()
118 #ifdef _MAIN_DEBUG_
119           printf(">> DHCP %d Failed\r\n", my_dhcp_retry);
120           Net_Conf();
121           Display_Net_Conf(); // print out static netinfo to serial
122 #endif
123           dhcpRetry = 0;
124           asm("BKPT #0");
125         }
126         break;
127       default:
128         break;
129       }
130     }
131   }
132   wizchip_setnetinfo(&netInfo);
133 }
```

`IO_LIBRARY_Init()` 函数负责正确配置 W5500 IC。它首先配置用于通过 SPI 总线交换数据的函数（第 83–88 行，本章前面的示例已介绍），然后在第 90 行调用 `ReadNetCfgFromFile()`，从 SD 卡上的文件读取网络配置。该文件名为 `net.cfg`，格式如下：

```text
1  NODHCP
2  0:11:22:33:44:55
3  192.168.1.165
4  255.255.255.0
5  192.168.1.1
6  8.8.8.8
```

第一行可取值 `NODHCP` 或 `DHCP`，分别表示使用静态 IP 配置或动态 IP 配置。第二行是 MAC 地址，接下来的四行依次为设备 IP 地址、子网掩码、默认网关和首选 DNS 服务器。读取该文件后，网络接口会据此自动完成配置。用户也可以通过专用网页修改网络参数，如图 26.8 所示。

从配置文件读取网络设置后，`IO_LIBRARY_Init()` 会循环等待，直到 LAN 网线插入 RJ45 端口（第 93–96 行）。检测到网线接入后，如果网络接口配置为 DHCP 模式，该函数就会启动 DHCP 发现过程。最后在第 132 行，函数使用 `net.cfg` 中的设置，或从同一网络上的 DHCP 服务器获取的设置，配置网络接口。

<p align="center"><img src="../images/page-0787-image-01.jpeg" alt="图 26.8：用于配置网络参数的网页"></p>

<p align="center">图 26.8：用于配置网络参数的网页</p>

应用程序的其余部分主要由 HTTP 服务器构成。套接字与通信对端建立连接后，`httpServer_run()` 会调用 `http_process_handler()` 处理收到的 HTTP 请求。

<!-- page: 788 -->

该函数首先分析 HTTP 请求方法（GET、POST、PUT 等）。这里重点看 GET 方法的处理过程。

**Filename:** `Middlewares/ioLibrary_Driver/Internet/httpServer/httpServer.c`

```c
531 case METHOD_GET :
532   get_http_uri_name(p_http_request->URI, uri_buf);
533   uri_name = uri_buf;
534
535   // If URI is "/", respond by index.html
536   if (!strcmp((char *)uri_name, "/")) strcpy((char *)uri_name, INITIAL_WEBPAGE);
537   if (!strcmp((char *)uri_name, "m")) strcpy((char *)uri_name, M_INITIAL_WEBPAGE);
538   if (!strcmp((char *)uri_name, "mobile")) strcpy((char *)uri_name, MOBILE_INITIAL_WEBPAGE);
539   // Checking requested file types (HTML, TEXT, GIF, JPEG and Etc. are included)
540   find_http_uri_type(&p_http_request->TYPE, uri_name);
541
542 #ifdef _HTTPSERVER_DEBUG_
543   printf("\r\n> HTTPSocket[%d] : HTTP Method GET\r\n", s);
544   printf("> HTTPSocket[%d] : Request Type = %d\r\n", s, p_http_request->TYPE);
545   printf("> HTTPSocket[%d] : Request URI = %s\r\n", s, uri_name);
546 #endif
547
548   if(p_http_request->TYPE == PTYPE_CGI)
549   {
550     content_found = http_get_cgi_handler(uri_name, pHTTP_TX, &file_len);
551     if(content_found && (file_len <= (DATA_BUF_SIZE-(strlen(RES_CGIHEAD_OK)+8))))
552     {
553       send_http_response_cgi(s, http_response, pHTTP_TX, (uint16_t)file_len);
554     }
555     else
556     {
557       send_http_response_header(s, PTYPE_CGI, 0, STATUS_NOT_FOUND);
558     }
559   }
560   else
561   {
562     // Find the User registered index for web content
563     if(find_userReg_webContent(uri_buf, &content_num, &file_len))
564     {
565       content_found = 1; // Web content found in code flash memory
566       content_addr = (uint32_t)content_num;
567       HTTPSock_Status[get_seqnum].storage_type = CODEFLASH;
568     }
569     // Not CGI request, Web content in 'SD card' or 'Data flash' requested
570 #if defined(_USE_SDCARD_) && !defined(OS_USE_SEMIHOSTING)
571 #ifdef _HTTPSERVER_DEBUG_
572     printf("\r\n> HTTPSocket[%d] : Searching the requested content\r\n", s);
573 #endif
574     if((fr = f_open(&HTTPSock_Status[get_seqnum].fs, (const char *)uri_name, FA_READ)) == 0)
575     {
576       content_found = 1; // file open succeed
577
578       file_len = f_size(&HTTPSock_Status[get_seqnum].fs);
579       HTTPSock_Status[get_seqnum].file_len = file_len;
580       strcpy(HTTPSock_Status[get_seqnum].file_name, uri_name);
581       HTTPSock_Status[get_seqnum].storage_type = SDCARD;
582     }
583 #elif defined(OS_USE_SEMIHOSTING)
584     // Not CGI request, Web content retrieved through ARM Semihosting
585     char *base_path = OS_BASE_FS_PATH;
586     char *path;
587
588     path = malloc(sizeof(char)*strlen(base_path)+strlen(uri_name));
589     strcpy(path, base_path);
590     strcpy(path+strlen(base_path), uri_name);
591
592     HTTPSock_Status[get_seqnum].fs = fopen((const char *)path,"r");
593     if(HTTPSock_Status[get_seqnum].fs != NULL) {
594       content_found = 1; // file open succeed
595
596       fseek(HTTPSock_Status[get_seqnum].fs, 0L, SEEK_END);
597       file_len = ftell(HTTPSock_Status[get_seqnum].fs);
598       HTTPSock_Status[get_seqnum].file_len = file_len;
599       fseek(HTTPSock_Status[get_seqnum].fs, 0L, SEEK_SET);
600       strcpy(HTTPSock_Status[get_seqnum].file_name, uri_name);
601       HTTPSock_Status[get_seqnum].storage_type = SDCARD;
602     }
603   }
```

第 532 行的 `get_http_uri_name()` 获取客户端请求的 URL。如果 URL 为 `/`，表示浏览器请求默认页面，即 `index.html`。第 541 行调用 `find_http_uri_type()`，根据请求 URL 的文件扩展名确定其 Content-Type（内容类型）；例如，扩展名为 `.gif` 的文件会被标记为 `PTYPE_GIF`。

如果 Content-Type 为 CGI¹⁹（第 549 行），则调用 `http_get_cgi_handler()` 生成动态内容；稍后将介绍该函数。对于其他已注册的内容类型（完整列表请参阅 `find_http_uri_type()` 的实现），`http_process_handler()` 会查找请求的资源（第 561 行）。它首先检查该内容是否通过 `reg_httpServer_webContent()` 注册；若已注册，就从 MCU 闪存中读取内容并发送给浏览器。

¹⁹ 通用网关接口（Common Gateway Interface，CGI）是一种标准化协议，用于连接服务器端应用程序，以动态处理客户端请求。CGI 最初用于动态生成 Web 内容；如今，这种服务器端处理方式已被大量基于 PHP、Python、Ruby 等动态脚本语言的 Web 框架取代。

如果请求内容未存储在 MCU 闪存中，且设置了 `_USE_SDCARD_` 宏，函数便会检查该内容是否位于 MicroSD 卡上（第 575–584 行），并使用 FatFs API 访问文件。若启用了 ARM 半主机（semihosting），则会使用标准 C 函数从开发者的 PC 读取文件（第 586–605 行）。

`http_get_cgi_handler()` 负责生成 Web 应用的动态内容，例如 ADC 外设采集的数据。该函数处理对 `/adc.cgi` 和 `/network.cgi` 两个动态页面的请求。先来看后者。

**Filename:** `Middlewares/ioLibrary_Driver/Internet/httpServer/httpUtil.c`

```c
 22 extern ADC_HandleTypeDef hadc1;
 23 extern uint16_t adcConv[100], _adcConv[200];
 24 extern TIM_HandleTypeDef htim2;
 25 extern osSemaphoreId adcSemID;
 26
 27 uint8_t http_get_cgi_handler(uint8_t * uri_name, uint8_t * buf, uint32_t * file_len)
 28 {
 29   uint8_t ret = HTTP_FAILED;
 30   uint16_t len = 0;
 31
 32   if(strcmp((const char*)uri_name, "adc.cgi") == 0) {
 33     char *pbuf = (char*)buf;
 34
 35     /* Compute the current TIM2 frequency */
 36     uint32_t freq = HAL_RCC_GetPCLK2Freq() / (((htim2.Init.Prescaler + 1) *
 37                                               (htim2.Init.Period + 1)));
 38     pbuf += sprintf(pbuf, "{\"f\":%lu,\"d\":[", freq);
 39
 40     /* Wait until the HAL_ADC_ConvCpltCallback() or
 41        * HAL_ADC_HalfConvCpltCallback() finish */
 42     osSemaphoreWait(adcSemID, osWaitForever);
 43     for(uint8_t i = 0; i < 100; i++)
 44         pbuf += sprintf(pbuf, "%.2f,", adcConv[i]*0.805);
 45     osSemaphoreRelease(adcSemID);
 46
 47     sprintf(--pbuf, "]}");
 48     *file_len = strlen((char*)buf);
 49
 50     return HTTP_OK;
 51
 52   } else if(strcmp((const char*)uri_name, "network.cgi") == 0) {
 53     wiz_NetInfo ni;
 54     wizchip_getnetinfo(&ni);
 55     sprintf((char*)buf, "{\"ip\":\"%d.%d.%d.%d\","
 56                          "\"nm\":\"%d.%d.%d.%d\","
 57                          "\"gw\":\"%d.%d.%d.%d\","
 58                        "\"dns\":\"%d.%d.%d.%d\","
 59                        "\"dhcp\":\"%d\"}", ni.ip[0], ni.ip[1], ni.ip[2], ni.ip[3],
 60                                            ni.sn[0], ni.sn[1], ni.sn[2], ni.sn[3],
 61                                            ni.gw[0], ni.gw[1], ni.gw[2], ni.gw[3],
 62                                            ni.dns[0], ni.dns[1], ni.dns[2], ni.dns[3],
 63                                            ni.dhcp);
 64   *file_len = strlen((char*)buf);
 65   return HTTP_OK;
 66 }
 67
 68 if(ret) *file_len = len;
```

`network.cgi` 页面会将当前网络配置返回给 `/network.html` 页面；后者再通过 AJAX 请求 `/network.cgi`。例如，假设 Nucleo 的 IP 地址为 `192.168.1.165`，在浏览器中访问 `http://192.168.1.165/network.cgi`²⁰，就会得到以下结果：

```json
{"ip":"192.168.1.165","nm":"255.255.255.0","gw":"192.168.1.1","dns":"8.8.8.8","dhcp":"1"}
```

这就是以 JSON 格式返回的网络配置。浏览器访问 `/adc.cgi` 动态页面时，应用会以 JSON 格式返回当前 TIM2 频率和 ADC 采样数据。第 32–52 行负责处理该请求；`http_get_cgi_handler()` 在第 36 行计算定时器频率，Web 应用会用它在图表上绘制数据。第 42–45 行是该函数中较为关键的部分。

ADC 以 DMA 循环模式持续转换，由 TIM2 定时器触发。如果定时器频率很高，访问 `_adcConv[]` 数组时可能发生竞态：`http_get_cgi_handler()` 在第 44 行将数组内容转换为字符串的同时，数组内容可能被修改。为避免这种情况，每当调用 `HAL_ADC_ConvHalfCpltCallback()` 或 `HAL_ADC_ConvCpltCallback()` 时，都会将 `_adcConv[]` 数组的一半复制到 `adcConv[]`，如下所示。

**Filename:** `src/ch25/main-ex2.c`

```c
259 void HAL_ADC_ConvHalfCpltCallback(ADC_HandleTypeDef* hadc) {
260   UNUSED(hadc);
261
262   if(osSemaphoreWait(adcSemID, 0) == osOK) {
263       memcpy(adcConv, _adcConv, sizeof(uint16_t)*100);
264       osSemaphoreRelease(adcSemID);
265   }
266 }
267
268 void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc) {
269   UNUSED(hadc);
270
271   if(osSemaphoreWait(adcSemID, 0) == osOK) {
272       memcpy(adcConv, _adcConv+100, sizeof(uint16_t)*100);
273       osSemaphoreRelease(adcSemID);
274   }
275 }
```

²⁰ http://192.168.1.165/network.cgi

调用 `HAL_ADC_ConvHalfCpltCallback()` 时，`_adcConv[]` 数组中已有 100 个值，因此将其前半部分复制到容量为 100 的 `adcConv[]` 数组中；调用另一个回调时，则复制后半部分。两个回调在复制 `_adcConv[]` 内容前，都会尝试获取 `adcSem` 信号量。若成功获取，就执行复制；若未能获取，则说明 `http_get_cgi_handler()` 已持有该信号量，正在转换 `adcConv[]` 数组的内容。此方案可以避免竞态，但并非速度最快的方案。

`http_get_cgi_handler()` 处理所有针对 CGI 脚本的 GET 请求；相应地，`http_post_cgi_handler()` 处理所有针对 CGI 脚本的 POST 请求。

**Filename:** `Middlewares/ioLibrary_Driver/Internet/httpServer/httpUtil.c`

```c
 72 uint8_t http_post_cgi_handler(uint8_t * uri_name, st_http_request * p_http_request, uint8_t * \
 73 buf, uint32_t * file_len)
 74 {
 75   uint8_t ret = HTTP_OK;
 76   uint16_t len = 0;
 77   uint8_t *param = p_http_request->URI;
 78
 79   if(strcmp((const char *)uri_name, "sf.cgi") == 0) {
 80     param = get_http_param_value((char*)p_http_request->URI, "f");
 81     if(param != p_http_request->URI) {
 82       /* User wants to change ADC sampling frequency. We so stop conversion */
 83       HAL_ADC_Stop_DMA(&hadc1);
 84       HAL_TIM_Base_Stop(&htim2);
 85
 86       /* Obtain the current TIM2 frequency */
 87       uint32_t cfreq = HAL_RCC_GetPCLK2Freq() / (((htim2.Init.Prescaler + 1) *
 88                                                 (htim2.Init.Period + 1))), nfreq = 0;
 89
 90       if(*param == '1')
 91         nfreq = cfreq * 2;
 92       else
 93         nfreq = cfreq / 2;
 94
 95       htim2.Init.Prescaler = 0;
 96       htim2.Init.Period = 1;
 97     /* We cycle until we reach the wanted frequency. At frequencies below 30Hz,
 98        * this algorithm is largely inefficient */
 99     while(1) {
100       cfreq = HAL_RCC_GetPCLK2Freq() / (((htim2.Init.Prescaler + 1) *
101                                       (htim2.Init.Period + 1)));
102       if (nfreq < cfreq) {
103         if(++htim2.Init.Period == 0) {
104           htim2.Init.Prescaler++;
105           htim2.Init.Period++;
106         }
107       } else {
108           break;
109       }
110     }
111     HAL_TIM_Base_Init(&htim2);
112     HAL_TIM_Base_Start(&htim2);
113     HAL_ADC_Start_DMA(&hadc1, (uint32_t*)_adcConv, 200);
114
115     sprintf((char*)buf, "OK");
116     len = strlen((char*)buf);
117   }
118
119 }
120 else if(strcmp((const char *)uri_name, "network.cgi") == 0) {
121   wiz_NetInfo netInfo;
122   wizchip_getnetinfo(&netInfo);
123
124   param = get_http_param_value((char*)p_http_request->URI, "dhcp");
125   if(param != 0) {
126     netInfo.dhcp = NETINFO_DHCP;
127   } else {
128     netInfo.dhcp = NETINFO_STATIC;
129
130     param = get_http_param_value((char*)p_http_request->URI, "ip");
131     if(param != 0)
132       inet_addr_((u_char*)param, netInfo.ip);
133     else
134       return HTTP_FAILED;
135
136     param = get_http_param_value((char*)p_http_request->URI, "sn");
137     if(param != 0)
138       inet_addr_((u_char*)param, netInfo.sn);
139     else
140       return HTTP_FAILED;
141
142     param = get_http_param_value((char*)p_http_request->URI, "gw");
143     if(param != 0)
144       inet_addr_((u_char*)param, netInfo.gw);
145     else
146       return HTTP_FAILED;
147
148     param = get_http_param_value((char*)p_http_request->URI, "dns");
149     if(param != 0)
150       inet_addr_((u_char*)param, netInfo.dns);
151     else
152       return HTTP_FAILED;
153   }
154   if(!WriteNetCfgInFile(&netInfo))
155     sprintf((char*)buf, "FAILED");
156   else
157     sprintf((char*)buf, "OK");
158
159   /* Change network parameters */
160   wizchip_setnetinfo(&netInfo);
161   len = strlen((char*)buf);
162 }
163
164 if(ret) *file_len = len;
```

这个函数处理两个动态页面：`/sf.cgi` 和 `/network.cgi`。后者处理用户通过 `network.html` 中的 HTML 表单修改网络设置的请求；`/sf.cgi` 则用于调整 TIM2 频率。用户点击“放大/缩小”图标时，浏览器会请求 `/sf.cgi`，传入 `1` 表示提高频率，传入 `0` 表示降低频率。

示例应用的其余部分由 HTML、CSS 和 JavaScript 构成。`index.html` 和 `network.html` 包含使用 D3.js 绘制图表，以及显示和修改网络设置所需的代码。

要运行此示例，可将 `src/ch25/webpages` 子目录中的内容复制到 SD 卡。也可以设置 `OS_BASE_FS_PATH` 宏，使其指向 PC 文件系统中的 `src/ch25/webpages` 完整路径，然后使用 ARM 半主机功能。例如，在 Windows 上，可将 `OS_BASE_FS_PATH` 设置为 `C:/STM32Toolchain/projects/nucleo-f401RE/src/ch25/webpages`。
