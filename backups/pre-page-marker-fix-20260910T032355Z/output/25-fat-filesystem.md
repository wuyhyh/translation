<!-- page: 750 -->

# 25. FAT 文件系统

电子嵌入式设备正变得越来越复杂，如今，需要读取和存储结构化数据的设备非常普遍。例如，考虑一个具有互联网连接的设备，它需要处理 HTTP 请求并传输 HTML 文件。除非 HTML 页面非常简单，否则该设备需要一种方法来处理多个独立的 HTML 文件，以及 CSS 样式表和 JavaScript 文件。因此，许多嵌入式开发人员需要在应用程序中处理结构化文件系统的方法。

ST 在其 CubeHAL 中集成了一个用于操作 FAT 文件系统（FAT12、FAT16 和 FAT32）的知名库：由 Chan¹ 开发的 FatFs 库。这是一个专为嵌入式系统设计的库，适用于 SRAM 和闪存资源有限的场景。它很受欢迎，并且已被证明是稳健的。

本章提供了对该中间件库的简要介绍。它描述了如何使用 CubeMX 生成集成该库的项目，以及如何基于这个有用的库开发应用程序。此外，我们将了解如何使用 SPI 接口 SD 卡，这是使用低成本嵌入式微控制器与存储卡配合的最普遍方式。

## 25.1 FatFs 库简介

文件分配表（File Allocation Table，FAT）是由微软在 20 世纪 80 年代初设计的文件系统架构，并一直作为 MS-DOS 和 Windows 操作系统的官方文件系统，直到 Windows NT 3.1 发布。FAT 文件系统随后被更先进的 NTFS 所取代，NTFS 提供了对元数据的改进支持，并使用高级数据结构来提高性能、可靠性和磁盘空间利用率，此外还增加了扩展功能，如安全访问控制列表（即文件权限）和文件系统日志记录。

凭借其简单性和稳健性，FAT 文件系统仍然常见于基于 USB 的存储器、闪存以及其他固态存储卡和模块（如 SD 卡）中，以及许多便携式和嵌入式设备中。从技术上讲，“FAT 文件系统”一词指的是该文件系统的三个主要变体：FAT12、FAT16 和 FAT32。这些数字基本上表示用于寻址文件系统簇（磁盘存储的连续区域）的位数。文件系统能处理的簇越多，可使用的字节数就越多。这就是为什么 FAT32 如今是大型固态和可移动存储器上最常用的文件系统的原因。使用 FAT 文件系统初始化的磁盘以及固态存储器可以拥有任意数量的分区。

FatFs 是一个空间优化²的库，提供以下功能：

¹https://bit.ly/2d6QUC5 ²为了完整性，我们必须指出，同一作者还制作了一个更小的 FatFs 库版本，名为 Petit FatFs(https://bit.ly/2drLLAa)，最适合 8 位微控制器。它基本上实现了主 FatFs 库的一个子集。

<!-- page: 751 -->

- 支持 FAT12、FAT16、FAT32(r0.0) 和 exFAT(r1.0) 文件系统。
- 允许打开无限数量的文件（唯一的限制是可用的 SRAM 内存）。
- 支持最多 10 个卷，每个卷的大小在 512 字节/扇区的情况下最大可达 2 TiB。
- 在 FAT 卷上，每个文件最大可增长至 4 GiB；在 exFAT 卷上则几乎无限制。
- 在 FAT 卷上，簇最大可达 128 个扇区；在 exFAT 卷上最大可达 16 MiB。
- 支持 4 种不同的扇区大小：512、1024、2048 和 4096 字节。

FatFs 库提供多达 37 个 API，并且可以通过多个配置宏选择性地禁用它们。事实上，为了减少闪存内存占用，可以禁用不需要的功能。FatFs 库使用纯 ANSI C 编写，并且完全与底层硬件抽象。官方库不提供对特定存储技术设备的支持，用户需要自行实现必要的胶水代码以接口硬件。

![Image from PDF page 751](../images/page-0751-image-01.png)

