<!-- page: 38 -->

#### 1.1.1.3 Bit-Banding

In embedded applications, it is quite common to work with single bits of a word using bit masking. For example, suppose that we want to set or clear the 3rd bit (bit 2) of an unsigned byte. We can simply do this using the following C code:

```text
...
uint8_t temp = 0;
temp |= 0x4;
temp &= ~0x4;
...
```

Bit masking is used when we want to save space in memory (using one single variable and assigning a different meaning to each of its bits) or we have to deal with internal MCU registers and peripherals.

⁵The final address is computed in the following way: 20K is equal to 20 * 1024 bytes, which in base 16 is 0x5000. But addresses start from 0, hence the final address is 0x2000 0000 + 0x4FFF.

<!-- page: 39 -->

Considering the previous C code, we can see that the compiler will generate the following ARM assembly code⁶:

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

As we can see, such a simple operation requires three assembly instructions (fetch, modify, save). This leads to two types of problems. First of all, there is a waste of CPU cycles related to those three instructions. Second, that code works fine if the CPU is working in single task mode, and we have just one execution stream, but, if we are dealing with concurrent execution, another task (or simply an interrupt routine) may affect the content of the memory before we complete the “bit mask” operation (that is, for example, an interrupt occurs between instructions at lines 0xC-0x10 or 0x14-0x18 in the above assembly code).

Bit-banding is the ability to map each bit of a given area of memory to a whole word in the aliased bit-banding memory region, allowing atomic access to such bit. Figure 1.5 shows how the Cortex CPU aliases the content of memory address 0x2000 0000 to the bit-banding region 0x2200 0000-1c. For example, if we want to modify (bit 2) of 0x2000 0000 memory location we can simply access to 0x2200 0008 memory location.

![Image from PDF page 39](../images/page-0039-image-01.jpeg)

Figure 1.5: Memory mapping of SRAM address 0x2000 0000 in bit-banding region (first 8 of 32 bits shown)

This is the formula to compute the addresses for alias regions:

```text
bit_band_address = alias_region_base + (region_base_offset x 32) + (bit_number x 4)
```

⁶That assembly code was generated compiling in thumb mode with any optimization disabled, invoking GCC in the following way: $ arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -fverbose-asm -save-temps -O0 -g -c file.c

<!-- page: 40 -->

For example, considering the memory address of Figure 1.5, to access bit 2 :

```text
alias_region_base = 0x22000000
region_base_offset = 0x20000000 - 0x20000000 = 0
bit_band_address = 0x22000000 + 0*32 + (0x2 x 0x4) = 0x22000008
```

ARM defines two bit-band regions for Cortex-M3/4 based MCUs, each one is 1MB wide and mapped to a 32Mbit bit-band alias region. Each consecutive 32-bit word in the “alias” memory region refers to each consecutive bit in the “bit-band” region (which explains that size relationship: 1Mbit <-> 32Mbit). The first one starts at 0x2000 0000 and ends at 0x200F FFFF, and it is aliased from 0x2200 0000 to 0x23FF FFFF. It is dedicated to the bit access of SRAM memory locations. Another bitbanding region starts at 0x4000 0000 and ends at 0x400F FFFF, as shown in Figure 1.6.

![Image from PDF page 40](../images/page-0040-image-01.jpeg)

Figure 1.6: Memory map and bit-banding regions

This other region is dedicated to the memory mapping of peripherals. For example, ST maps the GPIO Output Data Register (GPIO->ODR) of GPIOA peripheral from 0x4002 0014. This means that each bit of the word addressed at 0x4002 0014 allows modifying the output state of a GPIO (from LOW to HIGH and vice versa). So if we want to modify the status of PIN5 of GPIOA port⁷, using the previous formula we have:

```text
alias_region_base = 0x42000000
region_base_offset = 0x40020014 - 0x40000000 = 0x20014
bit_band_address = 0x42000000 + 0x20014*32 + (0x5 x 0x4) = 0x42400294
```

We can define two macros in C that allow to easily compute bit-band alias addresses:

⁷Anyone who has already played with Nucleo boards, knows that user LED LD2 (the green one) is connected to that port pin.

<!-- page: 41 -->

```text
1
// Define base address of bit-band
2
#define BITBAND_SRAM_BASE 0x20000000
3
// Define base address of alias band
4
#define ALIAS_SRAM_BASE 0x22000000
5
// Convert SRAM address to alias region
6
#define BITBAND_SRAM(a,b) ((ALIAS_SRAM_BASE + ((uint32_t)&(a)-BITBAND_SRAM_BASE)*32 + (b*4)))
```

7

```text
8
// Define base address of peripheral bit-band
9
#define BITBAND_PERI_BASE 0x40000000
10
// Define base address of peripheral alias band
11
#define ALIAS_PERI_BASE 0x42000000
12
// Convert PERI address to alias region
13
#define BITBAND_PERI(a,b) ((ALIAS_PERI_BASE + ((uint32_t)a-BITBAND_PERI_BASE)*32 + (b*4)))
```

Still using the above example, we can quickly modify the state of PIN5 of the GPIOA port as follows:

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
*GPIOA_PIN5 = 0x1; // Turns GPIO HIGH
```
