<!-- page: 588 -->

# 22. 启动过程

在第 20 章中，我们已经看到，复位（Reset）异常的处理程序对应于 CPU 启动时执行的第一例程。基于 Cortex-M 的处理器采用固定的内存布局模型，该模型规定复位异常处理程序在内存中的地址紧随主堆栈指针（Main Stack Pointer, MSP）之后，即位于地址 0x0000 0004。该内存位置通常对应于闪存（flash memory）的起始位置。然而，芯片供应商可以通过一种称为物理重映射（physical remapping）的操作，将其他内存“别名”（aliasing）到 0x0000 0000 地址，从而绕过这一限制。此操作在硬件层面经过几个时钟周期后执行，它与第 20 章中看到的向量表重定位不同，后者是由在 MCU 上运行的代码执行的。

此外，STM32 平台提供了一个出厂预编程的引导加载程序（boot loader），可用于从多个来源将固件加载到闪存中。根据所使用的 STM32 系列和销售类型，STM32 微控制器可以使用 USART、USB、CAN、I²C 和 SPI 通信外设来加载代码。引导加载程序是通过特定的启动引脚（boot pins）进行选择的。

本章通过展示 STM32 微控制器在系统复位后执行的启动过程，对第 20 章的内容进行了补充。它详细描述了引导（bootstrap）过程中涉及的步骤，并简要介绍了如何在所有 STM32 微控制器中使用出厂预编程的引导加载程序。最后，还展示了一个自定义引导加载程序，它允许使用 USART 接口和自定义上传过程来升级板载固件。

## 22.1 Cortex-M 统一内存布局与启动过程

与更先进的微处理器架构（如 ARM Cortex-A）不同，Cortex-M 微控制器不提供内存管理单元（Memory Management Unit, MMU），MMU 允许将逻辑地址别名到实际的物理地址。这意味着，从 Cortex-M 内核的角度来看，内存映射在所有实现中都是固定且标准化的。

在基于 Cortex-M 的微控制器中，代码区域从地址 0x0000 0000 开始（在 Cortex-M3/4/7 中通过 I-Bus/D-Bus¹ 总线访问，在 Cortex-M0/0+ 中通过 S-Bus 访问），而数据区域（SRAM）从地址 0x2000 0000 开始（通过 S-Bus 访问）。Cortex-M CPU 始终从 I-Bus 获取向量表，这意味着它们仅从代码区域（通常对应于闪存）启动。

STM32 微控制器实现了一种称为物理重映射的特殊机制，用于从闪存以外的其他内存启动，该机制包括采样两个专用的 MCU 引脚，称为 BOOT0 和

¹有关这些总线的更多信息，请参阅第 9 章。

<!-- page: 589 -->

BOOT1²。这些引脚的电状态确立了启动起始地址，从而确定了源内存。

![Image from PDF page 589](../images/page-0589-image-01.jpeg)

表 22.1：STM32F401RE 微控制器中可用的启动模式

表 22.1 展示了 STM32F401RE 微控制器中可用的启动模式，摘自相关的参考手册。BOOT1 列中的“x”表示，当 BOOT0 引脚接地时，BOOT1 引脚的逻辑状态可以是任意的。第一行对应于最常见的启动模式：微控制器将闪存别名到地址 0x0000 0000。另外两种启动模式对应于从内部 SRAM 和系统存储器（System Memory）启动，系统存储器是一种 ROM 内存，包含所有 STM32 微控制器中的引导加载程序，我们将在后面研究它。

BOOT 引脚的状态在复位后 SYSCLK 的第 4 个上升沿被锁存。用户需要在复位后设置 BOOT 引脚以选择所需的启动模式。当退出待机低功耗模式时，BOOT 引脚也会被重新采样。因此，在进入待机模式时，必须保持其处于所需的启动模式配置。一旦这段启动时间过去，CPU 从地址 0x0000 0000 获取主堆栈指针（MSP），并从地址 0x0000 0004 开始从启动内存执行代码。所选内存（闪存、SRAM 或 ROM）始终可以通过其原始地址空间访问。

如果我们配置微控制器从 SRAM 内存启动，这是一种易失性内存，我们必须将程序代码上传到该内存中，并确保在地址 0x0000 0000 处正确设置了一个有效的向量表（至少由指向基础堆栈的指针和指向复位异常的指针组成）。这要求我们使用调试器工具，该工具在开始执行之前将所有必要的代码预加载到 SRAM 中。此外，还需要一个自定义的链接器脚本。我们稍后将会看到一个完整的示例。

### 22.1.1 软件物理重映射

一旦微控制器启动，即复位异常正在执行时，仍然可以通过编程 SYSCFG 内存映射寄存器（memory mapped register）的某些位，来重映射通过代码区域（即通过 I-Bus 和 D-Bus 线）可访问的内存。在 Cortex-M0/0+ 内核中，这涉及设置两个

²根据所使用的封装，在某些 STM32 微控制器中，BOOT1 引脚不存在，而是由选项字节区域中的一个特殊位（称为 nBOOT1）取代。有关此问题的更多信息，请查阅您微控制器的参考手册。在其他一些 STM32 系列中，如 STM32F7，BOOT1 引脚的功能完全由两个专用的选项字节取代。最后，在提供两个启动引脚的那些微控制器中，BOOT0 大多数时候是一个专用引脚，仅用于选择启动源，而 BOOT1 与一个 GPIO 引脚共享。一旦 BOOT1 被采样，相应的 GPIO 引脚就会被释放，可用于其他目的。然而，在引脚数少于 36 的那些微控制器中存在例外，其中即使 BOOT0 引脚在第一个时钟周期采样后也被视为输入 GPIO（例如，STM32L011K4T 就是其中之一）。

<!-- page: 590 -->

SYSCFG_CFGR1（在 CMSIS 库中为 SYSCFG->CFGR1）的位。在 Cortex-M3/4/7/33 内核中，这涉及设置专用的 SYSCFG_MEMRMP 寄存器（在 CMSIS 库中为 SYSCFG->MEMRMP）。

根据特定的 STM32 微控制器，通过执行软件物理重映射，可以重映射以下内存：

- 内部闪存
- 内部 SRAM
- FMC NVM bank1
- FMC SDRAM bank

最后两种内存仅在提供灵活存储器控制器（Flexible Memory Controller, FMC）的微控制器中可用，FMC 是一种允许接口外部 NVM 和 SDRAM 内存的外设。根据表 22.1，不允许直接从外部 NOR 和 SDRAM 内存启动。这些内存只能在微控制器已经从内部闪存加载了最小固件并启动后，使用软件物理重映射映射到地址 0x0000 0000。

一旦外部内存被物理重映射到地址 0x0000 0000，CPU 就可以通过 I-Bus 和 D-Bus 线访问它，而不是拥挤的 S-Bus，从而提升整体性能。这对于基于 Cortex-M7 的微控制器尤为重要，因为这些线与专用的 L1 缓存紧密耦合。

当 CPU 启动时，Cortex-M0/0+ 中 SYSCFG->CFGR1 寄存器或 Cortex-M3/4/7/33 中 SYSCFG->MEMRMP 寄存器的内容被锁存为 BOOT 引脚的值：这意味着在采样 BOOT 引脚时，微控制器会自动执行物理重映射。在更改此寄存器的内容以执行重映射之前，重要的是要在目标内存中有一个工作正常的向量表³。

