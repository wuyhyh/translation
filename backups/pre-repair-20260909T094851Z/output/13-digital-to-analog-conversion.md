<!-- page: 403 -->

# 13. 数模转换

在上一章中，我们将注意力集中在 ADC 控制器上，展示了这一重要外设的所有 STM32 微控制器都具备的最相关特性。该操作的逆过程由数模转换器（Digital to Analog Converter, DAC）实现。

根据所使用的系列和封装，STM32 微控制器通常仅提供具有一个或两个专用输出的 DAC，除了少数 STM32F3 系列型号实现了两个 DAC（第一个具有两个输出，另一个仅有一个输出）之外。一些较新的 STM32G4 系列 MCU 甚至提供多达 5 个独立的 DAC 模块，但只有前两个具有输出 I/O：其他模块仅具备向内部外设（如 OPAMP、比较器和 ADC，如果支持的话）提供信号的可能性。

DAC 通道可以配置为工作在 8/12 位模式，两个通道的转换可以独立执行或同时执行：后一种模式在需要生成两个独立但同步信号的应用中非常有用（例如，在音频应用中）。与 ADC 外设一样，DAC 也可以由专用定时器触发，以在给定频率下生成模拟信号。

本章简要介绍了该外设的最相关特性，读者有责任深入理解其正在考虑的特定 STM32 微控制器中 DAC 的功能。一如既往，我们现在将简要解释 DAC 控制器的工作原理。

## 13.1 DAC 外设简介

DAC 是一种将数字量转换为模拟信号的设备，该信号与提供的参考电压 VREF 成正比（见图 13.1）。DAC 有许多类别。其中包括脉冲宽度调制器（PWM）、插值型、Sigma-Delta DAC 和高速 DAC。我们在第 11 章中分析了如何使用 STM32 定时器生成 PWM 信号，并利用此功能借助 RC 低通滤波器生成输出正弦波。

![Image from PDF page 403](../images/page-0403-image-01.png)

图 13.1：DAC 的一般结构

<!-- page: 404 -->

STM32 微控制器中可用的 DAC 外设基于通用的 R-2R 电阻梯形网络。电阻梯形是由电阻重复单元组成的电路，它是使用由高精度电阻制成的重复电阻网络进行数模转换的一种廉价且简单的方法。该网络在参考电压和地之间充当可编程分压器。

![Image from PDF page 404](../images/page-0404-image-01.png)

图 13.2：R-2R 网络如何用于将数字量转换为模拟信号

图 13.2 展示了一个 8 位 R–2R 电阻梯形网络。DAC 的每一位由数字逻辑门驱动。理想情况下，这些门在 V = 0（逻辑 0）和 V = VREF（逻辑 1）之间切换输入位。R–2R 网络使这些数字位对输出电压 VOUT 的贡献具有加权作用。根据哪些位被设置为 1 以及哪些位被设置为 0，输出电压将在 0 和 VREF 减去最小步长值（对应位 0）之间具有相应的阶梯值。

对于具有 N 位和 0V / VREF 逻辑电平的 R–2R DAC 的给定数值 D，输出电压 VOUT 为：

VOUT = VREF × D

2N [1]

例如，如果 N = 12（因此 2N = 4096）且 VREF = 3.3 V（STM32 MCU 中典型的模拟供电电压），则 VOUT 将在 0V（VAL = 0 = 000000002）和最大值（VAL = 4095 = 111111112）之间变化：

VOUT = 3.3 × 4095

# 4096 ≈3.29V

步长（对应 VAL = 1）为：

∆VOUT = 3.3 × 1 4096 ≈0.0002V

<!-- page: 405 -->

然而，始终请记住，DAC 输出的精度和稳定性受 VDDA 电源域质量和 PCB 布局的严重影响。

