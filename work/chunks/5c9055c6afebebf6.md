<!-- page: 477 -->

### 18.2.2 Configuring Alarms

STM32 RTC provides two alarms, named Alarm A and Alarm B, which have the same functionalities. An alarm can be generated at a given time or/and date programmed by the user. To setup an alarm we use the function:

<!-- page: 478 -->

```text
HAL_StatusTypeDef HAL_RTC_SetAlarm(RTC_HandleTypeDef *hrtc,
RTC_AlarmTypeDef *sAlarm, uint32_t Format);
```

We can eventually poll an alarm until the event has occurred by using the function:

```text
HAL_StatusTypeDef HAL_RTC_PollForAlarmAEvent(RTC_HandleTypeDef *hrtc, uint32_t Timeout);
```

An alarm can be configured so that it asserts a dedicated interrupt when it fires. The IRQ associated to both the alarms is the RTC_Alarm_IRQn, and to configure an alarm in interrupt mode we can use the following dedicated routine:

```text
HAL_StatusTypeDef HAL_RTC_SetAlarm_IT(RTC_HandleTypeDef *hrtc,
RTC_AlarmTypeDef *sAlarm, uint32_t Format);
```

Like all CubeHAL interrupt handler routines, we need to invoke the HAL_RTC_AlarmIRQHandler() from the RTC_Alarm_IRQn ISR. To be notified from the alarm event, we can implement the corresponding callback:

```text
void HAL_RTC_AlarmAEventCallback(RTC_HandleTypeDef *hrtc)
```

An alarm can be deactivated by using the function:

```text
HAL_StatusTypeDef HAL_RTC_DeactivateAlarm(RTC_HandleTypeDef *hrtc, uint32_t Alarm);
```

The struct RTC_AlarmTypeDef, used to setup an alarm, is defined in the following way:

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

- AlarmTime: this field is an instance of the RTC_TimeTypeDef struct seen before, and it is used to setup the alarm time.
- AlarmMask: an alarm consists of a register with the same length as the RTC time counter. When the RTC counter matches the value configured in the alarm register, it generates an event. The AlarmMask field defines the comparison criteria between the alarm and the RTC time register. It can assume one or more values (by bit-masking them) from those reported in Table 18.2. For example, if we want that the alarm occurs at 12:45:03, we use the RTC_ALARMMASK_NONE value. If, instead, we want to generate an alarm every hour, at a given minute and second, we can use the value RTC_ALARMMASK_HOURS.

<!-- page: 479 -->

Table 18.2: Available alarm masks to set up the alarm behaviour

Mask value Alarm behaviour

RTC_ALARMMASK_NONE All fields are used in alarm comparison (e.g., alarm occurs at 12:45:03) RTC_ALARMMASK_SECONDS Seconds do not matter in alarm comparison(e.g., alarm occurs at every seconds of 12:45) RTC_ALARMMASK_SECONDS Seconds do not matter in alarm comparison(e.g., alarm occurs at every seconds of 12:45) RTC_ALARMMASK_MINUTES Minutes do not matter in alarm comparison (e.g., alarm occurs at the 3rd second of every minute of 12:XX) RTC_ALARMMASK_HOURS Hours do not matter in alarm comparison (e.g., alarm occurs at the 3rd second of every 45th minute) RTC_ALARMMASK_DATEWEEKDAY Week day (or date, if selected) do not matter in alarm comparison (e.g., alarm occurs all days at 12:45:03) RTC_ALARMMASK_ALL Alarm occurs every second

