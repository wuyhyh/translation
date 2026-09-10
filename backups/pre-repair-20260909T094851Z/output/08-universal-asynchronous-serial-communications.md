<!-- page: 206 -->

# 8. 通用异步串行通信

如今，电子行业中存在许多串行通信协议和硬件接口。其中大多数专注于高传输带宽，例如较新的 USB 2.0 和 3.x 标准、Firewire (IEEE 1394) 等。有些标准源自过去，但至今仍很普及，尤其是在同一电路板上的模块间作为通信接口。其中之一是通用同步/异步收发器接口，通常简称为 USART。

几乎每个微控制器 都至少提供一个 UART 外设。几乎所有 STM32 MCU 都至少提供两个 UART/USART 接口，但根据 MCU 封装支持的 I/O 数量，大多数提供两个以上的接口（某些多达八个接口）。

在本章中，我们将学习如何使用 CubeHAL 来编程这个有用的外设。此外，我们将研究如何开发使用 UART 的应用程序，包括轮询模式和中断模式，而将第三种操作模式，即直接存储器访问 (direct memory access, DMA)，留到下一章讨论。

## 8.1 UART 和 USART 简介

在我们开始深入分析 HAL 提供的用于操作通用串行设备的功能之前，最好先简要了解一下 UART/USART 接口及其通信协议。

当我们希望两个（甚至更多）设备之间交换数据时，有两种选择：我们可以并行传输，即使用与每个数据字大小相等的通信线数量（例如，对于由 8 位组成的字，使用 8 条独立线路）；或者我们可以逐个传输构成我们字的每一位。UART/USART 是一种将并行位序列（通常分组为字节）转换为在单根线上流动的连续信号流的设备。

当信息在两个设备之间的公共信道中流动时，这两个设备（这里，为了简单起见，我们称它们为发送器和接收器）必须就时序达成一致，即传输信息的每个单独位需要多长时间。在同步传输中，发送器和接收器共享由其中一个设备（通常是充当此互连系统主设备的设备）生成的公共时钟。

<!-- page: 207 -->

![Image from PDF page 207](../images/page-0207-image-01.png)

图 8.1：使用共享时钟源的两个设备之间的串行通信

在图 8.1 中，我们有一个典型的时序图¹，显示设备 A 使用公共参考时钟将一字节 (0b01101001) 串行地发送到设备 B。公共时钟也用于确定何时开始采样位序列：当主设备开始在专用线上产生时钟时，意味着它将要发送一系列位。

在同步传输中，传输速度和持续时间由时钟定义：其频率决定了我们在通信信道上能多快传输单个字节²。但是，如果参与数据传输的两个设备就传输单个位所需的时间以及何时开始和结束采样传输位达成一致，那么我们就可以避免使用专用的时钟线。在这种情况下，我们就有了异步传输。

![Image from PDF page 207](../images/page-0207-image-02.png)

图 8.2：没有专用时钟线的串行通信时序图

图 8.2 显示了异步传输的时序图。空闲状态（即没有传输发生）由高电平信号表示。传输以 START 位开始，由低电平表示。接收器检测到负边沿，并在 1.5 个位周期后（在图 8.7.1s T1.5bit 中指示），开始采样位。采样 8 个数据位。最低有效位 (LSB) 通常最先传输。然后传输一个可选的奇偶校验位（用于数据位的错误检查）。如果假设传输信道无噪声，或者在协议层更高层存在错误检查，则通常省略此位。传输以 STOP 位结束，其持续时间为 1.5 个位。

¹时序图是时间域中一组信号的表示。²然而，请记住，最大传输速度由许多其他因素决定，例如电气信道的特性、参与传输的每个设备采样快速信号的能力等。

<!-- page: 208 -->

![Image from PDF page 208](../images/page-0208-image-01.png)

图 8.3：USART 和 UART 之间的信号差异

通用同步收发器接口是一种能够使用两个 I/O 串行传输数据字的设备，其中一个作为发送器 (TX)，另一个作为接收器 (RX)，外加一个额外的 I/O 作为时钟线；而通用异步收发器仅使用两个 RX/TX I/O（见图 8.3）。传统上，我们称第一种接口为 USART，第二种接口为 UART。

UART/USART 定义了信号方法，但没有说明电压电平。这意味着 STM32 UART/USART 将使用 MCU I/O 的电压电平，这几乎等于 VDD（通常也将这些电压电平称为 TTL 电压电平）。将这些电压电平转换以允许板外串行通信的方式由其他通信标准规定。例如，EIA-RS232 或 EIA-RS485 是两个流行的标准，除了定义时序和含义外，还定义了信号电压以及连接器的物理尺寸和引脚排列。此外，UART/USART 接口可用于使用其他物理和逻辑串行接口交换数据。例如，FT232RL 是一种流行的 IC，允许将 UART 映射到 USB 接口，如图 8.4 所示。

专用时钟线的存在，或关于传输频率的公共约定，并不能保证字节流的接收器能够以与主设备相同的传输速率处理它们。因此，一些通信标准，如 RS232 和 RS485，提供了使用专用硬件流控线的可能性。例如，使用 RS232 接口通信的两个设备可以共享两条额外的线，名为 Request To Send (RTS) 和 Clear To Send (CTS)：发送器设置其 RTS，向接收器发出信号开始监控其数据输入线。当准备好接收数据时，接收器会拉高其互补线 CTS，向发送器发出信号开始发送数据，并让发送器开始监控从设备的数据输出线。

<!-- page: 209 -->

![Image from PDF page 209](../images/page-0209-image-01.jpeg)

图 8.4：基于 FT232RL 的典型电路，用于将 3.3V TTL UART 接口转换为 USB

STM32 微控制器提供可变数量的 USART，可配置为在同步和异步模式下工作。一些 STM32 MCU 还提供仅能作为 UART 工作的接口。表 8.1 列出了本教材中使用的所有 Nucleo 板卡所配备的 STM32 MCU 提供的 UART/USART。大多数 USART 还能够自动实现硬件流控，适用于 RS232 和 RS485 标准。

所有 Nucleo-64 板卡都设计为将目标 MCU 的 USART2 连接到 ST-LINK 接口³。当我们安装 ST-LINK 驱动程序时，还会安装一个用于虚拟 COM 端口 (VCP) 的额外驱动程序：这允许我们通过 USB 接口访问目标 MCU 的 USART2，而无需使用专用的 TTL/USB 转换器。使用终端仿真程序，我们可以与我们的 Nucleo 交换消息和数据。

```text
CubeHAL 将用于管理 UART 和 USART 接口的 API 分离开来。所有用于处理 USART 的函数和 C 类型处理程序均以 HAL_USART 前缀开头，并包含在文件 stm32xxx_hal_usart.{c,h} 中；而与管理 UART 相关的函数则以 HAL_UART 前缀开头，并包含在文件 stm32xxx_hal_uart.{c,h} 中。由于这两个模块在概念上是相同的，且 UART 是不同模块之间最常见的串行互连形式，本书将仅涵盖 HAL_UART 模块的功能。
```

