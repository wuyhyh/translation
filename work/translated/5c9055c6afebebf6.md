<!-- page: 477 -->

### 18.2.2 配置闹钟

STM32 RTC 提供两个闹钟，分别命名为 Alarm A 和 Alarm B，它们具有相同的功能。用户可以通过编程在指定的时间或/和日期生成闹钟。要设置闹钟，我们使用以下函数：

<!-- page: 478 -->

```text
HAL_StatusTypeDef HAL_RTC_SetAlarm(RTC_HandleTypeDef *hrtc,
RTC_AlarmTypeDef *sAlarm, uint32_t Format);
```

我们最终可以通过使用以下函数轮询闹钟，直到事件发生：

```text
HAL_StatusTypeDef HAL_RTC_PollForAlarmAEvent(RTC_HandleTypeDef *hrtc, uint32_t Timeout);
```

可以配置闹钟，使其在触发时断言一个专用的中断。与两个闹钟关联的中断请求号（IRQ）均为 RTC_Alarm_IRQn，要配置闹钟处于中断模式，我们可以使用以下专用例程：

```text
HAL_StatusTypeDef HAL_RTC_SetAlarm_IT(RTC_HandleTypeDef *hrtc,
RTC_AlarmTypeDef *sAlarm, uint32_t Format);
```

与所有 CubeHAL 中断处理例程一样，我们需要从 RTC_Alarm_IRQn 的中断服务例程（ISR）中调用 HAL_RTC_AlarmIRQHandler()。为了接收闹钟事件的通知，我们可以实现相应的回调函数：

```text
void HAL_RTC_AlarmAEventCallback(RTC_HandleTypeDef *hrtc)
```

可以使用以下函数来停用闹钟：

```text
HAL_StatusTypeDef HAL_RTC_DeactivateAlarm(RTC_HandleTypeDef *hrtc, uint32_t Alarm);
```

用于设置闹钟的结构体 RTC_AlarmTypeDef 定义如下：

```text
typedef struct {
RTC_TimeTypeDef AlarmTime;
/* Specifies the RTC Alarm Time members */
uint32_t AlarmMask;
/* Specifies the RTC Alarm Masks. */
uint32_t AlarmSubSecondMask;
/* Specifies the RTC Alarm SubSeconds Masks. */
uint32_t AlarmDateWeekDaySel; /* Specifies the RTC Alarm is on Date or WeekDay. */
uint8_t AlarmDateWeekDay;
/* Specifies the RTC Alarm Date/WeekDay. */
uint32_t Alarm;
/* Specifies the alarm (A or B). */
} RTC_AlarmTypeDef;
```

- AlarmTime：此字段是之前看到的 RTC_TimeTypeDef 结构体的一个实例，用于设置闹钟时间。
- AlarmMask：闹钟由一个与 RTC 时间计数器长度相同的寄存器组成。当 RTC 计数器与闹钟寄存器中配置的值匹配时，它会生成一个事件。AlarmMask 字段定义了闹钟与 RTC 时间寄存器之间的比较标准。它可以采用表 18.2 中报告的一个或多个值（通过对它们进行位掩码操作）。例如，如果我们希望闹钟在 12:45:03 发生，我们使用 RTC_ALARMMASK_NONE 值。相反，如果我们希望每小时在指定的分钟和秒生成一次闹钟，我们可以使用值 RTC_ALARMMASK_HOURS。

<!-- page: 479 -->

表 18.2：用于设置闹钟行为的可用闹钟掩码

掩码值 闹钟行为

RTC_ALARMMASK_NONE 所有字段都用于闹钟比较（例如，闹钟在 12:45:03 发生） RTC_ALARMMASK_SECONDS 秒在闹钟比较中不重要（例如，闹钟在 12:45 的每一秒发生） RTC_ALARMMASK_SECONDS 秒在闹钟比较中不重要（例如，闹钟在 12:45 的每一秒发生） RTC_ALARMMASK_MINUTES 分钟在闹钟比较中不重要（例如，闹钟在 12:XX 的每一分钟的第 3 秒发生） RTC_ALARMMASK_HOURS 小时在闹钟比较中不重要（例如，闹钟在每 45 分钟的第 3 秒发生） RTC_ALARMMASK_DATEWEEKDAY 星期（或日期，如果已选择）在闹钟比较中不重要（例如，闹钟每天在 12:45:03 发生） RTC_ALARMMASK_ALL 闹钟每秒发生一次

