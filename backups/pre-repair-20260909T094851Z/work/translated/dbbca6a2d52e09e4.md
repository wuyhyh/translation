<!-- page: 194 -->

### 7.4.2 Cortex-M3/4/7/33

Cortex-M3/4/7/33 中的中断优先级机制比基于 Cortex-M0/0+ 内核的微控制器（microcontroller）中的机制更为先进。开发人员拥有更高的灵活性，但这往往也是新手感到头疼的根源之一。此外，ARM 和 ST 文档中呈现中断优先级的方式略显反直觉。

在 Cortex-M3/4/7/33 内核中，每个中断的优先级是通过 IPR 寄存器（register）定义的。在 ARMv7-M 内核架构中，这是一个 8 位寄存器，允许多达 255 个不同的优先级级别。然而，在实际应用中，实现 Cortex-M3/4/7 内核的 STM32 MCU 仅使用该寄存器的最高四位，而基于 Cortex-M33 内核的 STM32 MCU 仅使用最高三位。

![Image from PDF page 194](../images/page-0194-image-01.png)

图 7.15：基于 Cortex-M3/4/7 内核的 STM32 MCU 上 IPR 寄存器的内容

图 7.15 清楚地展示了 IPR 内容的解释方式。这意味着我们最多只有十六个优先级级别：0x00, 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80, 0x90, 0xA0, 0xB0, 0xC0, 0xD0, 0xE0, 0xF0。数值越低，优先级越高。也就是说，优先级为 0x10 的 IRQ 比优先级级别为 0xA0 的 IRQ 具有更高的优先级。如果两个中断同时触发，优先级较高的那个将首先得到服务。如果处理器正在服务一个中断，而一个更高优先级的中断触发，则当前中断将被挂起，控制权传递给更高优先级的中断。当该中断完成后，执行返回到之前的中断，除非在此期间没有其他更高优先级的中断发生。

到目前为止，该机制与 Cortex-M0/0+ 基本相同。复杂性源于 IPR 寄存器可以在逻辑上细分为两部分：一组定义抢占优先级（preemption priority）¹³ 的位和一组定义子优先级（sub-priority）的位。第一个优先级级别决定了 ISR 之间的抢占优先级。如果一个 ISR 的优先级高于另一个 ISR，当它触发时，它将抢占较低优先级 ISR 的执行。子优先级决定了在多个 ISR 处于挂起状态时，哪个 ISR 将首先执行，但它不会影响 ISR 的抢占。

¹³使中断优先级理解复杂化的事实是，在官方文档中，抢占优先级有时也被称为组优先级（group priority）。这导致了很多混淆，因为新手倾向于认为这些位定义了某种访问控制列表（ACL）权限。在这里，为了简化对此问题的理解，我们只讨论抢占优先级级别。

<!-- page: 195 -->

![Image from PDF page 195](../images/page-0195-image-01.png)

图 7.16：并发执行情况下的中断抢占

图 7.16 展示了中断抢占的一个示例。A 是一个在时间 t0 触发的最低优先级的 IRQ。ISR 开始执行，但具有更高优先级（更低优先级级别）的 IRQ B 在时间 t1 触发，A ISR 的执行停止。过了一会儿，C IRQ 在时间 t2 触发，B ISR 停止，C ISR 开始执行。当 C 完成后，B ISR 的执行恢复，直到它完成。当这种情况发生时，A ISR 的执行恢复。这种由中断优先级引起的“嵌套”机制导致了 NVIC 控制器的名称，即嵌套向量中断控制器（Nested Vectored Interrupt Controller）。

![Image from PDF page 195](../images/page-0195-image-02.png)

图 7.17：如果两个具有相同优先级的中断处于挂起状态，具有更高子优先级的中断将首先执行

图 7.17 展示了子优先级如何影响多个挂起 ISR 的执行。这里我们有三个中断，都具有相同的最高优先级。在时间 t0，IRQ A 触发并立即得到服务。在时间 t1，B IRQ 触发，但由于它具有与其他 IRQ 相同的优先级级别，它被保留在挂起状态。在时间 t2，C IRQ 也触发，但由于与之前相同的原因，它也被处理器保留在挂起状态。当 A ISR 完成时，C IRQ 首先得到服务，因为它的子优先级高于 B。只有当 C ISR 完成后，B IRQ 才能得到服务。

IPR 位逻辑细分的方式由 SCB->AIRCR 寄存器（系统控制块（SCB）寄存器的一组子位）定义，并且从一开始就强调，解释 IPR 寄存器内容的方式对所有 ISR 都是全局的。一旦我们定义了优先级方案（在 HAL 中也称为优先级分组），该方案对系统中使用的所有中断都是通用的。

<!-- page: 196 -->

![Image from PDF page 196](../images/page-0196-image-01.png)

图 7.18：IPR 位在抢占优先级和子优先级之间的细分

图 7.18 展示了 IPR 寄存器的所有五种可能细分方式，而表 2 展示了每种细分方案允许的最大抢占优先级级别数和子优先级级别数¹⁴。

表 2：基于当前优先级分组方案可用的抢占优先级级别数

NVIC 优先级组 抢占优先级级别数 子优先级级别数

```text
NVIC_PRIORITYGROUP_0
0
16
NVIC_PRIORITYGROUP_1
2
8
NVIC_PRIORITYGROUP_2
4
4
NVIC_PRIORITYGROUP_3
8
2
NVIC_PRIORITYGROUP_4
16
0
```

CubeHAL 提供了以下函数来为 IRQ 分配优先级：

```text
void HAL_NVIC_SetPriority(IRQn_Type IRQn, uint32_t PreemptPriority, uint32_t SubPriority);
```

HAL 库的设计使得 PreemptPriority 和 SubPriority 可以配置为 0 到 16 之间的优先级级别编号。该值会自动内部移位到最高有效位。这简化了代码移植到其他具有不同优先级位数的 MCU（这就是为什么硅厂商仅使用 IPR 寄存器的左侧部分的原因）。

相反，要定义优先级分组，即如何在抢占优先级和子优先级之间细分 IPR 寄存器，可以使用以下函数：

¹⁴如前所述，基于 Cortex-M33 内核的 STM32 MCU 仅使用 IPR 寄存器的最高三位。这意味着最多有八个优先级级别和三个优先级组。因此，NVIC_PRIORITYGROUP_4 完全不可用。

<!-- page: 197 -->

```text
void HAL_NVIC_SetPriorityGrouping(uint32_t PriorityGroup);
```