³请注意，如果您使用的是 Nucleo-32 或 Nucleo-144 开发板，此声明可能不成立。有关更多信息，请查阅 ST 文档。

<!-- page: 210 -->

![Image from PDF page 210](../images/page-0210-image-01.png)

表 8.1：所有 Nucleo 开发板上可用的 USART 和 UART 列表

## 8.2 UART 初始化

与所有 STM32 外设一样，USART⁴ 也映射在内存映射外设区域中，该区域从 0x4000 0000 开始。得益于 USART_TypeDef⁵ 描述符，CubeHAL 抽象了给定 STM32 微控制器中每个 USART 的实际位置。例如，我们可以简单地使用 USART2 宏来引用所有采用 LQFP64 封装的 STM32 微控制器提供的第二个 USART 外设。

然而，所有与 UART 管理相关的 HAL 函数都设计为接受 C 结构体 UART_HandleTypeDef 的一个实例作为第一个参数，其定义方式如下⁶：

⁴从本段开始，除非另有说明，否则 USART 和 UART 这两个术语可互换使用。 ⁵对该 C 结构体字段的分析超出了本书的范围。 ⁶请注意，结构体 UART_HandleTypeDef 的字段列表并不完整。此处省略了若干与本章节涵盖的主题无关的字段。有关更多信息，请参阅 CubeHAL。

<!-- page: 211 -->

```text
typedef struct {
USART_TypeDef
*Instance;
/* UART registers base address
*/
UART_InitTypeDef
Init;
/* UART communication parameters
*/
UART_AdvFeatureInitTypeDef
AdvancedInit;
/* UART Advanced Features initialization
parameters */
uint8_t
*pTxBuffPtr;
/* Pointer to UART Tx transfer Buffer */
uint16_t
TxXferSize;
/* UART Tx Transfer size
*/
uint16_t
TxXferCount;
/* UART Tx Transfer Counter
*/
uint8_t
*pRxBuffPtr;
/* Pointer to UART Rx transfer Buffer */
uint16_t
RxXferSize;
/* UART Rx Transfer size
*/
uint16_t
RxXferCount;
/* UART Rx Transfer Counter
*/
DMA_HandleTypeDef
*hdmatx;
/* UART Tx DMA Handle parameters
*/
DMA_HandleTypeDef
*hdmarx;
/* UART Rx DMA Handle parameters
*/
HAL_LockTypeDef
Lock;
/* Locking object
*/
__IO HAL_UART_StateTypeDef
gState;
/* UART communication state
*/
__IO HAL_UART_ErrorTypeDef
ErrorCode;
/* UART Error code
*/
} UART_HandleTypeDef;
```

让我们更深入地查看该结构体中最重要的字段。

- Instance：指向我们要使用的 USART 描述符（即外设映射在内存中的基地址）。例如，USART2 是与每个 Nucleo 开发板上的 ST-LINK 接口相关联的 UART 的描述符。
- Init：是 C 结构体 UART_InitTypeDef 的一个实例，用于配置 UART 接口。我们稍后将更深入地研究它。
- AdvancedInit：此字段用于配置更高级的 UART 功能，如自动波特率（BaudRate）检测和 TX/RX 引脚交换。某些 HAL 不提供此附加字段。这是因为并非所有 STM32 微控制器的 USART 接口都相同。这是在选择适用于您应用的正确微控制器时需要牢记的一个重要方面。对该字段的分析超出了本书的范围。
- pTxBuffPtr 和 pRxBuffPtr：这些字段分别指向发送和接收缓冲区。它们用作源，通过 UART 发送 TxXferSize 字节，并在 UART 配置为全双工模式（Full Duplex Mode）时接收 RxXferSize 字节。TxXferCount 和 RxXferCount 字段由 HAL 内部使用，用于统计已发送和已接收的字节数。
- Lock：此字段由 HAL 内部使用，用于锁定对 UART 接口的并发访问。

<!-- page: 212 -->

![Image from PDF page 212](../images/page-0212-image-01.png)

如上所述，Lock 字段用于在几乎所有 HAL 例程中控制并发访问。如果您查看 HAL 代码，可以看到多处使用了 __HAL_LOCK() 宏，其展开方式如下：

```text
#define __HAL_LOCK(__HANDLE__)
\
do{
\
if((__HANDLE__)->Lock == HAL_LOCKED)
\
{
\
return HAL_BUSY;
\
}
\
else
\
{
\
(__HANDLE__)->Lock = HAL_LOCKED;
\
}
\
}while (0)
```

尚不清楚 ST 工程师为何决定处理对 HAL 例程的并发访问。他们可能决定采用线程安全的方法，以便在多个线程在同一应用中运行的情况下，免除应用程序开发人员管理对同一硬件接口的多次访问的责任。

然而，这对所有 HAL 用户都有一个令人烦恼的副作用：即使我的应用程序不执行对同一外设的并发访问，我的代码也会因为大量关于 Lock 字段状态的检查而优化得很差。此外，这种锁定方式本质上是线程不安全的，因为没有使用临界区来防止在更高优先级的中断服务程序（ISR）抢占运行代码时发生竞态条件。最后，如果我的应用程序使用实时操作系统（RTOS），最好使用原生操作系统锁定原语（如信号量和互斥锁，它们不仅是原子的，而且能正确管理任务调度以避免忙等待）来处理并发访问，而无需检查 HAL 函数的特定返回值（HAL_BUSY）。

自 HAL 首次发布以来，许多开发人员都反对⁷这种锁定外设的方式。ST 工程师几年前宣布他们正在积极寻找更好的解决方案。然而，目前尚无最新消息。

所有 UART 配置活动都通过使用 C 结构体 UART_InitTypeDef 的一个实例来执行，其定义方式如下：

⁷https://bit.ly/3nOo63u

<!-- page: 213 -->

```text
typedef struct {
uint32_t BaudRate;
uint32_t WordLength;
uint32_t StopBits;
uint32_t Parity;
uint32_t Mode;
uint32_t HwFlowCtl;
uint32_t OverSampling;
} UART_InitTypeDef;
```

- BaudRate：此参数指连接速度，以每秒比特数表示。尽管该参数可以取任意值，但通常 BaudRate 来自一组众所周知的标准值列表。这是因为它是与 USART 关联的外设时钟的函数（在某些 STM32 微控制器中，由主 HSI 或 HSE 时钟通过 PLL 和倍频器链派生而来），并非所有 BaudRate 都能在不引入采样误差（从而导致通信错误）的情况下轻松实现。表 8.2 显示了 STM32F072 微控制器的常见 BaudRate 列表及相关误差计算。请务必查阅您微控制器的参考手册，以确定在给定 STM32 微控制器上哪种外设时钟频率最适合所需的 BaudRate。

![Image from PDF page 213](../images/page-0213-image-01.png)

表 8.2：在 48 MHz 下，分别采用 16 倍或 8 倍过采样时，编程波特率的误差计算

<!-- page: 214 -->

