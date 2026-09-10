<!-- page: 359 -->

```text
81
__HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_1, tim1_ch2_pulse);
82
__HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_2, tim1_ch1_pulse);
83
}
```

<!-- page: 360 -->

```text
84
}
85
}
```

86

```text
87
/* TIM1 init function */
88
void MX_TIM1_Init(void) {
89
TIM_OC_InitTypeDef sConfigOC;
```

90

```text
91
htim1.Instance = TIM1;
92
htim1.Init.Prescaler = 9;
93
htim1.Init.CounterMode = TIM_COUNTERMODE_UP;
94
htim1.Init.Period = 999;
95
HAL_TIM_Base_Init(&htim1);
```

96

```text
97
sConfigOC.OCMode = TIM_OCMODE_TOGGLE;
98
sConfigOC.Pulse = 499;
99
sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
100
sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
101
sConfigOC.OCIdleState = TIM_OCIDLESTATE_RESET;
102
sConfigOC.OCNPolarity = TIM_OCNPOLARITY_HIGH;
103
sConfigOC.OCNIdleState = TIM_OCNIDLESTATE_RESET;
104
HAL_TIM_OC_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_1);
105
106
sConfigOC.Pulse = 999; /* Phase B is shifted by 90° */
107
HAL_TIM_OC_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_2);
108
}
109
110
/* TIM3 init function */
111
void MX_TIM3_Init(void) {
112
TIM_Encoder_InitTypeDef sEncoderConfig;
113
114
htim3.Instance = TIM3;
115
htim3.Init.Prescaler = 0;
116
htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
117
htim3.Init.Period = 65535;
118
119
sEncoderConfig.EncoderMode = TIM_ENCODERMODE_TI12;
120
121
sEncoderConfig.IC1Polarity = TIM_ICPOLARITY_RISING;
122
sEncoderConfig.IC1Selection = TIM_ICSELECTION_DIRECTTI;
123
sEncoderConfig.IC1Prescaler = TIM_ICPSC_DIV1;
124
sEncoderConfig.IC1Filter = 0;
125
126
sEncoderConfig.IC2Polarity = TIM_ICPOLARITY_RISING;
127
sEncoderConfig.IC2Selection = TIM_ICSELECTION_DIRECTTI;
128
sEncoderConfig.IC2Prescaler = TIM_ICPSC_DIV1;
129
sEncoderConfig.IC2Filter = 0;
130
```

<!-- page: 361 -->

```text
131
HAL_TIM_Encoder_Init(&htim3, &sEncoderConfig);
132
}
```

函数 MX_TIM1_Init() 配置 TIM1 定时器，使其 OC1 和 OC2 通道工作在输出比较模式，每约 20μs 触发一次输出。通过设置两个不同的 Pulse 值（第 84 行和第 92 行），这两个输出在相位上相互偏移。MX_TIM3_Init() 函数将 TIM3 配置为编码器 X4 模式（TIM_ENCODERMODE_TI12）。

main() 函数的设计如下：SysTimer 被配置为每 1ms 生成一个滴答（tick），每当 SysTimer 计数达到 1000 个滴答时，将计数器寄存器（cnt2）的当前内容与保存的值（cnt1）进行比较：根据编码器方向（向上或向下）计算差值，并计算速度。代码还需要检测计数器可能发生的溢出/下溢，并相应地计算差值。另外请注意，由于我们每秒执行一次比较，必须配置 TIM1，使得通道 A 和 B 生成的脉冲总和每秒小于 65535。为此，我们将 TIM1 的 Prescaler 设置为 9 以减慢其速度。最后，当按下 Nucleo 用户按钮时，第 [76:83] 行会反转 A 和 B 之间的相位偏移（即 TIM1 定时器的 OC1 和 OC2 通道）。

#### 11.3.9.1 使用 CubeMX 配置编码器模式

若要使用 CubeMX 启用编码器模式，第一步是从 Combined Channels 组合框中启用此模式，如图 11.35 所示。接下来，在 TIMx 配置视图（此处未显示）中，可以配置其他通道的设置。

![Image from PDF page 361](../images/page-0361-image-01.jpeg)

图 11.35：如何在定时器中启用编码器模式

### 11.3.10 通用定时器和高级定时器中的其他功能

迄今为止介绍的功能代表了定时器最常见的用法。然而，STM32 的通用定时器和高级定时器还提供了其他重要功能，这些功能在某些特定的

<!-- page: 362 -->

应用领域中非常有用。我们现在将简要概述这些附加功能。由于这些功能共享前几段中其他应用示例中找到的共同概念，我们将不会深入探讨这些主题的详细信息（特别是因为如果没有专用硬件，很难安排示例）。

#### 11.3.10.1 霍尔传感器模式

在有刷直流电机中，电刷通过物理连接线圈来控制换向，并在正确的时刻进行连接。在无刷直流（BLDC）电机中，换向由电子电路控制，使用 PWM。电子电路可以具有位置传感器输入，提供关于何时进行换向的信息，或者使用线圈中产生的反电动势（BEF）。位置传感器最常用于启动扭矩变化很大或需要高初始扭矩的应用中。位置传感器也常用于电机用于定位的应用中。

霍尔效应传感器，或简称霍尔传感器，主要用于计算三相 BLDC 电机的位置（每个相位一个传感器）。STM32 通用定时器可以被编程为工作在霍尔传感器模式。通过将前三个输入设置为异或（XOR）模式，可以自动检测转子的位置。

这是通过使用高级控制定时器（TIM1）生成 PWM 信号来驱动电机，并使用另一个定时器（例如 TIM3）作为“接口定时器”来实现的。该接口定时器捕获通过异或门连接到 TI1 输入通道的三个定时器输入引脚（CC1、CC2、CC3）（参见图 11.16）。TIM3 处于从模式，配置为复位模式；从输入为 TI1F_ED³⁸。因此，每当三个输入之一切换时，计数器从 0 重新开始计数。这创建了一个由霍尔输入的任何变化触发的时间基准。

在“接口定时器”（TIM3）上，捕获/比较通道 1 被配置为捕获模式，捕获信号为 TRC（参见图 11.16 - TRC 以红色高亮显示）。捕获的值对应于输入之间两次变化之间的时间间隔，提供了关于电机速度的信息。“接口定时器”可以用作输出模式，生成一个脉冲，该脉冲改变高级控制定时器（TIM1）的通道配置（通过触发 COM 事件）。TIM1 定时器用于生成 PWM 信号以驱动电机。为此，接口定时器通道必须被编程，以便在编程延迟后生成一个正脉冲（在输出比较或 PWM 模式下）。该脉冲通过 TRGO 输出发送到高级定时器（TIM1）。