### 22.1.2 向量表重定位

在第 20 章中，我们介绍了如何将向量表重定位到 CCM 内存中，以便利用这种与内核耦合的内存。当我们执行物理重映射时，无论是设置 BOOT 引脚还是相应地配置 SYSCFG->MEMRMP 寄存器，都不需要执行向量表重定位，因为 MCU 会自动将所选内存的起始地址别名为 0x0000 0000。然而，有时我们希望将向量表移动到与其原始位置不对应的其他内存位置。例如，我们可能希望在闪存中存储两个独立的固件镜像（参见图 22.1），并根据给定的初始条件选择其中一个。这就是引导加载程序（bootloader）的情况，它是一种特殊的“系统”程序，负责执行重要的配置任务，例如升级主固件，我们将在本章后面看到这一点。

³需要澄清的是，一旦使用 SYSCFG->MEMRMP 寄存器完成内存重映射，CPU 不会重新启动复位序列，也不会调用 Reset 异常的处理程序。调用该异常处理程序并确保 CPU 处于目标固件所期望的初始状态（例如，所有外设已禁用等）将是您的责任。

<!-- page: 591 -->

向量表偏移寄存器（Vector Table Offset Register, VTOR）是系统控制块（System Control Block, SCB）中的一个寄存器（在 CMSIS 库中为 SCB->VTOR），它允许设置向量表的基地址。一旦设置了该寄存器的内容，CPU 将从新的基地址开始，将地址视为指向中断服务例程的指针。

![Image from PDF page 591](../images/page-0591-image-01.png)

图 22.1：可以在闪存中存储两个独立的固件镜像

![Image from PDF page 591](../images/page-0591-image-02.png)

图 22.2：VTOR 寄存器的结构

在修改 VTOR 寄存器的内容时，重要的是要考虑以下几点：

- VTOR 寄存器在基于 Cortex-M0 的 MCU 中不可用，因此在不使用物理重映射的情况下无法重定位向量表（存在一种绕过此限制的方法，我们稍后会看到）。
- 在基于 Cortex-M3 r1p0 内核修订版的 STM32F1 MCU 中，VTOR 寄存器的位 [31:30] 是保留位（参见图 22.2），因此只能将向量表重定位到代码内存（0x0000 0000）和 SRAM（0x2000 0000）中。

<!-- page: 592 -->

- ARM 规范建议在更新 VTOR 寄存器的内容之前使用 dmb（Data Memory Barrier，数据内存屏障）指令，并在更新之后使用 dsb（Data Synchronization Barrier，数据同步屏障）指令。请参见第 20 章中的示例 6 以获取完整示例。
- 在更改 VTOR 寄存器的内容之前，请确保应用程序的最小向量表已经位于新位置。
- 如果应用程序使用了外设中断，请在开始重定位过程之前暂停所有中断。

### 22.1.3 使用 STM32CubeIDE 从 SRAM 运行固件

有时，将二进制固件加载到 SRAM 中并从中启动会很有用。与常规的从闪存调试相比，这有一些优势：

- 它大大减少了加载时间，特别是在较旧且性能较低的 STM32 MCU 上，因为 RAM 内存的运行速度比闪存快，并且在写入固件之前不需要擦除周期；
- 它有助于延长闪存的使用寿命，避免仅仅为了检查固件的小改动而进行无用的擦除周期；
- 在调试涉及闪存高级操作的代码时（例如在开发自定义引导加载程序期间），它可以成为救命稻草。

然而，从 SRAM 调试设置了一些限制。最相关的是可用的 SRAM 内存量减少。此外，在调试期间无法复位 MCU 是另一个严重的限制。

STM32CubeIDE 和 ST-LINK 调试器完全能够加载代码到 RAM 并从中开始调试。使用某些 STM32 系列的用户应该已经注意到，CubeMX 会自动向项目添加两个不同的链接器脚本：一个文件名以 _FLASH.ld 结尾，另一个以 _RAM.ld 结尾（例如，Nucleo-F401RE 板的所有者将找到文件 STM32F401RETX_FLASH.ld 和 STM32F401RETX_RAM.ld）。这两个文件只有一个区别：在以 _RAM.ld 结尾的文件中，所有二进制部分都被生成并映射到 SRAM 内存中。调试器的工作是处理此配置并自动从 RAM 开始执行。

```text
To use the linker script for RAM debugging, we need to instruct the GNU LD accordingly. Go inside
Project Properties->C/C++ Build->Settings->MCU GCC Linker->General. You will find the en-
try Linker Script (-T) with this setting: ${workspace_loc:/${ProjName}/STM32FXXXXXX_FLASH.ld},
as shown in Figure 22.3. Change the linker script according t the filename of the linker script for
RAM debugging.
```

对于那些 CubeMX 未生成专用链接器脚本的项目，在您掌握第 20 章的概念后，修改提供的链接器脚本以使所有二进制部分映射到 SRAM 内存将很容易。

<!-- page: 593 -->

![Image from PDF page 593](../images/page-0593-image-01.png)

在因为此过程在您的情况下可能无法工作而向本作者提交支持请求之前，请考虑到，对于拥有基于 SRAM 内存较少的 STM32 MCU 的 Nucleo 板的用户，此过程可能无法工作。这是因为代码区域可能会落入堆栈区域。此过程基本上仅适用于真正小型且有限的程序。

![Image from PDF page 593](../images/page-0593-image-02.jpeg)

图 22.3：用于设置 LD 配置脚本的项目设置

## 22.2 集成式 STM32 引导加载程序

在现代数字电子领域，发布固件的后续升级版本几乎是不可避免的，否则就无法分发电子设备。对于集成了大量集成电路和外围设备的复杂电路板而言，这一点尤为真实。迟早，所有嵌入式开发人员都需要一种分发固件升级的方式，更重要的是，他们需要一种让客户在没有专用（且有时昂贵的）调试器的情况下将固件上传到微控制器的方法。此外，出于设计选择，最终 PCB 上往往不会添加 SWD 调试端口。⁴

引导加载程序（Bootloader）是一段软件，通常在微控制器启动时最先执行，它具有升级内部闪存中固件的能力。此操作也被称为应用内编程（In-Application Programming, IAP），这与使用外部专用调试器对微控制器进行编程不同：这种对微控制器进行编程的另一种方式也被称为系统内编程（In-System Programming, ISP）。

引导加载程序通常被设计为通过通信外围设备（USART、USB、以太网等）接受命令，该外围设备用于与微控制器交换固件二进制文件。

⁴对于那些想知道如何在没有调试端口且不使用集成引导加载程序的情况下将固件上传到电路板的人来说，了解以下信息可能很有用：ST 可以在微控制器生产期间为您预编程固件并发货。这种可能性通常针对相当大批量的订单（据我所知，数量超过 10,000 片）。请向您的销售代表咨询更多详情。最后，还存在一些专门从事此项工作的公司，他们甚至可以为您执行诸如重新卷带（re-reeling）等额外操作。

<!-- page: 594 -->

此外，通常还需要一个专门设计用于在外部 PC 上运行的程序。

所有 STM32 微控制器出厂时都在称为系统存储器（System memory）的 ROM 存储器中预编程了一个引导加载程序，在大多数 STM32 微控制器中，它映射在地址范围 0x1FFF 0000 - 0x1FFF 77FF 内⁵。根据所使用的微控制器系列和封装，该引导加载程序可以使用以下方式与外部世界交互：

