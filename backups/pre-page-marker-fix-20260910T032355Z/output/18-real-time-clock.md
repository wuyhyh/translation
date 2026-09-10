<!-- page: 471 -->

# 18. 实时时钟

存在大量需要跟踪当前日期和时间的嵌入式应用。数据记录器、计时器、家用电器和控制设备只是其中有限的几个例子。传统上，微控制器通过专用集成电路（IC）进行接口连接，这些 IC 能够使用 SPI 或 I²C 总线进行通信。例如，同一家 ST Microelectronics 公司销售 M41T81¹ IC，这是一款流行的实时时钟（Real-Time Clock, RTC），它需要几个无源元件和一个 32kHz 振荡器来跟踪当前时间。此外，该 IC 还能够生成报警事件并充当看门狗定时器。

所有 STM32 微控制器都提供了一个集成的 RTC 单元，其功能不仅限于跟踪当前日期/时间。事实上，RTC 还提供了一些额外的相关功能，例如防篡改检测、生成报警事件以及从更深的低功耗模式中唤醒 MCU 的能力。本章展示了如何使用相关的 CubeHAL 模块来编程此外设。

## 18.1 RTC 外设简介

STM32 的 RTC 是一个独立的二进制编码十进制（Binary Coded Decimal, BCD）计数器。BCD 是一种二进制编码类型，其中十进制数的每一位都由固定数量的位独立表示。例如，RTC 定时器以以下方式表示当前小时：

- 使用两位编码小时的十位；
- 使用四位编码小时的个位；
- 使用三位编码分钟的十位；
- 使用四位编码分钟的个位。

![Image from PDF page 471](../images/page-0471-image-01.png)

图 18.1：STM32 MCU 中时间如何以 BCD 格式编码

图 18.1 展示了 STM32 RTC 如何以 BCD 格式编码当前小时。为什么要使用这种方法来编码日期/时间？这种跟踪当前日期/时间的方式是小型嵌入式系统的典型特征，它允许以人类可读的格式表示时间，而无需

¹http://bit.ly/2fj3vCM

<!-- page: 472 -->

执行任何类型的转换。传统上，高级操作系统使用无符号长整型变量来跟踪时间，该变量每秒自动递增。例如，UNIX 时间表示自纪元（Epoch）以来经过的秒数，纪元对应于 1970 年 1 月 1 日星期四 00:00:00。然而，将自该日期以来经过的秒数转换为当前日期/时间需要大量的 CPU 算力和固件空间。转换例程需要跟踪多个因素，例如一个月有多少天、闰年以及秒数等。BCD 编码允许立即以地球上许多人可理解的方式排列当前日期/时间，代价是内部电路更加复杂。

STM32 的 RTC 外设允许轻松配置和显示日历数据字段：

- 日历包括：
  - 亚秒（不可编程）
  - 秒
  - 分钟
  - 小时（12 小时或 24 小时格式）
  - 星期几（day）
  - 月中的第几天（date）
  - 月份
  - 年份
- 自动管理 28 天、29 天（闰年）、30 天和 31 天的月份
- 可通过软件编程调整夏令时

与大多数 STM32 外设不同，RTC 可以由三个独立的时钟源独立提供时钟：LSI、LSE 和 HSE。一系列专用的预分频器（prescaler）允许向日历单元提供 1Hz 时钟，无论时钟源是什么。当 RTC 的时钟源（RTCCLK）为 HSE 时，用户有责任正确配置预分频器，以便正确的时钟频率能够馈送 RTC。然而，CubeMX 被设计为根据指定的 HSE 晶振频率自动处理此问题。

尽管 RTC 提供了校正时钟不精确性的工具（如后文所述），但并非所有时钟源都适合实现 RTC 的良好精度，特别是当 MCU 工作在不同于环境温度的温度下时。如果精度对你的应用很重要，则强烈建议使用专用的外部 LSE 晶振，并根据晶振规格和 PCB 布局进行调谐。