- WordLength：它指定帧中传输或接收的数据位数。此字段可以取值为 UART_WORDLENGTH_8B 或 UART_WORDLENGTH_9B，这意味着我们可以通过 UART 传输包含 8 位或 9 位数据的包。此数值不包括传输的开销位，例如起始位和停止位。
- StopBits：此字段指定传输的停止位数。它可以取值为 UART_STOPBITS_1 或 UART_STOPBITS_2，这意味着我们可以使用一个或两个停止位来指示帧的结束。
- Parity：它指示奇偶校验模式。此字段可以取表 8.3 中的值。请注意，当启用奇偶校验时，计算出的奇偶校验位会被插入到传输数据的最高有效位（MSB）位置（当字长设置为 9 位数据时为第 9 位；当字长设置为 8 位数据时为第 8 位）。奇偶校验是一种非常简单的错误检查形式。它有两种类型：奇校验或偶校验。为了生成奇偶校验位，所有数据位相加，总和的奇偶性决定该位是否被置位。例如，假设奇偶校验设置为偶校验，并且被添加到像 0b01011101 这样的数据字节中，该字节有奇数个 1（5 个），那么奇偶校验位将被置为 1。反之，如果奇偶校验模式设置为奇校验，奇偶校验位将为 0。奇偶校验是可选的，且使用并不广泛。它在通过噪声介质传输时可能有用，但它也会稍微降低数据传输速度，并要求发送方和接收方都实现错误处理（通常，接收失败的数据必须重新发送）。当发生奇偶校验错误时，所有 STM32 微控制器都会生成一个特定的中断，我们稍后将会看到。
- Mode：它指定 RX 或 TX 模式是启用还是禁用。此字段可以取表 8.4 中的一个值。
- HwFlowCtl：它指定是否启用或禁用 RS232⁸ 硬件流控模式。此参数可以取表 8.5 中的一个值。

表 8.3：UART 连接可用的奇偶校验模式

奇偶校验模式 描述

UART_PARITY_NONE 未启用奇偶校验 UART_PARITY_EVEN 如果等于 1 的位数计数为奇数，则奇偶校验位被置为 1 UART_PARITY_ODD 如果等于 1 的位数计数为偶数，则奇偶校验位被置为 1

表 8.4：可用的 UART 模式

UART 模式 描述

UART_MODE_RX UART 仅配置为接收模式 UART_MODE_TX UART 仅配置为发送模式 UART_MODE_TX_RX UART 配置为同时工作在接收和发送模式

⁸此字段仅用于启用 RS232 流控。要启用 RS485 流控，HAL 提供了一个特定函数 HAL_RS485Ex_Init()，定义在 stm32XXxx_hal_uart_ex.c 文件中。

<!-- page: 215 -->

表 8.5：UART 连接可用的流控模式

流控模式 描述

UART_HWCONTROL_NONE 禁用硬件流控 UART_HWCONTROL_RTS 启用请求发送 (RTS) 线 UART_HWCONTROL_CTS 启用清除发送 (CTS) 线 UART_HWCONTROL_RTS_CTS 同时启用 RTS 和 CTS 线

- OverSampling：当 UART 从远程对等方接收帧时，它会采样信号以计算构成消息的 1 和 0 的数量。过采样是一种以显著高于奈奎斯特率的采样频率对信号进行采样的技术。接收器实现了不同的用户可配置过采样技术（同步模式下除外），通过区分有效传入数据和噪声来进行数据恢复。这允许在最大通信速度和噪声/时钟不准确性免疫力之间进行权衡。OverSampling 字段可以取值为 UART_OVERSAMPLING_16 以执行每帧位 16 次采样，或 UART_OVERSAMPLING_8 以执行 8 次采样。表 8.2 展示了在 STM32F072 微控制器中，以 48 MHz 编程波特率时，分别进行过 16 倍或 8 倍过采样的误差计算。

现在是开始编写一些代码的好时机。让我们看看如何配置我们 Nucleo 板上微控制器的 USART2，以便通过 ST-LINK 接口交换消息。

```text
int main(void) {
UART_HandleTypeDef huart2;
/* Initialize the HAL */
HAL_Init();
/* Configure the system clock */
SystemClock_Config();
/* Configure the USART2 */
huart2.Instance = USART2;
huart2.Init.BaudRate = 38400;
huart2.Init.WordLength = UART_WORDLENGTH_8B;
huart2.Init.StopBits = UART_STOPBITS_1;
huart2.Init.Parity = UART_PARITY_NONE;
huart2.Init.Mode = UART_MODE_TX_RX;
huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
huart2.Init.OverSampling = UART_OVERSAMPLING_16;
HAL_UART_Init(&huart2);
...
}
```

第一步是配置 USART2 外设。这里我们使用此配置：38400, N, 1。即，波特率等于 38400 Bps，无奇偶校验，且只有一个停止位。接下来，我们禁用任何

<!-- page: 216 -->

形式的硬件流控，并选择最高的过采样率，即每个传输位 16 个时钟节拍。调用 HAL_UART_Init() 函数确保 HAL 根据给定的选项初始化 USART2。

然而，上述代码仍然不足以通过 Nucleo 虚拟 COM 端口交换消息。不要忘记，每个旨在与外部世界交换数据的外设都必须正确绑定到相应的 GPIO，即我们必须配置 USART2 的 TX 和 RX 引脚。查看 Nucleo 原理图，我们可以看到 USART2 的 TX 和 RX 引脚分别是 PA2 和 PA3。此外，我们在第 4 章中已经看到，HAL 的设计使得 HAL_UART_Init() 函数会自动调用 HAL_UART_MspInit()（参见第 4 章中的图 4.15）以正确初始化 I/O：编写此函数是我们的责任，该函数将由 HAL 自动调用。

![Image from PDF page 216](../images/page-0216-image-01.png)

是否必须定义此函数？

答案是否定的。这只是 HAL 和 CubeMX 自动生成的代码所强制的一种实践。HAL_UART_MspInit()，以及由 HAL_UART_DeInit() 函数调用的相应函数 HAL_UART_MspDeInit()，在 HAL 中是这样声明的：

```text
__weak void HAL_UART_MspInit(UART_HandleTypeDef *huart);
```

函数属性 __weak 是 GCC 声明具有弱作用域可见性的符号（此处为函数名）的一种方式，如果应用程序中其他地方（即另一个可重定位文件中）定义了具有相同名称且具有全局作用域（即没有 __weak 属性）的另一个符号，则该符号将被覆盖。如果我们在应用程序代码中实现了它，链接器将自动替换对 HAL 内部定义的函数 HAL_UART_MspInit() 的调用。

下面的代码展示了如何正确编写 HAL_UART_MspInit() 函数。

```text
void HAL_UART_MspInit(UART_HandleTypeDef* huart) {
GPIO_InitTypeDef GPIO_InitStruct;
if(huart->Instance==USART2) {
/* Peripheral clock enable */
__HAL_RCC_USART2_CLK_ENABLE();
/**USART2 GPIO Configuration
PA2
------> USART2_TX
PA3
------> USART2_RX
*/
GPIO_InitStruct.Pin = USART_TX_Pin|USART_RX_Pin;
GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
GPIO_InitStruct.Pull = GPIO_NOPULL;
GPIO_InitStruct.Speed = GPIO_SPEED_LOW;
```