在 STM32 微控制器中，DAC 模块具有 12 位精度，但也可以配置为工作在 8 位模式。在 12 位模式下，数据可以是左对齐或右对齐的。根据销售类型和使用的封装，DAC 具有两个输出通道，每个通道都有其自己的转换器。在双 DAC 通道模式下，当两个通道组合在一起用于同步更新操作时，转换可以独立执行或同时执行。为了获得更好的分辨率，提供了一个输入参考引脚 VREF+（与其他模拟外设共享）。与 ADC 外设一样，DAC 也可以与 DMA 控制器一起使用，以在给定固定频率下生成可变输出电压。这在音频应用中极其有用，或者当我们希望以给定载波频率工作来生成模拟信号时也是如此。正如我们将在本章后面看到的，STM32 DAC 具有生成噪声波和三角波的能力。

最后，STM32 MCU 中实现的 DAC 为每个通道集成了一个输出缓冲器（见图 13.2），可用于降低输出阻抗并直接驱动外部负载，而无需添加外部运算放大器。每个 DAC 通道输出缓冲器都可以启用和禁用。

表 13.1 列出了本书中考虑的九个 Nucleo 板所配备的所有 STM32 MCU 的确切 DAC 外设数量及其相关输出通道。

![Image from PDF page 405](../images/page-0405-image-01.jpeg)

表 13.1：配备 Nucleo 板的 STM32 MCU 中 DAC 外设的可用性

## 13.2 HAL_DAC 模块

在简要介绍 STM32 微控制器中 DAC 外设提供的最重要功能之后，现在是深入探讨相关 CubeHAL API 的合适时机。

为了操作 DAC 外设，HAL 定义了 C 结构体 `DAC_HandleTypeDef`，其定义方式如下：

<!-- page: 406 -->

```text
typedef struct {
DAC_TypeDef
*Instance;
/* Pointer to DAC descriptor
*/
__IO HAL_DAC_StateTypeDef
State;
/* DAC communication state
*/
HAL_LockTypeDef
Lock;
/* DAC locking object
*/
DMA_HandleTypeDef
*DMA_Handle1;
/* Pointer DMA handler for channel 1 */
DMA_HandleTypeDef
*DMA_Handle2;
/* Pointer DMA handler for channel 2 */
__IO uint32_t
ErrorCode;
/* DAC Error code
*/
} DAC_HandleTypeDef;
```

让我们分析该结构体中最重要的字段。

```text
• Instance: 是指向我们要使用的 DAC 描述符的指针。例如，DAC1 是第一个 DAC 外设的描述符。
• DMA_Handle{1,2}: 这是指向配置为在 DMA 模式下执行 D/A 转换的 DMA 处理器的指针。在具有两个输出通道的 DAC 中，存在两个独立的 DMA 处理器，用于分别为每个通道执行转换。
```

如您所见，`DAC_HandleTypeDef` 结构体与之前使用的其他处理器描述符有所不同。事实上，它没有提供专用的 Init 参数，该参数由 `HAL_DAC_Init()` 函数用于配置 DAC。这是因为 DAC 的实际配置是在通道级别进行的，并且要求使用结构体 `DAC_ChannelConfTypeDef`，其定义方式如下：

```text
typedef struct {
uint32_t DAC_Trigger;
/* Specifies the external trigger for the selected
DAC channel */
uint32_t DAC_OutputBuffer;/* Specifies whether the DAC channel output buffer
is enabled or disabled */
} DAC_ChannelConfTypeDef;
```

- `DAC_Trigger`：指定用于触发 DAC 转换的源。当使用 `HAL_DAC_SetValue()` 函数手动驱动 DAC 时，它可以取值 `DAC_TRIGGER_NONE`；当在 DMA 模式下驱动 DAC 且没有定时器来“时钟”转换时，取值为 `DAC_TRIGGER_SOFTWARE`；取值为 `DAC_TRIGGER_Tx_TRGO` 表示由专用定时器驱动的转换。
- `DAC_OutputBuffer`：启用专用的输出缓冲器。

要配置 DAC 通道，我们使用以下函数：

```text
HAL_StatusTypeDef HAL_DAC_ConfigChannel(DAC_HandleTypeDef* hdac,
DAC_ChannelConfTypeDef* sConfig, uint32_t Channel);
```

<!-- page: 407 -->

该函数接受指向 `DAC_HandleTypeDef` 结构体实例的指针、指向之前看到的 `DAC_ChannelConfTypeDef` 结构体实例的指针，以及宏 `DAC_CHANNEL_1` 以配置第一个通道，`DAC_CHANNEL_2` 用于第二个通道。