- USART
- USB（DFU 协议）
- CAN 总线
- I²C
- SPI

对于每一种通信外围设备，ST 都定义了一种标准化协议，允许执行以下操作：

- 获取引导加载程序的版本和支持的命令。⁶
- 获取芯片 ID。
- 从主机应用指定的地址开始读取一定数量的字节内存。
- 从主机应用指定的地址开始向 RAM 或闪存写入一定数量的字节。
- 擦除一个或多个闪存存储器页/扇区。
- 跳转到位于内部闪存存储器或 SRAM 中的用户应用程序代码。
- 启用/禁用某些页/扇区的读/写保护。

对于每种通信协议，ST 都提供了一份名为“STM32 引导加载程序中使用的 PPP 协议”的专用应用笔记，其中 PPP 代表外围设备类型。例如，AN3155⁷ 是关于 USART 协议的。

集成式引导加载程序被设计为持续采样所有支持的外围设备，以检测特定的“启动条件”：一旦满足该条件，就选择该外围设备与外部世界进行交互。例如，如果在 UARTx 接口上接收到字节 0x7F，则引导加载程序开始以 UART 模式工作。关于特定 STM32 微控制器引导加载程序选择序列的完整描述，请参阅 ST 的 AN2606⁸。

除了使用的通信外围设备外，引导加载程序还使用其他几种硬件资源：

- HSI 振荡器，被选为时钟源。

⁵第 1 章中的图 4 展示了系统存储器在 Cortex-M 4GB 地址空间中的位置。⁶这不是一个次要功能，因为存在不同版本的 STM32 引导加载程序，其中一些版本存在不可忽略的差异。⁷https://bit.ly/2cojjQI ⁸https://bit.ly/29sEb8t

<!-- page: 595 -->

- SysTick 定时器（并非所有通信外围设备都使用）。
- 约 2K 的 SRAM 存储器。
- IWDG 外围设备（预分频器配置为其最大值，并且定期刷新 IWDG，以防止在用户之前启用了硬件 IWDG 选项的情况下发生复位）。

此外，通过引导加载程序进行内存管理存在一些限制：

- 一些 STM32 微控制器不支持批量擦除操作。要使用引导加载程序执行批量擦除，有两种选择：使用 Erase 命令逐个擦除所有扇区，或者将闪存读保护级别设置为 Level 1，然后再将其设回 Level 0。
- STM32L1/L0 系列的引导加载程序固件允许操作 EEPROM，除了标准存储器（内部闪存和 SRAM、选项字节和系统存储器）之外。此存储器类型的起始地址和大小取决于具体的部件号。EEPROM 可以读取和写入，但不能使用 Erase 命令擦除。在向 EEPROM 位置写入时，引导加载程序固件会在任何写入之前管理该位置的擦除操作。向 EEPROM 的写入必须按字对齐（要写入的地址应为 4 的倍数），并且数据数量也必须是 4 的倍数。要擦除 EEPROM 位置，您可以在此位置写入零。
- STM32F2/F4/F7/L4 系列的引导加载程序固件支持 OTP 存储器，除了标准存储器（内部 Flash、内部 SRAM、选项字节和系统存储器）之外。该区域的起始地址和大小取决于具体的部件号。有关更多信息，请参阅产品参考手册。OTP 存储器可以读取和写入，但不能使用 Erase 命令擦除。在向 OTP 存储器位置写入时，请确保相关的保护位未被复位。
- 对于 STM32F2/F4/F7 系列，内部闪存的写入操作格式取决于电压范围。默认情况下，写入操作允许按单字节格式进行（不允许半字、字和双字操作）。为了提高写入操作的速度，用户应施加适当的电压范围，以允许按半字、字或双字进行写入操作，并使用引导加载程序软件在运行时更新此配置。为此操作保留了一些虚拟位置。有关此操作的更多信息，请参阅 ST 的 AN2606⁹。

要使用 USART 或 USB 协议接口集成式引导加载程序，可以通过选择相应的协议来使用 STM32CubeProgrammer，如图 22.4 所示。

还要考虑到，STM32CubeProgrammer 具有命令行接口，允许您将其用于生产环境。有关此功能的更多信息，请参阅相应的用户手册（UM2237¹⁰）。此外，如果您考虑使用 USB 引导加载程序，请注意，一些其他开源应用程序，如 dfu-util¹¹ 工具，也可以在 Windows 以及

⁹https://bit.ly/29sEb8t ¹⁰https://bit.ly/3E9bMzr ¹¹http://dfu-util.sourceforge.net/

<!-- page: 596 -->

Linux 和 MacOS 上使用。有关 STM32 引导加载程序中 USB DFU 模式的更多信息，请参阅 ST 的 UM0412¹² 用户手册。

![Image from PDF page 596](../images/page-0596-image-01.png)

图 22.4：如何在 STM32CubeProgrammer 中选择引导加载程序协议

### 22.2.1 从板载固件启动 STM32 引导加载程序

集成引导加载程序（bootloader）的执行与 BOOT 引脚的状态相关联，这些引脚在最初的几个时钟周期内被采样。然而，出于多种设计选择，您可能无法按要求配置 BOOT 引脚。因此，您可以从固件“跳转”到系统存储器（例如，用户可能被迫按下隐藏开关）。

从用户代码强制引导加载程序执行并不困难：只需定义一个函数指针即可。

```text
1
__set_MSP(SRAM_END);
2
uint32_t JumpAddress = *(volatile uint32_t*)(0x1FFF0000 + 4);
3
void (*boot_loader)(void) = JumpAddress;
4
SYSCFG->MEMRMP = 0x1; //Remap 0x0000 0000 to System Memory
5
boot_loader();
6
//Never coming here
```

第 1 行的指令将主堆栈指针（main stack pointer）设置为 SRAM 的末尾（通常不需要这样做，但以防万一……）。然后，我们创建一个指向函数的指针，该函数的地址被设置为系统存储器（System Memory）¹³ 的起始位置，并在物理重映射（physical remap）到系统存储器¹⁴ 后，通过调用函数 boot_loader() 简单地跳转到集成引导加载程序。

```text
¹²https://bit.ly/29sJen2
¹³The above address, 0x1FFF 0000, coincides with the starting address of System Memory in an STM32F401RE MCU; consult the reference
manual for your MCU for the exact value).
¹⁴Probably the physical remap is not strictly needed, since the bootloader seems to work well the same.
```

<!-- page: 597 -->

然而，在跳转到系统存储器时必须格外小心。事实上，引导加载程序被设计为仅在复位后立即调用，并且它假设 CPU 及其外设已设置为默认初始状态。一种更好的解决方案可能是将特殊代码存储在 SRAM 存储器中，然后在软件中强制系统复位：我们可以从复位异常处理程序（Reset exception handler）中检查该特殊代码，并在任何其他初始化过程之前跳转到系统存储器。该保护值必须存储在 .data 和 .bss 区域之外的内存位置，否则它可能在固件启动期间被初始化（或者，我们可以将此代码放置在复位异常处理程序中，在这些区域被初始化之前）。

### 22.2.2 STM32CubeIDE 工具链中的启动序列