<!-- page: 217 -->

```text
GPIO_InitStruct.Alternate = GPIO_AF1_USART2; /* WARNING: this depends on
the specific STM32 MCU */
HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
}
}
```

如您所见，该函数的设计使其适用于应用程序中使用的每个 USART。if 语句控制给定 USART（在我们的情况下是 USART2）的初始化代码。其余代码配置 PA2 和 PA3 引脚。请注意，备用功能可能会因您 Nucleo 板上配备的微控制器而异。查阅书籍示例以查看适用于您 Nucleo 的正确初始化代码。

一旦我们配置好了 USART2 接口，我们就可以开始与我们的 PC 交换消息了。

![Image from PDF page 217](../images/page-0217-image-01.png)

![Image from PDF page 217](../images/page-0217-image-02.png)

请注意，前面展示的代码可能不足以正确初始化某些 STM32 微控制器的 USART 外设。某些 STM32 微控制器，例如 STM32F334R8，允许开发者为特定外设选择时钟源（例如，STM32F334R8 微控制器中的 USART2 可以选择由 SYSCLK、HSI、LSE 或 PCLK1 提供时钟）。强烈建议首次配置微控制器外设时使用 CubeMX，并仔细检查生成的代码，以查找此类例外情况。否则，数据手册是获取此信息的唯一来源。

![Image from PDF page 217](../images/page-0217-image-03.png)

### 8.2.1 使用 CubeMX 配置 UART

如前所述，首次为我们的 Nucleo 配置 USART2 时，最好使用 CubeMX。第一步是在引脚布局（Pinout）视图中启用 USART2 外设：点击连接性（Connectivity）部分中的 USART2 条目，然后在 USART2 模式和配置（Mode and Configuration）窗格中的模式（Mode）组合框中选择异步（Asynchronous）条目，如图 8.5 所示。PA2 和 PA3 引脚将自动以绿色高亮显示。然后，进入配置（Configuration）部分并点击 USART2 按钮。通过使用配置窗格，您可以设置其他选项，例如波特率（BaudRate）、字长等⁹。

⁹你们中的一些人，特别是拥有 Nucleo-F3 的人，会注意到配置窗格可能包含比图 8.5 中显示的更多设置。有关更多信息，请参阅目标微控制器的参考手册。

<!-- page: 218 -->

![Image from PDF page 218](../images/page-0218-image-01.jpeg)

图 8.5：可以使用 CubeMX 轻松配置 UART2 接口

## 8.3 轮询模式下的 UART 通信

STM32 微控制器，因此 CubeHAL 也提供了三种通过 UART 通信在对等节点之间交换数据的方式：轮询（polling）、中断和直接存储器访问（direct memory access，DMA）模式。现在就有必要强调，这些模式不仅仅是处理 UART 通信的三种不同变体。它们是完成同一任务的三种不同编程方法，从设计和性能角度来看都带来了多种好处。让我们简要介绍它们。

- 在轮询模式（也称为阻塞模式）中，主应用程序或其线程之一会同步等待数据传输和接收。这是使用此外设进行数据通信的最简单形式，当传输速率不是太低，且 UART 未作为我们应用程序中的关键外设使用时（经典示例是将 UART 用作调试活动的输出控制台），可以使用此模式。
- 在中断模式（也称为非阻塞模式）中，主应用程序无需等待数据传输和接收完成即可释放。数据传输例程在完成外设配置后立即终止。当数据传输结束时，随后的中断将向主代码发出信号。当通信速度较低（低于 38400 Bps）或与其他微控制器执行的活动相比“很少”发生时，且我们不希望微控制器卡在等待数据传输上时，此模式更为适用。
- DMA 模式提供了最佳的数据传输吞吐量，这得益于 UART 外设对微控制器内部 RAM 的直接访问。此模式最适合高速通信，并且

<!-- page:219 -->

当我们希望完全将微控制器从数据传输开销中解放出来时。如果没有 DMA 模式，几乎不可能达到 USART 外设能够处理的最快传输速率。在本章中，我们将不讨论这种 USART 通信模式，将其留给下一章专门介绍 DMA 管理。

要在轮询模式下通过 USART 传输一系列字节，HAL 提供了以下函数：

```text
HAL_StatusTypeDef HAL_UART_Transmit(UART_HandleTypeDef *huart, uint8_t *pData,
uint16_t Size, uint32_t Timeout);
```

其中：

- huart：它是之前看到的 struct UART_HandleTypeDef 实例的指针，用于标识和配置 UART 外设；
- pData：是指向一个数组的指针，其长度等于 Size 参数，包含我们要传输的字节序列；
- Timeout：是我们等待传输完成的最大时间，以毫秒为单位。如果传输未在指定的超时时间内完成，函数将中止并返回 HAL_TIMEOUT 值；否则，如果没有发生其他错误，则返回 HAL_OK 值。此外，我们可以传递等于 HAL_MAX_DELAY (0xFFFF FFFF) 的超时值，以无限期地等待传输完成。

相反，要在轮询模式下通过 USART 接收一系列字节，HAL 提供了以下函数：

```text
HAL_StatusTypeDef HAL_UART_Receive(UART_HandleTypeDef *huart, uint8_t *pData,
uint16_t Size, uint32_t Timeout);
```

其中：

- huart：它是之前看到的 struct UART_HandleTypeDef 实例的指针，用于标识和配置 UART 外设；
- pData：是指向一个数组的指针，其长度至少等于 Size 参数，包含我们要接收的字节序列。该函数将阻塞，直到接收到 Size 参数指定的所有字节。
- Timeout：是我们愿意等待接收完成的最大时间，以毫秒为单位。如果传输未在指定的超时时间内完成，函数将中止并返回 HAL_TIMEOUT 值；否则，如果没有发生其他错误，则返回 HAL_OK 值。此外，我们可以传递等于 HAL_MAX_DELAY (0xFFFF FFFF) 的超时值，以无限期地等待接收完成。

<!-- page: 220 -->

## 请仔细阅读

![Image from PDF page 220](../images/page-0220-image-01.png)

需要特别指出的是，这两个函数提供的超时机制仅在每 1ms 调用一次 HAL_IncTick() 例程时才有效，正如 CubeMX 生成的代码所做的那样（递增 HAL 滴答计数器的函数在 SysTick 定时器 ISR 中被调用）。

## 好的，现在是时候看一个示例了。

```text
Filename: src/main-ex1.c
21
int main(void) {
22
uint8_t opt = 0;
```

23

```text
24
/* Reset of all peripherals, Initializes the Flash interface and the SysTick. */
25
HAL_Init();
```

26

```text
27
/* Configure the system clock */
28
SystemClock_Config();
```

29

```text
30
/* Initialize all configured peripherals */
31
MX_GPIO_Init();
32
MX_USART2_UART_Init();
```