图 1：FatFs 库如何接口底层硬件

ST 工程师已将 FatFs 库集成到 CubeHAL 中。他们开发了必要的适配器，以便使用 FatFs 库与以下设备配合：

- 使用 SDIO 外设的 SD 存储卡：安全数字输入输出（Secure Digital Input Output，SDIO）是 SD 规范的扩展，涵盖了与 SD 和 MMC 卡相关的 I/O 功能。更先进的 STM32 微控制器，如某些 STM32F4 系列（例如 STM32F401RE）和 STM32F7 微控制器，提供了这种专用外设。SDIO

<!-- page: 752 -->

- 接口可以配置为工作在 1 位模式（即，数据仅通过一个名为 DO 的输出数据端口传输，另外两个额外的 I/O 用于时钟和命令传输），或者工作在 4 位模式（即，数据使用 4 个专用 I/O 传输，外加时钟和命令线）。这是使用 SD 卡的最快方式，在高性能 STM32 微控制器中可以达到 50MHz 的最大传输速率。
- 静态和动态 RAM 存储器：为 SDRAM 和 SRAM 存储器提供了两个独立的低级驱动程序，允许在 RAM 中创建文件系统。这两个驱动程序与 FMC 和 FSMC 控制器配合工作。它们允许初始化 RAM 磁盘，当应用程序对性能要求极高时，此功能特别有用（SRAM 比 NVM 存储器快得多）。
- 基于 USB 的磁盘：基于 ST USB 库构建的特定驱动程序允许创建支持大容量存储类（Mass Storage Class，MSC）的 USB 主机设备（即可以接口 USB 磁盘的设备）。

图 1 展示了 FatFs 库与 CubeHAL 之间的关系。不幸的是，ST 工程师尚未开发用于 SPI 模式下工作的 SD 卡驱动程序。事实上，SD 卡被设计为支持多种协议，其中包括通过 SPI 总线交换的命令。然而，我整理了一个完整的符合 SPI 标准的 SD 驱动程序，稍后我会向大家介绍。

要将 FatFs 库与存储设备集成，我们基本上需要实现以下六个例程：

- disk_initialize()：此例程包含初始化硬件设备所需的所有代码。例如，对于工作在 SPI 模式的 SD 卡，此例程必须包含初始化 SPI 接口并将 SD 卡置于 SPI 模式所需的所有代码（存在一个特定的遵循程序，如 Chan 的网站³上所记录的那样）。
- disk_status()：此函数用于库获取设备状态信息（例如，是否已初始化等）。
- disk_read()：此例程用于从存储设备中检索指定数量的扇区，从指定扇区开始。
- disk_write()：顾名思义，此函数用于在设备上存储指定数量的扇区。
- disk_ioctl()：此函数读取和配置某些特定的设备参数，如扇区大小、设备电源状态等。
- get_fattime()：返回当前时间，以便文件可以拥有有效的时间戳。如果微控制器不提供 RTC 单元，则此函数可以返回 0。

此外，最后三个例程仅在 FatFs 库以选项 _FS_READONLY == 0 编译时才需要。也就是说，如果我们使用 FatFs 只读模式，就可以避免为这些函数提供有效的实现。

³http://bit.ly/2dtWpWS

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

### 25.1.2 相关的 FatFs 结构和函数

我们现在将分析 FatFs 库提供的用于操作 FAT 驱动器⁷的最重要的结构和函数。

#### 25.1.2.1 挂载文件系统

在访问文件系统上的任何文件或目录之前，我们需要使用以下函数将其挂载⁸：

⁵然而，此功能的实现对于 SD 制造商来说并非强制要求。市场上存在若干 SD 卡未实现 SPI 规范，或者至少未严格实现该规范。⁶https://bit.ly/2dtWpWS ⁷完整的 FatFS API 文档可在 Chan 的网站⁸上找到。磁盘的挂载是由文件系统驱动程序执行的操作，其本质是收集与物理驱动器或其一部分相关的所有逻辑信息（分区数量、分区尺寸、簇尺寸、簇数量等）。在挂载之前，无法使用任何文件系统原语（目录、文件等）。