现在启动过程应该已经清晰了，我们可以分析一个真正基本的主题：使用 STM32CubeIDE 工具链开发的应用程序在启动期间执行的确切步骤是什么？答案并不简单，使用此工具链的资深程序员必须知道几个重要的事项。

在第 20 章中，我们深入分析了复位异常（Reset exception）的工作方式。然而，该章节中的示例与真实工具链是隔离的：我们开发了一个最小的 STM32 应用程序，既不使用 CubeHAL，也不使用由 CubeMX 生成的启动文件。因此，为了理解实际的启动序列，我们必须从头开始：从复位异常开始。

在第 7 章中，我们看到汇编文件 system/src/cmsis/startup_stm32XXxx.s 包含向量表的定义。该文件由 ST 提供，并且针对给定的 STM32 MCU 是特定的。打开适合您 MCU 的文件，您可以在大约第 50-60 行找到 Reset_Handler 的定义。

```text
56
.section
.text.Reset_Handler
57
.weak
Reset_Handler
58
.type
Reset_Handler, %function
59
Reset_Handler:
60
ldr
sp, =_estack
/* set stack pointer */
```

61

```text
62
/* Copy the data segment initializers from flash to SRAM */
63
movs
r1, #0
64
b
LoopCopyDataInit
```

65

```text
66
CopyDataInit:
67
ldr
r3, =_sidata
68
ldr
r3, [r3, r1]
69
str
r3, [r0, r1]
70
adds
r1, r1, #4
```

71

```text
72
LoopCopyDataInit:
73
ldr
r0, =_sdata
74
ldr
r3, =_edata
75
adds
r2, r0, r1
```

<!-- page: 598 -->

```text
76
cmp
r2, r3
77
bcc
CopyDataInit
78
ldr
r2, =_sbss
79
b
LoopFillZerobss
80
/* Zero fill the bss segment. */
81
FillZerobss:
82
movs
r3, #0
83
str
r3, [r2], #4
```

84

```text
85
LoopFillZerobss:
86
ldr
r3, = _ebss
87
cmp
r2, r3
88
bcc
FillZerobss
```

89

```text
90
/* Call the clock system intitialization function.*/
91
bl
SystemInit
92
/* Call static constructors */
93
bl __libc_init_array
94
/* Call the application's entry point.*/
95
bl
main
96
bx
lr
97
.size
Reset_Handler, .-Reset_Handler
```

如您所见，Reset_Handler 是用汇编编写的，但现在我们已经掌握了许多基本概念，理解它应该很容易。例程主体从第 60 行开始。在这里，MSP（主堆栈指针）被设置为 _estack 链接器变量的内容（它与 SRAM 的末尾一致）。然后，控制权转移到 LoopCopyDataInit 例程，该例程初始化 .data 段。接着，控制权转移到 LoopFillZerobss 例程，该例程初始化 .bss 段并调用 SystemInit() 例程（我们稍后会分析它）；紧随此例程之后，通过调用 __libc_init_array() 初始化 C++ 静态构造函数。最后，控制权转移到 main() 例程。

CMSIS SystemInit() 例程是平台相关的，由 ST 在名为 Core/Src/system_stm32XXxx.c 的文件中提供。该例程通常包含激活附加协处理器（如果存在）- 如 FPU。在基于 Cortex-M3/4/7/33 的 MCU 中，该例程还包含根据特定的一组 C 宏定义进行的向量表重定位。请参阅您 MCU 的 SystemInit() 实现。

## 22.3 开发自定义引导加载程序

请仔细阅读

![Image from PDF page 598](../images/page-0598-image-01.png)

本段描述的引导加载程序（bootloader）仅在 ST-LINK 接口的固件版本等于或高于 2.27.15 时才能正常工作。旧版本在 VCP 上存在一个缺陷，导致 USART 接口无法按预期工作。请确保您的 Nucleo 板已更新。

<!-- page: 599 -->

集成引导加载程序在许多情况下表现良好。许多实际项目都可以从中受益。此外，ST 提供的免费工具可以减少开发用于向 MCU 上传固件的自定义应用程序所需的工作量。然而，对于某些应用，您可能需要标准引导加载程序未实现的其他功能。例如，我们可能希望加密分发的固件，使得只有板载引导加载程序能够使用硬编码在引导加载程序代码中的预共享密钥对其进行解码。

我们现在将开发一个自定义引导加载程序，以便我们能够将新固件上传到目标 MCU。这基本上只提供集成引导加载程序所实现功能的一小部分，但它将为我们提供审查开发自定义引导加载程序所需基本步骤的机会。它将提供以下功能：

- 使用 UART 接口上传新固件（在我们的情况下，是所有 Nucleo 板提供的 UART2 接口）。
- 获取 MCU 类型。
- 擦除给定数量的闪存扇区/页。
- 从给定地址开始写入一系列字节。
- 使用 AES-128 算法¹⁵ 对交换的固件进行加密/解密。

![Image from PDF page 599](../images/page-0599-image-01.jpeg)

表 22.2：STM32F401RE MCU 中的闪存内存组织

我们将在此分析的代码依赖于 STM32F401RE 微控制器的闪存内存布局，如表 22.2 所示，该表提取自相应的参考手册。如您所见，512KB 的闪存内存被划分为七个扇区。第一个扇区，即表 22.2 中以蓝色高亮显示的扇区 0，将用于存储集成引导加载程序。如果您正在使用不同的 STM32 MCU，请参阅本书示例，查看引导加载程序是如何为您的 MCU 安排的。

¹⁵在实际应用中，特别是如果您使用合同制造商来生产您的电路板，您可能需要更安全的引导加载程序和更复杂的生产环境。ST 提供了一个完整的扩展包，名为 X-CUBE-SBSFU，它由处理安全引导加载程序、安全固件升级和分发、密钥管理及其分发的完整解决方案组成。

<!-- page: 600 -->

一旦 MCU 复位，引导加载程序开始执行¹⁶。这意味着引导加载程序被编译为从 0x0800 0000 地址开始映射，就像本书中看到的任何常规 STM32 应用程序一样。

定义了一个最小的向量表，使 MCU 能够正确开始执行。引导加载程序随后采样 PC13 引脚，该引脚在几乎所有 Nucleo 板上对应于板上的蓝色按钮。如果按下按钮，则开始在 UART2 接口上接受命令。否则，它立即重定位 VTOR 寄存器，并将控制权传递给主固件的复位异常处理程序。

还提供了一个用 Python 2 编写的配套脚本。它名为 flasher.py，您可以在本书示例中找到它。我们将在后续段落中描述如何使用它。

在我们深入介绍用于与引导加载程序交换消息的命令细节之前，我们将开始分析在启动过程中执行的过程以及控制权如何转移到主固件。

```text
Filename: src/main-bootloader.c
7
/* Global macros */
8
#define ACK
0x79
9
#define NACK
0x1F
10
#define CMD_ERASE
0x43
11
#define CMD_GETID
0x02
12
#define CMD_WRITE
0x2b
```

13

```text
14
#define APP_START_ADDRESS
0x08004000 /* In STM32F401RE this corresponds with the start
15
address of Sector 1 */
```

16

```text
17
#define SRAM_SIZE
96*1024
// STM32F401RE has 96 KB of RAM
18
#define SRAM_END
(SRAM_BASE + SRAM_SIZE)
```

