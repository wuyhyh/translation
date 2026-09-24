<!-- page: 614 -->

# 23. 运行 FreeRTOS

充分利用 32 位微控制器提供的计算能力并不容易，尤其是对于功能强大的 STM32F4/G4/F7/H7 系列而言。除非我们的设备只需要执行简单的任务，否则在固件开发期间，计算资源的正确分配需要特别小心。此外，使用不当的同步结构以及设计不良的中断服务例程，可能导致重要异步事件的丢失，并导致设备整体行为不可预测。

实时操作系统（real-time operating system，RTOS）利用 Cortex-M 内核提供的异常系统，为程序员引入了线程（thread）¹的概念，即与其他参与并发活动的线程“竞争”微控制器（MCU）的独立执行流。此外，它们提供了高级同步原语，既允许协调不同线程对物理资源的并发访问，又允许在等待较慢的异步事件时避免浪费 CPU 周期。

如今，RTOS 市场相当拥挤，程序员可以选择多种商业解决方案以及免费开源解决方案。此外，随着物联网（IoT）的日益普及，许多 RTOS 通过增加对多种连接解决方案和远程云平台的支持而不断演进。由于 Cortex-M 是众多芯片制造商之间的标准化架构，STM32 开发者可以根据其对复杂性的处理需求以及专用（可能是商业的）支持需求，从广泛的 RTOS 系统组合中进行选择。

传统上，ST Microelectronics 为最流行且免费开源的 RTOS 之一——FreeRTOS 提供了全面支持。FreeRTOS 已成为电子行业的一种标准，也被开源社区广泛采用。根据一些统计数据²，FreeRTOS 是目前市场上嵌入式系统中最广泛使用的 RTOS。最近的 CubeMX 版本为所有 STM32 微控制器提供了 FreeRTOS 10.x 的全面集成。开发者在 CubeMX 项目中设置 FreeRTOS 并在实际应用程序中使用它非常容易。FreeRTOS 于 2017 年被 Amazon 收购，现在是 AWS 生态系统的一部分。它现在在更宽松且“对商业友好”的 MIT 许可证下分发。

¹一些 RTOS，如 FreeRTOS，使用术语“任务”（task）来表示与其他任务竞争 CPU 的独立执行流。然而，本作者认为这种术语并不恰当。传统上，在通用操作系统中，多任务（multitasking）是一种方法，通过该方法，多个任务（也称为进程）共享公共硬件资源（主要是 CPU 和 RAM）。使用多任务操作系统（如 Linux），您可以同时运行多个应用程序。多任务是指操作系统快速切换每个计算任务的能力，从而给人一种不同应用程序正在同时执行多个操作的印象。进程有一个重要特征：得益于 CPU 内部内存管理单元（Memory Management Unit，MMU）提供的功能，其内存空间与其他进程在物理上是隔离的。多线程（multithreading）将多任务的概念扩展到单个进程中，因此您可以将单个应用程序内的特定操作细分为独立的线程。每个线程都可以并行运行。线程的重要特征是它们共享相同的内存地址空间。像 STM32 这样的真正嵌入式架构不提供 MMU（其中一些仅提供功能有限的内存保护单元 - MPU）。该单元的缺失不允许拥有分离的地址空间，因为不可能将物理地址映射到逻辑地址。这意味着它们只能运行单个应用程序，该应用程序最终可以拆分为共享相同内存地址空间的多个线程。因此，我们将在本书中讨论线程，尽管在讨论某些 FreeRTOS API 或泛指固件活动时，我们有时也会使用“任务”一词。 ²https://bit.ly/3maUQT0

<!-- page: 615 -->

近年来，FreeRTOS 的演进主要集中于 AWS IoT 服务的集成。

然而，ST 于 2020 年 12 月³宣布与 Microsoft 进行关键合作，Microsoft 最近收购了 ThreadX RTOS 背后的公司，并将其更名为 Azure RTOS。Microsoft 正在大力推动为嵌入式平台开发完整的物联网解决方案生态系统，而 Azure RTOS 是 Microsoft 提供方案的核心元素。这种合作是双向的：ST 将把 Azure RTOS 集成为 STM32Cube 扩展包，而 Microsoft 将推动将 STM32 微控制器⁴作为物联网应用的参考“平台”。ST 对 Azure RTOS 的支持不仅限于内核。集成将包括 FileX，这是一个在 NAND 和 NOR Flash 存储器上提供高级功能（如容错或磨损平衡）的文件系统；NetX 和 NetX Duo，它们是提供 TCP/IP、IPv4 和 IPv6 以及物联网中使用的许多上层协议（如 MQTT 或 COAP）的网络栈；以及 USBX，它简化了 USB 接口的使用，既可作为主机也可作为设备，并支持完整的 USB 类集合。

在撰写本章时（2022 年 1 月），ST 仅为 STM32H7 和 STM32F4 系列发布了 X-AZURE Cube 扩展包。根据本作者的观点，STM 需要一年多的时间才能完成对完整 STM32 产品组合的集成。此外，未来几年 RTOS 市场将如何演变仍不清楚。因此，本书将仅涵盖 FreeRTOS，并保留在未来书籍更新中涵盖 Azure RTOS 的可能性。

## 23.1 理解实时操作系统（RTOS）背后的概念

> **注意**
>
> 本段简要介绍了实时操作系统背后的主要概念。经验丰富的用户可以安全地跳过此部分。

除了中断服务程序（ISR）和异常处理程序外，迄今为止构建的所有示例都旨在使我们的应用程序仅由一个执行流组成。通常，从 main() 例程开始，一个庞大且无限的 while 循环执行固件任务：

```c
...
while(1) {
        doOperation1();
        doOperation2();
        ...
        doOperationN();
}
```

每个 doOperationX() 所花费的时间大致由开发者估算，开发者有责任避免其中一个函数占用过长时间，从而阻止固件的其他部分正确运行。此外，函数的调用顺序也调度了它们的执行，定义了固件执行的操作序列。这确实是一种协作式调度（cooperative scheduling）⁵，其中每个函数通过定期自愿释放控制权来配合下一个活动的执行。

³https://blog.st.com/azure-rtos/ ⁴https://azure.microsoft.com/it-it/blog/new-azure-rtos-collaborations-with-leaders-in-the-semiconductor-industry/

<!-- page: 616 -->

在这种早期的多道程序设计形式中，没有保证某个函数不会独占 CPU。应用程序设计者需要仔细确保每个函数都在尽可能短的时间内完成。在这种执行模型中，一个“无辜”的忙等待循环可能会产生灾难性的影响。让我们考虑以下伪代码：

```c
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

```c
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

```c
1   void blinkTask() {
2     uint32_t timeKeep = HAL_GetTick();
3     while (1) {
4       if(HAL_GetTick() - timeKeep > 500) {
5         HAL_GPIO_TooglePin(GPIOA, GPIO_PIN_5);
6         timeKeep = HAL_GetTick();
7       }
8       yield; /* Pass the control to another routine, e.g. the scheduler */
9     }
10  }
```

协程的工作方式是，当下次控制权传递到 blinkTask() 时，执行将从第 3 行恢复。我们不会深入探讨支持协程的语言中协程的具体实现细节。然而，这通常涉及为每个协程创建独立的堆栈，这些协程可以调用其他协程，而这些协程又可能将控制权传递给其他续体。

⁷局部变量和静态变量会产生相同的效果，但不会改变这一概念。⁸这涉及使用 C 语言的 setjmp() 和 longjmp() 函数。

<!-- page: 618 -->

抢占式多任务操作系统是物理资源的协调者，它允许执行多个计算任务⁹，每个任务拥有独立的堆栈，并为每个任务分配有限的量子时间（也称为时间片）。每个任务都有一个明确定义的时间窗口，在嵌入式系统中通常约为 1ms，在此期间它执行其活动，随后被抢占。实时操作系统内核使用调度策略来决定就绪任务的执行顺序：调度器是一种算法，用于表征操作系统规划任务执行的方式。

任务通过上下文切换操作在 CPU 上被“移入/移出”。上下文切换由操作系统执行，这得益于我们接下来将要探讨的硬件特性，该特性通过保存内部 CPU 寄存器（PC、MSP、R0..R15 等）对当前任务状态进行“快照”，然后再切换到另一个任务，该任务将能够再次“复用” CPU，运行相同的时间片（或者如果它“愿意”的话，甚至更短）。

<p align="center"><img src="../images/page-0618-image-01.png" alt="Image from PDF page 618"></p>

<p align="center">图 23.1：操作系统如何通过为任务分配固定的时间片来调度任务的执行</p>

图 23.1 展示了前文示例中任务抢占的工作方式。此处假设我们只有两个任务：一个用于 blinkTask() 例程，另一个用于 readUART2Task() 例程。操作系统开始调度 blinkTask() 任务，该任务可以“使用”CPU 1000 微秒（即 1ms）¹⁰。时间用尽后，操作系统调度 readUART2Task() 的执行，该任务现在可以占用相同的量子时间。该时间段结束后，CPU 将重新调度第一个任务，依此类推。

图 23.2 展示了操作系统通常组织 SRAM 内存的方式。每个任务由一个内存段表示，其中包含线程控制块（Thread Control Block，TCB）。TCB 不过是一个描述符，其中包含与任务执行相关的所有重要信息，这些信息是在任务被抢占前“一瞬间”¹¹ 捕获的（包括堆栈指针、程序计数器、CPU 寄存器以及其他少量内容），此外还包括堆栈本身，即当前在线程堆栈上调用的那些例程的堆栈帧。通过上下文切换操作在多个线程之间跳转，操作系统保证了相同的执行时间分配给所有线程，从而营造出固件活动并行执行的假象。

⁹仅在本段中，术语“任务”和“线程”将被不加区分地混用。¹⁰这些时间片数值仅供参考，因为时间片的确切持续时间受许多因素影响。其中，上下文切换带来的开销不可忽略。此外，此处假设所有任务具有相同的优先级，但这在嵌入式系统中通常并不成立。¹¹这完全不是事实，因为在任务被抢占之前，还会发生其他若干事情。然而，详细解释这些方面超出了本书的范围。如果对深入了解基于 Cortex-M 微控制器的上下文切换机制感兴趣，请参阅 Joseph Yiu 的著作。

<!-- page: 619 -->

<p align="center"><img src="../images/page-0619-image-01.png" alt="Image from PDF page 619"></p>

<p align="center">图 23.2：操作系统如何在多个任务中组织内存</p>

实时操作系统（RTOS）是一种能够提供多任务（或更准确地说，如注释 1 中所述的多线程）概念，同时确保在指定时间约束（通常称为截止时间）内做出响应的操作系统。实时响应通常被理解为在毫秒级，有时甚至达到微秒级。未指定为实时运行的系统通常无法保证在任何时间范围内做出响应，尽管可能会给出实际或预期的响应时间。通用操作系统（如 Linux、Windows 和 MacOS）不能成为实时操作系统（即使存在某些针对实时应用进行工程化改造的衍生版本——尤其是 Linux 的某些版本），原因很简单：分页和交换。前者允许将任务内存分割为名为页的小块，这些页可以分散在 RAM 中，并通过 MMU 进行别名映射，从而产生进程可以管理整个 4GB 地址空间的错觉（即使计算机并未提供那么多 SRAM）。后者允许将这些“未使用”的页换入/换出到外部（且速度较慢）的存储设备（通常是硬盘）上。这两个特性本质上是非确定性的，阻止操作系统在短且可计数的时间内处理请求。

RTOS 允许使用 blinkTask() 函数的第一个版本，以最小化在 UART 传输过程中使用忙等待循环¹²。然而，正如我们将在本章后面看到的，实时操作系统（RTOS）通常也提供了完全避免忙等待循环的工具：利用软件定时器，可以请求操作系统仅在指定的时间间隔过去后才重新调度 blinkTask()。此外，RTOS 还提供了主动释放控制权的方式，当我们知道等待由另一个任务执行的操作（或等待异步事件）完全没有必要时，就可以这样做。

<!-- page: 620 -->

我们刚才提到，RTOS 提供了一种将控制权主动释放给其他线程的方式。但如果某个任务不想释放控制权呢？例如，blinkTask() 例程的首次发布在最坏情况下可能会独占 CPU 超过 500ms，考虑到 1ms 的典型时间片长度，这是一段相当长的时间。那么，如何执行上下文切换呢？如果不丢失一项关键信息——程序计数器本身的值，就不可能“跳转”到其他程序指令（上下文切换本质上是一种跳转到另一条程序指令的操作）。

上下文切换需要硬件的大力支持。在第 7 章中，我们已经看到中断和异常是多道程序设计的来源。Cortex-M 内核处理这些事件的方式允许跳转到异常处理程序，而不会丢失当前的执行上下文。通过利用专用的硬件定时器（通常是 SysTick 定时器），RTOS 使用溢出事件产生的周期性中断来执行上下文切换。该定时器被配置为每 1ms 发生一次溢出（对于作为递减计数器的 SysTick 而言，则是下溢）。随后，RTOS 捕获该异常，将当前执行上下文保存到线程控制块（TCB）中，通过恢复下一个任务的执行上下文并退出定时器中断，将控制权传递给调度列表中的下一个任务。被抢占的线程对此毫不知情¹³。

¹²这并不意味着使用实时操作系统后，编写劣质代码就不会影响整体性能。这仅意味着，真正的抢占式调度器可以保证更高的多道程序度，确保所有线程拥有相同的 CPU 时间片。除非我们随意调整任务优先级，正如我们稍后所见。¹³然而，这可能并不完全对应实时操作系统的实际行为。这里的机制更为复杂，它与特定的硬件架构以及中断的优先级方式有关。在中断处理程序执行期间，另一个具有更高优先级的中断可能会挂起当前中断的执行，如第 7 章所述。但当这种情况发生时，CPU 无法通过执行任务切换直接切换到线程模式（即执行常规代码时的正常模式），除非先退出所有中断（这些中断运行在处理程序模式——一种由 Cortex-M 内核在异常处理期间提供的特殊模式）。这意味着，如果 SysTick 中断请求（IRQ）在另一个 IRQ 处于活动状态时发生，SysTick 异常处理程序无法执行上下文切换（即将控制权传递给另一个在线程模式下运行的任务），因为另一个正在处理程序模式下运行的代码已被抢占，需要完成其活动。通常，这通过将实际的上下文切换操作延迟到 PendSV 处理程序来解决，PendSV 是一个被配置为以最低优先级运行的异常。然而，这只是实现上下文切换的一种方式。如果对深入探讨此主题感兴趣，必须查阅您的实时操作系统的源代码或文档。

<!-- page: 621 -->

<p align="center"><img src="../images/page-0621-image-01.png" alt="Image from PDF page 621"></p>

<p align="center">图 23.3：上下文切换对任务调度的影响</p>

鉴于我们到目前为止所阐述的考量，图 23.1 需要更新为图 23.3 所示的内容，其中也考虑了操作系统在执行上下文切换时所花费的时间。上下文切换通常计算密集，操作系统的许多设计旨在优化上下文切换的使用。当开发人员决定更改 SysTick 定时器的下溢频率（通常是增加它）时，必须格外小心，因为这也会影响每个单独任务的时间片，进而影响每秒的上下文切换次数。

在我们开始使用实时操作系统进行实际操作之前，我们需要解释最后一个概念。如果任务想要自愿放弃控制权怎么办？在这种情况下，实时操作系统通常使用由 Cortex-M 处理器实现的 SVC（SuperVisor Call，超级用户调用）指令，该指令会导致调用 SVC_Handler 异常处理程序，或者强制引发 PendSV 异常。解释何时使用其中一种以及何时使用另一种超出了本书的范围，这也是操作系统厂商的设计选择。如需更多信息，如果对深入探讨这些主题感兴趣，请参阅 Joseph Yiu¹⁴ 的书籍。

这只是对实时操作系统背后复杂主题的初步介绍。我们将在本章稍后分析其他几个概念，主要涉及并发任务的同步。我们现在将开始查看 FreeRTOS 的最相关特性。

## 23.2 配置 FreeRTOS 和 CMSIS-RTOS v2 封装

如本章开头所述，FreeRTOS 是 ST 为其 Cube 发行版选定的官方实时操作系统。CubeMX 的最新版本对该操作系统提供了良好的支持，将其作为中间件组件包含在项目中非常容易。CubeHAL 的许多附加模块（如 LwIP 协议栈）都依赖于它提供的服务。

然而，ST 并未将其集成仅限于在 CubeHAL 发行版中提供 FreeRTOS。它在其之上构建了两个完整的 CMSIS-RTOS 封装，一个用于 CMSIS-RTOS v1，另一个用于 CMSIS-RTOS v2，允许开发符合 CMSIS-RTOS 标准的应用程序。我们在第 1 章中介绍整个技术栈时讨论过 CMSIS-RTOS。

¹⁴http://amzn.to/1P5sZwq

<!-- page: 622 -->

CMSIS 倡议背后的理念是，通过使用多个芯片制造商和软件供应商之间通用的标准化 API 集合，可以“轻松”地将我们的应用程序移植到其他厂商的不同微控制器上。因此，我们将尽可能使用 CMSIS-RTOS v2 API 来介绍 FreeRTOS 的功能。

### 23.2.1 FreeRTOS 源代码树

FreeRTOS 源代码组织在一个紧凑的源代码树中，分布在少数几个文件夹和文件中。图 23.4 显示了 FreeRTOS 在 CubeHAL 中的组织方式。根文件夹中找到的 .c 文件包含主要的操作系统特性（例如，tasks.c 文件包含所有与线程管理相关的例程）。子文件夹 include 包含多个头文件，用于定义操作系统使用的大部分 C 结构体和宏。其中最重要的是 FreeRTOSConfig.h¹⁵ 文件，它包含了所有用于根据用户需求配置实时操作系统的用户定义宏。根树中包含的另一个子文件夹是 portable。FreeRTOS 旨在运行在许多不同的硬件架构和编译器上，同时确保相同的 API 一致性。所有平台特定特性都组织在两个文件¹⁶中，port.c 和 portmacro.h，它们又收集在特定于给定架构的子文件夹中。例如，文件夹 portable/GCC/ARM_CM0 包含提供特定于 Cortex-M0/0+ 架构和 GCC 编译器的代码的 port.c 和 portmacro.h 文件。另一个重要的子文件夹是 MemMang。该文件夹包含 FreeRTOS 使用的 5 种不同的内存分配方案。正如我们稍后所见，FreeRTOS 允许用户选择最适合应用程序特定要求的最佳内存分配策略。最后，CMSIS-RTOS_V2 文件夹包含 ST 在 FreeRTOS 之上开发的符合 CMSIS-RTOS v2 标准的层。

<p align="center"><img src="../images/page-0622-image-01.jpeg" alt="Image from PDF page 622"></p>

<p align="center">图 23.4：CubeHAL 中 FreeRTOS 源代码树的组织</p>

¹⁵然而，FreeRTOS 源代码树中的该文件只是一个模板。CubeMX 用于配置 FreeRTOS 的实际文件是 Core/Inc/FreeRTOSConfig.h。 ¹⁶FreeRTOS 的这一部分被视为与核心 FreeRTOS 源代码树分离，并且据说实现了 FreeRTOS 的移植层。

<!-- page: 623 -->

#### 23.2.1.1 如何使用 CubeMX 配置 FreeRTOS

CubeMX 允许轻松地将 FreeRTOS 添加到现有项目中。一旦您在 CubeMX 中配置了 MCU 外设，就可以通过在“类别”窗格的“中间件”部分中选择所需的 CMSIS-RTOS 封装（V1 或 V2）来轻松启用 FreeRTOS 中间件，如图 23.5 所示。

<p align="center"><img src="../images/page-0623-image-01.jpeg" alt="Image from PDF page 623"></p>

<p align="center">图 23.5：如何在 CubeMX 中启用 FreeRTOS 中间件</p>

在配置部分，可以设置 FreeRTOS 的配置参数。我们将在本章中分析其中最重要的参数。一旦生成项目，CubeMX 会显示一条警告消息（见图 23.6）。让我们解释一下这两条消息的含义。

第一条消息提醒您使用不同于 SysTick 的定时器来生成 HAL 时基。CubeMX 提出这一要求是因为 FreeRTOS 被设计为自动将 SysTick 中断（IRQ）优先级设置为最低（即优先级编号最高）。这是 FreeRTOS 的架构要求，不幸的是，这与 HAL 的设计方式相冲突。

正如之前多次提到的，STM32Cube HAL 是围绕唯一的时基源构建的，通常就是 SysTick 定时器。SysTick_Handler() 中断服务例程（ISR）每 1ms 自动递增全局 tick 计数器。HAL 使用这个唯一的计数器来实现 HAL_Delay() 函数，该函数在许多 HAL 例程中被频繁使用。这些 HAL 例程反过来又可能被 HAL_<PPP>_IRQHandler() 函数调用，而这些函数是在 ISR 上下文中执行的（例如，HAL_TIM_IRQHandler() 是从定时器的 ISR 中调用的）。如果 SysTick 中断未配置为以最高优先级中断（在基于 Cortex-M 的处理器中为 0）运行，那么从 ISR 上下文中调用 HAL_Delay() 可能会导致死锁¹⁷，如果调用 HAL_Delay() 的 ISR 的优先级高于 SysTick 定时器的优先级（如果您使用 FreeRTOS，如前所述，这种情况总是成立的）。因此，最好使用另一个定时器作为 HAL 的时基。要更改 HAL 时基源，请遵循第 11 章中的说明。

¹⁷在并发编程中，死锁是一种情况，其中两个或更多并发执行流彼此等待对方完成，因此谁也无法完成。陷入死锁并非难事，所有程序员迟早都会遇到这种难以调试的事件。

<!-- page: 624 -->

另一条警告消息与在多线程应用程序中使用来自 newlib 库（标准 C 运行时库）或 newlib-nano 库（紧凑 C 运行时库）的某些函数有关。我们将在本章后面深入探讨这个话题。目前，请考虑如果您打算从多个线程（包括中断处理程序）中调用标准 C 例程，必须特别小心地处理这些调用。

<p align="center"><img src="../images/page-0624-image-01.jpeg" alt="Image from PDF page 624"></p>

<p align="center">图 23.6：关于 HAL 时基发生器和 newlib 重入性的警告消息</p>

## 23.3 线程管理

一旦我们配置好 Eclipse 项目，就可以开始使用 CMSIS-RTOS 层，进而使用 FreeRTOS 进行编码。

在所有实时操作系统（RTOS）的基础中都有线程的概念，我们在本章的第一段中已经分析过。线程无非是一个 C 函数，FreeRTOS 要求以以下方式定义它：

```c
void ThreadFunc(void const *argument) {
  while(1) {
    ...
  }
  osThreadTerminate(osThreadGetId());
}
```

函数 osThreadTerminate() 用于终止一个线程，它接受线程 ID（TID），我们稍后会看到。一个线程通常由一个包含线程指令的无限循环组成。将 osThreadTerminate() 放置在该循环之外通常是一种预防措施，以防控制流退出该循环，因为简单地从函数返回来终止线程是不正确的。向 osThreadTerminate() 函数传递 NULL 参数会导致该函数返回 osErrorParameter 错误，而不会正确删除线程。因此，确保通过传递正确的 TID 来调用 osThreadTerminate()。

要使用 CMSIS-RTOS v2 API（或简称为 CMSIS-RTOS2）启动一个新线程，我们使用以下函数：

```c
osThreadId_t osThreadNew (osThreadFunc_t func, void *argument, const osThreadAttr_t *attr);
```

osThreadAttr_t 是线程属性描述符，是一个以以下方式定义的 C 结构体：

<!-- page: 625 -->

