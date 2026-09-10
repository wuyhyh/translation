<!-- page: 623 -->

#### 23.2.1.1 如何使用 CubeMX 配置 FreeRTOS

CubeMX 允许轻松地将 FreeRTOS 添加到现有项目中。一旦您在 CubeMX 中配置了 MCU 外设，就可以通过在“类别”窗格的“中间件”部分中选择所需的 CMSIS-RTOS 封装（V1 或 V2）来轻松启用 FreeRTOS 中间件，如图 23.5 所示。

![Image from PDF page 623](../images/page-0623-image-01.jpeg)

图 23.5：如何在 CubeMX 中启用 FreeRTOS 中间件

在配置部分，可以设置 FreeRTOS 的配置参数。我们将在本章中分析其中最重要的参数。一旦生成项目，CubeMX 会显示一条警告消息（见图 23.6）。让我们解释一下这两条消息的含义。

第一条消息提醒您使用不同于 SysTick 的定时器来生成 HAL 时基。CubeMX 提出这一要求是因为 FreeRTOS 被设计为自动将 SysTick 中断（IRQ）优先级设置为最低（即优先级编号最高）。这是 FreeRTOS 的架构要求，不幸的是，这与 HAL 的设计方式相冲突。

正如之前多次提到的，STM32Cube HAL 是围绕唯一的时基源构建的，通常就是 SysTick 定时器。SysTick_Handler() 中断服务例程（ISR）每 1ms 自动递增全局 tick 计数器。HAL 使用这个唯一的计数器来实现 HAL_Delay() 函数，该函数在许多 HAL 例程中被频繁使用。这些 HAL 例程反过来又可能被 HAL_<PPP>_IRQHandler() 函数调用，而这些函数是在 ISR 上下文中执行的（例如，HAL_TIM_IRQHandler() 是从定时器的 ISR 中调用的）。如果 SysTick 中断未配置为以最高优先级中断（在基于 Cortex-M 的处理器中为 0）运行，那么从 ISR 上下文中调用 HAL_Delay() 可能会导致死锁¹⁷，如果调用 HAL_Delay() 的 ISR 的优先级高于 SysTick 定时器的优先级（如果您使用 FreeRTOS，如前所述，这种情况总是成立的）。因此，最好使用另一个定时器作为 HAL 的时基。要更改 HAL 时基源，请遵循第 11 章中的说明。

¹⁷在并发编程中，死锁是一种情况，其中两个或更多并发执行流彼此等待对方完成，因此谁也无法完成。陷入死锁并非难事，所有程序员迟早都会遇到这种难以调试的事件。

<!-- page: 624 -->

另一条警告消息与在多线程应用程序中使用来自 newlib 库（标准 C 运行时库）或 newlib-nano 库（紧凑 C 运行时库）的某些函数有关。我们将在本章后面深入探讨这个话题。目前，请考虑如果您打算从多个线程（包括中断处理程序）中调用标准 C 例程，必须特别小心地处理这些调用。

![Image from PDF page 624](../images/page-0624-image-01.jpeg)

图 23.6：关于 HAL 时基生成器和 newlib 重入性的警告消息

## 23.3 线程管理

一旦我们配置好 Eclipse 项目，就可以开始使用 CMSIS-RTOS 层，进而使用 FreeRTOS 进行编码。

在所有实时操作系统（RTOS）的基础中都有线程的概念，我们在本章的第一段中已经分析过。线程无非是一个 C 函数，FreeRTOS 要求以以下方式定义它：

```text
void ThreadFunc(void const *argument) {
while(1) {
...
}
osThreadTerminate(osThreadGetId());
}
```

函数 osThreadTerminate() 用于终止一个线程，它接受线程 ID（TID），我们稍后会看到。一个线程通常由一个包含线程指令的无限循环组成。将 osThreadTerminate() 放置在该循环之外通常是一种预防措施，以防控制流退出该循环，因为简单地从函数返回来终止线程是不正确的。向 osThreadTerminate() 函数传递 NULL 参数会导致该函数返回 osErrorParameter 错误，而不会正确删除线程。因此，确保通过传递正确的 TID 来调用 osThreadTerminate()。

要使用 CMSIS-RTOS v2 API（或简称为 CMSIS-RTOS2）启动一个新线程，我们使用以下函数：

```text
osThreadId_t osThreadNew (osThreadFunc_t func, void *argument, const osThreadAttr_t *attr);
```

osThreadAttr_t 是线程属性描述符，是一个以以下方式定义的 C 结构体：

<!-- page: 625 -->

```text
typedef struct {
const char
*name;
/* Thread name */
uint32_t
attr_bits;
/* Bitmask to configure the thread:
this is meaningless in FreeR\
TOS */
void
*cb_mem;
/* Control block to hold thread's data (default: NULL).
Used only for static allocation */
uint32_t
cb_size;
/* Size of provided memory for control block (default: 0) */
void
*stack_mem; /* Pointer to the memory holding the thread stack (default: NULL)\
.
Used only for static allocation */
uint32_t
stack_size; /* Size of provided memory for stack (default: 128 * 4) */
osPriority_t
priority;
/* Initial thread priority (default: osPriorityNormal) */
TZ_ModuleId_t
tz_module;
/* TrustZone module identifier (used in Cortex-M33 based MCUs) */
uint32_t
reserved;
/* Reserved (must be 0) */
} osThreadAttr_t;
```