33

```text
34
printMessage:
```

35

```text
36
printWelcomeMessage();
```

37

```text
38
while (1)
{
39
opt = readUserInput();
40
processUserInput(opt);
41
if(opt == 3)
42
goto printMessage;
43
}
44
}
```

45

```text
46
void printWelcomeMessage(void) {
47
HAL_UART_Transmit(&huart2, (uint8_t*)"\033[0;0H", strlen("\033[0;0H"), HAL_MAX_DELAY);
48
HAL_UART_Transmit(&huart2, (uint8_t*)"\033[2J", strlen("\033[2J"), HAL_MAX_DELAY);
49
HAL_UART_Transmit(&huart2, (uint8_t*)WELCOME_MSG, strlen(WELCOME_MSG), HAL_MAX_DELAY);
50
HAL_UART_Transmit(&huart2, (uint8_t*)MAIN_MENU, strlen(MAIN_MENU), HAL_MAX_DELAY);
51
}
```

52

```text
53
uint8_t readUserInput(void) {
54
char readBuf[1];
```

55

```text
56
HAL_UART_Transmit(&huart2, (uint8_t*)PROMPT, strlen(PROMPT), HAL_MAX_DELAY);
57
HAL_UART_Receive(&huart2, (uint8_t*)readBuf, 1, HAL_MAX_DELAY);
```

<!-- page: 221 -->

```text
58
return atoi(readBuf);
59
}
```

60

```text
61
uint8_t processUserInput(uint8_t opt) {
62
char msg[30];
```

63

```text
64
if(!opt || opt > 3)
65
return 0;
```

66

```text
67
sprintf(msg, "%d", opt);
68
HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), HAL_MAX_DELAY);
```

69

```text
70
switch(opt) {
71
case 1:
72
HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
73
break;
74
case 2:
75
sprintf(msg, "\r\nUSER BUTTON status: %s",
76
HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_13) == GPIO_PIN_RESET ? "PRESSED" : "RELEASED");
77
HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), HAL_MAX_DELAY);
78
break;
79
case 3:
80
return 2;
81
};
```

82

```text
83
return 1;
84
}
```

该示例是一种简化的管理控制台。应用程序启动时打印欢迎消息（第 36 行），然后进入循环等待用户选择。第一个选项允许切换 LD2 LED，第二个选项用于读取 USER 按钮的状态。最后，选项 3 会导致欢迎屏幕再次打印。

![Image from PDF page 221](../images/page-0221-image-01.png)

字符串 "\033[0;0H" 和 "\033[2J" 是转义序列。它们是用于操作终端控制台的标准字符序列。第一个将光标放置在可用控制台屏幕的左上角，第二个清除屏幕。

要与这个简单的管理控制台交互，我们需要一个串行通信程序。有多种选择可用。最简单的方法是使用独立程序，例如 Windows 平台上的 putty¹⁰（如果您使用的是旧版 Windows，也可以考虑使用经典的 HyperTerminal 工具），或者 Linux 和 MacOS 上的 kermit¹¹。然而，我们现在将介绍一种在 STM32CubeIDE 内部集成串行通信工具的解决方案。

¹⁰http://bit.ly/1jsQjnt ¹¹https://www.kermitproject.org/

<!-- page: 222 -->

### 8.3.1 在 Eclipse 中安装终端模拟器

Eclipse 提供了一个方便且跨平台的插件，可以在 IDE 内部添加终端模拟器，无需外部工具。该插件可自由在 Eclipse Marketplace 上获取。

要安装该插件，请转到 Help->Eclipse Marketplace…。在 Find 文本框中输入“terminal”。稍等片刻，TM Terminal 插件应该会显示出来，如图 8.6 所示。点击 Install 按钮并按照说明操作。当被要求时，重启 Eclipse。

![Image from PDF page 222](../images/page-0222-image-01.jpeg)

图 8.6: Eclipse Marketplace

要打开 Terminal 面板，您可以简单地按 Ctrl+Alt+Shift+T，或者点击 Eclipse 工具栏上的专用图标，如图 8.7 所示。

![Image from PDF page 222](../images/page-0222-image-02.jpeg)

图 8.7: 如何启动新终端

Launch Terminal 对话框出现，选择 Serial Terminal 作为终端类型（见图 8.8），然后选择对应于 Nucleo VCP 的 COM 端口，并设置与 CubeMX 中配置的相同波特率。点击 OK 按钮。

<!-- page: 223 -->

![Image from PDF page 223](../images/page-0223-image-01.jpeg)

图 8.8: 终端类型选择对话框

现在您可以重置 Nucleo。使用 HAL_UART 库编程的管理控制台应出现在串行控制台窗口中，如图 8.9 所示。

![Image from PDF page 223](../images/page-0223-image-02.jpeg)

图 8.9: 在终端视图中显示的 Nucleo 管理控制台

## 8.4 中断模式下的 UART 通信

让我们再次回顾本章的第一个示例。它有什么问题？由于我们的固件完全致力于这个简单的任务，使用 UART 轮询模式（polling mode）并没有什么问题。微控制器基本上处于阻塞状态，等待用户输入（HAL_MAX_DELAY 超时值会阻塞 HAL_UART_Receive()，直到通过 UART 发送一个字符）。但是，如果我们的固件必须实时执行其他 CPU 密集型活动呢？

假设我们将第一个示例中的 main() 重新排列为以下形式：

<!-- page: 224 -->

```text
38
while (1)
{
39
opt = readUserInput();
40
processUserInput(opt);
41
if(opt == 3)
42
goto printMessage;
```

43

```text
44
performCriticalTasks();
45
}
```

在这种情况下，我们不能阻塞 processUserInput() 函数的执行以等待用户选择，而必须为 HAL_UART_Receive() 函数指定一个更短的超时值，否则 performCriticalTasks() 将永远不会被执行。然而，这可能会导致来自 UART 外设的重要数据丢失（请记住，UART 接口有一个单字节宽的缓冲区）。

为了解决这个问题，HAL 提供了另一种通过 UART 外设交换数据的方式：中断模式。要使用此模式，我们需要执行以下任务：

- 启用 USARTx_IRQn 中断并实现相应的 USARTx_IRQHandler() 中断服务程序（ISR）。
- 在 USARTx_IRQHandler() 内部调用 HAL_UART_IRQHandler()：这将执行与 UART 外设生成的中断管理相关的所有活动¹²。
- 使用函数 HAL_UART_Transmit_IT() 和 HAL_UART_Receive_IT() 通过 UART 交换数据。这些函数也会启用 UART 外设的中断模式：这样，当事件发生时，外设会在 NVIC 控制器中置位相应的线，从而触发 ISR。
- 设计我们的应用程序代码以处理异步事件。

在我们重新排列第一个示例的代码之前，最好先查看可用的 UART 中断以及 HAL 例程的设计方式。

### 8.4.1 UART 相关中断

每个 STM32 USART 外设都提供表 8.6 中列出的中断。这些中断包括与数据传输和通信错误相关的 IRQ。它们可以分为两组：

