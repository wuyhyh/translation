<!-- page: 421 -->

### 14.1.2 STM32 微控制器中 I²C 外设的可用性

根据所使用的系列类型和封装，STM32 微控制器最多可提供四个独立的 I²C 外设。表 14.1 总结了本书中考虑的九块 Nucleo 开发板所搭载的 STM32 微控制器中 I²C 外设的可用性情况。

<!-- page: 422 -->

![Image from PDF page 422](../images/page-0422-image-01.png)

表 14.1：九块 Nucleo 开发板所搭载微控制器中 I²C 外设的实际可用性

对于每一个 I²C 外设和给定的 STM32 微控制器，表 14.1 显示了 SDA 和 SCL 线对应的引脚。此外，较深色的行显示了在电路板布局期间可以使用的备用引脚。例如，对于 STM32F401RE 微控制器，我们可以看到 I2C1 外设映射到 PB7 和 PB6，但 PB9 和 PB8 也可以用作备用引脚。请注意，I2C1 外设在所有采用 LQFP-64 封装的 STM32 微控制器中使用相同的 I/O 引脚。这是 STM32 微控制器提供的引脚对引脚兼容性的一个关键示例。

我们现在准备看看如何使用 CubeHAL API 来编程此外设。

## 14.2 HAL_I2C 模块

为了编程 I²C 外设，CubeHAL 定义了 C 结构体 I2C_HandleTypeDef，其定义方式如下：

<!-- page: 423 -->

```text
typedef struct {
I2C_TypeDef
*Instance;
/* I²C registers base address
*/
I2C_InitTypeDef
Init;
/* I²C communication parameters
*/
uint8_t
*pBuffPtr;
/* Pointer to I²C transfer buffer */
uint16_t
XferSize;
/* I²C transfer size
*/
__IO uint16_t
XferCount;
/* I²C transfer counter
*/
DMA_HandleTypeDef
*hdmatx;
/* I²C Tx DMA handle parameters
*/
DMA_HandleTypeDef
*hdmarx;
/* I²C Rx DMA handle parameters
*/
HAL_LockTypeDef
Lock;
/* I²C locking object
*/
__IO HAL_I2C_StateTypeDef
State;
/* I²C communication state
*/
__IO HAL_I2C_ModeTypeDef
Mode;
/* I²C communication mode
*/
__IO uint32_t
ErrorCode;
/* I²C Error code
*/
} I2C_HandleTypeDef;
```

## 让我们分析这个 C 结构体中最重要的字段。

## - Instance：指向我们要使用的 I²C 描述符的指针。例如，I2C1 是第一个 I²C 外设的描述符。
- Init：C 结构体 I2C_InitTypeDef 的一个实例，用于配置外设。我们稍后会更深入地研究它。
- pBuffPtr：指向内部缓冲区的指针，该缓冲区用于临时存储传输到 I²C 外设和从 I²C 外设传输的数据。当 I²C 以中断模式工作时使用此缓冲区，并且不应从用户代码中修改它。
- hdmatx, hdmarx：指向 DMA_HandleTypeDef 结构体实例的指针，当 I²C 外设以 DMA 模式工作时使用。

## I²C 外设的设置通过使用 C 结构体 I2C_InitTypeDef 的一个实例来完成，其定义方式如下：

```text
typedef struct {
uint32_t ClockSpeed;
/* Specifies the clock frequency */
uint32_t DutyCycle;
/* Specifies the I²C fast mode duty cycle. */
uint32_t OwnAddress1;
/* Specifies the first device own address. */
uint32_t OwnAddress2;
/* Specifies the second device own address if dual addressing
mode is selected */
uint32_t AddressingMode;
/* Specifies if 7-bit or 10-bit addressing mode is selected. */
uint32_t DualAddressMode; /* Specifies if dual addressing mode is selected. */
uint32_t GeneralCallMode; /* Specifies if general call mode is selected. */
uint32_t NoStretchMode;
/* Specifies if nostretch mode is selected. */
} I2C_InitTypeDef;
```

## 以下是这个 C 结构体中最相关字段的功能。

## - ClockSpeed：此字段指定 I²C 接口的速度，它应对应于 I²C 规范中定义的总线速度（标准模式、快速模式等）。然而，

<!-- page: 424 -->

该字段的确切值也是 DutyCycle 字段的函数，正如我们接下来将看到的。对于支持高达快速模式的 STM32 微控制器，该字段的最大值为 400000（400kHz）。较新的 STM32 系列还支持快速模式加（1MHz）。在这些其他微控制器中，ClockSpeed 字段被另一个名为 Timing 的字段取代。Timing 字段的配置值计算方式不同，我们在这里不涵盖它。ST 提供了一份专门的应用笔记（AN4235¹⁰），解释了如何根据所需的 I²C 总线速度计算该字段的确切值。然而，CubeMX 能够为您生成正确的配置值。

![Image from PDF page 424](../images/page-0424-image-01.png)

表 14.2：标准、快速和快速模式加 I²C 总线设备的 SDA 和 SCL 总线线特性

- DutyCycle：此字段仅在那些不支持快速模式加通信速度的微控制器中可用，它指定 I²C SCL 线的 tLOW 和 tHIGH 之间的比率。它可以取 I2C_DUTYCYCLE_2 和 I2C_DUTYCYCLE_16_9 的值，分别表示占空比为 2:1 和 16:9。通过选择给定的时钟占空比，我们可以“预分频”外设时钟以实现所需的 I²C 时钟速度。为了更好地理解此配置参数的作用，我们需要回顾 I²C 总线的一些基本概念。在第 11 章中，我们看到占空比是一个时间周期（例如，10μs）中信号处于活动状态的百分比。对于每种 I²C 总线速度，I²C 规范精确定义了最小的 tLOW 和 tHIGH 值。表 14.2 摘自 NXP 的 UM10204¹¹，显示了给定通信速度下的 tLOW 和 tHIGH 值（表 14.2 中的值已用黄色高亮显示）。这两个值的比率是占空比，它与通信速度无关。例如，100kHz 的周期对应于 10μs，但表 14.2 中的 tHIGH + tLOW 小于 10μs（4μs + 4.7μs = 8.7μs）。因此，只要满足 tLOW 和 tHIGH 的最小定时要求（分别为 4.7μs 和 4μs），实际值的比率可以变化。这些比率的意义在于说明 I²C 模式之间的 I²C 定时约束是不同的。它们不是 STM32 I²C 外设必须保持的强制比率。例如，tHIGH = 4μs 和 tLOW = 6μs 将是 0.67 的比率，这仍然与标准模式（100kHz）的定时兼容（因为 tHIGH = 4μs 和 tLOW > 4.7μs，且它们的和等于 10μs）。STM32 微控制器中的 I²C 外设定义了以下占空比（比率）。对于标准模式，比率固定为 1:1。这意味着 tLOW = tHIGH = 5μs。对于快速模式，我们可以使用两个比率：2:1 或 16:9。2:1 比率意味着通过 tLOW = 2.66μs 和 tHIGH = 1.33μs 获得 4μs（=400kHz），且这两个值都高于表 14.2 中报告的数值（0.6μs 和 1.3μs）。16:9 比率意味着通过 tLOW = 2.56μs 和 tHIGH = 1.44μs 获得 4μs，且这两个值仍然高于表 14.2 中报告的数值。何时使用 2:1 比率而不是 16:9 比率，反之

¹⁰https://bit.ly/2bxBoP1 ¹¹https://bit.ly/3E18iPF

<!-- page: 425 -->
