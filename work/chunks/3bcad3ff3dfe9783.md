<!-- page: 491 -->

### 19.2.1 Entering/exiting sleep modes

As said in the previous paragraph, the CPU enters in sleep mode exclusively on a voluntary basis, by using specific ARM assembly instructions. This means that, as programmers, we have all the responsibility of the power consumption of devices we make⁶.

Cortex-M based MCUs offer two instructions to place the MCU in sleep mode: WFI and WFE. The Wait For Interrupt (WFI) instruction is also called the un-conditional sleep instruction. When the CPU executes that instruction, it immediately halts the core execution. The CPU will be resumed only by an interrupt request, depending on the interrupt priority and the effective sleep level (more about this later), or in case of debug events. If an interrupt is pending while the MCU executes the WFI instruction, it enters in sleep mode and wakes up again immediately.

The Wait For Event (WFE) is the other instruction that allows to place the MCU in sleep mode. It differs from the WFI since it checks the status of a particular event register⁷ before it halts the core: if this register is set, the WFE clears it and does not halt the CPU, continuing the program execution (this allows us to manage the pending event, if needed). Otherwise, it halts the MCU until this event register is set again.

But what is exactly the difference between an event and an interrupt? Events are a source of confusion in the STM32 world (also in the Cortex-M world in general). They appear like something intangible, compared to the interrupts that we have learned to handle in Chapter 7. Before we clarify what we mean with the term events, we need to better explain the role of the EXTI controller in an STM32 MCU. The Extended Interrupts and Events Controller (EXTI) is the hardware component internal to the MCU that manages the external and internal asynchronous interrupts/events and generates the event request to the CPU/NVIC controller and a wake-up request to the Power Controller (see Figure 19.2). The EXTI allows the management of several event lines, which can wake up the MCU from some sleep modes (not all events can wake up MCU). The lines are either configurable or direct and hence hardwired inside the MCU:

- The lines are configurable: the active edge can be chosen independently, and a status flag indicates the source of the interrupt. The configurable lines are used by the I/Os external interrupts, and by few peripherals (more about this soon).
- The lines are direct and hardwired: they are used by some peripherals to generate a wakeup from stop event or interrupt. The status flag is provided by the peripheral itself. For example, the RTC can be used to generate an event to wake up the MCU.

⁶Clearly, we are talking about the power consumption of the MCU core and all integrated peripherals. The power consumption of the overall board is determined by other things that we will not address here. ⁷This register is internal to the core and not accessible to the user.

<!-- page: 492 -->

![Image from PDF page 492](../images/page-0492-image-01.jpeg)

Figure 19.2: How events can be used to wake-up the core

Another important aspect to clarify about EXTI and NVIC controllers is that each line can be masked independently for an interrupt or an event generation. For example, in Chapter 6 we have seen that a GPIO can be configured to work in GPIO_MODE_EVT_* mode, which is different from the GPIO_- MODE_IT_* mode: in the first case, when an I/O is triggered it will not generate an IRQ request, but it will set the event flag. This will cause the MCU to wake up if it has entered a low-power mode using the WFE instruction.

So, the WFE instruction checks that no event is pending, and for this reason it is also called the conditional sleep instruction. This event register can be set by:

- exception entrance and exit;
- when SEV-On-Pend feature is enabled, the event register can be set when an interrupt pending status is changed from 0 to 1 (more about this soon);
- a peripheral sets its dedicated event line (this is peripheral-specific);
- execution of the SEV (Send Event) instruction;
- debug event (e.g., halting request).

In Chapter 7 we have seen that in Cortex-M3/4/7/33 cores we can temporarily mask the execution of those interrupts having a priority lower than a value set in the BASEPRI register. However, these interrupts are still enabled and marked as pending if they fire. We can configure the MCU to set the event register in case of pending interrupts, by setting the SCR->SEVONPEND bit. As the name suggest, this register will cause to “set the event register if interrupts are pending”. This means that, if the processor was placed in sleep mode by the WFE instruction, the CPU is immediately awakened, and we can eventually process pending interrupts. Instead, the WFI instruction would never wake up the core. The Cube HAL provides two convenient functions, HAL_PWR_EnableSEVOnPend() and HAL_PWR_DisableSEVOnPend(), to perform this setting.

<!-- page: 493 -->

If, instead, interrupts are masked by setting the PRIMASK register, a pending interrupt can wake up the processor, regardless for the sleep instruction used (WFI or WFE): this characteristic allows some parts of the MCU to be turned OFF by software by gating its clock, and the software can turn it back on after waking up before executing the ISR.

So, to recap, the WFI and WFE have the same following behaviour:

- wake up on interrupt/exception requests that are enabled and with higher priority than current level⁸;
- can be woken up by debug events;
- can be used to produce both sleep and deep sleep modes (more about this soon).

Instead, the WFI and WFE differ for the following reasons:

- execution of WFE does not enter sleep mode if the internal event register is set, while the execution of WFI always results in sleep;
- new pending of a disabled or masked interrupt can wake up the processor from WFE if SEVONPEND is set;
- WFE can be woken up by en external event;
- WFI can be woken up by an enabled interrupt when PRIMASK is set.
