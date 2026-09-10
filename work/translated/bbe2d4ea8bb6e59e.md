<!-- page: 428 -->

允许使用直接存储器访问（DMA）执行 I²C 事务。

为了构建完整且可运行的示例，我们需要一个能够通过 I²C 总线进行交互的外部设备，因为 Nucleo 开发板本身不提供此类外设。因此，我们将使用外部 EEPROM 存储器：24LCxx 系列。这是一个流行的串行 EEPROM 系列，在电子行业中已成为一种标准。它们价格低廉（通常只需几美分），提供多种封装形式（从传统的 THT P-DIP 封装到现代紧凑的 WLCP 封装），数据保持时间超过 200 年，且单个页面可擦除超过一百万次。此外，许多硅片制造商都提供兼容版本（ST 也提供其自己的 24LCxx 兼容 EEPROM 系列）。这些存储器的普及程度堪比 555 定时器，我敢打赌它们将在技术创新中存续多年。

![Image from PDF page 428](../images/page-0428-image-01.png)

图 14.6：采用 PDIP-8 封装的 24LCxx EEPROM 引脚图

我们的示例将基于 24LC64 型号，这是一款 64Kbits 的 EEPROM（这意味着存储器能够存储 8KB，或者换句话说，8192 字节）。PDIP-8 版本的引脚图如图 14.6 所示。A0、A1 和 A2 用于设置 I²C 地址的最低有效位（LSB），如图 14.7 所示：如果其中一个引脚接地，则对应的位被设置为 0；如果连接到 VDD，则位被设置为 1。如果这三个引脚都接地，则 I²C 地址对应于 0xA0。

![Image from PDF page 428](../images/page-0428-image-02.png)

图 14.7：24LCxx I²C 地址的组成方式。

WP 引脚是写保护引脚：如果接地，我们可以写入单个存储单元。相反，如果连接到 VDD，写操作将无效。由于 I2C1 外设

<!-- page: 429 -->

在所有 Nucleo 开发板上都映射到相同的引脚，图 14.8 展示了在本书中考虑的九种 Nucleo 开发板上将 24LCxx EEPROM 连接到 Arduino 接口的正确方式。

![Image from PDF page 429](../images/page-0429-image-01.png)

仔细阅读

![Image from PDF page 429](../images/page-0429-image-02.png)

STM32F1 微控制器不提供上拉 SDA 和 SCL 线的功能。其 GPIO 必须配置为开漏模式。因此，您需要添加两个额外的电阻来上拉 I²C 线。4K 到 10K 之间是经过验证的有效值。

![Image from PDF page 429](../images/page-0429-image-03.png)

如前所述，64Kbits 的 EEPROM 有 8192 个地址，范围从 0x0000 到 0x1FFF。单个字节写入是通过在 I²C 总线上发送 EEPROM 地址、内存地址的高半部分、低半部分以及要存储在该单元中的值来完成的，并以 STOP 条件结束事务。

![Image from PDF page 429](../images/page-0429-image-04.jpeg)

图 14.8：如何将 Nucleo 连接到 24LCxx EEPROM

假设我们要将值 0x4C 存储在内存位置 0x320 中，那么图 14.9 展示了正确的事务序列。地址 0x320 分为两部分：等于 0x3 的高位部分首先传输，等于 0x20 的低位部分紧随其后发送。然后发送要存储的数据。我们也可以在同一个事务中发送多个字节：内部地址计数器会在每发送一个字节后自动递增。这允许我们减少事务时间并提高总吞吐量。

I²C EEPROM 在最后一个发送字节后设置的 ACK 位并不意味着数据已有效存储在内存中。发送的数据存储在临时缓冲区中，因为 EEPROM 位置存储器是按页擦除的，而不是单独擦除的。整个页面（由 32 字节组成）在每次写操作时都会刷新，传输的字节仅在该操作结束时存储。在擦除期间，发送到 EEPROM 的任何命令都将被

<!-- page: 430 -->

忽略。为了检测写操作何时完成，我们需要使用应答轮询。这涉及主设备发送 START 条件，随后发送从设备地址以及写命令的控制字节（R/W 位设置为 0）。如果设备仍忙于写周期，则不会返回 ACK。如果没有返回 ACK，必须重新发送 START 位和控制字节。如果周期完成，设备将返回 ACK，主设备随后可以继续下一个读或写命令。

![Image from PDF page 430](../images/page-0430-image-01.png)

图 14.9：如何使用 24LCxx EEPROM 执行写操作

读操作的发起方式与写操作相同，区别在于控制字节的 R/W 位设置为 1。有三种基本的读操作类型：当前地址读、随机读和顺序读。在本书中，我们将只关注随机读模式，留给读者深入理解其他模式。

随机读操作允许主设备以随机方式访问任何内存位置。要执行这种类型的读操作，必须首先发送内存地址。这是通过将内存地址作为写操作的一部分（R/W 位设置为 ‘0’）发送给 24LCxx 来实现的。一旦发送了内存地址，主设备在 ACK¹³ 之后生成 RESTART 条件（重复 START）。这终止了写操作，但在内部地址计数器设置之前不会终止。然后主设备再次发出从设备地址，但这次将 R/W 位设置为 1。24LCxx 随后发出 ACK 并传输 8 位数据字。主设备不应答传输并生成 STOP 条件，这导致 EEPROM 停止传输（见图 14.10）。在随机读命令之后，内部地址计数器将指向刚刚读取的地址之后的地址位置。

![Image from PDF page 430](../images/page-0430-image-02.png)

图 14.10：如何使用 24LCxx EEPROM 执行随机读操作

我们终于准备好安排一个完整的示例了。我们将创建两个简单的函数，命名为 Read_From_24LCxx() 和 Write_To_24LCxx()，允许使用 CubeHAL 从 24LCxx 存储器中写入/读取数据。然后我们将通过简单地将一个字符串存储在 EEPROM 中，然后将其读回来，来测试这些例程：如果原始字符串等于从 EEPROM 读取的字符串，则 Nucleo LD2 LED 开始闪烁。

¹³24LCxx EEPROM 存储器被设计为即使我们通过发出 STOP 条件结束事务，然后立即以读模式开始新事务，也能以相同的方式工作。这种灵活性将允许我们构建本章的第一个示例，我们稍后会看到。

<!-- page: 431 -->

```text
Filename: src/main-ex1.c
14
int main(void) {
15
const char wmsg[] = "We love STM32!";
16
char rmsg[20] = {0};
```

17

```text
18
HAL_Init();
19
Nucleo_BSP_Init();
```

20

```text
21
MX_I2C1_Init();
```

22

```text
23
Write_To_24LCxx(&hi2c1, 0xA0, 0x1AAA, (uint8_t*)wmsg, strlen(wmsg)+1);
24
Read_From_24LCxx(&hi2c1, 0xA0, 0x1AAA, (uint8_t*)rmsg, strlen(wmsg)+1);
```

25

```text
26
if(strcmp(wmsg, rmsg) == 0) {
27
while(1) {
28
HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
29
HAL_Delay(100);
30
}
31
}
```

32

```text
33
while(1);
34
}
```

35

```text
36
/* I2C1 init function */
37
static void MX_I2C1_Init(void) {
38
GPIO_InitTypeDef GPIO_InitStruct;
```

39

```text
40
/* Peripheral clock enable */
41
__HAL_RCC_I2C1_CLK_ENABLE();
```

42