- AlarmDateWeekDaySel: specifies if the alarm is set on a date (day of the month) or on a weekday (monday, tuesday, etc.). It can assume the value RTC_ALARMDATEWEEKDAYSEL_DATE or RTC_ALARMDATEWEEKDAYSEL_WEEKDAY.
- AlarmDateWeekDay: if the AlarmDateWeekDaySel field is set to RTC_ALARMDATEWEEKDAYSEL_DATE, then this field must be set to a value in the 1-31 range. Instead, if the AlarmDateWeekDaySel field is set to RTC_ALARMDATEWEEKDAYSEL_WEEKDAY, then this field must be set to symbolic constants RTC_WEEKDAY_MONDAY, RTC_WEEKDAY_TUESDAY and so on.
- AlarmSubSecondMask: the sub-seconds register of the RTC time can be used to generate events with granularity lower than the second. By masking individual bits of the sub-seconds register it is possible to generate events every 1/128s, 1/64s, and so on. For more information about the masking possibilities, and their effect on the alarm behaviour, refer to the official AN3371 from ST³. This functionality allows, for example, to use the RTC as timebase generator for the HAL. ST provides a such example in the CubeHAL projects. Refer to them for more about this.
- Alarm: it specifies the configured alarm, and it can assume the values RTC_ALARM_A and RTC_- ALARM_B.

### 18.2.3 Periodic Wakeup Unit

In the next chapter we will see that STM32 microcontrollers provide the ability to selectively disable internal functionalities in order to reduce the power consumption. Several low-power modes give to programmers the possibility to decide the power consumption level that best fits his needs, especially when developing battery-powered devices.

The STM32 RTC features a periodic timebase and wakeup unit that can wakeup the system when the microcontroller operates in low-power modes. This unit is a programmable 16-bit down-counting and auto-reload timer. When this counter reaches zero, a flag is set and an interrupt (if enabled) is generated. The wakeup unit has the following features:

³http://bit.ly/2fcR1uE

<!-- page: 480 -->

- Programmable down-counting auto-reload timer.
- Specific flag and interrupt able of waking up the device from low power modes.
- Wakeup alternate function output that can be routed to RTC alarm output (the output is shared between Alarm A, Alarm B or Wakeup unit) with configurable polarity.
- A full set of prescalers to select the desired waiting period.

The wakeup counter counting frequency can be derived either by the RTCCLK source, and eventually further prescaled, or by the calendar clock (that is, after the asynchronous and synchronous prescalers). This gives the possibility to generate wakeup events with a frequency ranging from 122μs up to more than 48 days when an external clock is chosen for the LSE oscillator.

To setup a wakeup event, the CubeHAL provides the function:

```text
HAL_StatusTypeDef HAL_RTCEx_SetWakeUpTimer(RTC_HandleTypeDef *hrtc,
uint32_t WakeUpCounter, uint32_t WakeUpClock);
```

where the WakeUpCounter parameter sets the autoreload value (that is, the period) of the wakeup counter, and the WakeUpClock parameters sets the counter frequency, and it can assume one of the values listed in Table 18.3.

Table 18.3: Available values for the WakeUpClock parameter

Wakeup counter clock source Description

RTC_WAKEUPCLOCK_RTCCLK_DIV2 The wakeup counter clock source is set to RTCCLK/2 RTC_WAKEUPCLOCK_RTCCLK_DIV4 The wakeup counter clock source is set to RTCCLK/4 RTC_WAKEUPCLOCK_RTCCLK_DIV8 The wakeup counter clock source is set to RTCCLK/8 RTC_WAKEUPCLOCK_RTCCLK_DIV16 The wakeup counter clock source is set to RTCCLK/16 RTC_WAKEUPCLOCK_CK_SPRE_16BITS The wakeup counter clock source is set to CalendarCLK RTC_WAKEUPCLOCK_CK_SPRE_17BITS The wakeup counter clock source is set to CalendarCLK and the wakeup counter increases of an additional bit (so it can count up to 0x1FFFF).

An independent IRQ (RTC_WKUP_IRQn) is associated with the wakeup counter, and it can be enabled by using the function:

```text
HAL_RTCEx_SetWakeUpTimer_IT(RTC_HandleTypeDef *hrtc, uint32_t WakeUpCounter,
uint32_t WakeUpClock);
```

As usual, we must call the HAL_RTCEx_WakeUpTimerIRQHandler() from the ISR, and be prepared to be notified of the wakeup event by implementing the HAL_RTCEx_WakeUpTimerEventCallback(). Otherwise, if using the wakeup counter in polling mode, we can use the HAL_RTCEx_PollForWakeUp- TimerEvent() to detect the wakeup event (not that useful to be honest).

<!-- page: 481 -->