19

```text
20
#define ENABLE_BOOTLOADER_PROTECTION 0
21
/* Private variables ---------------------------------------------------------*/
```

22

```text
23
/* The AES_KEY cannot be defined const, because the aes_enc_dec() function
24
temporarily modifies its content */
25
uint8_t AES_KEY[] = { 0x4D, 0x61, 0x73, 0x74, 0x65, 0x72, 0x69, 0x6E, 0x67,
26
0x20, 0x20, 0x53, 0x54, 0x4D, 0x33, 0x32 };
```

27

```text
28
extern CRC_HandleTypeDef hcrc;
29
extern UART_HandleTypeDef huart2;
```

第 14 行的宏 APP_START_ADDRESS 定义了主固件的起始地址。根据 STM32F401RE MCU 的内存布局，第二个扇区从该地址开始，主应用程序固件将存储在那里。这意味着 MSP 将被放置在

¹⁶显然，必须配置 MCU 引脚，使闪存内存成为默认启动源。

<!-- page: 601 -->

## 位于 0x0800 4000 处，以及闪存内存中复位异常处理程序（Reset exception handler）的地址 0x0800 4004。在第 25 行定义的 AES_KEY 数组包含十六个字节，构成了用于加密/解密上传固件的 AES-128 密钥。我们稍后将会分析其用法。

```text
Filename: src/main-bootloader.c
44
/* Minimal vector table */
45
uint32_t *vector_table[] __attribute__((section(".isr_vector"))) = {
46
(uint32_t *) SRAM_END, // initial stack pointer
47
(uint32_t *) _start,
// _start is the Reset_Handler
48
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, (uint32_t *) SysTick_Handler };
```

## 向量表（vector table）定义在第 45 行。它仅包含 MSP 指针（与 SRAM 内存的末尾重合）、指向复位异常处理程序的指针（在本例中为 _start，它除了初始化 .data 和 .bss 段并将控制权转移到 main() 例程外，不做其他任何事情），以及指向 SysTick_Handler 的指针。这是必需的，因为我们将使用标准的 HAL 例程来接口外设，而 HAL 是围绕一个唯一的时间基准构建的，该时间基准通常使用 SysTick 定时器生成。因此，HAL 需要启用该定时器并捕获溢出事件，以便增加全局滴答计数。

```text
Filename: src/main-bootloader.c
93
int main(void) {
94
uint32_t ulTicks = 0;
95
uint8_t ucUartBuffer[20];
```

96

```text
97
/* HAL_Init() sets SysTick timer so that it overflows every 1ms */
98
HAL_Init();
99
MX_GPIO_Init();
100
101
#if ENABLE_BOOTLOADER_PROTECTION
102
/* Ensures that the first sector of flash is write-protected preventing that the
103
bootloader is overwritten */
104
CHECK_AND_SET_FLASH_PROTECTION();
105
#endif
106
107
/* If USER_BUTTON is pressed */
108
if (HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_13) == GPIO_PIN_RESET) {
109
/* CRC and UART2 peripherals enabled */
110
MX_CRC_Init();
111
MX_USART2_UART_Init();
112
113
ulTicks = HAL_GetTick();
114
115
while (1) {
116
/* Every 500ms the LD2 LED blinks, so that we can see the bootloader running. */
117
if (HAL_GetTick() - ulTicks > 500) {
```

<!-- page: 602 -->

```text
118
HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
119
ulTicks = HAL_GetTick();
120
}
121
122
/* We check for new commands arriving on the UART2 */
123
HAL_UART_Receive(&huart2, ucUartBuffer, 20, 10);
124
switch (ucUartBuffer[0]) {
125
case CMD_GETID:
126
cmdGetID(ucUartBuffer);
127
break;
128
case CMD_ERASE:
129
cmdErase(ucUartBuffer);
130
break;
131
case CMD_WRITE:
132
cmdWrite(ucUartBuffer);
133
break;
134
};
135
}
136
} else {
137
/* USER_BUTTON is not pressed. We first check if the first 4 bytes starting from
138
APP_START_ADDRESS contain the MSP(end of SRAM). If not, the LD2 LED blinks quickly. */
139
if (*((uint32_t*) APP_START_ADDRESS) != SRAM_END) {
140
while (1) {
141
HAL_Delay(30);
142
HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
143
}
144
} else {
145
/* A valid program seems to exist in the second sector: we so prepare the MCU
146
to start the main firmware */
147
MX_GPIO_Deinit(); //Puts GPIOs in default state
148
SysTick->CTRL = 0x0; //Disables SysTick timer and its related interrupt
149
HAL_DeInit();
150
151
RCC->CIR = 0x00000000; //Disable all interrupts related to clock
152
__set_MSP(*((volatile uint32_t*) APP_START_ADDRESS)); //Set the MSP
153
154
__DMB(); //ARM says to use a DMB instruction before relocating VTOR */
155
SCB->VTOR = APP_START_ADDRESS; //We relocate vector table to the sector 1
156
__DSB(); //ARM says to use a DSB instruction just after relocating VTOR */
157
158
/* We are now ready to jump to the main firmware */
159
uint32_t JumpAddress = *((volatile uint32_t*) (APP_START_ADDRESS + 4));
160
void (*reset_handler)(void) = (void*)JumpAddress;
161
reset_handler(); //We start the execution from he Reset_Handler of the main firmware
162
163
for (;;)
164
; //Never coming here
```

<!-- page: 603 -->

```text
165
}
166
}
167
}
```

现在我们将解释 main() 例程执行的任务。一旦它被复位异常处理程序（_start() 例程）调用，它首先初始化 CubeHAL，并将此阶段执行的操作数量降至最低：这有助于减少启动时间。HAL_Init() 例程还配置 SysTick 定时器，使其每 1ms 溢出一次。随后对 PC13 引脚进行采样，如果用户按住 USER BUTTON，则例程进入一个无限循环，接受 UART2 上的三个命令。我们稍后将会分析它们。请注意，我们保持默认的时钟源不变（即 HSI 振荡器）。

相反，如果 USER BUTTON 未被按下，则 main() 例程验证第二个扇区的第一个内存位置是否包含 MSP（我们简单地检查它是否包含 SRAM_END 值）。如果没有，固件将快速闪烁 LD2 LED，以指示没有要运行的主应用程序。

如果该内存位置包含 MSP 指针（第 144 行），我们可以开始启动序列。GPIO 被设置为默认状态，HAL 被去初始化，SysTick 定时器停止，并且其异常被禁用。第 151 行禁用了所有与时钟相关的中断，并将 MSP 设置为扇区 1 前 4 个字节中指定的地址（因为向量表放置在那里，我们稍后会看到）。随后，VTOR 基地址被设置为 APP_START_ADDRESS（对于 STM32F401RE 引导加载程序，即 0x0800 4000）。主固件的复位异常地址从 0x0800 4004 内存位置导出，并定义了指向该函数的指针。最后，在第 161 行调用复位异常，引导加载程序结束。

在我们分析引导加载程序实现的三个命令之前，最好先快速查看一下本章示例中附带的另一个应用程序。它名为 main-app1.c，只不过是一个简单的应用程序，用于闪烁 LD2 LED 并在 UART2 上打印消息。唯一值得注意的相关事项是相关的链接脚本，名为 STM32F401RETX_APP.ld，它以以下方式定义 FLASH 内存区域：