RTC 的功能不仅限于日期/时间管理。RTC 提供两个独立的报警单元，分别称为 Alarm A 和 Alarm B，可用于在 RTC 计数器达到配置的报警值时生成事件。报警单元高度可定制：亚秒、秒、分钟、小时和日期字段可以独立选择或屏蔽，以提供丰富的报警组合。除了两个报警单元外，RTC 还提供一个独立的、可编程的专用唤醒单元，用于从更深的睡眠状态唤醒 MCU。事实上，

<!-- page: 473 -->

在下一章中我们将看到，RTC 是唯一能够以可编程方式从待机睡眠状态唤醒 MCU 的外设。

最后，RTC 提供了对给定输入进行采样以检测篡改的能力：由于在多个 STM32 微控制器中，RTC 外设可以由电池²供电，因此即使设备断电，它也能检测篡改。在检测到篡改时，会设置一个特定的寄存器，并且备份存储器（backup memory）的内容也会被清零。

## 18.2 HAL_RTC 模块

为了编程 RTC 外设，HAL 定义了 C 结构体 `RTC_HandleTypeDef`，其定义方式如下：

```text
typedef struct {
RTC_TypeDef
*Instance;
/* Register base address
*/
RTC_InitTypeDef
Init;
/* RTC required parameters
*/
HAL_LockTypeDef
Lock;
/* RTC locking object
*/
__IO HAL_RTCStateTypeDef
State;
/* Time communication state */
} RTC_HandleTypeDef;
```

该结构体中值得注意的字段只有 `Instance`，它是指向 RTC 外设描述符的指针，以及用于配置外设的 `Init` 字段。该字段是 C 结构体 `RTC_InitTypeDef` 的一个实例，其定义方式如下：

```text
typedef struct {
uint32_t HourFormat;
/* Specifies the RTC Hour Format. */
uint32_t AsynchPrediv;
/* Specifies the RTC Asynchronous Predivider value. */
uint32_t SynchPrediv;
/* Specifies the RTC Synchronous Predivider value. */
uint32_t OutPut;
/* Specifies which signal will be routed to the RTC output. */
uint32_t OutPutPolarity;
/* Specifies the polarity of the output signal. */
uint32_t OutPutType;
/* Specifies the RTC Output Pin mode. */
} RTC_InitTypeDef;
```

- `HourFormat`：此字段指定小时格式，它可以取值为 `RTC_HOURFORMAT_12` 以设置 AM/PM 小时格式，或取值为 `RTC_HOURFORMAT_24` 以指定 24 小时/天格式。
- `AsynchPrediv` 和 `SynchPrediv`：使用两个预分频器从 LSI/LSE/HSE 振荡器源派生出 1Hz 时钟，以供给 RTC 外设。第一个是异步预分频器，它是一个 7 位计数器，进而供给同步预分频器，后者是另一个 15 位计数器。这两个字段的值必须设置为使 1Hz 频率达到要求，依据公式

²在下一章中我们将看到，具有较高引脚数量的 STM32 微控制器提供多个独立的电源域。RTC 属于 VBAT 域，即所有通过 VBAT 引脚供电的外设集合。该域特别设计为连接到电池，并且属于该域的所有外设即使在主电源关闭（因此微控制器内核关闭）时也能继续工作。

<!-- page: 474 -->

公式 [1]，其中 `CalendarCLK` 是 LSI/LSE/HSE 之一。在撰写本章时，最新的 CubeMX 版本（4.22）无法自动推导 `AsynchPrediv` 和 `SynchPrediv` 字段的正确值。对于大多数相关的振荡器频率，您可以使用表 18.1 中报告的数值。

```text
CalendarCLK =
RTCCLK
(AsynchPrediv + 1)(SynchPrediv + 1)
[1]
```

表 18.1：根据最常见的时钟源，`AsynchPrediv` 和 `SynchPrediv` 字段的正确值

CalendarCLK AsynchPrediv SynchPrediv HSE_RTC = 1MHz 124 7999 LSE = 32.768kHz 127 255 LSI = 32kHz 127 249 LSI = 37kHz 127 295