在一些较新的 STM32 微控制器中，如 STM32L476 或 STM32G474，DAC 还提供额外的低功耗功能。例如，可以启用采样保持电路，即使 DAC 断电也能保持输出电压稳定。这在电池供电的应用中极其有用。在这些 MCU 中，`DAC_ChannelConfTypeDef` 结构体的结构有所不同，以允许配置这些额外功能。请参阅您所考虑的 MCU 的 HAL 源代码。

### 13.2.1 手动驱动 DAC

DAC 外设可以手动驱动，也可以使用 DMA 和触发源（例如专用定时器）驱动。我们现在将分析第一种方法，该方法用于不需要高频转换的情况。

第一步是通过调用以下函数启动外设：

```text
HAL_StatusTypeDef HAL_DAC_Start(DAC_HandleTypeDef* hdac, uint32_t Channel);
```

该函数接受指向 `DAC_HandleTypeDef` 结构体实例的指针，以及要激活的通道（`DAC_CHANNEL_1` 或 `DAC_CHANNEL_2`）。

一旦 DAC 通道被启用，我们就可以通过调用以下函数执行转换：

```text
HAL_StatusTypeDef HAL_DAC_SetValue(DAC_HandleTypeDef* hdac, uint32_t Channel,
uint32_t Alignment, uint32_t Data);
```

其中，`Alignment` 参数可以取值 `DAC_ALIGN_8B_R` 以在 8 位模式下驱动 DAC，`DAC_ALIGN_12B_L` 或 `DAC_ALIGN_12B_R` 以在 12 位模式下驱动 DAC，分别传递左对齐或右对齐的输出值。

以下示例旨在 Nucleo-F072RB 上运行，展示了如何手动驱动 DAC 外设。该示例基于这样一个事实：在大多数提供 DAC 外设的 Nucleo 板上，其中一个输出通道对应于 PA5 引脚，该引脚连接到 LD2 LED。这允许我们使用 DAC 使 LD2 进行淡入淡出。

<!-- page: 408 -->

```text
Filename: Core/Src/main-ex1.c
8
DAC_HandleTypeDef hdac;
```

9

```text
10
/* Private function prototypes -----------------------------------------------*/
11
static void MX_DAC_Init(void);
```

12

```text
13
int main(void) {
14
HAL_Init();
15
Nucleo_BSP_Init();
```

16

```text
17
/* Initialize all configured peripherals */
18
MX_DAC_Init();
```

19

```text
20
HAL_DAC_Init(&hdac);
21
HAL_DAC_Start(&hdac, DAC_CHANNEL_2);
```

22

```text
23
while(1) {
24
int i = 2000;
25
while(i < 4000) {
26
HAL_DAC_SetValue(&hdac, DAC_CHANNEL_2, DAC_ALIGN_12B_R, i);
27
HAL_Delay(1);
28
i+=4;
29
}
```

30

```text
31
while(i > 2000) {
32
HAL_DAC_SetValue(&hdac, DAC_CHANNEL_2, DAC_ALIGN_12B_R, i);
33
HAL_Delay(1);
34
i-=4;
35
}
36
}
37
}
```

38

```text
39
/* DAC init function */
40
void MX_DAC_Init(void) {
41
DAC_ChannelConfTypeDef sConfig;
42
GPIO_InitTypeDef GPIO_InitStruct;
```

43

```text
44
__HAL_RCC_DAC1_CLK_ENABLE();
```

45

```text
46
/* DAC Initialization
*/
47
hdac.Instance = DAC;
48
HAL_DAC_Init(&hdac);
```

49

```text
50
/**DAC channel OUT2 config */
51
sConfig.DAC_Trigger = DAC_TRIGGER_NONE;
52
sConfig.DAC_OutputBuffer = DAC_OUTPUTBUFFER_ENABLE;
53
HAL_DAC_ConfigChannel(&hdac, &sConfig, DAC_CHANNEL_2);
```

<!-- page: 409 -->

54

```text
55
/* DAC GPIO Configuration
56
PA5
------> DAC_OUT2
57
*/
58
GPIO_InitStruct.Pin = GPIO_PIN_5;
59
GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;
60
GPIO_InitStruct.Pull = GPIO_NOPULL;
61
HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
62
}
```