- 传输期间生成的 IRQ：发送完成（Transmission Complete）、清除发送（Clear to Send）或发送数据寄存器空（Transmit Data Register Empty）中断。
- 接收期间生成的 IRQ：空闲线检测（Idle Line detection）、溢出错误（Overrun error）、接收数据寄存器非空（Receive Data register not empty）、奇偶校验错误（Parity error）、LIN 断点检测（LIN break detection）、噪声标志（Noise Flag，仅用于多缓冲区通信）和帧错误（Framing Error，仅用于多缓冲区通信）。

¹²如果我们使用 CubeMX 从 NVIC 配置部分启用 USARTx_IRQn（如第 7 章所示），它会自动在 ISR 中放置对 HAL_UART_IRQHandler() 的调用。

<!-- page: 225 -->

表 8.6：USART 相关中断列表

| 中断事件 | 事件标志 | 使能控制位 |
| :--- | :--- | :--- |
| 发送数据寄存器空 (Transmit Data Register Empty) | TXE | TXEIE |
| 清除发送 (Clear To Send, CTS) 标志 | CTS | CTSIE |
| 发送完成 (Transmission Complete) | TC | TCIE |
| 接收数据准备好读取 (Received Data Ready to be Read) | RXNE | RXNEIE |
| 检测到溢出错误 (Overrun Error Detected) | ORE | RXNEIE |
| 检测到空闲线 (Idle Line Detected) | IDLE | IDLEIE |
| 奇偶校验错误 (Parity Error) | PE | PEIE |
| 断点标志 (Break Flag) | LBD | LBDIE |
| 多缓冲区通信中的噪声标志、溢出错误和帧错误 (Noise Flag, Overrun error and Framing Error in multi buffer communication) | NF 或 ORE 或 FE | EIE |

如果相应的使能控制位被置位（表 8.6 的第三列），这些事件将生成中断。然而，STM32 微控制器被设计为每个 USART 外设的所有这些 IRQ 都绑定到同一个 ISR（见图 8.10¹³）。例如，USART2 仅为该外设生成的所有中断定义了一个 USART2_IRQn 作为 IRQ。用户代码需要分析相应的事件标志以推断是哪个中断生成了请求。

![Image from PDF page 225](../images/page-0225-image-01.jpeg)

图 8.10：USART 中断事件如何连接到同一个中断向量

CubeHAL 被设计为自动为我们完成这项工作。通过一系列由 HAL_UART_IRQHandler() 调用的回调函数，用户会收到关于中断生成的警告，该函数必须如前所述在 ISR 内部被调用。

从技术角度来看，UART 在轮询模式和中断模式下的传输没有太大区别。这两种方法都使用 UART 数据寄存器（DR）传输字节数组，算法如下：

¹³图 8.10 取自 STM32F030 参考手册（RM0390）。

<!-- page: 226 -->

- 对于数据传输，将一个字节放入 USART->DR 寄存器，并等待直到发送数据寄存器空（TXE）标志被置为真。
- 对于数据接收，等待直到接收数据准备好读取（RXNE）标志未被置为真，然后将 USART->DR 寄存器的内容存储到应用程序内存中。

两种方法的区别在于它们如何等待数据传输完成。在轮询模式下，HAL_UART_Receive()/HAL_UART_Transmit() 函数被设计为等待相应的事件标志被置位，针对我们要传输的每一个字节。在中断模式下，函数 HAL_UART_Receive_IT()/HAL_UART_Transmit_IT() 被设计为不等待数据传输完成，而是由 ISR 例程在生成 RXNEIE/TXEIE 中断时完成将新字节放入 DR 寄存器或将其内容加载到应用程序内存中的繁琐工作¹⁴。

要在中断模式下传输一系列字节，HAL 定义了以下函数：

```text
HAL_StatusTypeDef HAL_UART_Transmit_IT(UART_HandleTypeDef *huart,
uint8_t *pData, uint16_t Size);
```

其中：

- huart：它是之前看到的 struct UART_HandleTypeDef 实例的指针，用于标识和配置 UART 外设；
- pData：它是指向一个数组的指针，其长度等于 Size 参数，包含我们要传输的字节序列；该函数不会阻塞等待数据传输，一旦完成 UART 配置，它就会将控制权交还给主流程。

相反，要在中断模式下通过 USART 接收一系列字节，HAL 提供了以下函数：

```text
HAL_StatusTypeDef HAL_UART_Receive_IT(UART_HandleTypeDef *huart,
uint8_t *pData, uint16_t Size);
```

其中：

- huart：它是之前看到的 struct UART_HandleTypeDef 实例的指针，用于标识和配置 UART 外设；
- pData：它是指向一个数组的指针，其长度至少等于 Size 参数，包含我们要接收的字节序列。该函数不会阻塞等待数据接收，一旦完成 UART 配置，它就会将控制权交还给主流程。

现在我们可以继续重新排列第一个示例。

¹⁴这就是为什么当通信速度过高，或者我们需要非常频繁地传输大量数据时，在中断模式下传输一系列字节并不是明智之举。由于每个字节的传输发生得很快，CPU 会被 UART 为每个传输的字节生成的中断“淹没”。对于高速连续传输大量字节序列，最好使用 DMA 模式，我们将在下一章中看到。

<!-- page: 227 -->

```text
Filename: src/main-ex2.c
55
/* Enable USART2 interrupt */
56
HAL_NVIC_SetPriority(USART2_IRQn, 0, 0);
57
HAL_NVIC_EnableIRQ(USART2_IRQn);
```

58

```text
59
printMessage:
```

60

```text
61
printWelcomeMessage();
```

62

```text
63
while (1)
{
64
opt = readUserInput();
65
if(opt > 0) {
66
processUserInput(opt);
67
if(opt == 3)
68
goto printMessage;
69
}
70
performCriticalTasks();
71
}
72
}
```

73

```text
74
void USART2_IRQHandler(void) {
75
HAL_UART_IRQHandler(&huart2);
76
}
```

77

```text
78
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *UartHandle) {
79
/* Set transmission flag: transfer complete*/
80
UartReady = SET;
81
}
```

82

```text
83
void printWelcomeMessage(void) {
84
char *strings[] = {"\033[0;0H", "\033[2J", WELCOME_MSG, MAIN_MENU, PROMPT};
```

85

```text
86
for (uint8_t i = 0; i < 5; i++) {
87
HAL_UART_Transmit_IT(&huart2, (uint8_t*)strings[i], strlen(strings[i]));
88
while (HAL_UART_GetState(&huart2) == HAL_UART_STATE_BUSY_TX ||
89
HAL_UART_GetState(&huart2) == HAL_UART_STATE_BUSY_TX_RX);
90
}
91
}
```

92

```text
93
int8_t readUserInput(void) {
94
int8_t retVal = -1;
```

95

```text
96
if(UartReady == SET) {
97
UartReady = RESET;
98
HAL_UART_Receive_IT(&huart2, (uint8_t*)readBuf, 1);
99
retVal = atoi(readBuf);
100
}
```