- `OutPut`：指定路由到 RTC 输出的信号 I/O。它可以取值为 `RTC_OUTPUT_ALARMA`、`RTC_OUTPUT_ALARMB`、`RTC_OUTPUT_WAKEUP` 和 `RTC_OUTPUT_DISABLE`，以将输出路由到与报警 A、B、唤醒相关的信号，或禁用输出信号。请注意，与特定报警关联的实际 GPIO 是在微控制器开发期间设计的，并且是固定的。根据所使用的封装类型，可能只有一个信号 I/O 可用，并在三个报警源之间共享。例如，所有具有 LQFP-64 封装的 STM32 微控制器只有一个名为 AF1 的报警 I/O，并连接到 PC13 引脚。
- `OutPutPolarity`：此字段指定信号的输出极性，它可以取值为 `RTC_OUTPUT_POLARITY_HIGH` 和 `RTC_OUTPUT_POLARITY_LOW`。
- `OutPutType`：此字段指定输出信号的类型，它可以取值为 `RTC_OUTPUT_TYPE_OPENDRAIN` 和 `RTC_OUTPUT_TYPE_PUSHPULL`。

通常，为了配置 RTC 外设，我们使用函数：

```text
HAL_StatusTypeDef HAL_RTC_Init(RTC_HandleTypeDef *hrtc);
```

该函数接受指向之前看到的 `RTC_HandleTypeDef` 结构体实例的指针。

### 18.2.1 设置和获取当前日期/时间

CubeHAL 实现了独立的例程和 C 结构体来设置和获取当前日期和时间。函数：

<!-- page: 475 -->

```text
HAL_StatusTypeDef HAL_RTC_SetTime(RTC_HandleTypeDef *hrtc,
RTC_TimeTypeDef *sTime, uint32_t Format);
HAL_StatusTypeDef HAL_RTC_GetTime(RTC_HandleTypeDef *hrtc,
RTC_TimeTypeDef *sTime, uint32_t Format);
```

## 用于设置/获取当前时间，而函数：

```text
HAL_StatusTypeDef HAL_RTC_SetDate(RTC_HandleTypeDef *hrtc,
RTC_DateTypeDef *sDate, uint32_t Format);
HAL_StatusTypeDef HAL_RTC_GetDate(RTC_HandleTypeDef *hrtc,
RTC_DateTypeDef *sDate, uint32_t Format);
```

## 用于设置/获取当前日期。

## 用于设置/获取当前时间的 `RTC_TimeTypeDef` 结构体定义如下：

```text
typedef struct {
uint8_t Hours;
/* Specifies the RTC Time Hour.
This parameter must be a number between 0 and 12 if the
12 hours format is selected. Otherwise, it must be a
number between 0 and 23 if the 24 hours format is selected */
uint8_t Minutes;
/* Specifies the RTC Time Minutes.
This parameter must be a number between 0 and 59 */
uint8_t Seconds;
/* Specifies the RTC Time Seconds.
This parameter must be a number 0 and 59 */
uint8_t TimeFormat;
/* Specifies the RTC AM/PM Time. */
uint32_t SubSeconds;
/* Specifies the RTC_SSR RTC Sub Second register content.
Not used when setting the timer */
uint32_t SecondFraction; /* Specifies the range or granularity of Sub Second register */
uint32_t DayLightSaving; /* Specifies DayLight Save Operation. */
uint32_t StoreOperation; /* Specifies Store Operation value
*/
} RTC_TimeTypeDef;
```

## 让我们分析一下最重要字段的作用：

## - Hours, Minutes, Seconds：这些字段用于设置当前时间。
- TimeFormat：用于设置时间格式（12/24小时制），其值可以是 RTC_HOURFORMAT_12 或 RTC_HOURFORMAT_24。
- SubSeconds：当结构体 RTC_TimeTypeDef 由 HAL_RTC_GetTime() 例程填充时，此字段包含当前的亚秒值。它会被 HAL_RTC_SetTime() 例程忽略。此字段对应于 [0-1] 秒之间的时间单位范围，其粒度等于 1s/(SecondFraction+1)。
- SecondFraction：指定 SubSeconds 字段的粒度，对应于同步预分频因子值。此字段仅由 HAL_RTC_GetTime() 函数使用。
- DayLightSaving：此字段指定夏令时，其值可以是 RTC_DAYLIGHTSAVING_SUB1H、RTC_DAYLIGHTSAVING_ADD1H、RTC_DAYLIGHTSAVING_NONE。

