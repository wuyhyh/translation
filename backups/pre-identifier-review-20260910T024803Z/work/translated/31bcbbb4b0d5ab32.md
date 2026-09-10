<!-- page: 191 -->

### 这与基于 Cortex-M3/4/7/33 处理器的 HAL 中定义的内容完全不同。

## 以下示例¹⁰展示了中断优先级机制是如何工作的。

```text
Filename: src/main-ex3.c
39
uint8_t blink = 0;
```

40

```text
41
int main(void) {
42
GPIO_InitTypeDef GPIO_InitStruct;
```

43

```text
44
HAL_Init();
```

45

```text
46
/* GPIO Ports Clock Enable */
47
__HAL_RCC_GPIOC_CLK_ENABLE();
48
__HAL_RCC_GPIOB_CLK_ENABLE();
49
__HAL_RCC_GPIOA_CLK_ENABLE();
```

50

```text
51
/*Configure GPIO pin : PC13 - USER BUTTON */
52
GPIO_InitStruct.Pin = GPIO_PIN_13 ;
53
GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
54
GPIO_InitStruct.Pull = GPIO_PULLDOWN;
55
HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);
```

56

```text
57
/*Configure GPIO pin : PB2 */
58
GPIO_InitStruct.Pin = GPIO_PIN_2 ;
59
GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;
60
GPIO_InitStruct.Pull = GPIO_PULLUP;
61
HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
```

62

```text
63
/*Configure GPIO pin : PA5 - LD2 LED */
64
GPIO_InitStruct.Pin = GPIO_PIN_5;
65
GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
66
GPIO_InitStruct.Pull = GPIO_NOPULL;
67
GPIO_InitStruct.Speed = GPIO_SPEED_LOW;
```

¹⁰该示例旨在配合 Nucleo-F072RB 开发板使用。如果您使用的是其他型号的 Nucleo 开发板，请参阅本书中的其他示例。

<!-- page: 192 -->

```text
68
HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
```

69

```text
70
HAL_NVIC_SetPriority(EXTI4_15_IRQn, 0x1, 0);
71
HAL_NVIC_EnableIRQ(EXTI4_15_IRQn);
```

72

```text
73
HAL_NVIC_SetPriority(EXTI2_3_IRQn, 0x0, 0);
74
HAL_NVIC_EnableIRQ(EXTI2_3_IRQn);
```

75

```text
76
while(1);
77
}
```

78

```text
79
void EXTI4_15_IRQHandler(void) {
80
HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_13);
81
}
```

82

```text
83
void EXTI2_3_IRQHandler(void) {
84
HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_2);
85
}
```

86

```text
87
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {
88
if(GPIO_Pin == GPIO_PIN_13) {
89
blink = 1;
90
while(blink) {
91
HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
92
for(volatile int i = 0; i < 100000; i++) {
93
/* Busy wait */
94
}
95
}
96
}
97
else {
98
blink = 0;
```

如果前面的解释清晰易懂，这段代码应该很容易理解。这里有两个与 EXTI 线 2 和 13 相关联的中断请求（IRQ）。相应的中断服务程序（ISR）调用 HAL 函数 `HAL_GPIO_EXTI_IRQHandler()`，该函数进而调用 `HAL_GPIO_EXTI_Callback()` 回调函数，并传入参与中断的 GPIO。当按下连接到 PC13 信号的用户按钮时，ISR 启动一个无限循环，直到全局变量 `blink` 大于 0。此循环使 LD2 LED 快速闪烁。当 PB2 引脚被拉低时（请使用附录 C 中您 Nucleo 开发板的引脚图来识别 PB2 引脚的位置），`EXTI2_3_IRQHandler()`¹¹ 被触发，这导致 `HAL_GPIO_EXTI_IRQHandler()` 将 `blink` 变量设置为 0。此时 `EXTI4_15_IRQHandler()` 可以结束。每个中断的优先级在第 70 行和第 73 行配置：如您所见，由于基于 Cortex-M0/0+ 的微控制器（MCU）的中断优先级是静态的，我们必须在启用相应中断之前设置它。

¹¹请注意，对于 STM32F302 微控制器，与 EXTI 线 2 关联的中断请求的默认名称是 `EXTI2_TSC_IRQHandler`。如果您正在使用该微控制器，请参阅本书示例。

<!-- page: 193 -->

![Image from PDF page 193](../images/page-0193-image-01.png)

请注意，这是一种处理中断的非常糟糕的方式。在中断中锁定微控制器是一种糟糕的编程风格，也是嵌入式编程中所有问题的根源。不幸的是，考虑到本书在此处仍只涵盖少数主题，这是作者能想到的唯一示例。每个 ISR 的设计都应尽可能短，否则其他基本的 ISR 可能会被屏蔽很长时间，从而丢失来自其他外设的重要信息。

作为练习，尝试调整中断优先级，看看如果两个中断具有相同优先级时会发生什么。

![Image from PDF page 193](../images/page-0193-image-02.png)

![Image from PDF page 193](../images/page-0193-image-03.png)

可能会产生一个好问题：为什么不在第 87:89 行使用 `HAL_Delay()` 函数而不是忙等待（busywait）？答案很简单，并且与中断优先级直接相关。`HAL_Delay()` 在执行忙等待的同时，等待 SysTick 定时器递增全局变量 `uwTick`（一个以 1KHZ 频率递增的无符号 32 位整数）。然而，正如我们将在第 11 章中看到的，SysTick 定时器被配置为以中断模式工作，并且其中断优先级由 CubeMX 设置——默认情况下设置为尽可能低的优先级（请查看 `Core/Inc/stm32XXxx_hal_conf.h` 文件中的宏 `TICK_INT_PRIORITY`）。通过将 `EXTI15_10_IRQn` 中断的优先级级别设置为 1，将导致 SysTick 定时器的 ISR 永远不会触发，直到 `blink` 变量变为 0 且 ISR 可以终止。

![Image from PDF page 193](../images/page-0193-image-04.png)

您可能注意到，即使导线未接地，仅仅触摸导线就会触发中断。为什么会发生这种情况？导致中断“意外”触发的原因主要有两个。首先，现代微控制器试图最小化与使用内部上拉/下拉电阻相关的电源泄漏。因此，这些电阻的阻值选择得较高（大约 50kΩ）。如果您研究分压公式，您会发现当上拉/下拉电阻具有高阻值时，很容易将 I/O 拉低或拉高。其次，这里我们没有对输入引脚进行适当的去抖动（debouncing）。去抖动是减少由“不稳定”源（例如机械开关）产生的抖动影响的过程。通常，去抖动是通过硬件¹²或软件完成的，通过计算从输入状态首次变化开始经过的时间：在我们的情况下，如果输入保持低电平超过给定时段（通常 100ms 到 200ms 之间就足够了），那么我们可以说输入确实被接地了）。正如我们将在第 11 章中看到的，我们还可以使用配置为输入捕获模式工作的定时器的一个通道来检测 GPIO 何时改变状态。这使我们能够自动计算从第一个事件开始经过的时间。此外，定时器通道支持集成且可编程的硬件滤波器，这允许我们减少用于对 I/O 进行去抖动的元件数量。

¹²通常，在开关触点并联一个电容和一个电阻就足够了。例如，您可以查看 Nucleo 开发板的原理图，看看 ST 工程师如何对连接到 PC13 GPIO 的 USER 按钮进行去抖动。

<!-- page: 194 -->