```text
Filename: src/ldscript-app.ld
14
MEMORY {
15
FLASH (rx) : ORIGIN = 0x08004000, LENGTH = 512K - 16K
16
RAM (xrw) : ORIGIN = 0x20000000, LENGTH = 96K
```

如您所见，链接器将从 0x0800 4000 地址开始重新定位应用程序代码。此外，该内存区域的长度设置为 496KB：由于第一个扇区宽 16KB，512 - 16 等于 496。这种闪存内存区域的定义还允许我们使用 ST-LINK 调试器（或 STM32CubeProgrammer）上传和调试固件，而不会覆盖引导加载程序。

根据上一段所述，请确保 SystemInit() 例程不更改 VTOR 寄存器的值。

![Image from PDF page 603](../images/page-0603-image-01.png)

<!-- page: 604 -->

## 现在是分析此引导加载程序支持的三个命令的正确时机：CMD_GETID、CMD_ERASE 和 CMD_WRITE。

## 获取 ID 命令 CMD_GETID 命令用于获取 MCU ID¹⁷，其结构如图 22.5 所示。引导加载程序期望接收到字节 0x02，随后是该字节的 CRC-32 校验值。引导加载程序通过发送 ACK（定义在 mainbootloader.c 文件的第 8 行，值为 0x79）来响应请求，随后发送两个包含 MCU ID 的字节。

![Image from PDF page 604](../images/page-0604-image-01.png)

图 22.5：CMD_GETID 的结构

```text
Filename: src/main-bootloader.c
223
void cmdGetID(uint8_t *pucData) {
224
uint16_t usDevID;
225
uint32_t ulCrc = 0;
226
uint32_t ulCmd = pucData[0];
227
228
memcpy(&ulCrc, pucData + 1, sizeof(uint32_t));
229
230
/* Checks if provided CRC is correct */
231
if (ulCrc == HAL_CRC_Calculate(&hcrc, &ulCmd, 1)) {
232
usDevID = (uint16_t) (DBGMCU->IDCODE & 0xFFF); //Retrieves MCU ID from DEBUG interface
233
234
/* Sends an ACK */
235
pucData[0] = ACK;
236
HAL_UART_Transmit(&huart2, pucData, 1, HAL_MAX_DELAY);
237
238
/* Sends the MCU ID */
239
HAL_UART_Transmit(&huart2, (uint8_t *) &usDevID, 2, HAL_MAX_DELAY);
240
} else {
241
/* The CRC is wrong: sends a NACK */
242
pucData[0] = NACK;
243
HAL_UART_Transmit(&huart2, pucData, 1, HAL_MAX_DELAY);
244
}
245
}
```

## 上述代码展示了该命令的实现方式。如你所见，CRC 从通过 UART 接收的消息中提取，并与由 CRC 外设计算出的值进行比较。如果两个值匹配，则从 DEBUG 接口派生出 MCU ID，并通过 UART 连同 ACK 一起传输。

¹⁷MCU ID 不同于 CPU ID。前者标识 STM32 系列和芯片类型（例如，0x433 标识 STM32F401RE MCU）。后者是一个唯一 ID，用于标识特定的 MCU，不可能（或至少非常困难）存在两个具有相同 CPU ID 的 STM32 微控制器。

<!-- page: 605 -->

## 如果 CRC 不匹配，则发送 NACK（值为 0x1F）。

## 擦除命令 CMD_ERASE 命令用于擦除闪存存储器中的指定扇区，其结构如图 22.6 所示。该命令由标识命令类型的 ID 0x43 组成，后跟要删除的扇区数量（或值 0xFF 以删除除引导加载程序所在的第一个扇区以外的所有扇区）以及 CRC-32。当擦除过程完成时，引导加载程序通过发送 ACK 进行响应。

![Image from PDF page 605](../images/page-0605-image-01.png)

图 22.6：CMD_ERASE 的结构

```text
Filename: src/main-bootloader.c
180
void cmdErase(uint8_t *pucData) {
181
FLASH_EraseInitTypeDef eraseInfo;
182
uint32_t ulBadBlocks = 0, ulCrc = 0;
183
uint32_t pulCmd[] = { pucData[0], pucData[1] };
184
185
memcpy(&ulCrc, pucData + 2, sizeof(uint32_t));
186
187
/* Checks if provided CRC is correct */
188
if (ulCrc == HAL_CRC_Calculate(&hcrc, pulCmd, 2) &&
189
(pucData[1] > 0 && (pucData[1] < FLASH_SECTOR_TOTAL - 1 || pucData[1] == 0xFF))) {
190
/* If data[1] contains 0xFF, it deletes all sectors; otherwise
191
* the number of sectors specified. */
192
eraseInfo.Banks = FLASH_BANK_1;
193
eraseInfo.Sector = FLASH_SECTOR_1;
194
eraseInfo.NbSectors = pucData[1] == 0xFF ? FLASH_SECTOR_TOTAL - 1 : pucData[1];
195
eraseInfo.TypeErase = FLASH_TYPEERASE_SECTORS;
196
eraseInfo.VoltageRange = FLASH_VOLTAGE_RANGE_3;
197
198
HAL_FLASH_Unlock(); //Unlocks the flash memory
199
HAL_FLASHEx_Erase(&eraseInfo, &ulBadBlocks); //Deletes given sectors */
200
HAL_FLASH_Lock(); //Locks again the flash memory
201
202
/* Sends an ACK */
203
pucData[0] = ACK;
204
HAL_UART_Transmit(&huart2, (uint8_t *) pucData, 1, HAL_MAX_DELAY);
205
} else {
206
/* The CRC is wrong: sends a NACK */
207
pucData[0] = NACK;
208
HAL_UART_Transmit(&huart2, pucData, 1, HAL_MAX_DELAY);
```

<!-- page: 606 -->

```text
209
}
210
}
```

上述代码展示了该命令的实现方式。如你所见，CRC 从通过 UART 接收的消息中提取，并与由 CRC 外设计算出的值进行比较。注意，由于 CRC 外设具有 32 位宽的数据寄存器，且 CRC-32 是针对整个寄存器计算的，我们将前两个字节转换为两个 32 位值。

如果 CRC 匹配，则填充 FLASH_EraseInitTypeDef 结构体的一个实例，以便从第二个扇区（第 193 行）开始擦除闪存扇区，直到指定的扇区数量（第 194 行）。随后解锁闪存存储器（第 198 行），并通过调用 HAL_FLASHEx_Erase() 例程执行擦除过程。

写入命令 CMD_WRITE 命令用于从给定的内存位置开始存储十六个字节（即四个字），其结构如图 22.7 所示。该命令由两个不同的部分组成。第一部分由命令 ID 0x2b 组成，后跟放置数据字节的起始地址以及命令的 CRC-32。如果 CRC 匹配且指定地址等于或高于 APP_START_ADDRESS，引导加载程序以 ACK 进行响应。随后，引导加载程序期望接收另一组由十六个字节和这些字节的 CRC-32 校验值组成的序列。

![Image from PDF page 606](../images/page-0606-image-01.png)

图 22.7：CMD_WRITE 的结构

