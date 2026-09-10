<!-- page: 191 -->

### which is completely different from the one defined in the HALs for Cortex-M3/4/7/33 based processors.

## The following example¹⁰ shows how the interrupt priority mechanism works.

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

¹⁰The example is designed to work with a Nucleo-F072RB board. Please, refer to other book examples if you have a different Nucleo board.

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

The code should be easy to understand if my previous explanation is clear. Here we have two IRQs associated to EXTI lines 2 and 13. The corresponding ISRs call the HAL HAL_GPIO_EXTI_IRQHandler() which in turn calls the HAL_GPIO_EXTI_Callback() callback passing the GPIO involved in the interrupt. When the user button connected to PC13 signal is pushed, the ISR starts an infinite loop until the blink global variables is >0. This loop makes the LD2 LED blinking quickly. When the PB2 pin is asserted low (use the pinout diagram for your Nucleo from Appendix C to identify PB2 pin position), the EXTI2_3_IRQHandler()¹¹ fires and this causes the HAL_GPIO_EXTI_IRQHandler() to set the blink variable to 0. The EXTI4_15_IRQHandler() can now end. The priority of each interrupt is configured at lines 70 and 73: as you can see, since the interrupt priority is static in Cortex-M0/0+ based MCUs, we have to set it before we enable the corresponding interrupt.

¹¹Please, take note that for STM32F302 MCUs the default name of the IRQ associated to EXTI line 2 is EXTI2_TSC_IRQHandler. Refer to book examples if you are working with this MCU.

<!-- page: 193 -->

![Image from PDF page 193](../images/page-0193-image-01.png)

Please, take note that this is a really bad way to deal with interrupts. Locking the MCU inside an interrupt is a poor programming style, and it is the root of all evil in embedded programming. Unfortunately, this is the only example that came up to the author’s mind, considering that at this point the book still covers few topics. Every ISR must be designed to last as little as possible, otherwise other fundamental ISRs could be masked for a long time loosing important information coming from other peripherals.

As exercise, try to play with interrupt priorities, and see what happens if both interrupts have the same priority.

![Image from PDF page 193](../images/page-0193-image-02.png)

![Image from PDF page 193](../images/page-0193-image-03.png)

A good question might arise: why not using the HAL_Delay() function instead of the busywait at lines 87:89? The answer is simple, and it is directly connected to interrupt priorities. The HAL_Delay() performs a busy-wait while waiting for the SysTick timer to increment the global uwTick variable (an unsigned 32-bit integer incremented at 1KHZ frequency). However, as we will see in Chapter 11, the SysTick timer is configured to work in interrupt mode and the interrupt priority is set by CubeMX - by default - at the lowest possible priority (take a look to the macro TICK_INT_PRIORITY inside the Core/Inc/stm32XXxx_hal_conf.h file). By setting the priority level of the EXTI15_10_IRQn interrupt to 1 will cause that the ISR of SysTick timer will never fire until the blink variable goes to 0 and the ISR can terminate.

![Image from PDF page 193](../images/page-0193-image-04.png)

You may notice that often the interrupt fires by simply touching the wire, even if it is not tied to the ground. Why does this happen? There are essentially two reasons that cause the interrupt to “accidentally” trigger. First of all, modern microcontrollers try to minimize the power leakages connected with the usage of internal pull-up/down resistors. So, the value of these resistors is chosen high (something around 50kΩ). If you play with the voltage divider equation, you can figure out that it is really easy to pull an I/O low or high when a pull-up/down resistor has a high resistance value. Secondly, here we are not doing adequate debouncing of the input pin. Debouncing is the process of minimizing the effect of bounces produced by “unstable” sources (e.g., a mechanical switch). Usually, debouncing is performed in hardware¹² or in software, by counting how much time is elapsed from the first variation of the input state: in our case, if the input remains low for more than a given period (usually something between 100ms and 200ms is sufficient), then we can say that the input has been effectively tied to the ground). As we will see in Chapter 11, we can also use one channel of a timer configured to work in input capture mode to detect when a GPIO changes state. This gives us the ability to automatically count how much time is elapsed from the first event. Moreover, timer channels support integrated and programmable hardware filters, which allow us to reduce the number of external components to debounce the I/Os.

¹²Usually, a capacitor and a resistor in parallel with the switch contacts are sufficient in most cases. For example, you can take a look at schematics of the Nucleo board to see how ST engineers have debounced the USER button connected to PC13 GPIO.

<!-- page: 194 -->