## 用于设置/获取当前日期的 RTC_DateTypeDef 结构体定义如下：

<!-- page: 476 -->

```text
typedef struct {
uint8_t WeekDay;
/* Specifies the RTC Date WeekDay. */
uint8_t Month;
/* Specifies the RTC Date Month (in BCD format). */
uint8_t Date;
/* Specifies the RTC Date.
*/
uint8_t Year;
/* Specifies the RTC Date Year. */
} RTC_DateTypeDef;
```

所有四个与时间/日期相关的函数都将时间/日期相关字段的格式作为最后一个参数接受。该参数可以取 RTC_FORMAT_BIN 和 RTC_FORMAT_BCD 的值。如果传递 RTC_FORMAT_BIN 常量，则时间/日期相关字段以常规二进制格式表示。例如，时间“12:45”按原样表示。相反，如果传递 RTC_FORMAT_BCD 常量，则值以 BCD 表示。这意味着每个时间/日期相关字段（占用一个字节）必须被解释为两个子半字节，它们对应于十进制数的数字。因此，按照之前的相同示例，十进制数“12”在二进制格式中表示为 1810，这对应于十六进制表示中的 12（见图 18.2）。

![Image from PDF page 476](../images/page-0476-image-01.png)

图 18.2：以 BCD 格式编码的时间如何被返回

#### 18.2.1.1 读取日期/时间值的正确方式

当前日期/时间值不能随意读取，但必须遵循一个明确定义的过程。这是因为，默认情况下，我们无法直接访问 RTC 内部日期/时间寄存器。RTC 是一个独立运行的外设，不通过 APB 总线进行时钟驱动。当代码读取日历字段时，它访问的是包含由 RTC 时钟 (RTCCLK) 驱动的真实日历时间和日期副本的影子寄存器。该副本每两个 RTCCLK 周期执行一次，并与系统时钟 (SYSCLK) 同步。此外，即使我们不关心当前日期，我们也必须在调用 HAL_RTC_GetTime() 之后调用 HAL_RTC_GetDate()。这是因为调用 HAL_RTC_GetDate() 会解锁高阶日历影子寄存器中的值，以确保时间值和日期值之间的一致性。读取 RTC 当前时间会锁定日历影子寄存器中的值，直到读取当前日期为止。这是 STM32 平台新手经常犯的一个错误：当使用 HAL_RTC_GetTime() 访问时间相关字段时，除非我们读取相应影子寄存器中日期相关字段的内容，否则我们接收到的将是最后一次传输的时间。

在系统复位后或退出低功耗模式后，应用程序必须在读取日历影子寄存器之前，等待 RTC 内部寄存器和影子寄存器之间的同步。为了执行此操作，CubeHAL 提供了以下函数：

<!-- page: 477 -->

```text
HAL_StatusTypeDef HAL_RTC_WaitForSynchro(RTC_HandleTypeDef* hrtc);
```

然而，仅当我们在系统复位后或从低功耗模式唤醒后立即访问影子寄存器，且 SYSCLK 速度仍处于其最低频率（因为它由 HSI 供电）时，才需要调用此函数。如果 HCLK 速度至少是 RTCCLK 的八倍，则影子寄存器的同步会在几个时钟周期内完成。在使用 HAL_RTC_WaitForSynchro() 例程时，重要的是要记住，默认情况下，对所谓的备份域（包括 RTC 外设）的写模式访问是被禁用的，以防止因电源不稳定而导致外设寄存器损坏。然而，HAL_RTC_WaitForSynchro() 例程需要以写模式访问 RTC 寄存器，因此我们需要使用宏 __HAL_RTC_WRITEPROTECTION_DISABLE() 来启用对备份域的写模式访问，如下所示：

```text
1
/* Disable the write-protection */
2
__HAL_RTC_WRITEPROTECTION_DISABLE(&hrtc);
3
/* Wait until the shadow registers are synchronized */
4
HAL_RTC_WaitForSynchro(&hrtc);
5
/* Enable again the write-protection to prevent registers corruption */
6
__HAL_RTC_WRITEPROTECTION_ENABLE(&hrtc);
```

