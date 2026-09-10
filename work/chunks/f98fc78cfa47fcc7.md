<!-- page: 442 -->

## 14.3 Using CubeMX to Configure the I²C Peripheral

As usual, CubeMX reduces to the minimum the effort needed to configure the I²C peripheral. Once the peripheral is enabled in the Category list pane (from the Pinout view), we can configure all settings from the Configuration pane, as shown in Figure 14.13.

<!-- page: 443 -->

![Image from PDF page 443](../images/page-0443-image-01.jpeg)

Figure 14.13: The CubeMX configuration view to setup the I²C peripheral

Read Carefully

![Image from PDF page 443](../images/page-0443-image-02.png)

By default, when enabling the I2C1 peripheral in STM32 MCUs with LQFP-64 packages, CubeMX enables as default peripheral I/Os PB7 and PB6 pins (SDA and SCL respectively). These aren’t the pins latched to the Arduino connector on the Nucleo, but you need to select the two alternative pins PB9 and PB8 by clicking on them and then selecting the corresponding function from the drop-down menu, as shown in the following picture.

![Image from PDF page 443](../images/page-0443-image-03.jpeg)

Figure 14.14: How to select the right I2C1 pins in a Nucleo-64 board
