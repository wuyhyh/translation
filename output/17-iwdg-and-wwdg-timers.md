<!-- page: 464 -->

# 17. IWDG 和 WWDG 定时器

墨菲定律¹指出：凡是可能出错的事，终究会出错。对于嵌入式系统而言，这一点尤为戏剧化。除了可能影响软件的硬件故障外，即使是最谨慎的设计也可能存在导致设备行为异常的意外情况。如果设备被设计用于危险和关键场景，这种情况可能会带来严重的代价。

市场上几乎所有的嵌入式微控制器都提供看门狗定时器（WatchDog Timer, WDT）²。看门狗通常实现为一个自由运行的递减计数器：当其计数至零，或（对于窗口看门狗）计数器未在明确的时间窗口内重新加载为初始值时，便会触发 MCU 复位。一旦启用，固件必须持续将看门狗计数器寄存器刷新为其初始值，否则定时器会将 MCU 复位线拉低，从而引发硬复位。

对 WDT 进行恰当管理，有助于处理所有可能使嵌入式固件进入故障状态的不良情形（未处理的异常、堆栈溢出、访问无效内存位置、因电源不稳定导致的 SRAM 损坏、无限循环等）。此外，如果 WDT 能在定时器即将耗尽时发出警告，我们可以尝试恢复固件的正常活动，或者至少将设备置于安全状态。

STM32 微控制器提供两个独立的看门狗定时器：独立看门狗（Independent Watchdog, IWDG）和系统窗口看门狗（System Window Watchdog, WWDG）。它们具有几乎相同的特性，除了少数几个特性使得其中一个定时器在某些特定应用中比另一个更合适。本章展示了如何使用 CubeHAL 来利用这两个重要且常被低估的外设。

## 17.1 独立看门狗定时器

IWDG 是一个由低速内部（LSI）振荡器驱动的 12 位递减计数器定时器：这解释了“独立”这一形容词的含义，即该外设不由外设时钟供电，而外设时钟又由 HSI 或 HSE 振荡器生成。这是一项重要特性，它允许 IWDG 定时器在主时钟失效时仍能工作：即使 CPU 停止，看门狗仍会继续计数，并在达到零时复位 MCU。如果固件经过适当设计以应对此问题，MCU 可以使用 HSE 振荡器从主时钟故障中恢复。

在 STM32F0/F3/F7/L0/L4/L5/G0/G4 系列中，该定时器可以选择工作在窗口模式。这意味着我们可以设置一个时间窗口（范围从 0x0 到 0xFFF），以确定

¹这位作者更喜欢较不出名的史密斯定律，其内容是：墨菲是个乐观主义者。 ²确实存在一些成本极低的 MCU 不提供此功能，或者以不可靠的方式实现此功能，需要采用外部专用 IC。

<!-- page: 465 -->

何时允许刷新定时器计数器。如果在计数器达到窗口值之前刷新定时器，那么定时器达到零时 MCU 同样会复位。这确保了“事情”以正确的方式运行，特别是在 MCU 执行只能在明确定义的时间窗口内工作的重复任务时。

IWDG 定时器在复位 MCU 前需要多长时间？以下公式给出了 IWDG 定时器的更新事件：

<p align="center"><img src="../images/page-0465-image-01.png" alt="IWDG 更新事件公式"></p>

其中 `Period` 的范围为 0 至 4095，`IWDG_PSC` 对应一个专用的 3 位预分频器，取值范围为 2² 至 2⁸。例如，假设 LSI 时钟运行在 32 kHz，`Period` 等于 `0xFFF`，`IWDG_PSC` 等于 2²，则 IWDG 定时器将在以下时间后下溢：

<p align="center"><img src="../images/page-0465-image-02.png" alt="IWDG 下溢时间示例"></p>

IWDG 定时器还支持硬件看门狗功能。选项字节区域（Flash 内存中的一个区域，我们将在第 21 章中研究）中的一个特殊位可配置定时器，使其在每次系统复位后自动开始计数。

