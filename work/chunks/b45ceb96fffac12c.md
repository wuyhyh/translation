<!-- page: 36 -->

### Compiler will generate the following ARM assembly code²:

```text
1
movs
r3, #3
;move "3" in register r3
2
strb
r3, [r7, #7] ;store the content of r3 in "a"
3
movs
r3, #2
;move "2" in register r3
4
strb
r3, [r7, #6] ;store the content of r3 in "b"
5
ldrb
r2, [r7, #7] ;load the content of "a" in r2
6
ldrb
r3, [r7, #6] ;load the content of "b" in r3
7
smulbb
r3, r2, r3
;multiply "a" with "b" and store result in r3
8
strb
r3, [r7, #5] ;store the result in "c"
```

As we can see, all the operations always involve a register. Instructions at lines 1-2 move the number 3 into the register r3 and then store its content (that is, the number 3) inside the memory location given by the register r7 plus an offset of 7 memory locations - that is the place where a variable is stored. The same happens for the variable b at lines 3-4. Then lines 5-7 load the content of variables a and b and perform the multiplication. Finally, line 8 stores the result in the memory location of variable c.

![Image from PDF page 36](../images/page-0036-image-01.jpeg)

Figure 1.3: Cortex-M fixed memory address space

²That assembly code was generated compiling in thumb mode with any optimization disabled, invoking GCC in the following way: $ arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -fverbose-asm -save-temps -O0 -g -c file.c

<!-- page: 37 -->

#### 1.1.1.2 Memory Map

ARM defines a standardized memory address space common to all Cortex-M cores, which ensures code portability among different silicon manufacturers. The address space is 4GB wide, and it is organized in several sub-regions with different logical functionalities. Figure 1.3 shows the memory layout of a Cortex-M processor ³.

The first 512MB are dedicated to code area. STM32 devices further divide this area in some subregions as shown in Figure 1.4. Let us briefly introduce them.

![Image from PDF page 37](../images/page-0037-image-01.jpeg)

Figure 1.4: Memory layout of Code Area on STM32 MCUs

All Cortex-M processors map the code area starting at address 0x0000 0000⁴. This area also includes the pointer to the beginning of the stack (usually placed in SRAM) and the vector table, as we will see in Chapter 7. The position of the code area is standardized among all other Cortex-M vendors, even if the core architecture is sufficiently flexible to allow manufacturers to arrange this area in a different way. In fact, for all STM32 devices an area starting at address 0x0800 0000 is bound to the internal MCU flash memory, and it is the area where program code resides. However, thanks to a specific boot configuration we will explore in Chapter 22, this area is also aliased from address 0x0000 0000. This means that it is perfectly possible to refer to the content of the flash memory both starting at address 0x0800 0000 and 0x0000 0000 (for example, a routine located at address 0x0800

³Although the memory layout and the size of sub-regions (and therefore also their addresses) are standardized between all Cortex-M cores, some functionalities may differ. For example, Cortex-M7 does not provide bit-band regions, and some peripherals in the Private Peripheral Bus region differ. Always consult the reference manual for the architecture you are considering. ⁴To increase readability, all 32-bit addresses in this book are written splitting the upper two bytes from the lower ones. So, every time you see an address expressed in this way (0x0000 0000) you have to interpret it just as one common 32-bit address (0x00000000). This rule does not apply to C and assembly source code.

<!-- page: 38 -->

16DC can also be accessed from 0x0000 16DC).

The last two sections are dedicated to System memory and Option bytes. The first one is a ROM region reserved to bootloaders. Each STM32 family (and their sub-families - low density, medium density, and so on) provides a bootloader pre-programmed into the chip during production. As we will see in Chapter 22, this bootloader can be used to load code from several peripherals, including USARTs, USB and CAN bus. The Option bytes region contains a series of bit flags which can be used to configure several aspects of the MCU (such as flash read protection, hardware watchdog, boot mode and so on) and are related to the specific STM32 microcontroller.

Going back to the whole 4GB address space, the next main region is the one bounded to the internal MCU SRAM. It starts at address 0x2000 0000 and can potentially extend to 0x3FFF FFFF. However, the actual end address depends on the effective amount of internal SRAM. For example, in the case of an STM32F103RB MCU with 20KB of SRAM, we have a final address of 0x2000 4FFF⁵. Trying to access a location outside of this area will cause a Bus Fault exception (more about this later).

The next 0.5GB of memory is dedicated to the mapping of peripherals. Every peripheral provided by the MCU (timers, I²C and SPI interfaces, USARTs, and so on) has an alias in this region. It is up to the specific MCU to organize this memory space.

The next 2GB area is dedicated to external SRAM or flash. Cortex-M devices can execute code and load/store data from external memory, which extend the internal memory resources, through the EMI/FSMC interface. Some STM32 devices, like the STM32F7, are able to execute code from external memory without performance bottlenecks, thanks to an L1 cache and the ARTTM Accelerator.

The final 0.5 GB of memory is allocated to the internal (core) Cortex processor peripherals, plus a reserved area for future enhancements to Cortex processors. All Cortex processor registers are at fixed locations for all Cortex-based microcontrollers. This allows code to be more easily ported between different STM32 variants and indeed other vendors’ Cortex-based microcontrollers.
