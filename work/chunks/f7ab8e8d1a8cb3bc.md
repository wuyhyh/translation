<!-- page: 615 -->

## 23.1 Understanding the Concepts Underlying an RTOS

This paragraph gives a quick introduction to the main concepts underlying real-time Operating Systems. Experienced users can safely skip it.

![Image from PDF page 615](../images/page-0615-image-01.png)

Except for the ISRs and exception handlers, all the examples built so far are designed so that our applications are composed by just one execution stream. Typically, starting from the main() routine, a large and infinite while loop carries out firmware tasks:

```text
...
while(1) {
doOperation1();
doOperation2();
...
doOperationN();
}
```

The time spent by each doOperationX() is broadly estimated by the developer, who has the responsibility to avoid that one of those functions sticks for too much time, preventing other parts

³https://blog.st.com/azure-rtos/ ⁴https://azure.microsoft.com/it-it/blog/new-azure-rtos-collaborations-with-leaders-in-the-semiconductor-industry/

<!-- page: 616 -->

of the firmware from running correctly. Moreover, the calling order of the functions also schedules their execution, defining the sequence of operations performed by the firmware. This, indeed, is a form of cooperative scheduling⁵, where each function concurs to the execution of the next activity by voluntarily releasing the control periodically.

In this early form of multiprogramming, there is no guarantee that a function cannot monopolize the CPU. The application designer carefully needs to ensure that every function should be carried out in the shortest possible time. In this execution model, an “innocent” busy loop can have dramatic effects. Let us consider the following pseudo-code:

```text
uint32_t timeKeep = HAL_GetTick();
uint32_t uartData[20];
void blinkTask() {
while(HAL_GetTick() - timeKeep < 500);
HAL_GPIO_TooglePin(GPIOA, GPIO_PIN_5);
timeKeep = HAL_GetTick();
}
uint8_t readUART2Task() {
if(HAL_UART_Receive(&huart2, &uartData, 20, 1) == HAL_TIMEOUT)
return 0;
return 1;
}
while(1) {
blinkTask();
readUART2Task();
}
```

This code is quite common among several unexperienced embedded developers and, under certain hypothesis, it is also correct. However, that code has a subtle weird behavior. The blinkTask() is designed so that it will busy-spin for 500ms before releasing the control. If data arrives on the UART interface during this period, the readUART2Task() will certainly lose some data⁶. A better way to write down the blinkTask() is the following one:

⁵Experienced user will point out that it is not correct to talk about cooperative scheduling in this context for two fundamental reasons: the execution order of tasks is fixed (the “schedule” is computed by the programmer during the firmware development) and each routine is not able to save its execution context before leaving, that is the stack frame of the doOperationX() routine is destroyed when it returns. As we will see in a while, co-routines are a generalization of subroutines in non-preemptive multitasking systems. ⁶With high baudrates, polling the UART is certainly not correct at all, but here we are interested to the point.

<!-- page: 617 -->

```text
void blinkTask() {
if(HAL_GetTick() - timeKeep > 500) {
HAL_GPIO_TooglePin(GPIOA, GPIO_PIN_5);
timeKeep = HAL_GetTick();
}
}
```

A simple modification to that routine ensures that we will not lose data coming from the UART in the majority of situations, unless the UART transfers data quickly.

As you can see, with cooperative scheduling programmers have a great responsibility in ensuring their code will not affect the overall activities of the firmware, introducing performance bottlenecks.

The voluntary releasing of the execution flow is not the only limit of the code seen so far. Let us have a closer look at the blinkTask() routine. Here we need a global variable⁷, timeKeep, to keep track of the global tick counter incremented by the CubeHAL every 1ms and to perform a comparison to check if 500ms are elapsed. This is required because every time a routine exits, its execution context (that is, the stack frame) is popped from the main stack and it is destroyed. Unless we do not use some nasty tricks offered by the language⁸, there is no way to exit from a function without losing its context.

Continuation routines, abbreviated as co-routines or simply coroutines, are program structures that generalize the concept of subroutines for non-preemptive multitasking, by allowing multiple entry points for suspending and resuming execution at certain locations. Co-routines require special support from the run-time of the language, and they are traditionally provided from more highlevel languages like Scheme, but also more widespread languages like Python and Perl provide a form of co-routines. A co-routine is said not to return but to yield the execution flow. For example, the blinkTask() could be rewritten using co-routines in this way:

```text
1
void blinkTask() {
2
uint32_t timeKeep = HAL_GetTick();
3
while (1) {
4
if(HAL_GetTick() - timeKeep > 500) {
5
HAL_GPIO_TooglePin(GPIOA, GPIO_PIN_5);
6
timeKeep = HAL_GetTick();
```