```text
Filename: src/main-bootloader.c
267
void cmdWrite(uint8_t *pucData) {
268
uint32_t ulSaddr = 0, ulCrc = 0;
269
270
memcpy(&ulSaddr, pucData + 1, sizeof(uint32_t));
271
memcpy(&ulCrc, pucData + 5, sizeof(uint32_t));
272
273
uint32_t pulData[5];
274
for(int i = 0; i < 5; i++)
275
pulData[i] = pucData[i];
276
277
/* Checks if provided CRC is correct */
278
if (ulCrc == HAL_CRC_Calculate(&hcrc, pulData, 5) && ulSaddr >= APP_START_ADDRESS) {
```

<!-- page: 607 -->

```text
279
/* Sends an ACK */
280
pucData[0] = ACK;
281
HAL_UART_Transmit(&huart2, (uint8_t *) pucData, 1, HAL_MAX_DELAY);
282
283
/* Now retrieves given amount of bytes plus the CRC32 */
284
if (HAL_UART_Receive(&huart2, pucData, 16 + 4, 200) == HAL_TIMEOUT)
285
return;
286
287
memcpy(&ulCrc, pucData + 16, sizeof(uint32_t));
288
289
/* Checks if provided CRC is correct */
290
if (ulCrc == HAL_CRC_Calculate(&hcrc, (uint32_t*) pucData, 4)) {
291
HAL_FLASH_Unlock(); //Unlocks the flash memory
292
293
/* Decode the sent bytes using AES-128 ECB */
294
aes_enc_dec((uint8_t*) pucData, AES_KEY, 1);
295
for (uint8_t i = 0; i < 16; i++) {
296
/* Store each byte in flash memory starting from the specified address */
297
HAL_FLASH_Program(FLASH_TYPEPROGRAM_BYTE, ulSaddr, pucData[i]);
298
ulSaddr += 1;
299
}
300
HAL_FLASH_Lock(); //Locks again the flash memory
301
302
/* Sends an ACK */
303
pucData[0] = ACK;
304
HAL_UART_Transmit(&huart2, (uint8_t *) pucData, 1, HAL_MAX_DELAY);
305
} else {
306
goto sendnack;
307
}
308
} else {
309
goto sendnack;
310
}
311
312
sendnack:
313
pucData[0] = NACK;
314
HAL_UART_Transmit(&huart2, (uint8_t *) pucData, 1, HAL_MAX_DELAY);
315
}
```

## 上述代码展示了该命令的实现方式。如您所见，消息第一部分的 CRC 会与传输的值进行比对（第 [273:278] 行）。如果匹配，则发送 ACK，并处理接下来的字节。如果这些其他字节的 CRC-32 也匹配（第 290 行），则使用 AES-128 算法¹⁸和预共享密钥对发送的数据字节进行解密。数据字节