```c
typedef struct {
  const char     *name;      /* Thread name */
  uint32_t       attr_bits;  /* Bitmask to configure the thread:  this is meaningless in FreeR\TOS */
  void           *cb_mem;    /* Control block to hold thread's data (default: NULL).
                                Used only for static allocation */
  uint32_t       cb_size;    /* Size of provided memory for control block (default: 0) */
  void           *stack_mem; /* Pointer to the memory holding the thread stack (default: NULL)\.
                                Used only for static allocation */
  uint32_t       stack_size; /* Size of provided memory for stack (default: 128 * 4) */
  osPriority_t   priority;   /* Initial thread priority (default: osPriorityNormal) */
  TZ_ModuleId_t  tz_module;  /* TrustZone module identifier (used in Cortex-M33 based MCUs) */
  uint32_t       reserved;   /* Reserved (must be 0) */
} osThreadAttr_t;
```

可以将 NULL 值作为 attr 参数传递给 osThreadNew()：在这种情况下，线程将以 Core/Inc/FreeRTOSConfig.h 文件中由宏 configMINIMAL_STACK_SIZE 指定的默认堆栈大小创建。现在是时候看一个实际示例了。

**文件名：** `Core/Src/main-ex1.c`

```c
21  #include "nucleo_hal_bsp.h"
22  #include "cmsis_os.h"
23
24  /* Private function prototypes -----------------------------------------------*/
25  void blinkThread(void *argument);
26
27  /* Definitions for blinkThread */
28  osThreadId_t blinkThreadID;
29  const osThreadAttr_t blinkThread_attr = {
30    .name = "blinkThread",
31    .stack_size = 128 * 4, /* In bytes */
32    .priority = (osPriority_t) osPriorityNormal,
33  };
34
35  int main(void) {
36    HAL_Init();
37
38    Nucleo_BSP_Init();
39
40    /* Init scheduler */
41    osKernelInitialize();
42
43    /* Creation of blinkThread */
44    blinkThreadID = osThreadNew(blinkThread, NULL, &blinkThread_attr);
45
46    /* Start scheduler */
47    osKernelStart();
48
49    /* We should never get here as control is now taken by the scheduler */
50    while (1);
51  }
52
53  void blinkThread(void *argument) {
54    while(1) {
55      HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
56      osDelay(500);
57    }
58  }
```

<!-- page: 626 -->

第 [29:33] 行定义了线程的属性，为其分配名称 “blinkThread”，指定堆栈大小为 512 字节，并分配正常优先级（稍后会有更多介绍）。

> **仔细阅读**
>
> CMSIS-RTOS API 以字节为单位表示线程堆栈大小，你可以在 ST 开发的位于 FreeRTOS 之上的 CMSIS-RTOS 层中找到此信息。然而，FreeRTOS 将堆栈大小定义为 StackType_t 类型的倍数，在 Cortex-M 处理器中，这对应于 uint32_t，即 4 字节。这意味着，传递给 osThreadNew() 宏的值必须是 4 字节的倍数。这就是为什么明确指定堆栈大小为 4 的倍数是方便的：osThreadNew() 内部会将传入的值除以 4，然后相应的 FreeRTOS API xTaskCreate() 又会将该值乘以 4。这是一个无用且略显繁琐的过程，充分说明了这些抽象层实际上的可移植性。

main() 例程通过调用 osKernelInitialize()¹⁸ 初始化主操作系统的调度器，而第 44 行的 osThreadNew() 有效地创建了新线程，并要求内核调度其执行，返回线程 ID (TID)：其他 API 使用此 ID 来操作线程状态及其配置。osThreadNew() 函数的第二个参数是一个可选参数，用于传递给线程（通过 *argument 指针）。最后，我们使用函数 osKernelStart() 启动内核调度器，除非发生错误，否则该函数永不返回。

blinkThread() 函数不过是无处不在的闪烁应用程序。唯一显著的区别是使用 osDelay() 函数代替经典的 HAL_Delay()：osDelay() 的设计使得线程在 500ms 内保持阻塞状态，而不影响 CPU 性能。在那段时间之后，线程将被恢复，LD2 LED 将再次切换。我们稍后会更多讨论 osDelay() 函数。

¹⁸为了完整性起见，此函数在此处没有做任何相关的事情，因为 FreeRTOS 中没有内核初始化过程，该过程在 vTaskStartScheduler() 例程中执行（由 CMSIS-RTOS2 osKernelStart() 例程封装）。

<!-- page: 627 -->

> **仔细阅读**
>
> 请注意，由于我们在这里使用 SysTick 作为 FreeRTOS 内核的时间基准，SysTick IRQ 的中断服务程序 (ISR) 直接定义在 Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/cmsis_os2.c 文件中，大约在第 159 行。要为 SysTick IRQ 设置自定义处理程序，必须将宏 USE_CUSTOM_SYSTICK_HANDLER_IMPLEMENTATION 设置为 1。相反，SysTick 定时器的配置由 FreeRTOS 本身通过函数 vPortSetupTimerInterrupt() 执行（位于相应的移植文件中——例如，portable/GCC/ARM_CM0/port.c），该函数在 osKernelStart() 例程启动调度器时被调用。在更改 MCU 内核频率时，这是一个必须考虑的关键点。

### 23.3.1 线程状态

在 FreeRTOS 中，线程可以具有两种主要执行状态：运行和未运行。在单核架构上，一次只能有一个线程处于运行状态。

在 FreeRTOS 中，未运行状态由几个子状态组成，如图 23.7 所示。未运行线程可以是就绪状态（这也是新线程的状态），即它已准备好被实时操作系统内核调度执行。

运行中的线程可以通过调用 osThreadSuspend() 函数自愿暂停其执行，该函数接受要暂停的线程的 TID。在这种情况下，线程进入挂起状态。要恢复挂起的线程，使用 osThreadResume()。

<p align="center"><img src="../images/page-0627-image-02.png" alt="Image from PDF page 627"></p>

<p align="center">图 23.7：FreeRTOS 中线程的可能状态</p>

<!-- page:628 -->

运行中的线程可以通过开始等待“外部”事件而进入阻塞状态。该事件可以是例如一个同步原语（例如，信号量），它将由另一个线程解锁。阻塞状态的另一个来源是 osDelay() 函数，该函数将线程置于阻塞状态，直到指定的延迟时间过去。阻塞线程可以被置于就绪状态，从而准备好被调度执行，或者被置于挂起状态。

为了避免任何误解，重要的是要澄清，挂起或阻塞的线程需要外部实体的干预才能返回就绪状态。

### 23.3.2 线程优先级与调度策略

在第一个示例中，我们看到每个线程都有一个优先级。但优先级对线程执行有什么实际影响呢？优先级会影响调度算法，使得当具有更高优先级的线程进入就绪状态时，可以改变执行顺序。优先级是实时操作系统的一个基本方面，并为实现短响应时间以满足截止时间提供了基础模块。需要强调的是，线程优先级与中断请求（IRQ）的优先级无关。

想象一下，你正在设计一台机器的控制板，该机器在关键情况下可能会造成工人受伤。通常，这类机器都有一个紧急停止按钮。该按钮可以连接到微控制器的一个引脚，相应的中断可能会恢复一个正在等待此事件的阻塞线程。该线程可能被设计为关闭引擎或类似操作，并将机器置于安全状态。

一旦中断触发，当时正在运行的任务在形式上仍在运行，但实际上并未在 CPU 上有效运行，因为 CPU 正在处理中断服务程序（ISR）。通过调用适当的操作系统例程（我们稍后会看到），操作系统将我们的紧急线程置于就绪模式，但我们必须确保它将是第一个被执行的线程。优先级允许程序员区分可延迟的活动和不可延迟的活动。

FreeRTOS 具有用户定义的优先级系统，在定义优先级方面提供了很大的灵活性。最低优先级（意味着具有此优先级的线程如果准备执行，总是会被更高优先级的线程超越）等于零。然后，用户可以给更重要的线程分配递增的优先级，直到由符号常量 `configMAX_PRIORITIES` 定义的最大值，该常量定义在 `Core/Inc/FreeRTOSConfig.h` 文件中。

表 23.1：CMSIS-RTOS2 规范中定义的固定优先级

优先级级别 | 值 | 描述
--- | --- | ---
osPriorityNone | 0 | 无优先级（未初始化）。
osPriorityIdle | 1 | 优先级：空闲 - 保留给空闲线程。
osPriorityLow | 8 | 优先级：低
osPriorityLow[1..7] | 8+[1..7] | 优先级：低 + 1..7
osPriorityBelowNormal | 16 | 优先级：低于正常
osPriorityBelowNormal[1..7] | 16+1 | 优先级：低于正常 + 1..7
osPriorityNormal | 24 | 优先级：正常
osPriorityNormal[1..7] | 24+1 | 优先级：正常 + 1..7

<!-- page: 629 -->

表 23.1：CMSIS-RTOS2 规范中定义的固定优先级

优先级级别 | 值 | 描述
--- | --- | ---
osPriorityAboveNormal | 32 | 优先级：高于正常
osPriorityAboveNormal[1..7] | 32+1 | 优先级：高于正常 + 1
osPriorityHigh | 40 | 优先级：高
osPriorityHigh[1..7] | 40+1 | 优先级：高 + 1
osPriorityRealtime | 48 | 优先级：实时
osPriorityRealtime[1..7] | 48+1 | 优先级：实时 + 1
osPriorityISR | 56 | 优先级：ISR - 保留给 ISR 延迟线程
osPriorityError | -1 | 系统无法确定优先级或优先级非法
osPriorityReserved | 0x7FFFFFFF | 防止枚举缩小编译器优化

相反，CMSIS-RTOS2 具有一个定义明确的优先级方案，由八个主要级别组成，并且对于每个主要级别，有七个细粒度子级别（见表 23.1），这些子级别映射到 FreeRTOS 的优先级。例如，`osPriorityLow` 级别的 FreeRTOS 优先级值等于 8，其子级别 `osPriorityLow3` 对应于 FreeRTOS 优先级值等于 8+3=11。函数

```c
osStatus_t osThreadSetPriority(osThreadId_t thread_id, osPriority_t priority);
```

允许更改现有线程的优先级，而函数

```c
osPriority_t osThreadGetPriority(osThreadId_t thread_id);
```

允许获取现有线程的优先级。

如果不了解实时操作系统采用的确切调度策略，谈论线程优先级是没有意义的。对于单核架构¹⁹，如大多数 STM32 微控制器，FreeRTOS 提供三种不同的调度算法，这些算法通过符号常量 `configUSE_PREEMPTION` 和 `configUSE_TIME_SLICING` 的正确组合来选择，这两个常量都定义在 `Core/Inc/FreeRTOSConfig.h` 文件中²⁰。表 23.2 显示了这两个宏的组合，以选择所需的调度算法。

表 23.2：如何在 FreeRTOS 中选择所需的调度策略

configUSE_PREEMPTION | configUSE_TIME_SLICING | 调度算法
--- | --- | ---
1 | 1 或未定义 | 带时间片轮转的优先级抢占式调度
1 | 0 | 不带时间片轮转的优先级抢占式调度
0 | 任意值 | 协作式调度

¹⁹FreeRTOS 为多核嵌入式架构提供了专用的调度策略，这些架构在近年来变得越来越流行。此主题将在未来章节中涵盖。 ²⁰默认情况下，`Core/Inc/FreeRTOSConfig.h` 文件不包含 `configUSE_TIME_SLICING` 宏的定义。FreeRTOS 会在 `Middlewares/Third_Party/FreeRTOS/Source/include/FreeRTOS.` 文件中自动定义并将其设置为 1。

<!-- page: 630 -->

让我们简要介绍这些算法。

- 带时间片轮转的优先级抢占式调度：这是所有实时操作系统实现的最常见算法，也是 CubeMX 选择的默认调度策略，其工作方式如下。每个线程都有一个固定优先级，该优先级在创建时分配。调度器永远不会更改此优先级，但程序员可以自由地通过调用 `osThreadSetPriority()` 函数重新分配不同的优先级。在此模式下，如果具有更高优先级的线程变为可执行状态，调度器将立即抢占正在运行的线程。被抢占意味着在没有显式让出或阻塞的情况下，非自愿地从运行状态移动到就绪状态，以便更高优先级的线程变为运行状态。时间片轮转（也称为量子时间）用于在具有相同优先级的线程之间共享 CPU 处理时间，即使它们通过显式让出或阻塞来释放控制权。当一个线程“消耗”完其时间片时，调度器将从调度列表中选择下一个运行线程（如果可用），并为其分配相同的时间片。如果没有可用的就绪线程，调度器会将一个名为“空闲”（idle）的特殊线程标记为运行状态，我们将在下文描述。时间片对应于实时操作系统的滴答时间，默认等于 1kHz，即 1ms。这可以通过配置宏 `configTICK_RATE_HZ` 并重新排列用作时基发生器的定时器的 UEV 频率来更改。调整此值取决于特定应用程序，也取决于微控制器运行的速度。微控制器运行得越慢，滴答频率应该越低。通常，从 100Hz 到 1000Hz 的值适用于许多应用程序。
- 不带时间片轮转的优先级抢占式调度：该算法与上一个算法几乎相同，除了这样一个事实：一旦线程进入运行状态，它只有在自愿的基础上（通过阻塞、停止或让出）或当更高优先级的线程进入就绪状态时才会离开 CPU。该算法极大地减少了上下文切换对整体性能的影响，因为切换次数大大减少。然而，设计不当的线程可能会独占 CPU，导致整个设备行为不可预测。
- 协作式调度：当使用此算法时，线程只有在自愿的基础上（通过阻塞、停止或让出）才会离开 CPU。即使更高优先级的线程变为就绪状态，操作系统也永远不会抢占当前线程，并在发生外部中断时再次重新调度它。这种调度形式将所有责任交给程序员，程序员必须仔细设计线程，就像设计不使用实时操作系统的固件一样。

即使我们使用的是带时间片轮转的优先级抢占式调度，在分配线程优先级时也必须格外小心。让我们考虑这个例子。

<!-- page: 631 -->

**文件名：** `Core/Src/main-ex2.c`

```c
21  #include "nucleo_hal_bsp.h"
22  #include "cmsis_os.h"
23  #include <string.h>
24
25  /* Private variables ---------------------------------------------------------*/
26  extern UART_HandleTypeDef huart2;
27
28  /* Private function prototypes -----------------------------------------------*/
29  void blinkThread(void *argument);
30  void UARTThread(void  *argument);
31
32  /* Definitions for blinkThread and UARTThread */
33  osThreadId_t blinkThreadID;
34  const osThreadAttr_t blinkThread_attr = {
35    .name = "blinkThread",
36    .stack_size = 128 * 4, /* In bytes */
37    .priority = (osPriority_t) osPriorityNormal,
38  };
39
40  osThreadId_t UARTThreadID;
41  const osThreadAttr_t UARTThread_attr = {
42    .name = "UARTThread",
43    .stack_size = 128 * 4, /* In bytes */
44    .priority = (osPriority_t) osPriorityAboveNormal,
45  };
46
47  int main(void) {
48    HAL_Init();
49
50    Nucleo_BSP_Init();
51
52    /* Init scheduler */
53    osKernelInitialize();
54
55    /* Creation of blinkThread */
56    blinkThreadID = osThreadNew(blinkThread, NULL, &blinkThread_attr);
57    /* Creation of UARTThread */
58    UARTThreadID = osThreadNew(UARTThread, NULL, &UARTThread_attr);
59
60    /* Start scheduler */
61    osKernelStart();
62
63    /* We should never get here as control is now taken by the scheduler */
64    while (1);
65  }
66
67  void blinkThread(void *argument) {
68    while(1) {
69      HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
70      osDelay(500);
71    }
72  }
73
74  void UARTThread(void *argument) {
75    while(1) {
76      HAL_UART_Transmit(&huart2, (uint8_t *)"UARTThread\r\n",
77                        strlen("UARTThread\r\n"), HAL_MAX_DELAY);
78    }
79  }
```

<!-- page: 632 -->

这次我们有两个线程，一个用于闪烁 LD2 LED，另一个用于持续在 UART2 上打印消息。UARTThread() 的创建优先级高于 blinkThread()。运行此示例时，你会发现 LD2 LED 永远不会闪烁。这是因为 UARTThread() 被设计为持续执行某些操作，当它的执行时间片耗尽时，它仍处于就绪状态，并且由于具有更高的优先级，它会被重新调度执行。这清楚地证明，必须谨慎使用优先级，以防止其他进程发生饥饿²¹。

### 23.3.3 主动释放控制权

如果程序员知道消耗 CPU 周期是无用的，正在运行的线程可以释放控制权（这被称为让出控制权，即 yield），方法是调用函数

```c
osStatus_t osThreadYield(void);
```

这将导致一次上下文切换，调度列表中的下一个就绪线程将被置于运行状态。如果调度策略是协作式调度，osThreadYield() 起着重要作用。

### 23.3.4 空闲线程

除非我们进入 STM32 微控制器提供的低功耗模式之一，否则 CPU 永远不会停止。这意味着，如果系统中的所有线程都因等待外部事件而处于阻塞或挂起状态，那么我们需要一种在等待其他线程再次激活期间“做点什么”的方法。因此，所有操作系统都提供一个名为“空闲”（idle）的特殊任务，它在系统非活动状态下被调度，其优先级被定义为尽可能低。因此，通常说最低优先级对应于空闲优先级。

²¹在并发编程中，当线程被永久拒绝处理其工作所需的资源时，就会发生饥饿。饥饿通常是由线程之间糟糕的同步引起的，但也可能由错误的优先级分配方案引起。饥饿是一种不受欢迎的状态，没有任何程序员希望达到这种状态，而且有时识别其根源可能是一场噩梦。

<!-- page: 633 -->

在 FreeRTOS 9 之前的版本中，每当一个线程被删除时，FreeRTOS 为该线程分配的内存由空闲线程释放。在 FreeRTOS 10 中，如果一个线程删除另一个线程，则 FreeRTOS 为被删除线程分配的内存会立即释放。然而，如果一个线程删除自身，则 FreeRTOS 为该线程分配的内存由空闲线程释放。请注意，在所有情况下，只有 RTOS 为该线程分配的堆栈和线程控制块（TCB）会被自动释放。线程分配的任何动态缓冲区都需要由线程本身妥善管理。

空闲线程在低功耗设计中还起着重要作用，我们将在本章后面发现这一点。

> **关于并发编程的忠告**
>
> 实时操作系统的设计者向你展示的惊人数字会让你感到惊讶。他们会告诉你，他们的操作系统能够每秒 fork 数十万个线程，并展示惊人的上下文切换性能。
>
> 要知道，从实际角度来看，这和酒吧里的闲聊没有什么两样。
>
> <p align="center"><img src="../images/page-0633-image-02.jpeg" alt="Image from PDF page 633"></p>
>
> <p align="center">图 23.8：当线程数量增加得过多时通常会发生的情况</p>
>
> 过去，我审阅过读者发给我的一些项目（但有时我也见过由专业人士制作的项目，它们有着同样糟糕的方法——不管你信不信），在这些项目中，你可以看到代码中到处生成几十个线程，但它们并没有做相关的事情。有时你还会发现一些线程，它们所做的仅仅是经过比较后 fork 另一个线程。
>
> 并发编程的理论家会告诉你，你拥有的并发流越多，你遇到的问题可能越多。管理线程可能很困难，而且同步它们所涉及的成本往往超过了使用它们的优势。此外，生成新线程这一操作本身也有不可忽视的成本。上下文切换也是如此。
>
> 多线程编程必须始终谨慎处理，尤其是在嵌入式系统中，因为 SRAM 通常有限。记住：保持简单。

<!-- page: 634 -->

## 23.4 内存分配与管理

在前两个示例中，我们开始使用 FreeRTOS，但没有过多处理线程以及操作系统使用的其他结构的内存分配问题。唯一的例外是 `osThreadAttr_t.stack_size` 属性，它被 `osThreadNew()` 例程用于为线程的堆栈分配内存。然而，FreeRTOS 不仅需要足够的内存来分配线程，还使用额外的 SRAM 部分来分配其内部结构（如 TCB 列表等）。这同样适用于我们稍后将学习的其他同步原语，例如信号量和互斥锁。这些内存具体是从哪里获取的？

传统上，直到 8.x 版本，FreeRTOS 都实现了动态分配模型。这构成了一个重要的限制，因为在某些应用领域，动态内存分配是被强烈不推荐甚至明确禁止的。尽管正如我们很快会看到的，FreeRTOS 实现的五种动态分配器之一能够满足这些应用领域中关于内存分配的大部分需求，但不幸的是，这一 FreeRTOS 特性在存在此限制时阻碍了其使用。从最新的 9.x 版本开始，FreeRTOS 实现了两种内存分配模型：完全静态模型和动态模型。

使用两个宏来启用内存分配模型：`configSUPPORT_STATIC_ALLOCATION` 和 `configSUPPORT_DYNAMIC_ALLOCATION`。两者都可以取值为 0 或 1，以禁用/启用相应的内存模型。重要的是要强调，这两种内存模型并非互斥：根据用户需求，可以同时使用两者。正如我们稍后将看到的，这两种内存模型强制要求使用分离的 API。

### 23.4.1 动态内存分配模型

FreeRTOS 实现了一种动态内存分配模型，该模型使用 SRAM 区域来分配所有操作系统内部结构，包括 TCB。与静态分配模型相比，动态模型具有一些不可忽视的优势：

- 内存分配自动发生，位于 RTOS API 函数内部。
- 开发人员无需担心自行分配内存。
- 如果对象被删除，RTOS 对象使用的 RAM 可以被重用，从而潜在地减少应用程序的最大 RAM 占用。
- 提供了 RTOS API 函数以返回堆使用情况的信息，允许优化堆的大小。
- FreeRTOS 提供了五种动态内存分配方案，可以根据应用程序需求选择最合适的方案。
- 创建对象时需要更少的函数参数。

FreeRTOS 不使用 C 运行时库提供的经典 `malloc()` 和 `free()` 函数²²，原因如下：

²²有一个显著的例外，即 `heap_3.c` 分配器，我们很快就会看到。

<!-- page: 635 -->

1. 它们占用大量的代码空间，增加了固件的大小；
2. 它们不是线程安全的（稍后会有更多介绍）；
3. 它们不是确定性的（执行函数所需的时间在每次调用时会有所不同）。

因此，FreeRTOS 提供了自己的动态分配方案来处理其所需的内存，但由于实现方式有多种，每种方式都有其优点和权衡，FreeRTOS 的设计使得这部分与核心操作系统的其余部分抽象分离，并提供了五种不同的分配方案供用户根据具体需求选择。`pvPortMalloc()` 和 `vPortFree()` 是在每种方案中实现的最重要的函数，它们的名称清楚地说明了它们的功能。

这五种方案不属于 FreeRTOS 核心，而是属于移植层，它们实现在五个 C 源文件中，命名为 `heap_1.c` 到 `heap_5.c`，位于 `portable/MemMang` 文件夹内。通过编译其中一个文件并与 FreeRTOS 代码的其余部分一起编译，我们就自动为应用程序选择了该分配方案。此外，我们最终可以通过实现此 API 层（在最坏情况下，我们基本上需要实现 5 个函数）来提供自己的分配模型，以满足我们的具体需求。CubeMX 允许通过选择相应的设置轻松选择所需的内存方案，如图 23.9 所示。

<p align="center"><img src="../images/page-0635-image-01.jpeg" alt="Image from PDF page 635"></p>

<p align="center">图 23.9：CubeMX 如何允许选择所需的 FreeRTOS 内存方案</p>

#### 23.4.1.1 heap_1.c
许多嵌入式应用程序使用 RTOS 将固件逻辑划分为块。每个块都有自己的功能，并且通常独立于其他块运行。例如，假设您正在开发一个带有 TFT 显示屏的设备（可能是现代洗衣机的控制器）。通常，固件被划分为少数几个线程，其中一个负责图形交互（通过打印信息和显示精美的图形小部件来更新显示屏），其他线程负责管理洗涤程序（因此涉及传感器、电机、泵等的处理）。这些应用程序通常有一个 `main()` 来生成线程（正如我们在过去的示例中所做的那样），一旦操作系统开始运行，几乎不再初始化其他内容。

