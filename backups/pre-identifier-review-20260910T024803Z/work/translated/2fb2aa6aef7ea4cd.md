<!-- page: 753 -->

### 25.1.1 在项目中添加 FatFs 库

如前所述，FatFs 库是 CubeHAL 框架的一个组件，并且 CubeMX 支持它。然而，CubeMX 处理该库的方式对于初学者来说可能有点反直觉。

![Image from PDF page 753](../images/page-0753-image-01.jpeg)

图 2：CubeMX 为那些未提供兼容适配器的 STM32 微控制器显示的内容

你们中的许多人会注意到，如图 2 所示，CubeMX 仅显示一个与 FatFs 中间件库相关的选项。对于大多数 STM32 微控制器，会出现一个晦涩的“User-defined”（用户定义）条目。但这具体意味着什么？它仅仅意味着你特定的 STM32 微控制器没有提供与 ST 开发人员开发的适配器（SRAM/SDRAM、USB 和 SDIO）兼容的外设，因此你需要为底层 I/O 驱动程序提供自己的实现。

![Image from PDF page 753](../images/page-0753-image-02.jpeg)

图 3：CubeMX 为 STM32F746VG 微控制器显示的内容

相反，图 3 显示了如果你使用提供 SDIO 接口⁴、FMC 控制器和 USB 设备接口的 STM32F779BI 微控制器时可用的选项。然而，正如你在图 3 中看到的，生成选项呈灰色显示。这是因为我们需要先启用相应的外设，然后勾选所需的 FatFs 配置。例如，假设我们正在处理一个提供 SDIO 外设的 STM32F401RE 微控制器。我们首先需要在 IP Tree 视图中启用所需的 SDIO 模式（1 位、4 位等），然后勾选相应的 FatFs 选项。

生成的项目结构类似于图 4 所示。Middlewares/Third_- Party/FatFs/src 文件夹包含 FatFs 库，而 FATFS/Target/sd_diskio.c 文件包含通过特定接口（SDIO）处理 SD 卡的 I/O 例程。这些例程从特定的板级配置中抽象出来，并依赖于在 src/bsp_driver_sd.c 文件中实现的 API。该文件中包含的例程反过来使用 CubeHAL 函数（对于 SDIO 使用 HAL_SD 模块）。

⁴在 STM32F7 微控制器中，SDIO 外设被称为 SDMMC。

<!-- page: 754 -->

![Image from PDF page 754](../images/page-0754-image-01.jpeg)

图 4：带有 FatFs 中间件的生成项目结构

相反，如果你选择“User-defined”选项生成项目，那么你会找到文件 FATFS/Target/user_diskio.c，其中包含函数 USER_initialize()、USER_status()、USER_read()、USER_write() 和 USER_ioctl()。这些例程是空的模板，需要用驱动你特定存储设备的代码来填充。

#### 25.1.1.1 通用磁盘接口 API

ST 工程师在 FatFs 库和底层设备驱动程序之间开发了另一个抽象层。这被称为通用磁盘接口层（Generic Disk Interface layer），它本质上是一个抽象层，允许在同一应用程序中处理多个磁盘驱动程序。它类似于 Linux 操作系统中的虚拟文件系统（Virtual Filesystem）。

该层中的每个设备驱动程序对应于以下 C 结构体的一个实例：

```text
typedef struct {
DSTATUS (*disk_initialize) (BYTE);
DSTATUS (*disk_status)
(BYTE);
DRESULT (*disk_read)
(BYTE, BYTE*, DWORD, UINT);
#if _USE_WRITE == 1
DRESULT (*disk_write)
(BYTE, const BYTE*, DWORD, UINT);
#endif /* _USE_WRITE == 1 */
#if _USE_IOCTL == 1
DRESULT (*disk_ioctl)
(BYTE, BYTE, void*);
#endif /* _USE_IOCTL == 1 */
} Diskio_drvTypeDef;
```

<!-- page: 755 -->

这不过是一个包含五个函数指针的 C 结构体，这些函数指针对应于 FatFs 处理对特定存储设备访问所需的例程实现。函数：

```text
uint8_t FATFS_LinkDriver(Diskio_drvTypeDef *drv, char *path);
```

负责将该结构体的一个实例链接到给定的挂载路径（例如，路径 “0:/” 用于寻址卷 0）。

得益于 ST 团队的这一小项改进，我们可以使用不同的设备来使用不同的文件系统（例如，将 USB 磁盘文件系统与存储在 SD 卡上的另一个文件系统结合使用）。

#### 25.1.1.2 实现以 SPI 模式访问 SD 卡的驱动程序

SD 存储卡不仅仅是简单的闪存。它们还包含一个专用处理器，该处理器实现了通过 SD 接口交换数据的所有逻辑（响应多种通信协议）以及处理对特定闪存（NOR、NAND 等）的正确访问。此外，所有 SD 卡都实现了磨损均衡技术，以延长可擦写闪存的使用寿命。

SD 卡的一个显著特性是能够响应通过 SPI 总线⁵交换的命令和消息。这使得它们可以与低成本微控制器（即使是 8 位微控制器也适合此操作）一起使用，这也解释了它们在嵌入式应用中的流行。我在此不会描述 SD 卡支持的 SPI 协议。Chan 提供了⁶足够的信息来开始处理此事。在此重复它是无用且适得其反的。Chan 还提供了几个示例项目，展示了如何通过 SPI 接口连接 SD 卡。

下一章将展示如何在基于 Web 的嵌入式应用程序中使用 SPI 模式的 SD 卡来提供存储在 SD 卡上的网页。
