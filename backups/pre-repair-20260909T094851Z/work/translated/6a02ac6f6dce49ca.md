<!-- page: 38 -->

#### 1.1.1.3 位带操作 (Bit-Banding)

在嵌入式应用中，使用位掩码（bit masking）处理字（word）中的单个位是非常常见的。例如，假设我们要设置或清除无符号字节（unsigned byte）的第 3 位（即 bit 2）。我们可以简单地使用以下 C 代码来实现：

```text
...
uint8_t temp = 0;
temp |= 0x4;
temp &= ~0x4;
...
```

当我们希望节省内存空间（使用单个变量并为其每一位赋予不同的含义）或者必须处理微控制器（microcontroller）内部寄存器（register）和外围设备时，会使用位掩码。

⁵最终地址的计算方式如下：20K 等于 20 * 1024 字节，在十六进制中为 0x5000。但由于地址从 0 开始，因此最终地址是 0x2000 0000 + 0x4FFF。

<!-- page: 39 -->

考虑上述 C 代码，我们可以看到编译器将生成以下 ARM 汇编代码⁶：

```text
#temp |= 0x4;
a:
79fb
ldrb
r3, [r7, #7]
c:
f043 0304
orr.w
r3, r3, #4
10:
71fb
strb
r3, [r7, #7]
#temp &= ~0x4;
12:
79fb
ldrb
r3, [r7, #7]
14:
f023 0304
bic.w
r3, r3, #4
18:
71fb
strb
r3, [r7, #7]
```

如我们所见，如此简单的操作需要三条汇编指令（取数、修改、保存）。这导致了两种类型的问题。首先，这三条指令造成了 CPU 周期的浪费。其次，如果 CPU 处于单任务模式且只有一个执行流，该代码工作正常；但如果我们处理的是并发执行，另一个任务（或仅仅是中断（interrupt）例程）可能会在我们完成“位掩码”操作之前影响内存内容（例如，在上述汇编代码中，中断发生在第 0xC-0x10 行或 0x14-0x18 行指令之间）。

位带操作（Bit-banding）是一种将给定内存区域的每一位映射到别名位带内存区域（aliased bit-banding memory region）中一个完整字（word）的能力，从而允许对该位进行原子访问。图 1.5 展示了 Cortex 内核（core）如何将内存地址 0x2000 0000 的内容映射到位带区域 0x2200 0000-1c。例如，如果我们想要修改 0x2000 0000 内存位置（bit 2），我们只需访问 0x2200 0008 内存位置即可。

![Image from PDF page 39](../images/page-0039-image-01.jpeg)

图 1.5：SRAM 地址 0x2000 0000 在位带区域中的内存映射（显示前 8 个 32 位字）

计算别名区域地址的公式如下：

```text
bit_band_address = alias_region_base + (region_base_offset x 32) + (bit_number x 4)
```

⁶该汇编代码是在 Thumb 模式下编译生成的，未启用任何优化，调用 GCC 的方式如下：$ arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -fverbose-asm -save-temps -O0 -g -c file.c

<!-- page: 40 -->

例如，考虑图 1.5 中的内存地址，要访问 bit 2：

```text
alias_region_base = 0x22000000
region_base_offset = 0x20000000 - 0x20000000 = 0
bit_band_address = 0x22000000 + 0*32 + (0x2 x 0x4) = 0x22000008
```

ARM 为基于 Cortex-M3/4 的微控制器定义了两个位带区域，每个区域宽 1MB，并映射到一个 32Mbit 的位带别名区域。别名内存区域中每个连续的 32 位字对应位带区域中每个连续的位（这解释了尺寸关系：1Mbit <-> 32Mbit）。第一个区域从 0x2000 0000 开始，到 0x200F FFFF 结束，并从 0x2200 0000 映射到 0x23FF FFFF。它专门用于 SRAM 内存位置的位访问。另一个位带区域从 0x4000 0000 开始，到 0x400F FFFF 结束，如图 1.6 所示。

![Image from PDF page 40](../images/page-0040-image-01.jpeg)

图 1.6：内存映射和位带区域

这个区域专门用于外围设备的内存映射。例如，ST 将 GPIOA 外围设备的 GPIO 输出数据寄存器（GPIO->ODR）映射到 0x4002 0014。这意味着地址 0x4002 0014 处的字的每一位都允许修改 GPIO 的输出状态（从低电平到高电平，反之亦然）。因此，如果我们想要修改 GPIOA 端口的 PIN5 的状态⁷，使用之前的公式，我们有：

```text
alias_region_base = 0x42000000
region_base_offset = 0x40020014 - 0x40000000 = 0x20014
bit_band_address = 0x42000000 + 0x20014*32 + (0x5 x 0x4) = 0x42400294
```

我们可以在 C 中定义两个宏，以便轻松计算位带别名地址：

⁷任何已经玩过 Nucleo 开发板的人都知道，用户 LED LD2（绿色那个）连接到该端口引脚。

<!-- page: 41 -->

```text
1
// 定义位带基地址
2
#define BITBAND_SRAM_BASE 0x20000000
3
// 定义别名带基地址
4
#define ALIAS_SRAM_BASE 0x22000000
5
// 将 SRAM 地址转换为别名区域
6
#define BITBAND_SRAM(a,b) ((ALIAS_SRAM_BASE + ((uint32_t)&(a)-BITBAND_SRAM_BASE)*32 + (b*4)))
```

7

```text
8
// 定义外围设备位带基地址
9
#define BITBAND_PERI_BASE 0x40000000
10
// 定义外围设备别名带基地址
11
#define ALIAS_PERI_BASE 0x42000000
12
// 将 PERI 地址转换为别名区域
13
#define BITBAND_PERI(a,b) ((ALIAS_PERI_BASE + ((uint32_t)a-BITBAND_PERI_BASE)*32 + (b*4)))
```

继续使用上面的例子，我们可以快速修改 GPIOA 端口 PIN5 的状态，如下所示：

```text
1
#define GPIOA_PERH_ADDR 0x40020000
2
#define ODR_ADDR_OFF
0x14
```

3

```text
4
uint32_t *GPIOA_ODR = GPIOA_PERH_ADDR + ODR_ADDR_OFF;
5
uint32_t *GPIOA_PIN5 = BITBAND_PERI(GPIOA_ODR, 5);
```

6

```text
7
*GPIOA_PIN5 = 0x1; // 将 GPIO 设置为高电平
```