<!-- page: 228 -->

```text
101
return retVal;
102
}
```

如上述代码所示，第一步是启用 USART2_IRQn 并为其分配优先级¹⁵。接下来，我们定义相应的 ISR（中断服务程序），并添加对 HAL_UART_IRQHandler() 的调用。示例文件的其余部分都是关于重构 printWelcomeMessage() 和 readUserInput() 函数以处理异步事件。

readUserInput() 函数现在检查全局变量 UartReady 的值。如果它等于 SET，则表示用户已向管理控制台发送了一个字符。该字符包含在全局数组 readBuf 中。然后，该函数调用 HAL_UART_Receive_IT() 以在中断模式下接收下一个字符。当 readUserInput() 返回大于 0 的值时，会调用 processUserInput() 函数。最后，定义了 HAL_UART_RxCpltCallback() 函数，该函数在接收到一个字节时由 HAL 自动调用：它只是设置全局变量 UartReady，而该变量随后被 readUserInput() 使用，如前所述。

![Image from PDF page 228](../images/page-0228-image-01.png)

需要澄清的是，只有当通过传递给 HAL_UART_Receive_IT() 函数的 Size 参数指定的所有字节都接收完毕时，才会调用 HAL_UART_RxCpltCallback() 函数。

那么 HAL_UART_Transmit_IT() 函数呢？它的工作方式与 HAL_UART_Receive_IT() 类似：每当生成 Transmit Data Register Empty(TXE) 中断时，它就传输数组中的下一个字节。然而，多次调用它时必须格外小心。由于该函数在完成 UART 设置后立即将控制权返回给调用者，因此后续对同一函数的调用将会失败，并返回 HAL_BUSY 值。

假设将上一个示例中的 printWelcomeMessage() 函数重新排列如下：

```text
void printWelcomeMessage(void) {
HAL_UART_Transmit_IT(&huart2, (uint8_t*)"\033[0;0H", strlen("\033[0;0H"));
HAL_UART_Transmit_IT(&huart2, (uint8_t*)"\033[2J", strlen("\033[2J"));
HAL_UART_Transmit_IT(&huart2, (uint8_t*)WELCOME_MSG, strlen(WELCOME_MSG));
HAL_UART_Transmit_IT(&huart2, (uint8_t*)MAIN_MENU, strlen(MAIN_MENU));
HAL_UART_Transmit_IT(&huart2, (uint8_t*)PROMPT, strlen(PROMPT));
}
```

上述代码永远不会正常工作，因为对 HAL_UART_Transmit_IT() 函数的每次调用都比 UART 传输快得多，并且下一次调用会失败，从而扰乱 UART 流程。

如果速度不是您应用程序的严格要求，并且 HAL_UART_Transmit_IT() 的使用仅限于应用程序的少数部分，则上述代码可以重新排列，如示例

¹⁵该示例是为 STM32F4 设计的。请参阅书籍示例以获取您特定 Nucleo 的信息。

<!-- page: 229 -->

# 2（参见上方代码第 83:91 行）所示。在该实现中，我们使用 HAL_UART_Transmit_IT() 传输每个字符串，但在传输下一个字符串之前，我们等待传输完成。然而，这只是 HAL_UART_Transmit() 轮询模式的一种变体，因为我们对每次 UART 传输都有忙等待。

一种更优雅且性能更好的解决方案是使用一个临时内存区域来存储字节序列，并让 ISR 执行传输。队列是处理 FIFO 事件的最佳选择。实现队列有多种方法，既可以使用静态数据结构，也可以使用动态数据结构。如果我们决定使用预定义的内存区域来实现队列，那么环形缓冲区（circular buffer）是适合此类应用程序的数据结构。

![Image from PDF page 229](../images/page-0229-image-01.png)

图 8.11：使用数组和两个指针实现的环形缓冲区

环形缓冲区不过是一个固定大小的数组，其中使用两个指针来跟踪仍需要处理的数据的头部和尾部。在环形缓冲区中，数组的第一个和最后一个位置被视为“连续”的（见图 8.11）。这就是为什么这种数据结构被称为环形缓冲区的原因。环形缓冲区还有一个重要特性：除非我们的应用程序具有多达两个并发执行流（在我们的情况下，是将字符放入缓冲区的主流程以及通过 UART 发送这些字符的 ISR 例程），否则它们本质上是线程安全的，因为“消费者”线程（在我们的情况下是 ISR）只更新尾部指针，而生产者（主流程）只更新头部指针。

环形缓冲区可以通过多种方式实现。其中一些更快，另一些更安全（即，它们增加了额外的开销，以确保我们正确处理缓冲区内容）。您可以在书籍示例中找到一个简单且相当快速的实现。解释其编码方式超出了

<!-- page: 230 -->

## 本书的范围。

## 使用环形缓冲区，我们可以按以下方式定义一个新的 UART 发送函数：

```text
Filename: src/main-ex3.c
77
uint8_t UART_Transmit(UART_HandleTypeDef *huart, uint8_t *pData, uint16_t len) {
78
if(HAL_UART_Transmit_IT(huart, pData, len) != HAL_OK) {
79
if(RingBuffer_Write(&txBuf, pData, len) != RING_BUFFER_OK)
80
return 0;
81
}
82
return 1;
83
}
```

## 该函数仅执行两项操作：它尝试以中断模式通过 UART 发送缓冲区；如果 HAL_UART_Transmit_IT() 函数失败（这意味着 UART 正在发送另一条消息），则字节序列会被放入环形缓冲区中。由 HAL_UART_TxCpltCallback() 负责检查环形缓冲区中是否有待发送的字节：

```text
Filename: src/main-ex3.c
94
void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart) {
95
if(RingBuffer_GetDataLength(&txBuf) > 0) {
96
RingBuffer_Read(&txBuf, &txData, 1);
97
HAL_UART_Transmit_IT(huart, &txData, 1);
98
}
99
}
```

## printWelcomeMessage() 和 processUserInput() 函数现在可以安排为不执行忙等待（busy-wait），如下所示：

```text
Filename: src/main-ex3.c
105
void printWelcomeMessage(void) {
106
char *strings[] = {"\033[0;0H", "\033[2J", WELCOME_MSG, MAIN_MENU, PROMPT};
107
108
for (uint8_t i = 0; i < 5; i++)
109
UART_Transmit(&huart2, (uint8_t*)strings[i], strlen(strings[i]));
110
}
111
112
uint8_t processUserInput(uint8_t opt) {
113
char msg[30];
114
115
if(!opt || opt > 3)
116
return 0;
117
118
sprintf(msg, "%d", opt);
119
UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg));
```

<!-- page: 231 -->

```text
120
121
switch(opt) {
122
case 1:
123
HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
124
break;
125
case 2:
126
sprintf(msg, "\r\nUSER BUTTON status: %s",
127
HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_13) == GPIO_PIN_RESET ? "PRESSED" : "RELEASED");
128
UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg));
129
break;
130
case 3:
131
return 2;
132
};
133
134
UART_Transmit(&huart2, (uint8_t*)PROMPT, strlen(PROMPT));
135
return 1;
136
}
```