代码很直接。第 [40:62] 行配置 DAC，使通道 2 用作输出通道。因此，PA5 被配置为模拟输出（第 [58:61] 行）。请注意，由于我们将手动驱动 DAC 转换，通道触发源被设置为 `DAC_TRIGGER_NONE`（第 51 行）。最后，`main()` 只是一个无限循环，它增加/减少输出电压，从而使 LD2 淡入淡出。

### 13.2.2 使用定时器以 DMA 模式驱动 DAC

DAC 外设最常见的用途是以给定频率生成模拟波形（例如在音频应用中）。在这种情况下，驱动 DAC 的最佳方式是使用 DMA 和定时器来触发转换。

要启动 DAC 并在 DMA 模式下执行传输，我们需要配置相应的 DMA 通道/流对，并使用以下函数：

```text
HAL_StatusTypeDef HAL_DAC_Start_DMA(DAC_HandleTypeDef* hdac, uint32_t Channel,
uint32_t* pData, uint32_t Length, uint32_t Alignment);
```

该函数接受指向 DAC_HandleTypeDef 结构体实例的指针、要激活的通道（DAC_CHANNEL_1 或 DAC_CHANNEL_2）、要在 DMA 模式下传输的值数组的指针、其长度，以及内存中输出值的对齐方式。对齐方式可以取值为 DAC_ALIGN_8B_R 以 8 位模式驱动 DAC，或取值为 DAC_ALIGN_12B_L 或 DAC_ALIGN_12B_R 以 12 位模式驱动 DAC，分别对应输出值左对齐或右对齐。

例如，我们可以轻松地使用 DAC 生成正弦波。在第 11 章中，我们分析了如何使用定时器的 PWM 模式生成正弦波。如果我们的 MCU 提供了 DAC，那么同样的操作可以更容易地完成。此外，根据具体应用，通过启用输出缓冲器，我们可以完全避免使用外部无源元件。

要生成以给定频率运行的正弦波，我们必须将完整周期划分为若干步。通常，超过 200 步是对输出波形的良好近似。这意味着，如果我们想生成 50Hz 的正弦波，则需要每以下时间间隔执行一次转换：

fsinewave = 50Hz ∗200 = 10kHz [2]

<!-- page: 410 -->

## 由于 STM32 DAC 的分辨率为 12 位，我们必须使用以下公式将对应最大输出电压的值 4095 除以 200 步：

) + 1 ) (4096

) [3]

