<!-- page: 444 -->

# 15. SPI

在上一章中，我们分析了统治板内通信系统“市场”的两大最广泛通信标准之一：I²C 协议。现在，是时候分析另一位参与者：SPI 协议了。

所有 STM32 微控制器都至少提供一个 SPI 接口，该接口允许开发主设备和从设备应用。CubeHAL 实现了编程此类外设所需的所有必要功能。本章将首先简要介绍 SPI 规范，随后对 HAL_SPI 模块进行快速概述。

## 15.1 SPI 规范简介

串行外设接口（Serial Peripheral Interface, SPI）是一种关于主控制器（通常由 MCU 或具有可编程功能的设备实现）与多个从设备之间进行串行、同步和全双工通信的规范。正如我们接下来将看到的，SPI 接口的特性允许在同一总线上进行全双工和半双工通信。SPI 规范是一个事实标准，由 Motorola¹ 在 20 世纪 70 年代末定义，并且至今仍被广泛用作许多数字 IC 的通信协议。与 I²C 协议不同，SPI 规范不强制在总线上使用特定的消息协议，它仅限于总线信号传输，从而赋予从设备关于交换消息结构的完全自由度。

![Image from PDF page 444](../images/page-0444-image-01.png)

图 15.1：典型 SPI 总线的结构

¹Motorola 是半导体行业的先驱公司，多年来已拆分为几家子公司。Motorola 的半导体部门演变为 ON Semiconductor，而微控制器部门则成为 Freescale Semiconductor。后者于 2015 年被 NXP 收购。

<!-- page: 445 -->

典型的 SPI 总线由四个信号组成，如图 15.1 所示，尽管也可以使用仅三个 I/O 来驱动某些 SPI 设备（在这种情况下，我们称之为 3 线 SPI）：

- SCK：此信号 I/O 用于生成时钟，以同步 SPI 总线上的数据传输。它由主设备生成，这意味着在 SPI 总线中，每次传输总是由主设备启动。与 I²C 规范不同，SPI 本质上更快，SPI 时钟速度通常为几 MHz。如今，能够以高达 100MHz 的速率交换数据的 SPI 设备非常常见。此外，SPI 协议允许具有不同通信速度的设备在同一总线上共存。
- MOSI：此信号 I/O 的名称代表主输出从输入（Master Output Slave Input），用于将数据从主设备发送到从设备。与 I²C 总线不同，I²C 总线仅使用一根线进行双向数据交换，SPI 协议定义了两条独立的线用于主设备和从设备之间的数据交换。
- MISO：代表主输入从输出（Master Input Slave Output），对应于用于将从设备的数据发送到主设备的 I/O 线。
- SSn：代表从设备选择（Slave Select），在典型的 SPI 总线中存在 ‘n’ 条独立的线，用于寻址参与事务的特定 SPI 设备。与 I²C 协议不同，SPI 不使用从设备地址来选择设备，而是要求通过一条物理线执行此操作，该线被拉低（asserted LOW）以执行选择。在典型的 SPI 总线中，通过将其 SS 线拉低，同一时间只能有一个从设备处于活动状态。这就是为什么具有不同通信速度的设备可以在同一总线上共存²的原因。

由于拥有两条独立的数据通信线 MOSI 和 MISO，SPI 本质上允许全双工通信，因为从设备可以在接收来自主设备的新数据的同时向主设备发送数据。在一对一 SPI 总线（仅一个主设备和一个从设备）中，可以省略 SS 信号（相应的从设备 I/O 接地），并且 MISO/MOSI 线合并为一条称为从输入/从输出（Slave In/Slave Out, SISO）的单线。在这种情况下，我们可以称之为 2 线 SPI，尽管它本质上是一个 3 线总线。

²为了完整性，我们必须指出，这并不是在同一总线上拥有具有不同通信速度的设备的准确原因。主要原因是从设备 I/O 是用三态 I/O 实现的，即当 SS 线未被拉低时，它们处于高阻抗状态（断开连接）。

