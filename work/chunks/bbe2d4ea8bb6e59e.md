<!-- page: 428 -->

allow to perform I²C transactions using DMA.

To make complete and full working examples we need an external device able to interact through the I²C bus, since Nucleo boards do not provide such peripherals. For this reason, we will use an external EEPROM memory: the 24LCxx. This is a popular family of serial EEPROMs, which are become a sort of standard in electronics industry. They are cheap (cost usually few tens of cents), they are produced in several packages (ranging from “old” THT P-DIP packages, up to modern and compact WLCP ones), they provide a data retention for more than 200 years and individual pages can be erased more than one million of times. Moreover, a lot of silicon manufacturers have their own compatible versions (ST also provides its own set of 24LCxx compatible EEPROMs). These memories have the same popularity of 555 timers, and I bet that they will survive for a lot of years to technology innovation.

![Image from PDF page 428](../images/page-0428-image-01.png)

Figure 14.6: The pinout of a 24LCxx EEPROM with a PDIP-8 package

Our examples will be based on the 24LC64 model, which is a 64Kbits EEPROM (this means that the memory is able to store 8KB or, if you prefer, 8192 bytes). The pinout of the PDIP-8 version is shown in Figure 14.6. A0, A1 and A2 are used to set the LSB bits of the I²C address, as shown in Figure 14.7: if one of those pins is tied to the ground, then the corresponding bit is set to 0; if tied to VDD, then the bit is set to 1. If all three pins are tied to the ground, then the I²C address corresponds to 0xA0.

![Image from PDF page 428](../images/page-0428-image-02.png)

Figure 14.7: How the 24LCxx I²C address is composed.

WP pin is the write protection pin: if tied to the ground, we can write inside individual memory cells. On the contrary, if connected to VDD, write operations have no effects. Since I2C1 peripheral

<!-- page: 429 -->

is mapped to the same pins in all Nucleo boards, Figure 14.8 shows the right way to connect a 24LCxx EEPROM to the Arduino connector in all nine Nucleo boards we are considering in this book.

![Image from PDF page 429](../images/page-0429-image-01.png)

Read Carefully

![Image from PDF page 429](../images/page-0429-image-02.png)

STM32F1 microcontrollers do not provide the ability to pull-up SDA and SCL lines. Their GPIOs must be configured as open-drain. So, you have to add two additional resistors to pull-up I²C lines. Something between 4K and 10K is a proven value.

![Image from PDF page 429](../images/page-0429-image-03.png)

As said before, a 64Kbits EEPROM has 8192 addresses, ranging from 0x0000 up to 0x1FFF. An individual byte write is performed by sending over the I²C bus the EEPROM address, the upper half of the memory address followed by the lower half, and the value to store in that cell, closing the transaction with a STOP condition.

![Image from PDF page 429](../images/page-0429-image-04.jpeg)

Figure 14.8: How to connect a Nucleo to a 24LCxx EEPROM

Assuming we want to store the value 0x4C inside the memory location 0x320, then Figure 14.9 shows the right transaction sequence. The address 0x320 is split in two parts: the upper part, equal to 0x3 is transmitted first, and the lower part equal to 0x20 is sent right after. Then the data to store is sent. We can also send multiple bytes in the same transaction: an internal address counter automatically increments at every byte sent. This allows us to reduce the transaction time and increase the total throughput.

The ACK bit set by the I²C EEPROM after the last sent byte does not mean that data has been effectively stored inside the memory. Sent data is stored in a temporarily buffer, since EEPROM location memories are erased page-by-page and not individually. The whole page (which is composed by 32 bytes) is refreshed at every write operation, and the transferred bytes are stored only at the end of this operation. During the erase time, every command sent to the EEPROM will

<!-- page: 430 -->

be ignored. To detect when a write operation has been completed, we need to use the acknowledge polling. This involves the master sending a START condition followed by slave address plus the control byte for a write command (R/W bit set to 0). If the device is still busy with the write cycle, then no ACK will be returned. If no ACK is returned, the START bit and control byte must be re-sent. If the cycle is complete, the device will return the ACK and the master can then proceed with the next read or write command.

![Image from PDF page 430](../images/page-0430-image-01.png)

Figure 14.9: How to perform a write operation with a 24LCxx EEPROM

Read operations are initiated in the same way as write operations, with the exception that the R/W bit of the control byte is set to 1. There are three basic types of read operations: current address read, random read and sequential read. In this book we will focus our attention on the random read mode only, leaving to the reader the responsibility to deepen the other modes.

Random read operations allow the master to access any memory location in a random manner. To perform this type of read operation, the memory address must be sent first. This is accomplished by sending the memory address to the 24LCxx as part of a write operation (R/W bit set to ‘0’). Once the memory address is sent, the master generates a RESTART condition (repeating START) following the ACK¹³. This terminates the write operation, but not before the internal address counter is set. The master then issues the slave address again, but with the R/W bit set to a 1 this time. The 24LCxx will then issue an ACK and transmit the 8-bit data word. The master will not acknowledge the transfer and generates a STOP condition, which causes the EEPROM to discontinue transmission (see Figure 14.10). After a random read command, the internal address counter will point to the address location following the one that was just read.

![Image from PDF page 430](../images/page-0430-image-02.png)

Figure 14.10: How to perform a random read operation with a 24LCxx EEPROM

We are finally ready to arrange a complete example. We will create two simple functions, named Read_From_24LCxx() and Write_To_24LCxx() that allow to write/read data from a 24LCxx memory, using the CubeHAL. We will then test these routines by simply storing a string inside the EEPROM, and then reading it back: if the original string is equal to the one read from the EEPROM, then the Nucleo LD2 LED starts blinking.

¹³The 24LCxx EEPROM memories are designed so that they work in the same way even if we end the transaction by issuing a STOP condition, and then we immediately start a new one in read mode. This degree of flexibility we will allow us to build the first example of this chapter, as we will see in a while.

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