与常规定时器和其他微控制器架构不同，一旦 STM32 看门狗定时器启动，就没有办法停止它。这是在开发低功耗应用³时需要牢记的重要约束。

### 17.1.1 使用 CubeHAL 编程 IWDG 定时器

为了操作 IWDG 外设，HAL 定义了 C 结构体 IWDG_HandleTypeDef，其定义如下：

```c
typedef struct {
    IWDG_TypeDef                 *Instance; /* Pointer to IWDG descriptor */
    IWDG_InitTypeDef             Init;      /* IWDG initialization parameters */
    HAL_LockTypeDef              Lock;      /* IWDG locking object */
    __IO HAL_IWDG_StateTypeDef   State;     /* IWDG communication state */
} IWDG_HandleTypeDef;
```

为了配置 IWDG 外设，我们使用 C 结构体 IWDG_InitTypeDef 的一个实例，其定义如下：

³在第 19 章关于电源管理的章节中，我们将看到如何针对此限制采取措施。

<!-- page: 466 -->

```c
typedef struct {
    uint32_t Prescaler; /* Selects the prescaler of the IWDG */
    uint32_t Reload;    /* Specifies the IWDG down-counter reload value */
    uint32_t Window;    /* Specifies the window value to be compared to the down-counter */
} IWDG_InitTypeDef;
```

让我们研究一下这个 C 结构体的字段。

- `Prescaler`：此字段指定预分频值，可取 2² 至 2⁸ 的各个 2 的幂。为指定该值，CubeHAL 定义了七个宏：`IWDG_PRESCALER_4`、`IWDG_PRESCALER_8`、…、`IWDG_PRESCALER_256`。
- `Reload`：指定定时器周期，即刷新定时器时的自动重载值。其范围为 `0x0` 至 `0xFFF`（默认值）。
- `Window`：对于提供窗口 IWDG 的 STM32 MCU，此字段设置相应的窗口值，以允许在该窗口内刷新定时器。其范围为 `0x0` 至 `0xFFF`（默认值）。

为了配置并启动 IWDG 定时器，我们使用 CubeHAL 函数：

```c
HAL_StatusTypeDef HAL_IWDG_Init(IWDG_HandleTypeDef *hiwdg);
```

而在其达到零之前刷新它，我们使用函数：

```c
HAL_StatusTypeDef HAL_IWDG_Refresh(IWDG_HandleTypeDef *hiwdg);
```

## 17.2 系统窗口看门狗定时器

WWDG 是一个由 APB 时钟驱动的 7 位递减计数器定时器。与 IWDG 定时器不同，WWDG 被设计为必须在给定的时间窗口内进行刷新，否则将触发微控制器（MCU）复位。对于初学者来说，WWDG 定时器的工作方式可能显得有些反直觉。让我们逐步解释其工作原理。

WWDG 是一个 7 位定时器（参见图 17.1）。其计数器寄存器可设置为 `0x7F` 至 `0x40` 之间的值。刷新时，该值用于重新加载计数器寄存器（我们将此值称为 TS）。

<p align="center"><img src="../images/page-0466-image-01.png" alt="Image from PDF page 466"></p>

<p align="center">图 17.1：复位时 WWDG 计数器寄存器的内容</p>

<!-- page: 467 -->

WWDG 定时器具有如下特性：当计数器的第 7 位（图 17.1 中的 T6）从 1 变为 0 时，将发生系统复位。这意味着当计数器达到值 TE = `0x3F`（对应二进制 `0111111₂`）时，MCU 将被复位。

WWDG 由 APB 总线主时钟供电。时钟经过固定系数（4096）和可编程系数的分频，遵循以下公式：

<p align="center"><img src="../images/page-0467-image-02.png" alt="WWDG 预分频系数公式"></p>

例如，假设 `WWDG_PSC = 4096 · 8` 且 APB 时钟为 48 MHz，则计数器每 682.6 µs 递减 1。