<!-- page: 756 -->

```text
FRESULT f_mount(FATFS *fs, const TCHAR *path, BYTE opt);
```

fs 是 C 结构体 FATFS 的一个实例，其中保存了关于逻辑驱动器（分区）的信息；path 是指向以空字符结尾的字符串的指针，用于指定逻辑驱动器（稍后会有更多说明）；opt 可以取值为 0，表示延迟文件系统挂载，直到首次访问卷（例如，打开文件或目录）时才执行；或者取值为 1，表示立即挂载逻辑卷。应用程序程序不得修改 FATFS 结构的任何成员，否则原始逻辑/物理磁盘可能会遭受不可修复的损坏。

path 参数的格式类似于 Windows 操作系统中的驱动器名称规范，它可以采用 N:/ 的形式，其中 N 是从 0 开始的一个数字，用于唯一标识一个逻辑驱动器。默认情况下，每个物理驱动器只能有一个逻辑驱动器（即一个分区）。这意味着，如果我们的磁盘有多个分区，则只有分区表中的第一个分区会被挂载并分配给一个逻辑驱动器。相反，通过在 ffconf.h 文件中设置宏 _MULTI_PARTITION=1，FatFs 库将为物理磁盘中的每个分区关联一个逻辑驱动器。当省略驱动器号时，驱动器号被假定为默认驱动器（驱动器 0 或当前驱动器）。因此，我们可以向 path 参数传递斜杠或反斜杠字符（\ 或 /），甚至指定一个 NULL 字符串。例如，以下代码强制挂载物理驱动器上的第一个分区：

```text
FATFS fs;
f_mount(&fs, "/", 1);
```

如果逻辑磁盘正确挂载，则 f_mount() 函数返回 FR_OK 值。否则，可能会返回一系列错误条件（FR_INVALID_DRIVE, FR_DISK_ERR, FR_NOT_READY, FR_NO_FILESYSTEM）。

#### 25.1.2.2 打开文件

一旦驱动器被挂载，我们就可以使用以下函数打开文件：

```text
FRESULT f_open(FIL* fp, const TCHAR* path, BYTE mode);
```

fp 是 C 结构体 FIL 的一个实例，其中保存了关于已打开文件的信息（其名称、大小、起始簇等）；path 对应于到达该文件的文件系统路径（稍后会有更多说明）；mode 指定文件的访问类型和打开方式，它可以取表 1 中的值。

<!-- page: 757 -->

表 1：文件打开方式列表

值 描述

FA_READ 指定对对象的读访问。可以从文件中读取数据。 FA_WRITE 指定对对象的写访问。可以向文件中写入数据。它可以与 FA_READ 进行逻辑或运算（logically or-ed）以实现读写访问。 FA_OPEN_EXISTING 打开文件。如果文件不存在，函数将失败。（默认） FA_CREATE_NEW 创建一个新文件。如果文件已存在，函数 f_open() 将因 FR_EXIST 而失败。 FA_CREATE_ALWAYS 创建一个新文件。如果文件已存在，它将被截断并覆盖。 FA_OPEN_ALWAYS 如果文件存在，则打开该文件。如果不存在，将创建一个新文件。 FA_OPEN_APPEND 与 FA_OPEN_ALWAYS 相同，但读/写指针被设置为文件末尾。

关于文件路径，这对应于到文件的完整文件系统路径，包括其名称。例如，0:\dir1\filename.txt 打开第一个逻辑磁盘上名为 dir1 的目录中名为 filename.txt 的文件。如果我们的应用程序仅使用一个逻辑驱动器，则我们可以简单地以另一种形式指定路径：\dir1\filename.txt。请注意，FatFs 能够处理 Windows 和 UNIX 两种形式的路径。因此，遵循前面的示例，我们也可以以这种等效形式指定路径：0:/dir1/filename.txt。

如果文件正确打开，则 f_open() 函数返回 FR_OK 值。否则，可能会返回一系列错误条件（有关更多详细信息，请参阅文档⁹）。

