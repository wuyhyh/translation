<!-- page: 1 -->

[原文提取异常，第1页]

<!-- page: 2 -->

# Mastering STM32 - Second Edition

## A step-by-step guide to the most complete ARM Cortex-M platform, using the official STM32Cube development environment

## Carmine Noviello

This book is for sale at http://leanpub.com/mastering-stm32-2nd

This version was published on 2022-02-28

![Image from PDF page 2](../images/page-0002-image-01.png)

This is a Leanpub book. Leanpub empowers authors and publishers with the Lean Publishing process. Lean Publishing is the act of publishing an in-progress ebook using lightweight tools and many iterations to get reader feedback, pivot until you have the right book and build traction once you do.

© 2015-2022 Carmine Noviello

<!-- page: 3 -->

# Tweet This Book!

Please help Carmine Noviello by spreading the word about this book on Twitter!

The suggested hashtag for this book is #MasteringSTM32.

Find out what other people are saying about the book by clicking on this link to search for this hashtag on Twitter:

#MasteringSTM32

<!-- page: 4 -->

To my wife Anna, who has always blindly supported me in all my projects

To my daughter Giulia, who completely upset my projects

<!-- page: 5 -->

# Contents

Preface . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . i Who Is This Book For? . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ii How to Integrate This Book? . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . iii How Is the Book Organized? . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . iv Differences With the First Edition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . vii About the Author . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . viii Errata and Suggestions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ix Book Support . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ix How to Help the Author . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ix Copyright Disclaimer . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ix Credits . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . x

Acknowledgments to the First Edition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . xi

# I Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1

1. Introduction to STM32 MCU Portfolio . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2 1.1 Introduction to ARM Based Processors . . . . . . . . . . . . . . . . . . . . . . . . . . . 2 1.1.1 Cortex and Cortex-M Based Processors . . . . . . . . . . . . . . . . . . . . 4 1.1.1.1 Core Registers . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4 1.1.1.2 Memory Map . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7 1.1.1.3 Bit-Banding . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8 1.1.1.4 Thumb-2 and Memory Alignment . . . . . . . . . . . . . . . . 11 1.1.1.5 Pipeline . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13 1.1.1.6 Interrupts and Exceptions Handling . . . . . . . . . . . . . . . 14 1.1.1.7 SysTimer . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16 1.1.1.8 Power Modes . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17 1.1.1.9 TrustZoneTM . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18 1.1.1.10 CMSIS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19 1.1.1.11 Effective Implementation of Cortex-M Features in the STM32 Portfolio . . . . . . . . . . . . . . . . . . . . . . . . . . . 20 1.2 Introduction to STM32 Microcontrollers . . . . . . . . . . . . . . . . . . . . . . . . . . 21 1.2.1 Advantages of the STM32 Portfolio…. . . . . . . . . . . . . . . . . . . . . . 22

<!-- page: 6 -->

CONTENTS

### 1.2.2 ….And Its Drawbacks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23 1.3 A Quick Look at the STM32 Subfamilies . . . . . . . . . . . . . . . . . . . . . . . . . . 24 1.3.1 F0 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 26 1.3.2 F1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 27 1.3.3 F2 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28 1.3.4 F3 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29 1.3.5 F4 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 31 1.3.6 F7 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 33 1.3.7 H7 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 35 1.3.8 L0 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 37 1.3.9 L1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 38 1.3.10 L4 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 39 1.3.11 L4+ . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 41 1.3.12 L5 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 42 1.3.13 U5 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 43 1.3.14 G0 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 45 1.3.15 G4 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 46 1.3.16 STM32WB . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 48 1.3.17 STM32WL . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 50 1.3.18 How to Select the Right MCU for You? . . . . . . . . . . . . . . . . . . . . 51 1.4 The Nucleo Development Board . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 54

2. Get In Touch With SM32CubeIDE . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 60 2.1 Why Choose STM32CubeIDE as Tool-Chain for STM32 . . . . . . . . . . . . . . . . 60 2.1.1 Two Words About Eclipse… . . . . . . . . . . . . . . . . . . . . . . . . . . . 62 2.1.2 … and GCC . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 62 2.2 Downloading and Installing the STM32CubeIDE . . . . . . . . . . . . . . . . . . . . . 63 2.2.1 Windows - Installing the Tool-Chain . . . . . . . . . . . . . . . . . . . . . 64 2.2.2 Linux - Installing the Tool-Chain . . . . . . . . . . . . . . . . . . . . . . . . 67 2.2.3 Mac - Installing the Tool-Chain . . . . . . . . . . . . . . . . . . . . . . . . . 68 2.3 STM32CubeIDE overview . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 70

3. Hello, Nucleo! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 76 3.1 Create a Project . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 76 3.2 Adding Something Useful to the Generated Code . . . . . . . . . . . . . . . . . . . . 79 3.3 Connecting the Nucleo to the PC . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 84 3.3.1 ST-LINK Firmware Upgrade . . . . . . . . . . . . . . . . . . . . . . . . . . . 85 3.4 Flashing the Nucleo using STM32CubeProgrammer . . . . . . . . . . . . . . . . . . . 86

4. STM32CubeMX Tool . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 89 4.1 Introduction to CubeMX Tool . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 89 4.1.1 Target Selection Wizard . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 90 4.1.1.1 MCU/MPU Selector . . . . . . . . . . . . . . . . . . . . . . . . 91 4.1.1.2 Board Selector . . . . . . . . . . . . . . . . . . . . . . . . . . . . 92

<!-- page: 7 -->

CONTENTS