最后，可以绕过对影子寄存器的访问。在这种情况下，不必等待同步时间，但必须由软件检查日历寄存器的一致性。用户必须两次读取所需的日历字段值。然后比较两次读取序列的结果。如果结果匹配，则读取结果正确。如果不匹配，则必须再读取一次字段，第三次读取的结果有效。为了绕过影子寄存器，CubeHAL 提供了以下函数：

```text
HAL_StatusTypeDef HAL_RTCEx_EnableBypassShadow(RTC_HandleTypeDef* hrtc);
```

要重新启用影子寄存器访问，我们可以使用以下函数：

```text
HAL_StatusTypeDef HAL_RTCEx_DisableBypassShadow(RTC_HandleTypeDef* hrtc);
```

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

在下一章中，我们将看到 STM32 微控制器提供了选择性地禁用内部功能的能力，以减少功耗。多种低功耗模式使程序员能够决定最适合其需求的功耗水平，特别是在开发电池供电设备时。

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

### 18.2.4 时间戳生成与防篡改检测

RTC 外设根据所使用的封装不同，硬连线到若干信号 I/O 上。当这些 I/O 的状态发生变化时，可以利用它们生成时间戳。当前的日期/时间会被保存在专用寄存器中，如果已启用，相应的中断也会被触发。

要设置时间戳生成，CubeHAL 提供了以下函数：

```text
HAL_RTCEx_SetTimeStamp(RTC_HandleTypeDef *hrtc, uint32_t TimeStampEdge,
uint32_t RTC_TimeStampPin);
```

TimeStampEdge 参数指定激活时间戳的引脚边沿。该参数可以是以下值之一：RTC_TIMESTAMPEDGE_RISING 和 RTC_TIMESTAMPEDGE_- FALLING。RTC_TimeStampPin 指定用于生成时间戳的 I/O，它可以取值为 RTC_TIMESTAMPPIN_DEFAULT（通常对应 PC13 引脚），或者取值为 RTC_TIMESTAMPPIN_PA0 或 RTC_TIMESTAMPPIN_POS1 以指示替代引脚（通常是 PA0 或 PI8）。

要启用相应的中断，该中断与专用的 TAMP_STAMP_IRQn IRQ 相关联，我们可以使用以下函数：

```text
HAL_RTCEx_SetTimeStamp_IT(RTC_HandleTypeDef *hrtc, uint32_t TimeStampEdge,
uint32_t RTC_TimeStampPin);
```

HAL_RTCEx_TamperTimeStampIRQHandler() 是从 ISR 中调用的处理函数，而 HAL_- RTCEx_TimeStampEventCallback() 是对应的回调函数。相反，如果我们想以轮询模式使用时间戳功能，可以使用以下函数：

```text
HAL_RTCEx_PollForTimeStampEvent(RTC_HandleTypeDef *hrtc, uint32_t Timeout);
```

来轮询时间戳事件。要检索保存在时间戳寄存器中的日期/时间，可以使用以下函数：

```text
HAL_RTCEx_GetTimeStamp(RTC_HandleTypeDef *hrtc, RTC_TimeTypeDef *sTimeStamp,
RTC_DateTypeDef *sTimeStampDate, uint32_t Format);
```

相同的 I/O 也可以配置为检测篡改。CubeHAL 提供了专用的例程和 C 结构体来编程此功能。我们在此不详细讨论。有关此功能的更多信息，请参阅 CubeHAL 源代码（特别是 HAL_RTCEx 模块）。

### 18.2.5 RTC 校准

RTC 可以进行校准，以补偿 RTCCLK 源的不精确性。这对于需要高精度 RTC 的应用，以及要求在温度变化时保持 RTC 稳定性的应用特别有用。

RTC 外设提供两种类型的校准：粗校准和细校准。让我们来分析它们。

<!-- page: 482 -->

#### 18.2.5.1 RTC 粗校准

数字粗校准可以通过在异步预分频器输出端添加（正校准）或屏蔽（负校准）时钟周期来补偿晶体的不准确性。负校准可以以约 2 ppm 的分辨率执行，正校准可以以约 4 ppm 的分辨率执行。最大校准范围从 -63 ppm 到 126 ppm。