<!-- page: 446 -->

![Image from PDF page 446](../images/page-0446-image-01.png)

图 15.2：全双工传输中 SPI 总线上的数据交换方式

总线上的每次事务都是根据最大从设备频率启用 SCK 线而开始的。一旦时钟线开始生成信号，主设备将 SS 线拉低，数据传输即可开始。传输通常涉及两个给定字长³的寄存器，一个在主设备中，一个在从设备中。数据通常以最高有效位（most-significant bit）优先移出，同时将新的最低有效位（least-significant bit）移入同一寄存器。与此同时，来自从设备的数据被移入最低有效位寄存器。在寄存器位被移出和移入后，主设备和从设备已交换数据。如果需要交换更多数据，移位寄存器将被重新加载，过程重复。传输可以继续任意数量的时钟周期。完成时，主设备停止切换时钟信号，并通常取消选择从设备。

图 15.2 展示了全双工传输中数据传输的方式，而图 15.3 展示了半双工连接中数据通常交换的方式。

![Image from PDF page 446](../images/page-0446-image-02.png)

图 15.3：半双工传输中 SPI 总线上的数据交换方式

³8 位数据传输是常规做法，但某些从设备甚至支持 16 位传输。

<!-- page: 447 -->

### 15.1.1 时钟极性和相位

除了设置总线时钟频率外，主设备和从设备还必须就通过 MOSI 和 MISO 线交换数据时的时钟极性和相位达成一致。摩托罗拉（Motorola）的 SPI 规范⁴将这两个设置分别命名为 CPOL 和 CPHA，大多数芯片厂商都采用了这一约定。

极性和相位的组合通常被称为 SPI 总线模式，通常按照表 15.1 进行编号。最常见的模式是模式 0 和模式 3，但大多数从设备至少支持几种总线模式。

表 15.1：根据 CPOL 和 CPHA 配置划分的 SPI 总线模式

模式 CPOL CPHA 0 0 0 1 0 1 2 1 0 3 1 1

时序图如图 15.4 所示，并在下文进一步描述：

- 当 CPOL=0 时，时钟的基准值为零，即活动状态为 1，空闲状态为 0。

- – 对于 CPHA=0，数据在 SCK 上升沿（LOW →HIGH 转换）被捕获，数据在下降沿（HIGH →LOW 时钟转换）输出。 – 对于 CPHA=1，数据在 SCK 下降沿被捕获，数据在上升沿输出。
- 当 CPOL=1 时，时钟的基准值为 1（CPOL=0 的反相），即活动状态为 0，空闲状态为 1。

– 对于 CPHA=0，数据在 SCK 下降沿被捕获，数据在上升沿输出。 – 对于 CPHA=1，数据在 SCK 上升沿被捕获，数据在下降沿输出。

也就是说，CPHA=0 意味着在第一个时钟沿采样，而 CPHA=1 意味着在第二个时钟沿采样，无论该时钟沿是上升沿还是下降沿。请注意，当 CPHA=0 时，数据必须在第一个时钟周期之前保持半个周期的稳定。

⁴http://bit.ly/2cc3T3S

<!-- page: 448 -->

![Image from PDF page 448](../images/page-0448-image-01.png)

图 15.4：根据 CPOL 和 CPHA 设置划分的 SPI 时序图

### 15.1.2 从设备选择信号管理

如前所述，SPI 从设备没有用于在总线上标识它们的地址，但只要从设备选择（Slave Select，SS）信号为低电平（LOW），它们就会开始与主设备交换数据。STM32 微控制器提供两种不同的模式来处理 SS 信号，在 ST 文档中该信号被称为 NSS。让我们分析一下这两种模式。

- NSS 软件模式：SS 信号由固件驱动。当 MCU 工作在主模式时，可以使用任意空闲的 GPIO 来驱动 IC；当 MCU 工作在从模式时，可以使用它来检测另一个主设备是否开始传输。
- NSS 硬件模式：使用特定的 MCU I/O 来驱动 SS 信号，并由 SPI 外设内部进行管理。根据 NSS 输出配置，有两种可能的配置：

