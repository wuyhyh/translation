<!-- page: 421 -->

### 14.1.2 Availability of I²C Peripherals in STM32 MCUs

Depending on the family type and package used, STM32 microcontrollers can provide up to four independent I²C peripherals. Table 14.1 summarizes the availability of I²C peripherals in STM32 MCUs equipping all nine Nucleo boards we are considering in this book.

<!-- page: 422 -->

![Image from PDF page 422](../images/page-0422-image-01.png)

Table 14.1: Effective availability of I²C peripherals in MCUs equipping all nine Nucleo boards

For every I²C peripheral, and a given STM32 MCU, Table 14.1 shows the pins corresponding to SDA and SCL lines. Moreover, darker rows show alternate pins that can be used during the layout of the board. For example, given the STM32F401RE MCU, we can see that I2C1 peripheral is mapped to PB7 and PB6, but PB9 and PB8 can be also used as alternate pins. Note that the I2C1 peripheral uses the same I/O pins in all STM32 MCUs with LQFP-64 package. This is a paramount example of the pin-to-pin compatibility offered by STM32 microcontrollers.

We are now ready to see how-to use the CubeHAL APIs to program this peripheral.

## 14.2 HAL_I2C Module

To program the I²C peripheral, the CubeHAL defines the C struct I2C_HandleTypeDef, which is defined in the following way:

<!-- page: 423 -->

```text
typedef struct {
I2C_TypeDef
*Instance;
/* I²C registers base address
*/
I2C_InitTypeDef
Init;
/* I²C communication parameters
*/
uint8_t
*pBuffPtr;
/* Pointer to I²C transfer buffer */
uint16_t
XferSize;
/* I²C transfer size
*/
__IO uint16_t
XferCount;
/* I²C transfer counter
*/
DMA_HandleTypeDef
*hdmatx;
/* I²C Tx DMA handle parameters
*/
DMA_HandleTypeDef
*hdmarx;
/* I²C Rx DMA handle parameters
*/
HAL_LockTypeDef
Lock;
/* I²C locking object
*/
__IO HAL_I2C_StateTypeDef
State;
/* I²C communication state
*/
__IO HAL_I2C_ModeTypeDef
Mode;
/* I²C communication mode
*/
__IO uint32_t
ErrorCode;
/* I²C Error code
*/
} I2C_HandleTypeDef;
```

## Let us analyze the most important fields of this C struct.

## - Instance: is the pointer to the I²C descriptor we are going to use. For example, I2C1 is the descriptor of the first I²C peripheral.
- Init: is an instance of the C struct I2C_InitTypeDef used to configure the peripheral. We will study it more in depth in a while.
- pBuffPtr: pointer to the internal buffer used to temporarily store data transferred to and from the I²C peripheral. This is used when the I²C works in interrupt mode and should be not modified from the user code.
- hdmatx, hdmarx: pointer to instances of the DMA_HandleTypeDef struct used when the I²C peripheral works in DMA mode.

## The setup of the I²C peripheral is performed by using an instance of the C struct I2C_InitTypeDef, which is defined in the following way:

```text
typedef struct {
uint32_t ClockSpeed;
/* Specifies the clock frequency */
uint32_t DutyCycle;
/* Specifies the I²C fast mode duty cycle. */
uint32_t OwnAddress1;
/* Specifies the first device own address. */
uint32_t OwnAddress2;
/* Specifies the second device own address if dual addressing
mode is selected */
uint32_t AddressingMode;
/* Specifies if 7-bit or 10-bit addressing mode is selected. */
uint32_t DualAddressMode; /* Specifies if dual addressing mode is selected. */
uint32_t GeneralCallMode; /* Specifies if general call mode is selected. */
uint32_t NoStretchMode;
/* Specifies if nostretch mode is selected. */
} I2C_InitTypeDef;
```

## These are the functions of the most relevant fields of this C struct.

## - ClockSpeed: this field specifies the speed of the I²C interface and it should correspond to bus speeds defined in the I²C specifications (standard mode, fast mode, and so on). However, the

<!-- page: 424 -->

exact value of this field is also a function of the DutyCycle one, as we will see next. The maximum value for this field is 400000 (400kHz) for that STM32 MCUs supporting up to the fast mode. More recent STM32 families support also the fast mode plus (1MHz). In these other MCUs, ClockSpeed field is replaced with another one called Timing. The configuration value for the Timing field is computed differently, and we will not cover it here. ST provides a dedicated application note (AN4235¹⁰) that explains how to compute the exact value for this field according to the wanted I²C bus speed. However, CubeMX is able to generate the right configuration value for you.

![Image from PDF page 424](../images/page-0424-image-01.png)

Table 14.2: Characteristics of the SDA and SCL bus lines for standard, fast, and fast-mode plus I²C-bus devices

- DutyCycle: this field, which is available only in those MCU not supporting the fast mode plus communication speed, specifies the ratio between tLOW and tHIGH of the I²C SCL line. It can assume the values I2C_DUTYCYCLE_2 and I2C_DUTYCYCLE_16_9 to indicate a duty cycle equal to 2:1 and 16:9. By choosing a given clock duty we can “prescale” the peripheral clock to achieve the wanted I²C clock speed. To better understand the role of this configuration parameter, we need to review some fundamental concepts of the I²C bus. In Chapter 11 we have seen that the duty cycle is the percentage of one period of time (for example, 10μs) in which a signal is active. For every I²C bus speed, the I²C specification precisely defines the minimum tLOW and tHIGH values. Table 14.2, extracted from the UM10204 by NXP¹¹, shows tLOW and tHIGH values for the given communication speed (values have been highlighted in yellow in Table 14.2). The ratio of these two values is the duty cycle, which is independent of the communication speed. For example, a 100kHz period corresponds to 10μs, but tHIGH +tLOW from the Table 14.2 is less than 10μs (4μs+4.7μs=8.7μs). Thus, the ratio of the actual values can vary as long as the tLOW and tHIGH minimum timings are met (4.7μs and 4μs respectively). The point of these ratios is to illustrate that I²C timing constraints are different between I²C modes. They aren’t mandatory ratios that STM32 I²C peripherals need to keep. For example, tHIGH = 4s and tLOW = 6s would be a 0.67 ratio, which is still compatible with timings of the standard mode (100kHz) (because tHIGH = 4s and tLOW > 4.7s, and their sum is equal to 10μs). The I²C peripherals in STM32 MCUs define the following duty cycles (ratios). For standard mode the ratio is fixed to 1:1. This means that tLOW = tHIGH = 5s. For fast mode we can use two ratios: 2:1 or 16:9. 2:1 ratio means that 4μs (=400kHz) are obtained with tLOW = 2.66s and tHIGH = 1.33s and both the values are higher than the one reported in Table 14.2 (0.6μs and 1.3μs). A 16:9 ratio means that 4μs are obtained with tLOW = 2.56s and tHIGH = 1.44s and both the values are still higher than the one reported in Table 14.2. When to use a 2:1 ratio instead of the 16:9 one and vice

¹⁰https://bit.ly/2bxBoP1 ¹¹https://bit.ly/3E18iPF

<!-- page: 425 -->