#### 25.1.2.3 从文件读取/向文件写入

一旦文件被打开，我们就可以根据文件打开模式从中读取数据或向其写入新数据。为此，FatFs 库提供了以下函数：

```text
FRESULT f_read(FIL* fp, void* buff, UINT btr, UINT* br);
FRESULT f_write(FIL* fp, const void* buff, UINT btr, UINT* br);
```

fp 对应于传递给 f_open() 函数的文件句柄；buff 是指向包含要从文件中读取的数据或要存储到文件中的数据的缓冲区的指针；btr 指定要读取/写入的字节数；br 对应于实际读取/写入的字节数。

以下示例展示了前面看到的函数的应用。它不过是一个文件复制过程。

⁹https://bit.ly/3HqA8XO

<!-- page: 758 -->

```text
1
#define BUF_LEN 2048
```

2

```text
3
FRESULT copy_file (char *srcPath, char *dstPath) {
4
FATFS fs;
/* File system object corresponding to logical drive */
5
FIL fsrc, fdst;
/* File objects */
6
BYTE buffer[BUF_LEN]; /* File copy buffer */
7
FRESULT fr;
/* FatFs function common result code */
8
UINT br, bw;
/* File read/write count */
```

9

```text
10
/* Mount the filesystem */
11
f_mount(&fs[0], "0:", 0);
```

12

```text
13
/* Open source file */
14
fr = f_open(&fsrc, srcPath, FA_READ);
15
if (fr) return (int)fr;
```

16

```text
17
/* Create destination file */
18
fr = f_open(&fdst, dstPath, FA_WRITE | FA_CREATE_ALWAYS);
19
if (fr) return (int)fr;
```

20

```text
21
/* Copy source to destination */
22
while(1) {
23
/* Read 'BUF_LEN' bytes from source file */
24
fr = f_read(&fsrc, buffer, BUF_LEN, &br);
25
if (fr != FR_OK || br == 0) break; /* Error condition or EOF */
26
/* Write read data to the destination file */
27
fr = f_write(&fdst, buffer, br, &bw);
28
if (fr != FR_OK || bw < br) break; /* Error or disk full */
29
}
```

30

```text
31
/* Close open files */
32
f_close(&fsrc);
33
f_close(&fdst);
```

34

```text
35
/* Unmount volume */
36
f_mount(NULL, "0:", 0);
```

37

```text
38
return fr;
39
}
```

#### 25.1.2.4 创建和打开目录

## FatFs 库允许轻松操作文件和目录。要创建新目录，我们可以使用以下函数：

<!-- page: 759 -->

```text
FRESULT f_mkdir(const TCHAR* path);
```

该函数接受要创建的目录的完整路径。例如，如果我们的文件系统根目录下已经存储了一个名为 dir1 的目录，那么我们可以传递字符串 "0:/dir1/subdir1" 来在其中创建一个子目录。

要打开一个已存在的目录，我们可以使用以下函数：

```text
FRESULT f_opendir(DIR* dp, const TCHAR* path);
```

dp 是 C 结构体 DIR 的一个实例，它表示已打开目录的句柄；path 是我们想要打开的目录的完整路径。如果 f_opendir() 函数返回了一个有效的句柄，那么我们可以通过使用以下函数来读取其内容：

```text
FRESULT f_readdir(DIR* dp, FILINFO* fno);
```

dp 是使用 f_opendir() 函数打开的目录对应的实例；fno 是 FILINFO 结构体的一个实例，它保存有关目录中当前项的信息。f_readdir() 函数的工作方式如下。一旦目录被打开，我们就调用 f_readdir()，直到它返回一个不同于 FR_OK 的值（在发生错误的情况下）或者 fno.fname 条目为空。最后一种条件表示我们到达了目录的末尾，没有更多元素（文件或目录）可获取。

FILINFO 结构体定义如下：