– NSS 输出使能：此配置仅用于设备工作在主模式时。当主设备开始通信时，NSS 信号被驱动为低电平，并保持低电平直到 SPI 被禁用。重要的是要指出，当总线上只有一个 SPI 从设备且其 SS I/O 连接到 NSS 信号时，此模式才适用。此配置不允许多主模式。 – NSS 输出禁用：此配置允许工作在主模式的设备具备多主能力。对于设置为从设备的设备，NSS 引脚作为经典的 NSS 输入：当 NSS 为低电平时从设备被选中，当 NSS 为高电平时从设备被取消选中。

### 15.1.3 SPI TI 模式

STM32 微控制器中的 SPI 外设在主模式下工作且 NSS 信号配置为硬件工作时，支持 TI 模式。在 TI 模式下，无论设置值如何，时钟极性和相位都被强制符合德州仪器（Texas Instruments）协议的要求。NSS 管理也是 TI 协议特有的，这使得 NSS 管理的配置对用户来说是透明的。事实上，在 TI 模式下，NSS 信号在每个传输字节结束时“脉冲”（从 LSB 位开始从低电平变为高电平，并在下一个传输字节的 MSB 位开始时从高电平变为低电平

<!-- page: 449 -->

）。有关此通信模式的更多信息，请参阅您所考虑 MCU 的参考手册。

![Image from PDF page 449](../images/page-0449-image-01.jpeg)

表 15.2：配备所有九个 Nucleo 开发板的 MCU 中 SPI 外设的实际可用性

### 15.1.4 STM32 MCU 中 SPI 外设的可用性

根据所使用的家族类型和封装，STM32 微控制器最多可提供六个独立的 SPI 外设。表 15.2 总结了本书中考虑的配备所有九个 Nucleo 开发板的 STM32 MCU 中 SPI 外设的可用性。

对于每个 SPI 外设和给定的 STM32 MCU，表 15.2 显示了与 MOSI、MISO 和 SCK 线对应的引脚。此外，较深的行显示了在电路板布局期间可以使用的备用引脚。例如，对于 STM32F401RE MCU，我们可以看到 SPI1 外设映射到 PA7、PA6 和 PA5，但 PB5、PB5 和 PB3 也可以用作备用引脚。请注意，SPI1 外设在所有具有 LQFP-64 封装的 STM32 MCU 中使用相同的 I/O 引脚。这是 STM32 微控制器提供的引脚对引脚兼容性的另一个清晰示例。

我们现在准备好看看如何使用 CubeHAL API 来编程此外设。

<!-- page: 450 -->

## 15.2 HAL_SPI 模块

### 为了编程 SPI 外设，HAL 定义了 C 结构体 SPI_HandleTypeDef，其定义方式如下⁵：

```text
typedef struct __SPI_HandleTypeDef {
SPI_TypeDef
*Instance;
/* SPI 寄存器基地址 */
SPI_InitTypeDef
Init;
/* SPI 通信参数 */
uint8_t
*pTxBuffPtr;
/* 指向 SPI 发送传输缓冲区的指针 */
uint16_t
TxXferSize;
/* SPI 发送传输大小 */
__IO uint16_t
TxXferCount;
/* SPI 发送传输计数器 */
uint8_t
*pRxBuffPtr;
/* 指向 SPI 接收传输缓冲区的指针 */
uint16_t
RxXferSize;
/* SPI 接收传输大小 */
__IO uint16_t
RxXferCount;
/* SPI 接收传输计数器 */
DMA_HandleTypeDef
*hdmatx;
/* SPI 发送 DMA 句柄参数
*/
DMA_HandleTypeDef
*hdmarx;
/* SPI 接收 DMA 句柄参数
*/
HAL_LockTypeDef
Lock;
/* 锁定对象
*/
__IO HAL_SPI_StateTypeDef
State;
/* SPI 通信状态 */
__IO uint32_t
ErrorCode;
/* SPI 错误代码 */
} SPI_HandleTypeDef;
```