![Image from PDF page 231](../images/page-0231-image-01.png)

RingBuffer_Read() 的速度并不像采用更高性能的实现那样快。在某些实际情况下，HAL_UART_TxCpltCallback() 例程（从中断服务例程 ISR 中调用）的整体开销可能过高。如果这是你的情况，可以考虑创建一个如下所示的函数：

```text
void processPendingTXTransfers(UART_HandleTypeDef *huart) {
if(RingBuffer_GetDataLength(&txBuf) > 0) {
RingBuffer_Read(&txBuf, &txData, 1);
HAL_UART_Transmit_IT(huart, &txData, 1);
}
}
```

然后，你可以在主应用程序代码中调用此函数，或者如果你正在使用实时操作系统（RTOS），可以在较低权限的任务中调用它。

## 8.5 错误管理

在处理外部通信时，错误管理是我们必须重点考虑的一个方面。STM32 UART 外设提供了一些与通信错误相关的错误标志。此外，还可以启用相应的中断，以便在发生错误时收到通知。

CubeHAL 旨在自动检测错误状况并提醒我们。我们只需要在应用程序代码中实现 HAL_UART_ErrorCallback() 函数。如果发生错误，HAL_UART_IRQHandler() 会自动调用它。要了解发生了哪种错误，我们可以检查 UART_HandleTypeDef->ErrorCode 字段的值。错误代码列表如表 8.7 所示。

<!-- page: 232 -->

```text
Table 8.7: List of UART_HandleTypeDef->ErrorCode possible values
```

UART 错误代码描述

```text
HAL_UART_ERROR_NONE
未发生错误
HAL_UART_ERROR_PE
奇偶校验错误
HAL_UART_ERROR_NE
噪声错误
HAL_UART_ERROR_FE
帧错误
HAL_UART_ERROR_ORE
溢出错误
HAL_UART_ERROR_DMA
DMA 传输错误
```

HAL_UART_IRQHandler() 的设计使得我们无需关心 UART 错误管理的实现细节。HAL 代码将自动执行处理错误所需的所有步骤（例如清除事件标志、挂起位等），而将处理应用程序级别错误的责任留给我们（例如，我们可以要求对端重新发送损坏的帧）。

## 8.6 HAL_UART 模块中可用回调列表

到目前为止，我们看到了如何利用回调机制来接收 CubeHAL 库关于传输完成事件的通知。CubeHAL 采用事件驱动方法设计，几乎每个 HAL_XXX 模块都提供了一组回调，可用于捕获特定的外设事件。

表 8.8 列出了 STM32G4 库中与 UART 模块相关的所有可用回调。前八个回调与传输期间生成的事件相关。HAL_UART_MspInitCallback 和 HAL_UART_MspDeInitCallback 是由 CubeMX 在 Core/Src/stm32XXxx_hal_msp.c 文件中自动生成的两个回调。最后，最后两个回调与 UART FIFO 相关，这是像 G4 系列这样的近期 STM32 微控制器可用的功能。

表 8.8: STM32F4 库中 HAL_UART 模块的回调列表

HAL_UART 回调描述

```text
HAL_UART_TxHalfCpltCallback
发送半完成回调
HAL_UART_TxCpltCallback
发送完成回调
HAL_UART_RxHalfCpltCallback
接收半完成回调。
HAL_UART_RxCpltCallback
接收完成回调。
HAL_UART_ErrorCallback
错误回调。
HAL_UART_AbortCpltCallback
中止完成回调。
HAL_UART_AbortTransmitCpltCallback
中止发送完成回调。
HAL_UART_AbortReceiveCpltCallback
中止接收完成回调。
HAL_UART_MspInitCallback
UART MspInit。
HAL_UART_MspDeInitCallback
UART MspDeInit。
HAL_UARTEx_WakeupCallback
从停止模式唤醒回调。
HAL_UARTEx_RxFifoFullCallback
接收 FIFO 满回调。
HAL_UARTEx_TxFifoEmptyCallback
发送 FIFO 空回调。
```

<!-- page: 233 -->

HAL_PPP 与 HAL_PPPEx 模块之间的区别

![Image from PDF page 233](../images/page-0233-image-01.png)

```text
We have encountered several HAL modules until here, each one covering one specific
peripheral or core feature. Every HAL module is contained in a file named stm32XXxx_-
hal_ppp.{c,h}, where the “XX” represents the STM32 family, and “ppp” the peripheral type.
For example, the stm32f4xx_hal_uart.c file contains all the function definitions for the
HAL_DMA module, all those functions have an API common to all STM32 families. This
enforces the portability of code in STM32 lineup.
However, some peripheral functions are specific of a given family, and cannot be abstracted
in a general way common to all STM32 portfolio. In this cases, the HAL provide an extension
module named HAL_PPPEX and implemented in a file named stm32XXxx_hal_ppp_ex.{c,h}.
For example, the previous HAL_UARTEx_RxFifoFullCallback() function is defined in the
HAL_UARTEx module, implemented in stm32f4xx_hal_uart_ex.c file.
```

扩展模块中 API 的实现特定于相应的 STM32 系列，甚至特定于该系列中的某个具体部件号，使用这些 API 会导致代码的可移植性降低。

近期的 CubeHAL 提供了两种定义回调的方法。标准方法是在应用程序源文件中定义回调函数，并让编译器覆盖使用 __weak 修饰符定义的占位函数。第二种方法是使用一组专用的 API，允许在运行时定义回调例程。对于大多数 HAL 模块，可以在 Core/Inc/stm32f4xx_hal_conf.h 中将宏 USE_HAL_PPP_REGISTER_CALLBACKS 设置为 1（其中 PPP 是对应的外设名称）。这将启用以下函数：

```text
HAL_StatusTypeDef HAL_UART_RegisterCallback(UART_HandleTypeDef *huart,
HAL_UART_CallbackIDTypeDef CallbackID, pUART_CallbackTypeDef pCallback);
```

and

```text
HAL_StatusTypeDef HAL_UART_UnRegisterCallback(UART_HandleTypeDef *huart,
HAL_UART_CallbackIDTypeDef CallbackID, pUART_CallbackTypeDef pCallback);
```

这些函数接受与表 8.8 中回调对应的 CallbackID 以及指向回调函数的指针。在运行时配置回调的能力使程序员能够在运行时更改回调行为，代价是固件（FW）体积的增加。

<!-- page: 234 -->

![Image from PDF page 234](../images/page-0234-image-01.jpeg)

图 8.12：如何在 CubeMX 中启用寄存器回调机制

CubeMX 提供了一种方便的方式来启用运行时回调机制。在项目管理器（Project Manager）窗格中，点击高级设置（Advanced Settings）部分。右侧会出现寄存器回调（Register Callback）窗格，如图 8.12 所示。对于给定的外设，您可以通过在相应字段中选择 ENABLE 来启用运行时回调。