```text
typedef struct {
DWORD
fsize;
/* File size */
WORD
fdate;
/* Last modified date */
WORD
ftime;
/* Last modified time */
BYTE
fattrib;
/* Attribute */
TCHAR
fname[13]; /* Short file name (8.3 format) */
#if _USE_LFN
TCHAR* lfname;
/* Pointer to the LFN buffer */
UINT
lfsize;
/* Size of LFN buffer in TCHAR */
#endif
} FILINFO;
```

让我们分析这个结构体的字段。

- fsize：它存储文件的字节大小。如果对象是目录，则此字段无意义。
- fdate：指示文件被修改或目录被创建的日期，它具有以下结构

– bit [15:9]：自 1980 年起的年份（0..127） – bit [8:5]：月份（1..12）

<!-- page: 760 -->

- – bit [4:0]：日期（1..31）
- ftime：指示文件被修改或目录被创建的时间，它具有以下结构

- – bit [15:11]：小时（0..23） – bit [10:5]：分钟（0..59） – bit [4:0]：秒 / 2（0..29）
- fattrib：对应于文件/目录属性，它是表 2 中列出的属性的组合。
- fname：这个以空字符结尾的字符串对应于 FAT 8:3 格式的文件/目录名称。当没有更多项可读取时，会存储一个 NULL 字符串，这表明该结构体无效。
- lfname：这个以空字符结尾的字符串对应于启用长文件名支持（_USE_LFN 宏 != 0）时的文件/目录名称。稍后会有更多介绍。

表 2：文件/目录属性列表

文件/目录属性 描述

```text
AM_RDO
Read only
AM_ARC
Archive
AM_SYS
System
AM_HID
Hidden
```

以下示例展示了一个例程，该例程执行文件系统的深度优先遍历，并使用 trace_printf() 例程打印文件和文件夹的名称。该例程使用 f_opendir() 和 f_readdir() 函数来获取每个目录的内容。_USE_LFN 宏允许正确处理长文件名支持。其用法将在下一段中解释。

```text
1
FRESULT scan_files (TCHAR* path) {
2
FRESULT res;
3
DIR dir;
4
UINT i;
5
static FILINFO fno;
6
static TCHAR lfname[_MAX_LFN];
7
TCHAR *fname;
```

8

```text
9
res = f_opendir(&dir, path); /* Open the directory */
10
if (res == FR_OK) {
11
while(1) {
12
#if _USE_LFN > 0
13
fno.lfname = lfname;
14
fno.lfsize = _MAX_LFN - 1;
15
#endif
16
/* Read a directory item */
17
res = f_readdir(&dir, &fno);
```

<!-- page: 761 -->

```text
18
/* Break on error or end of directory */
19
if (res != FR_OK || fno.fname[0] == 0) break;
20
#if _USE_LFN > 0
21
fname = *fno.lfname ? fno.lfname : fno.fname;
22
#endif
23
if (fno.fattrib & AM_DIR) { /* It is a directory */
24
i = strlen(path);
25
sprintf(&path[i], "/%s", fname);
26
/* Scan directory recursively */
27
res = scan_files(path);
28
if (res != FR_OK) break;
29
path[i] = 0;
30
} else { /* It is a file. */
31
trace_printf("%s/%s\n", path, fname);
32
}
33
}
34
f_closedir(&dir);
35
}
36
return res;
37
}
```

### 25.1.3 如何配置 FatFs 库

FatFs 库具有高度的可定制性。一组配置参数（即配置宏）允许在编译时减少库的总占用空间，并启用/禁用某些功能。

所有配置参数都会由 CubeMX 自动导出到 FATFS/Target/ffconf.h 文件中。我们现在将分析其中最重要的几个。若要更全面地了解此主题，读者应参考官方文档¹⁰。

