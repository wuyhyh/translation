<!-- page: 684 -->

## 现在我们将分析最复杂的部分：vPortSuppressTicksAndSleep() 函数。我们将把它划分为若干代码块，以便更简单地分析其代码。强烈建议在 IDE 中随时保留并查看实际代码。

<!-- page: 685 -->

```text
Filename: Core/Src/tickless-mode.c
89
void vPortSuppressTicksAndSleep(TickType_t xExpectedIdleTime) {
90
uint32_t ulCounterValue, ulCompleteTickPeriods;
91
eSleepModeStatus eSleepAction;
92
TickType_t xModifiableIdleTime;
93
const TickType_t xRegulatorOffIdleTime = 50;
```

94

```text
95
/* Make sure the TIM2 reload value does not overflow the counter. */
96
if (xExpectedIdleTime > xMaximumPossibleSuppressedTicks) {
97
xExpectedIdleTime = xMaximumPossibleSuppressedTicks;
98
}
```

99

```text
100
/* Calculate the reload value required to wait xExpectedIdleTime tick
101
periods. */
102
ulCounterValue = ulPeriodValueForOneTick * xExpectedIdleTime;
103
104
/* To avoid race conditions, enter a critical section.
*/
105
__disable_irq();
106
107
/* If a context switch is pending then abandon the low power entry as
108
the context switch might have been pended by an external interrupt that
109
requires processing. */
110
eSleepAction = eTaskConfirmSleepModeStatus();
111
if (eSleepAction == eAbortSleep) {
112
/* Re-enable interrupts. */
113
__enable_irq();
114
return;
115
} else if (eSleepAction == eNoTasksWaitingTimeout) {
116
/* Stop TIM2 */
117
HAL_TIM_Base_Stop_IT(&htim2);
118
119
/* A user definable macro that allows application code to be inserted
120
here.
Such application code can be used to minimize power consumption
121
further by turning off IO, peripheral clocks, the Flash, etc. */
122
configPRE_STOP_PROCESSING();
123
124
125
/* There are no running state tasks and no tasks that are blocked with a
126
time out.
Assuming the application does not care if the tick time slips
127
with respect to calendar time then enter a deep sleep that can only be
128
woken by (in this demo case) the user button being pushed on the
129
STM32L discovery board.
If the application does require the tick time
130
to keep better track of the calendar time then the RTC peripheral can be
131
used to make rough adjustments. */
132
HAL_PWR_EnterSTOPMode(PWR_MAINREGULATOR_ON, PWR_STOPENTRY_WFI);
133
134
/* A user definable macro that allows application code to be inserted
```

<!-- page: 686 -->

```text
135
here.
Such application code can be used to reverse any actions taken
136
by the configPRE_STOP_PROCESSING().
In this demo
137
configPOST_STOP_PROCESSING() is used to re-initialize the clocks that
138
were turned off when STOP mode was entered. */
139
configPOST_STOP_PROCESSING();
140
141
/* Restart tick. */
142
HAL_TIM_Base_Start_IT(&htim2);
143
144
/* Re-enable interrupts. */
145
__enable_irq();
```

## 该函数首先检查预期的空闲时间，即我们可以安全停止滴答生成的时间窗口，是否小于 xMaximumPossibleSuppressedTicks：该值在 prvSetupTimerInterrupt() 例程中根据给定的 Prescaler 和 Period 值进行计算。然后，在第 102 行，它计算要使用的 Period 值，以便定时器在 xExpectedIdleTime 时间后溢出。为了避免竞态条件，我们随后进入临界区（第 105 行），并调用 eTaskConfirmSleepModeStatus() 以决定如何继续执行滴答抑制过程。如果该函数返回 eNoTasksWaitingTimeout，则我们可以完全停止 TIM2 定时器，并进入停止模式，直到 MCU 被事件或中断唤醒。

```text
Filename: Core/Src/tickless-mode.c
147
else {
148
/* Stop TIM2 momentarily.
The time TIM2 is stopped for is not accounted for
149
in this implementation (as it is in the generic implementation) because the
150
clock is so slow it is unlikely to be stopped for a complete count period
151
anyway. */
152
HAL_TIM_Base_Stop_IT(&htim2);
153
154
/* The tick flag is set to false before sleeping.
If it is true when sleep
155
mode is exited then sleep mode was probably exited because the tick was
156
suppressed for the entire xExpectedIdleTime period. */
157
ucTickFlag = pdFALSE;
158
159
/* Trap underflow before the next calculation. */
160
configASSERT(ulCounterValue >= __HAL_TIM_GET_COUNTER(&htim2));
161
162
/* Adjust the TIM2 value to take into account that the current time
163
slice is already partially complete. */
164
ulCounterValue -= (uint32_t) __HAL_TIM_GET_COUNTER(&htim2);
165
166
/* Trap overflow/underflow before the calculated value is written to TIM2. */
167
configASSERT(ulCounterValue < ( uint32_t ) USHRT_MAX);
168
configASSERT(ulCounterValue != 0);
169
170
/* Update to use the calculated overflow value. */
```

<!-- page: 687 -->

```text
171
__HAL_TIM_SET_AUTORELOAD(&htim2, ulCounterValue);
172
__HAL_TIM_SET_COUNTER(&htim2, 0);
173
174
/* Restart the TIM2. */
175
HAL_TIM_Base_Start_IT(&htim2);
176
177
/* Allow the application to define some pre-sleep processing.
This is
178
the standard configPRE_SLEEP_PROCESSING() macro as described on the
179
FreeRTOS.org website. */
180
xModifiableIdleTime = xExpectedIdleTime;
181
configPRE_SLEEP_PROCESSING( xModifiableIdleTime );
182
183
/* xExpectedIdleTime being set to 0 by configPRE_SLEEP_PROCESSING()
184
means the application defined code has already executed the wait/sleep
185
instruction. */
186
if (xModifiableIdleTime > 0) {
187
/* The sleep mode used is dependent on the expected idle time
188
as the deeper the sleep the longer the wake up time.
See the
189
comments at the top of main_low_power.c.
Note xRegulatorOffIdleTime
190
is set purely for convenience of demonstration and is not intended
191
to be an optimized value. */
192
if (xModifiableIdleTime > xRegulatorOffIdleTime) {
193
/* A slightly lower power sleep mode with a longer wake up time. */
194
HAL_PWR_EnterSLEEPMode(PWR_LOWPOWERREGULATOR_ON, PWR_SLEEPENTRY_WFI);
195
} else {
196
/* A slightly higher power sleep mode with a faster wake up time. */
197
HAL_PWR_EnterSLEEPMode(PWR_MAINREGULATOR_ON, PWR_SLEEPENTRY_WFI);
198
}
199
}
```
