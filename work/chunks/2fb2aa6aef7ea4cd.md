<!-- page: 753 -->

### 25.1.1 Adding FatFs Library in Your Projects

As said before, FatFs library is a component of the CubeHAL framework, and CubeMX supports it. However, the way CubeMX handles this library is a little bit counterintuitive, at least for beginners.

![Image from PDF page 753](../images/page-0753-image-01.jpeg)

Figure 2: What CubeMX shows for those STM32 MCUs that does not provide a compatible adapter

Many of you will notice that CubeMX shows just one option related to the FatFs middleware library, as shown in Figure 2. The obscure User-defined entry will appear for the majority of STM32 microcontrollers. But what exactly that means? It simply means that your specific STM32 microcontroller provides no peripheral compatible with the adapters developed by ST developers (SRAM/SDRAM, USB, and SDIO), and you will need to provide your own implementation for the low-level I/O drivers.

![Image from PDF page 753](../images/page-0753-image-02.jpeg)

Figure 3: What CubeMX shows for an STM32F746VG MCU

Figure 3, instead, shows the options available if you use an STM32F779BI MCU, which provides the SDIO interface⁴, the FMC controller and a USB-device interface. However, as you can see in Figure 3, the generation options appear grayed out. This happens because we need to enable the corresponding peripheral first, and then check the wanted FatFs configuration. For example, let us assume that we are working on an STM32F401RE MCU, which provides a SDIO peripheral. We first need to enable the wanted SDIO mode (1-bit, 4-bit, etc) in the IP Tree view, and then check the corresponding FatFs option.

The generated project has a structure similar to the one shown in Figure 4. The Middlewares/Third_- Party/FatFs/src folder contains the FatFs library, while the FATFS/Target/sd_diskio.c file contains I/O routines to handle SD cards through the specific interface (the SDIO). Those routines are abstracted from the specific board configurations, and they rely on APIs that are implemented inside the src/bsp_driver_sd.c file. The routines contained in that file use in turn CubeHAL functions (from the HAL_SD module for the SDIO).

⁴In STM32F7 MCUs the SDIO peripheral is called SDMMC.

<!-- page: 754 -->

![Image from PDF page 754](../images/page-0754-image-01.jpeg)

Figure 4: The structure of a generated project with the FatFs middleware

If, instead, you generate a project choosing the User-defined option, then you will find the file FATFS/Target/user_diskio.c, which contains the functions USER_initialize(), USER_status(), USER_read(), USER_write() and USER_ioctl(). Those routines are empty templates, and they need to be filled with the code to drive your specific memory device.

#### 25.1.1.1 The Generic Disk Interface API

ST Engineers have developed another abstraction layer between the FatFs library and the low-level device drivers. This is called Generic Disk Interface layer and it is essentially an abstraction layer that allows to handle multiple disk-drivers in the same application. It resembles the Virtual Filesystem in the Linux Operating System.

Each device driver in this layer corresponds to an instance of the following C struct:

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

This is nothing more than a C struct containing five function pointers, which correspond to the implementation of those routines needed by the FatFs to handle the access to the specific memory device. The function:

```text
uint8_t FATFS_LinkDriver(Diskio_drvTypeDef *drv, char *path);
```

is responsible of linking an instance of that struct to a given mount path (e.g. the path “0:/” to address the volume 0).

Thank to this little improvement by ST guys, we can use different filesystems using different devices (for example a USB-disk filesystem in conjunction with another filesystem stored in the SD card).

#### 25.1.1.2 The Implementation of a Driver to Access SD Cards in SPI Mode

SD memory cards are more than simple flash memories. They also include a dedicated processor, which implements all the logic to exchange data through the SD interface (answering to several communication protocols) and to handle the proper access to the specific flash memory (NOR, NAND, etc.). Moreover, all SD cards implement wear-leveling techniques for lasting the service life of erasable flash memories.

One distinctive feature of SD cards is the ability to answer to commands and messages exchanged over an SPI bus⁵. This allows them to be used in conjunction with low-cost microcontrollers (even 8bits ones are suitable for this operation), and this explains their popularity in embedded applications. I will not describe here the SPI protocol supported by SD cards. Chan provides⁶ sufficient information to get started with this matter. To repeat it here is useless and counterproductive. Chan also provides several example projects that show how to interface SD card through the SPI interface.

The next chapter will show how to use SD cards in SPI mode to serve web pages stored on the SD cards in a web-based embedded application.
