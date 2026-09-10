<!-- page: 157 -->

## 请注意，本示例假设项目是按照第 3 章中所示的相同步骤生成的。如果现在并非所有内容都清晰明了，请不要担心：在阅读完第 8 章后，您将能够理解所执行的每一项操作。

<!-- page: 158 -->

![Image from PDF page 158](../images/page-0158-image-01.png)

```text
printf() and float datatypes.
```

如果您打算使用 printf()/scanf() 函数在串行控制台上打印/读取浮点数据类型（或者如果您打算使用 sprintf() 及类似例程），您需要显式启用 newlib-nano 中的浮点支持，newlib-nano 是嵌入式系统中更紧凑的 C 运行时库版本。为此，请前往 Project->Properties… 菜单，然后进入 C/C++ Build->Settings->MCU Settings，并根据您的功能需求勾选 Use float with printf from newlib-nano 和 Use float with scanf from newlib-nano，如图 5.8 所示。这将增加固件二进制文件的大小。

![Image from PDF page 158](../images/page-0158-image-02.png)

图 5.8：如何在 printf() 和 scanf() 中启用浮点支持

<!-- page: 159 -->

II 深入硬件抽象层

[原文提取异常，第159页]