<!-- page: 636 -->

这意味着内存分配器不需要考虑任何更复杂的分配问题，如确定性和碎片化，因此可以简化。

`heap_1.c` 分配器实现了 `pvPortMalloc()` 的一个非常基本的版本，并且不提供 `vPortFree()`。从不删除线程或其他内核对象（如队列、信号量等）的应用程序适合使用此内存分配方案。在动态分配内存的使用受到不鼓励的应用领域中，可能会受益于这种分配方案，因为它提供了确定性的内存管理方法，避免了碎片化（因为内存永远不会被释放）。

`heap_1.c` 分配器将静态分配的数组细分为小块，随着 `pvPortMalloc()` 的调用进行分配。这确实是 FreeRTOS 的堆。该数组的总大小（以字节为单位）由 `FreeRTOSConfig.h` 文件中的宏 `configTOTAL_HEAP_SIZE` 定义。这种分配方案唯一的权衡是，由于整个数组在编译时分配，即使应用程序没有完全使用它，也会消耗大量的 SRAM。这意味着程序员必须仔细选择 `configTOTAL_HEAP_SIZE` 大小的正确值。

> **注意**
>
> 必须强调一件重要的事情。C 程序的内存传统上分为两个重要区域：堆栈和堆。堆被描述为在运行时动态增长，并且其增长方向与堆栈相反。然而，如您所见，`heap_1.c` 分配器与整个应用程序的堆没有任何关系，因为它使用一个声明为 `static` 的未初始化数组来存储其动态需要的对象，该数组如我们在第 13 章所学的那样，被分配在 `.bss` 段中。这确实是一种动态分配形式，但与 `malloc()` 和 `free()` 函数的使用无关。这意味着我们可以安全地在应用程序中使用它们，即使它们的使用在嵌入式应用程序中并不被鼓励。

#### 23.4.1.2 heap_2.c
`heap_2.c` 也通过细分静态分配的数组来工作，该数组由 `configTOTAL_HEAP_SIZE` 宏定义尺寸。它使用最佳适配算法来分配内存，并且与 `heap_1.c` 分配方案不同，它允许释放内存。该算法被认为已弃用，不适合新设计。`heap_4.c` 是此分配器的更好替代方案。因此，我们将不会详细介绍其工作原理。如果有兴趣，您可以查阅官方 FreeRTOS 文档²³。

#### 23.4.1.3 heap_3.c
heap_3.c 使用标准的 C malloc() 和 free() 函数来执行内存分配。这意味着 configTOTAL_HEAP_SIZE 参数对内存管理没有影响，因为 malloc() 被设计为自行管理堆。这意味着我们需要相应地配置链接器脚本，如第 13 章所示。此外，请注意 malloc()的实现与 newlib-nano 和常规 newlib 提供的实现不同。然而，newlib 库提供的更通用的实现需要更多的闪存空间。

²³https://bit.ly/1PMSPRM

<!-- page: 637 -->

heap_3.c 通过暂时挂起 FreeRTOS 调度器使 malloc() 和 free() 线程安全。我们将在本章后面深入探讨 malloc() 与 FreeRTOS 结合使用的情况。

#### 23.4.1.4 heap_4.c
heap_4.c 是 CubeMX 默认选择的分配器，其工作方式与 heap_1.c 和 heap_2.c 相同。也就是说，它使用一个静态分配的数组，其大小由 configTOTAL_HEAP_SIZE 宏的值决定，用于存储运行时分配的对象。然而，它在内存分配期间采用了不同的方法。事实上，它使用首次适应算法（first fit algorithm），将相邻的空闲块合并为一个大的块，从而降低内存碎片化的风险。这种技术通常用于具有动态和自动内存分配的语言中的垃圾回收器，也称为合并（coalescing）。

不幸的是，heap_4.c 分配器的这种行为导致其具有非确定性：许多小对象的分配/释放，加上线程的创建/销毁，可能会导致大量的碎片，这需要更多的计算处理来整理内存。此外，没有保证该算法能完全避免内存泄漏。然而，它通常比 malloc() 和 free() 的最标准实现更快，特别是 newlib-nano 库提供的实现。

详细解释 heap_4.c 算法超出了本书的范围。更多信息请参阅 FreeRTOS 文档²⁴。

#### 23.4.1.5 heap_5.c
heap_5.c 使用与 heap_4.c 分配器相同的算法，但它允许将内存池分割到不同的非连续内存区域。这对于提供 FSMC 控制器的 STM32 微控制器特别有用，该控制器允许透明地使用外部 SDRAM 来增加整个 RAM。程序员可以决定将一些重度使用的线程分配在内部 SRAM 内存中（如果可用，也可以是 CCM 内存），然后使用外部 SDRAM 来存储不太重要的对象，如信号量和互斥锁。

通过定义自定义链接器脚本，可以在两个内存区域中分配两个池，然后使用 FreeRTOS 的 vPortDefineHeapRegions() 函数将它们定义为内存池。然而，这是操作系统的进阶用法，我们不会在这里详细讨论。如果有兴趣，可以参考 FreeRTOS 的创建者 Richard Barry 所著的优秀书籍《Mastering the FreeRTOS Real Time Kernel》²⁵。

²⁴https://bit.ly/1TqxX9S ²⁵https://bit.ly/3A1avK9

<!-- page: 638 -->

#### 23.4.1.6 FreeRTOS 堆定义

从 FreeRTOS 9.x 开始，除了控制堆的大小外，还可以控制堆的定义。通过将 configAPPLICATION_ALLOCATED_HEAP 宏设置为 1，我们可以声明 FreeRTOS 堆，并决定将其放置在特定的内存区域（例如，像 CCM 这样的更快内存中），使用自定义链接器脚本。当将 configAPPLICATION_ALLOCATED_HEAP 配置为 1 时，我们必须提供一个具有确切名称和维度的 uint8_t 数组，如下所示。

```c
uint8_t ucHeap[ configTOTAL_HEAP_SIZE ];
```

### 23.4.2 静态内存分配模型

从 FreeRTOS 9.x 开始，可以启用完全静态的内存分配模型。这意味着我们完全负责正确分配操作系统执行其活动所需的内存池。静态分配的 RAM 为开发人员提供了一些重要优势：

- 操作系统结构可以放置在特定的内存位置。对于那些具有 CCM 内存或其他缓存 SRAM 内存的 STM32 微控制器来说，这是一个重要的优势。
- 最大 RAM 占用可以在链接时确定，而不是在运行时确定。
- 开发人员不需要担心内存分配失败的优雅处理。
- 它允许在根本不允许任何动态内存分配的应用程序中使用操作系统（尽管 FreeRTOS 包含可以克服大多数反对意见的分配方案，我们稍后会看到）。

通过设置 configSUPPORT_STATIC_ALLOCATION 宏为 1 来启用静态内存分配模型，它影响所有用于定义 FreeRTOS 对象的 API。configSUPPORT_DYNAMIC_ALLOCATION 和 configSUPPORT_STATIC_ALLOCATION 宏都可以设置为 1，允许混合动态和静态分配。当使用静态分配时，我们必须通过预分配来向 FreeRTOS 提供存储堆栈和 TCB 对象的内存区域。这可以通过相应地设置 osThreadAttr_t 结构体来完成：

<!-- page: 639 -->

```c
...
uint32_t threadStack[128];
StaticTask_t threadTCB;
const osThreadAttr_t thread_attr = {
  .name = "Thread",
  .priority = (osPriority_t) osPriorityNormal,
  .stack_size = 128 * 4, /* In bytes */
  .stack_mem = threadStack,
  .cb_mem = &threadTCB,
  .cb_size = sizeof(StaticTask_t)
};
```

> **仔细阅读**
>
> 请注意，FreeRTOS 允许选择性地静态和动态分配线程的 TCB 和堆栈。例如，完全可以将堆栈静态分配，并让 FreeRTOS 动态分配 TCB。相反，ST 当前实现的 osThreadNew() 要求堆栈和 TCB 必须同时静态分配（因此通过 osThreadAttr_t 结构体传递它们的引用），否则线程将被自动动态分配。这是一个在决定线程分配时必须考虑的限制。

#### 23.4.2.1 静态内存分配模型下的空闲线程分配

在使用动态分配时，FreeRTOS 完全负责空闲线程的内存分配（包括其堆栈和 TCB）。相反，当使用静态分配时，我们需要像处理其他任何线程一样，负责为空闲线程进行正确的内存分配。

由于空闲线程是由内核在初始化期间自动分配的，FreeRTOS 提供了一种通用的方法来为空闲线程提供必要的内存空间。该函数为：

```c
void vApplicationGetIdleTaskMemory(StaticTask_t **ppxIdleTaskTCBBuffer, StackType_t **ppxIdleT\askStackBuffer, uint32_t *pulIdleTaskStackSize);
```

该函数由 FreeRTOS 在启动空闲线程之前调用。必须使用该例程来分配空闲 TCB 和堆栈，并将这些内存区域的引用传递给内核。当使用 CubeMX 生成包含 FreeRTOS 的项目，并选择静态内存分配模型时，文件 Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/cmsis_os2.c 中已经包含了 vApplicationGetIdleTaskMemory() 函数的实现（请查看文件末尾）。

### 23.4.3 FreeRTOS 与 C 标准库

作为程序员，我们习惯于将某些事情视为理所当然。由于开发环境复杂度的日益增加，这一说法正变得越来越真实。

<!-- page: 640 -->

但是，作为嵌入式开发人员，我们必须确保使用诸如 sprintf() 甚至看似“无害”的 dtoa() 等函数，不会伤害正在操作危险机器的工人，或导致现代波音 737 的自动驾驶系统停滞。

因此，在使用 FreeRTOS（或任何其他并发系统——包括简单的 ISR）与 C 标准库配合之前，我们必须采取一些预防措施。

#### 23.4.3.1 如何配置 newlib 以处理与 FreeRTOS 的并发

newlib 及其精简（紧凑）版本 newlib-nano，是 STM 在其基于 GCC 的开发环境中采用的 C 运行时库。重要的是要澄清，newlib 并非唯一的选择，但由于 STM 仅提供 newlib 作为唯一替代方案，我们将只关注它。

每次我们在多线程环境中使用库（或任何给定的代码片段）时，我们必须问自己该库是否是可重入的。可重入性是函数的一个特性，它允许多个执行流使用同一函数，并保证存储在这些执行上下文中的值在调用之间保持不变。让我们考虑这个简单的例子：

```c
1   #define ENOERR     0
2   #define EDIVBYZERO 1
3   int errno;
4
5   int divide(int x, int y) {
6     if(y!=0){
7           errno = ENOERR;
8           return x/y;
9     }else{
10          errno = EDIVBYZERO;
11          return 0;
12      }
13  }
14
15  void funcA(void *argument) {
16      int x, y, ret;
17      //Long manipulation of x and y
18      //Here, both x and y are !=0
19      ret = divide(x,y);
20      ...
21  }
22
23  void funcB(void *argument) {
24      int x, y, ret;
25      //Long manipulation of x and y
26      //Here, y is == 0
27      ret = divide(x, 0);
28      if(errno == ENOERR && ret == 0) {
29          /* In a multithreaded environment this is possible */
30           ...
31  }
32  ....
```

<!-- page: 641 -->

现在，让我们分析 divide() 函数的存储，参考图 23.10 中的图表。该函数使用了三个内存位置：两个变量将存储在函数的堆栈上（x 和 y），而 errno 将存储在 .bss 段中（如果这个话题对您来说很新，请回到第 20 章）。假设 divide() 函数由两个在不同线程中运行且具有相同优先级的不同例程调用。由于每个线程都有自己的 TCB，因此也有自己的堆栈，对局部变量的访问不是问题。相反，对全局变量 errno 的访问会受到竞争条件的影响。运行 funcB() 的线程可能刚好在第 11 行的 return 指令之前被抢占，控制权可能传递给运行 funcA() 的线程，该线程会将 errno 变量设置为 ENOERR：在这种情况下，当控制权再次回到 funcB() 时，结果将是 0，调用者（即 funcB()）将假设除法结果为零（我们在这里处于整数空间）。

<p align="center"><img src="../images/page-0641-image-01.jpeg" alt="Image from PDF page 641"></p>

<p align="center">图 23.10：多线程环境中 divide() 函数的内存布局</p>

这里引用 errno 变量并非偶然。不幸的是，即使大多数 newlib 函数被设计为可重入，仍然存在一定数量的 C 标准库函数——至少在理论上——完全不可重入。这主要发生在全局 errno 变量上，但也发生在其他全局或静态分配的变量上。

为了解决这个问题，newlib 被设计为将所有全局定义的变量打包到一个名为 struct _reent 的结构体中。该结构体包含一个相关的字段列表²⁶（包括 errno，甚至包括指向 stdin/stdout/stderr 等指针等意想不到的字段），并且整个应用程序有一个该 struct _reent 的全局实例。对于所有不可重入函数²⁷，都有一个对应的包装函数（以 _ 开头并以 _r 结尾——例如，_dtoa_r() 用于包装 dtoa()），这些函数被设计为通过一个名为 “_impure_ptr” 的全局指针来访问这个全局分配的 _reent 结构体（只是好奇这个名字的来源……）。FreeRTOS 会在每次上下文切换时更改 _impure_ptr 的引用，更新指向 TCB 内部 _reent 结构体实例的引用（见图 23.11）。显然，这将导致 TCB 尺寸大幅增加：大约 100 字节，具体取决于编译选项（如果使用 newlib 或 newlib-nano，此大小会有很大变化）。

<!-- page: 642 -->

通过在全局 FreeRTOS 宏 configUSE_NEWLIB_REENTRANT 中将其设置为 1（位于 Core/Inc/FreeRTOSConfig.h 文件中），FreeRTOS 将在每个 TCB 中分配一个 struct _reent，以便 _impure_ptr 指向当前 TCB 堆栈内的一个“全局内存区域”。这将保证 newlib 的可重入性：然而，请记住，可重入性并不等同于“线程安全”。正如我们将在下一段中看到的那样。

<p align="center"><img src="../images/page-0642-image-01.jpeg" alt="Image from PDF page 642"></p>

<p align="center">图 23.11：FreeRTOS 如何处理各个线程对 _reent 结构体的访问</p>

²⁶您可以在此处查看 _reent 结构体。 ²⁷不可重入函数的完整列表在此处可用。

<!-- page: 643 -->

#### 23.4.3.2 如何在 FreeRTOS 中使用 malloc() 及依赖 malloc() 的 newlib 函数

如前所述，除了 heap_3.c 分配方案外，FreeRTOS 并不使用 stdlib C 堆内存来分配线程和其他对象。但是，如果我们项目中要使用的某个库使用了 malloc() 和 free()，我们该怎么办？

这个问题不能轻易忽视，需要对整个固件进行仔细检查。原因很简单：同一个 newlib 库中有一些函数使用 malloc() 来动态分配内存。例如，printf() 和 sprintf() 是两个根据需求动态分配缓冲区的 stdlib 函数。但它们并非唯一。Dave Nadler 曾广泛撰写²⁸ 关于此主题的文章，尽管根据该作者的说法，他混淆了两个独立的方面（重入性和内存分配策略），导致读者很容易迷失方向。此外，关于 STM 对 _sbrk() 例程实现的信息已不再更新，因为 STM 修正了最大堆栈边界的计算方式。

为了轻松理解如何处理此主题，我们需要回到第 20 章，当时我们讨论了使用 STM32CubeIDE 工具链构建的 STM32 应用的内存布局。图 23.12 展示了运行 FreeRTOS 的 STM32 应用的开箱即用²⁹ SRAM 内存布局。让我们从 SRAM 起始地址（ORIGIN）开始（这一点你应该很熟悉，但多了解一些总比不了解好）。

<p align="center"><img src="../images/page-0643-image-01.jpeg" alt="Image from PDF page 643"></p>

<p align="center">图 23.12：运行 FreeRTOS 的 STM32CubeIDE 应用的开箱即用 SRAM 内存布局</p>

- _sdata 是指向 SRAM 起始地址（即 0x2000 0000）的链接器符号，而 _edata 对应于已初始化数据段的末尾。

²⁸https://nadler.com/embedded/newlibAndFreeRTOS.html ²⁹“开箱即用”（out-of-the-box）一词指的是由 STM32CubeIDE 1.8.0 中的 CubeMX 生成的标准应用的内存布局。如果你使用的是更新版本的 IDE，情况可能会发生变化。因此，在将此段落中的信息视为绝对真理之前，请先进行检查。

<!-- page: 644 -->

- _sbss 指向未初始化数据的起始位置，而 _ebss（或链接器符号 _end）指向该区域的末尾，如果使用 heap_4.c 方案，该区域还包含 FreeRTOS 堆。如果使用 Core/Src/sysmem.c 中的 _sbrk() 实现，_ebss 对应于 C 堆区域的开始。
- _Min_Heap_Size 是堆区域的“逻辑”限制。此限制由程序员设定（默认情况下，CubeMX 将其设置为 0x200），并且应仔细检查以避免破坏堆栈区域，因为堆栈区域是向相反方向增长的。
- _Min_Stack_Size 是堆栈区域的逻辑限制。同样，此限制由程序员设定（默认情况下，CubeMX 将其设置为 0x400）。
- 当前堆栈指针（Current Stack Pointer）是 Cortex-M 内核寄存器 sp 的内容，它对应于当前主堆栈指针。
- _estack 默认表示 SRAM 内存的末尾，它是包含 MSP 的堆栈的第一个位置。

为了在我们的应用中安全地使用 malloc()/free() 例程，我们有以下选项。

**选项 1：完全不使用它们**

这听起来可能很极端，但这是一个值得考虑的选项。如果你的代码以及所有依赖的库都不使用 malloc()/free()，那么忽略它们是可以的。然而，永远不要信任他人的代码：你必须在运行时仔细检查，而不仅仅是查看代码或文档。你可以通过相应地指示链接器轻松执行测试。LD 允许使用命令行选项 -Xlinker --wrap 来“包装”一个例程（可以通过项目属性设置，如图 23.13 所示）。Dave Nadler 提供了一个³⁰ 优秀的包装器实现，用于跟踪 malloc() 的使用情况，如下所示。你可以设置断点来查看包装器是否被调用，或者检查 MallocCallCnt 变量的值（如果 MCU 支持 ITM，你可以通过 ITM 打印它）。

```c
size_t TotalMallocdBytes;
int MallocCallCnt;
static bool inside_malloc;
void *__wrap_malloc(size_t nbytes) {
    extern void * __real_malloc(size_t nbytes);
    MallocCallCnt++;
    TotalMallocdBytes += nbytes;
    inside_malloc = true;
    void *p = __real_malloc(nbytes); // will call malloc_r...
    inside_malloc = false;
    return p;
};
void *__wrap__malloc_r(void *reent, size_t nbytes) {
    (void)(reent);
    extern void * __real__malloc_r(size_t nbytes);
```

³⁰https://nadler.com/embedded/newlibAndFreeRTOS.html

<!-- page: 645 -->

```c
    if(!inside_malloc) {
      MallocCallCnt++;
      TotalMallocdBytes += nbytes;
    };
    void *p = __real__malloc_r(nbytes);
    return p;
};
```

**优点：**

- 简化的内存布局。
- 降低内存溢出的风险。
- 降低内存碎片的产生风险（特别是如果使用 newlib-nano）。

**缺点：**

- 可能会迫使你重新发明轮子，实现 newlib 和其他库提供的现有功能。
- 你可能被迫研究他人的代码。

<p align="center"><img src="../images/page-0645-image-01.jpeg" alt="Image from PDF page 645"></p>

<p align="center">图 23.13：</p>

**选项 2：让 FreeRTOS 处理动态内存分配**

这是另一个极端的解决方案，但如果你知道自己在做什么，它可能效果很好。malloc() 和 free() 都可以轻松重写，以便它们使用 FreeRTOS 分配例程：

<!-- page: 646 -->

```c
void *malloc (size_t size) {
    return pvPortMalloc(size);
}
void free (void *ptr) {
    vPortFree(ptr);
}
```

这之所以有效，是因为在 newlib 中这两个函数都被声明为 __weak。使用此选项时，重要的是要确定 _Min_Stack_Size 和全局 FreeRTOS 堆 ucHeap 的尺寸，以便不浪费任何 SRAM 空间（为了澄清，图 23.12 中名为 _sbrk() 的区域应尽可能缩小）。我强烈建议将 ucHeap 放在紧跟在 .bss 段之后的专用段中。

**优点：**

- 简化的内存布局。
- 自由选择最佳 FreeRTOS 动态分配器。

**缺点：**

- 你可能被迫研究他人的代码。

**选项 3：让 newlib 处理动态内存分配**

这个解决方案与上一个完全相反，也是 Dave Nadler 提出的解决方案。Dave 提供了一个新的内存分配器³¹，它是 FreeRTOS 提供的标准 heap_3.c 的高级版本。文件 heap_useNewlib_ST.c 包含大量代码，对于新手用户来说可能会感到困惑。该文件执行以下操作：

- 首先，它正确定义了堆栈和堆的边界，以便最佳地利用分配给 _sbrk() 的区域。
- 其次，它实现了一个适当的错误管理方案，以防我们用完空闲内存。
- 最后（这也是最相关的一点），它正确处理了对 malloc()/free() 例程的并发访问。

³¹https://bit.ly/3nIOtqC

<!-- page: 647 -->

**文件名：** `Middlewares/Third_Party/FreeRTOS/Source/portable/MemMang/heap_useNewlib_ST.c`

```c
1   extern char end, _estack, _Min_Stack_Size;  // symbols from linker LD command file
2
3   #ifdef MALLOCS_INSIDE_ISRs
4       // If we plan to use malloc() in a ISR context - not that good practice
5       #define DRN_ENTER_CRITICAL_SECTION(_usis) { _usis = taskENTER_CRITICAL_FROM_ISR(); }
6       #define DRN_EXIT_CRITICAL_SECTION(_usis)  { taskEXIT_CRITICAL_FROM_ISR(_usis);     }
7   #else
8       #define DRN_ENTER_CRITICAL_SECTION(_usis) vTaskSuspendAll();
9       #define DRN_EXIT_CRITICAL_SECTION(_usis)  xTaskResumeAll();
10  #endif
11
12  //! _sbrk_r version supporting reentrant newlib
13  void * _sbrk_r(struct _reent *pReent, int incr) {
14      #ifdef MALLOCS_INSIDE_ISRs //block interrupts during free-storage use
15        UBaseType_t usis; //saved interrupt status
16      #endif
17      static char *currentHeapEnd = &end;
18      if (currentHeapEnd + incr > &_Min_Stack_Size) {
19          // Ooops, no more memory available...
20              vApplicationMallocFailedHook();
21              pReent->_errno = ENOMEM; // newlib's thread-specific errno
22          return (char *)-1; // the malloc-family routine that called sbrk will return 0
23      }
24      // 'incr' of memory is available: update accounting and return it.
25      char *previousHeapEnd = currentHeapEnd;
26      currentHeapEnd += incr;
27      heapBytesRemaining -= incr;
28      return (char *) previousHeapEnd;
29  }
30
31  //! non-reentrant sbrk uses is actually reentrant by using current context
32  // ... because the current _reent structure is pointed to by global _impure_ptr
33  char * sbrk(int incr) { return _sbrk_r(_impure_ptr, incr); }
34  //! _sbrk is a synonym for sbrk.
35  char * _sbrk(int incr) { return sbrk(incr); };
36
37  #ifdef MALLOCS_INSIDE_ISRs // block interrupts during free-storage use
38    static UBaseType_t malLock_uxSavedInterruptStatus;
39  #endif
40  void __malloc_lock(struct _reent *r)   {
41    (void)(r);
42    #if defined(MALLOCS_INSIDE_ISRs)
43      DRN_ENTER_CRITICAL_SECTION(malLock_uxSavedInterruptStatus);
44    #else
45      bool insideAnISR = xPortIsInsideInterrupt();
46      configASSERT( !insideAnISR ); // Make damn sure no more mallocs inside ISRs!!
47      vTaskSuspendAll();
48    #endif
49  };
50  void __malloc_unlock(struct _reent *r) {
51    (void)(r);
52    #if defined(MALLOCS_INSIDE_ISRs)
53      DRN_EXIT_CRITICAL_SECTION(malLock_uxSavedInterruptStatus);
54    #else
55      (void)xTaskResumeAll();
56    #endif
57  };
58
59  // newlib also requires implementing locks for the application's environment memory space,
60  // accessed by newlib's setenv() and getenv() functions.
61  // As these are trivial functions, momentarily suspend task switching (rather than semaphore).
62  // Not required (and trimmed by linker) in applications not using environment variables.
63  // ToDo: Move __env_lock/unlock to a separate newlib helper file.
64  void __env_lock()    {       vTaskSuspendAll(); };
65  void __env_unlock()  { (void)xTaskResumeAll();  };
66
67  // ======================================================================
68  // Implement FreeRTOS's memory API using newlib-provided malloc family.
69  // ======================================================================
70
71  void *pvPortMalloc( size_t xSize ) PRIVILEGED_FUNCTION {
72      void *p = malloc(xSize);
73      return p;
74  }
75  void vPortFree( void *pv ) PRIVILEGED_FUNCTION {
76      free(pv);
77  };
```