- AlarmDateWeekDaySel：指定闹钟是按日期（月中的某一天）还是按星期（星期一、星期二等）设置的。它可以取值 RTC_ALARMDATEWEEKDAYSEL_DATE 或 RTC_ALARMDATEWEEKDAYSEL_WEEKDAY。
- AlarmDateWeekDay：如果 AlarmDateWeekDaySel 字段设置为 RTC_ALARMDATEWEEKDAYSEL_DATE，则此字段必须设置为 1-31 范围内的值。相反，如果 AlarmDateWeekDaySel 字段设置为 RTC_ALARMDATEWEEKDAYSEL_WEEKDAY，则此字段必须设置为符号常量 RTC_WEEKDAY_MONDAY、RTC_WEEKDAY_TUESDAY 等。
- AlarmSubSecondMask：RTC 时间的亚秒寄存器可用于生成粒度低于秒的事件。通过对亚秒寄存器的各个位进行掩码操作，可以生成每 1/128s、1/64s 等的事件。有关掩码可能性及其对闹钟行为影响的更多信息，请参阅 ST³ 的官方文档 AN3371。此功能允许例如将 RTC 用作 HAL 的时间基准发生器。ST 在 CubeHAL 项目中提供了这样一个示例。有关此功能的更多信息，请参阅它们。
- Alarm：它指定配置的闹钟，可以取值 RTC_ALARM_A 和 RTC_ALARM_B。

### 18.2.3 周期性唤醒单元

在下一章中，我们将看到 STM32 微控制器（microcontroller）提供了选择性地禁用内部功能的能力，以减少功耗。多种低功耗模式使程序员能够决定最适合其需求的功耗水平，特别是在开发电池供电设备时。

STM32 RTC 具有一个周期性时间基准和唤醒单元，当微控制器处于低功耗模式运行时，该单元可以唤醒系统。该单元是一个可编程的 16 位向下计数和自动重载定时器。当此计数器达到零时，会设置一个标志并生成一个中断（如果已启用）。唤醒单元具有以下特性：

³http://bit.ly/2fcR1uE

<!-- page: 480 -->

- 可编程的向下计数自动重载定时器。
- 特定的标志和中断，能够从低功耗模式中唤醒设备。
- 唤醒备用功能输出，可以路由到 RTC 闹钟输出（该输出在 Alarm A、Alarm B 或唤醒单元之间共享），并具有可配置的极性。
- 一组完整的预分频器，用于选择所需的等待周期。

唤醒计数器的计数频率可以由 RTCCLK 源导出，并最终进一步预分频，或者由日历时钟（即，在异步和同步预分频器之后）导出。这使得能够生成唤醒事件，其频率范围从 122μs 到超过 48 天（当为 LSE 振荡器选择外部时钟时）。

要设置唤醒事件，CubeHAL 提供了以下函数：

```text
HAL_StatusTypeDef HAL_RTCEx_SetWakeUpTimer(RTC_HandleTypeDef *hrtc,
uint32_t WakeUpCounter, uint32_t WakeUpClock);
```

其中 WakeUpCounter 参数设置唤醒计数器的自动重载值（即，周期），而 WakeUpClock 参数设置计数器频率，它可以取表 18.3 中列出的值之一。

表 18.3：WakeUpClock 参数的可用值

唤醒计数器时钟源 描述

RTC_WAKEUPCLOCK_RTCCLK_DIV2 唤醒计数器时钟源设置为 RTCCLK/2 RTC_WAKEUPCLOCK_RTCCLK_DIV4 唤醒计数器时钟源设置为 RTCCLK/4 RTC_WAKEUPCLOCK_RTCCLK_DIV8 唤醒计数器时钟源设置为 RTCCLK/8 RTC_WAKEUPCLOCK_RTCCLK_DIV16 唤醒计数器时钟源设置为 RTCCLK/16 RTC_WAKEUPCLOCK_CK_SPRE_16BITS 唤醒计数器时钟源设置为 CalendarCLK RTC_WAKEUPCLOCK_CK_SPRE_17BITS 唤醒计数器时钟源设置为 CalendarCLK，并且唤醒计数器增加一个额外的位（因此它可以计数到 0x1FFFF）。

一个独立的中断请求号（RTC_WKUP_IRQn）与唤醒计数器关联，可以使用以下函数启用它：

```text
HAL_RTCEx_SetWakeUpTimer_IT(RTC_HandleTypeDef *hrtc, uint32_t WakeUpCounter,
uint32_t WakeUpClock);
```

通常，我们必须从中断服务例程（ISR）中调用 HAL_RTCEx_WakeUpTimerIRQHandler()，并准备好通过实现 HAL_RTCEx_WakeUpTimerEventCallback() 来接收唤醒事件的通知。否则，如果在轮询模式下使用唤醒计数器，我们可以使用 HAL_RTCEx_PollForWakeUp-TimerEvent() 来检测唤醒事件（说实话，这不太有用）。

<!-- page: 481 -->