### 让我们分析该结构体中最重要的字段。

- Instance：是指向我们要使用的 SPI 描述符的指针。例如，SPI1 是第一个 SPI 外设的描述符。
- Init：是 C 结构体 SPI_InitTypeDef 的一个实例，用于配置外设。我们稍后会更深入地研究它。
- pTxBuffPtr, pRxBuffPtr：指向内部缓冲区的指针，用于临时存储传输到 SPI 外设和从 SPI 外设传输的数据。当 SPI 工作在 中断 模式下时使用此功能，并且不应由用户代码修改。
- hdmatx, hdmarx：指向 DMA_HandleTypeDef 结构体实例的指针，用于 SPI 外设工作在 直接存储器访问 模式时。

### SPI 外设的配置是通过使用 C 结构体 SPI_InitTypeDef 的一个实例来完成的，其定义方式如下：

⁵为了简洁起见，省略了一些字段。有关 SPI_HandleTypeDef 结构体的确切定义，请参阅 CubeHAL 源代码。

<!-- page: 451 -->

```text
typedef struct {
uint32_t Mode;
/* 指定 SPI 工作模式。 */
uint32_t Direction;
/* 指定 SPI 双向模式状态。 */
uint32_t DataSize;
/* 指定 SPI 数据大小。 */
uint32_t CLKPolarity;
/* 指定串行时钟的稳态。 */
uint32_t CLKPhase;
/* 指定用于位捕获的时钟有效边沿。 */
uint32_t NSS;
/* 指定 NSS 信号是由硬件（NSS 引脚）还是软件管理 */
uint32_t BaudRatePrescaler; /* 指定用于配置 SCK 时钟的波特率预分频值 */
uint32_t FirstBit;
/* 指定数据传输是从 MSB 还是 LSB 位开始。 */
uint32_t TIMode;
/* 指定是否启用 TI 模式。 */
uint32_t CRCCalculation;
/* 指定是否启用 CRC 计算。 */
uint32_t CRCPolynomial;
/* 指定用于 CRC 计算的多项式。 */
} SPI_InitTypeDef;
```

- Mode：此参数将 SPI 设置为主模式或从模式。它可以取值为 SPI_MODE_MASTER 和 SPI_MODE_SLAVE。
- Direction：它指定从外设工作在 4 线模式（输入/输出有两条独立的线）还是 3 线模式（仅有一条 I/O 线）。它可以取值为 SPI_DIRECTION_2LINES 以配置全双工 4 线模式；取值为 SPI_DIRECTION_2LINES_RXONLY 以配置半双工 4 线模式；取值为 SPI_DIRECTION_1LINE 以配置半双工 3 线模式。
- DataSize：配置通过 SPI 总线传输的数据大小，它可以取值为 SPI_DATASIZE_8BIT 和 SPI_DATASIZE_16BIT。
- CLKPolarity：它配置 SCK CPOL 设置，它可以取值为 SPI_POLARITY_LOW（对应 CPOL=0）和 SPI_POLARITY_HIGH（对应 CPOL=1）。
- CLKPhase：此相关字段设置时钟相位，它可以取值为 SPI_PHASE_1EDGE（对应 CPHA=0）和 SPI_PHASE_2EDGE（对应 CPHA=1）。
- NSS：此字段处理 NSS I/O 的行为。它可以取值为 SPI_NSS_SOFT 以在软件模式下配置 NSS 信号；取值为 SPI_NSS_HARD_INPUT 和 SPI_NSS_HARD_OUTPUT 以分别在输入和输出硬件模式下配置 NSS 信号。
- BaudRatePrescaler：它设置 APB 时钟的预分频器，并确定最大 SCK 时钟速度。它可以取值为 SPI_BAUDRATEPRESCALER_2, SPI_BAUDRATEPRESCALER_4, …, SPI_BAUDRATEPRESCALER_256（从 2¹ 到 2⁸ 的所有 2 的幂）。
- FirstBit：指定数据传输顺序，它可以取值为 SPI_FIRSTBIT_MSB 和 SPI_FIRSTBIT_LSB。
- TIMode：用于启用/禁用 TI 模式，它可以取值为 SPI_TIMODE_DISABLE 和 SPI_TIMODE_ENABLE。
- CRCCalculation 和 CRCPolynomial：所有 STM32 微控制器中的 SPI 外设都支持硬件 CRC 生成。在 Tx 模式下，CRC 值可以作为最后一个字节传输，或者可以对最后接收的字节执行自动 CRC 错误检查。CRC 值

