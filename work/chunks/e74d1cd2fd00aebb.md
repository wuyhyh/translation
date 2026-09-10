<!-- page: 173 -->

# 7. Interrupts Management

Hardware management is all about dealing with asynchronous events. The most of these come from hardware peripherals. For example, a timer reaching a configured period value, or a UART that warns about the arrival of data. Others are originated by the “world outside” our board. For example, the user presses that damned switch that causes your board to hang, and you are going to spend a whole day understanding what is going wrong.

All microcontrollers provide a feature called interrupts. An interrupt is an asynchronous event that causes stopping the execution of the current code on a priority basis (the more important the interrupt is, the higher its priority; this will cause that a lower-priority interrupt is suspended). The code that services the interrupt is called Interrupt Service Routine (ISR).

Interrupts are a source of multiprogramming: the hardware knows about them and it is responsible of saving the current execution context (that is, the stack frame, the current Program Counter (PC) and few other things) before switching to the ISR. Interrupts are exploited by Real Time Operating Systems (RTOS) to introduce the notion of tasks: without the help by the hardware it is impossible to have a true preemptive system, which allows switching between several execution contexts without irreparably losing the current execution flow.

Interrupts can originate both by the hardware and the software itself. ARM architecture distinguishes between the two types: interrupts originate by the hardware, exceptions by the software (e.g., an access to invalid memory location). In ARM terminology, an interrupt is a type of exception.

Cortex-M processors provide a unit dedicated to exceptions management. This is called Nested Vectored Interrupt Controller (NVIC) and this chapter is about programming this fundamental hardware component. However, here we will deal only with interrupts management. Exceptions handling will be treated in Chapter 24 about advanced debugging.

## 7.1 NVIC Controller

NVIC is a dedicated hardware unit inside the Cortex-M based microcontrollers that is responsible of the exceptions handling. Figure 7.1 shows the relation between the NVIC unit, the Processor Core and peripherals. Here we have to distinguish two types of peripherals: those external to the Cortex- M core, but internal to the STM32 MCU (e.g., timers, UARTS, and so on), and those peripherals external to the MCU at all. The source of the interrupts coming from the last kind of peripherals are the MCU I/O, which can be both configured as general purpose I/O (e.g., a tactile switch connected to a pin configured as input) or to drive an external advanced peripheral (e.g., I/Os configured to exchange data with an ethernet phyther through the RMII interface). A dedicated programmable controller, named External Interrupt/Event Controller (EXTI), is responsible of the interconnection between the external I/O signals and the NVIC controller, as we will see next.

<!-- page: 174 -->

![Image from PDF page 174](../images/page-0174-image-01.png)

Figure 7.1: the relation between the NVIC controller, the Cortex-M core and the STM32 peripherals

As stated before, ARM distinguishes between system exceptions, which originate inside the CPU core, and hardware exceptions coming from external peripherals, also called Interrupt Requests (IRQ). Programmers manage exceptions using specific ISRs, which are coded at higher level (most often using C language). The processor knows where to locate these routines thanks to an indirect table containing the addresses in memory of Interrupt Service Routines. This table is commonly called vector table, and every STM32 microcontrollers defines its own. Let us analyze this in depth.

### 7.1.1 Vector Table in STM32

All Cortex-M processors reserve a fixed set of fifteen exceptions common to all Cortex-M families. However, not all these exceptions are currently defined (they are marked as RESERVED in the ARM official documentation) and just a subset is available in Cortex-M0/0+ cores. We already encountered them in Chapter 1. Here, you can find the same table (Table 7.1) for your convenience. It is a good idea to take a quick look at these exceptions (we will study fault exceptions better in Chapter 24 dedicated to advanced debugging).

- Reset: this exception is raised just after the CPU resets. Its handler is the real entry point of the running firmware. In an STM32 application all starts from this exception. The handler contains some assembly-coded functions designed to initialize the execution environment, such as the main stack, the .bss area, etc. Chapter 22 dedicated to the booting process will explain in depth.
- NMI: this is a special exception, which has the highest priority after the Reset one. Like the Reset exception, it cannot be masked, and it can be associated to critical and non-deferrable activities. In all STM32 microcontrollers it is linked to the Clock Security System (CSS). CSS is a self- diagnostic peripheral that detects the failure of the external clock, called HSE. If this happens, HSE is automatically disabled (this means that the internal HSI is automatically enabled) and an NMI interrupt is raised to inform the software that something is wrong with the HSE. More about this feature in Chapter 10.
- Hard Fault: is the generic fault exception, and hence related to software interrupts. When the other fault exceptions are disabled, it acts as a collector for all types of exceptions (e.g., a

<!-- page: 175 -->
