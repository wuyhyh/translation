<!-- page: 194 -->

### 7.4.2 Cortex-M3/4/7/33

Interrupt priority mechanism in Cortex-M3/4/7/33 is more advanced than the one available in Cortex-M0/0+ based microcontrollers. Developers have a higher degree of flexibility, and this is often source of several headaches for novices. Moreover, the way interrupt priority is presented both in the ARM and ST documentation is a little bit counterintuitive.

In Cortex-M3/4/7/33 cores the priority of each interrupt is defined through the IPR register. This is an 8bit register in the ARMv7-M core architecture that allows up to 255 different priority levels. However, in practice, STM32 MCUs implementing Cortex-M3/4/7 cores use only the four upper bits of this register, while STM32 MCUs based on Cortex-M33 cores use only three upper bits.

![Image from PDF page 194](../images/page-0194-image-01.png)

Figure 7.15: The content of IPR register on an STM32 MCU based on Cortex-M3/4/7 core

Figure 7.15 clearly shows how the content of IPR is interpreted. This means that we have the only sixteen maximum priority levels: 0x00, 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80, 0x90, 0xA0, 0xB0, 0xC0, 0xD0, 0xE0, 0xF0. The lower this number is, the higher the priority is. That is, an IRQ having a priority equal to 0x10 has a higher priority than an IRQ with a priority level equal to 0xA0. If two interrupts fire at the same time, the one with the higher priority will be served first. If the processor is already servicing an interrupt and a higher priority interrupts fires, then the current interrupt is suspended, and the control passes to the higher priority interrupt. When this is completed, the execution goes back to the previous interrupt, if no other interrupts with higher priority occurs in the meantime.

So far, the mechanism is substantially the same of Cortex-M0/0+. The complication arises from the fact that the IPR register can be logically subdivided in two parts: a series of bits defining the preemption priority¹³ and a series of bits defining the sub-priority. The first priority level rules the preemption priorities between ISRs. If an ISR has a priority higher than another one, it will preempt the execution of the lower priority ISR in case it fires. The sub-priority determines what ISR will be executed first, in case of multiple pending ISR, but it will not act on ISR preemption.

¹³What complicates the understanding of interrupt priorities is the fact that in the official documentation sometimes the preemption priority is also called group priority. This leads to a lot of confusion, since novices tends to imagine that these bits define a sort of Access Control List (ACL) privileges. Here, to simplify the understanding of this matter, we will only speak about preemption priority level.

<!-- page: 195 -->

![Image from PDF page 195](../images/page-0195-image-01.png)

Figure 7.16: Preemption of interrupts in case of concurrent execution

Figure 7.16 shows an example of interrupt preemption. A is an IRQ with the lowest priority that fires at time t0. The ISR starts the execution but the IRQ B, which has a higher priority (lower priority level), fires at time t1and the execution of A ISR is stopped. After a while, C IRQ fires at time t2 and the B ISR is stopped and the C ISR starts execution. When this finishes, the execution of B ISR is resumed until it finishes. When this happens, the execution of A ISR is resumed. This “nested” mechanism induced by interrupt priorities leads to the name of the NVIC controller, which is Nested Vectored Interrupt Controller.

![Image from PDF page 195](../images/page-0195-image-02.png)

Figure 7.17: If two interrupts with the same priority are pending, the one with the higher sub-priority is executed first

Figure 7.17 shows how the sub-priority affects the execution of multiple pending ISRs. Here we have three interrupts, all with the same maximum priority. At time t0 the IRQ A fires and it is serviced immediately. At the time t1 B IRQ fires, but since it has the same priority level of other IRQs, it is leaved in pending state. At time t2 also C IRQ fires, but for the same reason as before it is leaved in pending state by the processor. When The A ISR finishes, the C IRQ is served first, since it has a higher sub-priority than B. Only when the C ISR finishes the B IRQ can be served.

The way how IPR bits are logically subdivided is defined by the SCB->AIRCR register (a sub-group of bits of the System Control Block (SCB) register), and it is important to stress right from the start that this way to interpret the content of the IPR register is global to all ISRs. Once we have defined a priority scheme (also called priority grouping in the HAL), this is common to all interrupts used in the system.

<!-- page: 196 -->

![Image from PDF page 196](../images/page-0196-image-01.png)

Figure 7.18: The subdivision of IPR bits between preemption priority and sub-priority

Figure 7.18 shows all five possible subdivisions of IPR register, while Table 2 shows the maximum number of preemption priority levels and sub-priority levels that each subdivision scheme allows¹⁴.

Table 2: The number of preemption priority level available based on the current priority grouping schema

NVIC Priority Group Number of preemption priority levels Number of sub-priority levels

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

The CubeHAL provides the following function to assign a priority to an IRQ:

```text
void HAL_NVIC_SetPriority(IRQn_Type IRQn, uint32_t PreemptPriority, uint32_t SubPriority);
```

The HAL library is designed so that the PreemptPriority and SubPriority can be configured with a priority level number ranging from 0 to 16. The value is internally shifted to the most significant bits automatically. This simplifies the porting of code to other MCU with a different number of priority bits (this is the reason why only the left part of IPR register is used by silicon vendors).

Instead, to define the priority grouping, that is how to subdivide the IPR register between the preemption priority and sub-priority, the following function can be used:

¹⁴As stated before, the STM32 MCUs based on Cortex-M33 cores use just the three upper bits of the IPR register. This means that there is a maximum of eight priority level and three priority groups. Thus, NVIC_PRIORITYGROUP_4 is not available at all.

<!-- page: 197 -->

```text
void HAL_NVIC_SetPriorityGrouping(uint32_t PriorityGroup);
```