<!-- page: 452 -->

使用奇数可编程多项式对每一位进行计算。计算在由 CPHA 和 CPOL 配置定义的采样时钟边沿上处理。计算出的 CRC 值在数据块结束时自动检查，无论是由 CPU 还是由 直接存储器访问 管理的传输。如果在内部计算的接收数据 CRC 与发送方发送的 CRC 之间检测到不匹配，则设置错误条件。当 SPI 在 DMA 循环模式下驱动时，CRC 功能不可用。有关此选项的更多信息，请参阅您所考虑的 STM32 MCU 的参考手册。

通常，为了配置 SPI 外设，我们使用以下函数：

```text
HAL_StatusTypeDef HAL_SPI_Init(SPI_HandleTypeDef *hspi);
```

该函数接受指向之前看到的 SPI_HandleTypeDef 结构体实例的指针。

### 15.2.1 使用 SPI 外设交换消息

一旦 SPI 外设配置完成，我们即可开始与从设备交换数据。由于 SPI 规范并未强制规定特定的通信协议，因此在使用 SPI 外设时，无论处于从模式还是主模式，CubeHAL 例程之间没有区别。唯一的区别在于外设配置，即相应地设置 SPI_InitTypeDef 结构体中的 Mode 参数。

通常，CubeHAL 提供了三种通过 SPI 总线通信的方式：轮询、中断和直接存储器访问（DMA）模式。

要在轮询模式下向从设备发送若干字节，我们使用以下函数：

```text
HAL_StatusTypeDef HAL_SPI_Transmit(SPI_HandleTypeDef *hspi, uint8_t *pData, uint16_t Size,
uint32_t Timeout);
```

该函数的签名与之前看到的其他通信例程（例如用于 UART 操作的例程）几乎相同，因此我们在此不再描述其参数。如果 SPI 外设被配置为在 SPI_DIRECTION_1LINE 或 SPI_DIRECTION_- 2LINES 模式下工作，均可使用此函数。要在轮询模式下接收若干字节，我们使用以下函数：

```text
HAL_StatusTypeDef HAL_SPI_Receive(SPI_HandleTypeDef *hspi, uint8_t *pData, uint16_t Size,
uint32_t Timeout);
```

此函数可用于所有三种方向模式。

如果从设备支持全双工模式，则我们可以使用以下函数：

<!-- page: 453 -->

```text
HAL_StatusTypeDef HAL_SPI_TransmitReceive(SPI_HandleTypeDef *hspi, uint8_t *pTxData,
uint8_t *pRxData, uint16_t Size,
uint32_t Timeout);
```

该函数允许在传输指定数量字节的同时，同时接收相同数量的数据。显然，这仅在 SPI 方向设置为 SPI_DIRECTION_2LINES 时有效。

要在中断模式下通过 SPI 交换数据，CubeHAL 提供了以下函数：

```text
HAL_StatusTypeDef HAL_SPI_Transmit_IT(SPI_HandleTypeDef *hspi, uint8_t *pData,
uint16_t Size);
HAL_StatusTypeDef HAL_SPI_Receive_IT(SPI_HandleTypeDef *hspi, uint8_t *pData,
uint16_t Size);
HAL_StatusTypeDef HAL_SPI_TransmitReceive_IT(SPI_HandleTypeDef *hspi, uint8_t *pTxData,
uint8_t *pRxData, uint16_t Size);
```

