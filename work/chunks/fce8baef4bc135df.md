<!-- page: 84 -->

## 1.4 The Nucleo Development Board

Every practical text about an electronic device requires a development board (also known as kit) to start working with it. In the STM32 world the most widespread development board is the STM32 Discovery. ST has developed more than 48 different discovery boards useful to test STM32 MCUs and their capabilities.

![Image from PDF page 84](../images/page-0084-image-02.jpeg)

Figure 1.17: The STM32L0538 Discovery kit introduced by ST in 2015

For example, the STM32L0538DISCOVERY board (Figure 1.17) allows to test both the STM32L053 MCU and an e-paper display. You can find a lot of tutorials around the Internet covering boards from the Discovery line.

²⁰http://apple.co/Uf20WR ²¹http://bit.ly/1Pvo8EV

<!-- page: 85 -->

ST introduced in 2015 a completely new range of development boards: the Nucleo. The Nucleo lineup is divided in three main groups: Nucleo-32, Nucleo-64 and Nucleo-144 (see Figure 1.18). The name of each group comes from the MCU package type used: Nucleo-32 uses an STM32 in an LQFP- 32 package; Nucleo-64 uses an LQFP-64; Nucleo-144 an LQFP-144. The Nucleo-64 was the first line introduced to the market and there are currently 32 different boards, each one with a given STM32 microcontroller. The Nucleo-144 has been introduced in January 2016, and it is the first low-cost kit equipping the powerful STM32F746. It also provides an Ethernet phyther²² and a LAN port. Since the Nucleo-64 is the most complete range, this book will cover only the most relevant boards from the Nucleo-64 line-up (see Table 1.21 for the complete list). In the remaining parts of this book, we refer to the Nucleo-64 simply with the term “Nucleo”.

The Nucleo is composed of two parts, as shown in Figure 1.19. The part with the mini-USB connector is an ST-LINK 2.1 integrated debugger, which is used to upload the firmware on the target MCU and to do step-by-step debugging. The ST-LINK interface also provides a Virtual COM Port (VCP), which can be used to exchange data and messages with the host PC. One key feature of Nucleo boards is that the ST-LINK interface can be easily separated from the rest of the board (two red scissors in Figure 1.19 show where to break). This way it can be used as stand-alone ST-LINK programmer (a stand-alone ST-LINK programmer cost about $25). However, the ST-LINK provides an optional SWD interface that can be used to program another board without detaching the ST-LINK interface from the Nucleo (as it already happens with the Discovery boards) by removing the two jumpers labeled ST-LINK. The rest of the board contains the target MCU (the microcontroller we will use to develop our applications), a RESET button (the black one), a user programmable tactile button (the blue one) and an LED. The board also contains one pad to mount an external high-speed crystal (HSE). All recent Nucleo boards already provide a low-speed crystal. Finally, the board has several pin headers we will look at in a while.

![Image from PDF page 85](../images/page-0085-image-01.jpeg)

Figure 1.18: A Nucleo development board

ST introduced this new kit to attract people from the Arduino world. In fact, Nucleo boards provide pin headers to accept Arduino shields, expansion boards specifically built to expand the Arduino

²²The Ethernet phyther (also called Ethernet PHY) is a device which translates messages exchanged over a LAN network in electrical signals.

<!-- page: 86 -->

UNO and all other Arduino boards. Figure 1.20²³ shows the STM32 peripherals and GPIOs associated with the Arduino compatible connector.

![Image from PDF page 86](../images/page-0086-image-01.jpeg)

Figure 1.19: The relevant parts of a Nucleo board

To be honest, the Nucleo boards have other interesting advantages compared to the Discovery ones. First of all, ST sells them at a really aggressive price (probably for the aforementioned reasons). A Nucleo costs between $10 and $15, depending on where you buy it, and if you think about what you can do with this architecture, you have to agree that it is really underpriced compared to an Arduino DUE board (which is also equipped with a 32-bit ARM processor from Microchip). Another interesting feature is that Nucleo boards are designed to be pin-to-pin compatible with each other. This means that you can develop the firmware for the STM32Nucleo-F103RB board (equipped with the popular STM32F103 MCU) and later adapt it to a more powerful Nucleo (e.g. STM32Nucleo- F401RE) if you need more computing power.

²³Figure 1.20 and 22 are taken from the mbed.org website and they refer to the Nucleo-F401RE board. Please, refer to Appendix C for the right pin-out of your Nucleo board.

<!-- page: 87 -->

![Image from PDF page 87](../images/page-0087-image-01.jpeg)

Figure 1.20: Peripherals and GPIOs associated to Arduino headers

In addition to Arduino compatible pin headers, the Nucleo provides its own expansion connectors. They are two 2x19, 2.54mm spaced male pin headers. They are called Morpho connectors and are a convenient way to access most of the MCU pins. Figure 1.21 shows the STM32 peripherals and GPIOs associated with the Morpho connector.

![Image from PDF page 87](../images/page-0087-image-02.jpeg)

Figure 1.21: Peripherals and GPIOs associated to Morpho headers

ST is releasing several expansion shields for the Nucleo that are compatible with the Arduino UNO or the ST Morpho header. For example, Figure 1.22 shows a Nucleo-F302R8 board with a X-NUCLEO- IHM07M1 expansion board, a shield which features the ST L6230 DMOS driver, a motor control

<!-- page: 88 -->
