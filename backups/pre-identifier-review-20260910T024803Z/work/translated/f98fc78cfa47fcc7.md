<!-- page: 442 -->

## 14.3 使用 CubeMX 配置 I²C 外设

一如既往，CubeMX 将配置 I²C 外设所需的工作量降至最低。一旦在引脚布局视图（Pinout view）的分类列表窗格中启用了该外设，我们就可以在配置窗格中设置所有参数，如图 14.13 所示。

<!-- page: 443 -->

![Image from PDF page 443](../images/page-0443-image-01.jpeg)

图 14.13：用于设置 I²C 外设的 CubeMX 配置视图

仔细阅读

![Image from PDF page 443](../images/page-0443-image-02.png)

默认情况下，在具有 LQFP-64 封装的 STM32 微控制器中启用 I2C1 外设时，CubeMX 会默认启用 PB7 和 PB6 引脚作为外设 I/O（分别为 SDA 和 SCL）。这些引脚并非 Nucleo 开发板上连接到 Arduino 接口的引脚，因此您需要点击 PB9 和 PB8 这两个替代引脚，然后从下拉菜单中选择相应的功能，如下图所示。

![Image from PDF page 443](../images/page-0443-image-03.jpeg)

图 14.14：如何在 Nucleo-64 开发板上选择正确的 I2C1 引脚
