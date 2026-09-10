<!-- page: 137 -->

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