- _FS_TINY：该宏可以取值为 0（默认）和 1。此选项允许减少 FatFs 库对 SRAM 的占用。当设置为 0 时，每个 FIL 结构体实例都有一个在文件读写期间使用的临时缓冲区。相反，当设置为 1 时，使用在 FATFS 结构体中定义的全局池。这会减慢读写操作的速度。
- _FS_READONLY：该宏可以取值为 0（默认）和 1。此宏通过移除写入 API 函数（如 f_write()、f_sync()、f_unlink()、f_mkdir()、f_chmod()、f_rename()、f_truncate()、f_getfree()）以及可选的写入功能，从而在编译时跳过用于修改文件系统的功能。
- _FS_MINIMIZE：该宏定义库的最小化级别，即移除某些 API 函数。如果设置为 0，则所有 API 均可用。如果设置为 1，则移除 f_stat()、f_getfree()、f_unlink()、f_mkdir()、f_chmod()、f_utime()、f_truncate() 和 f_rename() 函数。如果设置为 2，则除了 _FS_MINIMIZE 设置为 1 时移除的那些函数外，还移除 f_opendir()、f_readdir() 和 f_closedir() 例程

¹⁰https://bit.ly/2dJGh3E

<!-- page: 762 -->

- 如果设置为 3，则还会移除 f_lseek() 函数。
- _CODE_PAGE：此选项指定目标系统使用的 OEM 代码页。代码页设置不正确可能导致文件打开失败。对于西方国家，CP1252（又称 Latin1）是 Windows 操作系统中最广泛使用的代码页。
- _USE_LFN：此选项切换对长文件名（LFN）的支持。启用 LFN 模式时，需要将包含在 option/unicode.c 文件中的 Unicode 支持函数添加到项目中。此外，启用 LFN 支持时，我们需要提供一个预分配的缓冲区来存储长文件名。FatFs 库对此要求没有很好的文档说明，缺乏经验的人往往花费大量时间试图弄清楚如何检索 LFN 名称。前面看到的 scan_files() 例程清楚地展示了如何执行此操作。缓冲区 lfname 在第 6 行静态分配在堆栈上。然后，fno.lfname 指针在第 13 行被设置为指向 lfname 缓冲区。同样，缓冲区的大小在第 14 行指定。这使得 FatFs 库能够正确检索文件或目录的 LFN 名称。否则，fno.fname 缓冲区包含 8.3 格式的文件名。
- _MAX_LFN：该宏指定要处理的最大 LFN 长度（从 12 到 255）。
- _LFN_UNICODE：此选项切换 API 上的字符编码。（0:ANSI/OEM 或 1:Unicode）。要在路径名称中使用 Unicode 字符串，必须启用 LFN 功能并将 _LFN_UNICODE 设置为 1。此选项还影响字符串 I/O 函数的行为。请注意，为了允许在 FatFs 库中透明地使用 Unicode 字符串，库本身定义了 TCHAR 数据类型，如果禁用 Unicode 支持，它会自动转换为 char，如果启用，则转换为 uint16_t。有关此主题的更多信息，请参阅 FatFs 文档¹¹。
- _VOLUMES：该宏设置每个物理磁盘的最大逻辑驱动器数量。默认情况下，该宏设置为 1。有关此主题的更多信息，请参阅 FatFs 文档¹²。
- _FS_REENTRANT：此选项切换 FatFs 库本身的重入性（线程安全）。对不同卷的文件/目录访问始终是重入的，并且无论此选项如何设置，都可以同时工作。卷控制函数（f_mount()、f_mkfs() 和 f_fdisk()）始终不是重入的。对同一卷的文件/目录访问不是重入的，除非将 _FS_REENTRANT 宏设置为 1。要启用此功能，用户还需要提供同步处理例程，即 ff_req_grant()、ff_rel_grant()、ff_del_syncobj() 和 ff_cre_syncobj()。ST 工程师已实现这些例程，使其使用 FreeRTOS 信号量。有关此功能的更多信息，请查看 option/syscall.c 文件。
- _SYNC_t：当 _FS_REENTRANT 宏设置为 1 时，还必须指定此宏，该宏指定同步结构的“类型”。当使用 FreeRTOS 与 FatFs 库配合时，该宏设置为 osSemaphoreId 类型。

¹¹https://bit.ly/2dJP9q1 ¹²http://bit.ly/2dJPoBx