我们可以通过将异步预分频器之前的输出频率路由到专用引脚（通常与 AF1 引脚重合）来测量该频率。当此 I/O 用于此类操作时，也被称为 AFO_CALIB 引脚。通过使用示波器测量输出频率，我们可以评估 RTCCLK 的质量。AFO_CALIB 预期输出固定为 512Hz 频率的方波。

要设置粗校准，HAL 提供了以下函数：

```text
HAL_RTCEx_SetCoarseCalib(RTC_HandleTypeDef *hrtc, uint32_t CalibSign, uint32_t Value);
```

CalibSign 参数可以接受 RTC_CALIBSIGN_POSITIVE 和 RTC_CALIBSIGN_NEGA- TIVE 值，而 Value 参数在使用负号时可以从 0 到 63，步长为 2 ppm；在使用正号时可以从 0 到 126，步长为 4 ppm。

![Image from PDF page 482](../images/page-0482-image-01.jpeg)

图 18.3：RTC 时钟分配结构

在使用粗校准对 RTC 进行校准时，强调以下几点很重要。

- 无法检查校准结果，因为 512Hz 输出位于校准块之前（见图 18.3⁴）。在某些 STM32 微控制器中，由于 1Hz CK_Spre 输出位于粗校准块之后，因此可以检查校准。请参阅您微控制器的参考手册。
- 校准设置只能在初始化期间更改。因此，仅将粗校准用于静态校正。

#### 18.2.5.2 RTC 细校准

RTC 频率可以以约 0.954 ppm 的分辨率进行校准，范围从 -487.1 ppm 到 +488.5 ppm。频率校正通过使用一系列小调整来执行