如前所述，WWDG 定时器只能在给定的时间窗口内刷新：该可编程值可介于 TS 与 `0x40` 之间，且越接近 TS，窗口越宽。例如，如果将窗口寄存器配置为 TW = `0x5F`，则只能在计数器从 `0x5F` 递减至 `0x40` 期间刷新 WWDG 定时器。图 17.2 清楚地展示了时间窗口的作用。如果尝试在灰色区域（即 `0x7F` 与 `0x60` 之间，或计数器低于 `0x3F` 时）刷新 WWDG 定时器，MCU 将被复位。

<p align="center"><img src="../images/page-0467-image-01.png" alt="Image from PDF page 467"></p>

<p align="center">图 17.2：时间窗口如何定义允许刷新 WWDG 定时器的计数器区间</p>

时间窗口持续多久？这由以下公式定义：

<p align="center"><img src="../images/page-0467-image-03.png" alt="WWDG 时间窗口公式"></p>

其中：

<p align="center"><img src="../images/page-0467-image-04.png" alt="WWDG 周期公式"></p>

例如，假设将计数器刷新值（即 TS）设置为 `0x7F`，窗口值（即 TW）设置为 `0x5F`。此外，假设 APB 时钟等于 48 MHz，可编程分频系数等于 8。我们有：

<p align="center"><img src="../images/page-0467-image-05.png" alt="WWDG 最小时间窗口示例"></p>

<!-- page: 468 -->

这代表了我们必须等待的最小超时时间，之后才能刷新 WWDG 计数器。相反，最大超时时间由较低且固定的值 `0x40` 表示。再次使用 [2]，我们有：

<p align="center"><img src="../images/page-0468-image-01.png" alt="WWDG 最大时间窗口示例"></p>

这意味着，如果在上次刷新后的 22.5 ms 之前或 43.6 ms 之后刷新 WWDG 定时器，将导致系统复位。

WWDG 还有另一个重要特性：当计数器达到值 TI = `0x40` 时，即比导致 MCU 复位的 `0x3F` 早一个时钟节拍（tick），若已启用则会触发一个专用中断。该中断称为早期唤醒中断（Early Wakeup Interrupt, EWI），可用于在最后一刻刷新 WWDG 定时器，或将设备置于安全状态。专用的中断服务程序（ISR）名为 `WWDG_IRQHandler()`，它是紧随十五个 Cortex-M 异常之后的第一个 ISR。

最后，WWDG 也支持硬件看门狗功能，类似于 IWDG 定时器。

### 17.2.1 使用 CubeHAL 编程 WWDG 定时器

为了操作 WWDG 外设，HAL 定义了 C 结构体 WWDG_HandleTypeDef，其定义方式如下：

```c
typedef struct {
    WWDG_TypeDef                 *Instance; /* Pointer to WWDG descriptor */
    WWDG_InitTypeDef             Init;      /* WWDG initialization parameters */
    HAL_LockTypeDef              Lock;      /* WWDG locking object */
    __IO HAL_WWDG_StateTypeDef   State;     /* WWDG communication state */
} WWDG_HandleTypeDef;
```

为了配置 WWDG 外设，我们使用 C 结构体 WWDG_InitTypeDef 的一个实例，其定义方式如下：

```c
typedef struct {
    uint32_t Prescaler; /* Select the prescaler of the WWDG */
    uint32_t Window;    /* Specifies the window value to be compared to the down-counter */
    uint32_t Counter;   /* Specifies the WWDG down-counter reload value */
    uint32_t EWIMode;   /* Specifies if WWDG Early Wakeup Interupt is enable or not.
                           This parameter can be a value of @ref WWDG_EWI_Mode */
} WWDG_InitTypeDef;
```

让我们研究一下这个 C 结构体的字段。