DACOutput = ( sin ( x · 2π

2

ns

## 其中 ns 是采样数，在我们的例子中为 200。

## 使用上述公式，我们可以生成一个初始化向量，以在 DMA 模式下馈送 DAC。与 ADC 外设一样，我们可以使用配置为以公式 [2] 给定的频率触发 TRGO 线的定时器。以下示例展示了如何在 STM32F072 MCU 中使用 DAC 生成 50Hz 正弦波。

```text
Filename: Core/Src/main-ex2.c
7
#define PI
3.14159
8
#define SAMPLES 200
```

9

```text
10
/* Private variables ---------------------------------------------------------*/
11
DAC_HandleTypeDef hdac;
12
TIM_HandleTypeDef htim6;
13
DMA_HandleTypeDef hdma_dac_ch1;
```

14

```text
15
/* Private function prototypes -----------------------------------------------*/
16
static void MX_DAC_Init(void);
17
static void MX_TIM6_Init(void);
```

18

```text
19
int main(void) {
20
uint16_t IV[SAMPLES], value;
```

21

```text
22
HAL_Init();
23
Nucleo_BSP_Init();
```

24

```text
25
/* Initialize all configured peripherals */
26
MX_TIM6_Init();
27
MX_DAC_Init();
```

28

```text
29
for (uint16_t i = 0; i < SAMPLES; i++) {
30
value = (uint16_t) rint((sinf(((2*PI)/SAMPLES)*i)+1)*2048);
31
IV[i] = value < 4096 ? value : 4095;
32
}
```

33

```text
34
HAL_DAC_Init(&hdac);
35
HAL_TIM_Base_Start(&htim6);
36
HAL_DAC_Start_DMA(&hdac, DAC_CHANNEL_1, (uint32_t*)IV, SAMPLES, DAC_ALIGN_12B_R);
```

37

```text
38
while(1);
39
}
```

<!-- page: 411 -->

40

```text
41
/* DAC init function */
42
void MX_DAC_Init(void) {
43
DAC_ChannelConfTypeDef sConfig;
44
GPIO_InitTypeDef GPIO_InitStruct;
```

45

```text
46
__HAL_RCC_DAC1_CLK_ENABLE();
```

47

```text
48
/**DAC Initialization
*/
49
hdac.Instance = DAC;
50
HAL_DAC_Init(&hdac);
```

51

```text
52
/**DAC channel OUT1 config */
53
sConfig.DAC_Trigger = DAC_TRIGGER_T6_TRGO;
54
sConfig.DAC_OutputBuffer = DAC_OUTPUTBUFFER_ENABLE;
55
HAL_DAC_ConfigChannel(&hdac, &sConfig, DAC_CHANNEL_1);
```

56

```text
57
/**DAC GPIO Configuration
58
PA4
------> DAC_OUT1
59
*/
60
GPIO_InitStruct.Pin = GPIO_PIN_4;
61
GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;
62
GPIO_InitStruct.Pull = GPIO_NOPULL;
63
HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
```

64

```text
65
/* Peripheral DMA init*/
66
hdma_dac_ch1.Instance = DMA1_Channel3;
67
hdma_dac_ch1.Init.Direction = DMA_MEMORY_TO_PERIPH;
68
hdma_dac_ch1.Init.PeriphInc = DMA_PINC_DISABLE;
69
hdma_dac_ch1.Init.MemInc = DMA_MINC_ENABLE;
70
hdma_dac_ch1.Init.PeriphDataAlignment = DMA_PDATAALIGN_HALFWORD;
71
hdma_dac_ch1.Init.MemDataAlignment = DMA_MDATAALIGN_HALFWORD;
72
hdma_dac_ch1.Init.Mode = DMA_CIRCULAR;
73
hdma_dac_ch1.Init.Priority = DMA_PRIORITY_LOW;
74
HAL_DMA_Init(&hdma_dac_ch1);
```

75

```text
76
__HAL_LINKDMA(&hdac,DMA_Handle1,hdma_dac_ch1);
77
}
```

78

79

```text
80
/* TIM6 init function */
81
void MX_TIM6_Init(void) {
82
TIM_MasterConfigTypeDef sMasterConfig;
```

83

```text
84
__HAL_RCC_TIM6_CLK_ENABLE();
```

85

```text
86
htim6.Instance = TIM6;
```

<!-- page: 412 -->

```text
87
htim6.Init.Prescaler = 0;
88
htim6.Init.CounterMode = TIM_COUNTERMODE_UP;
89
htim6.Init.Period = 4799;
90
HAL_TIM_Base_Init(&htim6);
```

91

```text
92
sMasterConfig.MasterOutputTrigger = TIM_TRGO_UPDATE;
93
sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
94
HAL_TIMEx_MasterConfigSynchronization(&htim6, &sMasterConfig);
95
}
```

函数 MX_DAC_Init() 配置 DAC，使得当 TIM6 TRGO 线生成时，第一个通道执行转换。此外，DMA 也相应配置，将其设置为循环模式，以便连续地将初始化向量的内容传输到 DAC 数据寄存器中。MX_TIM6_Init() 函数设置 TIM6，使其以等于 10kHz 的频率溢出，从而触发内部连接到 DAC 的 TRGO 线。最后，第 [29:32] 行根据公式 [3] 生成初始化向量。其内容随后用于馈送 DAC，在 TIM6 启用后，DAC 以 DMA 模式启动。

![Image from PDF page 412](../images/page-0412-image-01.jpeg)

图 13.3：使用 DAC 外设生成的输出正弦波

通过将示波器探头连接到我们的 Nucleo 开发板的 PA4 引脚，我们可以看到由 DAC 生成的输出正弦波（见图 13.3）。

如果我们想知道何时完成了一次 DMA 模式下的 DAC 转换，我们可以实现回调函数：

```text
void HAL_DACEx_ConvCpltCallbackChX(DAC_HandleTypeDef* hdac);
```

该函数由从与 DAC 外设关联的 DMA 通道的 ISR 中调用的 HAL_DMA_IRQHandler() 例程自动调用。函数名称末尾的 X 必须根据使用的通道替换为 1 或 2。

仔细阅读

![Image from PDF page 412](../images/page-0412-image-02.png)

请注意，在 STM32G4 系列中，DAC 外设寄存器必须以字（32 位）为单位进行访问。因此，Nucleo-G474RE 开发板的用户会发现 IV 数组和 value 变量被定义为 unit32_t。

<!-- page: 413 -->

### 13.2.3 三角波生成

在许多音频应用中，生成三角波非常有用。虽然完全可以使用之前介绍的直接存储器访问（DMA）技术来生成三角波，但 STM32 的 DAC 允许在硬件层面生成具有三角形状的波形。

![Image from PDF page 413](../images/page-0413-image-01.jpeg)

图 13.4：使用 DAC 生成的三角波

图 13.4 展示了定义三角波形状的三个参数。让我们来分析它们。

- 幅度（Amplitude）：这是一个从 0 到 0xFFF 的值，它决定了波形的最大高度。它与偏移量（offset）值直接相关，我们稍后会看到这一点。幅度不能是任意值，而是固定值列表的一部分。请查阅 HAL 源代码以获取完整的可接受值列表。
- 偏移量（Offset）：它是最小输出值，代表波形的最低点。偏移量与幅度之和不能超过最大值 0xFFF。这意味着波形的最大幅度将由差值 amplitude - offset 给出。
- 频率（Frequency）：是波形的频率，由连接到 DAC 的定时器的更新频率决定。定时器的更新频率由下方的公式 [4] 决定。这意味着，如果我们想生成一个幅度等于 2047 的 50Hz 三角波，那么运行在 48MHz 的定时器的预分频器需要配置为 234。

fUEV = 2 · amplitude · fwave [4]

要生成三角波形，我们使用函数

```text
HAL_StatusTypeDef HAL_DACEx_TriangleWaveGenerate(DAC_HandleTypeDef* hdac, uint32_t Channel,
uint32_t Amplitude);
```

该函数接受要使用的 DAC 通道和所需的幅度。而波形偏移量则使用 HAL_DAC_SetValue() 例程进行配置。生成三角波的完整步骤如下：

<!-- page: 414 -->

- 配置用于生成波形的 DAC 通道。
- 配置与 DAC 关联的定时器，并根据公式 [4] 配置其预分频器。
- 使用 HAL_DAC_Start() 函数启动 DAC。
- 使用 HAL_DAC_SetValue() 例程配置所需的偏移量值。
- 调用 HAL_DACEx_TriangleWaveGenerate() 函数启动三角波生成。

### 13.2.4 噪声波生成

STM32 的 DAC 还能够使用伪随机数生成器生成噪声波（见图 13.5）。这在某些应用领域非常有用，例如音频应用和射频（RF）系统。此外，它还可以用于提高 ADC 外设¹的精度。

要生成可变幅度的伪噪声，DAC 中提供了一个 LFSR（线性反馈移位寄存器）。该寄存器预加载了值 0xAAA，该值可以被部分或完全屏蔽。然后，该值与 DAC 数据寄存器的内容相加（无溢出），并将结果用作输出值。

![Image from PDF page 414](../images/page-0414-image-01.jpeg)

图 13.5：使用 DAC 生成的噪声波

要生成噪声波，我们可以使用 HAL 例程

```text
HAL_StatusTypeDef HAL_DACEx_NoiseWaveGenerate(DAC_HandleTypeDef* hdac, uint32_t Channel,
uint32_t Amplitude);
```

该函数接受用于生成波形的通道和幅度值，该幅度值会与 LFSR 的内容相加以生成伪随机波。与三角波生成类似，可以使用定时器来触发转换：这意味着波形的频率由定时器的溢出频率决定。

¹ST 提供了专门针对此主题的 AN2668(https://bit.ly/25lJoqx)。