在 DMA 模式下通过 SPI 交换数据的 CubeHAL 例程与上述三个例程相同，只是它们以 _DMA 结尾。

一旦使用基于中断和 DMA 的例程，我们必须准备好在传输结束时收到通知，因为传输是异步执行的。这意味着我们需要在 NVIC 级别启用相应的中断，并从 ISR 中调用函数 HAL_SPI_IRQHandler()。存在六种不同的回调函数可供实现，如表 15.3 所示。

表 15.3：当 SPI 外设在中断或 DMA 模式下工作时，CubeHAL 可用的回调函数

回调函数 描述

HAL_SPI_TxCpltCallback() 指示已传输指定数量的字节 HAL_SPI_RxCpltCallback() 指示已接收指定数量的字节 HAL_SPI_TxRxCpltCallback() 指示已传输并接收指定数量的字节 HAL_SPI_TxHalfCpltCallback() 指示 DMA SPI 半传输过程已完成 HAL_SPI_RxHalfCpltCallback() 指示 DMA SPI 半接收过程已完成 HAL_SPI_TxRxHalfCpltCallback() 指示 DMA SPI 半传输和半接收过程已完成

当 SPI 外设配置为 DMA 循环模式时，我们可以使用以下例程来暂停/恢复/中止 DMA 循环事务：

```text
HAL_StatusTypeDef HAL_SPI_DMAPause(SPI_HandleTypeDef *hspi);
HAL_StatusTypeDef HAL_SPI_DMAResume(SPI_HandleTypeDef *hspi);
HAL_StatusTypeDef HAL_SPI_DMAStop(SPI_HandleTypeDef *hspi);
```

当 SPI 工作在 DMA 循环模式时，适用以下限制：

- 当 SPI 仅以接收模式访问时，不能使用 DMA 循环模式；

<!-- page: 454 -->

- 当启用 DMA 循环模式时，CRC 功能不受管理
- 当使用 SPI DMA 暂停/停止功能时，我们必须在 SPI 回调函数下仅使用函数 HAL_SPI_DMA- Pause()/ HAL_SPI_DMAStop()。

在本章中，我们不会分析任何具体示例。在第 26 章中，我们将使用 SPI 外设来编程一个硬连线 TCP/IP 嵌入式以太网控制器，这使我们能够使用 Nucleo 板构建基于互联网的应用程序。

### 15.2.2 使用 CubeHAL 可达到的最大传输频率

SCK 频率是通过可编程预分频器从 PCLK 频率派生而来的。该预分频器的范围从 2¹ 到 2⁸。然而，正如之前多次提到的，CubeHAL 在驱动外设时会增加不可避免的开销。这也适用于 SPI 外设。事实上，使用 CubeHAL 时，无法在不同的 SPI 模式下达到所有支持的 SPI 频率。

ST 工程师已在 CubeHAL 中清楚地记录了这一点。如果您打开 stm32XXxx_hal_spi.c 文件，可以看到（大约在第 120 行）两个表格，它们报告了给定方向模式（半双工或全双工）以及编程和使用外设的方式（轮询、中断和 DMA）下的最大可达传输频率。

例如，在 STM32F4 MCU 中，如果 SPI 外设工作在从模式，并且我们使用 CubeHAL 以中断模式对其进行编程，则可以达到等于 fP CLK/8 的 SCK 频率。

## 15.3 使用 CubeMX 配置 SPI 外设

若要使用 CubeMX 启用所需的 SPI 外设，必须按以下顺序操作。首先，我们需要选择所需的通信模式，如图 15.5 所示。接下来，我们需要在同一配置视图中指定 NSS 信号的行为。设置好这两个参数后，我们可以在 CubeMX 配置窗格中继续配置其他 SPI 设置。

![Image from PDF page 454](../images/page-0454-image-01.png)

图 15.5：如何在 CubeMX 中选择 SPI 通信模式