<!-- page: 648 -->

第 [3:10] 行定义了两个宏，用于暂停/恢复上下文切换，以避免在堆中分配新内存时出现任何竞态条件。这里我们有两种执行此操作的方法。如果我们不打算在中断服务程序（ISR）上下文中使用 malloc()（这通常应该是正确的方式），那么使用 FreeRTOS 的 vTaskSuspendAll()/xTaskResumeAll() 例程是可以的。否则，我们必须使用宏 taskENTER_CRITICAL_FROM_ISR()/taskEXIT_CRITICAL_FROM_ISR()³²。第 [13:29] 行定义了 _sbrk_r()：正如你所见，它与 STM 在工具链中提供的当前 _sbrk() 实现没有区别。最后，第 [40:57] 行定义了 __malloc_lock()/__malloc_unlock() 例程：这些钩子函数由 newlib 库自动调用，以避免内存分配期间的竞态条件。

³² Dave 提供了在中断服务程序（ISR）上下文中使用 malloc() 的可能性，因为一些 ST 库（特别是 USB 设备栈）在 ISR 中调用的代码中使用了 malloc()。发生这种情况的原因是，正如我们将在专门介绍 USB 外设的章节中看到的那样，大多数 USB 操作都是由栈在 ISR 上下文中处理的。

<!-- page: 649 -->

**优点：**

- 简化的内存布局。
- 如果使用 FreeRTOS 进行静态内存分配，这是唯一可用的选项（但如果是这样，为什么要处理 malloc() 呢？）

**缺点：**

- 如果你的代码在固件生命周期中创建和销毁许多任务，那么最好让 FreeRTOS 来处理内存分配。

**选项 4：混合使用 newlib 和 FreeRTOS 来处理动态内存分配**

这是 CubeMX 的“默认”解决方案，需要进行调整以避免问题。FreeRTOS 的内存空间将由全局宏 configTOTAL_HEAP_SIZE 定义，而 newlib 的 malloc() 将在 _Min_Stack_Size 和 _ebss 之间的空闲空间中分配动态内存。STM 的 _sbrk() 实现与 Dave Nadler 提供的实现没有太大区别，我们不需要更改它。相反，我们需要通过提供 __malloc_lock()/__malloc_unlock() 钩子来确保 malloc() 例程的线程安全。以下是 _sbrk() 例程的一个可能且更完整的实现。

> **仔细阅读**
>
> 基于 Cortex-M0/0+ 的微控制器（MCU）所有者会发现 `__malloc_lock()` 例程的不同实现。函数 `xPortIsInsideInterrupt()` 未在 Cortex-M0/0+ 端口中定义。在这种情况下，使用函数 `__get_IPSR()` 来检测我们是否正在中断服务例程（ISR）的上下文中运行。

**文件名：** `Core/Src/sysmem.c`

```c
30  #ifdef MALLOCS_INSIDE_ISRs
31      // If we plan to use malloc() in a ISR context - not that good practice
32      UBaseType_t usis; //saved interrupt status
33      #define DRN_ENTER_CRITICAL_SECTION(_usis) { _usis = taskENTER_CRITICAL_FROM_ISR(); }
34      #define DRN_EXIT_CRITICAL_SECTION(_usis)  { taskEXIT_CRITICAL_FROM_ISR(_usis);     }
35  #else
36      #define DRN_ENTER_CRITICAL_SECTION(_usis) vTaskSuspendAll();
37      #define DRN_EXIT_CRITICAL_SECTION(_usis)  xTaskResumeAll();
38  #endif
39
40  /**
41   * Pointer to the current high watermark of the heap usage
42   */
43  void * _sbrk_r(struct _reent *pReent, int incr) {
44    extern uint8_t _end; /* Symbol defined in the linker script */
45    extern uint8_t _estack; /* Symbol defined in the linker script */
46    extern uint32_t _Min_Stack_Size; /* Symbol defined in the linker script */
47    const uint32_t stack_limit = (uint32_t)&_estack - (uint32_t)&_Min_Stack_Size;
48    const uint8_t *max_heap = (uint8_t *)stack_limit;
49    static uint8_t *__sbrk_heap_end = NULL;
50
51    uint8_t *prev_heap_end;
52
53    /* Initialize heap end at first call */
54    if (NULL == __sbrk_heap_end) {
55      __sbrk_heap_end = &_end;
56    }
57
58    /* Protect heap from growing into the reserved MSP stack */
59    if (__sbrk_heap_end + incr > max_heap) {
60      errno = ENOMEM;
61      return (void *)-1;
62    }
63
64    prev_heap_end = __sbrk_heap_end;
65    __sbrk_heap_end += incr;
66
67    return (void *)prev_heap_end;
68  }
69
70  char * sbrk(int incr) {
71    return _sbrk_r(_impure_ptr, incr);
72  }
73
74  #ifdef MALLOCS_INSIDE_ISRs // block interrupts during free-storage use
75    static UBaseType_t malLock_uxSavedInterruptStatus;
76  #endif
77  void __malloc_lock(struct _reent *r)   {
78    (void)(r);
79    #if defined(MALLOCS_INSIDE_ISRs)
80      DRN_ENTER_CRITICAL_SECTION(malLock_uxSavedInterruptStatus);
81    #else
82      BaseType_t insideAnISR = xPortIsInsideInterrupt();
83      configASSERT( !insideAnISR ); // Make sure no malloc() inside ISRs
84      vTaskSuspendAll();
85    #endif
86  };
87
88  void __malloc_unlock(struct _reent *r) {
89    (void)(r);
90    #if defined(MALLOCS_INSIDE_ISRs)
91      DRN_EXIT_CRITICAL_SECTION(malLock_uxSavedInterruptStatus);
92    #else
93      (void)xTaskResumeAll();
94    #endif
95  };
```

<!-- page: 650 -->

<!-- page: 651 -->

**优点：**

- 每个组件各司其职。
- 您不必过于担心在其他库中使用 `malloc()` 的问题。

**缺点：**

- 您需要仔细定义内存区域的大小。

#### 23.4.3.3 STM32CubeMX 对线程安全的处理方法

从 STM32CubeIDE 1.7 和 STM32CubeMX 6.3 开始，ST 解决了常规 newlib C 函数的线程安全访问处理问题。在 CubeMX 的项目管理器部分，可以通过选择五种不同的锁定策略之一来启用多线程支持，如图 23.14 所示。这些策略分为通用策略和依赖实时操作系统（RTOS）的策略。

- 通用策略：

  - 策略 #1：用户定义处理线程安全的解决方案。
  - 策略 #2：允许从中断中使用锁。此实现通过例如在调用 `malloc()` 期间禁用所有中断来确保线程安全。
  - 策略 #3：拒绝从中断中使用锁。此实现假设单线程执行，并拒绝任何尝试从中断服务例程（ISR）上下文中获取锁的行为。
- 基于 FreeRTOS 的策略：

  - 策略 #4：允许从中断中使用锁。使用 FreeRTOS 锁实现。此实现通过例如在调用 `malloc()` 期间进入 RTOS 支持的中断临界区来确保线程安全。这意味着通过禁用低优先级中断和任务切换来实现线程安全。然而，高优先级中断并不安全。
  - 策略 #5：拒绝从中断中使用锁。使用 FreeRTOS 锁实现。此实现通过例如在调用 `malloc()` 期间挂起所有任务来确保线程安全。

有关完整技术解决方案的更多信息，请参阅 AN5731³³。

³³https://bit.ly/3B4GGJi

<!-- page: 652 -->

<p align="center"><img src="../images/page-0652-image-01.jpeg" alt="Image from PDF page 652"></p>

<p align="center">图 23.14：如何在 CubeMX 中选择线程安全锁定策略</p>

### 23.4.4 内存池

CMSIS-RTOS2 规范提供了内存池的概念，ST 在 FreeRTOS 操作系统之上开发的层实现了它们，即使 FreeRTOS 本身并不原生提供这种数据结构。内存池是由固定大小的块（块的大小可以任意指定）构成的动态分配内存，其实现方式是线程安全的。这使得它们可以从线程和中断服务例程（ISR）中同样访问。ST 使用 `pvPortMalloc()`/`vPortFree()` 例程实现内存池，因此实际的内存分配请求由 `heap_x.c` 分配器之一处理。相反，使用计数信号量来规范对池中内存块的访问。我们稍后将会讨论计数信号量。这意味着只有当 `Core/Inc/FreeRTOSConfig.h` 文件中的宏 `configUSE_COUNTING_SEMAPHORES` 被定义并设置为 1 时，内存池才可用。

使用以下函数创建并初始化内存池：

```c
osMemoryPoolId_t osMemoryPoolNew(uint32_t block_count,
                                 uint32_t block_size, const osMemoryPoolAttr_t *attr);
```

其中 `block_count` 定义块的数量，`block_size` 是池中每个块的维度（以字节为单位）。内存池由以下结构体定义：

<!-- page: 653 -->

```c
typedef struct {
  const char    *name;      /* Memory pool name */
  uint32_t      attr_bits;  /* Attribute bits: reserved for future use (set to '0') */
  void          *cb_mem;    /* Control block to hold MP's data (default: NULL).
                               Used only for static allocation */
  uint32_t      cb_size;    /* Size of provided memory for control block (default: 0) */
  void          *mp_mem;    /* Pointer to the memory holding all MP's blocks  (default: NULL).
                               Used only for static allocation */
  uint32_t      mp_size;    /* Size of provided memory for blocks storage */
} osMemoryPoolAttr_t;
```

函数 `osMemoryPoolNew()` 的 `attr` 参数可以设置为 NULL。CMSIS-RTOS2 规范定义了函数：

```c
void *osMemoryPoolAlloc(osMemoryPoolId_t mp_id, uint32_t timeout);
```

用于从池中检索单个内存块，其大小等于传递给 `osMemoryPoolNew()` 的 `block_size` 参数。如果池中不再有空闲空间，该函数返回 0。参数 `timeout` 指定系统等待分配内存的时间。根据 CMSIS-RTOS2 规范，在系统等待期间，调用此函数的线程被置于阻塞状态。一旦至少有一个内存块可用，该线程将变为就绪状态。参数 `timeout` 可以具有以下值：

- 当 `timeout` 为 0 时，函数立即返回（无论块是否可用）；
- 当 `timeout` 设置为 `osWaitForever` 时，函数将无限期等待，直到内存被分配；
- 所有其他值指定以内核滴答为单位的超时时间（例如，等于 100 的值对应于 100 个滴答，默认情况下对应于 100ms）。

然而，当前的 ST 实现仅处理 `timeout` 参数等于 0 的情况。在所有其他情况下，函数 `osMemoryPoolAlloc()` 将返回 NULL。

要释放池中的一个块，我们使用函数：

```c
osStatus_t osMemoryPoolFree(osMemoryPoolId_t mp_id, void *block);
```

通过调用以下函数来销毁池并释放其所有内存：

```c
osStatus_t osMemoryPoolDelete        (osMemoryPoolId_t mp_id);
```

CMSIS-RTOS2 规范还定义了几个实用函数，用于检索有关池状态的相关信息。例如，函数：

<!-- page: 654 -->

```c
uint32_t osMemoryPoolGetSpace(osMemoryPoolId_t mp_id);
```

该函数返回池中空闲块的数量。有关处理内存池的完整函数列表，请参阅官方 CMSIS-RTOS2 规范³⁴。

以下伪代码展示了如何轻松使用内存池。

```c
1   #include "cmsis_os2.h"                          // CMSIS RTOS header file
2
3   #define MEMPOOL_OBJECTS 16                      // Number of Memory Pool Objects
4
5   typedef struct {                                // Object data type
6     uint8_t Buf[32];
7     uint8_t Idx;
8   } MEM_BLOCK_t;
9
10  osMemoryPoolId_t mpid_MemPool;                  // Memory pool id
11  osThreadId_t tid_Thread_MemPool;                // Thread id
12
13  void Thread_MemPool (void *argument);           // Thread function
14
15  int Init_MemPool (void) {
16    mpid_MemPool = osMemoryPoolNew(MEMPOOL_OBJECTS, sizeof(MEM_BLOCK_t), NULL);
17    if (mpid_MemPool == NULL) {
18      ; // MemPool object not created, handle failure
19    }
20
21    tid_Thread_MemPool = osThreadNew(Thread_MemPool, NULL, NULL);
22    if (tid_Thread_MemPool == NULL) {
23      return(-1);
24    }
25    return(0);
26  }
27
28  void Thread_MemPool (void *argument) {
29    MEM_BLOCK_t *pMem;
30    osStatus_t status;
31
32    while (1) {
33      pMem = (MEM_BLOCK_t *)osMemoryPoolAlloc(mpid_MemPool, 0U);  // Get Mem Block
34      if (pMem != NULL) {                                         // Mem Block was available
35        pMem->Buf[0] = 0x55U;                                     // Do some work...
36        pMem->Idx    = 0U;
37
38        status = osMemoryPoolFree(mpid_MemPool, pMem);            // Free mem block
39      }
```

³⁴https://bit.ly/3tND6Se

<!-- page: 655 -->

```c
40      osThreadYield();                                            // Suspend thread
41    }
42  }
```

在第 16 行创建了一个新池，使其包含 16 个元素，每个元素的大小等于 sizeof(MEM_BLOCK_t)。然后，线程 Thread_MemPool 访问该池：在第 33 行从池中检索一个块并进行操作。

### 23.4.5 堆栈溢出检测

在讨论 FreeRTOS 提供的用于检测堆栈溢出的功能之前，我们应该花点时间谈谈如何计算线程所需的正确内存量。

不幸的是，很难给出一个确定的答案，因为这取决于相当长的一系列需要考虑的因素。首先，堆栈大小受调用堆栈深度的影响，即由我们的线程调用的函数数量以及每个函数占用的空间决定。这个空间基本上由局部变量和传递的参数组成。另一个相关因素是处理器架构、使用的编译器以及选择的优化级别。

通常，线程的堆栈大小是通过实验计算的，并且 FreeRTOS 提供了一种尝试检测堆栈溢出的方法。请仔细阅读我的措辞：尝试检测。因为堆栈溢出检测是调试中最困难的方面之一，也是程序代码静态分析中最困难的方面之一。

FreeRTOS 提供了两种检测堆栈溢出的方法。第一种是使用以下函数：

```c
UBaseType_t uxTaskGetStackHighWaterMark( TaskHandle_t xTask );
```

该函数返回线程堆栈中“未使用”的字（word）的数量。例如，假设定义了一个堆栈为 100 个字（即在 STM32 上为 400 字节）的线程。假设在最坏情况下，该线程使用了其堆栈的 90 个字。那么 uxTaskGetStackHighWaterMark() 将返回值 10。

参数 xTask 的 TaskHandle_t 类型只不过是 osThreadCreate() 函数返回的 osThreadId，如果我们从同一线程调用 uxTaskGetStackHighWaterMark()，则可以传递 NULL。

仅当满足以下条件之一时，此函数才可用：

- configCHECK_FOR_STACK_OVERFLOW 宏被定义为大于 0 的值，或者
- configUSE_TRACE_FACILITY 被定义为大于 0 的值，或者
- INCLUDE_uxTaskGetStackHighWaterMark 被定义为大于 1 的值。

显然，它们都必须在 FreeRTOSConfig.h 文件中定义。

<!-- page: 656 -->

> **注意**
>
> <p align="center"><img src="../images/page-0656-image-01.png" alt="Image from PDF page 656"></p>
>
> <p align="center">图 23.15：FreeRTOS 如何使用固定值 (0xA5) 填充堆栈以检测堆栈溢出</p>
>
> uxTaskGetStackHighWaterMark() 如何知道使用了多少堆栈？该函数并没有执行任何魔法操作。当定义了上述宏之一时，FreeRTOS 会用一个“魔法”数字（由 task.c 文件中的宏 tskSTACK_FILL_BYTE 定义）填充线程的堆栈，如图 23.15 所示。这是一个“水位线”，用于推导空闲内存位置的数量（即截至线程堆栈末尾、仍保存着该填充值的内存单元数量）。这是用于检测缓冲区溢出的最有效技术之一。

uxTaskGetStackHighWaterMark() 函数也可用于验证线程堆栈的实际使用情况，从而在浪费过多空间时减小其大小。

FreeRTOS 提供了两种额外的方法来在运行时检测堆栈溢出。这两种方法都涉及在 FreeRTOSConfig.h 文件中设置 configCHECK_FOR_STACK_OVERFLOW 宏。如果我们将其设置为 1，那么每次线程运行结束时，FreeRTOS 都会检查当前堆栈指针的值：如果它高于线程堆栈的顶部，则很可能发生了堆栈溢出。在这种情况下，回调函数：

```c
void vApplicationStackOverflowHook(xTaskHandle *pxTask, signed portCHAR *pcTaskName);
```

将被自动调用。通过在我们的应用程序中定义此函数，我们可以检测堆栈溢出并进行调试。例如，在调试会话期间，我们可以在其中放置一个软件断点：

```c
void vApplicationStackOverflowHook(xTaskHandle *pxTask, signed portCHAR *pcTaskName) {
        asm("BKPT #0"); /* If a stack overflow is detected then, the debugger stop
                           the firmware execution here */
}
```

这种方法很快，但它可能会漏掉在上下文切换过程中发生的堆栈溢出。因此，通过将宏 configCHECK_FOR_STACK_OVERFLOW 配置为 2，FreeRTOS 将应用与 uxTaskGetStackHighWaterMark() 函数相同的方法，即用水位线值填充堆栈，并在堆栈的最后 20 个字节与其预期值不同时调用 vApplicationStackOverflowHook。由于 FreeRTOS 在每次上下文切换时都执行此检查，因此此模式会影响整体性能，并且应仅在固件开发期间使用（特别是对于高滴答频率）。

<!-- page: 657 -->

## 23.5 同步原语

在多线程应用程序中，线程迟早需要一种方式来同步自身，无论是在访问共享资源时，还是在多个执行流之间传输数据时。关于并发编程的文献中充满了最适合作为同步原语的算法和数据结构。CMSIS-RTOS2 API 以及底层的 FreeRTOS 操作系统定义了所有操作系统和线程库通用的这些原语。本段简要介绍了其中最相关的几个。

### 23.5.1 消息队列

队列³⁵（见图 23.16）是一种先进先出（FIFO）集合，在 FreeRTOS 中通过线性数据结构实现，其中最先添加的元素将最先被移除。当元素被添加到队列中时，称为入队（enqueue）；当它被移除时，称为出队（dequeue）。

<p align="center"><img src="../images/page-0657-image-01.jpeg" alt="Image from PDF page 657"></p>

<p align="center">图 23.16：</p>

队列在并发编程中广泛使用，特别是在需要在对事件具有不同响应时间的多个线程之间交换数据时。例如，我们通常有两个线程，一个作为生产者，一个作为消费者，共享一个公共缓冲区。生产者的工作是生成数据片段，将其放入缓冲区并继续生成。同时，消费者的工作是从缓冲区中一次移除一个片段。问题在于确保当缓冲区已满时，生产者不会尝试向其中添加数据，并且当缓冲区为空时，消费者不会尝试从中移除数据。在实时操作系统（RTOS）中，队列的设计使得如果线程尝试向已满的队列添加数据，它可以被置于阻塞模式，直到至少有一个元素从队列中移除。同时，如果队列中没有可用数据，操作系统内核会将消费者置于阻塞模式）。由于由操作系统处理，队列的设计确保了不同线程之间不会发生竞态条件（除非程序员在代码中引入了明显的错误）。

使用以下函数创建并初始化队列：

³⁵CMSIS-RTOS2 使用术语“消息队列”来表示通常仅称为队列的对象。正如我们稍后所见，这也影响了 API（所有结构和函数都有 osMessage 前缀）。然而，在本章的其余部分，我们将简单地称它们为队列。

<!-- page: 658 -->

```c
osMessageQueueId_t osMessageQueueNew(uint32_t msg_count, uint32_t msg_size,
                                     const osMessageQueueAttr_t *attr);
```

其中 msg_count 是队列中的项目数量，msg_size 是单个项目的大小。结构体 osMessageQueueAttr_t 类似于之前看到的结构体 osMemoryPoolAttr_t，这里不再详细阐述。

要将新元素入队，我们使用函数

```c
osStatus_t osMessageQueuePut(osMessageQueueId_t mq_id, const void *msg_ptr,
                             uint8_t msg_prio, uint32_t timeout);
```

其中 mq_id 是函数 osMessageQueueNew 返回的队列 ID，msg_ptr 是指向要入队数据的指针，msg_prio 用于根据给定优先级对队列中的消息进行排序（这被 ST 开发的 CMSIS-RTOS2 层完全忽略），timeout 指示如果队列已满我们愿意等待的滴答数：如果在超时时间到期之前仍未腾出足够的空间，则 osMessageQueuePut() 函数返回 osErrorTimeout³⁶ 值。传入 osWaitForever 将导致 osMessagePut() 无限期等待。

要从队列中出队数据，我们使用函数

```c
osStatus_t osMessageQueueGet(osMessageQueueId_t mq_id, void *msg_ptr,
                             uint8_t *msg_prio, uint32_t timeout);
```

队列需要使用以下函数显式删除：

```c
osStatus_t osMessageQueueDelete(osMessageQueueId_t mq_id);
```

相反，可以使用以下函数将其内容重置为初始状态（空状态）：

```c
osStatus_t osMessageQueueReset(osMessageQueueId_t mq_id);
```

> **注意**
>
> 请注意，FreeRTOS 提供了两个独立的 API 来从线程或从 ISR 中操作队列。例如，xQueueReceive() 函数用于从线程中出队元素，而 xQueueReceiveFromISR() 用于从 ISR 中安全地出队元素。ST 开发的 CMSIS-RTOS2 层旨在抽象这一方面，并自动检查我们是从线程还是从 ISR 执行调用。通常，这是以牺牲速度为代价的。

以下示例展示了如何使用队列在两个线程之间交换数据，一个作为生产者（UARTThread()），另一个作为消费者（blinkThread()），如果指定了较大的超时时间，后者可能会运行得较慢。

