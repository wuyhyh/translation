<!-- page: 623 -->

#### 23.2.1.1 How to Configure FreeRTOS Using CubeMX

CubeMX allows to easily add FreeRTOS to an existing project. Once you have configured the MCU peripherals in CubeMX, you can easily enable the FreeRTOS middleware by selecting the wanted CMSIS-RTOS wrapper (V1 or V2) in the Middleware section of the Categories pane, as shown in Figure 23.5.

![Image from PDF page 623](../images/page-0623-image-01.jpeg)

Figure 23.5: How to enable the FreeRTOS middleware in CubeMX

In the configuration section it is possible to set the FreeRTOS configuration parameters. We will analyze the most relevant ones in this chapter. Once you generate the project, CubeMX will show you a warning message (see Figure 23.6). Let us explain the meaning of those two messages.

The first message warns you to use a timer different from the SysTick one for the HAL timebase generation. CubeMX asks this because FreeRTOS is designed so that it automatically sets the SysTick IRQ priority to the lowest one (highest priority number). This is an architectural requirement of FreeRTOS, which unfortunately conflicts with the way the HAL is designed.

As said several other times before, the STM32Cube HAL is built around a unique timebase source, which usually is SysTick timer. SysTick_Handler() ISR automatically increments the global tick counter every 1ms. The HAL uses this unique counter for the HAL_Delay() function, which is used often in several HAL routines. These HAL routines can in turn called by the HAL_<PPP>_IRQHandler() functions, which are executed in the context of an ISR (for example, the HAL_TIM_IRQHandler() is called from the ISR of a timer). If the SysTick IRQ is not configured to run at the highest priority interrupt (which is 0 in Cortex-M based processors), then calling the HAL_Delay() from an ISR context may lead to deadlocks¹⁷ if the priority of the ISR that makes call to the HAL_Delay() is higher than the one of the SysTick timer (and this is always true if you use FreeRTOS, as said before). So, it is best to use another timer for the HAL. To change the HAL timebase source, follow the instructions written in Chapter 11.

¹⁷In concurrent programming, a deadlock is a situation in which two or more concurrent execution streams are each waiting for the other to finish, and thus neither ever does. Incur in deadlock is anything but difficult, and all programmers soon or later will encounter this hard-to-debug event.

<!-- page: 624 -->

The other warning message is related to usage of some functions from the newlib library (the standard C run-time library) or from the newlib-nano library (the compact C run-time library) in multi-thread applications. We will deepen this topic later in this chapter. For now, consider that the usage of standard C routines must be handled with special care if you are going to call them from more than a thread (including interrupt handlers).

![Image from PDF page 624](../images/page-0624-image-01.jpeg)

Figure 23.6: The warning messages about timebase generator for the HAL and re-entrancy of newlib

## 23.3 Thread Management

Once we have configured the Eclipse project, we can start coding using the CMSIS-RTOS layer and hence FreeRTOS.

At the base of all RTOSes there is the notion of thread, which we have analyzed in the first paragraph of this chapter. A thread is nothing more than a C function, which FreeRTOS requires to be defined in the following way:

```text
void ThreadFunc(void const *argument) {
while(1) {
...
}
osThreadTerminate(osThreadGetId());
}
```

The function osThreadTerminate() is used to terminate a thread, and it accepts the Thread ID (TID), which we are going to see in a while. A thread is usually made of an infinite loop that contains the thread instructions. Placing the osThreadTerminate() outside that loop is usually a precaution in case the control exits from that loop, because it is not correct to terminate a thread by simply returning from its function. Passing the NULL parameter to the osThreadTerminate() function will cause that the function returns the osErrorParameter error, without correctly deleting the thread. So ensure that the osThreadTerminate() is invoked by passing the correct TID.

To start a new thread with the CMSIS-RTOS v2 API (or simply CMSIS-RTOS2) we use the following function:

```text
osThreadId_t osThreadNew (osThreadFunc_t func, void *argument, const osThreadAttr_t *attr);
```

The osThreadAttr_t is the thread attribute descriptor, a C struct defined in the following way:

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