⁴该图取自 ST 的 AN3371(http://bit.ly/2fcR1uE)。

<!-- page: 483 -->

（添加和/或同时减去单个 RTCCLK 脉冲）。这些调整在几秒（8、16 或 32 秒）的范围内均匀分布，因此即使在短时间观察下，RTC 也能得到很好的校准。

使用两个名为 CALP 和 CALM 的 RTC 寄存器，可以在选定的范围（8、16 或 32 秒）内添加和/或减去给定数量的 RTCCLK 脉冲。虽然 CALM 允许以精细分辨率将 RTC 频率降低多达 487.1 ppm，但位 CALP 可用于将频率增加 488.5 ppm。将 CALP 寄存器设置为 ‘1’ 实际上会在每 2¹¹ 个 RTCCLK 周期中插入一个额外的 RTCCLK 脉冲，这意味着在每个 32 秒周期中添加了 512 个时钟脉冲。通过使用 CALM 寄存器指定在 32 秒周期中要屏蔽的 RTCCLK 脉冲数量，可以减少要添加的时钟脉冲数量，直至 0。

同时使用 CALM 和 CALP，可以在 32 秒周期中添加 -511 到 +512 个 RTCCLK 周期的偏移量，这相当于 -487.1 ppm 到 +488.5 ppm 的校准范围，分辨率约为 0.954 ppm。给定输入频率 (FRT CCLK)，计算有效校准频率 (FCAL) 的公式如下：

FCAL = FRT CCLK × [1 + (CALP × 512 −CALM) (220 + CALM −CALP × 512)] [2]

要设置细校准，HAL 提供了以下函数：

```text
HAL_RTCEx_SetSmoothCalib(RTC_HandleTypeDef* hrtc, uint32_t SmoothCalibPeriod,
uint32_t SmoothCalibPlusPulses, uint32_t SmouthCalibMinusPulsesValue);
```

SmoothCalibPeriod 参数可以取表 18.4 中列出的值，并定义分布间隔。SmoothCalibPlusPulses 参数可以取 RTC_SMOOTHCALIB_- PLUSPULSES_SET 和 RTC_SMOOTHCALIB_PLUSPULSES_RESET 值，用于设置/复位 CALP 寄存器内的单个位。SmouthCalibMinusPulsesValue 参数设置要减去的时钟脉冲数量，可以是 0 到 511 之间的任何值。

表 18.4：SmoothCalibPeriod 参数的可用值

Wakeup counter clock source Description

RTC_SMOOTHCALIB_PERIOD_8SEC 细校准周期为 8s RTC_SMOOTHCALIB_PERIOD_16SEC 细校准周期为 16s RTC_SMOOTHCALIB_PERIOD_32SEC 细校准周期为 32s

与 RTC 粗校准不同，细校准对日历时钟 (RTC Clock) 的影响可以通过检查 AFO_CALIB 引脚的输出轻松检查。细校准也可以在线执行，因此可以在温度变化或检测到其他因素时进行更改。

<!-- page: 484 -->

#### 18.2.5.3 参考时钟检测

在某些应用中，RTC 可以使用外部参考时钟进行主动校准。参考时钟（频率为 50Hz 或 60Hz - 典型的市电频率）应具有比 32.768kHz LSE 时钟更高的精度。这就是为什么在引脚数较多的 STM32 微控制器中，RTC 提供了一个参考时钟输入（名为 RTC_50Hz 引脚），该引脚可用于补偿日历频率（1Hz）的不精确性。

RTC_50Hz 引脚应配置为输入浮空模式。此机制使日历的精度能够与参考时钟保持一致。通过使用以下函数启用参考时钟检测：

```text
HAL_StatusTypeDef HAL_RTCEx_SetRefClock(RTC_HandleTypeDef* hrtc);
```

当启用参考时钟检测时，异步预分频器和同步预分频器必须设置为其默认值：0x7F 和 0xFF。当启用参考时钟检测时，每个 1Hz 时钟边沿都会与最近的参考时钟边沿进行比较（如果在给定的时间窗口内找到该边沿）。在大多数情况下，这两个时钟边沿是对齐的。当 1Hz 时钟由于 LSE 时钟的不精确性而发生失准时，RTC 会稍微调整 1Hz 时钟，以便未来的 1Hz 时钟边沿能够对齐。更新窗口为三个 ck_calib 周期（ck_calib 是粗校准模块的输出 - 参见图 18.3）。

如果参考时钟停止，日历将仅基于 LSE 时钟持续更新。然后，RTC 使用以同步预分频器输出时钟（ck_spre）边沿为中心的检测窗口等待参考时钟。检测窗口为七个 ck_calib 周期。

参考时钟可能存在较大的局部偏差（例如在 500ppm 范围内），但从长期来看，其精度必须远高于 32kHz 石英晶体。检测系统仅在参考时钟丢失后需要重新检测时使用。由于检测窗口略大于参考时钟周期，该检测系统会带来 1 个 ck_ref 周期（对于 50Hz 参考时钟为 20ms）的不确定性，因为检测窗口内可能包含 2 个 ck_ref 边沿。随后使用更新窗口，由于更新窗口小于参考时钟周期，因此不会引入误差。我们假设 ck_ref 每天丢失不超过一次。因此，每月的总不确定性为 20ms * 1 * 30 = 0.6s，这远小于典型石英晶体的不确定性（对于 35ppm 石英晶体，每月为 1.53 分钟）。

## 18.3 使用备份 SRAM

大多数 STM32 微控制器提供一个额外的内存区域，称为备份内存（或 RTC 备份数据内存）。如果 VBAT 引脚连接到备份电源，当 VDD 关闭时，该内存由 VBAT 供电，因此其内容不会在系统复位时丢失。即使器件处于低功耗模式，备份内存中的内容仍然有效。相反，当发生篡改检测事件时，备份寄存器会被复位。

<!-- page: 485 -->

默认情况下，系统复位后，对所谓的备份域（包括备份内存和 RTC 寄存器）的写模式访问被禁用，以保护其免受因电源不稳定而导致的意外写访问。要修改整个域，从而修改备份内存，我们需要显式地遵循以下流程：

```text
• enable the power interface clock by using the macro __HAL_RCC_PWR_CLK_ENABLE();
• call the HAL_PWR_EnableBkUpAccess() function to enable the access to the backup domain (RTC
registers, RTC backup data memory).
• Use the functions HAL_RTCEx_BKUPWrite() and HAL_RTCEx_BKUPRead() function to write/read
inside the available backup registers (the number of registers differs among the several STM32
MCUs).
```

<!-- page: 486 -->

III 高级主题

[原文提取异常，第486页]