³⁶osMessageQueuePut() 和 osMessageQueueGet() 可以根据是从线程还是 ISR 调用而返回其他状态代码。有关更多信息，请参阅官方 CMSIS-RTOS2 规范 (https://bit.ly/3tND6Se)。

<!-- page: 659 -->

**文件名：** `Core/Src/main-ex3.c`

```c
51  osMessageQueueId_t msgQueueID;
52
53  int main(void) {
54    HAL_Init();
55
56    Nucleo_BSP_Init();
57    RetargetInit(&huart2);
58
59    /* Init scheduler */
60    osKernelInitialize();
61
62    /* Creation of msgQueue */
63    msgQueueID = osMessageQueueNew(5, sizeof(uint16_t), NULL);
64    /* Creation of blinkThread */
65    blinkThreadID = osThreadNew(blinkThread, NULL, &blinkThread_attr);
66    /* Creation of UARTThread */
67    UARTThreadID = osThreadNew(UARTThread, NULL, &UARTThread_attr);
68
69    /* Start scheduler */
70    osKernelStart();
71
72    /* We should never get here as control is now taken by the scheduler */
73    while (1);
74  }
75
76  void blinkThread(void *argument) {
77    uint16_t delay = 500; /* Default delay */
78    uint16_t msg = 0;
79    osStatus_t status;
80
81    while(1) {
82      status = osMessageQueueGet(msgQueueID, &msg, 0, 10);
83      if(status == osOK)
84        delay = msg;
85
86      HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
87      osDelay(delay);
88    }
89  }
90
91  void UARTThread(void *argument) {
92    uint16_t delay = 0;
93
94    while(1) {
95      printf("Specify the LD2 LED blink period: ");
96      fflush(stdout);
97      scanf("%hu", &delay);
98      printf("\r\nSpecified period: %hu\n\r", delay);
99      osMessageQueuePut(msgQueueID, &delay, 0, osWaitForever);
100   }
101 }
```

<!-- page: 660 -->

UARTThread，定义在第 [91:101] 行，使用了第 5 章中看到的 I/O 重定向技术，允许我们使用 C 标准库中的经典 printf()/scanf() 例程。该线程从 UART 读取一个 uint16_t 值并将其放入队列 msgQueueID 中。blinkThread()，定义在第 [76:89] 行，从队列中获取这些值，并将它们用作 osDelay() 函数的延迟值。这个简单的应用程序允许我们从终端模拟器传递所需的 LD2 LED 闪烁频率。

如果您指定一个较大的延迟值，您可以轻松看到当生产者线程运行得比消费者线程快时，队列是如何被使用的。通过传递一个等于 10000 的延迟，我们可以立即将另一个等于 50 的延迟值放入队列中（因为队列有足够的空间存储另一个值）。如您所见，我们需要大约 10 秒 LED 才开始以 20Hz 的频率闪烁，因为 blinkThread() 被 osDelay() 函数阻塞。

### 23.5.2 信号量

在并发编程中，信号量（Semaphore）是一种用于控制多个执行流对共享资源访问的数据类型。信号量的一种基本形式由一个布尔变量表示：该变量的状态被用作条件，以控制对资源的访问。例如，如果该变量等于 False，则线程进入阻塞状态，直到该变量再次变为 True。当某个线程获取信号量时，我们说该信号量被该线程“获取”（taken），即第一个发现信号量等于 True 的线程。这实际上是一个二进制信号量（binary semaphore），因为它只能取两个状态，并且在 FreeRTOS 中实现为仅包含一个元素的队列。如果队列为空，则第一个尝试获取它的线程会在队列中放入一个“标志”值，并继续执行；其他线程将无法添加其他“标志”，直到获取了信号量的线程将其标志出队。

<p align="center"><img src="../images/page-0660-image-01.jpeg" alt="Image from PDF page 660"></p>

<p align="center">图 23.17：</p>

<!-- page: 661 -->

信号量的一种更通用的形式是计数信号量（counting semaphore）（见图 23.17），它允许多于一个线程获取它。正如二进制信号量被实现为长度为一的队列一样，计数信号量可以被视为长度大于一的队列。计数信号量通常有一个初始值，每当一个线程获取它时，该值就会递减。虽然二进制信号量通常用于规范对单个资源的并发访问，但计数信号量可用于：

- 规范对共享资源池的访问：在这种情况下，计数值表示可用资源的数量。例如，STM 使用一个最大可用令牌数（最大计数器值）等于 block_count 的计数信号量来管理对内存池的访问。
- 统计重复发生事件的次数：在这种情况下，一个执行流（为简单起见，假设它是一个 ISR）会释放一个信号量（导致其计数器增加），以向另一个线程发出信号，表明某个给定事件已经发生（例如，来自 UART 的数据已准备好处理）；然后该线程可以获取信号量并开始执行其活动；如果发生另一个“事件”（新数据到达），则 ISR 会通过释放信号量再次增加信号量；这样，处理线程就可以再次获取信号量并执行其活动。

然而，简单的变量不能用作信号量，因为没有保证“获取”信号量的操作是以原子方式执行的。因此，为了获取信号量，我们需要“第三方”的介入，即操作系统内核，它在获取过程中会挂起其他线程的执行。

FreeRTOS 提供了两个不同的 API 来管理二进制信号量和计数信号量，而 CMSIS-RTOS2 规定信号量实现为计数信号量（将二进制信号量的角色留给互斥锁）。然而，使用计数信号量会增加 FreeRTOS 的代码库，这可能会对闪存内存较小的微控制器产生重要影响。因此，FreeRTOS 仅在 FreeRTOSConfig.h 文件中定义宏 configUSE_COUNTING_SEMAPHORES 且其值等于 1 时才提供它们。

在 CMSIS-RTOS2 API 中，使用以下函数创建信号量：

```c
osSemaphoreId_t osSemaphoreNew(uint32_t max_count, uint32_t initial_count,
                               const osSemaphoreAttr_t *attr);
```

其中 max_count 指定可用令牌的最大数量³⁷（max_count 值为 1 时创建二进制信号量），initial_count 设置可用令牌的初始数量。要获取信号量中的一个令牌，我们使用函数：

³⁷在 CMSIS-RTOS2 术语中，由计数信号量访问的资源称为令牌。因此，我们说信号量允许获取/释放令牌。

<!-- page: 662 -->

```c
osStatus_t osSemaphoreAcquire(osSemaphoreId_t semaphore_id, uint32_t timeout);
```

该函数接受信号量 ID 和以滴答（ticks）为单位的超时时间。如果信号量计数器大于零，线程获取它（减少计数器）并可以继续。否则，它将被置于阻塞状态，持续时间等于超时值，直到计数器再次增加。线程可以通过指定 osWaitForever 值无限期等待。如果线程成功获取信号量，osSemaphoreAcquire() 返回 osOK。要释放计数信号量中的一个令牌，我们使用函数

```c
osStatus_t osSemaphoreRelease(osSemaphoreId_t semaphore_id);
```

要查看计数信号量中有多少个空闲令牌（即，在计数器变为零之前我们还能获取信号量的次数），我们可以使用函数：

```c
uint32_t osSemaphoreGetCount(osSemaphoreId_t semaphore_id);
```

必须使用以下函数显式销毁信号量：

```c
osStatus_t osSemaphoreDelete(osSemaphoreId_t semaphore_id);
```

> **注意**
>
> 正如与队列操作相关的 API 所示，FreeRTOS 提供了两个独立的 API，用于从线程或从 ISR 中操作信号量。例如，xSemaphoreTake() 函数用于从线程中获取信号量，而 xSemaphoreTakeFromISR() 用于从 ISR 中执行此操作。由 ST 开发的 CMSIS-RTOS2 层旨在抽象这一方面。

以下示例展示了如何使用信号量作为通知原语。这再次是经典的闪烁应用程序，但这次 blinkThread() 的延迟由另一个线程 delayThread() 建立，该线程通过释放二进制信号量来“解锁”闪烁线程。

**文件名：** `Core/Src/main-ex4.c`

```c
51  osSemaphoreId_t semID;
52
53  int main(void) {
54    HAL_Init();
55
56    Nucleo_BSP_Init();
57    RetargetInit(&huart2);
58
59    /* Init scheduler */
60    osKernelInitialize();
61
62    /* Creation of binary semaphore */
63    semID = osSemaphoreNew(1, 1, NULL);
64    osSemaphoreAcquire(semID, osWaitForever);
65    /* Creation of blinkThread */
66    blinkThreadID = osThreadNew(blinkThread, NULL, NULL);
67    /* Creation of UARTThread */
68    delayThreadID = osThreadNew(delayThread, NULL, NULL);
69
70    /* Start scheduler */
71    osKernelStart();
72
73    /* We should never get here as control is now taken by the scheduler */
74    while (1);
75  }
76
77  void blinkThread(void *argument) {
78    while(1) {
79      osSemaphoreAcquire(semID, osWaitForever);
80      HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
81    }
82  }
83
84  void delayThread(void *argument) {
85    while(1) {
86      osDelay(500);
87      osSemaphoreRelease(semID);
88    }
89  }
```

<!-- page: 663 -->

第 63 行定义并创建了一个 ID 为 semID 的二进制信号量：该信号量立即被获取，导致其计数器变为零。blinkThread() 和 delayThread() 被调度，但前者一到达 osSemaphoreAcquire() 调用就被置于阻塞状态：由于信号量已经被“获取”，线程将被换出，直到 delayThread() 线程释放信号量，该线程每 500ms 执行一次此操作。这将导致 LD2 LED 以 2Hz 的频率闪烁。

### 23.5.3 事件标志与线程标志

示例 4 可以重新排列，以使用更适合此类应用程序的功能：事件标志（Event flags）。事件标志用于在线程之间或在中断服务程序（ISR）与线程之间触发执行状态。与队列和信号量不同：

- 事件标志允许任务在阻塞状态下等待一个或多个事件的组合发生。
- 事件标志可以被多个任务访问。

<!-- page: 664 -->

- 当事件发生时，事件标志会解除所有正在等待相同事件或事件组合的任务的阻塞。

事件标志的这些独特特性使其在同步多个任务、向多个任务广播事件、允许任务在阻塞状态下等待一组事件中的任意一个发生，以及允许任务在阻塞状态下等待多个操作完成时非常有用。事件标志还提供了减少应用程序使用的 SRAM 的机会，因为通常可以用单个事件标志替换许多二进制信号量。CMSIS-RTOS2 中的事件标志管理函数允许您控制或等待信号标志。事件标志构建在事件组（event groups）之上，这是 FreeRTOS 提供的一种类似的同步原语。在 CMSIS-RTOS2 规范中，每个事件标志最多有 31 个分配的信号标志，对应于 uint32_t 数据类型中的各个位。然而，在 FreeRTOS 中，一个事件标志最多可以有 24 个分配的信号标志，如图 23.18 所示。

<p align="center"><img src="../images/page-0664-image-01.jpeg" alt="Image from PDF page 664"></p>

<p align="center">图 23.18：事件标志中的位是如何被解释的</p>

通过使用以下函数创建事件标志：

```c
osEventFlagsId_t osEventFlagsNew(const osEventFlagsAttr_t *attr);
```

线程可以使用以下函数等待事件标志被设置：

```c
uint32_t         osEventFlagsWait(osEventFlagsId_t ef_id, uint32_t flags,
                          uint32_t options, uint32_t timeout);
```

其中 flags 是要等待的标志的按位或，timeout 是最大超时值（如果等于 0 则无超时），options 指定等待条件，可以取以下值：

- osFlagsWaitAny：等待任意标志（默认）。
- osFlagsWaitAll：等待所有标志。
- osFlagsNoClear：当线程唤醒并恢复执行时，其信号标志会自动清除，除非指定了选项 osFlagsNoClear；在这种情况下，可以使用函数 osEventFlagsClear() 手动清除标志。

如果所需的标志未设置，调用线程将进入阻塞状态。可以使用以下函数设置一个或多个标志：

<!-- page: 665 -->

```c
uint32_t osEventFlagsSet(osEventFlagsId_t ef_id, uint32_t flags);
```

或者，可以使用以下函数清除一个或多个标志：

```c
uint32_t osEventFlagsClear(osEventFlagsId_t ef_id, uint32_t flags);
```

要获取事件标志对象中标志的状态，可以使用以下函数：

```c
uint32_t osEventFlagsGet(osEventFlagsId_t ef_id);
```

以下示例展示了事件标志的一种可能用法。

**文件名：** `Core/Src/main-ex5.c`

```c
51  #define FLAG_LED_BLINK        (uint32_t)0xb00000001
52  #define FLAG_CHANGE_FREQUENCY (uint32_t)0xb00000010
53
54  osEventFlagsId_t evtID;
55
56  int main(void) {
57    HAL_Init();
58
59    Nucleo_BSP_Init();
60    RetargetInit(&huart2);
61
62    /* Init scheduler */
63    osKernelInitialize();
64
65    /* Creation of a event flag */
66    evtID = osEventFlagsNew(NULL);
67    /* Creation of blinkThread */
68    blinkThreadID = osThreadNew(blinkThread, NULL, NULL);
69    /* Creation of UARTThread */
70    delayThreadID = osThreadNew(delayThread, NULL, NULL);
71
72    /* Start scheduler */
73    osKernelStart();
74
75    /* We should never get here as control is now taken by the scheduler */
76    while (1);
77  }
78
79  void blinkThread(void *argument) {
80    while(1) {
81      osEventFlagsWait(evtID, FLAG_LED_BLINK, osFlagsWaitAll, osWaitForever);
82      HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
83    }
84  }
85
86  void delayThread(void *argument) {
87    uint8_t step = 100;
88    uint16_t delay = 500;
89
90    while(1) {
91      osEventFlagsSet(evtID, FLAG_LED_BLINK);
92
93      if(osEventFlagsWait(evtID, FLAG_CHANGE_FREQUENCY, osFlagsWaitAll, delay)
94         != osFlagsErrorTimeout ) {
95        delay -= step;
96        switch(delay) {
97        case 100:
98          step = 50;
99          break;
100       case 50:
101         step = 25;
102         break;
103       case 0:
104         step = 100;
105         delay = 500;
106         break;
107        }
108     }
109   }
110 }
111
112 void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {
113   if(GPIO_Pin == GPIO_PIN_13)
114     osEventFlagsSet(evtID, FLAG_CHANGE_FREQUENCY);
```

<!-- page: 666 -->

线程 blinkThread() 处于阻塞状态，直到标志 FLAG_LED_BLINK 被线程 delayThread() 设置。默认情况下，delayThread() 每 500ms 设置一次该标志，导致 LD2 LED 以 2Hz 的频率闪烁。当按下 USER 按钮时，相应的 EXTI 回调函数会设置标志 FLAG_CHANGE_FREQUENCY：这会导致 delay 变量递减，从而增加闪烁频率。

虽然事件标志可以被任意数量的线程和中断服务程序（ISR）访问，但线程标志（thread flags）是事件标志的更专业化版本，它们仅与特定的给定线程相关。每个线程实例都可以接收线程标志，而无需额外分配线程标志对象。然而，线程标志的底层实现与事件标志完全不同：它不使用 FreeRTOS 事件组，而是使用 FreeRTOS 提供的一种称为任务通知（task notifications）的特定机制。

<!-- page: 667 -->

无需创建新的线程标志，但可以使用以下函数直接设置给定线程的标志：

```c
uint32_t osThreadFlagsSet(osThreadId_t thread_id, uint32_t flags);
```

此函数是唯一可以从中断服务程序（ISR）上下文中调用的线程标志函数。一旦设置，标志可以由正在运行的线程通过调用以下函数来清除：

```c
uint32_t osThreadFlagsClear(uint32_t flags);
```

## 23.6 资源管理与互斥

在嵌入式应用中，访问硬件资源是非常常见的。例如，假设我们使用 UART 外设将调试消息写入控制台，并且假设我们的应用程序由多个线程组成，这些线程可以使用 HAL_UART_Trasmit() 例程打印消息。如果您还记得，在第 8 章中我们看到，当我们在轮询模式下使用 UART 时，我们要传输的消息中包含的字节会逐个传输到 UART 数据寄存器 (Data Register, DR) 中。与实时操作系统 (real-time operating system, RTOS) 在单位时间内可能执行的活动数量相比，这是一个相当“缓慢的过程”。这意味着，如果两个线程调用 HAL_UART_Trasmit()，它们很可能会覆盖缓冲寄存器的内容。

> **注意**
>
> 如果您还记得，同样在那一章中我们看到，HAL 试图通过使用 __HAL_LOCK() 宏来保护对外设的并发访问。然而，没有保证在多线程环境中该宏能防止竞态条件，因为锁定操作不是原子执行的。

虽然信号量最适合同步线程活动，但互斥锁 (mutex) 和临界区是并发编程中保护共享资源的一种方式。FreeRTOS 为我们提供了这两种原语，而 CMSIS-RTOS2 层仅定义了互斥锁的概念。然而，临界区在许多场合都很有用；有时，与其让开发人员付出更多编程努力去规避优先级反转这类微妙状况，使用临界区反而是更好的解决方案。

### 23.6.1 互斥锁

互斥锁 (Mutex) 是 MUTual EXclusion（互斥）的缩写，它是一种用于控制对共享资源访问的二进制信号量。从概念上讲，互斥锁与信号量有两个区别：

<!-- page: 668 -->

- 互斥锁必须始终被获取，然后释放以指示受保护的资源现在再次可用，而信号量甚至可以释放以唤醒阻塞的线程（我们在示例 4 中见过这种模式）；此外，通常互斥锁由同一个线程获取和释放³⁸；
- 互斥锁实现了优先级继承 (priority inheritance)，这是一个我们稍后将分析的特性，用于最小化优先级反转问题。

要使用互斥锁，我们需要在 FreeRTOSConfig.h 文件中定义宏 configUSE_MUTEXES 并将其设置为 1。使用以下函数定义互斥锁：

```c
osMutexId_t osMutexNew(const osMutexAttr_t *attr);
```

其中 osMutexAttr_t.attr_bits 字段可以取以下值：

- osMutexRecursive：线程可以多次获取互斥锁而不会造成自身死锁。稍后我们将详细介绍递归互斥锁。
- osMutexPrioInherit：拥有者线程继承（更高优先级的）等待线程的优先级。目前 osMutexNew() 忽略此选项，因为这是 FreeRTOS 的默认实现策略。接下来我们将讨论优先级反转问题。
- osMutexRobust：当拥有者线程终止时，互斥锁会自动释放。目前 osMutexNew() 忽略此选项，因为这是 FreeRTOS 的默认实现策略。

与信号量类似，要获取互斥锁，我们使用函数

```c
osStatus_t osMutexAcquire(osMutexId_t mutex_id, uint32_t timeout);
```

要释放它，我们使用函数：

```c
osStatus_t osMutexRelease(osMutexId_t mutex_id);
```

最后，要销毁互斥锁，我们必须显式调用函数

```c
osStatus_t osMutexDelete(osMutexId_t mutex_id);
```

³⁸然而，与其他操作系统不同，FreeRTOS 并未实现检查只有获取了互斥锁的线程才能释放它的功能。

<!-- page: 669 -->

#### 23.6.1.1 优先级反转问题

互斥锁可能会引入一个不希望的微妙问题，这在文献中被称为优先级反转问题。让我们借助图 23.19 来考虑这个场景。

<p align="center"><img src="../images/page-0669-image-01.png" alt="Image from PDF page 669"></p>

<p align="center">图 23.19：该图示意了优先级反转问题</p>

ThreadL()、ThreadM() 和 ThreadH() 是三个具有递增优先级的线程（L 代表低，M 代表中，H 代表高）。ThreadL() 开始执行并获取了一个用于保护共享资源的互斥锁。在其执行期间，ThreadH() 返回就绪模式，并且由于具有更高的优先级而被调度执行。然而，它也需要获取同一个互斥锁，并回到阻塞状态。突然，中等优先级的线程 ThreadM() 变为可用，并且由于具有比 ThreadL() 更高的优先级而被调度执行。因此 ThreadL() 无法完成其工作，互斥锁保持锁定状态，阻止 ThreadH() 执行。在这种情况下，我们得到了 ThreadL() 和 ThreadH() 之间优先级被反转的实际效果，因为 ThreadH() 在 ThreadL() 释放互斥锁之前无法执行。

应该通过以不同方式重新组织应用程序来完全避免优先级反转问题。然而，FreeRTOS 试图通过临时提高互斥锁持有者（在我们的情况下是 ThreadL()）的优先级到尝试获取同一互斥锁的最高优先级线程的优先级，来最小化此问题的影响。

<!-- page: 670 -->

<p align="center"><img src="../images/page-0670-image-01.png" alt="Image from PDF page 670"></p>

<p align="center">图 23.20：如何通过临时提高 ThreadL 的优先级来解决优先级反转问题</p>

图 23.20 清楚地展示了这一过程。ThreadL() 开始执行并获取了一个互斥锁。在其执行期间，ThreadH() 返回就绪模式，并且由于具有更高的优先级而被调度执行。然而，它也需要获取同一个互斥锁，并回到阻塞状态。这一次，ThreadL() 的优先级被提高到与 ThreadH() 相同，从而阻止 ThreadM() 执行。ThreadL() 再次被调度，它可以释放互斥锁，允许 ThreadH() 运行。最后，ThreadM() 可以执行，因为当 ThreadL() 释放互斥锁时，其优先级降低回原始优先级。

#### 23.6.1.2 递归互斥锁

有时，特别是当我们的应用程序分散在多个 API 中时，一个线程可能会意外地多次获取同一个互斥锁。由于互斥锁只能被获取一次，同一线程随后尝试再次获取该互斥锁将导致死锁（因为对 osMutexWait() 的后续调用会使该线程进入阻塞状态，但它是唯一被设计用来释放该互斥锁的线程）。

为了防止这种不期望的行为，FreeRTOS 引入了递归互斥锁（recursive mutexes）的概念，即可以被多次获取的互斥锁。显然，递归互斥锁需要被释放的次数与其被获取的次数相同。要通过 CMSIS-RTOS2 API 将互斥锁配置为递归类型，需要在调用 osMutexNew() 函数时指定 osMutexRecursive 属性。

### 23.6.2 临界区

有时，特别是当我们需要对共享资源执行快速操作时，最好完全避免使用同步原语。如前所述，除非我们特别小心地处理实时操作系统（real-time operating system, RTOS）提供的同步结构，否则很容易在应用程序中引入奇怪的行为。

临界区（critical sections）是一种保护共享资源访问的方式。临界区是一段代码区域，它在所有中断被禁用后执行。由于任务的抢占发生在中断服务程序（ISR）内部（即被选为时基发生器的定时器的 ISR），通过禁用所有 ISR，我们可以确保没有其他代码会抢占临界区内部代码的执行。

<!-- page: 671 -->

```c
...
__disable_irq();
//All IRQs are disabled and we are sure that the next code will not be preempted
...
//Critical code here
...
__enable_irq();
//All IRQs are now enabled again, and normal behaviour of the RTOS is restored
```

使用 CMSIS API 实现临界区并非一项简单的任务，因为我们需要注意可能发生的特殊硬件情况。然而，FreeRTOS 提供了四个例程，我们可以使用它们来在应用程序中定义临界区。

taskENTER_CRITICAL() 和 taskEXIT_CRITICAL() 函数允许在线程内部定义临界区。这些例程被设计为跟踪嵌套情况，即每次调用 taskENTER_CRITICAL() 时，一个计数器会递增，而在后续调用 taskEXIT_CRITICAL() 函数时，该计数器会递减。这意味着我们必须确保遵守调用顺序。

```c
taskENTER_CRITICAL(); //Internal counter increased to 1
...
        taskENTER_CRITICAL(); //Internal counter increased to 2
        ...
        taskEXIT_CRITICAL(); //Internal counter decreased to 1
...
taskEXIT_CRITICAL(); //Internal counter decreased to 0
```

临界区仅在用于保护少量代码行且这些代码能在短时间内完成其活动时才有效。否则，整个应用程序可能会受到其使用的影响。

taskENTER_CRITICAL() 和 taskEXIT_CRITICAL() 函数绝不应从中断服务程序（ISR）中调用：相应的 taskENTER_CRITICAL_FROM_ISR() 和 taskEXIT_CRITICAL_FROM_ISR() 函数适用于此场景。更多信息请参阅 FreeRTOS 文档。

### 23.6.3 使用 RTOS 进行中断管理

中断服务程序的一般经验法则是它们需要快速执行。缓慢的 ISR 可能导致其他事件的丢失，无论是来自同一外设还是来自其他源（如果该 ISR 具有更高的优先级）。

RTOS 的某些功能可以通过将实际的中断处理推迟到线程中来简化中断管理。延迟执行（deferred execution），或简称为延迟，是指将实际的中断处理委托给另一个执行流，该执行流不在与中断例程相同的“低级别”上运行。例如，在第 8 章中我们看到，当新的数据准备好从 UART 数据寄存器传输时，会生成 USARTx_IRQn 中断：ISR 实际上从寄存器中获取这些字节并将其放入缓冲区。然而，我们也看到 UART_IRQ_Handler() 执行了许多其他操作，这些操作会减慢 ISR 的执行速度。

<!-- page: 672 -->

在这种场景下，我们可以为每个 ISR 设置一个专用线程。该线程将花费大量时间处于阻塞模式，等待特定信号。当 IRQ 触发时，我们可以触发该信号，导致被阻塞的线程恢复执行，以完成原本由相应 ISR 执行的工作。通过为线程分配不同的优先级，我们可以在并发 ISR 的情况下建立执行顺序。另一种方法是使用队列将来自外设的数据传输到工作线程，该线程稍后处理这些数据。当消费者线程比外设 ISR 慢时，这种方法特别有用，在这种情况下，ISR 充当消费者线程。

FreeRTOS 提供了另一种方便的方式来将 ISR 执行延迟到另一个执行流。这被称为集中式延迟中断处理，它由将例程的执行延迟到 FreeRTOS 守护任务³⁹中组成。此方法使用 xTimerPendFunctionCallFromISR()，该函数在 FreeRTOS 手册⁴⁰中有文档说明。

然而，请记住，无论是将执行延迟到另一个线程还是使用队列交换数据，都意味着 CPU 执行了多个操作，这可能会影响 ISR 管理的可靠性。如果你的外设运行速度很快，最好使用其他方式传输数据，例如使用直接存储器访问（direct memory access, DMA）。始终考虑 UART 传输的例子，如果我们的应用程序通过 UART 交换固定长度的消息，我们可以设置 DMA 来传输一条消息，然后使用 DMA IRQ 将整个消息移入队列。这肯定会最小化与单个字节传输相关的开销。

#### 23.6.3.1 FreeRTOS API 与中断优先级

到目前为止，我们已经了解到 FreeRTOS 提供了一些专门设计用于在中断服务程序（ISR）中调用的 API。对于给定的 FreeRTOS 函数，存在一个对应的 ISR 安全例程，其名称以 FromISR() 结尾（例如，xQueueReceive() 例程对应的 xQueueReceiveFromISR()）。这些例程的设计使得中断会被屏蔽（通过进入然后退出临界区），从而防止执行其他可能通过调用其他 FreeRTOS 函数而产生竞态条件的中断。

中断屏蔽是必需的，因为中断是由硬件处理的多任务处理源。虽然线程是由实时操作系统（RTOS）处理的不同程序流，它通过简单地挂起调度器的执行来避免竞态条件，但 ISR 是由硬件生成的，除非我们屏蔽其执行或定义严格的基于优先级的执行顺序，否则我们几乎无法避免竞态条件。此外，Cortex-M 内核提供的嵌套机制增加了我们代码中发生竞态条件的风险。例如，一个正在获取信号量的 ISR 可能会被另一个执行相同操作的高优先级 ISR 抢占。这肯定会带来灾难性的后果。

³⁹FreeRTOS 守护任务也被称为定时器服务任务，因为它是处理定时器回调例程执行的线程，我们稍后将会分析。⁴⁰http://www.freertos.org/xTimerPendFunctionCallFromISR.html

<!-- page: 673 -->

尽管 CMSIS-RTOS2 层旨在抽象这种双 API 系统，但在基于 Cortex-M3/4/7 的微控制器中从 ISR 例程调用 FreeRTOS API 时，我们必须格外小心。

这是因为这些内核允许基于优先级级别选择性地屏蔽中断。在第 7 章中，我们看到 BASEPRI 寄存器允许通过屏蔽所有优先级低于给定值的中断请求（IRQ）来选择性地禁用 ISR 的执行。FreeRTOS 利用此机制允许执行高优先级中断（假设这些中断是不可中断的），同时挂起低优先级中断。这意味着从所有 ISR 中调用 FreeRTOS API 并不安全，只有从具有给定（或更低）优先级级别的 ISR 中调用 FreeRTOS 函数才是安全的。

我们可以通过在 FreeRTOSConfig.h 文件中定义宏 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY⁴¹ 来设置此最大优先级级别。CubeMX 会自动为我们执行此操作，通常最大优先级级别设置为 5。当使用 CubeMX 启用中断请求（IRQ）时必须格外小心：即使最近版本的 CubeMX 似乎能正确处理这一方面，也要始终确保调用 FreeRTOS 函数的 ISR 配置的优先级等于 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY 或更低。

⁴¹如果你阅读官方的 FreeRTOS 文档，可以看到用于设置最大可中断优先级级别的宏是 configMAX_SYSCALL_INTERRUPT_PRIORITY。然而，由于 FreeRTOS 在多个芯片供应商之间具有可移植性，该宏指定的优先级级别是 IPR 寄存器的确切值，在 STM32 微控制器中仅接受高 4 位（例如，等于 0x2 的优先级必须指定为 0x20）。ST 工程师定义了宏 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY，以便我们可以根据 HAL 约定（以最低有效位形式）指定优先级级别，而 configMAX_SYSCALL_INTERRUPT_PRIORITY 定义如下：#define configMAX_SYSCALL_INTERRUPT_PRIORITY ( configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY << (8 - configPRIO_BITS) )

尽管该宏也在 CubeMX 为 STM32F0/L0 微控制器生成的项目中定义，但这没有实际效果，因为针对这些系列的 FreeRTOS 移植版本使用 PRIMASK 寄存器来屏蔽所有中断（Cortex-M0/0+ 内核不提供选择性地禁用中断请求的方法）。因此，该宏被简单地忽略。

最后，重要的是要记住，FreeRTOS 的设计要求滴答中断（即与作为内核时基发生器的定时器相关联的中断请求）必须设置为尽可能低的中断优先级，在 STM32F0/L0 系列中等于 7，在所有其他微控制器中等于 15。FreeRTOSConfig.h 文件中的宏 configLIBRARY_LOWEST_INTERRUPT_PRIORITY 设置了此值，强烈建议保持其默认设置不变。

## 23.7 软件定时器

软件定时器是实时操作系统提供的一种基于时间调度例程执行的方式。软件定时器由 FreeRTOS 内核实现并受其控制。它们不需要特定的硬件支持（除了用作操作系统滴答生成器的定时器），并且与硬件定时器没有任何关系。此外，它们无法提供与硬件定时器相同的精度，并且永远不应用于执行与硬件相关的活动（例如，触发直接存储器访问事件）。

软件定时器是 FreeRTOS 中的一个可选功能，需要在 FreeRTOSConfig.h 文件中将宏 config_USE_TIMERS 设置为 1 来启用。当我们启用定时器时，FreeRTOS 还要求我们定义宏 configTIMER_TASK_PRIORITY、configTIMER_QUEUE_LENGTH、configTIMER_TASK_STACK_DEPTH。我们稍后将会看到这些宏的作用。

在 CMSIS-RTOS2 层中，使用以下函数创建软件定时器：

<!-- page: 674 -->

```c
osTimerId_t osTimerNew(osTimerFunc_t func, osTimerType_t type,
                       void *argument, const osTimerAttr_t *attr);
```

其中 func 是指向定时器到期时要调用的函数的指针，argument 是传递给回调例程的可选参数。CMSIS-RTOS2 API 提供两种类型的软件定时器，通过参数 type 进行配置：

- osTimerOnce：单次定时器，即只执行一次回调的定时器。
- osTimerPeriodic：周期定时器，其行为类似于在溢出后重新开始计数的硬件 STM32 定时器。

要启动定时器，我们使用函数

```c
osStatus_t osTimerStart(osTimerId_t timer_id, uint32_t ticks);
```

其中 ticks 参数表示以滴答（ticks）为单位的定时器周期。要停止定时器，我们使用函数

```c
osStatus_t osTimerStop(osTimerId_t timer_id);
```

相反，要检查定时器是否正在运行，我们使用函数：

```c
uint32_t osTimerIsRunning(osTimerId_t timer_id);
```

最后，定时器由操作系统动态分配，当不再需要时，必须使用以下函数将其销毁

```c
osStatus osTimerDelete(osTimerId timer_id);
```

以下示例展示了使用软件定时器实现的我们无处不在的闪烁应用程序。

**文件名：** `Core/Src/main-ex6.c`

```c
1   void blinkFunc(void *argument);
2
3   int main(void) {
4     osTimerId_t timID;
5
6     HAL_Init();
7
8     Nucleo_BSP_Init();
9
10    /* Init scheduler */
11    osKernelInitialize();
12
13    /* Creation of blinkThread */
14    timID = osTimerNew(blinkFunc, osTimerPeriodic, NULL, NULL);
15    osTimerStart(timID, 500);
16
17    /* Start scheduler */
18    osKernelStart();
19
20    /* We should never get here as control is now taken by the scheduler */
21    while (1);
22  }
23
24  void blinkFunc(void *argument) {
25    HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
26  }
```

<!-- page: 675 -->

### 23.7.1 FreeRTOS 如何管理定时器

正如前一个示例所示，我们的应用程序不使用线程。那么，谁负责处理定时器呢？FreeRTOS 使用一个集中式的线程，称为 RTOS 守护任务（也称定时器服务线程），当定时器到期时，该线程会自动调用回调例程。这是一个常规线程，其优先级由宏 configTIMER_TASK_PRIORITY 定义，堆栈大小由宏 configTIMER_TASK_STACK_DEPTH 定义。此外，它拥有一个内部定时器对象池，其大小由宏 configTIMER_QUEUE_LENGTH 定义。

另一个需要强调的重要方面是 FreeRTOS 内部计算时间的方式。FreeRTOS 根据滴答（tick）频率来测量时间，而滴答频率又由选作时基发生器的定时器的溢出频率定义。这意味着，如果我们使用配置为每 1ms 溢出一次的 SysTick 定时器，那么内部软件定时器的分辨率为 1ms（对应 1 个滴答）。传递给 osTimerStart() 例程的滴答值因此与全局滴答频率绑定。

## 23.8 案例研究：使用实时操作系统进行低功耗管理

> **注意**
>
> 这是一个非常高级的主题，需要了解实时操作系统背后的许多概念。此外，还需要对第 20 章中阐述的概念有相当的了解。经验不足的用户可以安全地跳过这部分内容。

在第 19 章中，我们分析了 STM32 微控制器提供的低功耗特性。我们看到，特别是对于属于 STM32L 系列的 MCU，它们提供了多种电源模式。当没有太多活跃工作时，这些模式有助于降低 MCU 的能耗。我们还看到，MCU 通过调用两条专用汇编指令之一（WFI 或 WFE）自愿进入其低功耗模式之一。如果我们知道固件在“较长”时间内没有重要任务要做，我们可以进入低功耗模式，等待外部中断或事件。

<!-- page: 676 -->

当我们使用实时操作系统时，很难判断“什么时候没有太多工作要做”。到目前为止，我们看到实时操作系统在所有其他线程都处于阻塞或挂起状态时调度特定的线程：即空闲线程。这意味着实时操作系统必须始终找到一种方法来执行某些操作（仅仅因为 CPU 永远不会停止），除非我们进入低功耗模式以停止 MCU 内核。

因此，如果我们找不到一种解决方案来暂停实时操作系统的执行，它就会成为“电源泄漏”的来源。当使用实时操作系统时，基本上有两种方法可以将 MCU 置于低功耗模式：一种适合“打个盹”，另一种适合更长、更深的睡眠模式。让我们分析这两种方法。

### 23.8.1 空闲线程钩子

到目前为止，我们看到与用作实时操作系统时基发生器的定时器（通常是 SysTick 定时器）相关联的中断服务例程（ISR）主导着实时操作系统的活动。每 1ms SysTick 定时器发生下溢，其中断服务例程将控制权传递给操作系统调度器，调度器确定下一个要执行的线程⁴²。如果没有线程处于就绪状态，则操作系统执行空闲线程，直到另一个线程变为就绪。这意味着，当空闲线程被调度时，很可能正是将 MCU 置于睡眠模式以降低功耗的正确时机。

因此，FreeRTOS 允许用户定义一个空闲钩子，即在空闲线程内调用的回调函数。要启用该钩子，我们必须在 FreeRTOSConfig.h 文件中定义宏 configUSE_IDLE_HOOK 并将其设置为 1。接下来，我们可以在源代码的某处定义函数 vApplicationIdleHook(void)。例如，为了在每次调度空闲线程时将 MCU 置于睡眠模式，我们可以这样定义该函数：

```c
void vApplicationIdleHook( void ) {
  //Assume __HAL_RCC_PWR_CLK_ENABLE() is called elsewhere
  HAL_PWR_EnterSLEEPMode(PWR_MAINREGULATOR_ON, PWR_SLEEPENTRY_WFE);
}
```

⁴²当调度策略为带时间片轮转的优先级抢占式调度时，会启用此行为，参见表 23.2。

<!-- page: 677 -->

> **应该使用哪种睡眠指令？**
>
> 基于 Cortex-M 的 MCU 提供两条汇编指令以进入低功耗模式：WFI 和 WFE。但是，哪一条更适合从空闲钩子中调用？WFI 指令将使 MCU 内核保持关闭状态，直到引发中断。这可能是 SysTick 定时器的中断，也可能是其他外设的中断。相反，WFE 指令是有条件的：如果事件寄存器已置位，它不会进入睡眠模式（如果存在挂起的中断，WFI 则总是先进入睡眠、再立即退出，白白浪费几个 CPU 周期）。此外，如果我们使用与特定外设相关联的事件而不是中断，WFE 允许唤醒处理器，同时它仍然能够在发生中断时唤醒。基于这些原因，在空闲循环中，WFE 指令总是优于 WFI 指令。

这种简单方法所能实现的节能效果受到限制，因为必须定期退出然后重新进入低功耗模式以处理滴答中断（这与 SysTick 定时器的下溢频率相关），如图 23.21 所示。此外，如果滴答中断的频率太高，那么对于每个滴答进入然后退出低功耗模式所消耗的能量和时间将超过除最轻量级节能模式以外的所有潜在节能收益。

基于这些原因，进入更深的睡眠模式（如停止模式）是完全不可行的。此外，与进入和退出低功耗模式相关的开销会影响滴答计数器的可靠性，导致偏移，从而影响软件定时器和超时延迟。

### 23.8.2 FreeRTOS 中的无滴答模式 (Tickless Mode)

为了解决这些问题，FreeRTOS 提供了一种名为无滴答空闲模式（或简称无滴答模式，tickless idle mode）的工作模式，该模式在空闲期间停止周期性的滴答中断（tick interrupt）。这些空闲时段的持续时间是不确定的：可以是几毫秒、几秒、几分钟甚至几天。当微控制器从低功耗模式退出时，如果需要，FreeRTOS 会在重启滴答中断时对滴答计数值进行校正调整（稍后我们将详细介绍这一点）。这意味着 FreeRTOS 根本不会停止定时器：它只是配置定时器，使其在溢出之前达到其最大更新周期。当微控制器再次唤醒时，内核（kernel）读取定时器的计数器值，并计算睡眠期间经过的滴答数。

<!-- page: 678 -->

<p align="center"><img src="../images/page-0678-image-01.jpeg" alt="Image from PDF page 678"></p>

<p align="center">图 23.21：SysTick 中断对功耗的影响</p>

例如，假设有一个 16 位定时器，其时钟频率为内核 SYSCLK 频率 48MHz。Period 寄存器和 Prescaler 寄存器的最大值为 0xFFFF。因此，与其将定时器配置为每 1ms 溢出一次，我们可以将其配置为在以下时间后溢出：

UpdateEvent = 48.000.000 / (0xFFFF × 0xFFFF) ≈ 90s

FreeRTOS 提供了内置的无滴答功能，通过在 FreeRTOSConfig.h 中将宏 configUSE_TICKLESS_IDLE 定义为 1 来启用。内置的无滴答模式依赖于平台：因此，它在 port.c 文件中实现。内置的无滴答功能适用于所有 Cortex-M 内核，但它有一个重要的限制：它依赖于 SysTick 定时器，因为这是基于该架构的所有微控制器中唯一可用的定时器。

这有什么问题？SysTick 定时器是一个 24 位递减计数器定时器，时钟频率与内核时钟频率相同。不幸的是，它不能像常规 STM32 定时器那样轻松地进行分频（在所有 STM32 微控制器中，它只有一个分频值，等于 8）。例如，对于一个运行在 48MHz 的 STM32F030，应用第 11 章中的公式 [1]，SysTick 定时器将每以下时间溢出一次：

UpdateEvent = 48.000.000 / (8 × 0xFFFFFF) ≈ 0.350Hz ≈ 2.8s

由于我们绝对不能丢失溢出事件，否则全局滴答计数将受到损害⁴³，因此即使没有重要的事情要做，我们也必须再次唤醒。对于大多数低功耗应用来说，两次连续睡眠之间的间隔是很短的。

⁴³ 正如我们稍后将发现的，在某些情况下，我们可以安全地停止递增全局滴答计数器。当我们不打算使用软件定时器和超时时，就可以这样做：如果所有线程都被无限期地阻塞或挂起，那么完全关闭时基发生器是安全的。

<!-- page: 679 -->

一种解决方案可能是降低 HCLK 速度以进一步增加溢出周期，但我们必须注意不要将内核频率降低得太多，因为当微控制器

从低功耗模式退出以处理中断时，较低的 HCLK 速度可能会损害系统的可靠性。而且从 ISR 中增加时钟速度也不是明智之举。

> **为什么滴答计数的准确性如此重要？**
>
> 全局滴答计数的准确性对于两个主要原因很重要：保证所有具有相同优先级的就绪线程（如果启用了抢占）获得相同的时间量子，以及确保精确的超时延迟。事实上，许多阻塞式操作系统例程允许指定在操作执行之前愿意等待的最大延迟。超时以滴答为单位指定，已知对于 Cortex-M FreeRTOS 移植，一个滴答通常持续 1ms。如果我们指定的超时小于 osWaitForever，那么滴答计数尽可能准确是很重要的。全局滴答计数也被 FreeRTOS 用于实现软件定时器。

使用 SysTick 定时器的另一个限制源于它不能在停止模式（stop modes）中使用，因为 HCLK 时钟源被关断了。这是大多数 STM32L 微控制器提供的低功耗定时器（LPTIM）的典型应用之一。事实上，LPTIM 定时器可以独立于系统时钟运行：这允许即使在停止模式下也可以使用它们。

基于所有这些原因，我们现在将提供一个无滴答空闲功能的自定义实现，该功能可以通过在 FreeRTOSConfig.h 中将 configUSE_TICKLESS_IDLE 定义为 2 来为任何 FreeRTOS 移植（包括提供内置实现的移植）提供。当选择此配置时，我们可以覆盖两个 FreeRTOS 函数：void prvSetupTimerInterrupt()⁴⁴ 和 void vPortSuppressTicksAndSleep()。前者由内核用于设置用作滴答发生器的定时器。后者在内核满足某些条件（我们稍后会看到）时自动调用，我们可以进入低功耗模式，从而延迟或完全挂起周期性定时器中断。

#### 23.8.2.1 无滴答模式的方案

在深入探讨实现这两个例程所需的实际源代码之前，最好先在不纠结于实现细节的情况下查看其底层逻辑。

```c
1   /* Override the default definition of vPortSetupTimerInterrupt() with a version
2    that configures another STM32 timer to generate the tick interrupt. */
3   void vPortSetupTimerInterrupt(void) {
4     /* Scale the clock so longer tickless periods can be achieved by dividing
5      the HCLK frequency for the wanted tick frequency (usuallu 1ms).  */
6
7     htimx.Instance = TIMx;
8     htimx.Init.Prescaler = PRESCALER_VALUE;
9     htimx.Init.Period = PERIOD_VALUE
10    HAL_TIM_Base_Init(&htimx);
11
```

⁴⁴在 Cortex-M3/4 移植层中，该函数被称为 vPortSetupTimerInterrupt()。

<!-- page: 680 -->

```c
12    /* Enable the TIMx interrupt.  This must execute at the lowest interrupt priority. */
13    HAL_NVIC_SetPriority(TIMx_IRQn, configLIBRARY_LOWEST_INTERRUPT_PRIORITY, 0);
14    HAL_NVIC_EnableIRQ(TIMx_IRQn);
15
16    /* Start the timer */
17    HAL_TIM_Base_Start_IT(&htimx);
18  }
```

我们要覆盖的第一个例程是 vPortSetupTimerInterrupt()。它简单地使用可用的 STM32 定时器之一作为时基发生器，通过配置正确的 Period（周期）和 Prescaler（预分频器）值，以实现频率等于 1kHz 的滴答中断。定时器 ISR（中断服务例程，稍后展示）将负责递增全局滴答计数器。

> **仔细阅读**
>
> 在第 10 章中，我们看到 HAL（硬件抽象层）被设计为在更改 HCLK 频率时自动调用 SystemCoreClockUpdate()。这确保了即使内核时钟发生变化，SysTick 中断仍每 1ms 生成一次。然而，如果我们使用另一个定时器作为 RTOS 滴答计数器，那么当该定时器所属的 APB 总线时钟速度发生变化时，由我们负责仔细确保定时器被相应地重新配置。

> **仔细阅读**
>
> 在 Cortex-M0/0+ 架构的移植文件（Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM0/port.c）中，设置定时器的函数被称为 prvSetupTimerInterrupt()，并且未定义为 __attribute__((weak))。将该函数的属性从 static 更改为 __attribute__((weak))，以便调用 Core/Src/tickless-mode.c 中的版本。完整代码请参考本书示例。

接下来的代码行展示了 vPortSuppressTicksAndSleep() 的一种可能实现，该函数在以下两个条件同时为真时被调用：

1. 空闲线程是唯一能够运行的线程，因为所有应用程序线程要么处于阻塞状态，要么处于挂起状态。
2. 在内核将应用程序线程移出阻塞状态之前，至少还有 n 个完整的滴答周期将过去，其中 n 由 FreeRTOS.h 文件中的 configEXPECTED_IDLE_TIME_BEFORE_SLEEP 宏设置⁴⁵。

如果满足上述条件，则调度器被挂起，并调用 vPortSuppressTicksAndSleep() 函数，允许我们暂时抑制滴答中断或延迟其执行。

⁴⁵这是一个用户定义的参数，表示在开始滴答抑制程序之前的额外延迟。由于该程序计算密集，且可能会引入全局滴答计数的微小偏移，我们可以编程决定在开始该程序之前至少等待 n 个连续的滴答。

<!-- page: 681 -->

```c
20  /* Override the default definition of vPortSuppressTicksAndSleep() with a version
21   that uses another STM32 timer to derive how long the micro is remained in sleep state */
22  void vPortSuppressTicksAndSleep(TickType_t xExpectedIdleTime) {
23    unsigned long ulLowPowerTimeBeforeSleep, ulLowPowerTimeAfterSleep;
24    eSleepModeStatus eSleepStatus;
25
26    /* Read the current time from the timer configured by the
27     vPortSetupTimerInterrupt() function */
28    ulLowPowerTimeBeforeSleep = __HAL_TIM_GET_COUNTER(TIMx);
29
30    /* Stop the timer that is generating the tick interrupt. */
31    HAL_TIM_Base_Stop_IT(TIMx);
32
33    /* Enter a critical section that will not affect interrupts bringing the MCU
34     out of sleep mode. */
35    __disable_irq();
36
37    /* Ensure it is still ok to enter the sleep mode. */
38    eSleepStatus = eTaskConfirmSleepModeStatus();
39
40    if (eSleepStatus == eAbortSleep) {
41      /* A task has been moved out of the Blocked state since this macro was
42       executed, or a context switch is being held pending.  Do not enter a
43       sleep state.  Restart the tick and exit the critical section. */
44      HAL_TIM_Base_Start_IT (TIMx)
45      __enable_irq();
46    } else {
47      if (eSleepStatus == eNoTasksWaitingTimeout) {
48        /* There are no running state tasks and no tasks that are blocked with a
49         time out.  Assuming the application does not care if the tick time slips
50         with respect to calendar time then enter a deep sleep that can only be
51         woken by another interrupt. */
52        StopMode();
53    }else{
54        /* Configure an interrupt to bring the microcontroller out of its low
55         power state at the time the kernel next needs to execute.  The
56         interrupt must be generated from a source that remains operational
57         when the microcontroller is in a low power state. */
58        vSetWakeTimeInterrupt(xExpectedIdleTime);
59
60        /* Enter the low power state. */
61        SleepMode();
62
63        /* Determine how long the microcontroller was actually in a low power
64         state for, which will be less than xExpectedIdleTime if the
65         microcontroller was brought out of low power mode by an interrupt
66         other than that configured by the vSetWakeTimeInterrupt() call.
67         Note that the scheduler is suspended before
68         vPortSuppressTicksAndSleep() is called, and resumed when it returns.
69         Therefore no other tasks will execute until this function completes. */
70        ulLowPowerTimeAfterSleep = __HAL_TIM_GET_COUNTER(TIMx);
71
72        /* Correct the kernels tick count to account for the time the
73         microcontroller spent in its low power state. */
74      vTaskStepTick( ulLowPowerTimeAfterSleep - ulLowPowerTimeBeforeSleep );
75    }
76
77    /* Exit the critical section - it might be possible to do this immediately
78     after the prvSleep() calls. */
79    __disable_irq();
80
81    /* Restart the timer that is generating the tick interrupt. */
82    HAL_TIM_Base_Stop_IT(TIMx);
83  }
```

<!-- page: 682 -->

该例程首先保存定时器停止前的当前计数器值。禁用所有中断以防止竞态条件，通过调用 CMSIS 函数 __disable_irq() 进入临界区。如前所述，当调度器被挂起时调用 vPortSuppressTicksAndSleep()，但在我们进入第 35 行的临界区之前触发的中断可能会要求内核恢复另一个处于阻塞状态的线程的执行⁴⁶。通过调用 eTaskConfirmSleepModeStatus()，我们可以知道是否需要中止滴答抑制程序并恢复定时器。如果该函数返回 eAbortSleep 值，则我们重启滴答发生器定时器，并通过重新启用所有中断（第 45 行）立即退出临界区。相反，如果该函数返回 eNoTasksWaitingTimeout 值，这意味着没有运行中的线程，没有软件定时器⁴⁷，也没有其他带有确定超时的阻塞线程。由于在这种情况下无需保持滴答计数的准确性（没有定时器，没有运行中的线程，没有超时），我们可以进入停止模式（stop mode），这将导致定时器时钟被门控。当外部中断唤醒 MCU 时，MCU 将从 StopMode() 例程中退出。

相反，如果 eTaskConfirmSleepModeStatus() 函数返回 eStandardSleep 值，则第 53 行的 else 分支匹配，我们可以睡眠一段等于 xExpectedIdleTime 参数的时间，该参数对应于线程被移回就绪状态之前的总滴答周期数。因此，该参数值就是微控制器可以在暂时抑制滴答中断的情况下安全保持低功耗状态的时间。定时器中断服务程序（ISR）将唤醒 MCU，从 SleepMode() 例程中退出，并在第 74 行调整全局滴答计数。

#### 23.8.2.2 自定义无滴答模式策略

上述伪代码代表了一种所有程序员都可以用来实现其自定义无滴答模式的模式。例如，如果我们知道我们的软件不使用软件定时器，并且非无限超时，那么我们可以安全地仅处理深度睡眠模式的情况。

⁴⁶ 之所以会发生这种情况，是因为如前所述，该例程是在具有最低可能优先级的中断请求（IRQ）内调用的。因此，具有更高优先级的 IRQ 可能会恢复另一个阻塞任务的执行。⁴⁷ 请注意，仅仅在我们的代码中不使用定时器是不够的。FreeRTOSConfig.h 中的宏 configUSE_TIMERS 必须设置为 0，否则 eTaskConfirmSleepModeStatus() 永远不会返回 eNoTasksWaitingTimeout 值。

<!-- page: 683 -->

现在，我们将实现一个自定义无滴答模式策略，分析为在 STM32F030 MCU 上工作而编写的实际代码。对于其他 STM32 MCU，请参阅本书示例，尽管实现几乎相同。

**文件名：** `Core/Src/tickless-mode.c`

```c
12  #define ulPeriodValueForOneTick   ((1000000U / 1000U) - 1U)
13
14  /* Holds the maximum number of ticks that can be suppressed - which is
15   basically how far into the future an interrupt can be generated without
16   loosing the overflow event at all. It is set during initialization. */
17  static TickType_t xMaximumPossibleSuppressedTicks = 0;
18
19  /* Flag set from the tick interrupt to allow the sleep processing to know if
20   sleep mode was exited because of an tick interrupt or a different interrupt. */
21  static volatile uint8_t ucTickFlag = pdFALSE;
22
23  /* The HAL handler of the TIM2 timer */
24  TIM_HandleTypeDef htim2;
25
26  void xPortSysTickHandler( void );
27
28  /* The callback function called by the HAL when TIM2 overflows. */
29  void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim) {
30    if (htim->Instance == TIM2) {
31      xPortSysTickHandler();
32
33      /* In case this is the first tick since the MCU left a low power mode.
34       The period is so configured by vPortSuppressTicksAndSleep(). Here
35       the reload value is reset to its default. */
36      __HAL_TIM_SET_AUTORELOAD(htim, ulPeriodValueForOneTick);
37      __HAL_TIM_SET_COUNTER(htim, 0);
38
39      /* The CPU woke because of a tick. */
40      ucTickFlag = pdTRUE;
41    } else if (htim->Instance == TIM3) {
42        HAL_IncTick();
43    }
44  }
45  /*-----------------------------------------------------------*/
46
47  /* Override the default definition of vPortSetupTimerInterrupt() that is weakly
48   defined in the FreeRTOS Cortex-M0 port layer with a version that configures TIM2
49   to generate the tick interrupt. */
50  void vPortSetupTimerInterrupt(void) {
51    uint32_t              uwTimclock = 0;
52    uint32_t              uwPrescalerValue = 0;
53
54    /* Enable the TIM2 clock. */
55    __HAL_RCC_TIM2_CLK_ENABLE();
56
57    /* Ensure clock stops in debug mode. */
58    __HAL_DBGMCU_FREEZE_TIM2();
59
60    /* Compute TIM2 clock */
61    uwTimclock = 2*HAL_RCC_GetPCLK1Freq();
62    /* Compute the prescaler value to have TIM2 counter clock equal to 1MHz */
63    uwPrescalerValue = (uint32_t) ((uwTimclock / 1000000U) - 1U);
64
65    /* Configure the TIM2 timer */
66    htim2.Instance = TIM2;
67    htim2.Init.Period = ulPeriodValueForOneTick;
68    htim2.Init.Prescaler = uwPrescalerValue;
69    htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
70    HAL_TIM_Base_Init(&htim2);
71
72    /* Enable the TIM2 interrupt. This must execute at the lowest interrupt priority. */
73    HAL_NVIC_SetPriority(TIM2_IRQn, configLIBRARY_LOWEST_INTERRUPT_PRIORITY, 0);
74    HAL_NVIC_EnableIRQ(TIM2_IRQn);
75
76    HAL_TIM_Base_Start_IT(&htim2);
77    /* See the comments where xMaximumPossibleSuppressedTicks is declared. */
78    xMaximumPossibleSuppressedTicks = ((unsigned long) USHRT_MAX)
79        / ulPeriodValueForOneTick;
80  }
```

<!-- page: 684 -->

我们要分析的前两个函数与用作滴答生成器的定时器设置以及相关溢出中断的处理有关。prvSetupTimerInterrupt() 函数在调用 osKernelStart() 例程时由 FreeRTOS 自动调用。它配置 TIM2 定时器，使其每 1ms 到期一次。相应的中断被使能，并且中断服务程序（ISR）的优先级被设置为最低（请记住，除非另有需要，始终重要的是将定时器 ISR 设置为最低优先级）。HAL_TIM_PeriodElapsedCallback() 回调只是将全局滴答计数增加 1。不要担心第 [36:37] 行的指令，因为它们稍后会变得清晰。同一个回调还负责增加 HAL 滴答计数器（第 42 行）。

现在我们将分析最复杂的部分：vPortSuppressTicksAndSleep() 函数。我们将把它划分为若干代码块，以便更简单地分析其代码。强烈建议在 IDE 中随时保留并查看实际代码。

<!-- page: 685 -->

**文件名：** `Core/Src/tickless-mode.c`

```c
89  void vPortSuppressTicksAndSleep(TickType_t xExpectedIdleTime) {
90    uint32_t ulCounterValue, ulCompleteTickPeriods;
91    eSleepModeStatus eSleepAction;
92    TickType_t xModifiableIdleTime;
93    const TickType_t xRegulatorOffIdleTime = 50;
94
95    /* Make sure the TIM2 reload value does not overflow the counter. */
96    if (xExpectedIdleTime > xMaximumPossibleSuppressedTicks) {
97      xExpectedIdleTime = xMaximumPossibleSuppressedTicks;
98    }
99
100   /* Calculate the reload value required to wait xExpectedIdleTime tick
101    periods. */
102   ulCounterValue = ulPeriodValueForOneTick * xExpectedIdleTime;
103
104   /* To avoid race conditions, enter a critical section.  */
105   __disable_irq();
106
107   /* If a context switch is pending then abandon the low power entry as
108    the context switch might have been pended by an external interrupt that
109    requires processing. */
110   eSleepAction = eTaskConfirmSleepModeStatus();
111   if (eSleepAction == eAbortSleep) {
112     /* Re-enable interrupts. */
113     __enable_irq();
114     return;
115   } else if (eSleepAction == eNoTasksWaitingTimeout) {
116     /* Stop TIM2 */
117     HAL_TIM_Base_Stop_IT(&htim2);
118
119     /* A user definable macro that allows application code to be inserted
120      here.  Such application code can be used to minimize power consumption
121      further by turning off IO, peripheral clocks, the Flash, etc. */
122     configPRE_STOP_PROCESSING();
123
124
125     /* There are no running state tasks and no tasks that are blocked with a
126      time out.  Assuming the application does not care if the tick time slips
127      with respect to calendar time then enter a deep sleep that can only be
128      woken by (in this demo case) the user button being pushed on the
129      STM32L discovery board.  If the application does require the tick time
130      to keep better track of the calendar time then the RTC peripheral can be
131      used to make rough adjustments. */
132     HAL_PWR_EnterSTOPMode(PWR_MAINREGULATOR_ON, PWR_STOPENTRY_WFI);
133
134     /* A user definable macro that allows application code to be inserted
135      here.  Such application code can be used to reverse any actions taken
136      by the configPRE_STOP_PROCESSING().  In this demo
137      configPOST_STOP_PROCESSING() is used to re-initialize the clocks that
138      were turned off when STOP mode was entered. */
139      configPOST_STOP_PROCESSING();
140
141      /* Restart tick. */
142      HAL_TIM_Base_Start_IT(&htim2);
143
144      /* Re-enable interrupts. */
145      __enable_irq();
```

<!-- page: 686 -->

该函数首先检查预期的空闲时间，即我们可以安全停止滴答生成的时间窗口，是否小于 xMaximumPossibleSuppressedTicks：该值在 prvSetupTimerInterrupt() 例程中根据给定的 Prescaler 和 Period 值进行计算。然后，在第 102 行，它计算要使用的 Period 值，以便定时器在 xExpectedIdleTime 时间后溢出。为了避免竞态条件，我们随后进入临界区（第 105 行），并调用 eTaskConfirmSleepModeStatus() 以决定如何继续执行滴答抑制过程。如果该函数返回 eNoTasksWaitingTimeout，则我们可以完全停止 TIM2 定时器，并进入停止模式，直到 MCU 被事件或中断唤醒。

**文件名：** `Core/Src/tickless-mode.c`

```c
147   else {
148     /* Stop TIM2 momentarily.  The time TIM2 is stopped for is not accounted for
149      in this implementation (as it is in the generic implementation) because the
150      clock is so slow it is unlikely to be stopped for a complete count period
151      anyway. */
152     HAL_TIM_Base_Stop_IT(&htim2);
153
154     /* The tick flag is set to false before sleeping.  If it is true when sleep
155      mode is exited then sleep mode was probably exited because the tick was
156      suppressed for the entire xExpectedIdleTime period. */
157     ucTickFlag = pdFALSE;
158
159     /* Trap underflow before the next calculation. */
160     configASSERT(ulCounterValue >= __HAL_TIM_GET_COUNTER(&htim2));
161
162     /* Adjust the TIM2 value to take into account that the current time
163      slice is already partially complete. */
164     ulCounterValue -= (uint32_t) __HAL_TIM_GET_COUNTER(&htim2);
165
166     /* Trap overflow/underflow before the calculated value is written to TIM2. */
167     configASSERT(ulCounterValue < ( uint32_t ) USHRT_MAX);
168     configASSERT(ulCounterValue != 0);
169
170     /* Update to use the calculated overflow value. */
171     __HAL_TIM_SET_AUTORELOAD(&htim2, ulCounterValue);
172     __HAL_TIM_SET_COUNTER(&htim2, 0);
173
174     /* Restart the TIM2. */
175     HAL_TIM_Base_Start_IT(&htim2);
176
177     /* Allow the application to define some pre-sleep processing.  This is
178      the standard configPRE_SLEEP_PROCESSING() macro as described on the
179      FreeRTOS.org website. */
180     xModifiableIdleTime = xExpectedIdleTime;
181     configPRE_SLEEP_PROCESSING( xModifiableIdleTime );
182
183     /* xExpectedIdleTime being set to 0 by configPRE_SLEEP_PROCESSING()
184      means the application defined code has already executed the wait/sleep
185      instruction. */
186     if (xModifiableIdleTime > 0) {
187       /* The sleep mode used is dependent on the expected idle time
188        as the deeper the sleep the longer the wake up time.  See the
189        comments at the top of main_low_power.c.  Note xRegulatorOffIdleTime
190        is set purely for convenience of demonstration and is not intended
191        to be an optimized value. */
192     if (xModifiableIdleTime > xRegulatorOffIdleTime) {
193         /* A slightly lower power sleep mode with a longer wake up time. */
194         HAL_PWR_EnterSLEEPMode(PWR_LOWPOWERREGULATOR_ON, PWR_SLEEPENTRY_WFI);
195   }else{
196         /* A slightly higher power sleep mode with a faster wake up time. */
197       HAL_PWR_EnterSLEEPMode(PWR_MAINREGULATOR_ON, PWR_SLEEPENTRY_WFI);
198       }
199   }
```

<!-- page: 687 -->

如果 eTaskConfirmSleepModeStatus() 返回 eStandardSleep，那么我们可以进入睡眠模式。定时器被停止，并且其 Period（周期）被设置为之前计算出的值（在第 171 行，基于第 164 行的计算）。configPRE_SLEEP_PROCESSING() 是一个我们可以实现的宏，用于执行进入睡眠模式前的预备操作（例如，在某些 STM32 微控制器中，需要降低时钟速度，或者我们可以使用此宏来关闭不需要的外设）。因此，我们可以根据计算出的睡眠时间进入睡眠模式或低功耗睡眠模式（在某些 STM32 微控制器中，从低功耗睡眠模式退出需要更多时间，如果睡眠周期过短，这会无用地浪费大量电力）。

<!-- page: 688 -->

**文件名：** `Core/Src/tickless-mode.c`

```c
201     /* Allow the application to define some post sleep processing.  This is
202      the standard configPOST_SLEEP_PROCESSING() macro, as described on the
203      FreeRTOS.org website. */
204     configPOST_SLEEP_PROCESSING( xModifiableIdleTime );
205
206     /* Re-enable interrupts. If the timer has overflowed during this period
207      then this will cause that the TIM2_IRQHandler() is called. So the
208      global tick counter is incremented by 1 and the ulTickFlag variable
209      is set to pdTRUE.
210      Take note that in the STM32L example in the official FreeRTOS
211      distribution interrupts are re-enabled after the TIM2 is stopped.
212      This is wrong, because it causes that the IRQ is leaved pending,
213      even if has been set. So we must first re-enable interrupts - this
214      causes that a pending TIM2 IRQ fires - and then stop the timer. */
215     __enable_irq();
216
217     /* Stop TIM2.  Again, the time the clock is stopped for in not accounted
218      for here (as it would normally be) because the clock is so slow it is
219      unlikely it will be stopped for a complete count period anyway. */
220     HAL_TIM_Base_Stop_IT(&htim2);
221
222     if (ucTickFlag != pdFALSE) {
223       /* The MCU has been woken up by the TIM2. So we trap overflows
224        before the next calculation. */
225       configASSERT(
226           ulPeriodValueForOneTick >= (uint32_t ) __HAL_TIM_GET_COUNTER(&htim2));
227
228       /* The tick interrupt has already executed, although because this
229        function is called with the scheduler suspended the actual tick
230        processing will not occur until after this function has exited.
231        Reset the reload value with whatever remains of this tick period. */
232       ulCounterValue = ulPeriodValueForOneTick
233           - (uint32_t) __HAL_TIM_GET_COUNTER(&htim2);
234
235       /* Trap under/overflows before the calculated value is used. */
236       configASSERT(ulCounterValue <= ( uint32_t ) USHRT_MAX);
237       configASSERT(ulCounterValue != 0);
238
239       /* Use the calculated reload value. */
240       __HAL_TIM_SET_AUTORELOAD(&htim2, ulCounterValue);
241       __HAL_TIM_SET_COUNTER(&htim2, 0);
242
243       /* The tick interrupt handler will already have pended the tick
244        processing in the kernel.  As the pending tick will be processed as
245        soon as this function exits, the tick value  maintained by the tick
246        is stepped forward by one less than the  time spent sleeping.  The
247        actual stepping of the tick appears later in this function. */
248       ulCompleteTickPeriods = xExpectedIdleTime - 1UL;
249   }else{
250       /* Something other than the tick interrupt ended the sleep.  How
251        many complete tick periods passed while the processor was
252        sleeping? */
253       ulCompleteTickPeriods = ((uint32_t) __HAL_TIM_GET_COUNTER(&htim2))
254           / ulPeriodValueForOneTick;
255
256       /* Check for over/under flows before the following calculation. */
257       configASSERT(
258           ((uint32_t ) __HAL_TIM_GET_COUNTER(&htim2)) >= (ulCompleteTickPeriods * ulPeriodValu\eForOneTick));
260
261       /* The reload value is set to whatever fraction of a single tick
262        period remains. */
263       ulCounterValue = ((uint32_t) __HAL_TIM_GET_COUNTER(&htim2))
264           - (ulCompleteTickPeriods * ulPeriodValueForOneTick);
265       configASSERT(ulCounterValue <= ( uint32_t ) USHRT_MAX);
266       if (ulCounterValue == 0) {
267         /* There is no fraction remaining. */
268         ulCounterValue = ulPeriodValueForOneTick;
269         ulCompleteTickPeriods++;
270        }
271       __HAL_TIM_SET_AUTORELOAD(&htim2, ulCounterValue);
272       __HAL_TIM_SET_COUNTER(&htim2, 0);
273     }
274
275     /* Restart TIM2 so it runs up to the reload value.  The reload value
276      will get set to the value required to generate exactly one tick period
277      the next time the TIM2 interrupt executes. */
278     HAL_TIM_Base_Start_IT(&htim2);
279
280     /* Wind the tick forward by the number of tick periods that the CPU
281      remained in a low power state. */
282     vTaskStepTick(ulCompleteTickPeriods);
283   }
284 }
```

<!-- page: 689 -->

当微控制器从睡眠模式退出时，无论是由于定时器溢出还是产生了其他中断，configPOST_SLEEP_PROCESSING() 宏允许我们执行必要的操作，例如恢复某些外设或提高时钟速度。现在棘手的部分出现了，我们需要仔细解释所涉及的操作。

在微控制器（MCU）退出低功耗模式后，通过退出临界区（第 215 行）解除中断服务程序（ISR）的屏蔽。如果因定时器溢出而从睡眠模式退出，这将导致调用 TIM2_IRQHandler() ISR。当这种情况发生时，HAL_TIM_PeriodElapsedCallback()

<!-- page: 690 -->

函数被调用：这会导致 ucTickFlag 被设置为 TRUE，并且需要相应地设置定时器周期。相反，如果微控制器因其他原因（例如被 EXTI 中断唤醒）退出低功耗模式，则 ucTickFlag 等于 FALSE。

代码在第 222 行检查 ucTickFlag 的状态。如果它等于 TRUE，则全局滴答计数器增加一个等于 xExpectedIdleTime 减一的数值，因为滴答计数器已经由 HAL_TIM_TIM_PeriodElapsedCallback() 例程增加了一（一旦我们在第 215 行离开临界区，ISR 就会被调用）。相反，如果它等于 FALSE，则计算微控制器在睡眠模式下花费了多长时间，并相应地增加滴答计数器。

此策略可以根据您的实际需求进行调整。例如，如果您正在 STM32L 平台上工作，可以考虑在停止模式期间使用 LPTIM 定时器，以便您可以知道在停止模式期间经过了多少滴答（常规 STM32 定时器在停止模式下无法工作）。

> **关于 LPTIM 定时器的说明**
>
> 我花了很多时间尝试使用 LPTIM 定时器作为时基发生器。虽然它作为常规定时器工作得很好，但我得出的结论是 LPTIM 定时器不适合用于无滴答模式，因为它们的实现方式使得读取计数器寄存器（LPTIM->CNT）的值不可靠，尤其是在定时器从更深的低功耗模式退出时。这在官方 STM32 文档中明确说明，根据本作者的观点，这构成了该外设的一个严重限制。

## 23.9 调试功能

使用实时操作系统（RTOS）构建的固件的调试可能并不简单。上下文切换可能会使单步调试变得复杂。FreeRTOS 提供了一些调试功能，其中一些在您使用大量动态生成的线程时特别有用。

### 23.9.1 configASSERT() 宏
FreeRTOS 源代码中充满了 configASSERT() 宏的调用。这是一个空宏，开发人员可以在 FreeRTOSConfig.h 中定义它，它起着与 C assert() 函数相同的作用。CubeMX 自动为我们以如下方式定义它：

```c
#define configASSERT( x ) if ((x) == 0) {taskDISABLE_INTERRUPTS(); for( ;; );}
```

该宏的工作方式是，如果断言条件为假，则禁用所有中断（在 Cortex-M0/0+ 内核上通过设置 PRIMASK 寄存器，在其他 STM32 微控制器上通过提高 BASEPRI 值），并进入无限循环。虽然这种行为在调试会话期间是可以接受的，但如果我们的设备未在调试器下运行，它可能会成为许多麻烦的来源，因为很难说明固件为什么停止工作。因此，本作者更喜欢以另一种方式定义该宏：

<!-- page: 691 -->

```c
void __configASSERT(uint8_t x) {
  if ((x) == 0) {
      taskDISABLE_INTERRUPTS();
      if((CoreDebug->DHCSR & 0x1) == 0x1) { /* If under debug */
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
        HAL_Delay(1000);
        asm("BKTP #0");
   }else{
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
        HAL_Delay(100);
      }
  }
}
#define configASSERT( x ) __configASSERT(x)
```

__configASSERT() 函数使用 Cortex-M CoreDebug 接口检查微控制器是否处于调试状态：当微控制器处于调试状态时，调试器会设置调试保持控制和状态寄存器（DHCSR）的第一位。如果是这样，当断言条件为假时，会放置一个软件断点。然而，此函数有两个相关的限制：

- 它仅在基于 Cortex-M3/4/7 的微控制器上工作；
- 当发生系统复位时，DHCSR 寄存器不会重置为零，并且在固件内部也不可能清除第一位；这意味着我们需要完全关闭设备的电源，否则如果断言条件为假，固件将会卡住。

### 23.9.2 运行时统计和线程状态信息

当线程动态生成时，很难跟踪它们的生命周期。FreeRTOS 提供了一种方法来获取所有活动线程的完整列表以及有关其状态的一些相关信息。

uxTaskGetNumberOfTasks() 函数返回活动线程的数量。术语“活动线程”指的是内核实际分配的所有线程，即使那些被标记为已删除⁴⁸的线程也是如此。函数

```c
UBaseType_t uxTaskGetSystemState(TaskStatus_t * const pxTaskStatusArray,
            const UBaseType_t uxArraySize, unsigned long * const pulTotalRunTime );
```

返回系统中每个线程的状态信息，通过为每个线程填充一个 TaskStatus_t 结构体的实例。TaskStatus_t 结构体定义如下：

⁴⁸已删除的线程通常在内存中保留很短的时间。当线程被标记为删除时，它实际上会被空闲线程从系统中移除。

<!-- page: 692 -->

```c
typedef struct xTASK_STATUS {
  TaskHandle_t xHandle;          /* The handle of the thread to which the rest of the
                                    information in the structure relates */
  const char *pcTaskName;        /* A pointer to the thread's name */
  UBaseType_t xTaskNumber;       /* Corresponds to Thread ID */
  eTaskState eCurrentState;      /* The state in which the thread existed when the
                                    structure was populated */
  UBaseType_t uxCurrentPriority; /* The priority at which the thread was running */
  UBaseType_t uxBasePriority;    /* The priority to which the thread will return
                                    if the thread's current priority has been inherited
                                    to avoid unbounded priority inversion when obtaining
                                    a mutex. Only valid if configUSE_MUTEXES is defined
                                    as 1 in FreeRTOSConfig.h. */
  uint32_t ulRunTimeCounter;     /* The total run time allocated to the thread so far,
                                    as defined by the run time stats clock. */
  uint16_t usStackHighWaterMark; /* The minimum amount of stack space that has remained
                                    for the thread since the thread was created */
} TaskStatus_t;
```

uxTaskGetSystemState() 接受一个预分配的数组，其中包含每个线程的 TaskHandle_t 结构体实例，数组可以容纳的最大元素数量（uxArraySize），以及指向一个变量（pulTotalRunTime）的指针，该变量将包含自内核启动以来的总运行时间。事实上，FreeRTOS 可以选择性地收集每个线程使用的处理时间量的信息。必须通过在 FreeRTOSConfig.h 中定义 configGENERATE_RUN_TIME_STATS 宏来显式启用运行时统计。此外，此功能要求我们使用另一个不同于用于填充滴答计数器的定时器。这是因为运行时统计的时基需要比滴答中断具有更高的分辨率，否则统计可能过于不准确而无法真正有用。

如果线程函数设计良好，并且不使用忙等待循环，通常一个线程的持续时间小于滴答时间（等于 1ms），这代表了分配给线程的最大时间片。然而，运行时统计的工作方式是，在线程进入运行状态之前，保存用于统计的定时器的当前值。当线程退出运行状态时（无论是因为它让出控制权，还是其时间片时间结束），都会对之前保存的时间与当前时间进行比较。如果使用滴答定时器进行此操作，这个差值始终等于零。因此，建议将用于统计的时基发生器配置为比滴答中断快 10 到 100 倍。时基越快，统计越准确——但定时器值溢出的速度也越快。

当 `configGENERATE_RUN_TIME_STATS` 宏被设置为 1 时，我们需要提供两个额外的宏。第一个宏 `portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()` 用于设置运行时间统计所需的定时器。第二个宏 `portGET_RUN_TIME_COUNTER_VALUE()` 由 FreeRTOS 用于获取定时器计数器的累积值。由于该定时器需要高速运行，不建议为其设置中断服务程序（ISR）并在其溢出时增加一个全局变量：这会影响整体系统性能。在提供 32 位定时器的 STM32 微控制器中，使用其中一个定时器即可，将其周期（Period）设置为最大值（0xFFFFFFFF）。另一种替代方案，在 Cortex-M3/4/7 上，是使用 DWT 周期计数器，如第 11 章所述。以下代码展示了这两个宏的一种可能实现：

<!-- page: 693 -->

```c
#define portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()  \
  do {                                            \
    DWT->CTRL |= 1 ; /* enable the counter */     \
    DWT->CYCCNT = 0;                              \
  }while(0)
#define portGET_RUN_TIME_COUNTER_VALUE() DWT->CYCCNT
```

现在我们将分析一个完整的跟踪实现，该实现包含一个专用线程，当按下 Nucleo USER 按钮时，在 UART2 接口上打印统计信息。

**文件名：** `Core/Src/main-ex8.c`

```c
48  void threadsDumpThread(void *argument) {
49   TaskStatus_t *pxTaskStatusArray = NULL;
50   char *pcBuf = NULL;
51   char *pcStatus;
52   uint32_t ulTotalRuntime;
53
54    while(1) {
55      if(HAL_GPIO_ReadPin(B1_GPIO_Port, B1_Pin) == GPIO_PIN_RESET) {
56        /* Allocate the message buffer. */
57        pcBuf = pvPortMalloc(100 * sizeof(char));
58
59        /* Allocate an array index for each task. */
60        pxTaskStatusArray = pvPortMalloc( uxTaskGetNumberOfTasks() * sizeof( TaskStatus_t ) );
61
62        if( pcBuf != NULL && pxTaskStatusArray != NULL ) {
63          /* Generate the (binary) data. */
64          uxTaskGetSystemState( pxTaskStatusArray, uxTaskGetNumberOfTasks(), &ulTotalRuntime );
65
66          sprintf(pcBuf, "         LIST OF RUNNING THREADS(%lu)         \r\n--------------------\---------------------\r\n", uxTaskGetNumberOfTasks());
68          HAL_UART_Transmit(&huart2, (uint8_t*)pcBuf, strlen(pcBuf), HAL_MAX_DELAY);
69
70          for(uint16_t i = 0; i < uxTaskGetNumberOfTasks(); i++ )
71           {
72            sprintf(pcBuf, "Thread: %s\r\n", pxTaskStatusArray[i].pcTaskName);
73            HAL_UART_Transmit(&huart2, (uint8_t*)pcBuf, strlen(pcBuf), HAL_MAX_DELAY);
74
75            sprintf(pcBuf, "Thread ID: %lu\r\n", pxTaskStatusArray[i].xTaskNumber);
76            HAL_UART_Transmit(&huart2, (uint8_t*)pcBuf, strlen(pcBuf), HAL_MAX_DELAY);
77
78            switch (pxTaskStatusArray[i].eCurrentState) {
79            case eRunning:
80              pcStatus = "RUNNING";
81              break;
82            case eReady:
83              pcStatus = "READY";
84              break;
85            case eBlocked:
86              pcStatus = "BLOCKED";
87              break;
88            case eSuspended:
89              pcStatus = "SUSPENDED";
90              break;
91            case eDeleted:
92              pcStatus = "DELETED";
93              break;
94
95            default: /* Should not get here, but it is included
96                        to prevent static checking errors. */
97              pcStatus = "UNKNOWN";
98              break;
99             }
100
101           sprintf(pcBuf, "\tStatus: %s\r\n", pcStatus);
102           HAL_UART_Transmit(&huart2, (uint8_t*)pcBuf, strlen(pcBuf), HAL_MAX_DELAY);
103
104           sprintf(pcBuf, "\tStack watermark number: %d\r\n", pxTaskStatusArray[i].usStackHighW\aterMark);
106           HAL_UART_Transmit(&huart2, (uint8_t*)pcBuf, strlen(pcBuf), HAL_MAX_DELAY);
107
108           sprintf(pcBuf, "\tPriority: %lu\r\n", pxTaskStatusArray[i].uxCurrentPriority);
109           HAL_UART_Transmit(&huart2, (uint8_t*)pcBuf, strlen(pcBuf), HAL_MAX_DELAY);
110
111           sprintf(pcBuf, "\tRun-time time: %lu\r\n", pxTaskStatusArray[i].ulRunTimeCounter);
112           HAL_UART_Transmit(&huart2, (uint8_t*)pcBuf, strlen(pcBuf), HAL_MAX_DELAY);
113
114           float data = (float)(((float)pxTaskStatusArray[i].ulRunTimeCounter)/ulTotalRuntime)*\100;
116           sprintf(pcBuf, "\tRun-time time in percentage: %lu%%\r\n", (uint32_t)data);
117           HAL_UART_Transmit(&huart2, (uint8_t*)pcBuf, strlen(pcBuf), HAL_MAX_DELAY);
118          }
119
120         vPortFree(pcBuf);
121         vPortFree(pxTaskStatusArray);
122        }
123     }
124     osDelay(50);
125   }
126 }
```

<!-- page: 694 -->

<!-- page: 695 -->

这段代码应该很容易理解。当按下 USER 按钮时，该线程分配一个缓冲区（`pxTaskStatusArray`），其中将包含系统中每个线程的 `TaskStatus_t` 结构体。第 64 行的 `uxTaskGetSystemState()` 填充此数组，并且对于其中包含的每个线程，一些统计信息会打印在 Nucleo VCP 上。

虽然 `uxTaskGetSystemState()` 为系统中的每个线程填充一个 `TaskStatus_t` 结构体，但 `vTaskGetInfo()` 仅为单个任务填充一个 `TaskStatus_t` 结构体，如果我们想获取关于特定线程的信息，它可能很有用。

最后，FreeRTOS 提供了一些方便的例程，用于自动将原始数据统计数据格式化为人类可读（ASCII）格式。例如，`vTaskGetRunTimeStats()` 将 `uxTaskGetSystemState()` 生成的原始数据格式化为一个人类可读（ASCII）表格，显示每个任务在运行状态中花费的时间（每个任务消耗了多少 CPU 时间）。更多信息，请参阅在线 FreeRTOS 文档的此页面⁴⁹。

### 23.9.3 在 STM32CubeIDE 中调试 FreeRTOS

STM32CubeIDE 提供了一些高级调试功能，允许使用专用视图调试以下 FreeRTOS 对象：

- 任务
- 信号量
- 定时器
- 队列

要启用额外的调试视图，您可以从调试透视图中点击菜单 Window->Show View->FreeRTOS，如图 23.22 所示。

为了从正在运行的固件中收集信息，这些视图需要 FreeRTOS 提供一些支持。

- 需要定义宏 `configUSE_TRACE_FACILITY` 并将其设置为 1。这允许 FreeRTOS 任务列表视图收集有关线程堆栈状态的额外信息，如图 23.23 所示，并显示已定义信号量的完整列表。
- 固件需要调用 FreeRTOS 例程 `vQueueAddToRegistry(QueueHandle_t xQueue, const char *pcQueueName )` 函数，以使 FreeRTOS 队列和 FreeRTOS 信号量视图能够显示对象。该函数将对象添加到 FreeRTOS 队列注册表中，并接收两个参数，第一个是队列的句柄，第二个是队列的描述，该描述将在 FreeRTOS 相关视图中呈现。

⁴⁹http://www.freertos.org/rtos-run-time-stats.html

<!-- page: 696 -->

- 为了获取有效的 RTOS 运行时统计信息，应用程序必须设置运行时统计时间基准。建议时间基准时钟的运行速度至少是用于处理 RTOS 滴答中断的时钟频率的 10 倍。要启用 FreeRTOS 的运行时收集，您需要设置宏 `configGENERATE_RUN_TIME_STATS`、`portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()` 和 `portGET_RUN_TIME_COUNTER_VALUE()`。请参阅上一段以了解如何设置这些宏。

<p align="center"><img src="../images/page-0696-image-01.jpeg" alt="Image from PDF page 696"></p>

<p align="center">图 23.22：如何启用 FreeRTOS 专用调试视图</p>

<p align="center"><img src="../images/page-0696-image-02.jpeg" alt="Image from PDF page 696"></p>

<p align="center">表 23.3：FreeRTOS 任务列表视图中各列的描述</p>

**FreeRTOS 任务列表视图**

FreeRTOS 任务列表视图显示目标系统中所有可用任务的详细信息。每次目标执行暂停时，任务列表会自动更新。每种类型的任务参数对应一列，每个任务对应一行。如果自上次调试器暂停以来，某个任务的任何参数值发生了变化，则对应的行会以黄色高亮显示，如图 23.23 中的示例所示。出于性能原因，堆栈分析（Min Free Stack 列）默认是禁用的。要启用堆栈分析，请点击图 23.23 中红圈标出的 Toggle Stack Checking 按钮。当 FreeRTOS 配置为将 `configRECORD_STACK_HIGH_ADDRESS` 设置为 1 时，Min Free Stack 列会变为 Stack Usage：在这种情况下，它以详细格式显示堆栈使用情况，格式为 Used/Total(%Used)。FreeRTOS 任务列表视图中的列信息描述见表 23.3。

<!-- page: 697 -->

<p align="center"><img src="../images/page-0697-image-01.jpeg" alt="Image from PDF page 697"></p>

<p align="center">图 23.23：FreeRTOS 任务列表视图</p>

**FreeRTOS 定时器视图**

FreeRTOS 定时器视图显示目标系统中所有可用软件定时器的详细信息。每次目标执行暂停时，该视图会自动更新。每种类型的定时器参数对应一列，每个定时器对应一行。如果自上次调试器暂停以来，某个定时器的任何参数值发生了变化，则对应的行会以黄色高亮显示。FreeRTOS 定时器视图中的列信息描述见表 23.4。

<p align="center"><img src="../images/page-0697-image-02.jpeg" alt="Image from PDF page 697"></p>

<p align="center">表 23.4：FreeRTOS 定时器视图中各列的描述</p>

**FreeRTOS 信号量视图**

FreeRTOS 信号量视图显示目标系统中所有可用同步对象的详细信息，包括：

- 互斥锁
- 计数信号量
- 二进制信号量
- 递归信号量

每次目标执行暂停时，该视图会自动更新。每种类型的信号量参数对应一列，每个信号量对应一行。如果自上次调试器暂停以来，某个信号量的任何参数值发生了变化，则对应的行会以黄色高亮显示。FreeRTOS 信号量视图中的列信息描述见表 23.5。

<!-- page: 698 -->

<p align="center"><img src="../images/page-0698-image-01.jpeg" alt="Image from PDF page 698"></p>

<p align="center">表 23.5：FreeRTOS 信号量视图中各列的描述</p>

**FreeRTOS 队列视图**

FreeRTOS 队列视图显示目标系统中所有可用队列的详细信息。每次目标执行暂停时，该视图会自动更新。每种类型的队列参数对应一列，每个队列对应一行。如果自上次调试器暂停以来，某个队列的任何参数值发生了变化，则对应的行会以黄色高亮显示。FreeRTOS 队列视图中的列信息描述见表 23.6。

<p align="center"><img src="../images/page-0698-image-02.jpeg" alt="Image from PDF page 698"></p>

<p align="center">表 23.6：FreeRTOS 队列视图中各列的描述</p>

### 23.9.4 在 STM32CubeIDE 中进行 FreeRTOS 内核感知调试

FreeRTOS 内核感知调试（kernel-aware debugging）是 STM32CubeIDE 提供的一项重要功能，当固件架构需要在特定硬件和难以追踪的快速事件发生时动态生成多个线程时，该功能非常有用。当启用 FreeRTOS 内核感知调试并启动调试会话时，所有线程都会列在调试视图中，如图 23.24 所示。通过在调试视图中选择一个线程，可以在视图中可视化该线程的当前上下文。例如，变量（Variables）、寄存器（Registers）和编辑器（Editor）视图会反映活动的堆栈帧。

内核感知调试需要调试器的专门支持，并由 STM32CubeIDE 自动启动一个特殊的代理守护进程。要启用 FreeRTOS 内核感知调试，调试配置（Debug Configurations）对话框中的调试器（Debugger）选项卡包含用于启用 RTOS 代理的设置，如图 23.25 所示。勾选“启用 RTOS 代理”（Enable RTOS Proxy）复选框后，必须选择 FreeRTOS 的驱动程序以及对应目标 MCU 的 Cortex-M 内核。强烈建议将端口号保留为 60000。

<!-- page: 699 -->

<p align="center"><img src="../images/page-0699-image-01.jpeg" alt="Image from PDF page 699"></p>

<p align="center">图 23.24：</p>

在撰写本章时（2022 年 1 月），有一些重要的限制需要考虑：

- 当与 ST-LINK GDB 服务器一起使用时，必须禁用实时表达式（Live expressions）（见图 23.25）。
- 对于被换出的线程，寄存器视图的内容在某些寄存器上与活动的 CPU 上下文混合在一起（并非所有寄存器都由上下文切换器保存）。
- 寄存器视图中的浮点寄存器未正确更新。

<p align="center"><img src="../images/page-0699-image-02.jpeg" alt="Image from PDF page 699"></p>

<p align="center">图 23.25：</p>

<!-- page: 700 -->

> **Cortex-M4F 和 Cortex-M7 内核中的 FPU 支持**
>
> Cortex-M4F 或 Cortex-M7 架构提供了专用的浮点单元（FPU），允许直接在硬件中处理浮点运算，而无需使用 C 运行时库提供的专用且必然较慢的函数。配备 FPU 单元的处理器实现了额外的硬件寄存器，这些寄存器需要在上下文切换操作期间保存。因此，针对 M4F/7 架构的 FreeRTOS GCC 移植版本期望 FPU 是启用的，而默认情况下它是禁用的。
>
> 要启用它，请进入项目设置（Project Settings）-> C/C++ 构建（C/C++ Build）-> 设置（Settings）-> MCU 设置（MCU Settings）部分，并在浮点单元（Floating-point unit）字段中选择 FPv4-SP-D16 条目（如果您拥有基于 Cortex-M7 的微控制器，则选择 FPv5-SP-D16⁵⁰），并在浮点 ABI（Float-point ABI）字段中选择硬件实现（Hardware implementation）。如果您正在处理较新的 STM32F76xx/STM32H7xx MCU，它们提供双精度 FPU 单元，则必须选择 FPv5-D16 条目。现在您需要重新构建整个源代码树。
>
> 然而，需要在 FreeRTOS 中显式启用对 FPU 的支持，方法是将 Core/Src/FreeRTOSConfig.h 文件中的宏 configENABLE_FPU 设置为 1。

## 23.10 FreeRTOS 的替代方案

正如本书引言中所述，市场上有几种不错的 FreeRTOS 替代方案。在这里，您将找到一些关于可用于 STM32 平台的其他优秀实时操作系统（RTOS）的介绍。

### 23.10.1 AzureRTOS

### 23.10.2 ChibiOS

如果您不是 STM32 平台的新手，您可能已经知道 ChibiOS⁵¹。ChibiOS 是一个独立的开源项目，由 STMicroelectronics 工程师 Giovanni Di Sirio 发起，他在 ST 位于意大利那不勒斯的站点工作。ChibiOS 在 STM32 社区中相当流行，因为 Giovanni 对 STM32 平台有深入的了解，这使他能够创建可能是针对 STM32 MCU 最优化的解决方案之一。然而，ChibiOS 被设计为可以在除 STM32 之外的任何 MCU 架构上运行。

ChibiOS 基本上由两层组成：内核（名为 ChibiOS/RT 或 ChibiOS/NIL）和一个完整的硬件抽象层（HAL，名为 Chibios/HAL），后者允许从底层硬件特性中抽象出来。虽然完全可以将官方 ST CubeHAL 与 ChibiOS/RT/NIL 内核混合使用，但对于受支持的外设而言，ChibiOS/HAL 可能是编程 STM32 设备的更简单解决方案。尽管作者没有直接经验，但 ChibiOS 在作者认识的许多人以及本书的一些读者中享有良好的声誉。此外，您可以在网络上找到许多基于此 RTOS 及其相关 HAL 的项目和优质教程⁵²。Chibios 使用完全静态内存分配模型，允许在禁止动态分配的应用领域中使用它。最后，Giovanni 还提供了一个预配置的 Eclipse 版本，名为 ChibiStudio，它附带所有必需的工具（GCC 工具链、OpenOCD 等），并且已经预配置好。在撰写本章时，它仅在 Windows 和 Linux 操作系统上运行。

ChibiOS 使用混合许可模型⁵³。ChibiOS RT 和 NIL 内核根据 GPL 3 许可证分发，HAL 根据更宽松的 Apache 2.0 许可证分发。GPL 3 阻止在出售电子设备时如果不公开发布固件源代码就使用该软件。存在一种“免费商业许可证”，可移除商业用户的 GPL 3。此许可证需要注册过程，并且对 500 个 MCU 内核有效。免费许可证可以通过重新提交请求表单以额外 500 个内核无限期续期。

⁵⁰FPv4-SP-D16 表示 MCU 实现了符合 VFPv4-D16 架构的浮点单元，单精度（SP），而 FPv5-SP-D16 指 VFPv5-D16 架构，单精度（SP）。 ⁵¹http://www.chibios.org/

<!-- page: 701 -->

### 23.10.3 Contiki 操作系统

Contiki⁵⁴ 是另一个开源实时操作系统（RTOS），其重点在于无线低功耗传感器和物联网（IoT）设备。该项目由 Adam Dunkels 于 2003 年发起，目前由包括德州仪器（Texas Instruments）和 Atmel 在内的多家大型公司支持。它在 TI 的 CC2xxx 系列设备中非常流行。它基于内核调度器和一个专为低资源设备设计的独立 TCP/IP 协议栈，提供 IPv4 网络功能、uIPv6 协议栈以及 Rime 协议栈。Rime 协议栈是一组专为低功耗无线网络设计的自定义轻量级网络协议。IPv6 协议栈由思科（Cisco）贡献，在发布时是获得 IPv6 Ready 认证的最小 IPv6 协议栈。该 IPv6 协议栈还包含用于低功耗有损 IPv6 网络的低功耗有损网络路由协议（RPL）路由协议，以及用于 IEEE 802.15.4 链路的 6LoWPAN 头部压缩和适配层。

ST 提供了一份应用笔记 UM2000⁵⁵，描述了如何在 ST 的微控制器上结合 SPIRIT 收发器启动 Contiki 操作系统，以开发亚 1GHz 无线设备。

Contiki 采用 BSD 风格许可证分发，允许在商业应用中使用其源代码，且不受任何形式限制。

### 23.10.4 OpenRTOS

OpenRTOS 是本章中描述的 FreeRTOS 的商业版本，并得到 ST 的官方支持。OpenRTOS 和 FreeRTOS 共享相同的代码库。OpenRTOS 为 FreeRTOS 用户提供的额外价值是一个“商业和法律包装”。

开发者升级到 OpenRTOS 许可证主要有两个原因：能够销售其设备和/或分发衍生代码而无需公开共享源代码，以及获得专门的支持以开发基于 OpenRTOS 的定制解决方案。对于大型公司而言，获得付费支持的可能性非常重要。

⁵²http://www.playembedded.org/ ⁵³https://bit.ly/3fT572c ⁵⁴http://www.contiki-os.org/ ⁵⁵https://bit.ly/1URnLZc

<!-- page: 702 -->