- `Prescaler`：此字段指定预分频值，可取 1 至 8 之间的各个 2 的幂。为指定该值，CubeHAL 定义了四个宏：`WWDG_PRESCALER_1`、`WWDG_PRESCALER_2`、…、`WWDG_PRESCALER_8`。
- `Window`：此字段设置允许刷新定时器的相应窗口值。其范围为 `Counter` 字段的值（默认值）至 `0x3F`。
- `Counter`：指定定时器周期，即刷新定时器时的重载值。其范围为 `0x7F`（默认值）至 `0x3F`。
- `EWIMode`：此字段启用早期唤醒中断（EWI），可取 `WWDG_EWI_ENABLE` 和 `WWDG_EWI_DISABLE`。

<!-- page: 469 -->

为了配置并启动 WWDG 定时器，我们使用 CubeHAL 函数：

```c
HAL_StatusTypeDef HAL_WWDG_Init(WWDG_HandleTypeDef *hwwdg);
```

当 WWDG 定时器启用 EWI 模式时，必须实现 `WWDG_IRQHandler()` ISR 并调用以下函数：

```c
void HAL_WWDG_IRQHandler(WWDG_HandleTypeDef *hwwdg);
```

在中断触发时收到通知的正确方法是实现回调例程：

```c
void HAL_WWDG_EarlyWakeupCallback(WWDG_HandleTypeDef* hwwdg);
```

为了在时间窗口内刷新 WWDG 定时器，我们使用以下函数：

```c
HAL_StatusTypeDef HAL_WWDG_Refresh(WWDG_HandleTypeDef *hwwdg, uint32_t Counter);
```

其中 `Counter` 参数对应于要在 WWDG 计数器寄存器中重载的值。

最后，由于 WWDT 定时器由 APB 时钟驱动，我们需要使用宏 `__HAL_RCC_WWDG_CLK_ENABLE()` 来启用外设时钟。

## 17.3 检测由看门狗定时器引起的系统复位

检测系统复位是否由看门狗定时器超时引起可能很有用。这有助于我们在调试会话期间了解问题所在。复位与时钟控制（RCC）外设中的一个寄存器包含两个特殊位，可用于检测此事件。

要检测复位是否由 IWDG 定时器引起，我们可以使用以下宏检查相应的标志：

<!-- page: 470 -->

```c
__HAL_RCC_GET_FLAG(RCC_FLAG_IWDGRST);
```

而对于 WWDG 定时器，我们可以检查另一个标志：

```c
__HAL_RCC_GET_FLAG(RCC_FLAG_WWDGRST));
```

## 17.4 在调试会话期间冻结看门狗定时器

在调试会话期间，WWDG 和 IWDG 定时器将继续计数。这将阻止我们进行单步调试。我们可以配置调试接口，以便在 MCU 停止时使用以下宏暂停看门狗定时器：

```c
__HAL_DBGMCU_FREEZE_IWDG();
__HAL_DBGMCU_FREEZE_WWDG();
```

## 17.5 为您的应用选择合适的看门狗定时器

两种看门狗定时器具有相似的功能，并且执行相同的工作：如果我们在给定时间内未刷新其计数器寄存器，则复位 MCU。但是，何时最好优先选择一种定时器而非另一种？

当需要确认主时钟是否正常工作时，应优先选择 IWDG 定时器。由于 IWDG 由独立的 LSI 提供时钟，因此它有助于检测此类故障。此外，如果正在使用实时操作系统（RTOS），可以设置一个配置为最高优先级的独立线程，并使用软件定时器定期刷新 IWDG 定时器。这也有助于我们了解内核是否正在正确调度线程。

当我们需要确保某些操作在固定且特征明确的时间窗口内完成时，应优先选择 WWDG 定时器而非 IWDG 定时器。如果该过程花费的时间少于或多于该时间窗口，将无法在该时间窗口内刷新定时器，从而导致系统复位。此外，如果我们希望执行关键操作（例如将机器置于安全状态或将特殊数据保存到非易失性存储器中），WWDG 是合适的选择：借助早期警告中断（IRQ），我们可以获知系统复位正在进行中。
