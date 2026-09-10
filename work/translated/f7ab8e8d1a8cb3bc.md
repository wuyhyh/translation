<!-- page: 615 -->

## 23.1 理解实时操作系统（RTOS）背后的概念

本段简要介绍了实时操作系统（real-time operating system）背后的主要概念。经验丰富的用户可以安全地跳过此部分。

![Image from PDF page 615](../images/page-0615-image-01.png)

除了中断服务程序（ISR）和异常（exception）处理程序外，迄今为止构建的所有示例都旨在使我们的应用程序仅由一个执行流组成。通常，从 main() 例程开始，一个庞大且无限的 while 循环执行固件任务：

```text
...
while(1) {
doOperation1();
doOperation2();
...
doOperationN();
}
```

每个 doOperationX() 所花费的时间大致由开发者估算，开发者有责任避免其中一个函数占用过长时间，从而阻止固件的其他部分

³https://blog.st.com/azure-rtos/ ⁴https://azure.microsoft.com/it-it/blog/new-azure-rtos-collaborations-with-leaders-in-the-semiconductor-industry/

<!-- page: 616 -->

正确运行。此外，函数的调用顺序也调度了它们的执行，定义了固件执行的操作序列。这确实是一种协作式调度（cooperative scheduling）⁵，其中每个函数通过定期自愿释放控制权来配合下一个活动的执行。

在这种早期的多道程序设计形式中，没有保证某个函数不会独占 CPU。应用程序设计者需要仔细确保每个函数都在尽可能短的时间内完成。在这种执行模型中，一个“无辜”的忙等待循环可能会产生灾难性的影响。让我们考虑以下伪代码：

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

这段代码在许多缺乏经验的嵌入式开发者中相当常见，并且在某些假设下也是正确的。然而，该代码存在一种微妙的怪异行为。blinkTask() 被设计为在释放控制权之前忙等待 500 毫秒。如果在此期间有数据通过 UART 接口到达，readUART2Task() 肯定会丢失一些数据⁶。编写 blinkTask() 的更好方法如下：

⁵经验丰富的用户会指出，在这种背景下谈论协作式调度是不正确的，有两个根本原因：任务的执行顺序是固定的（“调度”由程序员在固件开发期间计算得出），并且每个例程在退出时无法保存其执行上下文，也就是说，当 doOperationX() 例程返回时，其堆栈帧被销毁。正如我们稍后将看到的，协程是非抢占式多任务系统中子例程的泛化。⁶在高波特率下，轮询 UART 肯定完全不正确，但这里我们关注的是这一点。

<!-- page:617 -->

```text
void blinkTask() {
if(HAL_GetTick() - timeKeep > 500) {
HAL_GPIO_TooglePin(GPIOA, GPIO_PIN_5);
timeKeep = HAL_GetTick();
}
}
```

对该例程的简单修改确保了在大多数情况下我们不会丢失来自 UART 的数据，除非 UART 传输数据的速度很快。

如您所见，在协作式调度中，程序员承担着巨大的责任，以确保他们的代码不会影响固件的整体活动，从而引入性能瓶颈。

自愿释放执行流并非迄今为止所见代码的唯一限制。让我们更仔细地看看 blinkTask() 例程。在这里，我们需要一个全局变量⁷ timeKeep，以跟踪由 CubeHAL 每 1 毫秒递增的全局滴答计数器，并进行比较以检查是否已过去 500 毫秒。这是必需的，因为每次例程退出时，其执行上下文（即堆栈帧）会从主堆栈中弹出并被销毁。除非我们使用语言提供的一些棘手技巧⁸，否则没有办法在不丢失其上下文的情况下退出函数。

续例程（Continuation routines），缩写为协程（co-routines）或简称协程，是一种泛化非抢占式多任务中子例程概念的程序结构，它允许在特定位置暂停和恢复执行时具有多个入口点。协程需要语言运行时的特殊支持，传统上由 Scheme 等更高级的语言提供，但 Python 和 Perl 等更广泛使用的语言也提供某种形式的协程。协程被认为不是返回，而是让出（yield）执行流。例如，blinkTask() 可以使用协程重写如下：

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