¹⁸aes_enc_dec() 函数取自 TI 员工 Eric Peeters 制作的库。可以从 TI 网站 (http://www.ti.com/tool/AES-128) 下载，其许可证允许自由使用。ST 为 STM32 平台提供了一个完整的加密库，该库也兼容 Cube 框架 (https://bit.ly/29zWN81)。该库还可以利用那些提供专用硬件加密单元的 STM32 微控制器。然而，该库的许可证阻止作者将其与本书中的示例一起发布。

<!-- page: 608 -->

被存储在从给定内存位置开始的闪存（flash memory）中。

还有一件事需要分析：如果宏 ENABLE_BOOTLOADER_PROTECTION 被设置为 1，则 main() 函数会调用 CHECK_AND_SET_FLASH_PROTECTION() 函数。

```text
Filename: src/main-bootloader.c
317
void CHECK_AND_SET_FLASH_PROTECTION(void) {
318
FLASH_OBProgramInitTypeDef obConfig;
319
320
/* Retrieves current OB */
321
HAL_FLASHEx_OBGetConfig(&obConfig);
322
323
/* If the first sector is not protected */
324
if ((obConfig.WRPSector & OB_WRP_SECTOR_0) == OB_WRP_SECTOR_0) {
325
HAL_FLASH_Unlock(); //Unlocks flash
326
HAL_FLASH_OB_Unlock(); //Unlocks OB
327
obConfig.OptionType = OPTIONBYTE_WRP;
328
obConfig.WRPState = OB_WRPSTATE_ENABLE; //Enables changing of WRP settings
329
obConfig.WRPSector = OB_WRP_SECTOR_0; //Enables WP on first sector
330
HAL_FLASHEx_OBProgram(&obConfig); //Programs the OB
331
HAL_FLASH_OB_Launch(); //Ensures that the new configuration is saved in flash
332
HAL_FLASH_OB_Lock(); //Locks OB
333
HAL_FLASH_Lock(); //Locks flash
334
}
335
}
```

该函数简单地获取当前的选项字节（Option Bytes）配置，并检查第一个扇区是否已启用写保护（第 324 行）。如果没有，则启用写保护，以防止引导加载程序（bootloader）被覆盖。

如果您想对该函数进行实验，可以使用 STM32CubeProgrammer 来禁用写保护。

关于自定义引导加载程序的一些考量

![Image from PDF page 608](../images/page-0608-image-01.png)

这里介绍的自定义引导加载程序远非完整。它缺少一些重要功能，而且最重要的是，它不够健壮，无法覆盖错误条件。此外，针对 STM32F0/L0 平台的单一引导加载程序，在使用 GCC -Os 选项编译（该选项生成大小最优化的二进制映像）时，大小约为 13KB。这对于引导加载程序来说太大了。不幸的是，HAL 对最终二进制映像的大小产生了不可忽视的开销。设计良好的引导加载程序会通过将其占用空间（footprint）降至最低来编码。这一方面超出了本书的范围，本书仅展示启动过程背后的基本概念。

<!-- page: 609 -->

### 22.3.1 STM32F0 微控制器中的向量表重定位

到目前为止，我们已经看到，在基于 Cortex-M0 的微控制器中，无法像在 Cortex-M0+/3/4/7 微控制器中那样重定位向量表。这意味着我们不能使用之前看到的代码（第 [154:161] 行）将控制权传递给主固件，因为 Cortex-M0 内核始终期望在地址 0x0000 0000 处找到向量表，而在我们的场景中，这与引导加载程序的向量表重合。

然而，我们可以以某种更巧妙的方式绕过这一限制。我们要分析的想法基于这样一个事实：软件物理重映射允许将 SRAM 内存映射到 0x0000 0000 地址，而原始闪存内存始终可以在 0x0800 0000 地址处访问。因此，我们可以通过简单地将“目标”向量表复制到 SRAM 中，然后执行物理重映射，在将控制权传递给其 Reset 异常处理程序之前重定位主固件的向量表。目标向量表中包含的地址仍然可以在其原始位置访问，从而允许异常处理程序和 ISR 正确执行。

图 22.8 试图表示这一过程。左侧是主应用程序（未显示引导加载程序）。为了简单起见，假设其向量表位于地址 0x0800 2C00。这意味着，从地址 0x0800 2C04 开始，我们有 Cortex-M0 异常处理程序和 ISR 的内存地址。显然，这些地址指向 0x0800 2C00 地址之上的其他内存位置（在图 22.8 中它们表示为灰色箭头）。

![Image from PDF page 609](../images/page-0609-image-01.png)

图 22.8：如何在 STM32F0 微控制器中重定位向量表

<!-- page: 610 -->

## 引导加载程序（bootloader）的工作方式如下。它将向量表复制到 SRAM 内存中，从初始地址 0x2000 0000 开始放置其内容。这意味着从 0x2000 0004 内存位置开始，我们拥有闪存内存中异常处理程序和中断服务程序（ISR）的地址。显然，这些地址仍然指向相同的原始闪存内存位置，如图 22.8 中的黑色箭头所示。在复制过程结束时，内存被重新映射，使得 0x0000 0000 地址现在与 0x2000 0000 地址重合。随后，控制权转移到主固件的重置异常处理程序，并开始执行。通过这种方式，我们绕过了基于 Cortex-M0 的微控制器（MCU）的限制，这些微控制器不允许在内存中重定位向量表。

## 以下代码展示了我们为 STM32F030 微控制器实现的引导加载程序。仅显示了与向量表重定位相关的部分。

```text
Filename: src/main-bootloader.c
146
} else {
147
/* A valid program seems to exist in the second sector: we so prepare the MCU
148
to start the main firmware */
149
MX_GPIO_Deinit(); //Puts GPIOs in default state
150
SysTick->CTRL = 0x0; //Disables SysTick timer and its related interrupt
151
HAL_DeInit();
152
153
RCC->CIR = 0x00000000; //Disable all interrupts related to clock
154
155
uint32_t *pulSRAMBase = (uint32_t*)SRAM_BASE;
156
uint32_t *pulFlashBase = (uint32_t*)APP_START_ADDRESS;
157
uint16_t i = 0;
158
159
do {
160
if(pulFlashBase[i] == 0xAABBCCDD)
161
break;
162
pulSRAMBase[i] = pulFlashBase[i];
163
} while(++i);
164
165
__set_MSP(*((volatile uint32_t*) APP_START_ADDRESS)); //Set the MSP
166
167
SYSCFG->CFGR1 |= 0x3; /* __HAL_RCC_SYSCFG_CLK_ENABLE()
168
already called from HAL_MspInit() */
169
170
/* We are now ready to jump to the main firmware */
171
uint32_t JumpAddress = *((volatile uint32_t*) (APP_START_ADDRESS + 4));
172
void (*reset_handler)(void) = (void*)JumpAddress;
173
reset_handler(); //We start the execution from he Reset_Handler of the main firmware
174
175
for (;;)
176
; //Never coming here
177
}
178
}
```

<!-- page: 611 -->

我们感兴趣的代码从第 155 行开始。定义了两个指针：一个从 SRAM 内存的开头开始（pulSRAMBase），另一个从主固件的开头开始（pulFlashBase，根据前面的示例，其值为 0x0800 2C00）。第 [158:162] 行的循环将向量表复制到 SRAM 中，直到当前闪存内存位置包含值 0xAABBCCDD（稍后会有更多说明）。然后，MSP（主堆栈指针）被设置为 SRAM 的末尾（这应该是多余的，但以防万一……），并执行物理重映射（第 167 行）。随后，控制权转移到主固件。

有几点需要注意。首先，为了简化复制过程并避免向量表被不断增长的堆栈覆盖，向量表从 SRAM 的开头开始复制，而其余的应用数据（由 .data 段、.bss、堆和堆栈组成）则放置在旁边（参见图 22.8）。这要求主固件的链接器脚本正确配置，如下所示：

```text
MEMORY {
FLASH (rx) : ORIGIN = 0x08002C00, LENGTH = 64K - 10K
RAM (xrw) : ORIGIN = 0x200000B8, LENGTH = 8K - 0xB8
```

其次，我们需要一种方法来知道向量表在哪里结束。由于在应用程序中通常不会启用所有 IRQ（中断请求），我们可以在紧跟最后一个使用的 IRQ 之后的第一个向量条目中放置哨兵值 0xAABBCCDD。例如，假设我们的主固件使用中断模式下的 USART2，我们可以看到该 IRQ 是向量表中的第 46 个条目。因此，我们可以将该值放在第 47 个条目中。这可以通过修改文件 startup_stm32f0Xxx.s 轻松实现，如下所示。

```text
Filename: src/startup_stm32f030x8.S
180
.word
SPI1_IRQHandler
/* SPI1
*/
181
.word
SPI2_IRQHandler
/* SPI2
*/
182
.word
USART1_IRQHandler
/* USART1
*/
183
.word
USART2_IRQHandler
/* USART2
*/
184
.word
0xAABBCCDD
/* Reserved
*/
185
.word
0
/* Reserved
*/
186
.word
0
/* Reserved
*/
```

通过这种方式，我们拥有了一种通用且可配置的方法来设置向量表的结束位置。查看前面的链接器脚本片段，我们可以看到我们从 SRAM 内存大小中减去了值 0xB8，即十进制的 184。将 184 除以 4 字节，得到 46，这对应于最后一个向量表条目。

最后，请注意 SYSCFG 是一个独立于 Cortex-M 内核的外设，我们需要通过调用 __HAL_RCC_SYSCFG_CLK_ENABLE() 来启用它。

### 22.3.2 如何使用 flasher.py 工具

如前所述，您可以在本章的书籍源文件中找到一个名为 flasher.py 的 Python 2 脚本。该工具仅允许将使用 Intel

<!-- page: 612 -->

HEX 二进制格式生成的固件上传到 MCU。HEX 格式是 Intel 多年前开发的一种二进制文件规范，至今仍在低成本嵌入式平台中广泛使用。该脚本的源代码在此未显示，但理解其制作方式应该很容易。该脚本需要三个额外的模块：pyserial、IntelHex 和 pycryptodome 库¹⁹。

您可以使用 pip 命令轻松安装它们：

```text
$ sudo pip install intelhex pycryptodome pyserial
```

该脚本设计为在命令行接受两个参数：

- 对应于 Nucleo VCP 的串行端口

- – 在 Windows 中，这等于“COMx”字符串，其中‘x’必须替换为对应于 Nucleo VCP 的 COM 号（例如 COM3）。 – 在 Linux 和 Mac OS 中，这对应于映射在 /dev 路径下的文件（通常类似于 /dev/tty.usbmodemXXXX）。
- 对应于主固件的 HEX 文件的完整路径。

![Image from PDF page 612](../images/page-0612-image-01.jpeg)

图 22.9：Eclipse 构建文件夹中的 HEX 格式二进制文件

默认情况下，GNU MCU Eclipse 工具链会自动生成编译后固件的 HEX 文件。您可以在构建文件夹中找到它：这是一个与活动构建配置同名的 Eclipse 文件夹（通常命名为 Debug 或 Release）。图 22.9 显示了

¹⁹pycryptodome 是一个包含安全哈希函数（如 SHA256 和 RIPEMD160）以及各种加密算法（AES、DES、RSA 等）的集合。它是 Python 中最广泛使用的加密库。IntelHex 是一个小型库，允许轻松操作 Intel HEX 文件。它由 Alexander Belchenko 开发，并在 BSD 许可证下分发。

<!-- page: 613 -->

如果您正在官方书籍示例仓库上工作，则对应于活动配置（CH22-APP1）的构建文件夹。

![Image from PDF page 613](../images/page-0613-image-01.jpeg)

图 22.10：如何推导 HEX 文件的完整路径

您可以通过右键单击 HEX 文件，然后选择“属性”来推导其完整路径。您可以在资源视图中找到完整路径，如图 22.10 所示。
