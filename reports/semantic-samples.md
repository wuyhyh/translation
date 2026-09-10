# Semantic review samples

This is a deterministic sampling artifact for human review. It does not ask the translation model to judge its own correctness.
Seed: `20260909`. Samples: **118**. Repaired pages included: **58**.
Priority pages: `53, 56, 399, 454, 499, 644, 740`.

## PDF page 1 — Chapter 0: Front Matter

Focus: `numbers=; negation=; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>[原文提取异常，第1页]</pre></td>
<td><pre>[原文提取异常，第1页]</pre></td>
</tr></tbody></table>

## PDF page 2 — Chapter 0: Front Matter

Focus: `numbers=0002, 01, 02, 2, 2015, 2022, 28; negation=; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre># Mastering STM32 - Second Edition

## A step-by-step guide to the most complete ARM Cortex-M platform, using the official STM32Cube development environment

## Carmine Noviello

This book is for sale at http://leanpub.com/mastering-stm32-2nd

This version was published on 2022-02-28

![Image from PDF page 2](../images/page-0002-image-01.png)

This is a Leanpub book. Leanpub empowers authors and publishers with the Lean Publishing process. Lean Publishing is the act of publishing an in-progress ebook using lightweight tools and many iterations to get reader feedback, pivot until you have the right book and build traction once you do.

© 2015-2022 Carmine Noviello</pre></td>
<td><pre># 精通 STM32 - 第二版

## 使用官方 STM32Cube 开发环境，逐步掌握最完整的 ARM Cortex-M 平台

## Carmine Noviello

本书可在 http://leanpub.com/mastering-stm32-2nd 购买

本版本发布于 2022-02-28

![Image from PDF page 2](../images/page-0002-image-01.png)

这是一本 Leanpub 书籍。Leanpub 通过精益出版流程赋能作者和出版商。精益出版是指使用轻量级工具和多次迭代来发布正在编写中的电子书，以获取读者反馈，不断调整直至打造出合适的书籍，并在成功后建立影响力。

© 2015-2022 Carmine Noviello</pre></td>
</tr></tbody></table>

## PDF page 3 — Chapter 0: Front Matter

Focus: `numbers=; negation=; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre># Tweet This Book!

Please help Carmine Noviello by spreading the word about this book on Twitter!

The suggested hashtag for this book is #MasteringSTM32.

Find out what other people are saying about the book by clicking on this link to search for this hashtag on Twitter:

#MasteringSTM32</pre></td>
<td><pre># 在推特上分享这本书！

请在推特上帮忙向更多人推荐这本书，以支持卡米内·诺维耶洛（Carmine Noviello）！

本书建议使用的标签是 #MasteringSTM32。

点击此链接，在推特上搜索该标签，查看其他人对这本书的评价：

#MasteringSTM32</pre></td>
</tr></tbody></table>

## PDF page 4 — Chapter 0: Front Matter

Focus: `numbers=; negation=; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>To my wife Anna, who has always blindly supported me in all my projects

To my daughter Giulia, who completely upset my projects</pre></td>
<td><pre>献给我的妻子安娜，她始终无条件地支持我所有的事业

献给我的女儿朱莉娅，她总是彻底打乱我的计划</pre></td>
</tr></tbody></table>

## PDF page 5 — Chapter 0: Front Matter

Focus: `numbers=1, 1.1, 1.10, 1.11, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 11, 13, 14, 16, 17, 18, 19, 2, 20, 21, 22, 4, 7; negation=; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre># Contents

Preface . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . i Who Is This Book For? . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ii How to Integrate This Book? . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . iii How Is the Book Organized? . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . iv Differences With the First Edition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . vii About the Author . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . viii Errata and Suggestions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ix Book Support . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ix How to Help the Author . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ix Copyright Disclaimer . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ix Credits . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . x

Acknowledgments to the First Edition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . xi

# I Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1

1. Introduction to STM32 MCU Portfolio . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2 1.1 Introduction to ARM Based Processors . . . . . . . . . . . . . . . . . . . . . . . . . . . 2 1.1.1 Cortex and Cortex-M Based Processors . . . . . . . . . . . . . . . . . . . . 4 1.1.1.1 Core Registers . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4 1.1.1.2 Memory Map . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7 1.1.1.3 Bit-Banding . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8 1.1.1.4 Thumb-2 and Memory Alignment . . . . . . . . . . . . . . . . 11 1.1.1.5 Pipeline . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13 1.1.1.6 Interrupts and Exceptions Handling . . . . . . . . . . . . . . . 14 1.1.1.7 SysTimer . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16 1.1.1.8 Power Modes . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17 1.1.1.9 TrustZoneTM . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18 1.1.1.10 CMSIS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19 1.1.1.11 Effective Implementation of Cortex-M Features in the STM32 Portfolio . . . . . . . . . . . . . . . . . . . . . . . . . . . 20 1.2 Introduction to STM32 Microcontrollers . . . . . . . . . . . . . . . . . . . . . . . . . . 21 1.2.1 Advantages of the STM32 Portfolio…. . . . . . . . . . . . . . . . . . . . . . 22</pre></td>
<td><pre># 目录

前言 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . i 本书适合谁阅读？ . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ii 如何结合本书学习？ . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . iii 本书的结构安排 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . iv 与第一版的区别 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . vii 作者简介 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . viii 勘误与建议 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ix 图书支持 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ix 如何支持作者

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ix 版权声明 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ix 致谢 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . x

第一版致谢 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . xi

# 引言. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1

1。STM32 微控制器产品组合简介 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2

1.1 基于 ARM 的处理器简介 . . . . . . . . . . . . . . . . . . . . . . . . . . . 2

1.1.1 基于Cortex和Cortex-M的处理器 . . . . . . . . . . . . . . . . . . . . 4

1.1.1.1 内核寄存器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4

1.1.1.2 内存映射 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7

1.1.1.3 位带 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8

1.1.1.4 Thumb-2 与内存对齐 . . . . . . . . . . . . . . . . 11

1.1.1.5 流水线 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13

1.1.1.6 中断与异常处理 . . . . . . . . . . . . . . . 14

1.1.1.7 系统定时器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16

1.1.1.8 电源模式 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17

1.1.1.9 TrustZoneTM . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18

1.1.1.10 CMSIS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19

1.1.1.11 在 STM32 系列中有效实现 Cortex-M 特性 . . . . . . . . . . . . . . . . . . . . . . . . . . . 20

1.2 STM32 微控制器简介 . . . . . . . . . . . . . . . . . . . . . . . . . . 21

1.2.1STM32 产品组合的优势……. . . . . . . . . . . . . . . . . . . . . . 22</pre></td>
</tr></tbody></table>

## PDF page 6 — Chapter 0: Front Matter

Focus: `numbers=1, 1.1, 1.2, 1.3, 1.4, 10, 11, 12, 13, 14, 15, 16, 17, 18, 2, 2.1, 2.2, 2.3, 23, 24, 26, 27, 28, 29, 3; negation=; conditions=; identifiers=PC`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>CONTENTS

### 1.2.2 ….And Its Drawbacks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23 1.3 A Quick Look at the STM32 Subfamilies . . . . . . . . . . . . . . . . . . . . . . . . . . 24 1.3.1 F0 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 26 1.3.2 F1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 27 1.3.3 F2 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28 1.3.4 F3 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29 1.3.5 F4 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 31 1.3.6 F7 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 33 1.3.7 H7 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 35 1.3.8 L0 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 37 1.3.9 L1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 38 1.3.10 L4 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 39 1.3.11 L4+ . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 41 1.3.12 L5 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 42 1.3.13 U5 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 43 1.3.14 G0 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 45 1.3.15 G4 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 46 1.3.16 STM32WB . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 48 1.3.17 STM32WL . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 50 1.3.18 How to Select the Right MCU for You? . . . . . . . . . . . . . . . . . . . . 51 1.4 The Nucleo Development Board . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 54

2. Get In Touch With SM32CubeIDE . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 60 2.1 Why Choose STM32CubeIDE as Tool-Chain for STM32 . . . . . . . . . . . . . . . . 60 2.1.1 Two Words About Eclipse… . . . . . . . . . . . . . . . . . . . . . . . . . . . 62 2.1.2 … and GCC . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 62 2.2 Downloading and Installing the STM32CubeIDE . . . . . . . . . . . . . . . . . . . . . 63 2.2.1 Windows - Installing the Tool-Chain . . . . . . . . . . . . . . . . . . . . . 64 2.2.2 Linux - Installing the Tool-Chain . . . . . . . . . . . . . . . . . . . . . . . . 67 2.2.3 Mac - Installing the Tool-Chain . . . . . . . . . . . . . . . . . . . . . . . . . 68 2.3 STM32CubeIDE overview . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 70

3. Hello, Nucleo! . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 76 3.1 Create a Project . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 76 3.2 Adding Something Useful to the Generated Code . . . . . . . . . . . . . . . . . . . . 79 3.3 Connecting the Nucleo to the PC . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 84 3.3.1 ST-LINK Firmware Upgrade . . . . . . . . . . . . . . . . . . . . . . . . . . . 85 3.4 Flashing the Nucleo using STM32CubeProgrammer . . . . . . . . . . . . . . . . . . . 86

4. STM32CubeMX Tool . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 89 4.1 Introduction to CubeMX Tool . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 89 4.1.1 Target Selection Wizard . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 90 4.1.1.1 MCU/MPU Selector . . . . . . . . . . . . . . . . . . . . . . . . 91 4.1.1.2 Board Selector . . . . . . . . . . . . . . . . . . . . . . . . . . . . 92</pre></td>
<td><pre>目录

### 1.2.2 ……及其缺点 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23

1.3 STM32 子系列概览 . . . . . . . . . . . . . . . . . . . . . . . . . . 24

1.3.1 F0 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 26

1.3.2 F1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 27

1.3.3 F2 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28

1.3.4 F3 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29

1.3.5 F4 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 31

1.3.6 F7 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 33

1.3.7 H7 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 35

1.3.8 L0 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 37

1.3.9 L1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 38

1.3.10 L4 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 39

1.3.11 L4+ . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 41

1.3.12 L5 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 42

1.3.13 U5 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 43

1.3.14 G0 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 45

1.3.15 G4 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 46

1.3.16 STM32WB . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 48

1.3.17 STM32WL . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 50

1.3.18 如何为您选择合适的微控制器？ . . . . . . . . . . . . . . . . . . . . 51

1.4 Nucleo 开发板 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 54

2。与 STM32CubeIDE 建立联系 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 60 2.1 为何选择 STM32CubeIDE 作为 STM32 的工具链 . . . . . . . . . . . . . . . . 60 2.1.1 关于 Eclipse 的两句闲话… . . . . . . . . . . . . . . . . . . . . . . . . . . . 62 2.1.2 …以及 GCC . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 62 2.2 下载并安装 STM32CubeIDE . . . . . . . . . . . . . . . . . . . . . 63 2.2.1 Windows - 安装工具链 . . . . . . . . . . . . . . . . . . . . . 64 2.2.2 Linux - 安装工具链 . . . . . . . . . . . . . . . . . . . . . . . . 67 2.2.3 Mac - 安装工具链 . . . . . . . . . . . . . . . . . . . . . . . . . 68 2.3 STM32CubeIDE 概览 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 70

3。你好，Nucleo！. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 76 3.1 创建项目 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 76 3.2 为生成的代码添加实用功能 . . . . . . . . . . . . . . . . . . . . 79 3.3 将 Nucleo 连接到 PC . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 84 3.3.1 ST-LINK 固件升级 . . . . . . . . . . . . . . . . . . . . . . . . . . . 85 3.4 使用 STM32CubeProgrammer 对 Nucleo 进行烧录 . . . . . . . . . . . . . . . . . . . 86

4。STM32CubeMX 工具 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 89 4.1 CubeMX 工具简介 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 89 4.1.1 目标选择向导 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 90 4.1.1.1 MCU/MPU 选择器 . . . . . . . . . . . . . . . . . . . . . . . . 91 4.1.1.2 开发板选择器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 92</pre></td>
</tr></tbody></table>

## PDF page 7 — Chapter 0: Front Matter

Focus: `numbers=0, 1, 1.3, 1.4, 100, 102, 104, 105, 113, 115, 117, 119, 122, 125, 129, 130, 135, 136, 139, 140, 143, 144, 148, 149, 153; negation=; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>CONTENTS

#### 4.1.1.3 Example Selector . . . . . . . . . . . . . . . . . . . . . . . . . . 92 4.1.1.4 Cross Selector . . . . . . . . . . . . . . . . . . . . . . . . . . . . 94 4.1.2 MCU and Middleware Configuration . . . . . . . . . . . . . . . . . . . . . 94 4.1.2.1 Pinout View &amp; Configuration . . . . . . . . . . . . . . . . . . 95 4.1.2.2 Clock Configuration View . . . . . . . . . . . . . . . . . . . . 100 4.1.3 Project Manager . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 102 4.1.4 Tools View . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 104 4.2 Understanding Project Structure . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 105 4.3 Downloading Book Source Code Examples . . . . . . . . . . . . . . . . . . . . . . . . 113 4.4 Management of STM32Cube Packages . . . . . . . . . . . . . . . . . . . . . . . . . . . 115

5. Introduction to Debugging . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 117 5.1 What is Behind a Debug Session . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 117 5.2 Debugging With STM32CubeIDE . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 119 5.2.1 Debug Configurations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 122 5.3 I/O Retargeting . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 125

# II Diving into the HAL . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .129

6. GPIO Management . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 130 6.1 STM32 Peripherals Mapping and HAL Handlers . . . . . . . . . . . . . . . . . . . . . 130 6.2 GPIOs Configuration . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 135 6.2.1 GPIO Mode . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 136 6.2.2 GPIO Alternate Function . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 139 6.3 Driving a GPIO . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 140 6.4 De-initialize a GPIO . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 140

7. Interrupts Management . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 143 7.1 NVIC Controller . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 143 7.1.1 Vector Table in STM32 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 144 7.2 Enabling Interrupts . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 148 7.2.1 External Lines and NVIC . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 149 7.2.2 Enabling Interrupts with CubeMX . . . . . . . . . . . . . . . . . . . . . . . 153 7.3 Interrupt Lifecycle . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 155 7.4 Interrupt Priority Levels . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 159 7.4.1 Cortex-M0/0+ . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 159 7.4.2 Cortex-M3/4/7/33 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 164 7.4.3 Setting Interrupt Priority in CubeMX . . . . . . . . . . . . . . . . . . . . . 171 7.5 Interrupt Re-Entrancy . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 171 7.6 Mask All Interrupts at Once or an a Priority Basis . . . . . . . . . . . . . . . . . . . . 173

8. Universal Asynchronous Serial Communications . . . . . . . . . . . . . . . . . . . . . . . 176 8.1 Introduction to UARTs and USARTs . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 176</pre></td>
<td><pre>目录

#### 4.1.1.3 示例选择器 . . . . . . . . . . . . . . . . . . . . . . . . . . 92 4.1.1.4 交叉选择器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 94 4.1.2 MCU 和中间件配置 . . . . . . . . . . . . . . . . . . . . . 94 4.1.2.1 引脚视图与配置 . . . . . . . . . . . . . . . . . . 95 4.1.2.2 时钟配置视图 . . . . . . . . . . . . . . . . . . . . 100 4.1.3 项目管理器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 102 4.1.4 工具视图 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 104 4.2 理解项目结构 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 105 4.3 下载本书源代码示例 . . . . . . . . . . . . . . . . . . . . . . . . 113 4.4 STM32Cube 软件包管理 . . . . . . . . . . . . . . . . . . . . . . . . . . . 115

5调试简介. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 117 5.1调试会话背后的原理. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 117 5.2使用 STM32CubeIDE 进行调试. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 119 5.2.1调试配置. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 122 5.3 I/O重定向. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 125

# II 深入硬件抽象层 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .129

6。GPIO 管理 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 130 6.1 STM32 外设映射与 HAL 处理程序 . . . . . . . . . . . . . . . . . . . . . 130 6.2 GPIO 配置 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 135 6.2.1 GPIO 模式 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 136 6.2.2 GPIO 复用功能 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 139 6.3 驱动 GPIO . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 140 6.4 反初始化 GPIO . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 140

7。中断管理 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 143

7.1 NVIC 控制器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 143

7.1.1 STM32 中的向量表 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 144

7.2 启用中断 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 148

7.2.1 外部线路与 NVIC . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 149

7.2.2 使用 CubeMX 启用中断 . . . . . . . . . . . . . . . . . . . . . . . 153

7.3 中断生命周期 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 155

7.4 中断优先级 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 159

7.4.1 Cortex-M0/0+ . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 159

7.4.2 Cortex-M3/4/7/33 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 164

7.4.3 在 CubeMX 中设置中断优先级 . . . . . . . . . . . . . . . . . . . . . 171

7.5 中断重入 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 171

7.6 一次性屏蔽所有中断或按优先级屏蔽 . . . . . . . . . . . . . . . . . . . . 173

8。通用异步串行通信 . . . . . . . . . . . . . . . . . . . . . . . 176 8.1 UART 与 USART 简介 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 176</pre></td>
</tr></tbody></table>

## PDF page 8 — Chapter 0: Front Matter

Focus: `numbers=1, 1.1, 10, 10.1, 180, 187, 188, 192, 193, 194, 2, 2.1, 2.2, 2.3, 201, 202, 205, 206, 209, 210, 214, 217, 220, 223, 226; negation=; conditions=; identifiers=HAL_DMA, HAL_UART`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>CONTENTS

## 8.2 UART Initialization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 180 8.2.1 UART Configuration Using CubeMX . . . . . . . . . . . . . . . . . . . . . 187 8.3 UART Communication in Polling Mode . . . . . . . . . . . . . . . . . . . . . . . . . . 188 8.3.1 Installing a Terminal Emulator in Eclipse . . . . . . . . . . . . . . . . . . . 192 8.4 UART Communication in Interrupt Mode . . . . . . . . . . . . . . . . . . . . . . . . . 193 8.4.1 UART Related Interrupts . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 194 8.5 Error Management . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 201 8.6 List of Available Callbacks in the HAL_UART Module . . . . . . . . . . . . . . . . . . . 202

9. DMA Management . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 205 9.1 Introduction to DMA . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 205 9.1.1 The Need of a DMA and the Role of the Internal Buses . . . . . . . . . . 206 9.1.2 The DMA Controller . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 209 9.1.2.1 The DMA Implementation in F0/F1/F3/L0/L1/L4 MCUs . . 210 9.1.2.2 The DMA Implementation in F2/F4/F7 MCUs . . . . . . . . . 214 9.1.2.3 The DMA Implementation in G0/G4/L4+/L5/H7 MCUs . . . 217 9.2 HAL_DMA Module . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 220 9.2.1 DMA_HandleTypeDef in F0/F1/F3/L0/L1/L4 HALs . . . . . . . . . . . . . . . 220 9.2.2 DMA Configuration in G0/G4/L4+/L5/H7 HALs . . . . . . . . . . . . . . 223 9.2.3 DMA_HandleTypeDef in F2/F4/F7 HALs . . . . . . . . . . . . . . . . . . . . . 226 9.2.4 How to Perform DMA Transfers in Polling Mode . . . . . . . . . . . . . . 229 9.2.5 How to Perform DMA Transfers in Interrupt Mode . . . . . . . . . . . . . 232 9.2.6 Using the HAL_UART Module with DMA Mode Transfers . . . . . . . . . . 233 9.2.7 Programming the DMAMUX With the CubeHAL . . . . . . . . . . . . . . 236 9.2.8 Miscellaneous Functions From HAL_DMA and HAL_DMA_Ex Modules . . . . 237 9.3 Using CubeMX to Configure DMA Requests . . . . . . . . . . . . . . . . . . . . . . . 238 9.4 Correct Memory Allocation of DMA Buffers . . . . . . . . . . . . . . . . . . . . . . . 239 9.5 A Case Study: The DMA Memory-To-Memory Transfer Performance Analysis . . . 240

10. Clock Tree . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 245

## 10.1 Clock Distribution . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 245 10.1.1 Overview of the STM32 Clock Tree . . . . . . . . . . . . . . . . . . . . . . 246 10.1.1.1 The Multispeed Internal RC Oscillator in STM32L/U Families 250 10.1.2 Configuring Clock Tree Using CubeMX . . . . . . . . . . . . . . . . . . . . 251 10.1.3 Clock Source Options in Nucleo Boards . . . . . . . . . . . . . . . . . . . . 253 10.1.3.1 Clock Source in Nucleo-64 rev. MB1136 (older ones with ST-LINK V2.1) . . . . . . . . . . . . . . . . . . . . . . . . . . . . 254 10.1.3.1.1 OSC Clock Supply . . . . . . . . . . . . . . . . . . . . . . . . . . . 254 10.1.3.1.2 OSC 32kHz Clock Supply . . . . . . . . . . . . . . . . . . . . . . . 255

#### 10.1.3.2 Clock Source in Nucleo-64 rev. MB1367 (newer ones with ST-LINK v3) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 256 10.1.3.2.1 OSC Clock Supply . . . . . . . . . . . . . . . . . . . . . . . . . . . 256 10.1.3.2.2 OSC 32kHz Clock Supply . . . . . . . . . . . . . . . . . . . . . . . 257</pre></td>
<td><pre>目录

## 8.2 UART 初始化 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 180 8.2.1 使用 CubeMX 配置 UART . . . . . . . . . . . . . . . . . . . . . 187 8.3 轮询模式下的 UART 通信 . . . . . . . . . . . . . . . . . . . . . . . . . . 188 8.3.1 在 Eclipse 中安装终端仿真器 . . . . . . . . . . . . . . . . . . . 192 8.4 中断模式下的 UART 通信 . . . . . . . . . . . . . . . . . . . . . . . . . 193 8.4.1 UART 相关中断 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 194 8.5 错误管理 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 201 8.6 HAL_UART 模块中可用的回调函数列表 . . . . . . . . . . . . . . . . . . . 202

9。直接存储器访问管理 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 205

9.1 直接存储器访问简介 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 205

9.1.1 直接存储器访问（DMA）的需求及内部总线的作用 . . . . . . . . . . 206

9.1.2 DMA 控制器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 209

9.1.2.1 在 F0/F1/F3/L0/L1/L4 微控制器中的直接存储器访问实现 . . 210

9.1.2.2 在 F2/F4/F7 微控制器中的直接存储器访问实现 . . . . . . . . . 214

9.1.2.3 G0/G4/L4+/L5/H7 微控制器中的直接存储器访问实现 . . . 217

9.2 HAL_DMA 模块 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 220

9.2.1 在 F0/F1/F3/L0/L1/L4 硬件抽象层中的 . . . . . . . . . . . . . . . 220

9.2.2 在 G0/G4/L4+/L5/H7 硬件抽象层中的 DMA 配置 . . . . . . . . . . . . . . 223

9.2.3 在 F2/F4/F7 硬件抽象层中的 . . . . . . . . . . . . . . . . . . . . . 226

9.2.4 如何在轮询模式下执行 DMA 传输 . . . . . . . . . . . . . . 229

9.2.5 如何在中断模式下执行 DMA 传输 . . . . . . . . . . . . . 232

9.2.6 使用 HAL_UART 模块进行直接存储器访问模式传输 . . . . . . . . . . 233

9.2.7 使用 CubeHAL 编程 DMAMUX . . . . . . . . . . . . . . 236

9.2.8 来自 HAL_DMA 和 HAL_DMA_Ex 模块的杂项功能 . . . . 237

9.3 使用 CubeMX 配置 DMA 请求 . . . . . . . . . . . . . . . . . . . . . . . 238

9.4 直接存储器访问缓冲区的正确内存分配 . . . . . . . . . . . . . . . . . . . . . . . 239

9.5 案例研究：DMA 内存到内存传输性能分析 . . . 240

10。时钟树 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 245

## 10.1 时钟分配 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 245 10.1.1 STM32 时钟树概述 . . . . . . . . . . . . . . . . . . . . . . 246 10.1.1.1 STM32L/U 系列中的多速内部 RC 振荡器 250 10.1.2 使用 CubeMX 配置时钟树 . . . . . . . . . . . . . . . . . . . . 251 10.1.3 Nucleo 开发板中的时钟源选项 . . . . . . . . . . . . . . . . . . . . 253 10.1.3.1 Nucleo-64 rev. MB1136（较旧版本，配备 ST-LINK V2.1） . . . . . . . . . . . . . . . . . . . . . . . . . . . . 254 10.1.3.1.1 OSC 时钟供电 . . . . . . . . . . . . . . . . . . . . . . . . . . . 254 10.1.3.1.2 OSC 32kHz 时钟供电 . . . . . . . . . . . . . . . . . . . . . . . 255

#### 10.1.3.2 Nucleo-64 rev. MB1367 中的时钟源（较新版本，配备 ST-LINK v3） . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 256 10.1.3.2.1 OSC 时钟供电 . . . . . . . . . . . . . . . . . . . . . . . . . . . 256 10.1.3.2.2 OSC 32kHz 时钟供电 . . . . . . . . . . . . . . . . . . . . . . . 257</pre></td>
</tr></tbody></table>

## PDF page 9 — Chapter 0: Front Matter

Focus: `numbers=1, 1.1, 1.2, 1.3, 10, 10.1, 10.2, 10.3, 11, 11.1, 11.2, 11.3, 2, 2.1, 2.2, 257, 259, 260, 261, 263, 264, 266, 269, 272, 274; negation=; conditions=; identifiers=HAL_RCC`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>CONTENTS

## 10.2 Overview of the HAL_RCC Module . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 257 10.2.1 Compute the Clock Frequency at Run-Time . . . . . . . . . . . . . . . . . 259 10.2.2 Enabling the Master Clock Output . . . . . . . . . . . . . . . . . . . . . . . 260 10.2.3 Enabling the Clock Security System . . . . . . . . . . . . . . . . . . . . . . 260 10.3 HSI Calibration . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 261

11. Timers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 263

## 11.1 Introduction to Timers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 263 11.1.1 Timer Categories in an STM32 MCU . . . . . . . . . . . . . . . . . . . . . . 264 11.1.2 Effective Availability of Timers in the STM32 Portfolio . . . . . . . . . . 266 11.2 Basic Timers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 269 11.2.1 Using Timers in Interrupt Mode . . . . . . . . . . . . . . . . . . . . . . . . . 272 11.2.1.1 Time Base Generation in Advanced Timers . . . . . . . . . . 274 11.2.2 Using Timers in Polling Mode . . . . . . . . . . . . . . . . . . . . . . . . . . 274 11.2.3 Using Timers in DMA Mode . . . . . . . . . . . . . . . . . . . . . . . . . . . 275 11.2.4 Stopping a Timer . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 278 11.2.5 Using CubeMX to Configure a Basic Timer . . . . . . . . . . . . . . . . . 278 11.3 General Purpose Timers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 278 11.3.1 Time Base Generator with External Clock Sources . . . . . . . . . . . . . 279 11.3.1.1 External Clock Mode 2 . . . . . . . . . . . . . . . . . . . . . . . 281 11.3.1.2 External Clock Mode 1 . . . . . . . . . . . . . . . . . . . . . . . 284 11.3.1.3 Using CubeMX to Configure the Source Clock of a General Purpose Timer . . . . . . . . . . . . . . . . . . . . . . . . . . . . 289 11.3.2 Master/Slave Synchronization Modes . . . . . . . . . . . . . . . . . . . . . 290 11.3.2.1 Enable Trigger-Related Interrupts . . . . . . . . . . . . . . . . 296 11.3.2.2 Using CubeMX to Configure the Master/Slave Synchronization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 296 11.3.3 Generate Timer-Related Events by Software . . . . . . . . . . . . . . . . . 297 11.3.4 Counting Modes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 299 11.3.5 Input Capture Mode . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 300 11.3.5.1 Using CubeMX to Configure the Input Capture Mode . . . 307 11.3.6 Output Compare Mode . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 308 11.3.6.1 Using CubeMX to Configure the Output Compare Mode . . 313 11.3.7 Pulse-Width Generation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 313 11.3.7.1 Generating a Sinusoidal Wave Using PWM . . . . . . . . . . 317 11.3.7.2 Using CubeMX to Configure the PWM Mode . . . . . . . . . 322 11.3.8 One Pulse Mode . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 322 11.3.8.1 Using CubeMX to Configure the OPM Mode . . . . . . . . . 325 11.3.9 Encoder Mode . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 325 11.3.9.1 Using CubeMX to Configure the Encoder Mode . . . . . . . 331 11.3.10 Other Features Available in General Purpose and Advanced Timers . . . 331 11.3.10.1 Hall Sensor Mode . . . . . . . . . . . . . . . . . . . . . . . . . . 332</pre></td>
<td><pre>目录

## 10.2 HAL_RCC 模块概述 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 257 10.2.1 在运行时计算时钟频率 . . . . . . . . . . . . . . . . . 259 10.2.2 启用主时钟输出 . . . . . . . . . . . . . . . . . . . . . . . 260 10.2.3 启用时钟安全系统 . . . . . . . . . . . . . . . . . . . . . . 260 10.3 HSI 校准 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 261

11。定时器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 263

##

11.1 定时器简介 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 263

11.1.1 STM32 微控制器中的定时器类别 . . . . . . . . . . . . . . . . . . . . . . 264

11.1.2 STM32 系列中定时器的有效可用性 . . . . . . . . . . 266

11.2 基本定时器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 269

11.2.1 在中断模式下使用定时器 . . . . . . . . . . . . . . . . . . . . . . . . . 272

11.2.1.1 高级定时器中的时基生成 . . . . . . . . . . 274

11.2.2 以轮询模式使用定时器 . . . . . . . . . . . . . . . . . . . . . . . . . . 274

11.2.3 在直接存储器访问模式下使用定时器 . . . . . . . . . . . . . . . . . . . . . . . . . . . 275

11.2.4 停止定时器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 278

11.2.5 使用 CubeMX 配置基本定时器 . . . . . . . . . . . . . . . . . 278

11.3 通用定时器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 278

11.3.1 具有外部时钟源的时间基准发生器 . . . . . . . . . . . . . 279

11.3.1.1 外部时钟模式 2 . . . . . . . . . . . . . . . . . . . . . . . 281

11.3.1.2 外部时钟模式 1 . . . . . . . . . . . . . . . . . . . . . . . 284

11.3.1.3 使用 CubeMX 配置通用定时器的源时钟 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 289

11.3.2 Master/Slave 同步模式 . . . . . . . . . . . . . . . . . . . . . 290

11.3.2.1 启用触发器相关中断 . . . . . . . . . . . . . . . . 296

11.3.2.2 使用 CubeMX 配置 Master/Slave 同步 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 296

11.3.3 通过软件生成定时器相关事件 . . . . . . . . . . . . . . . . . 297

11.3.4 计数模式 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 299

11.3.5 输入捕获模式 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 300

11.3.5.1 使用 CubeMX 配置输入捕获模式 . . . 307

11.3.6 输出比较模式 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 308

11.3.6.1 使用 CubeMX 配置输出比较模式 313

11.3.7 脉宽生成 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 313

11.3.7.1 使用 PWM 生成正弦波 . . . . . . . . . . 317

11.3.7.2 使用 CubeMX 配置 PWM 模式 . . . . . . . . . 322

11.3.8 单脉冲模式 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 322

11.3.8.1 使用 CubeMX 配置 OPM 模式 . . . . . . . . . 325

11.3.9 编码器模式 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 325

11.3.9.1 使用 CubeMX 配置编码器模式 . . . . . . . 331

11.3.10 通用定时器和高级定时器中可用的其他功能 . . . 331

11.3.10.1 霍尔传感器模式 . . . . . . . . . . . . . . . . . . . . . . . . . . 332</pre></td>
</tr></tbody></table>

## PDF page 10 — Chapter 0: Front Matter

Focus: `numbers=1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 10, 10.2, 10.3, 10.4, 11, 11.3, 11.4, 11.5, 12, 12.1, 12.2, 12.3, 13, 13.1, 13.2, 14, 14.1, 2; negation=not; conditions=; identifiers=HAL_ADC, HAL_DAC`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>CONTENTS

#### 11.3.10.2 Combined Three-Phase PWM Mode and Other Motor- Control Related Features . . . . . . . . . . . . . . . . . . . . . 332 11.3.10.3 Break Input and Locking of Timer Registers . . . . . . . . . . 333 11.3.10.4 Preloading of Auto-Reload Register . . . . . . . . . . . . . . . 333 11.3.11 Debugging and Timers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 334 11.4 SysTick Timer . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 335 11.4.1 Use Another Timer as System Timebase Source . . . . . . . . . . . . . . . 336 11.5 A Case Study: How to Precisely Measure Microseconds with STM32 MCUs . . . . 337

12. Analog-To-Digital Conversion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 343

## 12.1 Introduction to SAR ADC . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 343 12.2 HAL_ADC Module . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 348 12.2.1 Conversion Modes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 350 12.2.1.1 Single-Channel, Single Conversion Mode . . . . . . . . . . . 350 12.2.1.2 Scan Single Conversion Mode . . . . . . . . . . . . . . . . . . 351 12.2.1.3 Single-Channel, Continuous Conversion Mode . . . . . . . . 351 12.2.1.4 Scan Continuous Conversion Mode . . . . . . . . . . . . . . . 352 12.2.1.5 Injected Conversion Mode . . . . . . . . . . . . . . . . . . . . 352 12.2.1.6 Dual Modes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 353 12.2.2 Channel Selection . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 353 12.2.3 ADC Resolution and Conversion Speed . . . . . . . . . . . . . . . . . . . . 355 12.2.4 A/D Conversions in Polling Mode . . . . . . . . . . . . . . . . . . . . . . . 356 12.2.5 A/D Conversions in Interrupt Mode . . . . . . . . . . . . . . . . . . . . . . 360 12.2.6 A/D Conversions in DMA Mode . . . . . . . . . . . . . . . . . . . . . . . . 361 12.2.6.1 Convert Multiple Times the Same Channel in DMA Mode . 365 12.2.6.2 Multiple and not Continuous Conversions in DMA Mode . 365 12.2.6.3 Continuous Conversions in DMA Mode . . . . . . . . . . . . 365 12.2.7 Errors Management . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 365 12.2.8 Timer-Driven Conversions . . . . . . . . . . . . . . . . . . . . . . . . . . . . 366 12.2.9 Conversions Driven by External Events . . . . . . . . . . . . . . . . . . . . 370 12.2.10 ADC Calibration . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 370 12.3 Using CubeMX to Configure ADC Peripheral . . . . . . . . . . . . . . . . . . . . . . . 371

13. Digital-To-Analog Conversion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 373

## 13.1 Introduction to the DAC Peripheral . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 373 13.2 HAL_DAC Module . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 375 13.2.1 Driving the DAC Manually . . . . . . . . . . . . . . . . . . . . . . . . . . . 377 13.2.2 Driving the DAC in DMA Mode Using a Timer . . . . . . . . . . . . . . . 379 13.2.3 Triangular Wave Generation . . . . . . . . . . . . . . . . . . . . . . . . . . . 383 13.2.4 Noise Wave Generation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 384

14. I²C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 385

## 14.1 Introduction to the I²C specification . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 385 14.1.1 The I²C Protocol . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 387</pre></td>
<td><pre>目录

#### 11.3.10.2 组合三相 PWM 模式及其他电机控制相关功能 . . . . . . . . . . . . . . . . . . . . . 332 11.3.10.3 中断输入和定时器寄存器锁定 . . . . . . . . . . 333 11.3.10.4 自动重载寄存器预加载 . . . . . . . . . . . . . . . 333 11.3.11 调试和定时器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 334 11.4 SysTick 定时器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 335 11.4.1 使用另一个定时器作为系统时基源 . . . . . . . . . . . . . . . 336 11.5 案例研究：如何使用 STM32 微控制器精确测量微秒 . . . . 337

12. 模数转换 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 343

##

12.1 SAR ADC 简介 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 343

12.2 HAL_ADC 模块 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 348

12.2.1 转换模式 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 350

12.2.1.1 单通道、单次转换模式 . . . . . . . . . . . 350

12.2.1.2 单次转换扫描模式 . . . . . . . . . . . . . . . . . . 351

12.2.1.3 单通道、连续转换模式 . . . . . . . . 351

12.2.1.4 扫描连续转换模式 . . . . . . . . . . . . . . . 352

12.2.1.5注入转换模式. . . . . . . . . . . . . . . . . . . . 352

12.2.1.6 双模式 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 353

12.2.2 通道选择 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 353

12.2.3 ADC 分辨率与转换速度 . . . . . . . . . . . . . . . . . . . . 355

12.2.4 A/D 轮询模式下的转换 . . . . . . . . . . . . . . . . . . . . . . . 356

12.2.5 A/D 中断模式下的转换 . . . . . . . . . . . . . . . . . . . . . . 360

12.2.6 A/D DMA 模式下的转换 . . . . . . . . . . . . . . . . . . . . . . . . 361

12.2.6.1 在 DMA 模式下对同一通道进行多次转换。 365

12.2.6.2 DMA 模式下的多次非连续转换。 365

12.2.6.3 DMA 模式下的连续转换 . . . . . . . . . . . . 365

12.2.7 错误管理 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 365

12.2.8 定时器触发的转换 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 366

12.2.9 由外部事件触发的转换 . . . . . . . . . . . . . . . . . . . . 370

12.2.10 ADC 校准 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 370

12.3 使用 CubeMX 配置 ADC 外设 . . . . . . . . . . . . . . . . . . . . . . . 371

13。数模转换 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 373

## 13.1 DAC 外设简介 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 373 13.2 HAL_DAC 模块 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 375 13.2.1 手动驱动 DAC . . . . . . . . . . . . . . . . . . . . . . . . . . . 377 13.2.2 使用定时器以 DMA 模式驱动 DAC . . . . . . . . . . . . . . . 379 13.2.3 三角波生成 . . . . . . . . . . . . . . . . . . . . . . . . . . . 383 13.2.4 噪声波生成 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 384

14. I²C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 385

## 14.1 I²C 规范简介 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 385 14.1.1 I²C 协议 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 387</pre></td>
</tr></tbody></table>

## PDF page 11 — Chapter 0: Front Matter

Focus: `numbers=1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 14.1, 14.2, 14.3, 15, 15.1, 15.2, 15.3, 16, 16.1, 16.2, 17, 17.1, 17.2, 17.3, 17.4, 17.5, 18; negation=Not; conditions=; identifiers=HAL_CRC, HAL_I2C, HAL_SPI`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>CONTENTS

#### 14.1.1.1 START and STOP Condition . . . . . . . . . . . . . . . . . . . 388 14.1.1.2 Byte Format . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 388 14.1.1.3 Address Frame . . . . . . . . . . . . . . . . . . . . . . . . . . . 388 14.1.1.4 Acknowledge (ACK) and Not Acknowledge (NACK) . . . . 389 14.1.1.5 Data Frames . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 389 14.1.1.6 Combined Transactions . . . . . . . . . . . . . . . . . . . . . . 390 14.1.1.7 Clock Stretching . . . . . . . . . . . . . . . . . . . . . . . . . . 391 14.1.2 Availability of I²C Peripherals in STM32 MCUs . . . . . . . . . . . . . . . 391 14.2 HAL_I2C Module . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 392 14.2.1 Using the I²C Peripheral in Master Mode . . . . . . . . . . . . . . . . . . . 396 14.2.1.1 I/O MEM Operations . . . . . . . . . . . . . . . . . . . . . . . . 403 14.2.1.2 Combined Transactions . . . . . . . . . . . . . . . . . . . . . . 405 14.2.1.3 A Note About the Clock Configuration in STM32F0/L0/L4 families . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 406 14.2.2 Using the I²C Peripheral in Slave Mode . . . . . . . . . . . . . . . . . . . . 406 14.3 Using CubeMX to Configure the I²C Peripheral . . . . . . . . . . . . . . . . . . . . . . 412

15. SPI . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 414

## 15.1 Introduction to the SPI Specification . . . . . . . . . . . . . . . . . . . . . . . . . . . . 414 15.1.1 Clock Polarity and Phase . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 417 15.1.2 Slave Select Signal Management . . . . . . . . . . . . . . . . . . . . . . . . 418 15.1.3 SPI TI Mode . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 418 15.1.4 Availability of SPI Peripherals in STM32 MCUs . . . . . . . . . . . . . . . 419 15.2 HAL_SPI Module . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 420 15.2.1 Exchanging Messages Using SPI Peripheral . . . . . . . . . . . . . . . . . . 422 15.2.2 Maximum Transmission Frequency Reachable using the CubeHAL . . . 424 15.3 Using CubeMX to Configure SPI Peripheral . . . . . . . . . . . . . . . . . . . . . . . . 424

16. Cyclic Redundancy Check . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 425

## 16.1 Introduction to CRC Computing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 425 16.1.1 CRC Calculation in STM32F1/F2/F4/L1 MCUs . . . . . . . . . . . . . . . . 428 16.1.2 CRC Peripheral in STM32F0/F3/F7/L0/L4/L5/G0/G4 MCUs . . . . . . . . 430 16.2 HAL_CRC Module . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 431

17. IWDG and WWDG Timers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 434 17.1 The Independent Watchdog Timer . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 434 17.1.1 Using the CubeHAL to Program IWDG Timer . . . . . . . . . . . . . . . . 435 17.2 The System Window Watchdog Timer . . . . . . . . . . . . . . . . . . . . . . . . . . . . 436 17.2.1 Using the CubeHAL to Program WWDG Timer . . . . . . . . . . . . . . . 438 17.3 Detecting a System Reset Caused by a Watchdog Timer . . . . . . . . . . . . . . . . 439 17.4 Freezing Watchdog Timers During a Debug Session . . . . . . . . . . . . . . . . . . . 440 17.5 Selecting the Right Watchdog Timer for Your Application . . . . . . . . . . . . . . . 440

18. Real-Time Clock . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 441</pre></td>
<td><pre>目录

#### 14.1.1.1 起始和停止条件 . . . . . . . . . . . . . . . . . . . 388 14.1.1.2 字节格式 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 388 14.1.1.3 地址帧 . . . . . . . . . . . . . . . . . . . . . . . . . . . 388 14.1.1.4 应答（ACK）和非应答（NACK） . . . . 389 14.1.1.5 数据帧 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 389 14.1.1.6 组合事务 . . . . . . . . . . . . . . . . . . . . . . 390 14.1.1.7 时钟拉伸 . . . . . . . . . . . . . . . . . . . . . . . . . . 391 14.1.2 STM32 微控制器中 I²C 外设的可用性 . . . . . . . . . . . . . . . 391 14.2 HAL_I2C 模块 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 392 14.2.1 以主模式使用 I²C 外设 . . . . . . . . . . . . . . . . . . . 396 14.2.1.1 I/O MEM 操作 . . . . . . . . . . . . . . . . . . . . . . . . 403 14.2.1.2 组合事务 . . . . . . . . . . . . . . . . . . . . . . 405 14.2.1.3 关于 STM32F0/L0/L4 系列时钟配置的说明 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 406 14.2.2 以从模式使用 I²C 外设 . . . . . . . . . . . . . . . . . . . . 406 14.3 使用 CubeMX 配置 I²C 外设 . . . . . . . . . . . . . . . . . . . . . . 412

15. SPI . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 414

## 15.1 SPI 规范简介 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 414 15.1.1 时钟极性和相位 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 417 15.1.2 从设备选择信号管理 . . . . . . . . . . . . . . . . . . . . . . . . 418 15.1.3 SPI TI 模式 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 418 15.1.4 STM32 微控制器中 SPI 外设的可用性 . . . . . . . . . . . . . . . 419 15.2 HAL_SPI 模块 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 420 15.2.1 使用 SPI 外设交换消息 . . . . . . . . . . . . . . . . . . 422 15.2.2 使用 CubeHAL 可达到的最大传输频率 . . . 424 15.3 使用 CubeMX 配置 SPI 外设 . . . . . . . . . . . . . . . . . . . . . . . . 424

16. 循环冗余校验 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 425

## 16.1 CRC 计算简介 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 425 16.1.1 在 STM32F1/F2/F4/L1 微控制器中执行 CRC 计算 . . . . . . . . . . . . . . . . 428 16.1.2 微控制器中的 CRC 外设 STM32F0/F3/F7/L0/L4/L5/G0/G4. . . . . . . . 430 16.2 HAL_CRC 模块 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 431

17.  IWDG 和 WWDG 定时器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 434 17.1 独立看门狗定时器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 434 17.1.1 使用 CubeHAL 编程 IWDG 定时器 . . . . . . . . . . . . . . . . 435 17.2 系统窗口看门狗定时器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 436 17.2.1 使用 CubeHAL 编程 WWDG 定时器 . . . . . . . . . . . . . . . 438 17.3 检测由看门狗定时器引起的系统复位 . . . . . . . . . . . . . . . . 439 17.4 在调试会话期间冻结看门狗定时器 . . . . . . . . . . . . . . . . . . . 440 17.5 为您的应用选择合适的看门狗定时器 . . . . . . . . . . . . . . . 440

18.  实时时钟 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 441</pre></td>
</tr></tbody></table>

## PDF page 12 — Chapter 0: Front Matter

Focus: `numbers=1, 1.1, 18.1, 18.2, 18.3, 19, 19.1, 19.2, 19.3, 19.4, 2, 2.1, 2.2, 2.3, 2.4, 2.5, 3, 4, 441, 443, 444, 446, 447, 449, 451; negation=; conditions=; identifiers=HAL_RTC`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>CONTENTS

## 18.1 Introduction to the RTC Peripheral . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 441 18.2 HAL_RTC Module . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 443 18.2.1 Setting and Retrieving the Current Date/Time . . . . . . . . . . . . . . . . 444 18.2.1.1 Correct Way to Read Date/Time Values . . . . . . . . . . . . 446 18.2.2 Configuring Alarms . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 447 18.2.3 Periodic Wakeup Unit . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 449 18.2.4 Timestamp Generation and Tamper Detection . . . . . . . . . . . . . . . . 451 18.2.5 RTC Calibration . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 451 18.2.5.1 RTC Coarse Calibration . . . . . . . . . . . . . . . . . . . . . . 452 18.2.5.2 RTC Smooth Calibration . . . . . . . . . . . . . . . . . . . . . 452 18.2.5.3 Reference Clock Detection . . . . . . . . . . . . . . . . . . . . 454 18.3 Using the Backup SRAM . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 454

# III Advanced topics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .456

19. Power Management . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 457

## 19.1 Power Management in Cortex-M Based MCUs . . . . . . . . . . . . . . . . . . . . . . 457 19.2 How Cortex-M MCUs Handle Run and Sleep Modes . . . . . . . . . . . . . . . . . . 458 19.2.1 Entering/exiting sleep modes . . . . . . . . . . . . . . . . . . . . . . . . . . 461 19.2.1.1 Sleep-On-Exit . . . . . . . . . . . . . . . . . . . . . . . . . . . . 463 19.2.2 Sleep Modes in Cortex-M Based MCUs . . . . . . . . . . . . . . . . . . . . 463 19.3 Power Management in STM32F Microcontrollers . . . . . . . . . . . . . . . . . . . . . 464 19.3.1 Power Sources . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 464 19.3.2 Power Modes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 465 19.3.2.1 Run Mode . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 466 19.3.2.1.1 Dynamic Voltage Scaling in STM32F4/F7 MCUs . . . . . . . . . 467 19.3.2.1.2 Over/Under-Drive Mode in STM32F4/F7 MCUs . . . . . . . . . 468

#### 19.3.2.2 Sleep Mode . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 468 19.3.2.3 Stop Mode . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 469 19.3.2.4 Standby Mode . . . . . . . . . . . . . . . . . . . . . . . . . . . . 470 19.3.2.5 Low-Power Modes Example . . . . . . . . . . . . . . . . . . . 470 19.3.3 An Important Warning for STM32F1 Microcontrollers . . . . . . . . . . . 474 19.4 Power Management in STM32L/G Microcontrollers . . . . . . . . . . . . . . . . . . . 476 19.4.1 Power Sources . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 476 19.4.2 Power Modes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 478 19.4.2.1 Run Modes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 478 19.4.2.2 Sleep Modes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 480 19.4.2.2.1 Batch Acquisition Mode . . . . . . . . . . . . . . . . . . . . . . . . 481

#### 19.4.2.3 Stop Modes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 481 19.4.2.4 Standby Modes . . . . . . . . . . . . . . . . . . . . . . . . . . . 482 19.4.2.5 Shutdown Mode . . . . . . . . . . . . . . . . . . . . . . . . . . . 483 19.4.3 Power Modes Transitions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 483</pre></td>
<td><pre>目录

##

18.1 RTC 外设简介 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 441

18.2 HAL_RTC 模块 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 443

18.2.1 设置和获取当前 Date/Time . . . . . . . . . . . . . . . . 444

18.2.1.1 正确读取 Date/Time 值的方法 . . . . . . . . . . . . 446

18.2.2 配置闹钟 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 447

18.2.3 周期性唤醒单元 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 449

18.2.4 时间戳生成与防篡改检测 . . . . . . . . . . . . . . . . 451

18.2.5 RTC 校准 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 451

18.2.5.1 RTC 粗校准 . . . . . . . . . . . . . . . . . . . . . . 452

18.2.5.2 RTC 平滑校准 . . . . . . . . . . . . . . . . . . . . . 452

18.2.5.3 参考时钟检测 . . . . . . . . . . . . . . . . . . . . 454

18.3 使用备份 SRAM . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 454

# III 高级主题 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .456

19。电源管理 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 457

##

19.1 基于 Cortex-M 的微控制器中的电源管理 . . . . . . . . . . . . . . . . . . . . . . 457

19.2 Cortex-M 微控制器如何处理运行模式和睡眠模式 . . . . . . . . . . . . . . . . . . 458

19.2.1 Entering/exiting 睡眠模式 . . . . . . . . . . . . . . . . . . . . . . . . . . 461

19.2.1.1 退出时休眠 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 463

19.2.2 基于Cortex-M的微控制器的睡眠模式 . . . . . . . . . . . . . . . . . . . . 463

19.3 STM32F 微控制器的电源管理 . . . . . . . . . . . . . . . . . . . . . 464

19.3.1 电源 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 464

19.3.2 电源模式 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 465

19.3.2.1 运行模式 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 466

19.3.2.1.1 在 STM32F4/F7 微控制器中的动态电压调节 . . . . . . . . . 467

19.3.2.1.2 Over/Under-Drive 模式在 STM32F4/F7 微控制器中 . . . . . . . . . 468

####

19.3.2.2 睡眠模式 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 468

19.3.2.3 停止模式 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 469

19.3.2.4 待机模式 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 470

19.3.2.5 低功耗模式示例 . . . . . . . . . . . . . . . . . . . 470

19.3.3 关于 STM32F1 微控制器的重要警告 . . . . . . . . . . . 474

19.4 STM32L/G 微控制器中的电源管理 . . . . . . . . . . . . . . . . . . . 476

19.4.1 电源 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 476

19.4.2 电源模式 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 478

19.4.2.1 运行模式 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 478

19.4.2.2 睡眠模式 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 480

19.4.2.2.1 批量采集模式 . . . . . . . . . . . . . . . . . . . . . . . . 481

#### 19.4.2.3 停止模式 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 481 19.4.2.4 待机模式 . . . . . . . . . . . . . . . . . . . . . . . . . . . 482 19.4.2.5 关机模式 . . . . . . . . . . . . . . . . . . . . . . . . . . . 483 19.4.3 电源模式转换 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 483</pre></td>
</tr></tbody></table>

## PDF page 13 — Chapter 0: Front Matter

Focus: `numbers=1, 1.1, 1.2, 19.4, 19.5, 19.6, 19.7, 19.8, 2, 2.1, 20, 20.1, 20.2, 20.3, 20.4, 21, 21.1, 21.2, 21.3, 21.4, 21.5, 22, 3, 4, 4.1; negation=; conditions=; identifiers=HAL_FLASH`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>CONTENTS

### 19.4.4 Low-Power Peripherals . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 484 19.4.4.1 LPUART . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 484 19.4.4.2 LPTIM . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 485 19.4.4.3 LPGPIO . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 485 19.4.4.4 LPDMA . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 486 19.5 Power Supply Supervisors . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 486 19.6 Debugging in Low-Power Modes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 487 19.7 Using the CubeMX Power Consumption Calculator . . . . . . . . . . . . . . . . . . . 487 19.8 A Case Study: Using Watchdog Timers With Low-Power Modes . . . . . . . . . . . 489

20. Memory layout . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 490

## 20.1 The STM32 Memory Layout Model . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 490 20.1.1 Flash Memory Typical Organization . . . . . . . . . . . . . . . . . . . . . . 490 20.1.2 SRAM Memory Typical Organization . . . . . . . . . . . . . . . . . . . . . 492 20.1.3 Understanding Compilation and Linking Processes . . . . . . . . . . . . . 493 20.2 The Really Minimal STM32 Application . . . . . . . . . . . . . . . . . . . . . . . . . . 495 20.2.1 ELF Binary File Inspection . . . . . . . . . . . . . . . . . . . . . . . . . . . . 499 20.2.2 .data and .bss Sections Initialization . . . . . . . . . . . . . . . . . . . . . 501 20.2.2.1 A Word About the COMMON Section . . . . . . . . . . . . . . . . 508 20.2.3 .rodata Section . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 509 20.2.4 Stack and Heap Regions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 511 20.2.5 Checking the Size of Heap and Stack at Compile-Time . . . . . . . . . . . 514 20.2.6 Differences With the Tool-Chain Script Files . . . . . . . . . . . . . . . . . 515 20.3 How to Use the CCM Memory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 520 20.3.1 Relocating the vector table in CCM Memory . . . . . . . . . . . . . . . . . 524 20.4 How to Use the MPU in Cortex-M0+/3/4/7 Based STM32 MCUs . . . . . . . . . . . 527 20.4.1 Programming the MPU With the CubeHAL . . . . . . . . . . . . . . . . . 531

21. Flash Memory Management . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 534

## 21.1 Introduction to STM32 Flash Memory . . . . . . . . . . . . . . . . . . . . . . . . . . . 534 21.2 The HAL_FLASH Module . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 537 21.2.1 Flash Memory Unlocking . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 538 21.2.2 Flash Memory Erasing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 538 21.2.3 Flash Memory Programming . . . . . . . . . . . . . . . . . . . . . . . . . . 540 21.2.4 Flash Read Access During Programming and Erasing . . . . . . . . . . . 541 21.3 Option Bytes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 541 21.3.1 Flash Memory Read Protection . . . . . . . . . . . . . . . . . . . . . . . . . 543 21.4 Optional OTP and True-EEPROM Memories . . . . . . . . . . . . . . . . . . . . . . . 545 21.5 Flash Read Latency and the ART™Accelerator . . . . . . . . . . . . . . . . . . . . . . 547 21.5.1 The Role of the TCM Memories in STM32F7/H7 MCUs . . . . . . . . . . 549 21.5.1.1 How to Access Flash Memory Through the TCM Interface . 555 21.5.1.2 Using CubeMX to Configure Flash Memory Interface . . . . 556

22. Booting Process . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 558</pre></td>
<td><pre>目录

### 19.4.4 低功耗外设 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 484 19.4.4.1 LPUART . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 484 19.4.4.2 LPTIM . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 485 19.4.4.3 LPGPIO . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 485 19.4.4.4 LPDMA . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 486 19.5 电源监控器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 486 19.6 低功耗模式下的调试 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 487 19.7 使用 CubeMX 功耗计算器 . . . . . . . . . . . . . . . . . . . 487 19.8 案例研究：在低功耗模式下使用看门狗定时器 . . . . . . . . . . . 489

20。内存布局 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 490

##

20.1 STM32 内存布局模型 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 490

20.1.1 闪存存储器典型组织结构 . . . . . . . . . . . . . . . . . . . . . . 490

20.1.2 SRAM 内存典型组织 . . . . . . . . . . . . . . . . . . . . . 492

20.1.3 理解编译与链接过程 . . . . . . . . . . . . . 493

20.2 极简 STM32 应用程序 . . . . . . . . . . . . . . . . . . . . . . . . . . 495

20.2.1 ELF 二进制文件检查 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 499 20.2.2 .data 和 .bss 段的初始化 . . . . . . . . . . . . . . . . . . . . . 501

20.2.2.1 关于 COMMON 段 . . . . . . . . . . . . . . . . 508 20.2.3 .rodata 段 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 509

20.2.4 堆栈和堆区域 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 511

20.2.5 在编译时检查堆和栈的大小 . . . . . . . . . . . 514

20.2.6 与工具链脚本文件的差异 . . . . . . . . . . . . . . . . . 515

20.3 如何使用 CCM 内存 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 520

20.3.1 将向量表重定位到 CCM 内存 . . . . . . . . . . . . . . . . . 524

20.4 如何在基于 /3/4/7 Cortex-M0+ . . . . . . . . . . .  的 STM32 微控制器中使用 MPU 527

20.4.1 使用 CubeHAL 编程 MPU . . . . . . . . . . . . . . . . . 531

21。闪存内存管理 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 534

##

21.1 STM32 闪存内存简介 . . . . . . . . . . . . . . . . . . . . . . . . . . . 534

21.2 HAL_FLASH 模块 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 537

21.2.1 闪存存储器解锁 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 538

21.2.2 闪存擦除 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 538

21.2.3 闪存存储器编程 . . . . . . . . . . . . . . . . . . . . . . . . . . 540

21.2.4 编程和擦除期间的闪存读取访问 . . . . . . . . . . . 541

21.3 选项字节 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 541

21.3.1 闪存存储器读取保护 . . . . . . . . . . . . . . . . . . . . . . . . . 543

21.4 可选的OTP和True-EEPROM存储器 . . . . . . . . . . . . . . . . . . . . . . . 545

21.5 闪存读取延迟与 ART™ 加速器 . . . . . . . . . . . . . . . . . . . . . . 547

21.5.1 TCM 存储器在 STM32F7/H7 微控制器中的作用 . . . . . . . . . . 549

21.5.1.1 如何通过 TCM 接口访问闪存存储器 . 555

21.5.1.2 使用 CubeMX 配置闪存存储器接口 . . . . 556

22。启动过程 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 558</pre></td>
</tr></tbody></table>

## PDF page 14 — Chapter 0: Front Matter

Focus: `numbers=1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 2, 2.1, 22.1, 22.2, 22.3, 23, 23.1, 23.2, 23.3, 23.4, 23.5, 3, 3.1, 3.2, 3.3, 4, 5, 558; negation=; conditions=; identifiers=malloc`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>CONTENTS

## 22.1 The Cortex-M Unified Memory Layout and the Booting Process . . . . . . . . . . . 558 22.1.1 Software Physical Remap . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 559 22.1.2 Vector Table Relocation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 560 22.1.3 Running the Firmware From SRAM Using the STM32CubeIDE . . . . . 562 22.2 Integrated STM32 Bootloader . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 563 22.2.1 Starting the STM32 Bootloader from the On-Board Firmware . . . . . . 566 22.2.2 The Booting Sequence in the STM32CubeIDE Tool-chain . . . . . . . . . 567 22.3 Developing a Custom Bootloader . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 568 22.3.1 Vector Table Relocation in STM32F0 Microcontrollers . . . . . . . . . . . 579 22.3.2 How to Use the flasher.py Tool . . . . . . . . . . . . . . . . . . . . . . . . 581

23. Running FreeRTOS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 584

## 23.1 Understanding the Concepts Underlying an RTOS . . . . . . . . . . . . . . . . . . . . 585 23.2 Configuring FreeRTOS and the CMSIS-RTOS v2 Wrapper . . . . . . . . . . . . . . . 591 23.2.1 The FreeRTOS Source Tree . . . . . . . . . . . . . . . . . . . . . . . . . . . . 592 23.2.1.1 How to Configure FreeRTOS Using CubeMX . . . . . . . . . 593 23.3 Thread Management . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 594 23.3.1 Thread States . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 597 23.3.2 Thread Priorities and Scheduling Policies . . . . . . . . . . . . . . . . . . . 598 23.3.3 Voluntary Release of the Control . . . . . . . . . . . . . . . . . . . . . . . . 602 23.3.4 The idle Thread . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 602 23.4 Memory Allocation and Management . . . . . . . . . . . . . . . . . . . . . . . . . . . 604 23.4.1 Dynamic Memory Allocation Model . . . . . . . . . . . . . . . . . . . . . . 604 23.4.1.1 heap_1.c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 605 23.4.1.2 heap_2.c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 606 23.4.1.3 heap_3.c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 606 23.4.1.4 heap_4.c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 607 23.4.1.5 heap_5.c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 607 23.4.1.6 FreeRTOS Heap Definition . . . . . . . . . . . . . . . . . . . . 608 23.4.2 Static Memory Allocation Model . . . . . . . . . . . . . . . . . . . . . . . . 608 23.4.2.1 idle Thread Allocation with Static Memory Allocation Model 609 23.4.3 FreeRTOS and the C stdlib . . . . . . . . . . . . . . . . . . . . . . . . . . . . 609 23.4.3.1 How to Configure newlib to Handle Concurrency with FreeRTOS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 610 23.4.3.2 How to Use malloc() and malloc()-dependant newlib Functions With FreeRTOS . . . . . . . . . . . . . . . . . . . . 613 23.4.3.3 STM32CubeMX Approach to Thread-Safety . . . . . . . . . 621 23.4.4 Memory Pools . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 622 23.4.5 Stack Overflow Detection . . . . . . . . . . . . . . . . . . . . . . . . . . . . 625 23.5 Synchronization Primitives . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 627 23.5.1 Message Queues . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 627 23.5.2 Semaphores . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 630 23.5.3 Event and Thread Flags . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 633</pre></td>
<td><pre>目录

## 22.1 Cortex-M 统一内存布局与启动过程 . . . . . . . . . . . 558 22.1.1 软件物理重映射 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 559 22.1.2 向量表重定位 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 560 22.1.3 使用 STM32CubeIDE 从 SRAM 运行固件 . . . . . 562 22.2 集成式 STM32 引导加载程序 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 563 22.2.1 从板载固件启动 STM32 引导加载程序 . . . . . . 566 22.2.2 STM32CubeIDE 工具链中的启动序列 . . . . . . . . . 567 22.3 开发自定义引导加载程序 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 568 22.3.1 STM32F0 微控制器中的向量表重定位 . . . . . . . . . . . 579 22.3.2 如何使用 flasher.py 工具 . . . . . . . . . . . . . . . . . . . . . . . . 581

23. 运行 FreeRTOS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 584

##

23.1 理解实时操作系统（RTOS）的底层概念 . . . . . . . . . . . . . . . . . . . . 585

23.2 配置 FreeRTOS 和 CMSIS-RTOS v2 封装 . . . . . . . . . . . . . . . 591

23.2.1 FreeRTOS 源代码树 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 592

23.2.1.1 如何使用 CubeMX 配置 FreeRTOS . . . . . . . . . 593

23.3 线程管理 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 594

23.3.1 线程状态 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 597

23.3.2 线程优先级与调度策略 . . . . . . . . . . . . . . . . . . . 598

23.3.3 主动释放控制权 . . . . . . . . . . . . . . . . . . . . . . . . 602

23.3.4 空闲线程 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 602

23.4 内存分配与管理 . . . . . . . . . . . . . . . . . . . . . . . . . . . 604

23.4.1 动态内存分配模型 . . . . . . . . . . . . . . . . . . . . . . 604 23.4.1.1 heap_1.c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 605 23.4.1.2 heap_2.c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 606 23.4.1.3 heap_3.c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 606 23.4.1.4 heap_4.c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 607 23.4.1.5 heap_5.c . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 607

23.4.1.6 FreeRTOS 堆定义 . . . . . . . . . . . . . . . . . . . . 608

23.4.2 静态内存分配模型 . . . . . . . . . . . . . . . . . . . . . . . . 608 23.4.2.1 在静态内存分配模型下空闲线程的分配 609

23.4.3 FreeRTOS 与 C 标准库 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 609

23.4.3.1 如何配置 newlib 以配合 FreeRTOS 处理并发 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 610

23.4.3.2 如何在 FreeRTOS 中使用 malloc() 和依赖 malloc() 的 newlib 函数 . . . . . . . . . . . . . . . . . . . . 613

23.4.3.3 STM32CubeMX 的线程安全方法 . . . . . . . . . 621

23.4.4 内存池 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 622

23.4.5 堆栈溢出检测 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 625

23.5 同步原语 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 627

23.5.1 消息队列 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 627

23.5.2 信号量 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 630

23.5.3 事件与线程标志 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 633</pre></td>
</tr></tbody></table>

## PDF page 15 — Chapter 0: Front Matter

Focus: `numbers=0, 1, 1.1, 1.2, 2, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 23.10, 23.6, 23.7, 23.8, 23.9, 24, 24.1, 24.2, 3, 3.1, 4, 637, 639; negation=; conditions=; identifiers=LR, configASSERT`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>CONTENTS

## 23.6 Resources Management and Mutual Exclusion . . . . . . . . . . . . . . . . . . . . . . 637 23.6.1 Mutexes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 637 23.6.1.1 The Priority Inversion Problem . . . . . . . . . . . . . . . . . 639 23.6.1.2 Recursive Mutexes . . . . . . . . . . . . . . . . . . . . . . . . . 640 23.6.2 Critical Sections . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 640 23.6.3 Interrupt Management With an RTOS . . . . . . . . . . . . . . . . . . . . . 641 23.6.3.1 FreeRTOS API and Interrupt Priorities . . . . . . . . . . . . . 642 23.7 Software Timers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 643 23.7.1 How FreeRTOS Manages Timers . . . . . . . . . . . . . . . . . . . . . . . . 645 23.8 A Case Study: Low-Power Management With an RTOS . . . . . . . . . . . . . . . . . 645 23.8.1 The idle Thread Hook . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 646 23.8.2 The Tickless Mode in FreeRTOS . . . . . . . . . . . . . . . . . . . . . . . . 647 23.8.2.1 A Schema for the tickless Mode . . . . . . . . . . . . . . . . . 649 23.8.2.2 A Custom tickless Mode Policy . . . . . . . . . . . . . . . . . 652 23.9 Debugging Features . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 660 23.9.1 configASSERT() Macro . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 660 23.9.2 Run-Time Statistics and Thread State Information . . . . . . . . . . . . . 661 23.9.3 FreeRTOS Debugging in STM32CubeIDE . . . . . . . . . . . . . . . . . . . 665 23.9.4 FreeRTOS Kernel-Aware Debugging in STM32CubeIDE . . . . . . . . . . 668 23.10 Alternatives to FreeRTOS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 670 23.10.1 AzureRTOS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 670 23.10.2 ChibiOS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 670 23.10.3 Contiki OS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 671 23.10.4 OpenRTOS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 671

24. Advanced Debugging Techniques . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 673

## 24.1 Understanding Cortex-M Fault-Related Exceptions . . . . . . . . . . . . . . . . . . . 673 24.1.1 The Cortex-M Exception Entrance Sequence and the ARM Calling Convention . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 675 24.1.1.1 How to Interpret the Content of the LR Register on Exception Entrance . . . . . . . . . . . . . . . . . . . . . . . . . . . . 680 24.1.2 Fault Exceptions and Faults Analysis . . . . . . . . . . . . . . . . . . . . . 681 24.1.2.1 Memory Management Exception . . . . . . . . . . . . . . . . 682 24.1.2.2 Bus Fault Exception . . . . . . . . . . . . . . . . . . . . . . . . 682 24.1.2.3 Usage Fault Exception . . . . . . . . . . . . . . . . . . . . . . . 683 24.1.2.4 Hard Fault Exception . . . . . . . . . . . . . . . . . . . . . . . 684 24.1.2.5 Secure Fault Exception . . . . . . . . . . . . . . . . . . . . . . . 685 24.1.2.6 Enabling Optional Fault Handlers . . . . . . . . . . . . . . . . 685 24.1.2.7 Fault Analysis in Cortex-M0/0+ Based Processors . . . . . . 686 24.2 STM32CubeIDE Advanced Debugging Features . . . . . . . . . . . . . . . . . . . . . 686 24.2.1 Expressions and Live Expressions . . . . . . . . . . . . . . . . . . . . . . . 686 24.2.1.1 Memory Monitors . . . . . . . . . . . . . . . . . . . . . . . . . 688 24.2.2 Watchpoints . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 689</pre></td>
<td><pre>目录

## 23.6 资源管理与互斥 . . . . . . . . . . . . . . . . . . . . . . 637 23.6.1 互斥锁 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 637 23.6.1.1 优先级反转问题 . . . . . . . . . . . . . . . . . 639 23.6.1.2 递归互斥锁 . . . . . . . . . . . . . . . . . . . . . . . . . 640 23.6.2 临界区 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 640 23.6.3 使用实时操作系统的中断管理 . . . . . . . . . . . . . . . . . . . . . 641 23.6.3.1 FreeRTOS API 与中断优先级 . . . . . . . . . . . . . 642 23.7 软件定时器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 643 23.7.1 FreeRTOS 如何管理定时器 . . . . . . . . . . . . . . . . . . . . . . . . 645 23.8 案例研究：使用实时操作系统进行低功耗管理 . . . . . . . . . . . . . . . . . 645 23.8.1 空闲线程钩子 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 646 23.8.2 FreeRTOS 中的无滴答模式 . . . . . . . . . . . . . . . . . . . . . . . . 647 23.8.2.1 无滴答模式的示意图 . . . . . . . . . . . . . . . . . 649 23.8.2.2 自定义无滴答模式策略 . . . . . . . . . . . . . . . . . 652 23.9 调试功能 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 660 23.9.1 configASSERT() 宏 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 660 23.9.2 运行时统计信息与线程状态信息 . . . . . . . . . . . . . 661 23.9.3 在 STM32CubeIDE 中调试 FreeRTOS . . . . . . . . . . . . . . . . . . . 665 23.9.4 在 STM32CubeIDE 中进行 FreeRTOS 内核感知调试 . . . . . . . . . . 668 23.10 FreeRTOS 的替代方案 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 670 23.10.1 AzureRTOS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 670 23.10.2 ChibiOS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 670 23.10.3 Contiki OS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 671 23.10.4 OpenRTOS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 671

24. 高级调试技术 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 673

## 24.1 理解 Cortex-M 故障相关异常 . . . . . . . . . . . . . . . . . . . 673 24.1.1 Cortex-M 异常入口序列与 ARM 调用约定 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 675 24.1.1.1 如何在异常入口时解读 LR 寄存器的内容 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 680 24.1.2 故障异常与故障分析 . . . . . . . . . . . . . . . . . . . . . 681 24.1.2.1 内存管理异常 . . . . . . . . . . . . . . . . 682 24.1.2.2 总线故障异常 . . . . . . . . . . . . . . . . . . . . . . . . 682 24.1.2.3 使用故障异常 . . . . . . . . . . . . . . . . . . . . . . . 683 24.1.2.4 硬故障异常 . . . . . . . . . . . . . . . . . . . . . . . 684 24.1.2.5 安全故障异常 . . . . . . . . . . . . . . . . . . . . . . . 685 24.1.2.6 启用可选故障处理程序 . . . . . . . . . . . . . . . . 685 24.1.2.7 基于 Cortex-M0/0+ 处理器的故障分析 . . . . . . 686 24.2 STM32CubeIDE 高级调试功能 . . . . . . . . . . . . . . . . . . . . . 686 24.2.1 表达式与实时表达式 . . . . . . . . . . . . . . . . . . . . . . . 686 24.2.1.1 内存监视器 . . . . . . . . . . . . . . . . . . . . . . . . . 688 24.2.2 观察点 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 689</pre></td>
</tr></tbody></table>

## PDF page 16 — Chapter 0: Front Matter

Focus: `numbers=1, 1.1, 1.2, 2, 2.1, 2.2, 2.3, 2.4, 24.2, 24.3, 24.4, 24.5, 24.6, 24.7, 25, 25.1, 26, 26.1, 26.2, 3, 3.1, 3.2, 3.3, 3.4, 3.5; negation=Without; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>CONTENTS

### 24.2.3 Instruction Stepping Mode . . . . . . . . . . . . . . . . . . . . . . . . . . . . 690 24.2.4 SFRs View . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 690 24.2.5 Fault Analyzer . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 691 24.2.5.1 Tracing Fault-Related Registers Without the IDE Support . 693 24.2.6 Build Analyzer . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 696 24.2.7 Static Stack Analyzer . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 697 24.3 Serial Wire Viewer Tracing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 698 24.3.1 Enabling SWV Debugging . . . . . . . . . . . . . . . . . . . . . . . . . . . . 700 24.3.2 Configuring SWV . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 701 24.3.3 SWV Views . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 703 24.3.3.1 SWV Trace Log . . . . . . . . . . . . . . . . . . . . . . . . . . . 704 24.3.3.2 SWV Exception Trace Log . . . . . . . . . . . . . . . . . . . . . 704 24.3.3.3 SWV Data Trace . . . . . . . . . . . . . . . . . . . . . . . . . . 705 24.3.3.4 SWV Data Trace Timeline Graph . . . . . . . . . . . . . . . . 706 24.3.3.5 SWV ITM Data Console . . . . . . . . . . . . . . . . . . . . . . 707 24.3.3.6 SWV Statistical Profiling . . . . . . . . . . . . . . . . . . . . . 708 24.4 Debugging Aids from the CubeHAL . . . . . . . . . . . . . . . . . . . . . . . . . . . . 709 24.5 External Debuggers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 709 24.6 Debugging two Nucleo Boards Simultaneously . . . . . . . . . . . . . . . . . . . . . . 711 24.7 ARM Semihosting . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 712 24.7.1 Enable Semihosting on a Project . . . . . . . . . . . . . . . . . . . . . . . . 713 24.7.2 Semihosting Drawbacks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 715 24.7.3 Understanding How Semihosting Works . . . . . . . . . . . . . . . . . . . 716

25. FAT Filesystem . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 720

## 25.1 Introduction to FatFs Library . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 720 25.1.1 Adding FatFs Library in Your Projects . . . . . . . . . . . . . . . . . . . . . 723 25.1.1.1 The Generic Disk Interface API . . . . . . . . . . . . . . . . . 724 25.1.1.2 The Implementation of a Driver to Access SD Cards in SPI Mode . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 725 25.1.2 Relevant FatFs Structures and Functions . . . . . . . . . . . . . . . . . . . 725 25.1.2.1 Mounting a Filesystem . . . . . . . . . . . . . . . . . . . . . . . 725 25.1.2.2 Opening a File . . . . . . . . . . . . . . . . . . . . . . . . . . . . 726 25.1.2.3 Reading From/Writing into a File . . . . . . . . . . . . . . . . 727 25.1.2.4 Creating and Opening a Directory . . . . . . . . . . . . . . . 728 25.1.3 How to Configure the FatFs Library . . . . . . . . . . . . . . . . . . . . . . 731

26. Develop IoT Applications . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 733

## 26.1 Solutions Offered by STM to Develop IoT Applications . . . . . . . . . . . . . . . . . 734 26.2 The W5500 Ethernet Controller . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 736 26.2.1 How to Use the W5500 Shield and the ioLibrary_Driver Module . . . . 740 26.2.1.1 Configuring the SPI Interface . . . . . . . . . . . . . . . . . . 742 26.2.1.2 Configuring the Socket Buffers and the Network Interface . 743</pre></td>
<td><pre>目录

###

24.2.3 指令单步模式 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 690

24.2.4 特殊功能寄存器视图 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 690

24.2.5 故障分析器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 691

24.2.5.1 在没有 IDE 支持的情况下追踪故障相关寄存器。 693

24.2.6 构建分析器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 696

24.2.7 静态堆栈分析器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 697

24.3 串行线查看器跟踪 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 698

24.3.1 启用 SWV 调试 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 700

24.3.2 配置 SWV . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 701

24.3.3 SWV 视图 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 703

24.3.3.1 SWV 跟踪日志 . . . . . . . . . . . . . . . . . . . . . . . . . . . 704

24.3.3.2 SWV 异常跟踪日志 . . . . . . . . . . . . . . . . . . . . . 704

24.3.3.3 SWV 数据跟踪 . . . . . . . . . . . . . . . . . . . . . . . . . . 705

24.3.3.4 SWV 数据跟踪时间线图表 . . . . . . . . . . . . . . . . 706

24.3.3.5 SWV ITM 数据控制台 . . . . . . . . . . . . . . . . . . . . . . 707

24.3.3.6 SWV 统计剖析 . . . . . . . . . . . . . . . . . . . . . 708

24.4 CubeHAL 提供的调试辅助功能 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 709

24.5 外部调试器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 709

24.6 同时调试两块 Nucleo 开发板 . . . . . . . . . . . . . . . . . . . . . . 711

24.7 ARM 半主机 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 712

24.7.1 在项目中启用半主机 . . . . . . . . . . . . . . . . . . . . . . . . 713

24.7.2 半托管的缺点 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 715

24.7.3 了解半托管的工作原理 . . . . . . . . . . . . . . . . . . . 716

25。FAT 文件系统 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 720

##

25.1 FatFs 库简介 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 720

25.1.1 在项目中添加 FatFs 库 . . . . . . . . . . . . . . . . . . . . . 723

25.1.1.1 通用磁盘接口 API . . . . . . . . . . . . . . . . . 724

25.1.1.2 以 SPI 模式访问 SD 卡的驱动程序实现 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 725

25.1.2 相关的 FatFs 结构和函数 . . . . . . . . . . . . . . . . . . . 725

25.1.2.1 挂载文件系统 . . . . . . . . . . . . . . . . . . . . . . . 725

25.1.2.2 打开文件 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 726

25.1.2.3 将 From/Writing 读取到文件中 . . . . . . . . . . . . . . . . 727

25.1.2.4 创建和打开目录 . . . . . . . . . . . . . . . 728

25.1.3 如何配置 FatFs 库 . . . . . . . . . . . . . . . . . . . . . . 731

26。开发物联网应用 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 733

## 26.1 ST 提供的用于开发物联网应用的解决方案 . . . . . . . . . . . . . . . . . 734 26.2 W5500 以太网控制器 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 736 26.2.1 如何使用 W5500 扩展板和 ioLibrary_Driver 模块 . . . . 740 26.2.1.1 配置 SPI 接口 . . . . . . . . . . . . . . . . . . 742 26.2.1.2 配置套接字缓冲区和网络接口 . 743</pre></td>
</tr></tbody></table>

## PDF page 17 — Chapter 0: Front Matter

Focus: `numbers=1, 1.1, 1.2, 1.3, 2, 2.0, 2.1, 2.2, 26.2, 27, 27.1, 27.2, 27.3, 27.4, 3, 3.1, 3.2, 4, 4.1, 4.2, 4.3, 4.4, 5, 745, 746; negation=; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>CONTENTS

### 26.2.2 Socket APIs . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 745 26.2.2.1 Handling Sockets in TCP Mode . . . . . . . . . . . . . . . . . 746 26.2.2.2 Handling Sockets in UDP Mode . . . . . . . . . . . . . . . . . 747 26.2.3 I/O Retargeting to a TCP/IP Socket . . . . . . . . . . . . . . . . . . . . . . . 748 26.2.4 Building up an HTTP Server . . . . . . . . . . . . . . . . . . . . . . . . . . . 749 26.2.4.1 A Web-Based Oscilloscope . . . . . . . . . . . . . . . . . . . . 752

27. Universal Serial Bus . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 765

## 27.1 USB 2.0 Specification Overview . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 766 27.1.1 The “Before-To-Die” Guide to USB . . . . . . . . . . . . . . . . . . . . . . . 766 27.1.2 USB Physical Architecture Overview . . . . . . . . . . . . . . . . . . . . . 769 27.1.3 USB Logical Architecture Overview . . . . . . . . . . . . . . . . . . . . . . 772 27.1.3.1 Device States . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 772 27.1.3.2 Communication Endpoints . . . . . . . . . . . . . . . . . . . . 774 27.1.4 USB 2.0 Communication Protocol Overview . . . . . . . . . . . . . . . . . 777 27.1.4.1 Packet Types . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 778 27.1.4.2 Transaction Types . . . . . . . . . . . . . . . . . . . . . . . . . 780 27.1.4.2.1 Control Transactions . . . . . . . . . . . . . . . . . . . . . . . . . . 780 27.1.4.2.2 IN/OUT Transactions . . . . . . . . . . . . . . . . . . . . . . . . . 784

#### 27.1.4.3 Device and Interface Descriptors . . . . . . . . . . . . . . . . 785 27.1.4.3.1 Device Descriptors . . . . . . . . . . . . . . . . . . . . . . . . . . . 786 27.1.4.3.2 Configuration Descriptors . . . . . . . . . . . . . . . . . . . . . . . 788 27.1.4.3.3 Interface Descriptors . . . . . . . . . . . . . . . . . . . . . . . . . . 789 27.1.4.3.4 Endpoint Descriptors . . . . . . . . . . . . . . . . . . . . . . . . . . 789 27.1.4.3.5 String Descriptors . . . . . . . . . . . . . . . . . . . . . . . . . . . . 791

#### 27.1.4.4 USB Classes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 791 27.2 STM32 USB Device Library . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 793 27.2.1 Understanding Generated Code . . . . . . . . . . . . . . . . . . . . . . . . . 794 27.2.2 USB Initialization Sequence . . . . . . . . . . . . . . . . . . . . . . . . . . . 798 27.2.3 USB Enumeration Sequence . . . . . . . . . . . . . . . . . . . . . . . . . . . 801 27.2.4 The USB CDC Class . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 804 27.2.4.1 USB CDC Descriptors . . . . . . . . . . . . . . . . . . . . . . . 805 27.2.4.2 USB CDC Class Initialization . . . . . . . . . . . . . . . . . . . 809 27.2.4.3 USB CDC Class Operations . . . . . . . . . . . . . . . . . . . . 810 27.3 Building Custom USB Devices . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 815 27.3.1 The USB HID Class . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 817 27.3.1.1 USB HID Descriptors . . . . . . . . . . . . . . . . . . . . . . . 818 27.3.1.2 Overview of the Report Descriptor . . . . . . . . . . . . . . . 820 27.3.1.3 USB HID Class-Specific Requests . . . . . . . . . . . . . . . . 824 27.3.2 Building a Vendor-Specific USB HID Device . . . . . . . . . . . . . . . . . 825 27.4 Debugging USB Devices . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 837 27.4.1 Software Sniffers and Analyzers . . . . . . . . . . . . . . . . . . . . . . . . 837 27.4.2 USB Hardware Analyzers . . . . . . . . . . . . . . . . . . . . . . . . . . . . 837</pre></td>
<td><pre>目录

### 26.2.2 Socket API . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 745 26.2.2.1 在 TCP 模式下处理套接字 . . . . . . . . . . . . . . . . . 746 26.2.2.2 在 UDP 模式下处理套接字 . . . . . . . . . . . . . . . . . 747 26.2.3 I/O 重定向到 TCP/IP 套接字 . . . . . . . . . . . . . . . . . . . . . . . 748 26.2.4 构建 HTTP 服务器 . . . . . . . . . . . . . . . . . . . . . . . . . . . 749 26.2.4.1 基于 Web 的示波器 . . . . . . . . . . . . . . . . . . . . 752

27。通用串行总线 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 765

##

27.1 通用串行总线

2.0 规范概述 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 766

27.1.1 USB“Before-To-Die”指南 . . . . . . . . . . . . . . . . . . . . . . . 766

27.1.2 USB 物理架构概述 . . . . . . . . . . . . . . . . . . . . . 769

27.1.3 USB 逻辑架构概述 . . . . . . . . . . . . . . . . . . . . . . 772

27.1.3.1 设备状态 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 772

27.1.3.2 通信端点 . . . . . . . . . . . . . . . . . . . . 774

27.1.4 USB

2.0 通信协议概述 . . . . . . . . . . . . . . . . . 777

27.1.4.1 数据包类型 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 778

27.1.4.2 事务类型 . . . . . . . . . . . . . . . . . . . . . . . . . 780

27.1.4.2.1 控制事务 . . . . . . . . . . . . . . . . . . . . . . . . . . 780

27.1.4.2.2 IN/OUT 事务 . . . . . . . . . . . . . . . . . . . . . . . . . 784

#### 27.1.4.3 设备和接口描述符 . . . . . . . . . . . . . . . . 785 27.1.4.3.1 设备描述符 . . . . . . . . . . . . . . . . . . . . . . . . . . . 786 27.1.4.3.2 配置描述符 . . . . . . . . . . . . . . . . . . . . . . . 788 27.1.4.3.3 接口描述符 . . . . . . . . . . . . . . . . . . . . . . . . . . 789 27.1.4.3.4 端点描述符 . . . . . . . . . . . . . . . . . . . . . . . . . . 789 27.1.4.3.5 字符串描述符 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 791

####

27.1.4.4 USB 类 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 791

27.2 STM32 USB 设备库 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 793

27.2.1 理解生成的代码 . . . . . . . . . . . . . . . . . . . . . . . . . 794

27.2.2 USB 初始化序列 . . . . . . . . . . . . . . . . . . . . . . . . . . . 798

27.2.3 USB 枚举序列 . . . . . . . . . . . . . . . . . . . . . . . . . . . 801

27.2.4 USB CDC 类 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 804

27.2.4.1 USB CDC 描述符 . . . . . . . . . . . . . . . . . . . . . . . 805

27.2.4.2 USB CDC 类初始化 . . . . . . . . . . . . . . . . . . . 809

27.2.4.3 USB CDC 类操作 . . . . . . . . . . . . . . . . . . . . 810

27.3 构建自定义 USB 设备 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 815

27.3.1 USB HID 类 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 817

27.3.1.1 USB HID 描述符 . . . . . . . . . . . . . . . . . . . . . . . 818

27.3.1.2 报告描述符概述 . . . . . . . . . . . . . . . 820

27.3.1.3 USB HID 类特定请求 . . . . . . . . . . . . . . . . 824

27.3.2 构建厂商特定的 USB HID 设备 . . . . . . . . . . . . . . . . . 825

27.4 调试 USB 设备 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 837

27.4.1 软件嗅探器与分析器 . . . . . . . . . . . . . . . . . . . . . . . . 837

27.4.2 USB 硬件分析仪 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 837</pre></td>
</tr></tbody></table>

## PDF page 18 — Chapter 0: Front Matter

Focus: `numbers=1, 10, 11, 2, 27.5, 27.6, 28, 28.1, 28.2, 3, 4, 5, 6, 7, 8, 838, 839, 842, 843, 844, 845, 847, 848, 850, 851; negation=Not; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>CONTENTS

## 27.5 Optimizing the STM32 USB Device Library . . . . . . . . . . . . . . . . . . . . . . . . 838 27.6 Going to the Market . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 839

28. Getting Started with a New Design . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 842 28.1 Hardware Design . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 842 28.1.1 PCB Layer Stack-Up . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 843 28.1.2 MCU Package . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 844 28.1.3 Decoupling of Power-Supply Pins . . . . . . . . . . . . . . . . . . . . . . . 845 28.1.4 Clocks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 847 28.1.5 Filtering of RESET Pin . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 848 28.1.6 Debug Port . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 848 28.1.7 Boot Mode . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 850 28.1.8 Pay attention to “pin-to-pin” Compatibility… . . . . . . . . . . . . . . . . 851 28.1.9 …And to Selecting the Right Peripherals . . . . . . . . . . . . . . . . . . . 852 28.1.10 The Role of CubeMX During the Board Design Stage . . . . . . . . . . . 852 28.1.11 Board Layout Strategies . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 856 28.2 Software Design . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 857 28.2.1 Generating the binary image for production . . . . . . . . . . . . . . . . . 857

# Appendix . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .860

A. Miscellaneous HAL functions and STM32 features . . . . . . . . . . . . . . . . . . . . . . . . 861

Force MCU reset from the firmware . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 861 STM32 96-bit Unique CPU ID . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 861

B. Troubleshooting Guide . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 863

STM32CubeIDE Issues . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 863

Debugging Continuously Breaks at Every Instruction During a Debug Session . . 863 The Step-by-Step Debugging is Really Slow . . . . . . . . . . . . . . . . . . . . . . . . 863 The Firmware Works Only Under a Debug Session . . . . . . . . . . . . . . . . . . . 864 STM32 Related Issues . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 864

The Microcontroller Does Not Boot Correctly . . . . . . . . . . . . . . . . . . . . . . . 864 It is Not Possible to Flash or to Debug the MCU . . . . . . . . . . . . . . . . . . . . . 866

C. Nucleo pin-out . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 868

Nucleo-G474RE . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 869

Arduino compatible headers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 869 Morpho headers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 869 Nucleo-F446RE . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 870

Arduino compatible headers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 870 Morpho headers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 870 Nucleo-F401RE . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 871

Arduino compatible headers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 871</pre></td>
<td><pre>目录

## 27.5 优化 STM32 USB 设备库 . . . . . . . . . . . . . . . . . . . . . . . . 838 27.6 走向市场 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 839

28.  开始新设计 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 842 28.1 硬件设计 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 842 28.1.1 PCB 层叠结构 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 843 28.1.2 MCU 封装 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 844 28.1.3 电源引脚去耦 . . . . . . . . . . . . . . . . . . . . . . . 845 28.1.4 时钟 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 847 28.1.5 RESET 引脚滤波 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 848 28.1.6 调试端口 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 848 28.1.7 启动模式 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 850 28.1.8 注意“引脚对引脚”兼容性…… . . . . . . . . . . . . . . . . 851 28.1.9 ……以及选择合适的外设 . . . . . . . . . . . . . . . . . . . 852 28.1.10 CubeMX 在板级设计阶段的作用 . . . . . . . . . . . 852 28.1.11 板级布局策略 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 856 28.2 软件设计 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 857 28.2.1 生成用于生产的二进制镜像 . . . . . . . . . . . . . . . . . 857

# 附录 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .860

A. 其他 HAL 函数和 STM32 特性 . . . . . . . . . . . . . . . . . . . . . . . . 861

从固件中强制 MCU 复位 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 861 STM32 96位唯一 CPU ID . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 861

B. 故障排除指南 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 863

STM32CubeIDE 问题 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 863

调试过程中每条指令都持续中断 . . 863 单步调试速度非常慢 . . . . . . . . . . . . . . . . . . . . . . . . 863 固件仅在调试会话期间运行 . . . . . . . . . . . . . . . . . . . 864 STM32 相关问题 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 864

微控制器无法正确启动 . . . . . . . . . . . . . . . . . . . . . . . 864 无法对 MCU 进行烧录或调试 . . . . . . . . . . . . . . . . . . . . . 866

C. Nucleo 引脚分配 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 868

Nucleo-G474RE . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 869

Arduino 兼容排针 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 869 Morpho 排针 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 869 Nucleo-F446RE . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 870

Arduino 兼容排针 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 870 Morpho 排针 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 870 Nucleo-F401RE . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 871

Arduino 兼容排针 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 871</pre></td>
</tr></tbody></table>

## PDF page 19 — Chapter 0: Front Matter

Focus: `numbers=1, 10, 11, 12, 2, 22, 23, 24, 25, 26, 27, 28, 3, 4, 5, 6, 7, 8, 871, 872, 873, 874, 875, 876, 877; negation=; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>CONTENTS

Morpho headers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 871 Nucleo-F303RE . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 872

Arduino compatible headers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 872 Morpho headers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 872 Nucleo-F103RB . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 873

Arduino compatible headers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 873 Morpho headers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 873 Nucleo-F072RB . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 874

Arduino compatible headers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 874 Morpho headers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 874 Nucleo-L476RG . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 875

Arduino compatible headers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 875 Morpho headers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 875 Nucleo-L152RE . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 876

Arduino compatible headers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 876 Morpho headers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 876 Nucleo-L073R8 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 877

Arduino compatible headers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 877 Morpho headers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 877

D. Differences with the 1st edition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 878

Chapter 1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 878 Chapter 2 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 878 Chapter 3 and 4 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 878 Chapter 5 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 878 Chapter 6 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 879 Chapter 7 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 879 Chapter 8 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 879 Chapter 9 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 879 Chapter 10 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 879 Chapter 11 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 879 Chapter 12-22 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 880 Chapter 23 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 880 Chapter 24 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 880 Chapter 25-26 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 880 Chapter 27 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 880 Chapter 28 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 880</pre></td>
<td><pre>目录

Morpho 标头 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 871 Nucleo-F303RE . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 872

Arduino 兼容引脚 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 872 Morpho 引脚 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 872 Nucleo-F103RB . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 873

Arduino 兼容引脚 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 873 Morpho 引脚 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 873 Nucleo-F072RB . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 874

Arduino 兼容引脚 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 874 Morpho 引脚 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 874 Nucleo-L476RG . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 875

Arduino 兼容引脚 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 875 Morpho 引脚 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 875 Nucleo-L152RE . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 876

Arduino 兼容引脚 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 876 Morpho 引脚 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 876 Nucleo-L073R8 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 877

Arduino 兼容引脚 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 877 Morpho 引脚 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 877

D. 与 1st 版本的差异 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 878

第 1 章 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 878 第 2 章 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 878 第 3 章和 4 章 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 878 第 5 章 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 878 第 6 章 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 879 第 7 章 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 879 第 8 章 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 879 第 9 章 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

. . . 879 第 10 章 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 879 第 11 章 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 879 第 12-22 章 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 880 第 23 章 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 880 第 24 章 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 880 第 25-26 章 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 880 第 27 章 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 880 第 28 章 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

. . . . 880</pre></td>
</tr></tbody></table>

## PDF page 20 — Chapter 0: Front Matter

Focus: `numbers=1200, 2015, 2021, 5, 500, 7, 900; negation=not, unless; conditions=unless, when; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre># Preface

It was the summer of 2015 when I began to consider the hypothesis of grouping a series of posts on my personal blog to give shape to a more structured guide about the use of STM32 microcontrollers. At that time, it was not trivial to setup a complete tool-chain for the STM32 portfolio, unless you could afford a license for the ARM Keil. Moreover, STM was migrating from the historical Standard Peripheral Library (SPL) to the new CubeHAL SDK, and it was not clear the path to follow to start learning this very interesting product lineup.

I so started writing the very first chapters of this book, showing how-to setup a complete and free Eclipse tool-chain based on the GNU MCU Eclipse plug-ins by Liviu Ionescu (now called Eclipse Embedded CDT and officially supported by the Eclipse Foundation), and I decided to use the LeanPub platform, which allowed me to publish an in-progress book that I could update as soon as I added a new chapter. From the very first release of the book, many people adopted the text and helped me a lot in shaping the book structure and its contents. It took me two years to complete the first edition and, trust me, it was a very hard work especially because things changed day-by-day. During the years, the book has been adopted by several Universities around the world as official text in Embedded System classes. A lot of people contacted me to provide feedback, some asking for help with the text and some others with the development of their board, some asking for a revision of the text and some others for a revision of the examples, some criticizing the whole book and some other letting me know that they thank me every time they go to sleep.

Seven years later things have changed. A lot. STM pushed hard the development of both the hardware and software ecosystem. The first release of the book was about nine STM32 families, ranging on about 500 P/N. Now there are seventeen families in the STM32 portfolio, spreading over more than 1200 P/N. But the huge improvement was on the software part. STM decided to fix the main issue with the STM32 portfolio: the lack of an official tool-chain. STM acquired Atollic and its TrueStudio IDE, and launched the STM32CubeIDE that, together with the whole STM32Cube initiative, represents a quantum leap for the development of STM32-based devices.

This required me to make a deep revision of the text. I so started working on this second edition in the spring of 2021 and it took to me about one year to update the text and to add new contents that lacked in the first edition. This is a lot of time but things changed a lot even for me in these years. A totally different job, full of too many responsibilities, and a daughter came in the middle, and now my free time ranges from the 5:00am to 7:00am, and you can figure out how hard is to work to a book with 900 pages in just two hours a day.

Even in the second edition, the book is divided in three parts: an introductory part showing how to setup the STM32CubeIDE and how to work with it; a part that introduces the basics of STM32 programming and the main aspects of the official HAL (Hardware Abstraction Layer); a more advanced section covering aspects such as the use of a Real Time Operating Systems, the boot sequence and the memory layout of an STM32 application, advanced peripherals like the USB.</pre></td>
<td><pre># 前言

2015 年夏天，我开始考虑将个人博客上的一系列文章整理成册，以形成一份关于 STM32 微控制器（microcontroller）使用的更结构化的指南。当时，除非你能负担得起 ARM Keil 的许可证，否则为 STM32 产品系列搭建一套完整的工具链（toolchain）并非易事。此外，ST 公司正从历史悠久的标准外设库（Standard Peripheral Library, SPL）迁移到新的 CubeHAL SDK，对于如何开始学习这个非常有趣的产品系列，路径并不清晰。

于是，我开始撰写本书的最初章节，展示如何基于 Liviu Ionescu 开发的 GNU MCU Eclipse 插件（现称为 Eclipse Embedded CDT，并得到 Eclipse 基金会的官方支持）搭建一套完整且免费的 Eclipse 工具链。我决定使用 LeanPub 平台，该平台允许我发布一本正在编写中的书籍，并在我添加新章节时随时更新。从本书的首次发布起，许多人采用了该文本，并在塑造书籍结构和内容方面给予了我很大帮助。我花了两年时间完成第一版，相信我，这是一项非常艰巨的工作，尤其是因为情况每天都在变化。多年来，本书已被全球多所大学采用，作为嵌入式系统课程的官方教材。许多人联系我提供反馈，有些人请求帮助理解文本，有些人询问他们开发板的开发问题，有些人要求修订文本，有些人要求修订示例，有些人批评整本书，还有些人告诉我，他们每次睡觉前都会感谢我。

七年后，情况发生了巨大变化。STM 大力推动了硬件和软件生态系统的开发。本书的首次发布涵盖了九个 STM32 系列，涉及约 500 个料号（P/N）。如今，STM32 产品系列中有十七个系列，涵盖超过 1200 个料号。但巨大的改进在于软件部分。STM 决定解决 STM32 产品系列的主要问题：缺乏官方工具链。STM 收购了 Atollic 及其 TrueStudio IDE，并推出了 STM32CubeIDE。STM32CubeIDE 连同整个 STM32Cube 计划，代表了基于 STM32 设备开发的一次量子飞跃。

这要求我对文本进行深度修订。于是，我在 2021 年春天开始着手编写第二版，并花了一年左右的时间更新文本并添加第一版中缺失的新内容。这是一段很长的时间，但在这几年里，即使对我个人而言，情况也发生了巨大变化。我换了一份完全不同的工作，承担了许多责任，中间还迎来了一个女儿，现在我空闲的时间只有早上 5:00 到 7:00，你可以想象，每天只有两个小时来编写一本 900 页的书是多么艰难。

即使在第二版中，本书仍分为三个部分：一个介绍部分，展示如何设置 STM32CubeIDE 以及如何在其上工作；一个部分介绍 STM32 编程的基础知识和官方硬件抽象层（Hardware Abstraction Layer, HAL）的主要方面；一个更高级的部分，涵盖诸如实时操作系统（Real Time Operating System）的使用、STM32 应用的启动序列和内存布局、以及 USB 等高级外设等方面。</pre></td>
</tr></tbody></table>

## PDF page 36 — Chapter 1: Introduction to STM32 MCU Portfolio

Focus: `numbers=0036, 01, 1, 1.3, 2, 3, 36, 4, 5, 6, 7, 8; negation=disabled; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>### Compiler will generate the following ARM assembly code²:

```text
1
movs
r3, #3
;move &quot;3&quot; in register r3
2
strb
r3, [r7, #7] ;store the content of r3 in &quot;a&quot;
3
movs
r3, #2
;move &quot;2&quot; in register r3
4
strb
r3, [r7, #6] ;store the content of r3 in &quot;b&quot;
5
ldrb
r2, [r7, #7] ;load the content of &quot;a&quot; in r2
6
ldrb
r3, [r7, #6] ;load the content of &quot;b&quot; in r3
7
smulbb
r3, r2, r3
;multiply &quot;a&quot; with &quot;b&quot; and store result in r3
8
strb
r3, [r7, #5] ;store the result in &quot;c&quot;
```

As we can see, all the operations always involve a register. Instructions at lines 1-2 move the number 3 into the register r3 and then store its content (that is, the number 3) inside the memory location given by the register r7 plus an offset of 7 memory locations - that is the place where a variable is stored. The same happens for the variable b at lines 3-4. Then lines 5-7 load the content of variables a and b and perform the multiplication. Finally, line 8 stores the result in the memory location of variable c.

![Image from PDF page 36](../images/page-0036-image-01.jpeg)

Figure 1.3: Cortex-M fixed memory address space

²That assembly code was generated compiling in thumb mode with any optimization disabled, invoking GCC in the following way: $ arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -fverbose-asm -save-temps -O0 -g -c file.c</pre></td>
<td><pre>### 编译器将生成以下 ARM 汇编代码²：

```text
1
movs
r3, #3
;move &quot;3&quot; in register r3
2
strb
r3, [r7, #7] ;store the content of r3 in &quot;a&quot;
3
movs
r3, #2
;move &quot;2&quot; in register r3
4
strb
r3, [r7, #6] ;store the content of r3 in &quot;b&quot;
5
ldrb
r2, [r7, #7] ;load the content of &quot;a&quot; in r2
6
ldrb
r3, [r7, #6] ;load the content of &quot;b&quot; in r3
7
smulbb
r3, r2, r3
;multiply &quot;a&quot; with &quot;b&quot; and store result in r3
8
strb
r3, [r7, #5] ;store the result in &quot;c&quot;
```

我们可以看到，所有操作始终涉及一个寄存器。第 1-2 行的指令将数字 3 移入寄存器 r3，然后将其内容（即数字 3）存储到由寄存器 r7 加上 7 个内存位置偏移量所给出的内存位置中——这就是变量存储的位置。第 3-4 行对变量 b 执行相同的操作。然后，第 5-7 行加载变量 a 和 b 的内容并执行乘法运算。最后，第 8 行将结果存储在变量 c 的内存位置中。

![Image from PDF page 36](../images/page-0036-image-01.jpeg)

图 1.3：Cortex-M 固定内存地址空间

²该汇编代码是在 thumb 模式下编译生成的，且未启用任何优化，调用 GCC 的方式如下：$ arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -fverbose-asm -save-temps -O0 -g -c file.c</pre></td>
</tr></tbody></table>

## PDF page 37 — Chapter 1: Introduction to STM32 MCU Portfolio

Focus: `numbers=0000, 0037, 01, 0x0000, 0x00000000, 0x0800, 1.1, 1.2, 1.3, 1.4, 22, 32, 37, 7; negation=not; conditions=if; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>#### 1.1.1.2 Memory Map

ARM defines a standardized memory address space common to all Cortex-M cores, which ensures code portability among different silicon manufacturers. The address space is 4GB wide, and it is organized in several sub-regions with different logical functionalities. Figure 1.3 shows the memory layout of a Cortex-M processor ³.

The first 512MB are dedicated to code area. STM32 devices further divide this area in some subregions as shown in Figure 1.4. Let us briefly introduce them.

![Image from PDF page 37](../images/page-0037-image-01.jpeg)

Figure 1.4: Memory layout of Code Area on STM32 MCUs

All Cortex-M processors map the code area starting at address 0x0000 0000⁴. This area also includes the pointer to the beginning of the stack (usually placed in SRAM) and the vector table, as we will see in Chapter 7. The position of the code area is standardized among all other Cortex-M vendors, even if the core architecture is sufficiently flexible to allow manufacturers to arrange this area in a different way. In fact, for all STM32 devices an area starting at address 0x0800 0000 is bound to the internal MCU flash memory, and it is the area where program code resides. However, thanks to a specific boot configuration we will explore in Chapter 22, this area is also aliased from address 0x0000 0000. This means that it is perfectly possible to refer to the content of the flash memory both starting at address 0x0800 0000 and 0x0000 0000 (for example, a routine located at address 0x0800

³Although the memory layout and the size of sub-regions (and therefore also their addresses) are standardized between all Cortex-M cores, some functionalities may differ. For example, Cortex-M7 does not provide bit-band regions, and some peripherals in the Private Peripheral Bus region differ. Always consult the reference manual for the architecture you are considering. ⁴To increase readability, all 32-bit addresses in this book are written splitting the upper two bytes from the lower ones. So, every time you see an address expressed in this way (0x0000 0000) you have to interpret it just as one common 32-bit address (0x00000000). This rule does not apply to C and assembly source code.</pre></td>
<td><pre>#### 1.1.1.2 内存映射

ARM 定义了一个标准化的内存地址空间，该空间为所有 Cortex-M 内核所共有，从而确保了代码在不同硅片制造商之间的可移植性。该地址空间宽度为 4GB，并划分为具有不同逻辑功能的若干子区域。图 1.3 展示了 Cortex-M 处理器的内存布局³。

前 512MB 专门用于代码区域。STM32 器件进一步将此区域划分为若干子区域，如图 1.4 所示。让我们简要介绍这些区域。

![Image from PDF page 37](../images/page-0037-image-01.jpeg)

图 1.4：STM32 微控制器上代码区域的内存布局

所有 Cortex-M 处理器都将代码区域映射到起始地址 0x0000 0000⁴。该区域还包括指向堆栈起始位置的指针（通常放置在 SRAM 中）以及向量表，我们将在第 7 章中对此进行介绍。代码区域的位置在所有其他 Cortex-M 供应商之间是标准化的，尽管内核架构足够灵活，允许制造商以不同的方式安排该区域。事实上，对于所有 STM32 器件，从地址 0x0800 0000 开始的区域绑定到内部 MCU 闪存，程序代码就驻留在该区域。然而，得益于我们将在第 22 章中探讨的特定启动配置，该区域也从地址 0x0000 0000 进行别名映射。这意味着完全可以通过地址 0x0800 0000 和 0x0000 0000 来引用闪存的内容（例如，位于地址 0x0800

³虽然内存布局以及子区域的大小（因此也包括它们的地址）在所有 Cortex-M 内核之间是标准化的，但某些功能可能存在差异。例如，Cortex-M7 不提供位带区域，且私有外设总线区域中的某些外设有所不同。请务必查阅您所考虑架构的参考手册。⁴为了提高可读性，本书中所有 32 位地址均将高两个字节与低两个字节分开书写。因此，每当看到以这种方式表示的地址（0x0000 0000）时，您应将其解释为一个普通的 32 位地址（0x00000000）。此规则不适用于 C 和汇编源代码。</pre></td>
</tr></tbody></table>

## PDF page 53 — Chapter 1: Introduction to STM32 MCU Portfolio

Focus: `numbers=1.2, 100, 16, 2, 25, 3.3V, 32, 5V, 8; negation=no, not, unless, without; conditions=If, if, unless; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>- working on a given STM32Fx CPU can easily be applied to other devices from the same family. Moreover, working with Cortex-M processors allows you to reuse much of the acquired skills if you (or your purchase team) decide to switch to Cortex-M MCUs from other vendors (in theory).
- Official development environment: ST invested a lot in recent years in building-up a complete development environment. They made too many mistakes in the past, by funding several projects around that ended in nothing. CooCox IDE and SW4STM32 where two previous attempts by ST to support open-source communities in growing-up a complete tool- chain for its microcontrollers, but they failed miserably. Finally, ST understood that this was discouraging a lot of people from adopting the STM32 portfolio, and so they decided to acquire Atollic in order to use their TrueSTUDIO IDE as the official tool-chain for the STM32 family of microcontrollers.
- Pin-to-pin compatibility: most of STM32 MCUs are designed to be pin-to-pin compatible inside the extensive STM32 portfolio. This is especially true for LQFP64-100 packages, and it is a big plus. You will have less responsibility in the initial choice of the right microcontroller for your application, knowing that you can eventually jump to another family in case you find it does not fit your needs.
- 5V tolerant: Most STM32 pins are 5V tolerant. This means that you can interface other devices that do not provide 3.3V I/O without using level shifters (unless speed is key to your application, a level shifter always introduce a parasitic capacitance that reduced the commutation frequency).
- 32 cents for 32 bit¹³: STM32F0 is the right choice if you want to migrate from 8/16-bit MCUs to a powerful and coherent platform, while keeping a comparable target price. You can use an RTOS to boost your application and write much better code.
- Integrated bootloader: STM32 MCUs are shipped with an integrated bootloader, which allows to reprogram the internal flash memory using some communication peripherals (USART, I²C, etc.). For some of you this will not be a killer feature, but it can dramatically simplify the work of people developing devices as professionals.

### 1.2.2 ….And Its Drawbacks

This book is not a brochure, or a document made by marketing people. Nor is the author an ST employee or is he having business with ST. So, it is right to say that there are some pitfalls regarding this platform.

- Learning curve: STM32’s learning curve can be quite steep, especially for inexperienced users. If you are completely new to embedded development, the process of learning how to develop STM32 applications can be frustrating. Even if ST is doing a great job at trying to improve the overall documentation and the official libraries, it is still hard to deal with this platform, and this is a shame. Historically, ST documentation has not been the best one for inexperienced people, being too cryptic and lacking clear examples.

¹³Due to the silicon market crisis in the twenties, this slogan is no longer valid. The crazy situation of the IC industry pushed prices of low-cost ICs (which are the most affected ones) by more than 25%. However, misery loves company and for low-cost applications STM32F0 family is still an interesting series to evaluate, unless a 8-bit solution is suitable for you.</pre></td>
<td><pre>- 针对特定 STM32Fx CPU 工作时获得的知识可以轻松地应用于同一系列的其他设备。此外，使用 Cortex-M 处理器允许您在（或您的采购团队）决定切换到其他供应商的 Cortex-M MCU 时（理论上）复用大部分已获得的技能。
- 官方开发环境：近年来，ST 在构建完整的开发环境方面投入了大量精力。过去他们犯了很多错误，资助了几个最终一无所成的项目。CooCox IDE 和 SW4STM32 是 ST 之前试图支持开源社区为其微控制器构建完整工具链的两次尝试，但都以惨败告终。最终，ST 意识到这阻碍了很多人采用 STM32 产品组合，因此他们决定收购 Atollic，以便将其 TrueSTUDIO IDE 用作 STM32 微控制器系列的官方工具链。
- 引脚对引脚兼容性：大多数 STM32 MCU 旨在在庞大的 STM32 产品组合内实现引脚对引脚兼容。这在 LQFP64-100 封装中尤为真实，这是一个巨大的加分项。在初始选择适合您应用程序的正确微控制器时，您的责任将更小，因为您知道如果当前选择不符合您的需求，最终可以跳转到另一个系列。
- 5V 容忍：大多数 STM32 引脚具有 5V 容忍能力。这意味着您可以连接其他不提供 3.3V I/O 的设备，而无需使用电平转换器（除非速度是您应用程序的关键，电平转换器总会引入寄生电容，从而降低换向频率）。
- 32 美分换 32 位¹³：如果您希望从 8/16 位 MCU 迁移到一个强大且一致的平台，同时保持可比较的目标价格，STM32F0 是合适的选择。您可以使用实时操作系统（real-time operating system）来提升您的应用程序并编写更好的代码。
- 集成引导加载程序：STM32 MCU 出厂时带有集成引导加载程序，允许使用某些通信外设（USART、I²C 等）重新编程内部闪存存储器。对你们中的一些人来说，这可能不是一个杀手级特性，但它可以极大地简化专业设备开发人员的工作。

### 1.2.2 …及其缺点

本书不是宣传册，也不是由营销人员编写的文档。作者也不是 ST 的员工，或与 ST 有业务往来。因此，可以说该平台存在一些陷阱。

- 学习曲线：STM32 的学习曲线可能相当陡峭，尤其是对经验不足的用户而言。如果你完全新手于嵌入式开发，学习如何开发 STM32 应用的过程可能会令人沮丧。尽管 ST 在努力改善整体文档和官方库方面做得很好，但处理该平台仍然很困难，这很遗憾。历史上，ST 的文档对于经验不足的人来说并不是最好的，过于晦涩且缺乏清晰的示例。

¹³由于 2020 年代的硅片市场危机，这一口号不再有效。IC 行业的疯狂状况导致低成本 IC（受影响最大的部分）价格上涨超过 25%。然而，祸不单行，对于低成本应用，STM32F0 系列仍然是一个值得评估的系列，除非 8 位解决方案适合你。</pre></td>
</tr></tbody></table>

## PDF page 56 — Chapter 1: Introduction to STM32 MCU Portfolio

Focus: `numbers=0056, 01, 1, 1.3, 1.4, 16, 256, 32, 4, 48, 56, 8, 96; negation=; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>MCUs feature a Cortex-M0+ core (named Network Processor) dedicated to the radio management and a user-programmable Cortex-M4 core (named Application Processor) for the main embedded application. STM32Wx solutions are compatible with multiple protocols, from point-to-point &amp; mesh to wide-area networks.

The following paragraphs give a brief description of each STM32 family, introducing its main features. The most important ones will be summarized inside tables. Tables were arranged by the author of this book, inspired by the official ST documentation.

### 1.3.1 F0

![Image from PDF page 56](../images/page-0056-image-01.png)

Table 1.4: STM32F0 features

The STM32F0 series is the most cost-effective line of MCU from the STM32 portfolio. It is designed to have a street price able to compete with some 8/16-bit MCUs from other vendors, offering a more advanced and powerful platform. The most important features of this series are:

- Core:

- – ARM Cortex-M0 core at a maximum clock rate of 48 MHz. – Cortex-M0 options include the SysTick Timer.
- Memory:

- – Static RAM from 4 to 32 KB. – Flash from 16 to 256 KB. – Each chip has a factory-programmed 96-bit unique device identifier number.
- Peripherals:

– Each F0-series device features a range of peripherals which vary from line to line (see Table 1.4 for a quick overview).</pre></td>
<td><pre>MCU 具有一个名为网络处理器 (Network Processor) 的 Cortex-M0+ 内核，专门用于无线电管理，以及一个名为应用处理器 (Application Processor) 的用户可编程 Cortex-M4 内核，用于主嵌入式应用。STM32Wx 解决方案兼容多种协议，从点对点和网状网络到广域网。

以下段落简要描述了每个 STM32 家族，介绍了其主要特性。最重要的特性将在表格中总结。表格由本书作者根据 ST 官方文档的灵感整理而成。

### 1.3.1 F0

![Image from PDF page 56](../images/page-0056-image-01.png)

表 1.4：STM32F0 特性

STM32F0 系列是 STM32 产品组合中性价比最高的微控制器（MCU）系列。其设计目标是以能够与其他厂商的 8/16 位 MCU 竞争的市场价格，提供一个更先进、更强大的平台。该系列最重要的特性包括：

- 内核：

- – 最高时钟频率为 48 MHz 的 ARM Cortex-M0 内核。 – Cortex-M0 选项包括 SysTick 定时器。
- 存储器：

- – 4 到 32 KB 的静态 RAM。 – 16 到 256 KB 的 Flash。 – 每颗芯片都有一个出厂预编程的 96 位唯一设备标识号。
- 外设：

– 每个 F0 系列器件都具备一系列外设，具体因产品线而异（快速概览请参见表 1.4）。</pre></td>
</tr></tbody></table>

## PDF page 90 — Chapter 2: Get In Touch With SM32CubeIDE

Focus: `numbers=2, 2.1; negation=; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre># 2. Get In Touch With SM32CubeIDE

Before we can start developing applications for the STM32 platform, we need a complete tool-chain. A tool-chain is a set of programs, compilers and tools that allows us:

- to write down our code and to navigate inside source files of our application;
- to navigate inside the application code, allowing us to inspect variables, function definition- s/declarations, and so on;
- to compile the source code using a cross-platform compiler;
- to upload and debug our application on the target development board (or a custom board we have made).

To accomplish these activities, we essentially need:

- an IDE with integrated source editor and navigator;
- a cross-platform compiler able to compile source code for the ARM Cortex-M platform;
- a debugger that allows us to execute step by step debugging of firmware on the target board;
- a tool that allows to interact with the integrated hardware debugger of our Nucleo board (the ST-LINK interface) or the dedicated programmer (e.g., a JTAG adapter).

In this chapter I will show how to install and to run the STM32CubeIDE tool-chain on Windows, Mac OS and Linux and I will provide to you an essential overview of the main functionalities of the Eclipse IDE.

## 2.1 Why Choose STM32CubeIDE as Tool-Chain for STM32

It has been a long time since the first edition of this book, and a lot of things are changed. Traditionally, STM32 lacked an official development environment fully, directly and actively maintained by ST. In the past years, ST tried to support several open source and community-based projects, all based on the free Eclipse/GCC tool-chains. However, none of these projects (CooCox, AC6) reached a real maturity level and this represented one of the major roadblocks in starting to work with STM32 microcontrollers.

The first edition of this book was characterized by the fact that it showed how to setup a complete, cross-platform and totally free tool-chain from scratch. It was an Eclipse-based tool-chain with the</pre></td>
<td><pre># 2。与 STM32CubeIDE 建立联系

在开始为 STM32 平台开发应用程序之前，我们需要一套完整的工具链。工具链是一组程序、编译器和工具，它使我们能够：

- 编写代码并在应用程序的源文件中进行导航；
- 在应用程序代码中进行导航，从而检查变量、函数定义s/declarations等；
- 使用跨平台编译器编译源代码；
- 将应用程序上传到目标开发板（或我们自行制作的定制板）并进行调试。

要完成这些活动，我们基本上需要：

- 一个集成源代码编辑器和导航器的集成开发环境（IDE）；
- 一个能够针对 ARM Cortex-M 平台编译源代码的跨平台编译器；
- 一个允许我们在目标板上对固件进行单步调试的调试器；
- 一个允许我们与 Nucleo 板上的集成硬件调试器（ST-LINK 接口）或专用编程器（例如 JTAG 适配器）进行交互的工具。

在本章中，我将展示如何在 Windows、Mac OS 和 Linux 上安装并运行 STM32CubeIDE 工具链，并为您提供 Eclipse IDE 主要功能的必要概述。

## 2.1 为何选择 STM32CubeIDE 作为 STM32 的工具链

自本书第一版以来已经过去了很长时间，很多事情都发生了变化。传统上，STM32 缺乏一个由 ST 完全、直接且积极维护的官方开发环境。在过去几年里，ST 尝试支持多个基于免费 Eclipse/GCC 工具链的开源和社区项目。然而，这些项目（CooCox、AC6）均未达到真正的成熟度，这构成了开始使用 STM32 微控制器的主要障碍之一。

本书第一版的特点是展示了如何从零开始搭建一套完整的、跨平台的且完全免费的工具链。那是一个基于 Eclipse 的工具链，其</pre></td>
</tr></tbody></table>

## PDF page 91 — Chapter 2: Get In Touch With SM32CubeIDE

Focus: `numbers=2017; negation=Without, cannot, no, unless, without; conditions=if, unless; identifiers=PC`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>addition of a set of plug-ins, named Eclipse Embedded CDT¹, developed and maintained by Liviu Ionescu, who did a really excellent work in providing support for the GCC ARM tool-chain. Without those plug-ins it was almost impossible to develop and run code with Eclipse for the STM32 platform. This project is now one of the official Eclipse Foundation projects, and it is still a good development environment to work with, especially if you are used to work with different Cortex-M platform.

At the end of 2017 STM decided to acquire Atollic², the company behind the TrueStudio IDE, a commercial distribution of Eclipse CDT and ARM GCC with the addition of dedicated plug-ins to develop embedded applications for ARM Cortex-M microcontrollers. After the acquisition of Atollic, ST decided to release the TrueStudio IDE for free for all STM32 developers, and the IDE was renamed in STM32CubeIDE. As we will see in this book, STM32CubeIDE is much more than a flavor of Eclipse CDT. ST invested a lot in integrating all the STM32-related tools inside just one piece of software, without requiring to developers to deal with the installation of several non-integrated tools scattered around the STM website. Moreover, STM finally completed the porting of all fundamental development tools to Linux and MacOS, allowing programmers to work with their favorite OS. This represents a true quantum leap for the STM32 platform, and nowadays I cannot see any real reason to use other development environments, unless you have strong requirements related to your very specific application (for example, to develop electronics for the automotive/aerospace industry). For this and other reasons better explained next, this edition of the book will be entirely based on the STM32CubeIDE.

However, despite the fact that STM32CubeIDE is now the official development environment by ST, there are several additional considerations to take in account while evaluating your tool-chain if you are in doubt about which to choose. Here you can find just a few considerations:

- It is GCC based: GCC is probably the best compiler on the earth, and it gives excellent results even with ARM based processors. ARM is nowadays the most widespread architecture (thanks to the embedded systems becoming widespread in the recent years), and many hardware and software manufacturers use GCC as the base tool for their platform.
- It is cross-platform: if you have a Windows PC, the latest sexy Mac or a Linux server you will be able to successfully develop, compile and upload the firmware on your development board with no difference. Nowadays, this is a mandatory requirement.
- Eclipse diffusion: a lot of IDEs for STM32 are also based on Eclipse, which has become a sort of standard. There are a lot of useful plug-ins for Eclipse that you can download with just one click. And it is a product that evolves day by day.
- Eclipse It is Open Source: ok. I agree. For such giant pieces of software, it is really hard to try to understand their internals and modify the code, especially if you are a hardware engineer committed to transistors and interrupts management. But if you get in trouble with your tool, it is simpler to try to understand what goes wrong with an open source tool than a closed one.
- Large and growing community: these tools have by now a great international community, which continuously develops new features and fixes bugs. You will find tons of examples and blogs, which can help you during your work. Moreover, many companies, which have adopted

¹https://eclipse-embed-cdt.github.io/ ²https://www.st.com/content/st_com/en/about/media-center/press-item.html/c2839.html</pre></td>
<td><pre>增加了一组名为 Eclipse Embedded CDT¹ 的插件，由 Liviu Ionescu 开发和维护，他在为 GCC ARM 工具链提供支持方面做出了非常出色的工作。如果没有这些插件，几乎不可能使用 Eclipse 为 STM32 平台开发和运行代码。该项目现在是 Eclipse 基金会的官方项目之一，并且仍然是一个良好的开发环境，特别是如果您习惯于在不同的 Cortex-M 平台上工作。

在 2017 末尾，ST 决定收购 Atollic²，即 TrueStudio IDE 背后的公司。TrueStudio IDE 是 Eclipse CDT 和 ARM GCC 的商业发行版，并增加了用于开发 ARM Cortex-M 微控制器嵌入式应用的专用插件。收购 Atollic 后，ST 决定向所有 STM32 开发者免费提供 TrueStudio IDE，并将该 IDE 更名为 STM32CubeIDE。正如我们将在本书中看到的那样，STM32CubeIDE 远不止是 Eclipse CDT 的一个变体。ST 投入了大量资源，将所有与 STM32 相关的工具集成到单一软件中，无需开发者处理分散在 ST 网站上的多个未集成工具的安装问题。此外，ST 最终完成了将所有基础开发工具移植到 Linux 和 MacOS 的工作，使程序员能够使用他们喜爱的操作系统。这代表了一次真正的量子

对于 STM32 平台而言，这是一次飞跃，如今我看不出有任何实际理由去使用其他开发环境，除非你对自己的特定应用有强烈需求（例如，为 automotive/aerospace 行业开发电子产品）。出于此及其他将在下文详细阐述的原因，本书的这一版将完全基于 STM32CubeIDE。

然而，尽管 STM32CubeIDE 如今已成为 ST 官方的开发环境，但如果您在工具链的选择上存在疑虑，在评估时仍需考虑若干额外因素。以下是一些可供参考的考量事项：

- 它基于 GCC：GCC 可能是地球上最好的编译器，即使在使用 ARM 内核的处理器上也能提供出色的结果。如今，ARM 是最普及的架构（得益于近年来嵌入式系统的广泛普及），许多硬件和软件制造商都将 GCC 作为其平台的基础工具。
- 它是跨平台的：无论您使用的是 Windows PC、最新的时尚 Mac 还是 Linux 服务器，您都能毫无差别地成功地在开发板上进行开发、编译和上传固件。如今，这是一项必备要求。
- Eclipse 的普及：许多用于 STM32 的集成开发环境也基于 Eclipse，它已成为一种标准。Eclipse 有许多有用的插件，只需单击一下即可下载。而且，它是一个每天都在不断演进的产品。
- Eclipse 是开源的：好的。我同意。对于如此庞大的

对于软件组件而言，想要理解其内部机制并修改代码确实非常困难，尤其是当你是一名专注于晶体管和中断管理的硬件工程师时。但是，如果你在使用工具时遇到问题，尝试理解一个开源工具出了什么问题，要比理解一个闭源工具简单得多。
- 庞大且不断壮大的社区：这些工具如今已拥有一个庞大的国际社区，该社区持续开发新功能并修复错误。你会找到大量的示例和博客，它们可以在你的工作中提供帮助。此外，许多已经采用

¹https://eclipse-embed-cdt.github.io/ ²https://www.st.com/content/st_com/en/about/media-center/press-item.html/c2839.html</pre></td>
</tr></tbody></table>

## PDF page 92 — Chapter 2: Get In Touch With SM32CubeIDE

Focus: `numbers=1, 2, 2.1; negation=not; conditions=If; identifiers=PC`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>- this software as official tools, give economical contribution to the main development. This guarantees that the software will not suddenly disappear.
- It is free: Yep. I placed this as the last point, but it is not the least. As said before, a commercial IDE can cost a fortune for a small company or a hobbyist/student. And the availability of free tools is one of the key advantages of the STM32 platform.

If you are completely new to Eclipse and/or GCC, here are some more specific considerations regarding these two products.

### 2.1.1 Two Words About Eclipse…

Eclipse³ is an Open Source and a free Java based IDE. Despite this fact (unfortunately, Java programs tend to eat a lot of machine resources and to slow down your PC), Eclipse is one of the most widespread and complete development environments. Eclipse comes in several pre-configured versions, customized for specific uses. For example, the Eclipse IDE for Java Developers comes preconfigured to work with Java and with all those tools used in this development platform (Ant, Maven, and so on). In our case, the STM32CubeIDE is essentially based on the Eclipse IDE for C/C++ Developers.

Eclipse is designed to be expandable thanks to plug-ins. There are several plug-ins available in Eclipse Marketplace useful for software development for embedded systems. We will install and use most of them in this book. Moreover, Eclipse is highly customizable. I strongly suggest you to take a look at its settings, which allow you to adapt it to your needs and flavor.

### 2.1.2 … and GCC

The GNU Compiler Collection⁴ (GCC) is a complete and widespread compiler suite. It is the only development tool able to compile several programming languages (front-end) to tens of hardware architectures that come in several variants. GCC is a really complex piece of software. It provides several tools to accomplish compilation tasks. These include, in addition to the compiler itself, an assembler, a linker, a debugger (known as GNU Debugger - GDB), several tools for binary files inspection, disassembly and optimization. Moreover, GCC is also equipped with the run-time environment for the C language, customized for the target architecture.

In recent years, several companies, even in the embedded world, have adopted GCC as their official compiler. For example, NXP uses GCC as cross-compiler for its LPC family of Cortex microcontrollers.

³http://www.eclipse.org ⁴https://gcc.gnu.org/</pre></td>
<td><pre>- 将这款软件作为官方工具，为主开发工作提供经济上的支持。这保证了该软件不会突然消失。
- 它是免费的：没错。我将这一点放在最后，但它并非最不重要。如前所述，对于小型公司或hobbyist/student.而言，商业集成开发环境可能价格高昂。而免费工具的可用性正是STM32平台的关键优势之一。

如果您完全不熟悉Eclipseand/or和GCC，以下是关于这两款产品的一些更具体的考量。

### 2.1.1 关于 Eclipse 的两句闲话…

Eclipse³ 是一款开源且免费的基于 Java 的集成开发环境（IDE）。尽管存在这一事实（不幸的是，Java 程序往往消耗大量机器资源并导致你的 PC 变慢），Eclipse 仍然是最普及且最完整的开发环境之一。Eclipse 提供多种预配置版本，针对特定用途进行了定制。例如，面向 Java 开发者的 Eclipse IDE 预配置了与 Java 以及该开发平台中使用的各种工具（如 Ant、Maven 等）协同工作的能力。在我们的案例中，STM32CubeIDE 本质上基于面向 C/C++ 开发者的 Eclipse IDE。

Eclipse 被设计为可通过插件进行扩展。Eclipse Marketplace 中有多个可用于嵌入式系统软件开发的插件。我们将在本书中安装并使用其中大部分插件。此外，Eclipse 具有高度的可定制性。我强烈建议你查看其设置，以便根据你的需求和偏好进行适配。

### 2.1.2 …以及 GCC

GNU 编译器集合⁴（GCC）是一套完整且广泛使用的编译器套件。它是唯一能够编译多种编程语言（前端）并生成数十种硬件架构（具有多种变体）代码的开发工具。GCC 是一个真正复杂的软件。它提供了多种工具以完成编译任务。除了编译器本身外，这些工具还包括汇编器、链接器、调试器（即 GNU Debugger - GDB），以及用于二进制文件检查、反汇编和优化的多种工具。此外，GCC 还配备了针对目标架构定制的 C 语言运行时环境。

近年来，多家公司，甚至是在嵌入式领域，都采用了 GCC 作为其官方编译器。例如，NXP 使用 GCC 作为其 LPC 系列 Cortex 微控制器的交叉编译器。

³http://www.eclipse.org ⁴https://gcc.gnu.org/</pre></td>
</tr></tbody></table>

## PDF page 95 — Chapter 2: Get In Touch With SM32CubeIDE

Focus: `numbers=0095, 01, 02, 2.2, 2.3, 95; negation=; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>![Image from PDF page 95](../images/page-0095-image-01.jpeg)

Figure 2.2: Windows installer welcome page

After few seconds the “Welcome to…” page of the installer appears, as shown in Figure 2.2. Click on “Next”, read the license agreement and click on “I Agree” to accept the terms of the agreement. In the next dialog (see Figure 2.3), it is possible to select the location for the installation. It is recommended to choose a short path to avoid facing Windows limitations with too long paths for the workspace. My suggestion is to leave the default path (C:\ST\STM32CubeIDE).

![Image from PDF page 95](../images/page-0095-image-02.jpeg)

Figure 2.3: Chose Install Location dialog</pre></td>
<td><pre>![Image from PDF page 95](../images/page-0095-image-01.jpeg)

图 2.2：Windows 安装程序欢迎页面

几秒钟后，安装程序的“欢迎使用……”页面将出现，如图 2.2 所示。点击“下一步”，阅读许可协议并点击“我同意”以接受协议条款。在下一个对话框中（见图 2.3），可以选择安装位置。建议选择较短的路径，以避免因工作区路径过长而遇到 Windows 的限制。我的建议是保留默认路径（C:\ST\STM32CubeIDE）。

![Image from PDF page 95](../images/page-0095-image-02.jpeg)

图 2.3：选择安装位置对话框</pre></td>
</tr></tbody></table>

## PDF page 102 — Chapter 2: Get In Touch With SM32CubeIDE

Focus: `numbers=01, 0102, 02, 102, 2.10, 2.8, 2.9; negation=; conditions=When; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>![Image from PDF page 102](../images/page-0102-image-01.png)

Figure 2.8: The Eclipse interface once started for the first time

Eclipse is a multi-view IDE, organized so that all the functionalities are displayed in one window, but the user is free to arrange the interface at its needs. When Eclipse starts, a welcome screen is presented. The content of that Welcome Tab is called view.

![Image from PDF page 102](../images/page-0102-image-02.jpeg)

Figure 2.9: How to close the Welcome view by clicking on the X.

To close the Welcome view, click on the cross icon, as shown in Figure 2.9. Once the Welcome view goes away, the C/C++ perspective appears, as shown in Figure 2.10.</pre></td>
<td><pre>![Image from PDF page 102](../images/page-0102-image-01.png)

图 2.8：Eclipse 首次启动后的界面

Eclipse 是一个多视图 IDE，其组织方式使得所有功能都显示在一个窗口中，但用户可以自由地根据自己的需求安排界面。当 Eclipse 启动时，会显示一个欢迎屏幕。该欢迎选项卡的内容称为视图（view）。

![Image from PDF page 102](../images/page-0102-image-02.jpeg)

图 2.9：通过点击 X 关闭欢迎视图。

要关闭欢迎视图，请点击交叉图标，如图 2.9 所示。一旦欢迎视图消失，C/C++ 透视图（perspective）就会出现，如图 2.10 所示。</pre></td>
</tr></tbody></table>

## PDF page 107 — Chapter 3: Hello, Nucleo!

Focus: `numbers=01, 0107, 02, 1, 1.18, 107, 144, 3.1, 32, 64; negation=; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>![Image from PDF page 107](../images/page-0107-image-01.jpeg)

Figure 3.1: The Target Selection wizard - STEP 1

![Image from PDF page 107](../images/page-0107-image-02.png)

As mentioned in Chapter 1, this book is entirely based on the Nucleo-64 board, and the examples in the text are tested for the boards listed in Table 1.18. However, the aim of this book is to teach the foundation concepts of STM32 programming. My opinion is that it should be relatively easy to adapt this and all other examples in the text to any other development board (Nucleo-32, Nucleo-144, Discovery, and so on).</pre></td>
<td><pre>![Image from PDF page 107](../images/page-0107-image-01.jpeg)

图 3.1：目标选择向导 - 步骤 1

![Image from PDF page 107](../images/page-0107-image-02.png)

如第 1 章所述，本书完全基于 Nucleo-64 开发板，且文中的示例已在表 1.18 中列出的开发板上进行了测试。然而，本书的目的是教授 STM32 编程的基础概念。我认为，将本文中的此示例及其他所有示例适配到其他任何开发板（Nucleo-32、Nucleo-144、Discovery 等）应该相对容易。</pre></td>
</tr></tbody></table>

## PDF page 114 — Chapter 3: Hello, Nucleo!

Focus: `numbers=01, 0114, 02, 114, 3.3, 3.7; negation=not; conditions=if, when; identifiers=PC`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>## 3.3 Connecting the Nucleo to the PC

Once we have compiled our test project, you can connect the Nucleo board to your computer using a USB cable connected to micro-USB port (called VCP in Figure 3.7). You should see at least two LEDs turning ON.

Read Carefully

![Image from PDF page 114](../images/page-0114-image-01.png)

Please, ensure that the USB port is able to provide sufficient power to the board. It is strongly suggested to use a USB port able to provide at least 500mAh or a self-powered external hub.

![Image from PDF page 114](../images/page-0114-image-02.jpeg)

Figure 3.7: A Nucleo board and its main interfaces

The first one is the LD1 LED, which in Figure 3.7 is labeled ST-LINK LED. It is a red/green LED, and it is used to signal the ST-LINK activity: once the board is connected to the computer, that LED is green; during a debug session or while uploading the firmware on the MCU it blinks green and red alternatively.

Another LED that turns ON when the board is connected to the computer is the LED LD3, which is labeled POWER LED in Figure 3.7. It is a red LED that turns ON when the USB port ends enumeration, that is the ST-LINK interface is properly recognized by the computer OS as a USB peripheral. The target MCU on the board is powered only when that LED is ON (this means that the ST-LINK interface also manages the powering of the target MCU).

Finally, if you have not still flashed your board with a custom firmware, you will see that the LD2 LED, the green LED labeled USER LED in Figure 3.7, also blinks: this happens because ST preloads</pre></td>
<td><pre>## 3.3 将 Nucleo 连接到 PC

一旦我们编译了测试项目，就可以使用连接到 micro-USB 端口（在图 3.7 中称为 VCP）的 USB 线将 Nucleo 板连接到你的计算机。你应该至少能看到两个 LED 亮起。

仔细阅读

![Image from PDF page 114](../images/page-0114-image-01.png)

请确保 USB 端口能够为板卡提供足够的电力。强烈建议使用能够提供至少 500mAh 的 USB 端口或自供电的外部集线器。

![Image from PDF page 114](../images/page-0114-image-02.jpeg)

图 3.7：Nucleo 板及其主要接口

第一个是 LD1 LED，在图 3.7 中标记为 ST-LINK LED。它是一个红/绿 LED，用于指示 ST-LINK 的活动状态：一旦板卡连接到计算机，该 LED 为绿色；在调试会话期间或向 MCU 上传固件时，它会交替闪烁绿色和红色。

另一个在板卡连接到计算机时会点亮的 LED 是 LD3，在图 3.7 中标记为 POWER LED。它是一个红色 LED，当 USB 端口完成枚举时点亮，即 ST-LINK 接口被计算机操作系统正确识别为 USB 外设。板卡上的目标 MCU 仅在该 LED 点亮时才通电（这意味着 ST-LINK 接口还负责管理目标 MCU 的供电）。

最后，如果你还没有用自定义固件刷写你的板卡，你会看到 LD2 LED，即图 3.7 中标记为 USER LED 的绿色 LED，也在闪烁：这是因为 ST 预加载了</pre></td>
</tr></tbody></table>

## PDF page 119 — Chapter 4: STM32CubeMX Tool

Focus: `numbers=32, 350, 4, 4.1, 8; negation=not, without; conditions=if, when; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre># 4. STM32CubeMX Tool

The times when the configuration of an 8-bit microcontroller peripheral could be performed with a few assembly instructions are far away. Although there is a well-established group of people that still develops embedded software in pure assembly code¹, time is the most expensive thing during project development nowadays, and it is important to receive as much help as possible for a quite complex hardware platform like the STM32. Moreover, in modern 32-bit MCUs, especially those with a very high number of I/Os, to drive even a simple GPIO could require to you digging inside tens of pages of a one thousand pages datasheet. Believe me or not, it could be really frustrating to simply initialize an advanced peripheral like DCMI or ETH interface in an STM32H7 without dedicated support by the ST HAL. Finally, to know all the possible configuration alternatives of a GPIO requires that you have a complete overview of all supported peripherals by the very specific STM32 part number, with its specific pinout and configuration. Lucky for us, ST provides a powerful and convenient tool that avoid us to simply ignore all the specific implementation details underling a peripheral configuration: STM32CubeMX.

STM32CubeMX² is the Swiss army knife of every STM32 developer, and it is a fundamental tool especially if you are new to the STM32 platform. It is a quite complex piece of software distributed freely by ST, and it is available both as a stand-alone tool downloadable from the ST website and as integrated component inside the STM32CubeIDE.

In this chapter we will see how CubeMX works, and how to generate working projects from scratch using the code generated by it. This will allow us to create better code and ready to be integrated with the rest of STM32Cube HAL. However, this chapter is not a substitute for the official ST documentation for CubeMX tool³, a document made of more than 350 pages that explains in depth all its functionalities.

## 4.1 Introduction to CubeMX Tool

CubeMX is the tool used to configure the microcontroller chosen for our project. It is used both to choose the right hardware connections and to generate the code necessary to configure the ST HAL.

CubeMX is an MCU-centric application. This means that all activities performed by the tool are based on:

- The family of the STM32 MCU (F0, F1, and so on).

¹Probably, one day someone will explain them that, except for rare and specific cases, a modern compiler can generate better assembly code from C than could be written directly in assembly by hand. However, we have to say that these habits are limited to ultra low-cost 8-bit MCUs like PIC12 and similar. ²STM32CubeMX name will be simplified in CubeMX in the rest of the book. ³https://bit.ly/3k8HeE2</pre></td>
<td><pre># 4. STM32CubeMX 工具

通过几条汇编指令即可配置 8 位微控制器外设的时代已经远去。尽管仍有一群根深蒂固的开发者坚持使用纯汇编代码¹开发嵌入式软件，但在当今的项目开发中，时间是最昂贵的资源，对于 STM32 这样相当复杂的硬件平台，获得尽可能多的帮助至关重要。此外，在现代 32 位 MCU 中，尤其是那些拥有大量 I/O 端口的型号，即使驱动一个简单的 GPIO 也可能需要你在长达一千页的数据手册中翻阅数十页。信不信由你，如果没有 ST HAL 的专门支持，仅仅初始化 STM32H7 上像 DCMI 或 ETH 接口这样的高级外设，真的会令人非常沮丧。最后，要了解 GPIO 的所有可能配置选项，要求你对特定 STM32 型号所支持的所有外设、其特定的引脚布局和配置有完整的概览。幸运的是，ST 提供了一款强大且便捷的工具，使我们无需关注外设配置底层的所有特定实现细节，这就是 STM32CubeMX。

STM32CubeMX² 是每位 STM32 开发者的瑞士军刀，特别是对于 STM32 平台的新手来说，它是一款基础工具。这是一款相当复杂的软件，由 ST 免费分发，既可以作为从 ST 网站下载的独立工具使用，也可以作为 STM32CubeIDE 内部的集成组件使用。

在本章中，我们将了解 CubeMX 的工作原理，以及如何利用它生成的代码从零开始创建可运行的项目。这将使我们能够创建更好的代码，并准备好与 STM32Cube HAL 的其余部分集成。然而，本章不能替代 CubeMX 工具的官方 ST 文档³，该文档长达 350 多页，深入解释了其所有功能。

## 4.1 CubeMX 工具简介

CubeMX 是用于配置我们项目中选定的微控制器的工具。它既用于选择正确的硬件连接，也用于生成配置 ST HAL 所需的代码。

CubeMX 是一个以 MCU 为中心的应用程序。这意味着该工具执行的所有活动都基于：

- STM32 MCU 的系列（F0、F1 等）。

¹ 可能有一天，有人会向他们解释，除了少数特定情况外，现代编译器从 C 语言生成的汇编代码比手工直接编写的汇编代码更好。然而，我们必须说，这些习惯仅限于 PIC12 等超低成本 8 位 MCU。 ² 在本书其余部分，STM32CubeMX 的名称将简化为 CubeMX。 ³ https://bit.ly/3k8HeE2</pre></td>
</tr></tbody></table>

## PDF page 134 — Chapter 4: STM32CubeMX Tool

Focus: `numbers=01, 0134, 134, 4, 4.1, 4.13; negation=; conditions=If; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>### 4.1.4 Tools View

The Tools view contains other relevant configuration panes, some of which are available on more advanced STM32 MCUs like the STM32MP1 series. Instead, for all STM32 microcontrollers it is available the Power Consumption Calculator (PCC), which is a feature of CubeMX that, given a microcontroller, a battery model and a user-defined power sequence, provides an estimation of the following parameters:

- Average power consumption.
- Battery life.
- Average DMIPS.

It is possible to add user-defined batteries through a dedicated interface. For each step, the user can choose VBUS as possible power source instead of the battery. This will impact the battery life estimation. If power consumption measurements are available at different voltage levels, CubeMX will also propose a choice of voltage values.

PCC view will be analyzed in a following chapter.

![Image from PDF page 134](../images/page-0134-image-01.png)

Figure 4.13: The CubeMX Tools view</pre></td>
<td><pre>### 4.1.4 工具视图

工具视图包含其他相关的配置面板，其中一些面板仅在更高级的 STM32 微控制器（如 STM32MP1 系列）上可用。相反，对于所有 STM32 微控制器，都可用功耗计算器（PCC）。这是 CubeMX 的一项功能，给定一个微控制器、一个电池模型和一个用户定义的电源序列，它可以估算以下参数：

- 平均功耗。
- 电池寿命。
- 平均 DMIPS。

可以通过专用界面添加用户定义的电池。对于每个步骤，用户可以选择 VBUS 作为可能的电源，而不是电池。这将影响电池寿命的估算。如果在不同的电压级别下有功耗测量数据，CubeMX 还会提供电压值的选择。

PCC 视图将在后续章节中进行分析。

![Image from PDF page 134](../images/page-0134-image-01.png)

图 4.13：CubeMX 工具视图</pre></td>
</tr></tbody></table>

## PDF page 151 — Chapter 5: Introduction to Debugging

Focus: `numbers=01, 0151, 02, 03, 04, 05, 06, 07, 08, 151, 5.2, 5.3, 5.5; negation=without; conditions=When, otherwise; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>![Image from PDF page 151](../images/page-0151-image-01.png)

Figure 5.5: How to add a breakpoint at a given line number

Eclipse allows to easily setup breakpoints inside the code from the editor view in the center of Debug perspective. To place a breakpoint, simply double-click on the greyish stripe on the left of the editor, near to the instruction where we want to halt the MCU execution. A blue bullet will appear, as shown in Figure 5.5.

When the program counter reaches the first assembly instruction constituting that line of code, the execution is halted, and Eclipse shows the corresponding line of code as shown in Figure 5.3. Once we have inspected the code, we have several options to resume the execution. Table 5.2 explain the usage of the most relevant icons on the Eclipse debug toolbar.

Table 5.2: Most relevant icons on the Eclipse debug toolbar

Icon Description

![Image from PDF page 151](../images/page-0151-image-02.jpeg)

This icon is used ignore all breakpoints and continue the execution without interruptions.

![Image from PDF page 151](../images/page-0151-image-03.jpeg)

This icon is used to do a soft reset of MCU, without stopping the debug and relaunch it again.

![Image from PDF page 151](../images/page-0151-image-04.jpeg)

This icon terminates the debug session, starts a build of the project and restart debug session.

![Image from PDF page 151](../images/page-0151-image-05.jpeg)

This icon resumes the debug session after the MCU reached a breakpoint or an explicit pause by the user.

![Image from PDF page 151](../images/page-0151-image-06.jpeg)

This icon halts the code execution to the next C statement.

![Image from PDF page 151](../images/page-0151-image-07.jpeg)

This icon causes the end of the debug session. GDB is terminated and the target board is halted.

![Image from PDF page 151](../images/page-0151-image-08.jpeg)

This icon is the first one of two icons used to do step-by-step debugging. When we execute the firmware line-by-line, it could be important to enter inside a called routine. This icon allows to do this, otherwise the next icon is what needed to execute the next instruction inside the current stack frame.</pre></td>
<td><pre>![Image from PDF page 151](../images/page-0151-image-01.png)

图 5.5：如何在特定行号处添加断点

Eclipse 允许在调试透视图中央的编辑器视图中轻松地在代码内设置断点。要放置断点，只需双击编辑器左侧的灰色条纹，靠近我们希望暂停 MCU 执行的指令处。将出现一个蓝色圆点，如图 5.5 所示。

当程序计数器到达构成该行代码的第一条汇编指令时，执行将被暂停，Eclipse 将显示相应的代码行，如图 5.3 所示。一旦我们检查了代码，就有几个选项来恢复执行。表 5.2 解释了 Eclipse 调试工具栏上最相关图标的用法。

表 5.2：Eclipse 调试工具栏上最相关的图标

图标 描述

![Image from PDF page 151](../images/page-0151-image-02.jpeg)

此图标用于忽略所有断点并继续执行，而不中断。

![Image from PDF page 151](../images/page-0151-image-03.jpeg)

此图标用于对 MCU 进行软复位，而不停止调试并再次启动它。

![Image from PDF page 151](../images/page-0151-image-04.jpeg)

此图标终止调试会话，开始构建项目并重新启动调试会话。

![Image from PDF page 151](../images/page-0151-image-05.jpeg)

此图标在 MCU 到达断点或用户显式暂停后恢复调试会话。

![Image from PDF page 151](../images/page-0151-image-06.jpeg)

此图标将代码执行暂停到下一个 C 语句。

![Image from PDF page 151](../images/page-0151-image-07.jpeg)

此图标导致调试会话结束。GDB 被终止，目标板被暂停。

![Image from PDF page 151](../images/page-0151-image-08.jpeg)

此图标是用于逐步调试的两个图标中的第一个。当我们逐行执行固件时，进入被调用的例程可能很重要。此图标允许这样做，否则下一个图标才是执行当前栈帧内下一条指令所需的。</pre></td>
</tr></tbody></table>

## PDF page 157 — Chapter 5: Introduction to Debugging

Focus: `numbers=0, 1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 2, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 3, 30; negation=not; conditions=If; identifiers=HAL_Delay, HAL_Init, HAL_UART_, MX_GPIO_Init, MX_USART2_UART_Init, SystemClock_Config, printf`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>## HAL_UART_* routines to exchange data over the UART.

## To retarget the standard streams in your firmware, just initialize the library calling the RetargetInit() and passing the pointer to the UART_HandleTypeDef instance of the UART2 (line 46). For example, the following code shows how to use printf()/scanf() functions in your firmware:

```text
Filename: CH5-EX1/Core/Src/main.c
1
#include &quot;main.h&quot;
2
#include &lt;retarget.h&gt;
3
#include &lt;stdio.h&gt;
```

4

```text
5
/* Private variables ---------------------------------------------------------*/
6
UART_HandleTypeDef huart2;
```

7

```text
8
/* Private function prototypes -----------------------------------------------*/
9
void SystemClock_Config(void);
10
static void MX_GPIO_Init(void);
11
static void MX_USART2_UART_Init(void);
```

12

```text
13
int main(void) {
14
uint8_t uTimes = 0;
```

15

```text
16
/* Reset of all peripherals, Initializes the Flash interface and the Systick. */
17
HAL_Init();
18
/* Configure the system clock */
19
SystemClock_Config();
```

20

```text
21
/* Initialize all configured peripherals */
22
MX_GPIO_Init();
23
MX_USART2_UART_Init();
24
/* Enables retarget of standard I/O over the USART2 */
25
RetargetInit(&amp;huart2);
```

26

```text
27
printf(&quot;How many times to print the message?: &quot;);
28
scanf(&quot;%hhu&quot;, &amp;uTimes);
29
printf(&quot;\r\n&quot;);
```

30

```text
31
for(uint8_t i = 0; i &lt; uTimes;) {
32
HAL_Delay(500);
33
printf(&quot;Hello, Nucleo: %u \r\n&quot;, ++i);
34
}
35
while(1);
36
}
```

## Please, take note that this example assumes a project generated by following the same procedure shown in Chapter 3. If not all things are clear now, do not worry: after reading the Chapter 8 you will be able to understand every operations performed.</pre></td>
<td><pre>## `HAL_UART_*` 例程通过 UART 交换数据。

## 要在固件中重定向标准流，只需调用 `RetargetInit()` 初始化库，并传入 UART2 的 `UART_HandleTypeDef` 实例指针（第 46 行）。例如，以下代码展示了如何在固件中使用 `printf()`/`scanf()` 函数：

```text
Filename: CH5-EX1/Core/Src/main.c
1
#include &quot;main.h&quot;
2
#include &lt;retarget.h&gt;
3
#include &lt;stdio.h&gt;
```

4

```text
5
/* Private variables ---------------------------------------------------------*/
6
UART_HandleTypeDef huart2;
```

7

```text
8
/* Private function prototypes -----------------------------------------------*/
9
void SystemClock_Config(void);
10
static void MX_GPIO_Init(void);
11
static void MX_USART2_UART_Init(void);
```

12

```text
13
int main(void) {
14
uint8_t uTimes = 0;
```

15

```text
16
/* Reset of all peripherals, Initializes the Flash interface and the Systick. */
17
HAL_Init();
18
/* Configure the system clock */
19
SystemClock_Config();
```

20

```text
21
/* Initialize all configured peripherals */
22
MX_GPIO_Init();
23
MX_USART2_UART_Init();
24
/* Enables retarget of standard I/O over the USART2 */
25
RetargetInit(&amp;huart2);
```

26

```text
27
printf(&quot;How many times to print the message?: &quot;);
28
scanf(&quot;%hhu&quot;, &amp;uTimes);
29
printf(&quot;\r\n&quot;);
```

30

```text
31
for(uint8_t i = 0; i &lt; uTimes;) {
32
HAL_Delay(500);
33
printf(&quot;Hello, Nucleo: %u \r\n&quot;, ++i);
34
}
35
while(1);
36
}
```

## 请注意，本示例假设项目是按照第 3 章中所示的相同步骤生成的。如果现在并非所有内容都清晰明了，请不要担心：在阅读完第 8 章后，您将能够理解所执行的每一项操作。</pre></td>
</tr></tbody></table>

## PDF page 160 — Chapter 6: GPIO Management

Focus: `numbers=6, 6.1; negation=; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre># 6. GPIO Management

All STM32 microcontrollers have a variable number of General Programmable I/Os (GPIO) . The exact number depends on:

- The type of package chosen (LQFP48, BGA176, and so on).
- The family of microcontroller (F0, F1, etc.).
- The usage of external crystals for HSE and LSE.

GPIOs are the way an MCU communicates with the external world. Every electronic board uses a variable number of I/Os to drive external peripherals (e.g. an LED) or to exchange data through several types of communication peripherals (UART, USB, SPI, etc.).

This chapter starts our journey inside the CubeHAL by looking to one of its simplest modules: HAL_- GPIO. We have already used several functions from this module in the early examples in this book, but now it is the right time to understand all possibilities offered by a so simple and commonly used peripheral. However, before we can start describing HAL features, it is best to give a quick look at how the STM32 peripherals are mapped to logical addresses and how they are represented inside the HAL library.

## 6.1 STM32 Peripherals Mapping and HAL Handlers

Every STM32 peripheral is interconnected to the MCU core by several orders of buses, as shown in Figure 6.1¹.

¹Here, to simplify this topic, we are considering the bus organization of one of the simplest STM32 microcontrollers, the STM32F072. STM32F4 and STM32F7, for example, have a more advanced bus interconnection system, which is outside the scope of this book. Please, always refer to the reference manual of your MCU.</pre></td>
<td><pre># 6. GPIO 管理

所有 STM32 微控制器都具有可变数量的通用可编程输入/输出（GPIO）。具体数量取决于：

- 所选的封装类型（如 LQFP48、BGA176 等）。
- 微控制器的系列（F0、F1 等）。
- 是否使用外部晶振用于 HSE 和 LSE。

GPIO 是 MCU 与外部世界通信的方式。每个电子板卡都使用可变数量的 I/O 来驱动外部外设（例如 LED）或通过多种类型的通信外设（UART、USB、SPI 等）交换数据。

本章通过查看 CubeHAL 中最简单的模块之一：HAL_- GPIO，开始了我们在 CubeHAL 内部的旅程。我们已经在本书早期的示例中使用过该模块的几个函数，但现在正是理解如此简单且常用的外设所提供的所有可能性的合适时机。然而，在我们开始描述 HAL 功能之前，最好先快速了解一下 STM32 外设如何映射到逻辑地址，以及它们在 HAL 库中是如何表示的。

## 6.1 STM32 外设映射和 HAL 句柄

每个 STM32 外设都通过多个级别的总线与 MCU 内核互连，如图 6.1¹ 所示。

¹ 此处，为了简化主题，我们考虑的是最简单的 STM32 微控制器之一，即 STM32F072 的总线组织。例如，STM32F4 和 STM32F7 具有更先进的总线互连系统，这超出了本书的范围。请始终参考您的 MCU 参考手册。</pre></td>
</tr></tbody></table>

## PDF page 172 — Chapter 6: GPIO Management

Focus: `numbers=01, 0172, 172; negation=; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>Eclipse Intermezzo

It is possible to heavily customize the Eclipse interface by installing custom themes. A theme essentially allows to change the appearance of the Eclipse user interface. This may seem a nonessential feature, but nowadays a lot of programmers prefer to customize colors, fonts type and size and so on of their favorite development environment. That is one of the success reasons of some minimal yet highly customizable source code editors, like TextMate, Sublime Text or Visual Studio Code.

Instead of customizing the interface with regular Eclipse settings, there are several theme packs available for Eclipse on the Eclipse Marketplace. This author prefers dark themes, instead of light ones. A recent theme pack is the Darkest Dark Themeincluded with DevStyle theming pack. The STM32CubeIDE interface will change quite a lot, with a UX similar to recent releases of Android Studio, as you can see in the following capture.

![Image from PDF page 172](../images/page-0172-image-01.png)

https://marketplace.eclipse.org/content/darkest-dark-theme-devstyle</pre></td>
<td><pre>Eclipse 插曲

通过安装自定义主题，可以深度定制 Eclipse 界面。主题基本上允许更改 Eclipse 用户界面的外观。这似乎是一个非必要的功能，但如今许多程序员更喜欢定制他们喜爱的开发环境的颜色、字体类型和大小等。这是 TextMate、Sublime Text 或 Visual Studio Code 等极简但高度可定制的源代码编辑器成功的原因之一。

除了使用常规的 Eclipse 设置来定制界面外，Eclipse Marketplace 上还有几个可供 Eclipse 使用的主题包。作者更喜欢深色主题，而不是浅色主题。一个较新的主题包是包含在 DevStyle 主题包中的 Darkest Dark Theme。STM32CubeIDE 的界面会发生很大变化，用户体验类似于 Android Studio 的最新版本，如下面的截图所示。

![Image from PDF page 172](../images/page-0172-image-01.png)

https://marketplace.eclipse.org/content/darkest-dark-theme-devstyle</pre></td>
</tr></tbody></table>

## PDF page 188 — Chapter 7: Interrupts Management

Focus: `numbers=0, 01, 0188, 1, 188, 7.12; negation=no, not, unless; conditions=When, if, otherwise, unless; identifiers=HAL_NVIC_GetPendingIRQ, HAL_NVIC_SetPendingIRQ`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>![Image from PDF page 188](../images/page-0188-image-01.png)

Figure 7.12: When an interrupt is forced setting its pending bit, the corresponding peripheral IRQ remains unset

The Figure 7.12 shows another case. Here we force the execution of the ISR setting its pending bit. Since this time the external peripheral is not involved, there is no need to clear the corresponding IRQ pending bit.

Since the presence of the IRQ pending bit is peripheral dependent, it is always opportune to use the ST HAL functions to manage interrupts, leaving all the underlying details to the HAL implementation (unless we want to have full control, but this is not case of this book). However, take in mind that to avoid losing important interrupts, it is a good design practice to clear peripherals IRQ pending status bit as their ISR start to be serviced. The processor core does not keep track of multiple interrupts (it does not queue interrupts), so if we clear the peripheral pending bit at the end of an ISR, we may lose important IRQs that fire in the middle.

To see if an interrupt is pending (that is, fired but not running), we can use the HAL function:

```text
uint32_t HAL_NVIC_GetPendingIRQ(IRQn_Type IRQn);
```

which returns 0 if the IRQ is not pending, 1 otherwise. To set the pending bit of an IRQ we can use the HAL function:

```text
void HAL_NVIC_SetPendingIRQ(IRQn_Type IRQn);
```

This will cause the interrupt to fire, as it would be generated by the hardware. A distinctive feature of Cortex-M processors it that it is possible to programmatically fire an interrupt inside the ISR routine of another interrupt. Instead, to clear the pending bit of an IRQ, we can use the function:</pre></td>
<td><pre>![Image from PDF page 188](../images/page-0188-image-01.png)

图 7.12：当通过设置其挂起位强制中断时，相应的外设 IRQ 保持未设置状态

图 7.12 展示了另一种情况。在这里，我们通过设置其挂起位来强制 ISR 的执行。由于这次外部外设没有参与，因此无需清除相应的 IRQ 挂起位。

由于 IRQ 挂起位的存在取决于外设，因此始终建议使用 ST HAL 函数来管理中断，将所有底层细节留给 HAL 实现（除非我们想要完全控制，但本书并非这种情况）。然而，请记住，为了避免丢失重要的中断，良好的设计实践是在 ISR 开始被服务时清除外设 IRQ 挂起状态位。处理器内核不跟踪多个中断（它不排队中断），因此如果我们在 ISR 结束时清除外设挂起位，我们可能会丢失在中间触发的重要 IRQ。

要检查中断是否处于挂起状态（即已触发但未运行），我们可以使用 HAL 函数：

```text
uint32_t HAL_NVIC_GetPendingIRQ(IRQn_Type IRQn);
```

如果 IRQ 不处于挂起状态，则返回 0，否则返回 1。要设置 IRQ 的挂起位，我们可以使用 HAL 函数：

```text
void HAL_NVIC_SetPendingIRQ(IRQn_Type IRQn);
```

这将导致中断触发，就像由硬件生成的一样。Cortex-M 处理器的一个显著特征是，可以在另一个中断的 ISR 例程中编程触发一个中断。相反，要清除 IRQ 的挂起位，我们可以使用函数：</pre></td>
</tr></tbody></table>

## PDF page 203 — Chapter 7: Interrupts Management

Focus: `numbers=0, 01, 0203, 1, 203, 32, 7.22, 7.6; negation=disable, disabled, disables, not, without; conditions=if, otherwise; identifiers=BASEPRI, FAULTMASK, PRIMASK, __disable_irq, __enable_irq, __get_FAULTMASK, __get_PRIMARK, __set_FAULTMASK, __set_PRIMASK`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>## 7.6 Mask All Interrupts at Once or an a Priority Basis

Sometimes we want to be sure that our code is not preempted to allow the execution of interrupts or more privileged code. That is, we want to ensure that our code is thread-safe. Cortex-M based processors allow to temporarily mask the execution of all interrupts and exceptions, without disabling one by one. Two special registers, named PRIMASK and FAULTMASK allow to disable all interrupts and exceptions respectively.

![Image from PDF page 203](../images/page-0203-image-01.png)

```text
Figure 7.22: PRIMASK, FAULTMASK and BASEPRI registers
```

Even if these registers are 32-bit wide, just the first bit is used to enable/disable interrupts and exceptions. The ARM assembly instruction CPSID i disables all interrupt by setting the PRIMASK bit to 1, while the CPSIE i instructions enables them by setting PRIMASK to zero. Instead, the instruction CPSID f disables all exceptions (except for the NMI one) by setting the FAULTMASK bit to 1, while the CPSIE f instructions enables them.

The CMSIS-Core package provides several macros that we can use to perform these operation: __disable_irq() and __enable_irq() automatically set and clear the PRIMASK. Any critical task can be placed between these two macros, as shown below:

```text
...
__disable_irq();
/* All exceptions with configurable priority are temporarily disabled.
You can place critical code here */
...
__enable_irq();
```

However, take in mind that, as general rule, interrupt must be masked only for really short time, otherwise you could lose important interrupts. Remember that interrupts are not queued.

Another macro we can use is the __set_PRIMASK(x) one, where x is the content of the PRIMASK register (0 or 1). The macro __get_PRIMARK() returns the content of the PRIMASK register. Instead, the macros __set_FAULTMASK(x) and __get_FAULTMASK() allow to manipulate the FAULTMASK register.

It is important to remark that, once the PRIMASK register is again set to zero, all pending interrupts are serviced according to their priority: PRIMASK causes that the the interrupt pending bit is set but the ISR is not serviced. This is the reason why we say that interrupts are masked and not disabled. Interrupts start to be serviced as soon as the PRIMASK is cleared.</pre></td>
<td><pre>## 7.6 一次性屏蔽所有中断或基于优先级屏蔽

有时，我们希望确保代码不会被抢占，从而允许执行中断或更高权限的代码。也就是说，我们希望确保代码是线程安全的。基于 Cortex-M 的处理器允许临时屏蔽所有中断和异常的执行，而无需逐个禁用。两个特殊的寄存器，名为 PRIMASK 和 FAULTMASK，分别允许禁用所有中断和异常。

![Image from PDF page 203](../images/page-0203-image-01.png)

```text
Figure 7.22: PRIMASK, FAULTMASK and BASEPRI registers
```

尽管这些寄存器是 32 位宽的，但仅使用第一个位来启用/禁用中断和异常。ARM 汇编指令 CPSID i 通过将 PRIMASK 位设置为 1 来禁用所有中断，而 CPSIE i 指令通过将 PRIMASK 设置为零来启用它们。相反，指令 CPSID f 通过将 FAULTMASK 位设置为 1 来禁用所有异常（NMI 除外），而 CPSIE f 指令则启用它们。

CMSIS-Core 包提供了几个宏，我们可以使用它们来执行这些操作：__disable_irq() 和 __enable_irq() 会自动设置和清除 PRIMASK。任何关键任务都可以放置在这两个宏之间，如下所示：

```text
...
__disable_irq();
/* All exceptions with configurable priority are temporarily disabled.
You can place critical code here */
...
__enable_irq();
```

然而，请记住，作为一般规则，中断只能被屏蔽很短的时间，否则您可能会丢失重要的中断。请记住，中断不会被排队。

我们可以使用的另一个宏是 __set_PRIMASK(x)，其中 x 是 PRIMASK 寄存器的内容（0 或 1）。宏 __get_PRIMARK() 返回 PRIMASK 寄存器的内容。相反，宏 __set_FAULTMASK(x) 和 __get_FAULTMASK() 允许操作 FAULTMASK 寄存器。

重要的是要指出，一旦 PRIMASK 寄存器再次被设置为零，所有挂起的中断将根据其优先级得到服务：PRIMASK 导致中断挂起位被设置，但 ISR 未被服务。这就是为什么我们说中断是被屏蔽而不是被禁用的原因。一旦 PRIMASK 被清除，中断就开始得到服务。</pre></td>
</tr></tbody></table>

## PDF page 218 — Chapter 8: Universal Asynchronous Serial Communications

Focus: `numbers=01, 0218, 218, 38400, 8.3, 8.5; negation=not; conditions=When, when; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>![Image from PDF page 218](../images/page-0218-image-01.jpeg)

Figure 8.5: CubeMX can be used to configure the UART2 interface easily

## 8.3 UART Communication in Polling Mode

STM32 microcontrollers, and hence the CubeHAL, offer three ways to exchange data between peers over a UART communication: polling, interrupt and DMA mode. It is important to stress right from now that these modes are not only three different flavors to handle UART communications. They are three different programming approach to the same task, which introduce several benefits both from the design and performance point of view. Let us introduce them briefly.

- In polling mode, also called blocking mode, the main application, or one of its threads, synchronously waits for the data transmission and reception. This is the simplest form of data communication using this peripheral, and it can be used when the transmit rate is not too much low and when the UART is not used as critical peripheral in our application (the classical example is the usage of the UART as output console for debug activities).
- In interrupt mode, also called non-blocking mode, the main application is freed from waiting for the completion of data transmission and reception. The data transfer routines terminate as soon as they complete to configure the peripheral. When the data transmission ends, a subsequent interrupt will signal the main code about this. This mode is more suitable when communication speed is low (below 38400 Bps) or when it happens “rarely”, compared to other activities performed by the MCU, and we do not want to stick it waiting for data transmission.
- DMA mode offers the best data transmission throughput, thanks to the direct access of the UART peripheral to MCU internal RAM. This mode is best for high-speed communications and</pre></td>
<td><pre>![Image from PDF page 218](../images/page-0218-image-01.jpeg)

图 8.5：可以使用 CubeMX 轻松配置 UART2 接口

## 8.3 轮询模式下的 UART 通信

STM32 微控制器，因此 CubeHAL 也提供了三种通过 UART 通信在对等节点之间交换数据的方式：轮询（polling）、中断（interrupt）和直接存储器访问（direct memory access，DMA）模式。现在就有必要强调，这些模式不仅仅是处理 UART 通信的三种不同变体。它们是完成同一任务的三种不同编程方法，从设计和性能角度来看都带来了多种好处。让我们简要介绍它们。

- 在轮询模式（也称为阻塞模式）中，主应用程序或其线程之一会同步等待数据传输和接收。这是使用此外设进行数据通信的最简单形式，当传输速率不是太低，且 UART 未作为我们应用程序中的关键外设使用时（经典示例是将 UART 用作调试活动的输出控制台），可以使用此模式。
- 在中断模式（也称为非阻塞模式）中，主应用程序无需等待数据传输和接收完成即可释放。数据传输例程在完成外设配置后立即终止。当数据传输结束时，随后的中断将向主代码发出信号。当通信速度较低（低于 38400 Bps）或与其他微控制器执行的活动相比“很少”发生时，且我们不希望微控制器卡在等待数据传输上时，此模式更为适用。
- DMA 模式提供了最佳的数据传输吞吐量，这得益于 UART 外设对微控制器内部 RAM 的直接访问。此模式最适合高速通信，并且</pre></td>
</tr></tbody></table>

## PDF page 230 — Chapter 8: Universal Asynchronous Serial Communications

Focus: `numbers=0, 033, 1, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 3, 30, 5, 77, 78, 79, 80; negation=without; conditions=if; identifiers=HAL_OK, HAL_UART_Transmit_IT, HAL_UART_TxCpltCallback, MAIN_MENU, RING_BUFFER_OK, RingBuffer_GetDataLength, RingBuffer_Read, RingBuffer_Write, UART_Transmit, WELCOME_MSG, printWelcomeMessage, processUserInput, sprintf`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>## the scope of this book.

## Using a circular buffer, we can define a new UART transmit function in the following way:

```text
Filename: src/main-ex3.c
77
uint8_t UART_Transmit(UART_HandleTypeDef *huart, uint8_t *pData, uint16_t len) {
78
if(HAL_UART_Transmit_IT(huart, pData, len) != HAL_OK) {
79
if(RingBuffer_Write(&amp;txBuf, pData, len) != RING_BUFFER_OK)
80
return 0;
81
}
82
return 1;
83
}
```

## The function does just two things: it tries to send the buffer over the UART in interrupt mode; if the HAL_UART_Transmit_IT() function fails (which means that the UART is already transmitting another message), then the byte sequence is placed inside a circular buffer. It is up to the HAL_UART_TxCpltCallback() to check for pending bytes inside the circular buffer:

```text
Filename: src/main-ex3.c
94
void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart) {
95
if(RingBuffer_GetDataLength(&amp;txBuf) &gt; 0) {
96
RingBuffer_Read(&amp;txBuf, &amp;txData, 1);
97
HAL_UART_Transmit_IT(huart, &amp;txData, 1);
98
}
99
}
```

## The printWelcomeMessage() and processUserInput() functions can be now arranged without performing the busy-wait, as shown below:

```text
Filename: src/main-ex3.c
105
void printWelcomeMessage(void) {
106
char *strings[] = {&quot;\033[0;0H&quot;, &quot;\033[2J&quot;, WELCOME_MSG, MAIN_MENU, PROMPT};
107
108
for (uint8_t i = 0; i &lt; 5; i++)
109
UART_Transmit(&amp;huart2, (uint8_t*)strings[i], strlen(strings[i]));
110
}
111
112
uint8_t processUserInput(uint8_t opt) {
113
char msg[30];
114
115
if(!opt || opt &gt; 3)
116
return 0;
117
118
sprintf(msg, &quot;%d&quot;, opt);
119
UART_Transmit(&amp;huart2, (uint8_t*)msg, strlen(msg));
```</pre></td>
<td><pre>## 本书的范围。

## 使用环形缓冲区，我们可以按以下方式定义一个新的 UART 发送函数：

```text
Filename: src/main-ex3.c
77
uint8_t UART_Transmit(UART_HandleTypeDef *huart, uint8_t *pData, uint16_t len) {
78
if(HAL_UART_Transmit_IT(huart, pData, len) != HAL_OK) {
79
if(RingBuffer_Write(&amp;txBuf, pData, len) != RING_BUFFER_OK)
80
return 0;
81
}
82
return 1;
83
}
```

## 该函数仅执行两项操作：它尝试以中断模式通过 UART 发送缓冲区；如果 HAL_UART_Transmit_IT() 函数失败（这意味着 UART 正在发送另一条消息），则字节序列会被放入环形缓冲区中。由 HAL_UART_TxCpltCallback() 负责检查环形缓冲区中是否有待发送的字节：

```text
Filename: src/main-ex3.c
94
void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart) {
95
if(RingBuffer_GetDataLength(&amp;txBuf) &gt; 0) {
96
RingBuffer_Read(&amp;txBuf, &amp;txData, 1);
97
HAL_UART_Transmit_IT(huart, &amp;txData, 1);
98
}
99
}
```

## printWelcomeMessage() 和 processUserInput() 函数现在可以安排为不执行忙等待（busy-wait），如下所示：

```text
Filename: src/main-ex3.c
105
void printWelcomeMessage(void) {
106
char *strings[] = {&quot;\033[0;0H&quot;, &quot;\033[2J&quot;, WELCOME_MSG, MAIN_MENU, PROMPT};
107
108
for (uint8_t i = 0; i &lt; 5; i++)
109
UART_Transmit(&amp;huart2, (uint8_t*)strings[i], strlen(strings[i]));
110
}
111
112
uint8_t processUserInput(uint8_t opt) {
113
char msg[30];
114
115
if(!opt || opt &gt; 3)
116
return 0;
117
118
sprintf(msg, &quot;%d&quot;, opt);
119
UART_Transmit(&amp;huart2, (uint8_t*)msg, strlen(msg));
```</pre></td>
</tr></tbody></table>

## PDF page 247 — Chapter 9: DMA Management

Focus: `numbers=01, 0247, 2.3, 247, 9.1, 9.6; negation=not; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>![Image from PDF page 247](../images/page-0247-image-01.jpeg)

Figure 9.6: The multi-layer BusMatrix in an STM32F405 MCU

#### 9.1.2.3 The DMA Implementation in G0/G4/L4+/L5/H7 MCUs

The DMA controller architecture in STM32G0/G4/L4+/L5/H7 MCUs is similar to the one in STM32F0/F1/F3/L0/L1/L4 families, but it is enhanced by a DMA request Multiplexer (DMAMUX) unit. DMAMUX adds a fully configurable routing of any DMA request from a given peripheral in DMA mode to any DMA channel of the two DMA controllers. This means that the peripheral requests bound to a given channel are not defined by design, giving to both programmers and hardware developers the maximum flexibility during design phase. DMAMUX does not add any clock cycle between the DMA request sent by the peripheral and the DMA request received by the configured DMA channel. It features synchronization of DMA requests using dedicated inputs. DMAMUX is also capable of generating requests from own trigger inputs or by software.</pre></td>
<td><pre>![Image from PDF page 247](../images/page-0247-image-01.jpeg)

图 9.6：STM32F405 微控制器中的多层 BusMatrix

#### 9.1.2.3 G0/G4/L4+/L5/H7 微控制器中的 DMA 实现

STM32G0/G4/L4+/L5/H7 微控制器中的 DMA 控制器架构与 STM32F0/F1/F3/L0/L1/L4 系列中的架构相似，但通过 DMA 请求复用器（DMAMUX）单元进行了增强。DMAMUX 为来自给定外设的任何 DMA 请求（在 DMA 模式下）到两个 DMA 控制器中任何 DMA 通道的完全可配置路由。这意味着绑定到给定通道的外设请求不是由设计定义的，从而为程序员和硬件开发者在设计阶段提供了最大的灵活性。DMAMUX 不会在外设发送的 DMA 请求和配置的 DMA 通道接收的 DMA 请求之间增加任何时钟周期。它使用专用输入来同步 DMA 请求。DMAMUX 还能够从自身的触发输入或由软件生成请求。</pre></td>
</tr></tbody></table>

## PDF page 263 — Chapter 9: DMA Management

Focus: `numbers=0, 1, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 6, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71; negation=Disable; conditions=if; identifiers=DMA_MDATAALIGN_BYTE, DMA_MEMORY_TO_PERIPH, DMA_MINC_ENABLE, DMA_NORMAL, DMA_PDATAALIGN_BYTE, DMA_PINC_DISABLE, DMA_PRIORITY_LOW, GPIO_PIN_SET, HAL_DMA_Init, HAL_DMA_Start_IT, HAL_GPIO_WritePin, HAL_NVIC_EnableIRQ, HAL_NVIC_SetPriority, HAL_UART, USART_CR3_DMAT`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>```text
Filename: Core/Src/main-ex2.c
50
hdma_usart2_tx.Instance = DMA1_Channel4;
51
hdma_usart2_tx.Init.Direction = DMA_MEMORY_TO_PERIPH;
52
hdma_usart2_tx.Init.PeriphInc = DMA_PINC_DISABLE;
53
hdma_usart2_tx.Init.MemInc = DMA_MINC_ENABLE;
54
hdma_usart2_tx.Init.PeriphDataAlignment = DMA_PDATAALIGN_BYTE;
55
hdma_usart2_tx.Init.MemDataAlignment = DMA_MDATAALIGN_BYTE;
56
hdma_usart2_tx.Init.Mode = DMA_NORMAL;
57
hdma_usart2_tx.Init.Priority = DMA_PRIORITY_LOW;
58
hdma_usart2_tx.XferCpltCallback = &amp;DMATransferComplete;
59
HAL_DMA_Init(&amp;hdma_usart2_tx);
```

60

```text
61
/* DMA interrupt init */
62
HAL_NVIC_SetPriority(DMA1_Channel4_5_IRQn, 0, 0);
63
HAL_NVIC_EnableIRQ(DMA1_Channel4_5_IRQn);
```

64

```text
65
HAL_DMA_Start_IT(&amp;hdma_usart2_tx,
(uint32_t)msg,
66
(uint32_t)&amp;huart2.Instance-&gt;TDR, strlen(msg));
```

67

```text
68
//Enable UART in DMA mode
69
huart2.Instance-&gt;CR3 |= USART_CR3_DMAT;
```

70

```text
71
/* Infinite loop */
72
while (1);
73
}
```

74

```text
75
void DMATransferComplete(DMA_HandleTypeDef *hdma) {
76
if(hdma-&gt;Instance == DMA1_Channel4) {
77
//Disable UART DMA mode
78
huart2.Instance-&gt;CR3 &amp;= ~USART_CR3_DMAT;
79
//Turn LD2 ON
80
HAL_GPIO_WritePin(LD2_GPIO_Port, LD2_Pin, GPIO_PIN_SET);
81
}
82
}
```

### 9.2.6 Using the HAL_UART Module with DMA Mode Transfers

## In Chapter 8 we left out how to use the UART in DMA mode. We have already seen in the previous paragraphs how to do it. However, we had to play with some USART registers to enable the peripheral in DMA mode.

## The HAL_UART module is designed to abstract from all underlying hardware details. The steps required to use it are the following:

## - configure the DMA channel/stream hardwired to the UART you are going to use, as seen in this chapter;</pre></td>
<td><pre>```text
Filename: Core/Src/main-ex2.c
50
hdma_usart2_tx.Instance = DMA1_Channel4;
51
hdma_usart2_tx.Init.Direction = DMA_MEMORY_TO_PERIPH;
52
hdma_usart2_tx.Init.PeriphInc = DMA_PINC_DISABLE;
53
hdma_usart2_tx.Init.MemInc = DMA_MINC_ENABLE;
54
hdma_usart2_tx.Init.PeriphDataAlignment = DMA_PDATAALIGN_BYTE;
55
hdma_usart2_tx.Init.MemDataAlignment = DMA_MDATAALIGN_BYTE;
56
hdma_usart2_tx.Init.Mode = DMA_NORMAL;
57
hdma_usart2_tx.Init.Priority = DMA_PRIORITY_LOW;
58
hdma_usart2_tx.XferCpltCallback = &amp;DMATransferComplete;
59
HAL_DMA_Init(&amp;hdma_usart2_tx);
```

60

```text
61
/* DMA interrupt init */
62
HAL_NVIC_SetPriority(DMA1_Channel4_5_IRQn, 0, 0);
63
HAL_NVIC_EnableIRQ(DMA1_Channel4_5_IRQn);
```

64

```text
65
HAL_DMA_Start_IT(&amp;hdma_usart2_tx,
(uint32_t)msg,
66
(uint32_t)&amp;huart2.Instance-&gt;TDR, strlen(msg));
```

67

```text
68
//Enable UART in DMA mode
69
huart2.Instance-&gt;CR3 |= USART_CR3_DMAT;
```

70

```text
71
/* Infinite loop */
72
while (1);
73
}
```

74

```text
75
void DMATransferComplete(DMA_HandleTypeDef *hdma) {
76
if(hdma-&gt;Instance == DMA1_Channel4) {
77
//Disable UART DMA mode
78
huart2.Instance-&gt;CR3 &amp;= ~USART_CR3_DMAT;
79
//Turn LD2 ON
80
HAL_GPIO_WritePin(LD2_GPIO_Port, LD2_Pin, GPIO_PIN_SET);
81
}
82
}
```

### 9.2.6 使用 HAL_UART 模块进行 DMA 模式传输

## 在第 8 章中，我们遗漏了如何以 DMA 模式使用 UART。我们在前面的段落中已经看到了如何做到这一点。然而，我们必须操作一些 USART 寄存器来启用外设的 DMA 模式。

## HAL_UART 模块旨在抽象所有底层硬件细节。使用它所需的步骤如下：

## - 配置硬连线到您将要使用的 UART 的 DMA 通道/流，如本章所述；</pre></td>
</tr></tbody></table>

## PDF page 280 — Chapter 10: Clock Tree

Focus: `numbers=0, 01, 0280, 1, 1.1, 10.1, 10.2, 100kHz, 16MHz, 25, 280, 3, 48MHz, 4MHz, 85, 8MHz; negation=without; conditions=If, if; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>(a wrong clock configuration could lead to abnormal behavior, strange and unpredictable resets and so on). Luckily for us, the STM32 engineers have provided a great tool to simplify the clock configuration: CubeMX.

#### 10.1.1.1 The Multispeed Internal RC Oscillator in STM32L/U Families

The clock source and its distribution network have a non-negligible impact on the overall power consumption of the MCU. If we need a SYSCLK frequency higher or lower than the internal HSI clock source (which is 8MHz for the most of STM32 MCUs and 16MHz for some others), we have to increase/reduce it by using the PLL Source Mux and intermediate prescalers. Unfortunately, these components consume energy, and this can have a dramatic impact on battery-powered devices.

![Image from PDF page 280](../images/page-0280-image-01.png)

Table 10.2: A comparison between clock sources in an STM32L476 MCU

STM32L/U MCUs are explicitly designed for low-power applications, and they address this specific issue by supplying a dedicated internal clock source, named MultiSpeed Internal (MSI) RC oscillator. MSI is a low-power RC oscillator, with a ±1%@25°C factory pre-calibrated accuracy, which can increase up to ±3% in the 0-85°C range. The main characteristic of the MSI is that it supplies up to twelve different frequencies, without adding any external component. For example, the MSI in an STM32L476 provides an internal clock source ranging from 100kHz up to 48MHz. The MSI clock is used as SYSCLK after restart from Reset, wakeup from Standby and Shutdown low-power modes. After restart from Reset, the MSI frequency is set to its default (for example, the default MSI frequency in an STM32L476 is 4MHz). Table 10.2 summarizes the most relevant characteristics of all possible clock sources in an STM32L476 MCU. As you can see, the best power consumption is achieved while the MCU is clocked by the MSI (without using the PLL Multiplexer). Moreover, this clock source guarantees the shortest startup time, if compared with the HSI. It is interesting to see that up to two seconds are required to stabilize the LSE clock: if startup speed is really important for your application, then using a separated thread¹³ to start the LSE is an option to consider.

¹³This clearly implies the usage of an RTOS. We will study this matter in a later chapter.</pre></td>
<td><pre>（错误的时钟配置可能导致异常行为、奇怪且不可预测的重置等）。幸运的是，STM32 工程师提供了一个简化工具来简化时钟配置：CubeMX。

#### 10.1.1.1 STM32L/U 系列中的多速度内部 RC 振荡器

时钟源及其分配网络对 MCU 的整体功耗有不可忽略的影响。如果我们需要的 SYSCLK 频率高于或低于内部 HSI 时钟源（对于大多数 STM32 MCU 为 8MHz，对于某些其他型号为 16MHz），我们必须使用 PLL 源复用器和中间预分频器来增加/减少它。不幸的是，这些组件消耗能量，这对电池供电设备可能产生巨大影响。

![Image from PDF page 280](../images/page-0280-image-01.png)

表 10.2：STM32L476 MCU 中时钟源的比较

STM32L/U MCU 明确针对低功耗应用设计，并通过提供一个专用的内部时钟源来解决这一特定问题，该源名为多速度内部（MSI）RC 振荡器。MSI 是一个低功耗 RC 振荡器，具有 ±1%@25°C 的工厂预校准精度，在 0-85°C 范围内可能增加到 ±3%。MSI 的主要特点是它提供多达十二种不同的频率，而无需添加任何外部组件。例如，STM32L476 中的 MSI 提供从 100kHz 到 48MHz 的内部时钟源。MSI 时钟在从复位重启、从待机模式和关机低功耗模式唤醒后用作 SYSCLK。从复位重启后，MSI 频率设置为其默认值（例如，STM32L476 中的默认 MSI 频率为 4MHz）。表 10.2 总结了 STM32L476 MCU 中所有可能时钟源的最相关特性。如您所见，当 MCU 由 MSI 时钟驱动时（不使用 PLL 复用器），可实现最佳的功耗。此外，与 HSI 相比，该时钟源保证了最短的启动时间。有趣的是，稳定 LSE 时钟最多需要两秒钟：如果启动速度对您的应用确实很重要，那么使用一个单独的线程¹³来启动 LSE 是一个值得考虑的选项。

¹³这显然意味着使用 RTOS。我们将在后面的章节中研究这个问题。</pre></td>
</tr></tbody></table>

## PDF page 284 — Chapter 10: Clock Tree

Focus: `numbers=01, 02, 03, 1, 10.1, 29, 3.1, 64, 8; negation=cannot, not; conditions=; identifiers=OSC_IN`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>#### 10.1.3.1 Clock Source in Nucleo-64 rev. MB1136 (older ones with ST-LINK V2.1)

##### 10.1.3.1.1 OSC Clock Supply

There are four ways to configure the pins corresponding to external high-speed clock external highspeed clock (HSE):

- MCO from ST-LINK: MCO output of ST-LINK MCU is used as input clock. This frequency cannot be changed, it is fixed at 8 MHz and connected to PF0/PD0/PH0-OSC_IN of target STM32 MCU. The following configuration is needed:

- – SB55 OFF – SB16 and SB50 ON – R35 and R37 removed
- HSE oscillator on-board from X3 crystal (not provided): for typical frequencies and its capacitors and resistors, refer to STM32 microcontroller datasheet. Please refer to the AN2867 for oscillator design guide for STM32 microcontrollers. The following configuration is needed:

- – SB54 and SB55 OFF – R35 and R37 soldered – C33 and C34 soldered – SB16 and SB50 OFF
- Oscillator from external PF0/PD0/PH0: from an external oscillator through pin 29 of the CN7 connector. The following configuration is needed:

- – SB55 ON – SB50 OFF – R35 and R37 removed
- HSE not used: PF0/PD0/PH1 and PF1/PD1/PH1 are used as GPIO instead of Clock The following configuration is needed:

– SB54 and SB55 ON – SB16 and SB50 (MCO) OFF – R35 and R37 removed

There are two possible default configurations of the HSE pins depending on the version of NUCLEO board hardware. The board version MB1136 C-01/02/03 is mentioned on sticker placed on bottom side of the PCB.

- The board marking MB1136 C-01 corresponds to a board, configured for HSE not used.
- The board marking MB1136 C-02 (or higher) corresponds to a board, configured to use STLINK MCO as clock input.</pre></td>
<td><pre>#### 10.1.3.1 Nucleo-64 rev. MB1136（旧版，配备 ST-LINK V2.1）的时钟源

##### 10.1.3.1.1 OSC 时钟供电

配置对应外部高速时钟 external highspeed clock (HSE) 的引脚有四种方式：

- 来自 ST-LINK 的 MCO：使用 ST-LINK 微控制器的 MCO 输出作为输入时钟。该频率不可更改，固定为 8 MHz，并连接到目标 STM32 微控制器的 PF0/PD0/PH0-OSC_IN。需要以下配置：

- – SB55 OFF – SB16 和 SB50 ON – 移除 R35 和 R37
- 板载 HSE 振荡器，来自 X3 晶振（未提供）：关于典型频率及其电容和电阻，请参阅 STM32 微控制器数据手册。关于 STM32 微控制器的振荡器设计指南，请参阅 AN2867。需要以下配置：

- – SB54 和 SB55 OFF – 焊接 R35 和 R37 – 焊接 C33 和 C34 – SB16 和 SB50 OFF
- 来自外部 PF0/PD0/PH0 的振荡器：通过 CN7 连接器的第 29 引脚从外部振荡器引入。需要以下配置：

- – SB55 ON – SB50 OFF – 移除 R35 和 R37
- 未使用 HSE：PF0/PD0/PH1 和 PF1/PD1/PH1 用作 GPIO，而非时钟。需要以下配置：

– SB54 和 SB55 ON – SB16 和 SB50 (MCO) OFF – 移除 R35 和 R37

根据 NUCLEO 板硬件版本的不同，HSE 引脚有两种可能的默认配置。PCB 底部贴纸上标有板版本 MB1136 C-01/02/03。

- 板标记 MB1136 C-01 对应配置为未使用 HSE 的板。
- 板标记 MB1136 C-02（或更高版本）对应配置为使用 STLINK MCO 作为时钟输入的板。</pre></td>
</tr></tbody></table>

## PDF page 339 — Chapter 11: Timers

Focus: `numbers=1, 11.19, 11.20, 11.21, 2; negation=no, not; conditions=otherwise, when; identifiers=TIM_OCFAST_DISABLE, TIM_OCFAST_ENABLE, TIM_OCIDLESTATE_RESET, TIM_OCIDLESTATE_SET, TIM_OCMODE_ACTIVE, TIM_OCMODE_FORCED_ACTIVE, TIM_OCMODE_FORCED_INACTIVE, TIM_OCMODE_INACTIVE, TIM_OCMODE_PWM1, TIM_OCMODE_PWM2, TIM_OCMODE_TIMING, TIM_OCMODE_TOGGLE, TIM_OCNIDLESTATE_RESET, TIM_OCNIDLESTATE_SET`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>```text
typedef struct {
uint32_t OCMode;
/* Specifies the TIM mode. */
uint32_t Pulse;
/* Specifies the pulse value to be loaded
into the Capture Compare Register. */
uint32_t OCPolarity;
/* Specifies the output polarity. */
uint32_t OCNPolarity;
/* Specifies the complementary output polarity.*/
uint32_t OCFastMode;
/* Specifies the Fast mode state. */
uint32_t OCIdleState;
/* Specifies the TIM Output Compare pin state during Idle state.*/
uint32_t OCNIdleState; /* Specifies the complementary
TIM Output Compare pin
state during Idle state. */
} TIM_OC_InitTypeDef;
```

- OCMode: specifies the output compare mode and it can assume a value from Table 11.19.
- Pulse: the content of this field will be stored inside the CCRx register and it establishes when to trigger the output. Please, ensure that the timer period is set to a multiple of the Pulse field, otherwise be prepared to handle the reminder of integer division accordingly.
- OCPolarity: defines the output channel polarity when the CCRx registers matches with the CNT one. It can assume a value from Table 11.20.
- OCNPolarity: defines the complimentary output polarity. It is a mode available only in TIM1 and TIM8 advanced timers, which allow to generate, on additional dedicated channels, complimentary signals (that is, when the CH1 is HIGH the CH1n is LOW and vice versa). This feature is especially designed for motor control applications, and it is not described in this book. It can assume a value from Table 11.21.
- OCFastMode: specifies the fast mode state. This parameter is valid only in PWM1 and PWM2 mode and it can assume the values TIM_OCFAST_DISABLE and TIM_OCFAST_ENABLE.
- OCIdleState: specifies the channel output compare pin state during the timer idle state. It can assume the values TIM_OCIDLESTATE_SET and TIM_OCIDLESTATE_RESET. This parameter is available only in TIM1 and TIM8 advanced timers.
- OCNIdleState: specifies the complementary channel output compare pin state during the timer idle state. It can assume the values TIM_OCNIDLESTATE_SET and TIM_OCNIDLESTATE_RESET. This parameter is available only in TIM1 and TIM8 advanced timers.

Table 11.19: Available output compare modes

Output compare mode Description

TIM_OCMODE_TIMING The comparison between the output compare register (CCRx) and the counter (CNT) has no effect on the output (aka, frozen mode) TIM_OCMODE_ACTIVE Set the channel output to active level on match TIM_OCMODE_INACTIVE Set channel to inactive level on match TIM_OCMODE_TOGGLE The channel output toggles when the counter (CNT) matches the capture/compare register (CCRx) TIM_OCMODE_PWM1 PWM Mode 1 - see next paragraph TIM_OCMODE_PWM2 PWM Mode 2 - see next paragraph TIM_OCMODE_FORCED_ACTIVE The channel output is forced high independently from the counter value TIM_OCMODE_FORCED_INACTIVE The channel output is forced low independently from the counter value</pre></td>
<td><pre>```text
typedef struct {
uint32_t OCMode;
/* Specifies the TIM mode. */
uint32_t Pulse;
/* Specifies the pulse value to be loaded
into the Capture Compare Register. */
uint32_t OCPolarity;
/* Specifies the output polarity. */
uint32_t OCNPolarity;
/* Specifies the complementary output polarity.*/
uint32_t OCFastMode;
/* Specifies the Fast mode state. */
uint32_t OCIdleState;
/* Specifies the TIM Output Compare pin state during Idle state.*/
uint32_t OCNIdleState; /* Specifies the complementary
TIM Output Compare pin
state during Idle state. */
} TIM_OC_InitTypeDef;
```

- OCMode：指定输出比较模式，其值可取自表 11.19。
- Pulse：该字段的内容将存储在 CCRx 寄存器中，并确定何时触发输出。请确保定时器周期设置为 Pulse 字段的倍数，否则请准备好相应处理整数除法的余数。
- OCPolarity：定义当 CCRx 寄存器与 CNT 寄存器匹配时的输出通道极性。其值可取自表 11.20。
- OCNPolarity：定义互补输出极性。这是仅在 TIM1 和 TIM8 高级定时器中可用的模式，允许在额外的专用通道上生成互补信号（即当 CH1 为高电平时 CH1n 为低电平，反之亦然）。此功能特别针对电机控制应用设计，本书中不予详细描述。其值可取自表 11.21。
- OCFastMode：指定快速模式状态。此参数仅在 PWM1 和 PWM2 模式下有效，可取值为 TIM_OCFAST_DISABLE 和 TIM_OCFAST_ENABLE。
- OCIdleState：指定定时器空闲状态期间通道输出比较引脚的状态。可取值为 TIM_OCIDLESTATE_SET 和 TIM_OCIDLESTATE_RESET。此参数仅在 TIM1 和 TIM8 高级定时器中可用。
- OCNIdleState：指定定时器空闲状态期间互补通道输出比较引脚的状态。可取值为 TIM_OCNIDLESTATE_SET 和 TIM_OCNIDLESTATE_RESET。此参数仅在 TIM1 和 TIM8 高级定时器中可用。

表 11.19：可用的输出比较模式

输出比较模式 描述

TIM_OCMODE_TIMING 输出比较寄存器（CCRx）与计数器（CNT）之间的比较对输出没有影响（又称冻结模式） TIM_OCMODE_ACTIVE 匹配时将通道输出设置为激活电平 TIM_OCMODE_INACTIVE 匹配时将通道设置为非激活电平 TIM_OCMODE_TOGGLE 当计数器（CNT）与捕获/比较寄存器（CCRx）匹配时，通道输出发生翻转 TIM_OCMODE_PWM1 PWM 模式 1 - 见下一段 TIM_OCMODE_PWM2 PWM 模式 2 - 见下一段 TIM_OCMODE_FORCED_ACTIVE 无论计数器值如何，通道输出被强制置高 TIM_OCMODE_FORCED_INACTIVE 无论计数器值如何，通道输出被强制置低</pre></td>
</tr></tbody></table>

## PDF page 348 — Chapter 11: Timers

Focus: `numbers=01, 02, 0348, 1, 10, 103, 11.26, 11.27, 15, 3, 348, 4.3, 5, 9; negation=; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>The cut-off frequency (fc) of a first order RC low-pass filter is expressed by the formula:

fc = 1 2πRC [9]

Figure 11.26 shows the effect of a low-pass filter on a PWM signal with a frequency of 100Hz. Here we have chosen a 1K resistor and a 10µF capacitor. This means that the cut-off frequency is equal to:

fc = 1 2π103 × 10−5 ≈15.9Hz

![Image from PDF page 348](../images/page-0348-image-01.jpeg)

Figure 11.26: The effect of a low-pass filter with cut-off frequency equal to 15.9Hz

Figure 11.27 shows the effect of the low-pass filter with a 4300K resistor and a 10µF capacitor. This means that the cut-off frequency is equal to:

fc = 1 2π(4.3 × 103) × 10−5 ≈3.7Hz

As you can see, the second filter allows to have a (Vpp) equal to about 160mV, which is a voltage difference passable for a lot of applications.

![Image from PDF page 348](../images/page-0348-image-02.jpeg)

Figure 11.27: The effect of a low-pass filter with cut-off frequency equal to 3.7Hz

By varying the output voltage (which implies that we vary the duty cycle) we can generate an arbitrary output waveform, whose frequency is a fraction of the PWM period. The basic idea here</pre></td>
<td><pre>一阶 RC 低通滤波器的截止频率 (fc) 由以下公式表示：

fc = 1 2πRC [9]

图 11.26 展示了低通滤波器对频率为 100Hz 的 PWM 信号的影响。在这里，我们选择了 1K 电阻和 10µF 电容。这意味着截止频率等于：

fc = 1 2π103 × 10−5 ≈15.9Hz

![Image from PDF page 348](../images/page-0348-image-01.jpeg)

图 11.26：截止频率等于 15.9Hz 的低通滤波器的影响

图 11.27 展示了使用 4300K 电阻和 10µF 电容的低通滤波器的影响。这意味着截止频率等于：

fc = 1 2π(4.3 × 103) × 10−5 ≈3.7Hz

如你所见，第二个滤波器允许 Vpp 约为 160mV，这对于许多应用来说是一个可以接受的电压差。

![Image from PDF page 348](../images/page-0348-image-02.jpeg)

图 11.27：截止频率等于 3.7Hz 的低通滤波器的影响

通过改变输出电压（这意味着我们改变占空比），我们可以生成任意的输出波形，其频率是 PWM 周期的一部分。这里的基本思想</pre></td>
</tr></tbody></table>

## PDF page 373 — Chapter 12: Analog-To-Digital Conversion

Focus: `numbers=12, 12.1, 16; negation=not; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre># 12. Analog-To-Digital Conversion

It is quite common to interface analog peripherals to a microcontroller. In the digital era, there are still a lot of devices that produce analog signals: sensors, potentiometers, transducers and audio peripherals are just few examples of analog devices that generate a variable voltage, which usually ranges in a fixed interval. By reading this voltage, we can convert it in a numerical entity useful to be processed by our firmware. For example, the TMP36 is a quite-popular temperature sensor, which produces a variable voltage proportional to the circuit operating voltage (it is said to give a ratiometric output) and the ambient temperature.

All STM32 microcontrollers provide at least one Analog-to-Digital Converter (ADC), a peripheral able to acquire several input voltages through dedicated I/O, and to convert them to a number. The input voltage is compared against a well know and fixed voltage, also known as reference voltage. This reference voltage can be either derived from the VDDA domain or, in MCUs with high pin count, supplied by an external and fixed reference voltage generator (those MCUs provide a dedicated pin named VREF+). The majority of STM32 MCUs provide a 12-bit ADC. Some of them from the STM32F3 and STM32H7 portfolio even a 16-bit ADC.

Differently from other STM32 peripherals seen so far, ADCs can diverge a lot between the various STM32-series and even inside a given family. For this reason, will give only an introduction to this useful peripheral, leaving to the reader the responsibility to analyze in depth the ADC in the specific MCU he is considering.

Before we analyze the features offered by the ADC in an STM32 microcontroller, and the related CubeHAL, it is best to give a quick introduction to the way this peripheral works.

## 12.1 Introduction to SAR ADC

In almost all STM32 microcontrollers, the ADC is implemented as a 12-bit Successive Approximation Register ADC¹. Depending on the sales type and packaged used, it can have a variable number of multiplexed input channels (usually more than ten channels in the most of STM32 MCUs with high pin count), allowing to measure signals from external sources. Moreover, some internal channels are also available: a channel for internal temperature sensor (VSENSE), one for internal reference voltage (VREF INT), one for monitoring external VBAT power supply and a channel for monitoring LCD voltage in those MCUs providing a native monochrome passive LCD controller (for example, the STM32L053 is one of these). ADCs implemented in more recent STM32 families (STM32F3/L4/L4+/L5/G0/G5/H7) are also capable of converting fully differential inputs. Table 12.1

¹At the time of writing this chapter, the ADC provided by STM32F37/38xx and STM32H7 series is the only notably exception to this rule, since they provide a more accurate 16-bit ADC with Sigma-Delta(Σ-Δ) modulator. This type of ADC will not be covered in this book. ST provides the AN4207 to cover this topic. However, the HAL routines to use it have the same organization.</pre></td>
<td><pre># 12. 模数转换

将模拟外设连接到微控制器（microcontroller）是非常常见的做法。在数字时代，仍然有许多设备产生模拟信号：传感器、电位器、换能器和音频外设只是生成可变电压的模拟设备的少数几个例子，这些电压通常在一个固定的区间内变化。通过读取该电压，我们可以将其转换为一个数值实体，以便我们的固件进行处理。例如，TMP36 是一种相当流行的温度传感器，它产生一个与电路工作电压（据称提供比率输出）和环境温度成比例的变电压。

所有 STM32 微控制器都至少提供一个模数转换器（Analog-to-Digital Converter, ADC），这是一种能够通过专用 I/O 获取多个输入电压并将其转换为数字的外设。输入电压会与一个众所周知的固定电压进行比较，该电压也称为参考电压。此参考电压可以源自 VDDA 域，或者在引脚数较多的 MCU 中，由外部固定参考电压发生器提供（这些 MCU 提供了一个名为 VREF+ 的专用引脚）。大多数 STM32 MCU 提供 12 位 ADC。其中一些来自 STM32F3 和 STM32H7 产品组合的 MCU 甚至提供 16 位 ADC。

与迄今为止看到的其他 STM32 外设不同，ADC 在不同的 STM32 系列之间，甚至在同一系列内部都可能存在很大差异。因此，我们将仅对此有用外设进行介绍，并留给读者责任去深入分析其正在考虑的具体 MCU 中的 ADC。

在分析 STM32 微控制器中 ADC 提供的功能及相关 CubeHAL 之前，最好先简要介绍该外设的工作方式。

## 12.1 SAR ADC 简介

在几乎所有 STM32 微控制器中，ADC 都实现为 12 位逐次逼近寄存器（Successive Approximation Register, SAR）ADC¹。根据销售类型和使用的封装，它可以具有可变数量的多路复用输入通道（在大多数高引脚数的 STM32 MCU 中通常超过十个通道），从而允许测量来自外部源的信号。此外，还提供了一些内部通道：一个用于内部温度传感器（VSENSE）的通道，一个用于内部参考电压（VREF INT）的通道，一个用于监控外部 VBAT 电源的通道，以及一个用于监控 LCD 电压的通道（在那些提供原生单色被动 LCD 控制器的 MCU 中，例如 STM32L053 就是其中之一）。在较新的 STM32 系列（STM32F3/L4/L4+/L5/G0/G5/H7）中实现的 ADC 还能够转换全差分输入。表 12.1

¹在撰写本章时，STM32F37/38xx 和 STM32H7 系列提供的 ADC 是这一规则的唯一显著例外，因为它们提供了更精确的带有 Sigma-Delta(Σ-Δ) 调制器的 16 位 ADC。本书不会涵盖这种类型的 ADC。ST 提供了 AN4207 来涵盖此主题。然而，使用它的 HAL 例程具有相同的组织结构。</pre></td>
</tr></tbody></table>

## PDF page 379 — Chapter 12: Analog-To-Digital Conversion

Focus: `numbers=12.2, 2, 4, 6, 8; negation=not; conditions=; identifiers=__HAL_LINKDMA`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>## - DMA_Handle: this is the pointer to the DMA handler configured to perform A/D conversion in DMA mode. It is automatically configured by the __HAL_LINKDMA() macro.

## ADC configuration is performed by using an instance of the C struct ADC_InitTypeDef, which is defined in the following way⁵:

```text
typedef struct {
uint32_t ClockPrescaler;
/* Selects the ADC clock frequency */
uint32_t Resolution;
/* Configures the ADC resolution mode */
uint32_t ScanConvMode;
/* The scan sequence direction. */
uint32_t ContinuousConvMode;
/* Specifies whether the conversion is performed in
Continuous or Single mode */
uint32_t DataAlign;
/* Specifies whether the ADC data alignment
is left or right */
uint32_t NbrOfConversion;
/* Specifies the number of ranks that will be converted
within the regular group sequencer */
uint32_t NbrOfDiscConversion;
/* Specifies the number of discontinuous conversions in
which the
main sequence of regular group */
uint32_t DiscontinuousConvMode; /* Specifies whether the conversion sequence of regular
group is performed in Complete-sequence/Discontinuous
sequence */
uint32_t ExternalTrigConv;
/* Select the external event used to trigger the start
of conversion */
uint32_t ExternalTrigConvEdge;
/* Select the external trigger edge and enable it */
uint32_t DMAContinuousRequests; /* Specifies whether the DMA requests are performed in
one shot or in continuous mode */
uint32_t EOCSelection;
/* Specifies what EOC (End Of Conversion) flag is used
for conversion polling and interruption */
} ADC_InitTypeDef;
```

## Let us analyze the most relevant field of this struct.

## - ClockPrescaler: defines the speed of the clock (ADCCLK) for the analog circuitry part of ADC. In the previous paragraph we have seen that the ADC has an internal timing unit that controls the switching frequency of the input switch (see Figure 12.2). The ADCCLK establishes the speed of this timing unit, and it impacts on the number of samples per seconds, because it defines the amount of time used by each conversion cycle. This clock is generated from the peripheral clock divided by a programmable prescaler that allows the ADC to work at fP CLK/2,/4,/6 or /8 (refer to the datasheets of the specific MCU for the maximum values of ADCCLK and its prescaler). In some STM32 MCUs the ADCCLK can also be derived from the HSI oscillator. The value of this field affects the ADCCLK speed of all ADCs implemented in the MCU.

⁵The ADC_InitTypeDef struct slightly differs from the one defined in CubeF0 and CubeL0 HALs. This because the ADC in those families does not provide the ability to define custom input sampling sequences (by assigning rank values). Moreover, the ADC in those families provide the ability to perform oversampling of the input signal, and in CubeL0 HAL it is possible to enable dedicated low-power features offered by the ADC in those MCUs. For more information, refer to the CubeHAL source code.</pre></td>
<td><pre>## - DMA_Handle：这是指向配置为以直接存储器访问（DMA）模式执行 A/D 转换的 DMA 处理器的指针。它由 __HAL_LINKDMA() 宏自动配置。

## ADC 配置通过使用 C 结构体 ADC_InitTypeDef 的实例来完成，其定义方式如下⁵：

```text
typedef struct {
uint32_t ClockPrescaler;
/* Selects the ADC clock frequency */
uint32_t Resolution;
/* Configures the ADC resolution mode */
uint32_t ScanConvMode;
/* The scan sequence direction. */
uint32_t ContinuousConvMode;
/* Specifies whether the conversion is performed in
Continuous or Single mode */
uint32_t DataAlign;
/* Specifies whether the ADC data alignment
is left or right */
uint32_t NbrOfConversion;
/* Specifies the number of ranks that will be converted
within the regular group sequencer */
uint32_t NbrOfDiscConversion;
/* Specifies the number of discontinuous conversions in
which the
main sequence of regular group */
uint32_t DiscontinuousConvMode; /* Specifies whether the conversion sequence of regular
group is performed in Complete-sequence/Discontinuous
sequence */
uint32_t ExternalTrigConv;
/* Select the external event used to trigger the start
of conversion */
uint32_t ExternalTrigConvEdge;
/* Select the external trigger edge and enable it */
uint32_t DMAContinuousRequests; /* Specifies whether the DMA requests are performed in
one shot or in continuous mode */
uint32_t EOCSelection;
/* Specifies what EOC (End Of Conversion) flag is used
for conversion polling and interruption */
} ADC_InitTypeDef;
```

## 让我们分析该结构体中最相关的字段。

## - ClockPrescaler：定义 ADC 模拟电路部分时钟（ADCCLK）的速度。在前一段中，我们看到 ADC 有一个内部定时单元，用于控制输入开关的切换频率（参见图 12.2）。ADCCLK 确立了该定时单元的速度，并影响每秒的采样次数，因为它定义了每个转换周期所用的时间。该时钟由外设时钟经过可编程预分频器分频后生成，允许 ADC 以 fP CLK/2、/4、/6 或 /8 的频率工作（具体 MCU 的 ADCCLK 最大值及其预分频器请参考数据手册）。在某些 STM32 MCU 中，ADCCLK 也可以从 HSI 振荡器派生。该字段的值会影响 MCU 中所有实现的 ADC 的 ADCCLK 速度。

⁵ADC_InitTypeDef 结构体与 CubeF0 和 CubeL0 HAL 中定义的略有不同。这是因为这些系列的 ADC 不提供定义自定义输入采样序列（通过分配通道序号）的能力。此外，这些系列的 ADC 提供对输入信号进行过采样的能力，并且在 CubeL0 HAL 中，可以启用这些 MCU 中 ADC 提供的专用低功耗功能。更多信息，请参考 CubeHAL 源代码。</pre></td>
</tr></tbody></table>

## PDF page 395 — Chapter 12: Analog-To-Digital Conversion

Focus: `numbers=01, 0395, 12.2, 395, 6.1, 6.2, 6.3, 7; negation=DISABLE, not; conditions=If, Otherwise, When, otherwise, when; identifiers=ADC_SR, DMA_CIRCULAR, HAL_ADC_Start_DMA, HAL_ADC_Stop_DMA`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>For this reason, this and the next example will cycle on just one channel for the STM32L073RZ examples.

![Image from PDF page 395](../images/page-0395-image-01.png)

#### 12.2.6.1 Convert Multiple Times the Same Channel in DMA Mode

To perform a given number of conversions of the same channel (or the same channel sequence) in DMA mode, you need to do the following way:

- Set the hadc.Init.ContinuousConvMode field to ENABLE.
- Allocate a sufficient-sized buffer.
- Pass to the HAL_ADC_Start_DMA() the number of wanted acquisitions.

#### 12.2.6.2 Multiple and not Continuous Conversions in DMA Mode

To perform multiple conversions in DMA mode, you need to do the following steps:

```text
• Set the hadc.Init.DMAContinuousRequests field to ENABLE.
• Call the HAL_ADC_Start_DMA() to start conversions in DMA mode.
```

If, instead, the hadc.Init.DMAContinuousRequests field is set to DISABLE, then you need to call the HAL_ADC_Stop_DMA() at the end of every conversion sequence and before calling the HAL_ADC_Start_- DMA() again. Otherwise, the conversion will not start.

#### 12.2.6.3 Continuous Conversions in DMA Mode

To perform continuous conversions in DMA mode, you need to do the following steps:

- Set the hadc.Init.ContinuousConvMode field to ENABLE.
- Set the hadc.Init.DMAContinuousRequests field to ENABLE, otherwise the ADC does not retrigger the DMA once the first scan sequence completes.
- Configure the DMA Stream/Channel in DMA_CIRCULAR mode.

### 12.2.7 Errors Management

ADC peripheral has the ability to notify developers in case a conversion is lost. This error condition happens when a continuous or scan mode conversion is ongoing, and the ADC data register is overwritten by the successive transaction before it is read. When this happens a special bit in the ADC_SR register is set and the ADC interrupt is generated.

We can capture the overrun error by implementing the following callback:</pre></td>
<td><pre>因此，对于 STM32L073RZ 示例，本例及下一个示例将仅循环使用一个通道。

![Image from PDF page 395](../images/page-0395-image-01.png)

#### 12.2.6.1 在 DMA 模式下对同一通道进行多次转换

要在 DMA 模式下对同一通道（或同一通道序列）执行指定次数的转换，您需要执行以下操作：

- 将 hadc.Init.ContinuousConvMode 字段设置为 ENABLE。
- 分配大小足够的缓冲区。
- 将所需的采集次数传递给 HAL_ADC_Start_DMA()。

#### 12.2.6.2 DMA 模式下的多次非连续转换

要在直接存储器访问模式下执行多次转换，您需要执行以下步骤：

```text
• Set the hadc.Init.DMAContinuousRequests field to ENABLE.
• Call the HAL_ADC_Start_DMA() to start conversions in DMA mode.
```

如果将 hadc.Init.DMAContinuousRequests 字段设置为 DISABLE，则需要在每个转换序列结束时调用 HAL_ADC_Stop_DMA()，并在再次调用 HAL_ADC_Start_DMA() 之前执行此操作。否则，转换将不会启动。

#### 12.2.6.3 DMA 模式下的连续转换

要在 DMA 模式下执行连续转换，您需要执行以下步骤：

- 将 hadc.Init.ContinuousConvMode 字段设置为 ENABLE。
- 将 hadc.Init.DMAContinuousRequests 字段设置为 ENABLE，否则在首次扫描序列完成后，ADC 不会重新触发直接存储器访问。
- 配置直接存储器访问 Stream/Channel in DMA_CIRCULAR 模式。

### 12.2.7 错误管理

ADC 外设具备在转换丢失时通知开发人员的能力。当连续模式或扫描模式转换正在进行，且 ADC 数据寄存器在读取之前被后续事务覆盖时，就会发生这种错误情况。此时，ADC_SR 寄存器中的一个特殊位会被置位，并产生 ADC 中断。

我们可以通过实现以下回调函数来捕获溢出错误：</pre></td>
</tr></tbody></table>

## PDF page 396 — Chapter 12: Analog-To-Digital Conversion

Focus: `numbers=01, 0396, 12.2, 20kHz, 396, 8; negation=disabled, no, not; conditions=When, if, when; identifiers=ADC_OVR_DATA_, HAL_ADC_ErrorCallback, HAL_ADC_IRQHandler, HAL_ADC_Start_DMA`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>```text
void HAL_ADC_ErrorCallback(ADC_HandleTypeDef *hadc);
```

When the overrun error occurs, DMA transfers are disabled, and DMA requests are no longer accepted. In this case, if a DMA request is made, the regular conversion in progress is aborted and further regular triggers are ignored. It is then necessary to clear the OVR flag and the DMAEN bit of the used DMA stream, and to reinitialize both the DMA and the ADC to have the wanted converted channel data transferred to the right memory location (all these operations are automatically performed by the HAL when calling the HAL_ADC_Start_DMA() routine).

We can simulate an overrun error by enabling the continuous conversion mode in the previous example, and setting to ENABLE the hadc.Init.DMAContinuousRequests field¹³: if the ADC interrupt is enabled, and the HAL_ADC_IRQHandler() is invoked from it, then you will be able to catch the overrun error.

![Image from PDF page 396](../images/page-0396-image-01.png)

The overrun error is not only related to wrong configurations of the ADC interface. It can be generated even when the ADC works in DMA circular mode. For a custom design based on an STM32F4 MCU I made a while ago, where the DMA was heavily exploited by several peripherals, I experienced that the overrun error could occur when other concurrent transactions are performed by the DMA. Even if the bus arbitration should avoid race conditions, especially when priorities are properly set, I experienced this error in some non-reproducible situations. By correctly handling the overrun error I was able to restart conversions when this happened. Needless to say that, before I realized the source of unexpected stops in DMA conversion, I spent several days trying to debug the issue.

### 12.2.8 Timer-Driven Conversions

ADC peripheral can be configured to be driven from a timer through the TRGO trigger line. The timer used to perform this operation is hardwired during the chip design. For example, in an STM32F401RE MCU the ADC1 peripheral can be synchronized using the TIM2 timer. This feature is extremely useful to perform ADC conversions at a given frequency. For example, we can sample an audio wave generated by a microphone at 20kHz frequency. The result data can be then stored in a persistent memory.

The ADC conversions can be driven by timers both in interrupt and DMA mode. The former is useful when we sample just one channel at low frequencies. The latter is mandatory for scan mode conversions at high frequencies. To enable timer-driven conversions you can follow this procedure:

- Configure the timer connected to the ADC through the TRGO line according to the wanted sampling frequency.

¹³In some STM32 MCUs it is also required to explicitly enable the overrun detection by setting the hadc.Init.Overrun to ADC_OVR_DATA_- OVERWRITTEN. Consult the HAL source code for the MCU family you are considering.</pre></td>
<td><pre>```text
void HAL_ADC_ErrorCallback(ADC_HandleTypeDef *hadc);
```

当发生溢出错误时，DMA 传输将被禁用，且不再接受 DMA 请求。在这种情况下，如果发出 DMA 请求，正在进行的常规转换将被中止，后续的常规触发将被忽略。随后，必须清除 OVR 标志位以及所用 DMA 流的 DMAEN 位，并重新初始化 DMA 和 ADC，以便将所需转换通道的数据传送到正确的内存位置（当调用 HAL_ADC_Start_DMA() 例程时，HAL 会自动执行所有这些操作）。

我们可以通过启用前一个示例中的连续转换模式，并将 hadc.Init.DMAContinuousRequests 字段设置为 ENABLE 来模拟溢出错误¹³：如果启用了 ADC 中断，并且从中断中调用了 HAL_ADC_IRQHandler()，那么您将能够捕获溢出错误。

![Image from PDF page 396](../images/page-0396-image-01.png)

溢出错误不仅与ADC接口的错误配置有关。即使ADC工作在DMA循环模式下，也可能产生该错误。在我之前基于STM32F4微控制器所做的一款自定义设计中，多个外设大量使用了DMA，我发现当DMA执行其他并发传输时，可能会发生溢出错误。尽管总线仲裁本应避免出现竞态条件，尤其是在优先级设置正确的情况下，但我仍在一些无法复现的场景中遇到了此错误。通过正确处理溢出错误，我得以在发生该情况时重新启动转换。不用说，在我意识到DMA转换意外停止的根本原因之前，我花了数天时间尝试调试该问题。

### 12.2.8 定时器触发的转换

ADC 外设可配置为由定时器通过 TRGO 触发线驱动。用于执行此操作的定时器在芯片设计阶段即已硬连线固定。例如，在 STM32F401RE 微控制器中，ADC1 外设可使用 TIM2 定时器进行同步。该功能对于以特定频率执行 ADC 转换极为有用。例如，我们可以以 20kHz 频率对麦克风生成的音频波形进行采样。随后，结果数据可存储到持久性存储器中。

ADC 转换可以由定时器驱动，既支持中断模式，也支持直接存储器访问（DMA）模式。前者适用于以低频率仅采样单个通道的场景。后者则是高频扫描模式转换的必需方式。要启用定时器驱动的转换，您可以按照以下步骤操作：

- 根据所需的采样频率，配置通过 TRGO 线连接到 ADC 的定时器。

¹³在某些 STM32 微控制器中，还需要通过将 hadc.Init.Overrun 设置为 ADC_OVR_DATA_OVERWRITTEN 来显式启用溢出检测。请查阅您所考虑的微控制器系列的硬件抽象层源代码。</pre></td>
</tr></tbody></table>

## PDF page 397 — Chapter 12: Analog-To-Digital Conversion

Focus: `numbers=1, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 2, 3, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95; negation=DISABLE, disabled, not, without; conditions=if, otherwise; identifiers=ADC_CHANNEL_TEMPSENSOR, ADC_CLOCK_SYNC_PCLK_DIV8, ADC_DATAALIGN_RIGHT, ADC_EOC_SEQ_CONV, ADC_EXTERNALTRIG2_T2_TRGO, ADC_EXTERNALTRIGCONVEDGE_RISING, ADC_RESOLUTION_12B, ADC_SAMPLETIME_480CYCLES, HAL_ADC_ConfigChannel, HAL_ADC_Init, HAL_TIMEx_MasterConfigSynchronization, TIM_TRGO_UPDATE`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>## - Configure the timer’s TRGO line so that it triggers every time the update event is generated (TIM_TRGO_UPDATE)¹⁴.
- Configure the ADC so that the selected timer TRGO line triggers the conversions and be sure that continuous conversion mode is disabled (because it is the TRGO line that fires the conversion). Moreover, set the hadc.Init.DMAContinuousRequests field to ENABLE and the DMA in circular mode if you want to perform N conversion at time indefinitely, or set the hadc.Init.DMAContinuousRequests field to DISABLE if you want to stop after N conversions are performed.
- Be sure to set the hadc.Init.ContinuousConvMode field to DISABLE, otherwise the ADC performs conversions by its own without waiting the timer trigger.
- Start the timer.
- Start the ADC in interrupt or DMA mode.

## The following example shows how to trigger a conversion every 1s in an STM32F401RE MCU using the TIM2 timer.

```text
Filename: Core/Src/main-ex3.c
85
/** Configure the global features of the ADC (Clock, Resolution,
86
*
Data Alignment and number of conversion) */
87
hadc1.Instance = ADC1;
88
hadc1.Init.ClockPrescaler = ADC_CLOCK_SYNC_PCLK_DIV8;
89
hadc1.Init.Resolution = ADC_RESOLUTION_12B;
90
hadc1.Init.ScanConvMode = DISABLE;
91
hadc1.Init.ContinuousConvMode = DISABLE;
92
hadc1.Init.DiscontinuousConvMode = DISABLE;
93
hadc1.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_RISING;
94
hadc1.Init.ExternalTrigConv = ADC_EXTERNALTRIG2_T2_TRGO;
95
hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
96
hadc1.Init.NbrOfConversion = 3;
97
hadc1.Init.DMAContinuousRequests = ENABLE;
98
hadc1.Init.EOCSelection = ADC_EOC_SEQ_CONV;
99
HAL_ADC_Init(&amp;hadc1);
100
101
/** Configure for the selected ADC regular channel its corresponding
102
*
rank in the sequencer and its sample time. */
103
sConfig.Channel = ADC_CHANNEL_TEMPSENSOR;
104
sConfig.Rank = 1;
105
sConfig.SamplingTime = ADC_SAMPLETIME_480CYCLES;
106
HAL_ADC_ConfigChannel(&amp;hadc1, &amp;sConfig);
107
108
sConfig.Rank = 2;
109
HAL_ADC_ConfigChannel(&amp;hadc1, &amp;sConfig);
110
```

¹⁴Please, take note that it is important to configure the timer’s TRGO output mode by using the HAL_TIMEx_MasterConfigSynchronization() routine even if the timer does not work in master mode. This is a source of confusion for novice users, and I have to admit that that is a little bit counter-intuitive.</pre></td>
<td><pre>## - 配置定时器的 TRGO 线，使其在每次生成更新事件时都触发（TIM_TRGO_UPDATE）¹⁴。
- 配置 ADC，使所选定时器的 TRGO 线触发转换，并确保禁用连续转换模式（因为是由 TRGO 线触发转换的）。此外，如果希望无限期地每次执行 N 次转换，请将 hadc.Init.DMAContinuousRequests 字段设置为 ENABLE，并将 DMA 设置为循环模式；如果希望在执行 N 次转换后停止，请将 hadc.Init.DMAContinuousRequests 字段设置为 DISABLE。
- 务必将 hadc.Init.ContinuousConvMode 字段设置为 DISABLE，否则 ADC 将在不等待定时器触发的情况下自行执行转换。
- 启动定时器。
- 以中断模式或 DMA 模式启动 ADC。

## 以下示例展示了如何在 STM32F401RE 微控制器中使用 TIM2 定时器，每 1 秒触发一次转换。

```text
Filename: Core/Src/main-ex3.c
85
/** Configure the global features of the ADC (Clock, Resolution,
86
*
Data Alignment and number of conversion) */
87
hadc1.Instance = ADC1;
88
hadc1.Init.ClockPrescaler = ADC_CLOCK_SYNC_PCLK_DIV8;
89
hadc1.Init.Resolution = ADC_RESOLUTION_12B;
90
hadc1.Init.ScanConvMode = DISABLE;
91
hadc1.Init.ContinuousConvMode = DISABLE;
92
hadc1.Init.DiscontinuousConvMode = DISABLE;
93
hadc1.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_RISING;
94
hadc1.Init.ExternalTrigConv = ADC_EXTERNALTRIG2_T2_TRGO;
95
hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
96
hadc1.Init.NbrOfConversion = 3;
97
hadc1.Init.DMAContinuousRequests = ENABLE;
98
hadc1.Init.EOCSelection = ADC_EOC_SEQ_CONV;
99
HAL_ADC_Init(&amp;hadc1);
100
101
/** Configure for the selected ADC regular channel its corresponding
102
*
rank in the sequencer and its sample time. */
103
sConfig.Channel = ADC_CHANNEL_TEMPSENSOR;
104
sConfig.Rank = 1;
105
sConfig.SamplingTime = ADC_SAMPLETIME_480CYCLES;
106
HAL_ADC_ConfigChannel(&amp;hadc1, &amp;sConfig);
107
108
sConfig.Rank = 2;
109
HAL_ADC_ConfigChannel(&amp;hadc1, &amp;sConfig);
110
```

¹⁴请注意，即使定时器未工作在主模式，使用 HAL_TIMEx_MasterConfigSynchronization() 例程配置定时器的 TRGO 输出模式也是非常重要的。这对初学者来说是一个容易混淆的点，我必须承认这有点反直觉。</pre></td>
</tr></tbody></table>

## PDF page 399 — Chapter 12: Analog-To-Digital Conversion

Focus: `numbers=0, 1, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122; negation=; conditions=If; identifiers=HAL_ADC_ConvCpltCallback, HAL_ADC_Start_DMA, HAL_Init, HAL_MAX_DELAY, HAL_TIM_Base_Start, HAL_UART_Transmit, MX_ADC1_Init, MX_DMA_Init, MX_GPIO_Init, MX_TIM2_Init, MX_USART2_UART_Init, SystemClock_Config, sprintf`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>## The DMA is so configured accordingly to work in circular mode (line 122).

```text
Filename: Core/Src/main-ex3.c
85
int main(void) {
86
/* Reset of all peripherals, Initializes the Flash interface and the Systick. */
87
HAL_Init();
```

88

```text
89
/* Configure the system clock */
90
SystemClock_Config();
```

91

```text
92
/* Initialize all configured peripherals */
93
MX_DMA_Init();
94
MX_ADC1_Init();
95
MX_GPIO_Init();
96
MX_USART2_UART_Init();
97
MX_TIM2_Init();
```

98

```text
99
HAL_TIM_Base_Start(&amp;htim2);
100
HAL_ADC_Start_DMA(&amp;hadc1, (uint32_t*)rawValues, 3);
101
102
while(1) {
103
while(!convCompleted);
104
105
for(uint8_t i = 0; i &lt; hadc1.Init.NbrOfConversion; i++) {
106
temp = ((float)rawValues[i]) / 4095 * 3300;
107
temp = ((temp - 760.0) / 2.5) + 25;
108
109
sprintf(msg, &quot;rawValue %d: %hu\r\n&quot;, i, rawValues[i]);
110
HAL_UART_Transmit(&amp;huart2, (uint8_t*) msg, strlen(msg), HAL_MAX_DELAY);
111
112
sprintf(msg, &quot;Temperature %d: %f\r\n&quot;,i,
temp);
113
HAL_UART_Transmit(&amp;huart2, (uint8_t*) msg, strlen(msg), HAL_MAX_DELAY);
114
}
115
convCompleted = 0;
116
}
117
}
118
119
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef*hadc) {
120
convCompleted = 1;
121
}
```

## The above code shows the content of the main() function, which should be easy to understand. The timer is started at line 56 and the ADC is started in DMA mode to perform three acquisitions from the ADC. If you run the example, you can see that ever three seconds the DMA completes the transfer and the convCompleted variable is set: this causes that the three conversions are printed on the UART2 interface every three seconds.</pre></td>
<td><pre>## DMA 相应地被配置为工作在循环模式（第 122 行）。

```text
Filename: Core/Src/main-ex3.c
85
int main(void) {
86
/* Reset of all peripherals, Initializes the Flash interface and the Systick. */
87
HAL_Init();
```

88

```text
89
/* Configure the system clock */
90
SystemClock_Config();
```

91

```text
92
/* Initialize all configured peripherals */
93
MX_DMA_Init();
94
MX_ADC1_Init();
95
MX_GPIO_Init();
96
MX_USART2_UART_Init();
97
MX_TIM2_Init();
```

98

```text
99
HAL_TIM_Base_Start(&amp;htim2);
100
HAL_ADC_Start_DMA(&amp;hadc1, (uint32_t*)rawValues, 3);
101
102
while(1) {
103
while(!convCompleted);
104
105
for(uint8_t i = 0; i &lt; hadc1.Init.NbrOfConversion; i++) {
106
temp = ((float)rawValues[i]) / 4095 * 3300;
107
temp = ((temp - 760.0) / 2.5) + 25;
108
109
sprintf(msg, &quot;rawValue %d: %hu\r\n&quot;, i, rawValues[i]);
110
HAL_UART_Transmit(&amp;huart2, (uint8_t*) msg, strlen(msg), HAL_MAX_DELAY);
111
112
sprintf(msg, &quot;Temperature %d: %f\r\n&quot;,i,
temp);
113
HAL_UART_Transmit(&amp;huart2, (uint8_t*) msg, strlen(msg), HAL_MAX_DELAY);
114
}
115
convCompleted = 0;
116
}
117
}
118
119
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef*hadc) {
120
convCompleted = 1;
121
}
```

## 上述代码展示了 main() 函数的内容，应该很容易理解。定时器在第 56 行启动，ADC 以 DMA 模式启动以执行三次 ADC 采集。如果你运行该示例，可以看到每三秒 DMA 完成一次传输，并且 convCompleted 变量被置位：这导致每三秒在 UART2 接口上打印三次转换结果。</pre></td>
</tr></tbody></table>

## PDF page 410 — Chapter 13: Digital-To-Analog Conversion

Focus: `numbers=0, 1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 2, 20, 200, 2048, 21, 22, 23, 24, 25, 26, 27, 28, 29; negation=; conditions=; identifiers=DAC_ALIGN_12B_R, DAC_CHANNEL_1, HAL_DAC_Init, HAL_DAC_Start_DMA, HAL_Init, HAL_TIM_Base_Start, MX_DAC_Init, MX_TIM6_Init, Nucleo_BSP_Init`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>## Since the STM32 DAC has a resolution of 12-bit, we have to divide the value 4095, which corresponds to the maximum output voltage, by 200 steps using the following formula:

) + 1 ) (4096

) [3]

DACOutput = ( sin ( x · 2π

2

ns

## where ns is the number of samples, that is 200 in our example.

## Using the above formula, we can generate an initialization vector to feed the DAC in DMA mode. Like for the ADC peripheral, we can use a timer configured to trigger the TRGO line at the frequency given by [2]. The following example shows how to generate a 50Hz sine wave using the DAC in an STM32F072 MCU.

```text
Filename: Core/Src/main-ex2.c
7
#define PI
3.14159
8
#define SAMPLES 200
```

9

```text
10
/* Private variables ---------------------------------------------------------*/
11
DAC_HandleTypeDef hdac;
12
TIM_HandleTypeDef htim6;
13
DMA_HandleTypeDef hdma_dac_ch1;
```

14

```text
15
/* Private function prototypes -----------------------------------------------*/
16
static void MX_DAC_Init(void);
17
static void MX_TIM6_Init(void);
```

18

```text
19
int main(void) {
20
uint16_t IV[SAMPLES], value;
```

21

```text
22
HAL_Init();
23
Nucleo_BSP_Init();
```

24

```text
25
/* Initialize all configured peripherals */
26
MX_TIM6_Init();
27
MX_DAC_Init();
```

28

```text
29
for (uint16_t i = 0; i &lt; SAMPLES; i++) {
30
value = (uint16_t) rint((sinf(((2*PI)/SAMPLES)*i)+1)*2048);
31
IV[i] = value &lt; 4096 ? value : 4095;
32
}
```

33

```text
34
HAL_DAC_Init(&amp;hdac);
35
HAL_TIM_Base_Start(&amp;htim6);
36
HAL_DAC_Start_DMA(&amp;hdac, DAC_CHANNEL_1, (uint32_t*)IV, SAMPLES, DAC_ALIGN_12B_R);
```

37

```text
38
while(1);
39
}
```</pre></td>
<td><pre>## 由于 STM32 DAC 的分辨率为 12 位，我们必须使用以下公式将对应最大输出电压的值 4095 除以 200 步：

) + 1 ) (4096

) [3]

DACOutput = ( sin ( x · 2π

2

ns

## 其中 ns 是采样数，在我们的例子中为 200。

## 使用上述公式，我们可以生成一个初始化向量，以在 DMA 模式下馈送 DAC。与 ADC 外设一样，我们可以使用配置为以公式 [2] 给定的频率触发 TRGO 线的定时器。以下示例展示了如何在 STM32F072 MCU 中使用 DAC 生成 50Hz 正弦波。

```text
Filename: Core/Src/main-ex2.c
7
#define PI
3.14159
8
#define SAMPLES 200
```

9

```text
10
/* Private variables ---------------------------------------------------------*/
11
DAC_HandleTypeDef hdac;
12
TIM_HandleTypeDef htim6;
13
DMA_HandleTypeDef hdma_dac_ch1;
```

14

```text
15
/* Private function prototypes -----------------------------------------------*/
16
static void MX_DAC_Init(void);
17
static void MX_TIM6_Init(void);
```

18

```text
19
int main(void) {
20
uint16_t IV[SAMPLES], value;
```

21

```text
22
HAL_Init();
23
Nucleo_BSP_Init();
```

24

```text
25
/* Initialize all configured peripherals */
26
MX_TIM6_Init();
27
MX_DAC_Init();
```

28

```text
29
for (uint16_t i = 0; i &lt; SAMPLES; i++) {
30
value = (uint16_t) rint((sinf(((2*PI)/SAMPLES)*i)+1)*2048);
31
IV[i] = value &lt; 4096 ? value : 4095;
32
}
```

33

```text
34
HAL_DAC_Init(&amp;hdac);
35
HAL_TIM_Base_Start(&amp;htim6);
36
HAL_DAC_Start_DMA(&amp;hdac, DAC_CHANNEL_1, (uint32_t*)IV, SAMPLES, DAC_ALIGN_12B_R);
```

37

```text
38
while(1);
39
}
```</pre></td>
</tr></tbody></table>

## PDF page 414 — Chapter 13: Digital-To-Analog Conversion

Focus: `numbers=01, 0414, 0xAAA, 13.2, 13.5, 4, 414; negation=without; conditions=; identifiers=HAL_DACEx_NoiseWaveGenerate, HAL_DACEx_TriangleWaveGenerate, HAL_DAC_SetValue, HAL_DAC_Start`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>- Configure the DAC channel used to generate the wave.
- Configure the timer associated to the DAC, and configure its prescaler according to equation [4].
- Start the DAC using the HAL_DAC_Start() function.
- Configure the wanted offset value using the HAL_DAC_SetValue() routine.
- Start triangular wave generation by calling the HAL_DACEx_TriangleWaveGenerate() function.

### 13.2.4 Noise Wave Generation

STM32 DACs are also able to generate noise waves (see Figure 13.5), using a pseudo-random generator. This is useful in some application domains, like audio applications and RF systems. Moreover, it can be also used to increase the accuracy of ADC peripheral¹.

To generate a variable-amplitude pseudo-noise, an LFSR (linear feedback shift register) is available in the DAC. This register is preloaded with the value 0xAAA, which may be masked partially or totally. This value is then added up to the DAC data register contents without overflow and this value is then used as output value.

![Image from PDF page 414](../images/page-0414-image-01.jpeg)

Figure 13.5: a noise wave generated with the DAC

To generate the noise wave, we can use the HAL routine

```text
HAL_StatusTypeDef HAL_DACEx_NoiseWaveGenerate(DAC_HandleTypeDef* hdac, uint32_t Channel,
uint32_t Amplitude);
```

which accepts the channel used to generate the wave and the amplitude value, which is added to the LFSR content to generate the pseudo-random wave. Like for the triangular wave generation, a timer can be used to trigger conversion: this means that the frequency of the wave is determined by the overflow frequency of the timer.

¹ST provides the AN2668(https://bit.ly/25lJoqx) dedicated to this topic.</pre></td>
<td><pre>- 配置用于生成波形的 DAC 通道。
- 配置与 DAC 关联的定时器，并根据公式 [4] 配置其预分频器。
- 使用 HAL_DAC_Start() 函数启动 DAC。
- 使用 HAL_DAC_SetValue() 例程配置所需的偏移量值。
- 调用 HAL_DACEx_TriangleWaveGenerate() 函数启动三角波生成。

### 13.2.4 噪声波生成

STM32 的 DAC 还能够使用伪随机数生成器生成噪声波（见图 13.5）。这在某些应用领域非常有用，例如音频应用和射频（RF）系统。此外，它还可以用于提高 ADC 外设¹的精度。

要生成可变幅度的伪噪声，DAC 中提供了一个 LFSR（线性反馈移位寄存器）。该寄存器预加载了值 0xAAA，该值可以被部分或完全屏蔽。然后，该值与 DAC 数据寄存器的内容相加（无溢出），并将结果用作输出值。

![Image from PDF page 414](../images/page-0414-image-01.jpeg)

图 13.5：使用 DAC 生成的噪声波

要生成噪声波，我们可以使用 HAL 例程

```text
HAL_StatusTypeDef HAL_DACEx_NoiseWaveGenerate(DAC_HandleTypeDef* hdac, uint32_t Channel,
uint32_t Amplitude);
```

该函数接受用于生成波形的通道和幅度值，该幅度值会与 LFSR 的内容相加以生成伪随机波。与三角波生成类似，可以使用定时器来触发转换：这意味着波形的频率由定时器的溢出频率决定。

¹ST 提供了专门针对此主题的 AN2668(https://bit.ly/25lJoqx)。</pre></td>
</tr></tbody></table>

## PDF page 422 — Chapter 14: I²C

Focus: `numbers=01, 0422, 14.1, 14.2, 422, 64; negation=; conditions=; identifiers=HAL_I2C`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>![Image from PDF page 422](../images/page-0422-image-01.png)

Table 14.1: Effective availability of I²C peripherals in MCUs equipping all nine Nucleo boards

For every I²C peripheral, and a given STM32 MCU, Table 14.1 shows the pins corresponding to SDA and SCL lines. Moreover, darker rows show alternate pins that can be used during the layout of the board. For example, given the STM32F401RE MCU, we can see that I2C1 peripheral is mapped to PB7 and PB6, but PB9 and PB8 can be also used as alternate pins. Note that the I2C1 peripheral uses the same I/O pins in all STM32 MCUs with LQFP-64 package. This is a paramount example of the pin-to-pin compatibility offered by STM32 microcontrollers.

We are now ready to see how-to use the CubeHAL APIs to program this peripheral.

## 14.2 HAL_I2C Module

To program the I²C peripheral, the CubeHAL defines the C struct I2C_HandleTypeDef, which is defined in the following way:</pre></td>
<td><pre>![Image from PDF page 422](../images/page-0422-image-01.png)

表 14.1：九块 Nucleo 开发板所搭载微控制器中 I²C 外设的实际可用性

对于每一个 I²C 外设和给定的 STM32 微控制器，表 14.1 显示了 SDA 和 SCL 线对应的引脚。此外，较深色的行显示了在电路板布局期间可以使用的备用引脚。例如，对于 STM32F401RE 微控制器，我们可以看到 I2C1 外设映射到 PB7 和 PB6，但 PB9 和 PB8 也可以用作备用引脚。请注意，I2C1 外设在所有采用 LQFP-64 封装的 STM32 微控制器中使用相同的 I/O 引脚。这是 STM32 微控制器提供的引脚对引脚兼容性的一个关键示例。

我们现在准备看看如何使用 CubeHAL API 来编程此外设。

## 14.2 HAL_I2C 模块

为了编程 I²C 外设，CubeHAL 定义了 C 结构体 I2C_HandleTypeDef，其定义方式如下：</pre></td>
</tr></tbody></table>

## PDF page 433 — Chapter 14: I²C

Focus: `numbers=0, 0xFF, 0xFF00, 1, 1.1, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 14.2, 14.8, 14.9, 2, 73, 78, 8, 90, 92; negation=cannot; conditions=if; identifiers=HAL_I2C_Master_Transmit, HAL_MAX_DELAY, HAL_OK, Read_From_24LCxx, Write_To_24LCxx, free, memcpy`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>```text
92
/* We compute the MSB and LSB parts of the memory address */
93
data[0] = (uint8_t) ((MemAddress &amp; 0xFF00) &gt;&gt; 8);
94
data[1] = (uint8_t) (MemAddress &amp; 0xFF);
```

95

```text
96
/* And copy the content of the pData array in the temporary buffer */
97
memcpy(data+2, pData, len);
```

98

```text
99
/* We are now ready to transfer the buffer over the I2C bus */
100
returnValue = HAL_I2C_Master_Transmit(hi2c, DevAddress, data, len + 2, HAL_MAX_DELAY);
101
if(returnValue != HAL_OK)
102
return returnValue;
103
104
free(data);
105
106
/* We wait until the EEPROM effectively stores data in memory */
107
while(HAL_I2C_Master_Transmit(hi2c, DevAddress, 0, 0, HAL_MAX_DELAY) != HAL_OK);
108
109
return HAL_OK;
110
}
```

We can now focus our attention on the two routines to use the 24LCxx EEPROM. Both of them are designed to accept:

- the I²C slave address of the EEPROM memory (DevAddress);
- the memory address where start storing/reading data (MemAddress);
- the pointer to the memory buffer used to exchange data with the EEPROM (pData);
- the amount of data to store/read (len);

The Read_From_24LCxx() function starts computing the two halves of the memory address (MSB and LSB part). It then sends the two parts over the I²C bus using the HAL_I2C_Master_Transmit() routine (line 73). As said before, the 24LCxx memory is designed so that it sets the internal address counter to the passed address. We can so start a new transaction in read mode to retrieve the amount of data from the EEPROM (line 78).

The Write_To_24LCxx() functions does a similar thing, but in a different way. It must adhere to the 24LCxx protocol described in Figure 14.9, which slightly differs from the one in Figure 14.8 . This means that we cannot use two separated transactions for the memory address and the data to store, but we have to perform a unique I²C transaction. For this reason, we use a temporary and dynamic buffer (line 90), which contains the two halves of the memory address plus the data to store in the EEPROM. We can so perform a transaction over the I²C bus (line 98) and then wait until the EEPROM completes the memory transfer (line 107).

#### 14.2.1.1 I/O MEM Operations

The protocol used by the 24LCxx EEPROM is indeed common to all I²C devices that have memoryaddressable registers to read to and to write from. For example, a lot of I²C sensors, like the HTS221</pre></td>
<td><pre>```text
92
/* We compute the MSB and LSB parts of the memory address */
93
data[0] = (uint8_t) ((MemAddress &amp; 0xFF00) &gt;&gt; 8);
94
data[1] = (uint8_t) (MemAddress &amp; 0xFF);
```

95

```text
96
/* And copy the content of the pData array in the temporary buffer */
97
memcpy(data+2, pData, len);
```

98

```text
99
/* We are now ready to transfer the buffer over the I2C bus */
100
returnValue = HAL_I2C_Master_Transmit(hi2c, DevAddress, data, len + 2, HAL_MAX_DELAY);
101
if(returnValue != HAL_OK)
102
return returnValue;
103
104
free(data);
105
106
/* We wait until the EEPROM effectively stores data in memory */
107
while(HAL_I2C_Master_Transmit(hi2c, DevAddress, 0, 0, HAL_MAX_DELAY) != HAL_OK);
108
109
return HAL_OK;
110
}
```

我们现在可以将注意力集中在用于操作 24LCxx EEPROM 的两个例程上。它们都设计为接受以下参数：

- EEPROM 存储器的 I²C 从机地址 (DevAddress)；
- 开始存储/读取数据的内存地址 (MemAddress)；
- 用于与 EEPROM 交换数据的内存缓冲区指针 (pData)；
- 要存储/读取的数据量 (len)；

Read_From_24LCxx() 函数首先计算内存地址的两个部分（最高有效字节 MSB 和最低有效字节 LSB）。然后，它使用 HAL_I2C_Master_Transmit() 例程（第 73 行）通过 I²C 总线发送这两个部分。如前所述，24LCxx 存储器被设计为将内部地址计数器设置为传入的地址。因此，我们可以启动一个新的读模式事务，以从 EEPROM 中检索所需的数据量（第 78 行）。

Write_To_24LCxx() 函数执行类似的操作，但方式不同。它必须遵循图 14.9 中描述的 24LCxx 协议，该协议与图 14.8 中的协议略有不同。这意味着我们不能使用两个独立的事务分别传输内存地址和要存储的数据，而必须执行单一的 I²C 事务。为此，我们使用一个临时的动态缓冲区（第 90 行），其中包含内存地址的两个部分以及要存储在 EEPROM 中的数据。然后，我们可以执行一次 I²C 总线事务（第 98 行），并等待 EEPROM 完成内存传输（第 107 行）。

#### 14.2.1.1 I/O MEM 操作

24LCxx EEPROM 所使用的协议实际上是所有具有可寻址寄存器（memory-addressable registers）以进行读取和写入的 I²C 设备的通用协议。例如，许多 I²C 传感器，如 HTS221</pre></td>
</tr></tbody></table>

## PDF page 449 — Chapter 15: SPI

Focus: `numbers=01, 0449, 15.1, 15.2, 4, 449, 64; negation=; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>at the starting of the MSB bit forming the next transferred byte). For more information about this communication mode, refer to the reference manual for the MCU you are considering.

![Image from PDF page 449](../images/page-0449-image-01.jpeg)

Table 15.2: Effective availability of SPI peripherals in MCUs equipping all nine Nucleo boards

### 15.1.4 Availability of SPI Peripherals in STM32 MCUs

Depending on the family type and package used, STM32 microcontrollers can provide up to six independent SPI peripherals. Table 15.2 summarizes the availability of SPI peripherals in STM32 MCUs equipping all nine Nucleo boards we are considering in this book.

For every SPI peripheral, and a given STM32 MCU, Table 15.2 shows the pins corresponding to MOSI, MISO and SCK lines. Moreover, darker rows show alternate pins that can be used during the layout of the board. For example, given the STM32F401RE MCU, we can see that SPI1 peripheral is mapped to PA7, PA6 and PA5, but PB5, PB5 and PB3 can be also used as alternate pins. Note that the SPI1 peripheral uses the same I/O pins in all STM32 MCUs with LQFP-64 package. This is another clear example of the pin-to-pin compatibility offered by STM32 microcontrollers.

We are now ready to see how-to use the CubeHAL APIs to program this peripheral.</pre></td>
<td><pre>）。有关此通信模式的更多信息，请参阅您所考虑 MCU 的参考手册。

![Image from PDF page 449](../images/page-0449-image-01.jpeg)

表 15.2：配备所有九个 Nucleo 开发板的 MCU 中 SPI 外设的实际可用性

### 15.1.4 STM32 MCU 中 SPI 外设的可用性

根据所使用的家族类型和封装，STM32 微控制器最多可提供六个独立的 SPI 外设。表 15.2 总结了本书中考虑的配备所有九个 Nucleo 开发板的 STM32 MCU 中 SPI 外设的可用性。

对于每个 SPI 外设和给定的 STM32 MCU，表 15.2 显示了与 MOSI、MISO 和 SCK 线对应的引脚。此外，较深的行显示了在电路板布局期间可以使用的备用引脚。例如，对于 STM32F401RE MCU，我们可以看到 SPI1 外设映射到 PA7、PA6 和 PA5，但 PB5、PB5 和 PB3 也可以用作备用引脚。请注意，SPI1 外设在所有具有 LQFP-64 封装的 STM32 MCU 中使用相同的 I/O 引脚。这是 STM32 微控制器提供的引脚对引脚兼容性的另一个清晰示例。

我们现在准备好看看如何使用 CubeHAL API 来编程此外设。</pre></td>
</tr></tbody></table>

## PDF page 452 — Chapter 15: SPI

Focus: `numbers=1, 15.2; negation=no, not; conditions=If, When, if, when; identifiers=HAL_SPI_Init, HAL_SPI_Receive, HAL_SPI_Transmit, SPI_DIRECTION_, SPI_DIRECTION_1LINE`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>calculated using an odd programmable polynomial on each bit. The calculation is processed on the sampling clock edge defined by the CPHA and CPOL configurations. The calculated CRC value is checked automatically at the end of the data block as well as for transfer managed by CPU or by the DMA. When a mismatch is detected between the CRC calculated internally on the received data and the CRC sent by the transmitter, an error condition is set. The CRC feature is not available when the SPI is driven in DMA circular mode. For more information about this option, refer to the reference manual for the STM32 MCU you are considering.

As usual, to configure the SPI peripheral we use the function:

```text
HAL_StatusTypeDef HAL_SPI_Init(SPI_HandleTypeDef *hspi);
```

which accepts a pointer to an instance of the SPI_HandleTypeDef struct seen before.

### 15.2.1 Exchanging Messages Using SPI Peripheral

Once the SPI peripheral is configured, we can start exchanging data with slave devices. Since the SPI specification does not forces a given communication protocol, there is no difference among the CubeHAL routines when using the SPI peripheral in slave or master mode. The only difference resides in the peripheral configuration, setting the Mode parameter of the SPI_InitTypeDef structure accordingly.

As usual, the CubeHAL provides three ways to communicate over a SPI bus: polling, interrupt and DMA mode.

To send a number of bytes to a slave device in polling mode, we use the function:

```text
HAL_StatusTypeDef HAL_SPI_Transmit(SPI_HandleTypeDef *hspi, uint8_t *pData, uint16_t Size,
uint32_t Timeout);
```

The function signature is almost identical to other communication routines seen so far (for example, those used for the UART manipulation), so we will not describe its parameters here. This function can be used if the SPI peripheral is configured to work both in SPI_DIRECTION_1LINE or SPI_DIRECTION_- 2LINES modes. To receive a number of bytes in polling mode, we use the function:

```text
HAL_StatusTypeDef HAL_SPI_Receive(SPI_HandleTypeDef *hspi, uint8_t *pData, uint16_t Size,
uint32_t Timeout);
```

This function can be used in all three Direction modes.

If the slave device supports the full-duplex mode, then we can use the function:</pre></td>
<td><pre>使用奇数可编程多项式对每一位进行计算。计算在由 CPHA 和 CPOL 配置定义的采样时钟边沿上处理。计算出的 CRC 值在数据块结束时自动检查，无论是由 CPU 还是由 直接存储器访问 管理的传输。如果在内部计算的接收数据 CRC 与发送方发送的 CRC 之间检测到不匹配，则设置错误条件。当 SPI 在 DMA 循环模式下驱动时，CRC 功能不可用。有关此选项的更多信息，请参阅您所考虑的 STM32 MCU 的参考手册。

通常，为了配置 SPI 外设，我们使用以下函数：

```text
HAL_StatusTypeDef HAL_SPI_Init(SPI_HandleTypeDef *hspi);
```

该函数接受指向之前看到的 SPI_HandleTypeDef 结构体实例的指针。

### 15.2.1 使用 SPI 外设交换消息

一旦 SPI 外设配置完成，我们即可开始与从设备交换数据。由于 SPI 规范并未强制规定特定的通信协议，因此在使用 SPI 外设时，无论处于从模式还是主模式，CubeHAL 例程之间没有区别。唯一的区别在于外设配置，即相应地设置 SPI_InitTypeDef 结构体中的 Mode 参数。

通常，CubeHAL 提供了三种通过 SPI 总线通信的方式：轮询、中断和直接存储器访问（DMA）模式。

要在轮询模式下向从设备发送若干字节，我们使用以下函数：

```text
HAL_StatusTypeDef HAL_SPI_Transmit(SPI_HandleTypeDef *hspi, uint8_t *pData, uint16_t Size,
uint32_t Timeout);
```

该函数的签名与之前看到的其他通信例程（例如用于 UART 操作的例程）几乎相同，因此我们在此不再描述其参数。如果 SPI 外设被配置为在 SPI_DIRECTION_1LINE 或 SPI_DIRECTION_- 2LINES 模式下工作，均可使用此函数。要在轮询模式下接收若干字节，我们使用以下函数：

```text
HAL_StatusTypeDef HAL_SPI_Receive(SPI_HandleTypeDef *hspi, uint8_t *pData, uint16_t Size,
uint32_t Timeout);
```

此函数可用于所有三种方向模式。

如果从设备支持全双工模式，则我们可以使用以下函数：</pre></td>
</tr></tbody></table>

## PDF page 454 — Chapter 15: SPI

Focus: `numbers=01, 0454, 120, 15.2, 15.3, 15.5, 2, 26, 454, 8; negation=not; conditions=If, if, when; identifiers=HAL_SPI_DMA, HAL_SPI_DMAStop`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>- the CRC feature is not managed when the DMA circular mode is enabled
- when the SPI DMA pause/stop features are used, we must use the function HAL_SPI_DMA- Pause()/ HAL_SPI_DMAStop() only under the SPI callbacks.

In this chapter we will not analyze any concrete example. In Chapter 26 we will use the SPI peripheral to program a hardwired TCP/IP embedded Ethernet controller, which allows us to build Internetbased applications with Nucleo boards.

### 15.2.2 Maximum Transmission Frequency Reachable using the CubeHAL

The SCK frequency is derived from the PCLK frequency using a programmable prescaler. This prescaler ranges from 2¹ up to 2⁸. However, as said several other times before, the CubeHAL adds an unavoidable overhead when driving peripherals. And this also applies to the SPI one. In fact, using the CubeHAL it is not possible to reach all supported SPI frequencies with the different SPI modes.

ST engineers have clearly documented this in the CubeHAL. If you open the stm32XXxx_hal_spi.c file, you can see (about at line 120) two tables that report the maximum reachable transmission frequency given the direction mode (half-duplex or full-duplex) and the way to program and use the peripheral (polling, interrupt and DMA).

For example, in an STM32F4 MCU we can reach a SCK frequency equal to fP CLK/8 if the SPI peripheral works in slave mode and we program it using CubeHAL in interrupt mode.

## 15.3 Using CubeMX to Configure SPI Peripheral

To use CubeMX to enable the wanted SPI peripheral, we have to proceed in the following order. First, we need to select the wanted communication, as shown in Figure 15.5. Next, we need to specify the behavior of the NSS signal in the same configuration view. Once these two parameters are set, we can proceed by configuring other SPI settings in the CubeMX Configuration pane.

![Image from PDF page 454](../images/page-0454-image-01.png)

Figure 15.5: How to select the SPI communication mode in CubeMX</pre></td>
<td><pre>- 当启用 DMA 循环模式时，CRC 功能不受管理
- 当使用 SPI DMA 暂停/停止功能时，我们必须在 SPI 回调函数下仅使用函数 HAL_SPI_DMA- Pause()/ HAL_SPI_DMAStop()。

在本章中，我们不会分析任何具体示例。在第 26 章中，我们将使用 SPI 外设来编程一个硬连线 TCP/IP 嵌入式以太网控制器，这使我们能够使用 Nucleo 板构建基于互联网的应用程序。

### 15.2.2 使用 CubeHAL 可达到的最大传输频率

SCK 频率是通过可编程预分频器从 PCLK 频率派生而来的。该预分频器的范围从 2¹ 到 2⁸。然而，正如之前多次提到的，CubeHAL 在驱动外设时会增加不可避免的开销。这也适用于 SPI 外设。事实上，使用 CubeHAL 时，无法在不同的 SPI 模式下达到所有支持的 SPI 频率。

ST 工程师已在 CubeHAL 中清楚地记录了这一点。如果您打开 stm32XXxx_hal_spi.c 文件，可以看到（大约在第 120 行）两个表格，它们报告了给定方向模式（半双工或全双工）以及编程和使用外设的方式（轮询、中断和 DMA）下的最大可达传输频率。

例如，在 STM32F4 MCU 中，如果 SPI 外设工作在从模式，并且我们使用 CubeHAL 以中断模式对其进行编程，则可以达到等于 fP CLK/8 的 SCK 频率。

## 15.3 使用 CubeMX 配置 SPI 外设

若要使用 CubeMX 启用所需的 SPI 外设，必须按以下顺序操作。首先，我们需要选择所需的通信模式，如图 15.5 所示。接下来，我们需要在同一配置视图中指定 NSS 信号的行为。设置好这两个参数后，我们可以在 CubeMX 配置窗格中继续配置其他 SPI 设置。

![Image from PDF page 454](../images/page-0454-image-01.png)

图 15.5：如何在 CubeMX 中选择 SPI 通信模式</pre></td>
</tr></tbody></table>

## PDF page 455 — Chapter 16: Cyclic Redundancy Check

Focus: `numbers=0, 1, 16, 16.1, 8; negation=not; conditions=If, if, when; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre># 16. Cyclic Redundancy Check

In digital systems it is perfectly possible that data gets corrupted, especially if it flows through a communication medium. In digital electronics, a message is a stream of bits either equal to 0 or 1 and it becomes corrupted when one of more of these bits accidentally change during transmission. For this reason, messages are always exchanged with some additional data used to detect if the original message was corrupted. In Chapter 8 we have analyzed an early form of error detection related to data transmission: the parity bit is an additional bit added to the message used to keep track if the number of bits equal to 1 is odd or even (depending on the type of parity). However, this method is not able to detect errors if two or more bits change at the same time.

The Cyclic Redundancy Check (CRC) is a widely used technique for detecting errors in digital data, both during transmission and storage. In the CRC method, several check bits, called the checksum¹, are appended to the message being transmitted. The receiver can determine whether the check bits agree with the data, to assert with a certain degree of probability if an error occurred in transmission. If so, the receiver can ask to the sender to retransmit the message again. This technique is also applied in some data storage devices, such as Hard Disk Drives. In this case each block on the disk would have certain check bits, and the hardware might automatically initiate a reread of the block when an error is detected, or it might report the error to software. It is important to underline that CRC is a good method to identify corrupted messages, but not for making corrections when errors are detected.

Being the CRC method used by a lot of communication peripherals and protocols (like the Ethernet, MODBUS, etc.), it is quite common to find in microcontrollers dedicated hardware peripherals able to compute CRC checksum of byte streams, freeing the CPU from performing this operation in software. All STM32 microcontrollers provide a dedicated CRC peripheral, and this chapter briefly explains how to use the corresponding CubeHAL module.

As usual, before going into the implementation details, we will first give a brief introduction to the math behind the CRC technique².

## 16.1 Introduction to CRC Computing

CRC technique is based on well-known properties of polynomial arithmetic. To compute the checksum of a stream of bits, the message is seen as a polynomial that is divided by another fixed polynomial, called generator polynomial. The remainder of this operation is the checksum, which is

¹The checksum is often called the CRC. This is not entirely correct, because the CRC is a specific error-detecting method, which uses a well-characterized algorithm plus a checksum sequence of bits to detect if a message is corrupted. However, it is quite common to refer to the checksum as the CRC, or the CRC code. ²An excellent dissertation of CRC algorithms is represented by this on-line document by Ross N. Williams (http://www.zlib.net/crc_v3.txt)</pre></td>
<td><pre># 16。循环冗余校验

在数字系统中，数据损坏是完全可能发生的，尤其是在数据通过通信介质传输时。在数字电子学中，消息是一串比特流，其值要么为 0，要么为 1；当其中一个或多个比特在传输过程中意外改变时，消息即被视为损坏。因此，消息交换时总会附带一些额外数据，用于检测原始消息是否已损坏。在第 8 章中，我们分析了与数据传输相关的一种早期错误检测形式：奇偶校验位是附加在消息中的一个额外比特，用于跟踪值为 1 的比特数量是奇数还是偶数（具体取决于奇偶校验的类型）。然而，如果同时有两个或更多比特发生改变，该方法将无法检测到错误。

循环冗余校验（CRC）是一种广泛用于检测数字数据在传输和存储过程中错误的技术。在 CRC 方法中，若干校验位（称为校验和¹）会被附加到待传输的消息上。接收方可以判断校验位是否与数据一致，从而以一定的概率断定传输过程中是否发生了错误。如果是，接收方可以要求发送方重新传输该消息。该技术也应用于某些数据存储设备，例如硬盘驱动器。在这种情况下，磁盘上的每个数据块都会包含特定的校验位，当检测到错误时，硬件可能会自动发起对该数据块的重新读取，或者将错误报告给软件。需要强调的是，CRC 是一种识别损坏消息的有效方法，但并非用于在发生错误时进行纠错

检测到。

由于循环冗余校验（CRC）方法被许多通信外设和协议（如以太网、MODBUS 等）所采用，因此微控制器中通常都配备了能够计算字节流 CRC 校验和的专用硬件外设，从而将 CPU 从在软件中执行此操作的任务中解放出来。所有 STM32 微控制器都提供专用的 CRC 外设，本章将简要介绍如何使用相应的 CubeHAL 模块。

一如既往，在深入实现细节之前，我们首先简要介绍 CRC 技术背后的数学原理²。

## 16.1 CRC 计算简介

CRC 技术基于多项式算术的已知特性。要计算比特流的校验和，可将消息视为一个多项式，并用另一个固定的多项式（称为生成多项式）对其进行除法运算。该运算的余数即为校验和，

¹校验和通常被称为CRC。这种说法并不完全准确，因为CRC是一种特定的差错检测方法，它使用一种定义明确的算法以及一串校验位来检测消息是否已损坏。然而，将校验和称为CRC或CRC码的做法非常普遍。²关于CRC算法的优秀论述见Ross N. Williams撰写的这份在线文档（http://www.zlib.net/crc_v3.txt）</pre></td>
</tr></tbody></table>

## PDF page 456 — Chapter 16: Cyclic Redundancy Check

Focus: `numbers=0, 1, 111001102, 2, 8; negation=; conditions=if, when; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>added to original message. The receiver will use it, together with the generator polynomial, to check if the message is correct.

In practice, all CRC methods use polynomials in GF(2ⁿ). GF(pⁿ) stands for Galois field, also known as finite field, that is a field with a finite number of elements. As with any field, a Galois field is a set on which the operations of multiplication, addition, subtraction and division are defined and satisfy certain basic rules. The most common examples of finite fields are given by the integers modulo p, where p is a prime number. In our case, p is equal to 2 and this implies that the GF(2ⁿ) field contains only two elements, when n=1: 0 and 1.

In GF(2ⁿ) addition and subtraction are performed modulo 2, that is they correspond to the XOR logical operation.

⊕ 0 1 0 0 1 1 1 0

The multiplication, instead, corresponds to the AND logical operation.

∧0 1 0 0 0 1 0 1

Polynomials in GF(2ⁿ) are polynomials in a single variable x whose coefficients are either 0 or 1. The CRC technique interprets the bits of a data message as coefficients of a polynomial in GF(2ⁿ) with a degree equal to n −1, where n is the length of the message. For example, assuming the message 111001102, whose length is equal to 8, this corresponds to the polynomial:

x7 · 1 + x6 · 1 + x5 · 1 + x4 · 0 + x3 · 0 + x2 · 1 + x1 · 1 + x0 · 0 = x7 + x6 + x5 + x2 + x

As said before, in GF(2ⁿ) addition and subtraction correspond to XOR logical operation. This means that the sum of the polynomials x4 + x3 + 1 and x3 + x + 1 is equal to x4 + x³. Clearly, this is also the same of the subtraction of the two polynomials.

Multiplication of polynomials in GF(2ⁿ) is, as usual, much like multiplying decimal integers keeping track of powers of x instead of decimal places. For example, multiplying the previous two polynomials we have:

³Instead, in normal algebra the addition would be equal to x4 + 2x3 + x + 2.</pre></td>
<td><pre>添加到原始消息中。接收方将使用它，并结合生成多项式，来检查消息是否正确。

在实践中，所有 CRC 方法都使用 GF（2ⁿ）中的多项式。GF（pⁿ）代表伽罗瓦域，也称为有限域，即元素数量有限的域。与任何域一样，伽罗瓦域是一个集合，在其上定义了乘法、加法、减法和除法运算，并满足某些基本规则。有限域最常见的例子是模 p 的整数，其中 p 是一个质数。在我们的情况下，p 等于 2，这意味着 GF（2ⁿ）域仅包含两个元素，当 n=1 时：0 和 1。

在 GF（2ⁿ）中，加法和减法是按模 2 进行的，即它们对应于异或逻辑运算。

⊕ 0 1 0 0 1 1 1 0

而乘法则对应于与逻辑运算。

∧0 1 0 0 0 1 0 1

GF（2ⁿ）中的多项式是单变量 x 的多项式，其系数为 0 或 1。CRC 技术将数据消息的位解释为 GF（2ⁿ）中多项式的系数，其次数等于 n −1，其中 n 是消息的长度。例如，假设消息为 111001102，其长度等于 8，这对应于多项式：

x7 · 1 + x6 · 1 + x5 · 1 + x4 · 0 + x3 · 0 + x2 · 1 + x1 · 1 + x0 · 0 = x7 + x6 + x5 + x2 + x

如前所述，在 GF（2ⁿ）中，加法和减法对应于异或逻辑运算。这意味着多项式 x4 + x3 + 1 和 x3 + x + 1 的和等于 x4 + x³。显然，这两个多项式的差也是相同的。

GF（2ⁿ）中多项式的乘法，通常与十进制整数乘法类似，只是跟踪的是 x 的幂次而不是十进制位。例如，将上述两个多项式相乘，我们得到：

³相反，在常规代数中，加法将等于 x4 + 2x3 + x + 2。</pre></td>
</tr></tbody></table>

## PDF page 457 — Chapter 16: Cyclic Redundancy Check

Focus: `numbers=01, 02, 03, 04, 0457, 1, 457; negation=no; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>![Image from PDF page 457](../images/page-0457-image-01.png)

As you can see, each term in the first multiplies each term in the second, and then we add them following the addition rules in GF(2ⁿ).

Division of one polynomial by another in GF(2ⁿ) is analogous to long division (with remainder) of integers, except there is no borrowing nor carrying. For example, let us divide the polynomial x7 + x6 + x5 + x2 + x by the polynomial x3 + x + 1.

![Image from PDF page 457](../images/page-0457-image-02.png)

We start by dividing the first term of the dividend by the highest term of the divisor (meaning the one with the highest power of x, which in this case is x3). Next, we multiply the divisor by the result just obtained (the first term of the eventual quotient).

![Image from PDF page 457](../images/page-0457-image-03.png)

Now we subtract the product just obtained from the appropriate terms of the original dividend applying the rules of subtraction in GF(2ⁿ).

![Image from PDF page 457](../images/page-0457-image-04.png)

We repeat the previous steps, except this time use the two terms that have just been written as the dividend.</pre></td>
<td><pre>![Image from PDF page 457](../images/page-0457-image-01.png)

如你所见，第一个多项式中的每一项都与第二个多项式中的每一项相乘，然后按照 GF（2ⁿ）中的加法规则将它们相加。

在 GF（2ⁿ）中，一个多项式除以另一个多项式类似于整数的长除法（带余数），区别在于没有借位或进位。例如，让我们用多项式 x3 + x + 1 去除多项式 x7 + x6 + x5 + x2 + x。

![Image from PDF page 457](../images/page-0457-image-02.png)

首先，用被除数的第一项除以除数的最高次项（即 x 的最高次幂，在本例中为 x3）。然后，将除数乘以刚刚得到的结果（即最终商的第一项）。

![Image from PDF page 457](../images/page-0457-image-03.png)

现在，按照 GF（2ⁿ）中的减法规则，从原始被除数的相应项中减去刚刚得到的乘积。

![Image from PDF page 457](../images/page-0457-image-04.png)

重复上述步骤，但这次使用刚刚写出的两项作为被除数。</pre></td>
</tr></tbody></table>

## PDF page 458 — Chapter 16: Cyclic Redundancy Check

Focus: `numbers=0, 000001001100000100011101101101112, 01, 02, 0458, 0x04C1, 1, 16.1, 2, 32, 458; negation=cannot; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>![Image from PDF page 458](../images/page-0458-image-01.png)

The process continues until the obtained dividend has a degree lower than the divisor. We have so obtained the remainder of the division, which represents the checksum to append to the original message.

![Image from PDF page 458](../images/page-0458-image-02.png)

There are two ways for the receiver to assess the correctness of the transmission. It can compute the checksum from the first n bits of the received data, and verify that it agrees with the last r received bits. Alternatively, and following usual practice, the receiver can divide all the received bits by the generator polynomial and check that the r-bit remainder is 0.

However, the exact algorithm of CRC calculation usually differs from the normal polynomial division. Moreover, the generator polynomial may define specific initial and final condition, as we will see soon. This means that the generator polynomial cannot be left to change, but it is kept from a portfolio⁴ of well-studied polynomials. For example, the widely adopted CRC-32 polynomial has the form:

x26 + x23 + x22 + x16 + x12 + x11 + x10 + x8 + x7 + x5 + x4 + x2 + x + 1

which can be represented in binary with the sequence 000001001100000100011101101101112 and in hexadecimal with the number 0x04C1 1DB7. It is adopted by many transmission and storage protocols, like Ethernet, Serial ATA, MPEG-2, BZip2 and PNG.

### 16.1.1 CRC Calculation in STM32F1/F2/F4/L1 MCUs

The long division of polynomial is suitable to perform manual calculations. However, another more efficient CRC algorithm is the polynomial division with the bitwise message XORing technique,

⁴http://bit.ly/293h2Hd</pre></td>
<td><pre>![Image from PDF page 458](../images/page-0458-image-01.png)

该过程持续进行，直到所得到的被除数的次数低于除数的次数。至此，我们便得到了除法的余数，该余数即为需要附加到原始消息末尾的校验和。

![Image from PDF page 458](../images/page-0458-image-02.png)

接收方有两种方式来评估传输的正确性。它可以计算所接收数据前 n 个位的校验和，并验证其是否与最后接收到的 r 个位一致。或者，按照通常的做法，接收方可以将所有接收到的位除以生成多项式，并检查 r 位余数是否为 0。

然而，CRC 计算的具体算法通常与常规多项式除法有所不同。此外，生成多项式可能会定义特定的初始和最终条件，我们很快就会看到这一点。这意味着生成多项式不能随意更改，而是从一组⁴经过充分研究的多项式库中选取。例如，被广泛采用的 CRC-32 多项式具有以下形式：

x26 + x23 + x22 + x16 + x12 + x11 + x10 + x8 + x7 + x5 + x4 + x2 + x + 1

该值可以用二进制序列 000001001100000100011101101101112 表示，也可以用十六进制数 0x04C1 1DB7 表示。许多传输和存储协议都采用了该值，例如以太网、串行 ATA、MPEG-2、BZip2 和 PNG。

### 16.1.1 STM32F1/F2/F4/L1 微控制器中的 CRC 计算

多项式长除法适合进行手动计算。然而，另一种更高效的 CRC 算法是结合按位消息异或（XOR）技术的多项式除法，

⁴http://bit.ly/293h2Hd</pre></td>
</tr></tbody></table>

## PDF page 462 — Chapter 16: Cyclic Redundancy Check

Focus: `numbers=0x65, 0xFFFF, 1, 16, 16.2, 16.3, 32, 7, 8; negation=; conditions=if; identifiers=CRC_INPUTDATA_FORMAT_BYTES, CRC_INPUTDATA_FORMAT_HALFWORDS, CRC_INPUTDATA_FORMAT_WORDS, DEFAULT_INIT_VALUE_DISABLE, DEFAULT_INIT_VALUE_ENABLE, DEFAULT_POLYNO, DEFAULT_POLYNOMIAL_ENABLE, MIAL_DISABLE`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>```text
typedef struct {
CRC_TypeDef
*Instance;
/* Register base address
*/
CRC_InitTypeDef
Init;
/* CRC configuration parameters */
HAL_LockTypeDef
Lock;
/* CRC Locking object
*/
__IO HAL_CRC_StateTypeDef
State;
/* CRC communication state
*/
uint32_t InputDataFormat;
/* Specifies input data format. */
} CRC_HandleTypeDef;
```

The only relevant difference is the existence of the Init field, which is used to configure the CRC peripheral as we will see in a while, and the InputDataFormat field, which specifies the data size of the input data: it can assume a value from Table 16.2.

Table 16.2: Input data formats for the CRC peripheral

Data format Description

CRC_INPUTDATA_FORMAT_BYTES Input data is a stream of bytes (8-bit data) CRC_INPUTDATA_FORMAT_HALFWORDS Input data is a stream of half-words (16-bit data) CRC_INPUTDATA_FORMAT_WORDS Input data is a stream of words (32-bits data)

### To configure the CRC peripheral in those MCUs we use an instance of the CRC_InitTypeDef struct, which is defined in the following way:

```text
typedef struct {
uint8_t DefaultPolynomialUse;
/* Indicates if default polynomial is used */
uint8_t DefaultInitValueUse;
/* Indicates if default init value is used */
uint32_t GeneratingPolynomial;
/* Set CRC generating polynomial */
uint32_t CRCLength;
/* Indicates CRC length */
uint32_t InitValue;
/* Set the initial value to start CRC computation */
uint32_t InputDataInversionMode;
/* Specifies input data inversion mode */
uint32_t OutputDataInversionMode; /* Specifies output data (i.e. CRC) inversion mode */
} CRC_InitTypeDef;
```

### Let us analyze the fields of this struct:

- DefaultPolynomialUse: this field indicates if the default polynomial (that is, the CRC-32) or a custom one is used. It can assume the values DEFAULT_POLYNOMIAL_ENABLE or DEFAULT_POLYNO- MIAL_DISABLE. In this last case, the fields GeneratingPolynomial and CRCLength must be set.
- DefaultInitValueUse: this field indicates if the default CRC initialization value (that is, 0xFFFF FFFF) or a custom one is used. It can assume the values DEFAULT_INIT_VALUE_ENABLE or DEFAULT_INIT_VALUE_DISABLE. In this last case, the field InitValue must be set.
- GeneratingPolynomial: sets CRC generating polynomial. 7, 8, 16 or 32-bit long value for a polynomial degree equal to 7, 8, 16 or 32. This field is written in normal representation, e.g., for a polynomial of degree 7, X7 + X6 + X5 + X2 + 1 is written 0x65.
- CRCLength: this field indicates the length of the CRC, and it can assume a value from Table 16.3.</pre></td>
<td><pre>```text
typedef struct {
CRC_TypeDef
*Instance;
/* Register base address
*/
CRC_InitTypeDef
Init;
/* CRC configuration parameters */
HAL_LockTypeDef
Lock;
/* CRC Locking object
*/
__IO HAL_CRC_StateTypeDef
State;
/* CRC communication state
*/
uint32_t InputDataFormat;
/* Specifies input data format. */
} CRC_HandleTypeDef;
```

唯一相关的区别在于存在 Init 字段，该字段用于配置 CRC 外设（我们稍后会看到），以及 InputDataFormat 字段，该字段指定输入数据的大小：它可以取表 16.2 中的值。

表 16.2：CRC 外设的输入数据格式

数据格式 描述

CRC_INPUTDATA_FORMAT_BYTES 输入数据是字节流（8 位数据） CRC_INPUTDATA_FORMAT_HALFWORDS 输入数据是半字流（16 位数据） CRC_INPUTDATA_FORMAT_WORDS 输入数据是字流（32 位数据）

### 要配置这些微控制器中的 CRC 外设，我们使用 CRC_InitTypeDef 结构体的一个实例，其定义方式如下：

```text
typedef struct {
uint8_t DefaultPolynomialUse;
/* Indicates if default polynomial is used */
uint8_t DefaultInitValueUse;
/* Indicates if default init value is used */
uint32_t GeneratingPolynomial;
/* Set CRC generating polynomial */
uint32_t CRCLength;
/* Indicates CRC length */
uint32_t InitValue;
/* Set the initial value to start CRC computation */
uint32_t InputDataInversionMode;
/* Specifies input data inversion mode */
uint32_t OutputDataInversionMode; /* Specifies output data (i.e. CRC) inversion mode */
} CRC_InitTypeDef;
```

### 让我们分析该结构体的字段：

- DefaultPolynomialUse：此字段指示使用的是默认多项式（即 CRC-32）还是自定义多项式。它可以取值为 DEFAULT_POLYNOMIAL_ENABLE 或 DEFAULT_POLYNOMIAL_DISABLE。在后一种情况下，必须设置 GeneratingPolynomial 和 CRCLength 字段。
- DefaultInitValueUse：此字段指示使用的是默认 CRC 初始值（即 0xFFFFFFFF）还是自定义初始值。它可以取值为 DEFAULT_INIT_VALUE_ENABLE 或 DEFAULT_INIT_VALUE_DISABLE。在后一种情况下，必须设置 InitValue 字段。
- GeneratingPolynomial：设置 CRC 生成多项式。对于等于 7、8、16 或 32 的多项式阶数，其值为 7、8、16 或 32 位长。此字段以常规表示法写入，例如，对于 7 阶多项式，X7 + X6 + X5 + X2 + 1 被写为 0x65。
- CRCLength：此字段指示 CRC 的长度，它可以取表 16.3 中的值。</pre></td>
</tr></tbody></table>

## PDF page 468 — Chapter 17: IWDG and WWDG Timers

Focus: `numbers=0x3F, 0x40, 1, 17.2, 2, 22.5ms, 23, 4096, 43.6ms, 48000000, 8; negation=not; conditions=if, when; identifiers=PRESCALER_1, WWDG_IRQHandler, WWDG_PRESCALER_2, WWDG_PRESCALER_8`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>This represents the minimum timeout we have to wait before we can refresh the WWDG counter. The maximum timeout, instead, is represented by the lower and fixed value 0x40. Using again [2], we have that:

WWDGWMAX = 4096 · (23) · (0x3F + 1)

# 48000000 ≈43.6ms

This means that refreshing the WWDG timer before 22.5ms or after 43.6ms since the last refresh will cause a system reset.

WWDG has another important characteristic: when the counter reaches the value TI = 0x40, just one “tick” before the 0x3F value that will cause the MCU reset, a dedicate IRQ fires, if enabled. This interrupt, called Early Wakeup Interrupt (EWI), can be used to eventually refresh the WWDG timer in extremis, or to place the device in a safe state. The dedicated ISR is called WWDG_IRQHandler(), and it is the first ISR after the fifteen Cortex-M exceptions.

Finally, even the WWDG supports the hardware watchdog feature like the IWDG timer.

### 17.2.1 Using the CubeHAL to Program WWDG Timer

To manipulate the WWDG peripheral, the HAL defines the C struct WWDG_HandleTypeDef, which is defined in the following way:

```text
typedef struct {
WWDG_TypeDef
*Instance; /* Pointer to WWDG descriptor */
WWDG_InitTypeDef
Init;
/* WWDG initialization parameters */
HAL_LockTypeDef
Lock;
/* WWDG locking object
*/
__IO HAL_WWDG_StateTypeDef
State;
/* WWDG communication state */
} WWDG_HandleTypeDef;
```

To configure the WWDG peripheral we use an instance of the C struct WWDG_InitTypeDef, which is defined in the following way:

```text
typedef struct {
uint32_t Prescaler; /* Select the prescaler of the WWDG */
uint32_t Window;
/* Specifies the window value to be compared to the down-counter */
uint32_t Counter;
/* Specifies the WWDG down-counter reload value */
uint32_t EWIMode;
/* Specifies if WWDG Early Wakeup Interupt is enable or not.
This parameter can be a value of @ref WWDG_EWI_Mode */
} WWDG_InitTypeDef;
```

Let us study the fields of this C struct.

- Prescaler: this field specifies the prescaler value, and it can range from all powers of two between 1 and 8. To specify this value, the CubeHAL defines four different macros - WWDG_- PRESCALER_1, WWDG_PRESCALER_2, …, WWDG_PRESCALER_8.</pre></td>
<td><pre>这代表了我们必须等待的最小超时时间，之后才能刷新 WWDG 计数器。相反，最大超时时间由较低且固定的值 0x40 表示。再次使用 [2]，我们有：

WWDGWMAX = 4096 · (23) · (0x3F + 1)

# 48000000 ≈43.6ms

这意味着，如果在自上次刷新以来 22.5ms 之前或 43.6ms 之后刷新 WWDG 定时器，将导致系统复位。

WWDG 还有另一个重要特性：当计数器达到值 TI = 0x40 时，即在导致 MCU 复位的 0x3F 值之前的一个“tick”，如果已启用，则会触发一个专用中断。这个中断称为早期唤醒中断（Early Wakeup Interrupt, EWI），可用于在最后一刻刷新 WWDG 定时器，或将设备置于安全状态。专用的中断服务程序（ISR）名为 WWDG_IRQHandler()，它是紧随十五个 Cortex-M 异常之后的第一个 ISR。

最后，WWDG 也支持硬件看门狗功能，类似于 IWDG 定时器。

### 17.2.1 使用 CubeHAL 编程 WWDG 定时器

为了操作 WWDG 外设，HAL 定义了 C 结构体 WWDG_HandleTypeDef，其定义方式如下：

```text
typedef struct {
WWDG_TypeDef
*Instance; /* Pointer to WWDG descriptor */
WWDG_InitTypeDef
Init;
/* WWDG initialization parameters */
HAL_LockTypeDef
Lock;
/* WWDG locking object
*/
__IO HAL_WWDG_StateTypeDef
State;
/* WWDG communication state */
} WWDG_HandleTypeDef;
```

为了配置 WWDG 外设，我们使用 C 结构体 WWDG_InitTypeDef 的一个实例，其定义方式如下：

```text
typedef struct {
uint32_t Prescaler; /* Select the prescaler of the WWDG */
uint32_t Window;
/* Specifies the window value to be compared to the down-counter */
uint32_t Counter;
/* Specifies the WWDG down-counter reload value */
uint32_t EWIMode;
/* Specifies if WWDG Early Wakeup Interupt is enable or not.
This parameter can be a value of @ref WWDG_EWI_Mode */
} WWDG_InitTypeDef;
```

让我们研究一下这个 C 结构体的字段。

- Prescaler：此字段指定分频器值，它可以是 1 到 8 之间的所有 2 的幂次方。要指定此值，CubeHAL 定义了四个不同的宏 - WWDG_- PRESCALER_1, WWDG_PRESCALER_2, …, WWDG_PRESCALER_8。</pre></td>
</tr></tbody></table>

## PDF page 470 — Chapter 17: IWDG and WWDG Timers

Focus: `numbers=17.4, 17.5; negation=not; conditions=If, if, when; identifiers=RCC_FLAG_IWDGRST, RCC_FLAG_WWDGRST, __HAL_DBGMCU_FREEZE_IWDG, __HAL_DBGMCU_FREEZE_WWDG, __HAL_RCC_GET_FLAG`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>```text
__HAL_RCC_GET_FLAG(RCC_FLAG_IWDGRST);
```

while for the WWDG timer we can check this other flag:

```text
__HAL_RCC_GET_FLAG(RCC_FLAG_WWDGRST));
```

## 17.4 Freezing Watchdog Timers During a Debug Session

During a debug session, both WWDG and IWDG timers will keep counting. This will prevent us to carry out a step-by-step debugging. We can configure debug interface so that it halts watchdog timers when the MCU is halted using the following macros:

```text
__HAL_DBGMCU_FREEZE_IWDG();
__HAL_DBGMCU_FREEZE_WWDG();
```

## 17.5 Selecting the Right Watchdog Timer for Your Application

Both the watchdog timers have similar functionalities, and both do the same thing: to reset the MCU if we do not refresh their counter register in a given amount of time. But when it is best to prefer a timer over to other?

The IWDG timer is to prefer when we need to be sure that the main clock is working. Being the IWDG clocked by the independent LSI, it is useful to detect such malfunctions. Moreover, if we are using an RTOS, we can setup an independent thread configured with the maximum priority and that uses a software timer to refresh the IWDG timer periodically. This also helps us understanding that the kernel is properly scheduling threads.

The WWDG timer must be preferred to the IWDG one when we must be sure that some operations are carried out in a fixed and well-characterized temporal window. If that procedure takes less or more time, it will not be able to refresh the timer in the temporal window, causing a system reset. Moreover, the WWDG is the right choice if we want to perform critical operations (like putting the machine in a safe state or saving special data in non-volatile memory): thanks to the early-warning IRQ, we can get notified of the ongoing system reset.</pre></td>
<td><pre>```text
__HAL_RCC_GET_FLAG(RCC_FLAG_IWDGRST);
```

而对于 WWDG 定时器，我们可以检查另一个标志：

```text
__HAL_RCC_GET_FLAG(RCC_FLAG_WWDGRST));
```

## 17.4 在调试会话期间冻结看门狗定时器

在调试会话期间，WWDG 和 IWDG 定时器将继续计数。这将阻止我们进行单步调试。我们可以配置调试接口，以便在 MCU 停止时使用以下宏暂停看门狗定时器：

```text
__HAL_DBGMCU_FREEZE_IWDG();
__HAL_DBGMCU_FREEZE_WWDG();
```

## 17.5 为您的应用选择合适的看门狗定时器

两种看门狗定时器具有相似的功能，并且执行相同的工作：如果我们在给定时间内未刷新其计数器寄存器，则复位 MCU。但是，何时最好优先选择一种定时器而非另一种？

当我们需要确保主时钟正常工作时应优先选择 IWDG 定时器。由于 IWDG 由独立的 LSI 提供时钟，因此它有助于检测此类故障。此外，如果我们正在使用实时操作系统（RTOS），可以设置一个配置为最高优先级的独立线程，并使用软件定时器定期刷新 IWDG 定时器。这也有助于我们理解内核是否正在正确调度线程。

当我们需要确保某些操作在固定且特征明确的时间窗口内完成时，应优先选择 WWDG 定时器而非 IWDG 定时器。如果该过程花费的时间少于或多于该时间窗口，将无法在该时间窗口内刷新定时器，从而导致系统复位。此外，如果我们希望执行关键操作（例如将机器置于安全状态或将特殊数据保存到非易失性存储器中），WWDG 是合适的选择：借助早期警告中断（IRQ），我们可以获知系统复位正在进行中。</pre></td>
</tr></tbody></table>

## PDF page 474 — Chapter 18: Real-Time Clock

Focus: `numbers=1, 124, 127, 18.1, 18.2, 1MHz, 249, 255, 295, 32.768kHz, 32kHz, 37kHz, 4.22, 64, 7999; negation=disable, not; conditions=; identifiers=HAL_RTC_Init, HSE_RTC, RTC_OUTPUT_, RTC_OUTPUT_ALARMB, RTC_OUTPUT_DISABLE, RTC_OUTPUT_POLARITY_HIGH, RTC_OUTPUT_POLARITY_LOW, RTC_OUTPUT_TYPE_OPENDRAIN, RTC_OUTPUT_TYPE_PUSHPULL, RTC_OUTPUT_WAKEUP`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>equation [1], where CalendarCLK is one of LSI/LSE/HSE. At the time of writing this chapter, the latest CubeMX release (4.22) is not able to automatically derive the proper values for the AsynchPrediv and SynchPrediv fields. You can use the values reported in Table 18.1 for most relevant oscillator frequencies.

```text
CalendarCLK =
RTCCLK
(AsynchPrediv + 1)(SynchPrediv + 1)
[1]
```

Table 18.1: Correct values for the AsynchPrediv and SynchPrediv fields according to the most common clock sources

CalendarCLK AsynchPrediv SynchPrediv HSE_RTC = 1MHz 124 7999 LSE = 32.768kHz 127 255 LSI = 32kHz 127 249 LSI = 37kHz 127 295

- OutPut: specifies the signal I/O routed to the RTC output. It can assume the values RTC_OUTPUT_- ALARMA, RTC_OUTPUT_ALARMB, RTC_OUTPUT_WAKEUP and RTC_OUTPUT_DISABLE to route the output to the signal related to Alarm A, B, Wakeup or to disable the output signal. Please, take note that the actual GPIO associated to a given alarm is designed during the MCU development and it is fixed. Depending on the type of package used, just one signal I/O may be available and shared between the three alarm sources. For example, all STM32 MCU with LQFP-64 package have just one alarm I/O named AF1 and connected to the PC13 pin.
- OutPutPolarity: this field specifies the output polarity of the signal, and it can assume the values RTC_OUTPUT_POLARITY_HIGH and RTC_OUTPUT_POLARITY_LOW.
- OutPutType: this field specifies the type of the output signal, and it can assume the values RTC_OUTPUT_TYPE_OPENDRAIN and RTC_OUTPUT_TYPE_PUSHPULL.

As usual, to configure the RTC peripheral we use the function:

```text
HAL_StatusTypeDef HAL_RTC_Init(RTC_HandleTypeDef *hrtc);
```

which accepts a pointer to an instance of the RTC_HandleTypeDef struct seen before.

### 18.2.1 Setting and Retrieving the Current Date/Time

The CubeHAL implements separated routines and C structs to set and retrieve the current date and time. The functions:</pre></td>
<td><pre>公式 [1]，其中 `CalendarCLK` 是 LSI/LSE/HSE 之一。在撰写本章时，最新的 CubeMX 版本（4.22）无法自动推导 `AsynchPrediv` 和 `SynchPrediv` 字段的正确值。对于大多数相关的振荡器频率，您可以使用表 18.1 中报告的数值。

```text
CalendarCLK =
RTCCLK
(AsynchPrediv + 1)(SynchPrediv + 1)
[1]
```

表 18.1：根据最常见的时钟源，`AsynchPrediv` 和 `SynchPrediv` 字段的正确值

CalendarCLK AsynchPrediv SynchPrediv HSE_RTC = 1MHz 124 7999 LSE = 32.768kHz 127 255 LSI = 32kHz 127 249 LSI = 37kHz 127 295

- `OutPut`：指定路由到 RTC 输出的信号 I/O。它可以取值为 `RTC_OUTPUT_ALARMA`、`RTC_OUTPUT_ALARMB`、`RTC_OUTPUT_WAKEUP` 和 `RTC_OUTPUT_DISABLE`，以将输出路由到与报警 A、B、唤醒相关的信号，或禁用输出信号。请注意，与特定报警关联的实际 GPIO 是在微控制器开发期间设计的，并且是固定的。根据所使用的封装类型，可能只有一个信号 I/O 可用，并在三个报警源之间共享。例如，所有具有 LQFP-64 封装的 STM32 微控制器只有一个名为 AF1 的报警 I/O，并连接到 PC13 引脚。
- `OutPutPolarity`：此字段指定信号的输出极性，它可以取值为 `RTC_OUTPUT_POLARITY_HIGH` 和 `RTC_OUTPUT_POLARITY_LOW`。
- `OutPutType`：此字段指定输出信号的类型，它可以取值为 `RTC_OUTPUT_TYPE_OPENDRAIN` 和 `RTC_OUTPUT_TYPE_PUSHPULL`。

通常，为了配置 RTC 外设，我们使用函数：

```text
HAL_StatusTypeDef HAL_RTC_Init(RTC_HandleTypeDef *hrtc);
```

该函数接受指向之前看到的 `RTC_HandleTypeDef` 结构体实例的指针。

### 18.2.1 设置和获取当前日期/时间

CubeHAL 实现了独立的例程和 C 结构体来设置和获取当前日期和时间。函数：</pre></td>
</tr></tbody></table>

## PDF page 478 — Chapter 18: Real-Time Clock

Focus: `numbers=03, 12, 18.2, 45; negation=; conditions=If, When, if, when; identifiers=HAL_RTC_AlarmAEventCallback, HAL_RTC_AlarmIRQHandler, HAL_RTC_DeactivateAlarm, HAL_RTC_PollForAlarmAEvent, HAL_RTC_SetAlarm, HAL_RTC_SetAlarm_IT, RTC_ALARMMASK_HOURS, RTC_ALARMMASK_NONE`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>```text
HAL_StatusTypeDef HAL_RTC_SetAlarm(RTC_HandleTypeDef *hrtc,
RTC_AlarmTypeDef *sAlarm, uint32_t Format);
```

We can eventually poll an alarm until the event has occurred by using the function:

```text
HAL_StatusTypeDef HAL_RTC_PollForAlarmAEvent(RTC_HandleTypeDef *hrtc, uint32_t Timeout);
```

An alarm can be configured so that it asserts a dedicated interrupt when it fires. The IRQ associated to both the alarms is the RTC_Alarm_IRQn, and to configure an alarm in interrupt mode we can use the following dedicated routine:

```text
HAL_StatusTypeDef HAL_RTC_SetAlarm_IT(RTC_HandleTypeDef *hrtc,
RTC_AlarmTypeDef *sAlarm, uint32_t Format);
```

Like all CubeHAL interrupt handler routines, we need to invoke the HAL_RTC_AlarmIRQHandler() from the RTC_Alarm_IRQn ISR. To be notified from the alarm event, we can implement the corresponding callback:

```text
void HAL_RTC_AlarmAEventCallback(RTC_HandleTypeDef *hrtc)
```

An alarm can be deactivated by using the function:

```text
HAL_StatusTypeDef HAL_RTC_DeactivateAlarm(RTC_HandleTypeDef *hrtc, uint32_t Alarm);
```

The struct RTC_AlarmTypeDef, used to setup an alarm, is defined in the following way:

```text
typedef struct {
RTC_TimeTypeDef AlarmTime;
/* Specifies the RTC Alarm Time members */
uint32_t AlarmMask;
/* Specifies the RTC Alarm Masks. */
uint32_t AlarmSubSecondMask;
/* Specifies the RTC Alarm SubSeconds Masks. */
uint32_t AlarmDateWeekDaySel; /* Specifies the RTC Alarm is on Date or WeekDay. */
uint8_t AlarmDateWeekDay;
/* Specifies the RTC Alarm Date/WeekDay. */
uint32_t Alarm;
/* Specifies the alarm (A or B). */
} RTC_AlarmTypeDef;
```

- AlarmTime: this field is an instance of the RTC_TimeTypeDef struct seen before, and it is used to setup the alarm time.
- AlarmMask: an alarm consists of a register with the same length as the RTC time counter. When the RTC counter matches the value configured in the alarm register, it generates an event. The AlarmMask field defines the comparison criteria between the alarm and the RTC time register. It can assume one or more values (by bit-masking them) from those reported in Table 18.2. For example, if we want that the alarm occurs at 12:45:03, we use the RTC_ALARMMASK_NONE value. If, instead, we want to generate an alarm every hour, at a given minute and second, we can use the value RTC_ALARMMASK_HOURS.</pre></td>
<td><pre>```text
HAL_StatusTypeDef HAL_RTC_SetAlarm(RTC_HandleTypeDef *hrtc,
RTC_AlarmTypeDef *sAlarm, uint32_t Format);
```

我们最终可以通过使用以下函数轮询闹钟，直到事件发生：

```text
HAL_StatusTypeDef HAL_RTC_PollForAlarmAEvent(RTC_HandleTypeDef *hrtc, uint32_t Timeout);
```

可以配置闹钟，使其在触发时断言一个专用的中断。与两个闹钟关联的中断请求号（IRQ）均为 RTC_Alarm_IRQn，要配置闹钟处于中断模式，我们可以使用以下专用例程：

```text
HAL_StatusTypeDef HAL_RTC_SetAlarm_IT(RTC_HandleTypeDef *hrtc,
RTC_AlarmTypeDef *sAlarm, uint32_t Format);
```

与所有 CubeHAL 中断处理例程一样，我们需要从 RTC_Alarm_IRQn 的中断服务例程（ISR）中调用 HAL_RTC_AlarmIRQHandler()。为了接收闹钟事件的通知，我们可以实现相应的回调函数：

```text
void HAL_RTC_AlarmAEventCallback(RTC_HandleTypeDef *hrtc)
```

可以使用以下函数来停用闹钟：

```text
HAL_StatusTypeDef HAL_RTC_DeactivateAlarm(RTC_HandleTypeDef *hrtc, uint32_t Alarm);
```

用于设置闹钟的结构体 RTC_AlarmTypeDef 定义如下：

```text
typedef struct {
RTC_TimeTypeDef AlarmTime;
/* Specifies the RTC Alarm Time members */
uint32_t AlarmMask;
/* Specifies the RTC Alarm Masks. */
uint32_t AlarmSubSecondMask;
/* Specifies the RTC Alarm SubSeconds Masks. */
uint32_t AlarmDateWeekDaySel; /* Specifies the RTC Alarm is on Date or WeekDay. */
uint8_t AlarmDateWeekDay;
/* Specifies the RTC Alarm Date/WeekDay. */
uint32_t Alarm;
/* Specifies the alarm (A or B). */
} RTC_AlarmTypeDef;
```

- AlarmTime：此字段是之前看到的 RTC_TimeTypeDef 结构体的一个实例，用于设置闹钟时间。
- AlarmMask：闹钟由一个与 RTC 时间计数器长度相同的寄存器组成。当 RTC 计数器与闹钟寄存器中配置的值匹配时，它会生成一个事件。AlarmMask 字段定义了闹钟与 RTC 时间寄存器之间的比较标准。它可以采用表 18.2 中报告的一个或多个值（通过对它们进行位掩码操作）。例如，如果我们希望闹钟在 12:45:03 发生，我们使用 RTC_ALARMMASK_NONE 值。相反，如果我们希望每小时在指定的分钟和秒生成一次闹钟，我们可以使用值 RTC_ALARMMASK_HOURS。</pre></td>
</tr></tbody></table>

## PDF page 490 — Chapter 19: Power Management

Focus: `numbers=01, 0490, 1, 100ms, 19.1, 23, 490, 500, 500ms; negation=not; conditions=If, When, if, when; identifiers=HAL_Delay, HAL_GPIO_TogglePin`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>![Image from PDF page 490](../images/page-0490-image-01.png)

Figure 19.1: How a firmware could potentially manage clock speed and power modes during its activity

The Figure 19.1 shows a possible strategy for the minimization of power consumption. During the microcontroller booting process, the MCU runs at its maximum speed to allow a fast completion of all initialization activities. When all peripherals are configured, the clock speed is lowered and the MCU enters in sleep modes. In this period, the MCU is woken-up by interrupts that can be processed at lower CPU speeds. When CPU-intensive operations need to be carried out, the clock speed can be increased up to the maximum, and then decreased again once finished.

So, when to go into sleep mode? As said before, it is up to us to decide the right time to place the MCU in one of the possible sleep modes. If we know that the MCU is waiting for asynchronous events notified with interrupts, then it could be the right time to go into sleep mode instead of doing busy-wait. Let us consider the classical blinking LED application we have seen several times in this book.

```text
...
while(1) {
HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
HAL_Delay(500);
}
```

This apparently innocent code has a dramatic impact on the power consumption of our device. Even if we do not have too much to do during those 500ms, we waste a lot of power checking the value of the global SysTick tick count to see if that time has been elapsed. Instead, we can rearrange that code to stay in sleep mode for most of the time, and we can set up a timer that wakes up the MCU after 100ms.

Letting other software components decide when to place the MCU in sleep mode could represent another approach. As we will discover in Chapter 23, a Real-Time Operating System may be programmed to automatically put the MCU in sleep mode when there is nothing to do⁵.

⁵We will discover in that chapter that one possible strategy consists in placing the MCU in sleep mode when the idle thread is scheduled. The idle thread is that thread executed by an RTOS when all other threads are “un-runnable”. This clearly means that the MCU has nothing relevant to do, and it can be placed in sleep mode safely.</pre></td>
<td><pre>![Image from PDF page 490](../images/page-0490-image-01.png)

图 19.1：固件如何潜在地管理其活动期间的时钟速度和电源模式

图 19.1 展示了一种最小化功耗的可能策略。在微控制器启动过程中，微控制器以最大速度运行，以允许快速完成所有初始化活动。当所有外设配置完成后，时钟速度降低，微控制器进入睡眠模式。在此期间，微控制器由中断唤醒，这些中断可以在较低的 CPU 速度下处理。当需要执行 CPU 密集型操作时，时钟速度可以增加到最大值，完成后再次降低。

那么，何时进入睡眠模式？如前所述，由我们决定将微控制器置于可能的睡眠模式之一的正确时间。如果我们知道微控制器正在等待通过中断通知的异步事件，那么进入睡眠模式而不是进行忙等待可能是正确的时机。让我们考虑一下我们在本书中多次看到的经典闪烁 LED 应用。

```text
...
while(1) {
HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
HAL_Delay(500);
}
```

这段看似无害的代码对我们设备的功耗有巨大影响。即使在那 500ms 内我们没有太多事情要做，我们也在浪费大量电力来检查全局 SysTick 计数值，以查看该时间是否已过。相反，我们可以重新排列该代码，使其大部分时间保持在睡眠模式，并设置一个定时器，在 100ms 后唤醒微控制器。

让其他软件组件决定何时将微控制器置于睡眠模式可以代表另一种方法。正如我们将在第 23 章中发现的，实时操作系统（Real-Time Operating System）可以被编程为在无事可做时自动将微控制器置于睡眠模式⁵。

⁵我们将在该章中发现，一种可能的策略是在空闲线程被调度时将微控制器置于睡眠模式。空闲线程是当所有其他线程都“不可运行”时由实时操作系统执行的那个线程。这显然意味着微控制器没有相关的事情要做，可以安全地将其置于睡眠模式。</pre></td>
</tr></tbody></table>

## PDF page 499 — Chapter 19: Power Management

Focus: `numbers=1, 1.8V, 19.3, 2.3; negation=disable, disabled, no, not; conditions=If, Otherwise, When, if, when; identifiers=HAL_PWR_EnterSTOPMode, PWR_LOWPOWERREGULATOR_ON, PWR_MAINREGULATOR_ON, PWR_STOPENTRY_WFE, PWR_STOPENTRY_WFI`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>If the WFI instruction is used to enter in sleep mode, any peripheral interrupt acknowledged by the nested vectored interrupt controller (NVIC) can wake up the device from sleep mode. If the WFE instruction is used to enter sleep mode, the MCU exits sleep mode as soon as an event occurs. The wakeup event can be generated either by:

- enabling an interrupt in the peripheral control register but not in the NVIC, and enabling the SEVONPEND bit in the System Control Registe - When the MCU resumes from WFE, the peripheral interrupt pending bit and the peripheral NVIC IRQ channel pending bit (in the NVIC interrupt clear pending register) have to be cleared;
- or configuring an external or internal EXTI line in event mode - When the CPU resumes from WFE, it is not necessary to clear the peripheral interrupt pending bit or the NVIC IRQ channel pending bit as the pending bit corresponding to the event line is not set.

This mode offers the lowest wakeup time as no time is wasted in interrupt entry/exit.

#### 19.3.2.3 Stop Mode

The stop mode is based on the Cortex-M deep sleep mode combined with peripheral clock gating. In stop mode all clocks in the 1.8V domain are stopped, the PLL, the HSI and the HSE oscillators are disabled. SRAM and register contents are preserved. In the stop mode, all I/O pins keep the same state as in the run mode. The voltage regulator can be configured either in normal or low-power mode. To place the MCU in stop mode the HAL provides the function:

```text
void HAL_PWR_EnterSTOPMode(uint32_t Regulator, uint8_t STOPEntry);
```

where the Regulator parameter accepts the value PWR_MAINREGULATOR_ON to leave the internal voltage regulator ON, or the value PWR_LOWPOWERREGULATOR_ON to place it in low-power mode. The parameter STOPEntry can assume the values PWR_STOPENTRY_WFI or PWR_STOPENTRY_WFE.

To enter stop mode, all EXTI-line pending bits, all peripherals interrupt pending bits and RTC Alarm flag must be reset. Otherwise, the stop mode entry procedure is ignored, and program execution continues. If the application needs to disable the external high-speed oscillator (HSE) before entering stop mode, the system clock source must be first switched to HSI and then clear the HSEON bit. Otherwise, if before entering stop mode the HSEON bit is kept at 1, the security system (CSS) feature must be enabled to detect any external oscillator (external clock) failure and avoid a malfunction when entering stop mode.

Any EXTI-line configured in interrupt or event mode forces the CPU to exit from stop mode, according if it entered in low-power mode using the WFI or WFE instruction. Since both HSE and PLL are disabled before entering in stop mode, when exiting from this low-power mode the MCU source clock is set to the HSI. This means that our code shall reconfigure the clock tree according to wanted SYSCLK speed.</pre></td>
<td><pre>如果使用 WFI 指令进入睡眠模式，任何由嵌套向量中断控制器 (NVIC) 确认的外设中断都可以将器件从睡眠模式唤醒。如果使用 WFE 指令进入睡眠模式，一旦发生事件，MCU 即退出睡眠模式。唤醒事件可以由以下任一方式产生：

- 在外设控制寄存器中使能中断，但在 NVIC 中未使能，并在系统控制寄存器 (System Control Register) 中使能 SEVONPEND 位 - 当 MCU 从 WFE 恢复时，必须清除外设中断挂起位和外设 NVIC IRQ 通道挂起位（位于 NVIC 中断清除挂起寄存器中）；
- 或者将外部或内部 EXTI 线配置为事件模式 - 当 CPU 从 WFE 恢复时，无需清除外设中断挂起位或 NVIC IRQ 通道挂起位，因为对应于事件线的挂起位未被置位。

此模式提供最短的唤醒时间，因为在中断进入/退出过程中没有浪费时间。

#### 19.3.2.3 停止模式

停止模式基于 Cortex-M 深度睡眠模式并结合外设时钟门控。在停止模式下，1.8V 域中的所有时钟停止，PLL、HSI 和 HSE 振荡器被禁用。SRAM 和寄存器内容得以保留。在停止模式下，所有 I/O 引脚保持与运行模式相同的状态。电压调节器可配置为正常模式或低功耗模式。为使 MCU 进入停止模式，HAL 提供了以下函数：

```text
void HAL_PWR_EnterSTOPMode(uint32_t Regulator, uint8_t STOPEntry);
```

其中，Regulator 参数接受值 PWR_MAINREGULATOR_ON 以保持内部电压调节器开启，或接受值 PWR_LOWPOWERREGULATOR_ON 将其置于低功耗模式。参数 STOPEntry 可以取值为 PWR_STOPENTRY_WFI 或 PWR_STOPENTRY_WFE。

要进入停止模式，所有 EXTI 线挂起位、所有外设中断挂起位以及 RTC 闹钟标志必须被复位。否则，停止模式进入过程将被忽略，程序执行将继续。如果应用程序需要在进入停止模式之前禁用外部高速振荡器 (HSE)，则必须先将系统时钟源切换到 HSI，然后清除 HSEON 位。否则，如果在进入停止模式之前 HSEON 位保持为 1，则必须启用安全系统 (CSS) 功能以检测任何外部振荡器（外部时钟）故障，并避免在进入停止模式时发生故障。

任何配置为中断或事件模式的 EXTI 线都会强制 CPU 退出停止模式，具体取决于它是使用 WFI 还是 WFE 指令进入低功耗模式的。由于在进入停止模式之前 HSE 和 PLL 均被禁用，因此当退出此低功耗模式时，MCU 源时钟被设置为 HSI。这意味着我们的代码必须根据所需的 SYSCLK 速度重新配置时钟树。</pre></td>
</tr></tbody></table>

## PDF page 502 — Chapter 19: Power Management

Focus: `numbers=0, 1, 100, 101, 102, 103, 104, 105, 106, 1ms, 200, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73; negation=Disable, Never, disabled; conditions=Otherwise, if, when; identifiers=GPIO_MODE_IT_RISING, GPIO_NOPULL, GPIO_PIN_13, GPIO_PIN_SET, HAL_Delay, HAL_GPIO_Init, HAL_GPIO_ReadPin, HAL_MAX_DELAY, HAL_PWR_EnterSLEEPMode, HAL_ResumeTick, HAL_SuspendTick, HAL_UART_DeInit, HAL_UART_Transmit, MX_GPIO_Deinit, MX_GPIO_Init, MX_USART2_UART_Init, PWR_SLEEPENTRY_WFI, __HAL_RCC_GPIOC_CLK_ENABLE, __HAL_RCC_PWR_CLK_ENABLE, sprintf`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>60

```text
61
while(HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_13) == GPIO_PIN_SET);
62
HAL_Delay(200);
```

63

```text
64
sprintf(msg, &quot;Entering in STANDBY mode\r\n&quot;);
65
HAL_UART_Transmit(&amp;huart2, (uint8_t*)msg, strlen(msg), HAL_MAX_DELAY);
```

66

```text
67
StandbyMode();
```

68

```text
69
while(1); //Never arrives here, since MCU is reset when exiting from STANDBY
70
}
71
}
```

72

73

```text
74
void SleepMode(void)
75
{
76
GPIO_InitTypeDef GPIO_InitStruct;
```

77

```text
78
/* Disable all GPIOs to reduce power */
79
MX_GPIO_Deinit();
```

80

```text
81
/* Configure User push-button as external interrupt generator */
82
__HAL_RCC_GPIOC_CLK_ENABLE();
83
GPIO_InitStruct.Pin = B1_Pin;
84
GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
85
GPIO_InitStruct.Pull = GPIO_NOPULL;
86
HAL_GPIO_Init(B1_GPIO_Port, &amp;GPIO_InitStruct);
```

87

```text
88
HAL_UART_DeInit(&amp;huart2);
```

89

```text
90
/* Suspend Tick increment to prevent wakeup by Systick interrupt.
91
Otherwise the Systick interrupt will wake up the device within 1ms (HAL time base) */
92
HAL_SuspendTick();
```

93

```text
94
__HAL_RCC_PWR_CLK_ENABLE();
95
/* Request to enter SLEEP mode */
96
HAL_PWR_EnterSLEEPMode(0, PWR_SLEEPENTRY_WFI);
```

97

```text
98
/* Resume Tick interrupt if disabled prior to sleep mode entry*/
99
HAL_ResumeTick();
100
101
/* Reinitialize GPIOs */
102
MX_GPIO_Init();
103
104
/* Reinitialize UART2 */
105
MX_USART2_UART_Init();
106
}
```</pre></td>
<td><pre>60

```text
61
while(HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_13) == GPIO_PIN_SET);
62
HAL_Delay(200);
```

63

```text
64
sprintf(msg, &quot;Entering in STANDBY mode\r\n&quot;);
65
HAL_UART_Transmit(&amp;huart2, (uint8_t*)msg, strlen(msg), HAL_MAX_DELAY);
```

66

```text
67
StandbyMode();
```

68

```text
69
while(1); //Never arrives here, since MCU is reset when exiting from STANDBY
70
}
71
}
```

72

73

```text
74
void SleepMode(void)
75
{
76
GPIO_InitTypeDef GPIO_InitStruct;
```

77

```text
78
/* Disable all GPIOs to reduce power */
79
MX_GPIO_Deinit();
```

80

```text
81
/* Configure User push-button as external interrupt generator */
82
__HAL_RCC_GPIOC_CLK_ENABLE();
83
GPIO_InitStruct.Pin = B1_Pin;
84
GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
85
GPIO_InitStruct.Pull = GPIO_NOPULL;
86
HAL_GPIO_Init(B1_GPIO_Port, &amp;GPIO_InitStruct);
```

87

```text
88
HAL_UART_DeInit(&amp;huart2);
```

89

```text
90
/* Suspend Tick increment to prevent wakeup by Systick interrupt.
91
Otherwise the Systick interrupt will wake up the device within 1ms (HAL time base) */
92
HAL_SuspendTick();
```

93

```text
94
__HAL_RCC_PWR_CLK_ENABLE();
95
/* Request to enter SLEEP mode */
96
HAL_PWR_EnterSLEEPMode(0, PWR_SLEEPENTRY_WFI);
```

97

```text
98
/* Resume Tick interrupt if disabled prior to sleep mode entry*/
99
HAL_ResumeTick();
100
101
/* Reinitialize GPIOs */
102
MX_GPIO_Init();
103
104
/* Reinitialize UART2 */
105
MX_USART2_UART_Init();
106
}
```</pre></td>
</tr></tbody></table>

## PDF page 523 — Chapter 20: Memory layout

Focus: `numbers=01, 0523, 20.1, 20.2, 3, 5, 523; negation=; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>### 20.1.3 Understanding Compilation and Linking Processes

The process that goes from the compilation of the C source code to the generation of the final binary image to flash on our MCU involves several steps and tools provided by the GCC tool-chain. The Figure 20.2 tries to outline this process. All starts from the C source files. They usually contain the following program structures.

![Image from PDF page 523](../images/page-0523-image-01.png)

Figure 20.2: The compilation process from the source file to the final binary image

- Global variables: these can be in turn divided between un-initialized and initialized variables; a global variable can also defined as static, that is its visibility is limited to the current source file.
- Local variables: these can be divided between simple local (also called automatic) variables and static local variables (that is those variables whose lifetime extends across the entire run of the program).
- Const data: these can be in turn divided between const data types (e.g. const int c = 5) and string constants (e.g. &quot;Hello World!&quot;).
- Routines: these constitute the program and they will be translated in assembly instructions.
- External resources: these are both global variables (declared as extern) and routines defined in other source files. It will be a linker job to “link” the references to these symbols defined in other source files and to merge the sections coming from the corresponding binary files.

Once a source file is compiled, the above program structures are mapped inside specific sections of the binary file. The Table 20.1 summarizes the most relevant ones.</pre></td>
<td><pre>### 20.1.3 理解编译和链接过程

从 C 源代码的编译到生成最终用于烧录到我们微控制器（MCU）的二进制映像的过程，涉及 GCC 工具链（toolchain）提供的多个步骤和工具。图 20.2 试图概述这一过程。一切始于 C 源文件。它们通常包含以下程序结构。

![Image from PDF page 523](../images/page-0523-image-01.png)

图 20.2：从源文件到最终二进制映像的编译过程

- 全局变量：这些变量可以进一步分为未初始化和已初始化变量；全局变量也可以定义为静态（static），即其可见性仅限于当前源文件。
- 局部变量：这些变量可以分为简单的局部变量（也称为自动变量）和静态局部变量（即那些生命周期贯穿整个程序运行期间的变量）。
- 常量数据：这些可以进一步分为常量数据类型（例如 `const int c = 5`）和字符串常量（例如 `&quot;Hello World!&quot;`）。
- 例程：这些构成了程序，它们将被翻译为汇编指令。
- 外部资源：这些既包括全局变量（声明为 `extern`），也包括在其他源文件中定义的例程。链接器的工作是“链接”指向这些在其他源文件中定义的符号的引用，并合并来自相应二进制文件的节（section）。

一旦源文件被编译，上述程序结构就被映射到二进制文件中的特定节中。表 20.1 总结了其中最重要的部分。</pre></td>
</tr></tbody></table>

## PDF page 531 — Chapter 20: Memory layout

Focus: `numbers=01, 0531, 0x0, 0x1, 0x20, 0x3f, 0x4, 0x400, 10, 11, 2, 20.2, 200000, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47; negation=disable, not; conditions=if, when; identifiers=GPIOA_MODER, GPIOA_ODR, RCC_APB1ENR`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>![Image from PDF page 531](../images/page-0531-image-01.jpeg)

The Build Analyzer view

### 20.2.2 .data and .bss Sections Initialization

Let us introduce a minor modification to the previous example.

```text
36
volatile uint32_t dataVar = 0x3f;
```

37

```text
38
int main() {
39
/* enable clock on GPIOA and GPIOC peripherals */
40
*RCC_APB1ENR = 0x1 | 0x4;
41
*GPIOA_MODER |= 0x400; // Sets MODER[11:10] = 0x1
```

42

```text
43
while(dataVar == 0x3f) { // This is always true
44
*GPIOA_ODR = 0x20;
45
delay(200000);
46
*GPIOA_ODR = 0x0;
47
delay(200000);
48
}
49
}
```

This time we use a global initialized variable, dataVar to start the blinking loop. The variable has been declared volatile just to avoid that the compiler optimizes it (however, when compiling this example, disable all optimizations [-ON] in the project settings). Looking at the code, we can reach to the conclusion that it does the same thing of the previous example. However, if you try to flash your Nucleo, you will see that the LD2 LED does not blink. Why not?

To understand what’s happening, we have to review some things from the C programming language. Consider the following code fragment:</pre></td>
<td><pre>![Image from PDF page 531](../images/page-0531-image-01.jpeg)

构建分析器视图

### 20.2.2 .data 和 .bss 段的初始化

让我们对前面的示例做一个小的修改。

```text
36
volatile uint32_t dataVar = 0x3f;
```

37

```text
38
int main() {
39
/* enable clock on GPIOA and GPIOC peripherals */
40
*RCC_APB1ENR = 0x1 | 0x4;
41
*GPIOA_MODER |= 0x400; // Sets MODER[11:10] = 0x1
```

42

```text
43
while(dataVar == 0x3f) { // This is always true
44
*GPIOA_ODR = 0x20;
45
delay(200000);
46
*GPIOA_ODR = 0x0;
47
delay(200000);
48
}
49
}
```

这次我们使用一个全局初始化变量 dataVar 来启动闪烁循环。该变量被声明为 volatile，仅仅是为了避免编译器对其进行优化（不过，在编译此示例时，请在项目设置中禁用所有优化 [-ON]）。查看代码，我们可以得出结论，它执行的操作与前面的示例相同。然而，如果你尝试将程序烧录到 Nucleo 开发板上，你会发现 LD2 LED 不会闪烁。这是为什么？

为了理解正在发生的事情，我们需要回顾一些 C 编程语言的知识。考虑以下代码片段：</pre></td>
</tr></tbody></table>

## PDF page 573 — Chapter 21: Flash Memory Management

Focus: `numbers=01, 02, 0573, 1, 21.1, 21.3, 573; negation=disable, not; conditions=if; identifiers=HAL_FLASH_OB_Launch`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>```text
HAL_StatusTypeDef HAL_FLASH_OB_Launch(void);
```

Please take note that changing some option bits in some STM32 MCUs may cause a reset of the chip.

Finally, the ST STM32CubeProgrammer provides the ability to easily modify the option bytes. Once you have connected the ST-LINK debugger to the target MCU, click on the Option bytes icon (the third green icon on the left). The Option bytes section appears, as shown in Figure 21.1. The same STM32CubeProgrammer tool also allows to erase selected flash sectors/pages.

![Image from PDF page 573](../images/page-0573-image-01.jpeg)

Figure 21.1: The Option Bytes configuration dialog in the STM32CubeProgrammer

### 21.3.1 Flash Memory Read Protection

Read Carefully

![Image from PDF page 573](../images/page-0573-image-02.png)

Some procedures described in this paragraph may brick your microcontroller preventing you from flashing and erasing it forever. Read carefully the content of this paragraph and avoid performing operations if they are not totally clear.

One option byte (called RDP) deserves a separated paragraph: the configuration byte related to the flash read protection. To avoid unwanted access to the flash memory through the debug interface it is possible to temporarily or permanently disable the read access to this memory from the external world (clearly, the access from the CPU core and the DMA controllers is always possible). There exist three protection levels, which correspond to three different values to store in the option byte:</pre></td>
<td><pre>```text
HAL_StatusTypeDef HAL_FLASH_OB_Launch(void);
```

请注意，在某些 STM32 微控制器中更改某些选项位可能会导致芯片复位。

最后，ST STM32CubeProgrammer 提供了轻松修改选项字节的功能。一旦你将 ST-LINK 调试器连接到目标 MCU，点击选项字节图标（左侧第三个绿色图标）。将出现选项字节部分，如图 21.1 所示。相同的 STM32CubeProgrammer 工具还允许擦除选定的闪存扇区/页面。

![Image from PDF page 573](../images/page-0573-image-01.jpeg)

图 21.1：STM32CubeProgrammer 中的选项字节配置对话框

### 21.3.1 Flash Memory Read Protection

Read Carefully

![Image from PDF page 573](../images/page-0573-image-02.png)

本段中描述的一些操作可能会导致您的微控制器（microcontroller）变砖，从而永久无法对其进行烧录和擦除。请仔细阅读本段内容，如果某些操作不完全清晰，请避免执行。

一个选项字节（称为 RDP）值得单独讨论：即与闪存读取保护相关的配置字节。为了避免通过调试接口对闪存进行非预期的访问，可以临时或永久地禁用来自外部世界对该存储器的读取访问（显然，来自 CPU 内核（core）和直接存储器访问（direct memory access）控制器的访问始终是允许的）。存在三个保护级别，对应存储在选项字节中的三个不同值：</pre></td>
</tr></tbody></table>

## PDF page 578 — Chapter 21: Flash Memory Management

Focus: `numbers=1, 128, 16, 256, 32, 64; negation=not, without; conditions=If, When, if; identifiers=INSTRUCTION_CACHE_ENABLE, PREFETCH_ENABLE`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>designed so that it preservers the Harvard architecture of Cortex-M microcontrollers, providing separated cache pools for the I-Bus and the D-Bus.

The ARTTM Accelerator is composed by:

- an instruction prefetch buffer;
- a dedicated instruction cache to reduce the effects of branching;
- a data cache for literal pools;
- a scheduling policy of the AHB bus that facilitates the access of the CPU to the flash controller through the D-Bus bus.

Let us analyze the exact role of these technologies.

The Instruction Prefetch Buffer When the CPU accesses to the flash memory, it does not fetch one byte at a time, but it usually reads from 64 up to 256 bits at a time depending on the specific STM32 MCU. These bits contain a variable number of instructions and for this reason they are called instruction lines: assuming that the CPU reads 128 bits (this is what happens in STM32F4 MCUs), this may contain four 32-bit wide instructions or eight 16-bit wide instructions (it depends if the CPU is running in thumb mode or not). So, in case of sequential code, at least four CPU cycles are needed to execute the previous read instruction line. Prefetch on the I-Bus bus can be used to read the next sequential instruction line from the flash memory while the current instruction line is being requested by the CPU. This feature is useful if at least one wait state is needed to access the flash memory.

Instruction prefetch buffer can be enabled by setting the PREFETCH_ENABLE macro to 1 inside the stm32XXxx_hal_conf.h file.

The Instruction Cache Memory The content of the prefetch buffer can be invalided due branching. To limit the time lost due to jumps, it is possible to retain a given number of instruction lines in an instruction cache memory. Each time a miss occurs (requested data not present in the currently used instruction line, in the prefetched instruction line or in the instruction cache memory), the line read is copied into the instruction cache memory. If the CPU requests data contained in the instruction cache memory, it is provided without inserting any delay. Once all the “empty” instruction cache memory lines have been filled, a Least Recently Used (LRU) policy is used to determine the line to replace in the instruction memory cache. This feature is particularly useful in case of code containing loops.

This feature can be enabled by setting the INSTRUCTION_CACHE_ENABLE macro to 1 inside the stm32XXxx_hal_conf.h file, for those MCU providing the ARTTM Accelerator. Data Cache Memory Assembly instructions often move data between memory locations and CPU registers. Sometimes, this data is stored inside the flash memory (they are constant values): in this case, we talk about literal pools. Literal pools are fetched from flash memory through the D-Bus bus during the execution stage of the CPU pipeline. The CPU pipeline is consequently stalled until the requested literal pool is provided. To limit the time lost due to literal pools, accesses through the AHB data-bus D-Bus have priority over accesses through the AHB instruction bus I-Bus (this is indeed a bus-arbitration policy over the D-Bus bus).</pre></td>
<td><pre>被设计为保持 Cortex-M 微控制器的哈佛架构，为 I-Bus 和 D-Bus 提供分离的缓存池。

ART™ 加速器由以下部分组成：

- 指令预取缓冲区；
- 专用的指令缓存，用于减少分支的影响；
- 用于字面量池（literal pools）的数据缓存；
- AHB 总线的调度策略，便于 CPU 通过 D-Bus 总线访问闪存控制器。

让我们分析这些技术的具体作用。

**指令预取缓冲区** 当 CPU 访问闪存时，它并不是一次获取一个字节，而是通常根据特定的 STM32 微控制器一次读取 64 到 256 位。这些位包含可变数量的指令，因此被称为指令行（instruction lines）：假设 CPU 读取 128 位（这是在 STM32F4 微控制器中发生的情况），这可能包含四个 32 位宽的指令或八个 16 位宽的指令（这取决于 CPU 是否运行在 Thumb 模式下）。因此，在顺序代码的情况下，至少需要四个 CPU 周期来执行之前读取的指令行。I-Bus 总线上的预取可用于在当前指令行被 CPU 请求的同时，从闪存中读取下一个顺序指令行。如果需要至少一个等待状态来访问闪存，此功能非常有用。

可以通过在 stm32XXxx_hal_conf.h 文件中将 PREFETCH_ENABLE 宏设置为 1 来启用指令预取缓冲区。

**指令缓存存储器** 预取缓冲区的内容可能因分支而失效。为了限制因跳转而丢失的时间，可以在指令缓存存储器中保留给定数量的指令行。每次发生未命中（miss）时（请求的数据不存在于当前使用的指令行、预取的指令行或指令缓存存储器中），读取的行会被复制到指令缓存存储器中。如果 CPU 请求包含在指令缓存存储器中的数据，则无需插入任何延迟即可提供。一旦所有“空”的指令缓存存储器行都被填充，就会使用最近最少使用（LRU）策略来确定要替换的指令缓存存储器中的行。此功能对于包含循环的代码特别有用。

对于提供 ART™ 加速器的微控制器，可以通过在 stm32XXxx_hal_conf.h 文件中将 INSTRUCTION_CACHE_ENABLE 宏设置为 1 来启用此功能。

**数据缓存存储器** 汇编指令经常在内存位置和 CPU 寄存器之间移动数据。有时，这些数据存储在闪存中（它们是常量值）：在这种情况下，我们称之为字面量池。字面量池在 CPU 流水线的执行阶段通过 D-Bus 总线从闪存中获取。因此，CPU 流水线会停滞，直到请求的字面量池被提供。为了限制因字面量池而丢失的时间，通过 AHB 数据总线 D-Bus 的访问优先于通过 AHB 指令总线 I-Bus 的访问（这实际上是 D-Bus 总线上的总线仲裁策略）。</pre></td>
</tr></tbody></table>

## PDF page 605 — Chapter 22: Booting Process

Focus: `numbers=0, 01, 0605, 0x1F, 0x43, 0xFF, 1, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197; negation=not; conditions=If, if, otherwise, when; identifiers=CMD_ERASE, FLASH_BANK_1, FLASH_SECTOR_1, FLASH_SECTOR_TOTAL, FLASH_TYPEERASE_SECTORS, FLASH_VOLTAGE_RANGE_3, HAL_CRC_Calculate, HAL_FLASHEx_Erase, HAL_FLASH_Lock, HAL_FLASH_Unlock, HAL_MAX_DELAY, HAL_UART_Transmit, cmdErase, memcpy`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>## the UART together with the ACK. If the CRC does not match, a NACK (which is equal to 0x1F) is sent.

## Erase Command The CMD_ERASE command is used to erase a given sector of the flash memory and it has the structure shown in Figure 22.6. The command is composed by the id 0x43 that identifies the command type, followed by the number of sectors to delete (or the value 0xFF to delete all sector except the first one where the bootloader resides) and the CRC-32. The bootloader answers by sending an ACK when the erasing procedure completes.

![Image from PDF page 605](../images/page-0605-image-01.png)

Figure 22.6: The structure of the CMD_ERASE

```text
Filename: src/main-bootloader.c
180
void cmdErase(uint8_t *pucData) {
181
FLASH_EraseInitTypeDef eraseInfo;
182
uint32_t ulBadBlocks = 0, ulCrc = 0;
183
uint32_t pulCmd[] = { pucData[0], pucData[1] };
184
185
memcpy(&amp;ulCrc, pucData + 2, sizeof(uint32_t));
186
187
/* Checks if provided CRC is correct */
188
if (ulCrc == HAL_CRC_Calculate(&amp;hcrc, pulCmd, 2) &amp;&amp;
189
(pucData[1] &gt; 0 &amp;&amp; (pucData[1] &lt; FLASH_SECTOR_TOTAL - 1 || pucData[1] == 0xFF))) {
190
/* If data[1] contains 0xFF, it deletes all sectors; otherwise
191
* the number of sectors specified. */
192
eraseInfo.Banks = FLASH_BANK_1;
193
eraseInfo.Sector = FLASH_SECTOR_1;
194
eraseInfo.NbSectors = pucData[1] == 0xFF ? FLASH_SECTOR_TOTAL - 1 : pucData[1];
195
eraseInfo.TypeErase = FLASH_TYPEERASE_SECTORS;
196
eraseInfo.VoltageRange = FLASH_VOLTAGE_RANGE_3;
197
198
HAL_FLASH_Unlock(); //Unlocks the flash memory
199
HAL_FLASHEx_Erase(&amp;eraseInfo, &amp;ulBadBlocks); //Deletes given sectors */
200
HAL_FLASH_Lock(); //Locks again the flash memory
201
202
/* Sends an ACK */
203
pucData[0] = ACK;
204
HAL_UART_Transmit(&amp;huart2, (uint8_t *) pucData, 1, HAL_MAX_DELAY);
205
} else {
206
/* The CRC is wrong: sends a NACK */
207
pucData[0] = NACK;
208
HAL_UART_Transmit(&amp;huart2, pucData, 1, HAL_MAX_DELAY);
```</pre></td>
<td><pre>## 如果 CRC 不匹配，则发送 NACK（值为 0x1F）。

## 擦除命令 CMD_ERASE 命令用于擦除闪存存储器中的指定扇区，其结构如图 22.6 所示。该命令由标识命令类型的 ID 0x43 组成，后跟要删除的扇区数量（或值 0xFF 以删除除引导加载程序所在的第一个扇区以外的所有扇区）以及 CRC-32。当擦除过程完成时，引导加载程序通过发送 ACK 进行响应。

![Image from PDF page 605](../images/page-0605-image-01.png)

图 22.6：CMD_ERASE 的结构

```text
Filename: src/main-bootloader.c
180
void cmdErase(uint8_t *pucData) {
181
FLASH_EraseInitTypeDef eraseInfo;
182
uint32_t ulBadBlocks = 0, ulCrc = 0;
183
uint32_t pulCmd[] = { pucData[0], pucData[1] };
184
185
memcpy(&amp;ulCrc, pucData + 2, sizeof(uint32_t));
186
187
/* Checks if provided CRC is correct */
188
if (ulCrc == HAL_CRC_Calculate(&amp;hcrc, pulCmd, 2) &amp;&amp;
189
(pucData[1] &gt; 0 &amp;&amp; (pucData[1] &lt; FLASH_SECTOR_TOTAL - 1 || pucData[1] == 0xFF))) {
190
/* If data[1] contains 0xFF, it deletes all sectors; otherwise
191
* the number of sectors specified. */
192
eraseInfo.Banks = FLASH_BANK_1;
193
eraseInfo.Sector = FLASH_SECTOR_1;
194
eraseInfo.NbSectors = pucData[1] == 0xFF ? FLASH_SECTOR_TOTAL - 1 : pucData[1];
195
eraseInfo.TypeErase = FLASH_TYPEERASE_SECTORS;
196
eraseInfo.VoltageRange = FLASH_VOLTAGE_RANGE_3;
197
198
HAL_FLASH_Unlock(); //Unlocks the flash memory
199
HAL_FLASHEx_Erase(&amp;eraseInfo, &amp;ulBadBlocks); //Deletes given sectors */
200
HAL_FLASH_Lock(); //Locks again the flash memory
201
202
/* Sends an ACK */
203
pucData[0] = ACK;
204
HAL_UART_Transmit(&amp;huart2, (uint8_t *) pucData, 1, HAL_MAX_DELAY);
205
} else {
206
/* The CRC is wrong: sends a NACK */
207
pucData[0] = NACK;
208
HAL_UART_Transmit(&amp;huart2, pucData, 1, HAL_MAX_DELAY);
```</pre></td>
</tr></tbody></table>

## PDF page 607 — Chapter 22: Booting Process

Focus: `numbers=0, 1, 128, 16, 200, 273, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296; negation=; conditions=If, if; identifiers=AES_KEY, FLASH_TYPEPROGRAM_BYTE, HAL_CRC_Calculate, HAL_FLASH_Lock, HAL_FLASH_Program, HAL_FLASH_Unlock, HAL_MAX_DELAY, HAL_TIMEOUT, HAL_UART_Receive, HAL_UART_Transmit, aes_enc_dec, memcpy`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>```text
279
/* Sends an ACK */
280
pucData[0] = ACK;
281
HAL_UART_Transmit(&amp;huart2, (uint8_t *) pucData, 1, HAL_MAX_DELAY);
282
283
/* Now retrieves given amount of bytes plus the CRC32 */
284
if (HAL_UART_Receive(&amp;huart2, pucData, 16 + 4, 200) == HAL_TIMEOUT)
285
return;
286
287
memcpy(&amp;ulCrc, pucData + 16, sizeof(uint32_t));
288
289
/* Checks if provided CRC is correct */
290
if (ulCrc == HAL_CRC_Calculate(&amp;hcrc, (uint32_t*) pucData, 4)) {
291
HAL_FLASH_Unlock(); //Unlocks the flash memory
292
293
/* Decode the sent bytes using AES-128 ECB */
294
aes_enc_dec((uint8_t*) pucData, AES_KEY, 1);
295
for (uint8_t i = 0; i &lt; 16; i++) {
296
/* Store each byte in flash memory starting from the specified address */
297
HAL_FLASH_Program(FLASH_TYPEPROGRAM_BYTE, ulSaddr, pucData[i]);
298
ulSaddr += 1;
299
}
300
HAL_FLASH_Lock(); //Locks again the flash memory
301
302
/* Sends an ACK */
303
pucData[0] = ACK;
304
HAL_UART_Transmit(&amp;huart2, (uint8_t *) pucData, 1, HAL_MAX_DELAY);
305
} else {
306
goto sendnack;
307
}
308
} else {
309
goto sendnack;
310
}
311
312
sendnack:
313
pucData[0] = NACK;
314
HAL_UART_Transmit(&amp;huart2, (uint8_t *) pucData, 1, HAL_MAX_DELAY);
315
}
```

## The above code shows how the command is implemented. As you can see, the CRC of the first part of the message is checked against the transmitted value (lines [273:278]). If it corresponds, an ACK is sent, and the next bytes are processed. If the CRC-32 of these other bytes matches (line 290), then the sent data bytes are decrypted using the AES-128 algorithm¹⁸ and the pre-shared key. Data bytes

¹⁸The aes_enc_dec() function is taken from a library made by Eric Peeters, a TI employee. It can be downloaded from the TI website(http://www.ti.com/tool/AES-128) and its license allows to use it freely. ST provides a complete cryptographic library for the STM32 platform, which is also compatible with the Cube framework (https://bit.ly/29zWN81). This library can also take advantage of those STM32 MCUs providing a dedicated hardware crypto unit. However, the license of this library prevents this author from shipping the library with the examples in this book.</pre></td>
<td><pre>```text
279
/* Sends an ACK */
280
pucData[0] = ACK;
281
HAL_UART_Transmit(&amp;huart2, (uint8_t *) pucData, 1, HAL_MAX_DELAY);
282
283
/* Now retrieves given amount of bytes plus the CRC32 */
284
if (HAL_UART_Receive(&amp;huart2, pucData, 16 + 4, 200) == HAL_TIMEOUT)
285
return;
286
287
memcpy(&amp;ulCrc, pucData + 16, sizeof(uint32_t));
288
289
/* Checks if provided CRC is correct */
290
if (ulCrc == HAL_CRC_Calculate(&amp;hcrc, (uint32_t*) pucData, 4)) {
291
HAL_FLASH_Unlock(); //Unlocks the flash memory
292
293
/* Decode the sent bytes using AES-128 ECB */
294
aes_enc_dec((uint8_t*) pucData, AES_KEY, 1);
295
for (uint8_t i = 0; i &lt; 16; i++) {
296
/* Store each byte in flash memory starting from the specified address */
297
HAL_FLASH_Program(FLASH_TYPEPROGRAM_BYTE, ulSaddr, pucData[i]);
298
ulSaddr += 1;
299
}
300
HAL_FLASH_Lock(); //Locks again the flash memory
301
302
/* Sends an ACK */
303
pucData[0] = ACK;
304
HAL_UART_Transmit(&amp;huart2, (uint8_t *) pucData, 1, HAL_MAX_DELAY);
305
} else {
306
goto sendnack;
307
}
308
} else {
309
goto sendnack;
310
}
311
312
sendnack:
313
pucData[0] = NACK;
314
HAL_UART_Transmit(&amp;huart2, (uint8_t *) pucData, 1, HAL_MAX_DELAY);
315
}
```

## 上述代码展示了该命令的实现方式。如您所见，消息第一部分的 CRC 会与传输的值进行比对（第 [273:278] 行）。如果匹配，则发送 ACK，并处理接下来的字节。如果这些其他字节的 CRC-32 也匹配（第 290 行），则使用 AES-128 算法¹⁸和预共享密钥对发送的数据字节进行解密。数据字节

¹⁸aes_enc_dec() 函数取自 TI 员工 Eric Peeters 制作的库。可以从 TI 网站 (http://www.ti.com/tool/AES-128) 下载，其许可证允许自由使用。ST 为 STM32 平台提供了一个完整的加密库，该库也兼容 Cube 框架 (https://bit.ly/29zWN81)。该库还可以利用那些提供专用硬件加密单元的 STM32 微控制器。然而，该库的许可证阻止作者将其与本书中的示例一起发布。</pre></td>
</tr></tbody></table>

## PDF page 615 — Chapter 23: Running FreeRTOS

Focus: `numbers=01, 0615, 1, 2022, 23.1, 615; negation=not; conditions=; identifiers=doOperation1, doOperation2, doOperationN, doOperationX`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>In the recent years, the evolution of FreeRTOS was mostly focused on the integration of AWS IoT services.

However, ST announced in December 2020³ a key collaboration with Microsoft, which recently acquired the company behind ThreadX RTOS, renaming it in Azure RTOS. Microsoft is pushing hard the development of a complete ecosystems of IoT solutions for embedded platforms, and Azure RTOS is the central element of Microsoft offering. The collaboration is mutual: ST will integrate the Azure RTOS as STM32Cube expansion pack, and Microsoft will push STM32 microcontrollers⁴ as reference “platform” for IoT applications. ST will not limit the support to Azure RTOS to the kernel. The integration will include FileX, a filesystem offering advanced features on NAND and NOR Flash memories like fault tolerance, or wear leveling; NetX, and NetX Duo, which are network stacks that offer TCP/IP, IPv4, and IPv6, as well as many upper-level protocols used in IoT like MQTT or COAP; USBX that facilitates the use of a USB interface, both as a host or as a device, with a complete set of supported USB classes.

At the time of writing this chapter (January 2022), ST released just X-AZURE Cube Extension Pack for STM32H7 and STM32F4 families. According to this author, it will take more than a year before STM will complete the integration to the complete STM32 portfolio. Moreover, it is still not clear how the RTOS market will evolve in the next years. For this reason, this book will cover just FreeRTOS, leaving the possibility to cover Azure RTOS to future updates of the book.

## 23.1 Understanding the Concepts Underlying an RTOS

This paragraph gives a quick introduction to the main concepts underlying real-time Operating Systems. Experienced users can safely skip it.

![Image from PDF page 615](../images/page-0615-image-01.png)

Except for the ISRs and exception handlers, all the examples built so far are designed so that our applications are composed by just one execution stream. Typically, starting from the main() routine, a large and infinite while loop carries out firmware tasks:

```text
...
while(1) {
doOperation1();
doOperation2();
...
doOperationN();
}
```

The time spent by each doOperationX() is broadly estimated by the developer, who has the responsibility to avoid that one of those functions sticks for too much time, preventing other parts

³https://blog.st.com/azure-rtos/ ⁴https://azure.microsoft.com/it-it/blog/new-azure-rtos-collaborations-with-leaders-in-the-semiconductor-industry/</pre></td>
<td><pre>近年来，FreeRTOS 的演进主要集中于 AWS IoT 服务的集成。

然而，ST 于 2020 年 12 月³宣布与 Microsoft 进行关键合作，Microsoft 最近收购了 ThreadX RTOS 背后的公司，并将其更名为 Azure RTOS。Microsoft 正在大力推动为嵌入式平台开发完整的物联网解决方案生态系统，而 Azure RTOS 是 Microsoft 提供方案的核心元素。这种合作是双向的：ST 将把 Azure RTOS 集成为 STM32Cube 扩展包，而 Microsoft 将推动将 STM32 微控制器⁴作为物联网应用的参考“平台”。ST 对 Azure RTOS 的支持不仅限于内核。集成将包括 FileX，这是一个在 NAND 和 NOR Flash 存储器上提供高级功能（如容错或磨损平衡）的文件系统；NetX 和 NetX Duo，它们是提供 TCP/IP、IPv4 和 IPv6 以及物联网中使用的许多上层协议（如 MQTT 或 COAP）的网络栈；以及 USBX，它简化了 USB 接口的使用，既可作为主机也可作为设备，并支持完整的 USB 类集合。

在撰写本章时（2022 年 1 月），ST 仅为 STM32H7 和 STM32F4 系列发布了 X-AZURE Cube 扩展包。根据本作者的观点，STM 需要一年多的时间才能完成对完整 STM32 产品组合的集成。此外，未来几年 RTOS 市场将如何演变仍不清楚。因此，本书将仅涵盖 FreeRTOS，并保留在未来书籍更新中涵盖 Azure RTOS 的可能性。

## 23.1 理解实时操作系统（RTOS）背后的概念

本段简要介绍了实时操作系统（real-time operating system）背后的主要概念。经验丰富的用户可以安全地跳过此部分。

![Image from PDF page 615](../images/page-0615-image-01.png)

除了中断服务程序（ISR）和异常（exception）处理程序外，迄今为止构建的所有示例都旨在使我们的应用程序仅由一个执行流组成。通常，从 main() 例程开始，一个庞大且无限的 while 循环执行固件任务：

```text
...
while(1) {
doOperation1();
doOperation2();
...
doOperationN();
}
```

每个 doOperationX() 所花费的时间大致由开发者估算，开发者有责任避免其中一个函数占用过长时间，从而阻止固件的其他部分

³https://blog.st.com/azure-rtos/ ⁴https://azure.microsoft.com/it-it/blog/new-azure-rtos-collaborations-with-leaders-in-the-semiconductor-industry/</pre></td>
</tr></tbody></table>

## PDF page 617 — Chapter 23: Running FreeRTOS

Focus: `numbers=1, 10, 1ms, 2, 3, 4, 5, 500, 500ms, 6, 7, 8, 9; negation=Unless, no, not, unless, without; conditions=Unless, if, unless; identifiers=GPIO_PIN_5, HAL_GPIO_TooglePin, HAL_GetTick, blinkTask`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>```text
void blinkTask() {
if(HAL_GetTick() - timeKeep &gt; 500) {
HAL_GPIO_TooglePin(GPIOA, GPIO_PIN_5);
timeKeep = HAL_GetTick();
}
}
```

A simple modification to that routine ensures that we will not lose data coming from the UART in the majority of situations, unless the UART transfers data quickly.

As you can see, with cooperative scheduling programmers have a great responsibility in ensuring their code will not affect the overall activities of the firmware, introducing performance bottlenecks.

The voluntary releasing of the execution flow is not the only limit of the code seen so far. Let us have a closer look at the blinkTask() routine. Here we need a global variable⁷, timeKeep, to keep track of the global tick counter incremented by the CubeHAL every 1ms and to perform a comparison to check if 500ms are elapsed. This is required because every time a routine exits, its execution context (that is, the stack frame) is popped from the main stack and it is destroyed. Unless we do not use some nasty tricks offered by the language⁸, there is no way to exit from a function without losing its context.

Continuation routines, abbreviated as co-routines or simply coroutines, are program structures that generalize the concept of subroutines for non-preemptive multitasking, by allowing multiple entry points for suspending and resuming execution at certain locations. Co-routines require special support from the run-time of the language, and they are traditionally provided from more highlevel languages like Scheme, but also more widespread languages like Python and Perl provide a form of co-routines. A co-routine is said not to return but to yield the execution flow. For example, the blinkTask() could be rewritten using co-routines in this way:

```text
1
void blinkTask() {
2
uint32_t timeKeep = HAL_GetTick();
3
while (1) {
4
if(HAL_GetTick() - timeKeep &gt; 500) {
5
HAL_GPIO_TooglePin(GPIOA, GPIO_PIN_5);
6
timeKeep = HAL_GetTick();
```

# 7 }

```text
8
yield; /* Pass the control to another routine, e.g. the scheduler */
```

# 9 }

```text
10
}
```

Co-routines work so that, the next time the control passes to blinkTask(), the execution will resume from line 3. We will not go into details of how co-routines are implemented in languages that support them. However, this usually involves the creation of separated stacks for each co-routine, which could call other co-routines that in turn may pass the control to other continuations.

⁷A local and static variable would have the same effect, however without changing the concept. ⁸Which involves the use of the C setjmp() and longjmp() functions.</pre></td>
<td><pre>```text
void blinkTask() {
if(HAL_GetTick() - timeKeep &gt; 500) {
HAL_GPIO_TooglePin(GPIOA, GPIO_PIN_5);
timeKeep = HAL_GetTick();
}
}
```

对该例程的简单修改确保了在大多数情况下我们不会丢失来自 UART 的数据，除非 UART 传输数据的速度很快。

如您所见，在协作式调度中，程序员承担着巨大的责任，以确保他们的代码不会影响固件的整体活动，从而引入性能瓶颈。

自愿释放执行流并非迄今为止所见代码的唯一限制。让我们更仔细地看看 blinkTask() 例程。在这里，我们需要一个全局变量⁷ timeKeep，以跟踪由 CubeHAL 每 1 毫秒递增的全局滴答计数器，并进行比较以检查是否已过去 500 毫秒。这是必需的，因为每次例程退出时，其执行上下文（即堆栈帧）会从主堆栈中弹出并被销毁。除非我们使用语言提供的一些棘手技巧⁸，否则没有办法在不丢失其上下文的情况下退出函数。

续例程（Continuation routines），缩写为协程（co-routines）或简称协程，是一种泛化非抢占式多任务中子例程概念的程序结构，它允许在特定位置暂停和恢复执行时具有多个入口点。协程需要语言运行时的特殊支持，传统上由 Scheme 等更高级的语言提供，但 Python 和 Perl 等更广泛使用的语言也提供某种形式的协程。协程被认为不是返回，而是让出（yield）执行流。例如，blinkTask() 可以使用协程重写如下：

```text
1
void blinkTask() {
2
uint32_t timeKeep = HAL_GetTick();
3
while (1) {
4
if(HAL_GetTick() - timeKeep &gt; 500) {
5
HAL_GPIO_TooglePin(GPIOA, GPIO_PIN_5);
6
timeKeep = HAL_GetTick();
```

# 7 }

```text
8
yield; /* Pass the control to another routine, e.g. the scheduler */
```

# 9 }

```text
10
}
```

协程的工作方式是，当下次控制权传递到 blinkTask() 时，执行将从第 3 行恢复。我们不会深入探讨支持协程的语言中协程的具体实现细节。然而，这通常涉及为每个协程创建独立的堆栈，这些协程可以调用其他协程，而这些协程又可能将控制权传递给其他续体。

⁷局部变量和静态变量会产生相同的效果，但不会改变这一概念。⁸这涉及使用 C 语言的 setjmp() 和 longjmp() 函数。</pre></td>
</tr></tbody></table>

## PDF page 618 — Chapter 23: Running FreeRTOS

Focus: `numbers=01, 0618, 1ms, 23.1, 23.2, 618; negation=Not, not; conditions=if; identifiers=MSP, PC, R0, R15, blinkTask, readUART2Task`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>A preemptive multitasking Operating System is a coordinator of physical resources that allows the execution of multiple computing tasks⁹, each one with its independent stack, by assigning a limited quantum time (also called slice time) to each task. Every task has a well-defined temporal window, usually large about 1ms in embedded systems, during which it performs its activities before it is preempted. The RTOS kernel decides the execution order of the tasks ready to be executed using a scheduling policy: a scheduler is an algorithm that characterizes the way the OS plans the execution of tasks.

A task is “moved” in/out from the CPU by a context switch operation. A context switch is performed by the OS, thanks to hardware features we will explore next, which makes a “snapshot” of the current task state by saving the internal CPU registers (PC, MSP, R0..R15, etc.) before switching to another task, which will be able to “re-use” again the CPU for the same quantum time (or even less if “it wants”).

![Image from PDF page 618](../images/page-0618-image-01.png)

Figure 23.1: How an OS schedules the tasks execution by assigning them a fixed quantum time

Figure 23.1 shows how the task preemption works for the case of the example seen before. Here we are supposing that we have just two tasks: one for the blinkTask() routine and one for the readUART2Task() one. The OS start scheduling the blinkTask() task, which can “use” the CPU for 1000μs (that is, 1ms)¹⁰. After the time is gone, the OS schedules the execution of the readUART2Task() which can now occupy the CPU for the same quantum time. After that period, the CPU will reschedule the first task, and so on.

Figure 23.2 shows the way SRAM memory is typically organized by an OS. Each task is represented by a memory segment containing the Thread Control Block (TCB), which is nothing more than a descriptor containing all relevant information related to the task execution just “a moment”¹¹ before it is preempted (the stack pointer, the program counter, CPU registers and other few things), plus the stack itself, that is the stack frame of those routines currently invoked on the thread stack. By jumping between several threads, thanks to context switch operations, the OS guarantees the same

⁹In this paragraph, and only in this one, the term task and thread will be used indiscriminately. ¹⁰Those values of quantum time are indicative, since the exact duration of a quantum is affected by a lot of things. Not last, the overhead connected with a context switch, which is non-negligible. Moreover, here we are assuming that tasks have all the same priority, which usually is not true especially in embedded systems. ¹¹This is not true at all, since before a task is preempted several other things take place. However, explaining into details these aspects is outside the scope of this book. Refer to Joseph Yiu books if interested in deepening how context switch is performed on Cortex-M based microcontrollers.</pre></td>
<td><pre>抢占式多任务操作系统是物理资源的协调者，它允许执行多个计算任务⁹，每个任务拥有独立的堆栈，并为每个任务分配有限的量子时间（也称为时间片）。每个任务都有一个明确定义的时间窗口，在嵌入式系统中通常约为 1ms，在此期间它执行其活动，随后被抢占。实时操作系统内核使用调度策略来决定就绪任务的执行顺序：调度器是一种算法，用于表征操作系统规划任务执行的方式。

任务通过上下文切换操作从 CPU 上被“移出” in/out。上下文切换由操作系统执行，这得益于我们接下来将要探讨的硬件特性，该特性通过保存内部 CPU 寄存器（PC、MSP、R0..R15 等）对当前任务状态进行“快照”，然后再切换到另一个任务，该任务将能够再次“复用” CPU，运行相同的时间片（或者如果它“愿意”的话，甚至更短）。

![Image from PDF page 618](../images/page-0618-image-01.png)

图 23.1：操作系统如何通过为任务分配固定的时间片来调度任务的执行

图 23.1 展示了前文示例中任务抢占的工作方式。此处假设我们只有两个任务：一个用于 blinkTask() 例程，另一个用于 readUART2Task() 例程。操作系统开始调度 blinkTask() 任务，该任务可以“使用”CPU 1000 微秒（即 1ms）¹⁰。时间用尽后，操作系统调度 readUART2Task() 的执行，该任务现在可以占用相同的量子时间。该时间段结束后，CPU 将重新调度第一个任务，依此类推。

图 23.2 展示了操作系统通常组织 SRAM 内存的方式。每个任务由一个内存段表示，其中包含线程控制块（TCB）。TCB 不过是一个描述符，其中包含与任务执行相关的所有重要信息，这些信息是在任务被抢占前“一瞬间”¹¹ 捕获的（包括堆栈指针、程序计数器、CPU 寄存器以及其他少量内容），此外还包括堆栈本身，即当前在线程堆栈上调用的那些例程的堆栈帧。通过上下文切换操作在多个线程之间跳转，操作系统保证了相同的

⁹仅在本段中，术语“任务”和“线程”将被不加区分地混用。¹⁰这些时间片数值仅供参考，因为时间片的确切持续时间受许多因素影响。其中，上下文切换带来的开销不可忽略。此外，此处假设所有任务具有相同的优先级，但这在嵌入式系统中通常并不成立。¹¹这完全不是事实，因为在任务被抢占之前，还会发生其他若干事情。然而，详细解释这些方面超出了本书的范围。如果对深入了解基于 Cortex-M 微控制器的上下文切换机制感兴趣，请参阅 Joseph Yiu 的著作。</pre></td>
</tr></tbody></table>

## PDF page 619 — Chapter 23: Running FreeRTOS

Focus: `numbers=01, 0619, 1, 23.2, 619; negation=cannot, not; conditions=if; identifiers=blinkTask`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>execution time to all threads, giving the impression that firmware activities are performed in parallel.

![Image from PDF page 619](../images/page-0619-image-01.png)

Figure 23.2: How the memory is organized in several tasks by an OS

A Real Time Operating Systems (RTOS) is an OS able to offer the notion of multitasking (or better, multithreading as seen in note 1) while ensuring response within specified time constraints, often referred to as deadlines. Real-time responses are often understood to be in the order of milliseconds, and sometimes microseconds. A system not specified as operating in real-time cannot usually guarantee a response within any timeframe, although actual or expected response times may be given. General-purpose Operating Systems (like Linux, Windows and MacOS) cannot be real-time Operating Systems (even if exist some their derivative releases - especially of Linux - engineered for real-time applications) for two simply reasons: pagination and swapping. The former allows to segment the task memory in small chunks named pages, which can be scattered in the RAM and aliased from the MMU giving the illusion that the process can manage the whole 4GB address space (even if the computer do not provide that amount of SRAM). The latter allows to swap-in/swap-out those “unused” pages on an external (and slower) memorization unit (typically a hard drive). Those two features are intrinsically non-deterministic and preventing the OS from servicing requests in short and countable time.

An RTOS allows to use the first version of the blinkTask() function minimizing the impact of the</pre></td>
<td><pre>执行时间分配给所有线程，从而营造出固件活动并行执行的假象。

![Image from PDF page 619](../images/page-0619-image-01.png)

图 23.2：操作系统如何在多个任务中组织内存

实时操作系统（RTOS）是一种能够提供多任务（或更准确地说，如注释 1 中所述的多线程）概念，同时确保在指定时间约束（通常称为截止时间）内做出响应的操作系统。实时响应通常被理解为在毫秒级，有时甚至达到微秒级。未指定为实时运行的系统通常无法保证在任何时间范围内做出响应，尽管可能会给出实际或预期的响应时间。通用操作系统（如 Linux、Windows 和 MacOS）不能成为实时操作系统（即使存在某些针对实时应用进行工程化改造的衍生版本——尤其是 Linux 的某些版本），原因很简单：分页和交换。前者允许将任务内存分割为名为页的小块，这些页可以分散在 RAM 中，并通过 MMU 进行别名映射，从而产生进程可以管理整个 4GB 地址空间的错觉（即使计算机并未提供那么多 SRAM）。后者允许将这些“未使用”的页 swap-in/swap-out 到外部（且速度较慢）的存储单元（通常是硬盘）上。这两个特性本质上是非确定性的，阻止操作系统在短且可计数的时间内处理请求。

RTOS 允许使用 blinkTask() 函数的第一个版本，以最小化</pre></td>
</tr></tbody></table>

## PDF page 620 — Chapter 23: Running FreeRTOS

Focus: `numbers=1ms, 500ms, 7; negation=Unless, cannot, not, without; conditions=If, Unless, if, when; identifiers=blinkTask`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>busy loop on the UART transfer process¹². However, as we will see later in this chapter, typically an RTOS also gives us tools to completely avoid busy loops: using software timers it is possible to ask to the OS to re-schedule the blinkTask() only when the specified amount of time is elapsed. Moreover, the RTOS also provides ways to voluntary release the control when we know that it is completely useless to wait for an operation that will be performed by another task (or if we are waiting for an asynchronous event).

We have said just one moment before that an RTOS gives a way to voluntary release the control to other threads. But what if one task does not want to release it? For example, the first release of the blinkTask() routine could monopolize the CPU up to more than 500ms in the worst case that, given the typical slice time of 1ms, is a long time. So, what can to perform the context switch? It is impossible to “jump” to other program instructions (a context switch, is a sort of goto to another program instruction) without losing one relevant information: the value of the program counter itself.

The context switch needs a substantial help from the hardware. In Chapter 7 we have seen that interrupts and exceptions are a source of multiprogramming. The way they are handled by the Cortex-M core allows to jump to the exception handler without losing the current execution context. By taking advantage of a dedicated hardware timer, usually the SysTick one, the RTOS uses the periodic interrupt generated on the overflow event to perform the context switch. This timer is configured to overflow (or underflow in case of the SysTick, which is a downcounter timer) every 1ms. The RTOS then captures the exception and saves the current execution context in the TCB, passing the control to the next task in the scheduling list by restoring its execution context and exiting from the timer interrupt. The preempted threads will not know anything that this happened¹³.

¹²This does not mean that using an RTOS we can write bad code without impacting on the overall performances. This only means that, a true preemptive scheduler can guarantee a higher multiprogramming degree, ensuring that all threads have the same CPU time-slice. Unless we mess with task priorities, as we will see later. ¹³However, this could not correspond to what an RTOS does. The story here is more complex, and it is related to the specific hardware architectures and to the way interrupts are prioritized. During the execution of an interrupt handler, another interrupt with a higher priority could suspend the execution of the current interrupt, as seen in Chapter 7. But when this happens, the CPU cannot switch to the thread mode (which is the regular mode when the normal code is executed) by performing the task switch without prior exiting from all interrupts (which run in the handler mode - a special mode provided by Cortex-M core during the exception handling). This means that if the SysTick IRQ takes place while another IRQ is active, the SysTick exception handler cannot perform the context switch (that is to pass the control to another task running in thread mode), because another code running in handler mode has been preempted and needs to complete its activities. Usually this is solved by deferring the effective context switch operation to the PendSV Handler, which is an exception configured to run at the lowest priority. However, this is just one way to implement the context switch. If interested in deepening this topic, you have to consult the source code or the documentation of your RTOS.</pre></td>
<td><pre>在 UART 传输过程中使用忙等待循环¹²。然而，正如我们将在本章后面看到的，实时操作系统（RTOS）通常也提供了完全避免忙等待循环的工具：利用软件定时器，可以请求操作系统仅在指定的时间间隔过去后才重新调度 blinkTask()。此外，RTOS 还提供了主动释放控制权的方式，当我们知道等待由另一个任务执行的操作（或等待异步事件）完全没有必要时，就可以这样做。

我们刚才提到，RTOS 提供了一种将控制权主动释放给其他线程的方式。但如果某个任务不想释放控制权呢？例如，blinkTask() 例程的首次发布在最坏情况下可能会独占 CPU 超过 500ms，考虑到 1ms 的典型时间片长度，这是一段相当长的时间。那么，如何执行上下文切换呢？如果不丢失一项关键信息——程序计数器本身的值，就不可能“跳转”到其他程序指令（上下文切换本质上是一种跳转到另一条程序指令的操作）。

上下文切换需要硬件的大力支持。在第 7 章中，我们已经看到中断和异常是多道程序设计的来源。Cortex-M 内核处理这些事件的方式允许跳转到异常处理程序，而不会丢失当前的执行上下文。通过利用专用的硬件定时器（通常是 SysTick 定时器），RTOS 使用溢出事件产生的周期性中断来执行上下文切换。该定时器被配置为每 1ms 发生一次溢出（对于作为递减计数器的 SysTick 而言，则是下溢）。随后，RTOS 捕获该异常，将当前执行上下文保存到任务控制块（TCB）中，通过恢复下一个任务的执行上下文并退出定时器中断，将控制权传递给调度列表中的下一个任务。被抢占的线程对此毫不知情¹³。

¹²这并不意味着使用实时操作系统（real-time operating system）后，编写劣质代码就不会影响整体性能。这仅意味着，真正的抢占式调度器可以保证更高的多道程序度，确保所有线程拥有相同的 CPU 时间片。除非我们随意调整任务优先级，正如我们稍后所见。¹³然而，这可能并不完全对应实时操作系统的实际行为。这里的机制更为复杂，它与特定的硬件架构以及中断（interrupt）的优先级方式有关。在中断处理程序执行期间，另一个具有更高优先级的中断可能会挂起当前中断的执行，如第 7 章所述。但当这种情况发生时，CPU 无法通过执行任务切换直接切换到线程模式（即执行常规代码时的正常模式），除非先退出所有中断（这些中断运行在处理程序模式——一种由 Cortex-M 内核在异常（exception）处理期间提供的特殊模式）。这意味着，如果 SysTick 中断请求（IRQ）在另一个 IRQ 处于活动状态时发生，SysTick 异常处理程序无法执行上下文切换（即将控制权传递给另一个在线程模式下运行的任务），因为另一个正在处理程序模式下运行的代码已被抢占，需要完成其活动。通常，这通过将实际的上下文切换操作延迟到 PendSV 处理程序来解决，PendSV 是一个被配置为以最低优先级运行的异常。然而，这只是实现上下文切换的一种方式。如果对深入探讨此主题感兴趣，必须查阅您的实时操作系统的源代码或文档。</pre></td>
</tr></tbody></table>

## PDF page 644 — Chapter 23: Running FreeRTOS

Focus: `numbers=0x200, 0x400, 1, 23.13; negation=Not, never, not; conditions=If, if; identifiers=MSP, __real__malloc_r, __real_malloc, __wrap__malloc_r, __wrap_malloc, free, malloc`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>- _sbss points to the start of the uninitialized data while _ebss (or the linker symbol _end) points to the end of this region, which also contains the FreeRTOS heap if using heap_4.c scheme. _ebss corresponds to the begininning of the C Heap region, if using the _sbrk() implementa- tion in Core/Src/sysmem.c.
- _Min_Heap_Size is the “logical” limit of the Heap region. This limit is established by the programmer (by default, CubeMX sets this to 0x200). and it should be carefully checked to avoid any corruption of the Stack region, which grows in the opposite direction.
- _Min_Stack_Size is the logical limit of the Stack region. Again, this limit is established by the programmer (by default, CubeMX sets this to 0x400).
- Current Stack Pointer is the content of the Cortex-M core register sp, and it corresponds to the current base stack pointer.
- _estack by default represent the end of the SRAM memory and it is the first location of the stack that contains the MSP.

To safely use the malloc()/free() routines in our application, we have the following options.

OPTION 1: Not Use Them at All Well, this may seem drastic, but it is an option to consider. If your code, and all dependant libraries, do not use malloc()/free(), then it is ok to do not care about them. However, never trust others’ code: you have to carefully check it at run-time, and not by simply looking at the code or the documentation. You can easily perform the test by instructing the linker accordingly. LD allows to “wrap” a routine by using the command-line option -Xlinker --wrap (which can be set using Project properties as shown in Figure 23.13). Dave Nadler provides³⁰ an excellent implementation of the wrapper to keep track of malloc() usage, which is reported below. You can place a breakpoint to see if the wrappers are called or you can inspect the value of MallocCallCnt variable (you could print it by using the ITM, if supported by the MCU).

```text
size_t TotalMallocdBytes;
int MallocCallCnt;
static bool inside_malloc;
void *__wrap_malloc(size_t nbytes) {
extern void * __real_malloc(size_t nbytes);
MallocCallCnt++;
TotalMallocdBytes += nbytes;
inside_malloc = true;
void *p = __real_malloc(nbytes); // will call malloc_r...
inside_malloc = false;
return p;
};
void *__wrap__malloc_r(void *reent, size_t nbytes) {
(void)(reent);
extern void * __real__malloc_r(size_t nbytes);
```

³⁰https://nadler.com/embedded/newlibAndFreeRTOS.html</pre></td>
<td><pre>- _sbss 指向未初始化数据的起始位置，而 _ebss（或链接器符号 _end）指向该区域的末尾，如果使用 heap_4.c 方案，该区域还包含 FreeRTOS 堆。如果使用 Core/Src/sysmem.c 中的 _sbrk() 实现，_ebss 对应于 C 堆区域的开始。
- _Min_Heap_Size 是堆区域的“逻辑”限制。此限制由程序员设定（默认情况下，CubeMX 将其设置为 0x200），并且应仔细检查以避免破坏堆栈区域，因为堆栈区域是向相反方向增长的。
- _Min_Stack_Size 是堆栈区域的逻辑限制。同样，此限制由程序员设定（默认情况下，CubeMX 将其设置为 0x400）。
- 当前堆栈指针（Current Stack Pointer）是 Cortex-M 内核寄存器 sp 的内容，它对应于当前主堆栈指针。
- _estack 默认表示 SRAM 内存的末尾，它是包含 MSP 的堆栈的第一个位置。

为了在我们的应用中安全地使用 malloc()/free() 例程，我们有以下选项。

选项 1：完全不使用它们 这听起来可能很极端，但这是一个值得考虑的选项。如果你的代码以及所有依赖的库都不使用 malloc()/free()，那么忽略它们是可以的。然而，永远不要信任他人的代码：你必须在运行时仔细检查，而不仅仅是查看代码或文档。你可以通过相应地指示链接器轻松执行测试。LD 允许使用命令行选项 -Xlinker --wrap 来“包装”一个例程（可以通过项目属性设置，如图 23.13 所示）。Dave Nadler 提供了一个³⁰ 优秀的包装器实现，用于跟踪 malloc() 的使用情况，如下所示。你可以设置断点来查看包装器是否被调用，或者检查 MallocCallCnt 变量的值（如果 MCU 支持 ITM，你可以通过 ITM 打印它）。

```text
size_t TotalMallocdBytes;
int MallocCallCnt;
static bool inside_malloc;
void *__wrap_malloc(size_t nbytes) {
extern void * __real_malloc(size_t nbytes);
MallocCallCnt++;
TotalMallocdBytes += nbytes;
inside_malloc = true;
void *p = __real_malloc(nbytes); // will call malloc_r...
inside_malloc = false;
return p;
};
void *__wrap__malloc_r(void *reent, size_t nbytes) {
(void)(reent);
extern void * __real__malloc_r(size_t nbytes);
```

³⁰https://nadler.com/embedded/newlibAndFreeRTOS.html</pre></td>
</tr></tbody></table>

## PDF page 675 — Chapter 23: Running FreeRTOS

Focus: `numbers=01, 0675, 1, 12, 13, 14, 15, 16, 17, 18, 19, 1ms, 20, 21, 22, 23, 23.7, 23.8, 24, 25, 26, 500, 675; negation=never, not; conditions=if, when; identifiers=HAL_GPIO_TogglePin, blinkFunc, osKernelStart, osTimerNew, osTimerStart`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>12

```text
13
/* Creation of blinkThread */
14
timID = osTimerNew(blinkFunc, osTimerPeriodic, NULL, NULL);
15
osTimerStart(timID, 500);
```

16

```text
17
/* Start scheduler */
18
osKernelStart();
```

19

```text
20
/* We should never get here as control is now taken by the scheduler */
21
while (1);
22
}
```

23

```text
24
void blinkFunc(void *argument) {
25
HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
26
}
```

### 23.7.1 How FreeRTOS Manages Timers

As you can see in the previous example, our application does not use threads. So, who takes care of timers? FreeRTOS uses a centralized thread, named RTOS daemon (or also timer service thread), which automatically calls the callback routines when a timer expires. This thread is a regular thread, which has a priority defined by the macro configTIMER_TASK_PRIORITY and a stack with a size defined by the macro configTIMER_TASK_STACK_DEPTH. Moreover, it has an internal pool of timer objects, whose size is defined by the macro configTIMER_QUEUE_LENGTH.

Another important aspect to stress is the way FreeRTOS computes the time internally. FreeRTOS measure the time in function of the tick frequency, which is in turn defined by the overflow frequency of the timer chosen as timebase generator. This means that, if we use the SysTick timer configured to overflow ever 1ms, then internal software timers have a resolution of 1ms (which corresponds to 1 tick). The ticks value passed to the osTimerStart() routine is so bound to the global tick frequency.

## 23.8 A Case Study: Low-Power Management With an RTOS

![Image from PDF page 675](../images/page-0675-image-01.png)

This is a really advanced topic, that requires the knowledge of many concepts underlying an RTOS. Moreover, a decent knowledge of the concepts illustrated in Chapter 20 is required. Un-experienced users can safely skip this part.

In Chapter 19 we have analyzed the low-power features offered by STM32 microcontrollers. We have seen that, especially for MCUs belonging to the STM32L-series, they offer several power modes</pre></td>
<td><pre>12

```text
13
/* Creation of blinkThread */
14
timID = osTimerNew(blinkFunc, osTimerPeriodic, NULL, NULL);
15
osTimerStart(timID, 500);
```

16

```text
17
/* Start scheduler */
18
osKernelStart();
```

19

```text
20
/* We should never get here as control is now taken by the scheduler */
21
while (1);
22
}
```

23

```text
24
void blinkFunc(void *argument) {
25
HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
26
}
```

### 23.7.1 FreeRTOS 如何管理定时器

正如前一个示例所示，我们的应用程序不使用线程。那么，谁负责处理定时器呢？FreeRTOS 使用一个集中式的线程，称为 RTOS 守护进程（或定时器服务线程），当定时器到期时，该线程会自动调用回调例程。这是一个常规线程，其优先级由宏 configTIMER_TASK_PRIORITY 定义，堆栈大小由宏 configTIMER_TASK_STACK_DEPTH 定义。此外，它拥有一个内部定时器对象池，其大小由宏 configTIMER_QUEUE_LENGTH 定义。

另一个需要强调的重要方面是 FreeRTOS 内部计算时间的方式。FreeRTOS 根据滴答（tick）频率来测量时间，而滴答频率又由选作时基生成器的定时器的溢出频率定义。这意味着，如果我们使用配置为每 1ms 溢出一次的 SysTick 定时器，那么内部软件定时器的分辨率为 1ms（对应 1 个滴答）。传递给 osTimerStart() 例程的滴答值因此与全局滴答频率绑定。

## 23.8 案例研究：使用实时操作系统进行低功耗管理

![Image from PDF page 675](../images/page-0675-image-01.png)

这是一个非常高级的主题，需要了解实时操作系统背后的许多概念。此外，还需要对第 20 章中阐述的概念有相当的了解。经验不足的用户可以安全地跳过这部分内容。

在第 19 章中，我们分析了 STM32 微控制器提供的低功耗特性。我们看到，特别是对于属于 STM32L 系列的 MCU，它们提供了多种电源模式</pre></td>
</tr></tbody></table>

## PDF page 684 — Chapter 23: Running FreeRTOS

Focus: `numbers=0, 1, 1MHz, 1ms, 2, 36, 37, 42, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69; negation=unless; conditions=unless, when; identifiers=HAL_NVIC_EnableIRQ, HAL_NVIC_SetPriority, HAL_RCC_GetPCLK1Freq, HAL_TIM_Base_Init, HAL_TIM_Base_Start_IT, HAL_TIM_PeriodElapsedCallback, TIM_COUNTERMODE_UP, USHRT_MAX, __HAL_DBGMCU_FREEZE_TIM2, __HAL_RCC_TIM2_CLK_ENABLE, osKernelStart, prvSetupTimerInterrupt, vPortSuppressTicksAndSleep`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>53

```text
54
/* Enable the TIM2 clock. */
55
__HAL_RCC_TIM2_CLK_ENABLE();
```

56

```text
57
/* Ensure clock stops in debug mode. */
58
__HAL_DBGMCU_FREEZE_TIM2();
```

59

```text
60
/* Compute TIM2 clock */
61
uwTimclock = 2*HAL_RCC_GetPCLK1Freq();
62
/* Compute the prescaler value to have TIM2 counter clock equal to 1MHz */
63
uwPrescalerValue = (uint32_t) ((uwTimclock / 1000000U) - 1U);
```

64

```text
65
/* Configure the TIM2 timer */
66
htim2.Instance = TIM2;
67
htim2.Init.Period = ulPeriodValueForOneTick;
68
htim2.Init.Prescaler = uwPrescalerValue;
69
htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
70
HAL_TIM_Base_Init(&amp;htim2);
```

71

```text
72
/* Enable the TIM2 interrupt. This must execute at the lowest interrupt priority. */
73
HAL_NVIC_SetPriority(TIM2_IRQn, configLIBRARY_LOWEST_INTERRUPT_PRIORITY, 0);
74
HAL_NVIC_EnableIRQ(TIM2_IRQn);
```

75

```text
76
HAL_TIM_Base_Start_IT(&amp;htim2);
77
/* See the comments where xMaximumPossibleSuppressedTicks is declared. */
78
xMaximumPossibleSuppressedTicks = ((unsigned long) USHRT_MAX)
79
/ ulPeriodValueForOneTick;
80
}
```

## The first two functions we are going to analyze are related to the setup of the timer used as tick generator and the handling of the related overflow interrupt. The prvSetupTimerInterrupt() function is automatically invoked by FreeRTOS when the osKernelStart() routine is called. It configures the TIM2 timer so that it expires every 1ms. The corresponding interrupt is enabled, and the ISR priority is set to the lowest one (remember that, unless different needed, it is always important to setup the timer ISR with the lowest priority). The HAL_TIM_PeriodElapsedCallback() callback simply increases the global tick count by 1. Don’t care about the instructions at lines [36:37] because they will be clear later. The same callback is responsible of the increment of the HAL tick counter (line 42)

## Now we are going to analyze the most complex part: the vPortSuppressTicksAndSleep() function. We will divide it in blocks, so that it is simpler to analyze its code. It is strongly suggested to keep the real code in the IDE at your hands.</pre></td>
<td><pre>53

```text
54
/* Enable the TIM2 clock. */
55
__HAL_RCC_TIM2_CLK_ENABLE();
```

56

```text
57
/* Ensure clock stops in debug mode. */
58
__HAL_DBGMCU_FREEZE_TIM2();
```

59

```text
60
/* Compute TIM2 clock */
61
uwTimclock = 2*HAL_RCC_GetPCLK1Freq();
62
/* Compute the prescaler value to have TIM2 counter clock equal to 1MHz */
63
uwPrescalerValue = (uint32_t) ((uwTimclock / 1000000U) - 1U);
```

64

```text
65
/* Configure the TIM2 timer */
66
htim2.Instance = TIM2;
67
htim2.Init.Period = ulPeriodValueForOneTick;
68
htim2.Init.Prescaler = uwPrescalerValue;
69
htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
70
HAL_TIM_Base_Init(&amp;htim2);
```

71

```text
72
/* Enable the TIM2 interrupt. This must execute at the lowest interrupt priority. */
73
HAL_NVIC_SetPriority(TIM2_IRQn, configLIBRARY_LOWEST_INTERRUPT_PRIORITY, 0);
74
HAL_NVIC_EnableIRQ(TIM2_IRQn);
```

75

```text
76
HAL_TIM_Base_Start_IT(&amp;htim2);
77
/* See the comments where xMaximumPossibleSuppressedTicks is declared. */
78
xMaximumPossibleSuppressedTicks = ((unsigned long) USHRT_MAX)
79
/ ulPeriodValueForOneTick;
80
}
```

## 我们要分析的前两个函数与用作滴答生成器的定时器设置以及相关溢出中断的处理有关。prvSetupTimerInterrupt() 函数在调用 osKernelStart() 例程时由 FreeRTOS 自动调用。它配置 TIM2 定时器，使其每 1ms 到期一次。相应的中断被使能，并且中断服务程序（ISR）的优先级被设置为最低（请记住，除非另有需要，始终重要的是将定时器 ISR 设置为最低优先级）。HAL_TIM_PeriodElapsedCallback() 回调只是将全局滴答计数增加 1。不要担心第 [36:37] 行的指令，因为它们稍后会变得清晰。同一个回调还负责增加 HAL 滴答计数器（第 42 行）。

## 现在我们将分析最复杂的部分：vPortSuppressTicksAndSleep() 函数。我们将把它划分为若干代码块，以便更简单地分析其代码。强烈建议在 IDE 中随时保留并查看实际代码。</pre></td>
</tr></tbody></table>

## PDF page 685 — Chapter 23: Running FreeRTOS

Focus: `numbers=100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124; negation=no, not; conditions=If, if; identifiers=HAL_PWR_EnterSTOPMode, HAL_TIM_Base_Stop_IT, PWR_MAINREGULATOR_ON, PWR_STOPENTRY_WFI, __disable_irq, __enable_irq, configPRE_STOP_PROCESSING, eTaskConfirmSleepModeStatus, vPortSuppressTicksAndSleep`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>```text
Filename: Core/Src/tickless-mode.c
89
void vPortSuppressTicksAndSleep(TickType_t xExpectedIdleTime) {
90
uint32_t ulCounterValue, ulCompleteTickPeriods;
91
eSleepModeStatus eSleepAction;
92
TickType_t xModifiableIdleTime;
93
const TickType_t xRegulatorOffIdleTime = 50;
```

94

```text
95
/* Make sure the TIM2 reload value does not overflow the counter. */
96
if (xExpectedIdleTime &gt; xMaximumPossibleSuppressedTicks) {
97
xExpectedIdleTime = xMaximumPossibleSuppressedTicks;
98
}
```

99

```text
100
/* Calculate the reload value required to wait xExpectedIdleTime tick
101
periods. */
102
ulCounterValue = ulPeriodValueForOneTick * xExpectedIdleTime;
103
104
/* To avoid race conditions, enter a critical section.
*/
105
__disable_irq();
106
107
/* If a context switch is pending then abandon the low power entry as
108
the context switch might have been pended by an external interrupt that
109
requires processing. */
110
eSleepAction = eTaskConfirmSleepModeStatus();
111
if (eSleepAction == eAbortSleep) {
112
/* Re-enable interrupts. */
113
__enable_irq();
114
return;
115
} else if (eSleepAction == eNoTasksWaitingTimeout) {
116
/* Stop TIM2 */
117
HAL_TIM_Base_Stop_IT(&amp;htim2);
118
119
/* A user definable macro that allows application code to be inserted
120
here.
Such application code can be used to minimize power consumption
121
further by turning off IO, peripheral clocks, the Flash, etc. */
122
configPRE_STOP_PROCESSING();
123
124
125
/* There are no running state tasks and no tasks that are blocked with a
126
time out.
Assuming the application does not care if the tick time slips
127
with respect to calendar time then enter a deep sleep that can only be
128
woken by (in this demo case) the user button being pushed on the
129
STM32L discovery board.
If the application does require the tick time
130
to keep better track of the calendar time then the RTC peripheral can be
131
used to make rough adjustments. */
132
HAL_PWR_EnterSTOPMode(PWR_MAINREGULATOR_ON, PWR_STOPENTRY_WFI);
133
134
/* A user definable macro that allows application code to be inserted
```</pre></td>
<td><pre>```text
Filename: Core/Src/tickless-mode.c
89
void vPortSuppressTicksAndSleep(TickType_t xExpectedIdleTime) {
90
uint32_t ulCounterValue, ulCompleteTickPeriods;
91
eSleepModeStatus eSleepAction;
92
TickType_t xModifiableIdleTime;
93
const TickType_t xRegulatorOffIdleTime = 50;
```

94

```text
95
/* Make sure the TIM2 reload value does not overflow the counter. */
96
if (xExpectedIdleTime &gt; xMaximumPossibleSuppressedTicks) {
97
xExpectedIdleTime = xMaximumPossibleSuppressedTicks;
98
}
```

99

```text
100
/* Calculate the reload value required to wait xExpectedIdleTime tick
101
periods. */
102
ulCounterValue = ulPeriodValueForOneTick * xExpectedIdleTime;
103
104
/* To avoid race conditions, enter a critical section.
*/
105
__disable_irq();
106
107
/* If a context switch is pending then abandon the low power entry as
108
the context switch might have been pended by an external interrupt that
109
requires processing. */
110
eSleepAction = eTaskConfirmSleepModeStatus();
111
if (eSleepAction == eAbortSleep) {
112
/* Re-enable interrupts. */
113
__enable_irq();
114
return;
115
} else if (eSleepAction == eNoTasksWaitingTimeout) {
116
/* Stop TIM2 */
117
HAL_TIM_Base_Stop_IT(&amp;htim2);
118
119
/* A user definable macro that allows application code to be inserted
120
here.
Such application code can be used to minimize power consumption
121
further by turning off IO, peripheral clocks, the Flash, etc. */
122
configPRE_STOP_PROCESSING();
123
124
125
/* There are no running state tasks and no tasks that are blocked with a
126
time out.
Assuming the application does not care if the tick time slips
127
with respect to calendar time then enter a deep sleep that can only be
128
woken by (in this demo case) the user button being pushed on the
129
STM32L discovery board.
If the application does require the tick time
130
to keep better track of the calendar time then the RTC peripheral can be
131
used to make rough adjustments. */
132
HAL_PWR_EnterSTOPMode(PWR_MAINREGULATOR_ON, PWR_STOPENTRY_WFI);
133
134
/* A user definable macro that allows application code to be inserted
```</pre></td>
</tr></tbody></table>

## PDF page 686 — Chapter 23: Running FreeRTOS

Focus: `numbers=0, 102, 105, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157; negation=not; conditions=If, if, when; identifiers=HAL_TIM_Base_Start_IT, HAL_TIM_Base_Stop_IT, USHRT_MAX, __HAL_TIM_GET_COUNTER, __enable_irq, configASSERT, configPOST_STOP_PROCESSING, configPRE_STOP_PROCESSING, eTaskConfirmSleepModeStatus, prvSetupTimerInterrupt`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>```text
135
here.
Such application code can be used to reverse any actions taken
136
by the configPRE_STOP_PROCESSING().
In this demo
137
configPOST_STOP_PROCESSING() is used to re-initialize the clocks that
138
were turned off when STOP mode was entered. */
139
configPOST_STOP_PROCESSING();
140
141
/* Restart tick. */
142
HAL_TIM_Base_Start_IT(&amp;htim2);
143
144
/* Re-enable interrupts. */
145
__enable_irq();
```

## The function starts checking if the expected idle time, that is the time window within we can safely stop the tick generation, is less than the xMaximumPossibleSuppressedTicks: this value is computed inside the prvSetupTimerInterrupt() routine according to the given Prescaler and Period values. Then, at line 102, it computes the Period value to use so that the timer will overflow after the xExpectedIdleTime time. To avoid race conditions, we then enter in a critical section (line 105) and we invoke the eTaskConfirmSleepModeStatus() to decide how to proceed in the tick suppression procedure. If the function returns eNoTasksWaitingTimeout, then we can stop the TIM2 timer at all, and we can enter in stop mode until the MCU is woken up by an event or an interrupt.

```text
Filename: Core/Src/tickless-mode.c
147
else {
148
/* Stop TIM2 momentarily.
The time TIM2 is stopped for is not accounted for
149
in this implementation (as it is in the generic implementation) because the
150
clock is so slow it is unlikely to be stopped for a complete count period
151
anyway. */
152
HAL_TIM_Base_Stop_IT(&amp;htim2);
153
154
/* The tick flag is set to false before sleeping.
If it is true when sleep
155
mode is exited then sleep mode was probably exited because the tick was
156
suppressed for the entire xExpectedIdleTime period. */
157
ucTickFlag = pdFALSE;
158
159
/* Trap underflow before the next calculation. */
160
configASSERT(ulCounterValue &gt;= __HAL_TIM_GET_COUNTER(&amp;htim2));
161
162
/* Adjust the TIM2 value to take into account that the current time
163
slice is already partially complete. */
164
ulCounterValue -= (uint32_t) __HAL_TIM_GET_COUNTER(&amp;htim2);
165
166
/* Trap overflow/underflow before the calculated value is written to TIM2. */
167
configASSERT(ulCounterValue &lt; ( uint32_t ) USHRT_MAX);
168
configASSERT(ulCounterValue != 0);
169
170
/* Update to use the calculated overflow value. */
```</pre></td>
<td><pre>```text
135
here.
Such application code can be used to reverse any actions taken
136
by the configPRE_STOP_PROCESSING().
In this demo
137
configPOST_STOP_PROCESSING() is used to re-initialize the clocks that
138
were turned off when STOP mode was entered. */
139
configPOST_STOP_PROCESSING();
140
141
/* Restart tick. */
142
HAL_TIM_Base_Start_IT(&amp;htim2);
143
144
/* Re-enable interrupts. */
145
__enable_irq();
```

## 该函数首先检查预期的空闲时间，即我们可以安全停止滴答生成的时间窗口，是否小于 xMaximumPossibleSuppressedTicks：该值在 prvSetupTimerInterrupt() 例程中根据给定的 Prescaler 和 Period 值进行计算。然后，在第 102 行，它计算要使用的 Period 值，以便定时器在 xExpectedIdleTime 时间后溢出。为了避免竞态条件，我们随后进入临界区（第 105 行），并调用 eTaskConfirmSleepModeStatus() 以决定如何继续执行滴答抑制过程。如果该函数返回 eNoTasksWaitingTimeout，则我们可以完全停止 TIM2 定时器，并进入停止模式，直到 MCU 被事件或中断唤醒。

```text
Filename: Core/Src/tickless-mode.c
147
else {
148
/* Stop TIM2 momentarily.
The time TIM2 is stopped for is not accounted for
149
in this implementation (as it is in the generic implementation) because the
150
clock is so slow it is unlikely to be stopped for a complete count period
151
anyway. */
152
HAL_TIM_Base_Stop_IT(&amp;htim2);
153
154
/* The tick flag is set to false before sleeping.
If it is true when sleep
155
mode is exited then sleep mode was probably exited because the tick was
156
suppressed for the entire xExpectedIdleTime period. */
157
ucTickFlag = pdFALSE;
158
159
/* Trap underflow before the next calculation. */
160
configASSERT(ulCounterValue &gt;= __HAL_TIM_GET_COUNTER(&amp;htim2));
161
162
/* Adjust the TIM2 value to take into account that the current time
163
slice is already partially complete. */
164
ulCounterValue -= (uint32_t) __HAL_TIM_GET_COUNTER(&amp;htim2);
165
166
/* Trap overflow/underflow before the calculated value is written to TIM2. */
167
configASSERT(ulCounterValue &lt; ( uint32_t ) USHRT_MAX);
168
configASSERT(ulCounterValue != 0);
169
170
/* Update to use the calculated overflow value. */
```</pre></td>
</tr></tbody></table>

## PDF page 687 — Chapter 23: Running FreeRTOS

Focus: `numbers=0, 164, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193; negation=not; conditions=If, if; identifiers=HAL_PWR_EnterSLEEPMode, HAL_TIM_Base_Start_IT, PWR_LOWPOWERREGULATOR_ON, PWR_MAINREGULATOR_ON, PWR_SLEEPENTRY_WFI, __HAL_TIM_SET_AUTORELOAD, __HAL_TIM_SET_COUNTER, configPRE_SLEEP_PROCESSING, eTaskConfirmSleepModeStatus`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>```text
171
__HAL_TIM_SET_AUTORELOAD(&amp;htim2, ulCounterValue);
172
__HAL_TIM_SET_COUNTER(&amp;htim2, 0);
173
174
/* Restart the TIM2. */
175
HAL_TIM_Base_Start_IT(&amp;htim2);
176
177
/* Allow the application to define some pre-sleep processing.
This is
178
the standard configPRE_SLEEP_PROCESSING() macro as described on the
179
FreeRTOS.org website. */
180
xModifiableIdleTime = xExpectedIdleTime;
181
configPRE_SLEEP_PROCESSING( xModifiableIdleTime );
182
183
/* xExpectedIdleTime being set to 0 by configPRE_SLEEP_PROCESSING()
184
means the application defined code has already executed the wait/sleep
185
instruction. */
186
if (xModifiableIdleTime &gt; 0) {
187
/* The sleep mode used is dependent on the expected idle time
188
as the deeper the sleep the longer the wake up time.
See the
189
comments at the top of main_low_power.c.
Note xRegulatorOffIdleTime
190
is set purely for convenience of demonstration and is not intended
191
to be an optimized value. */
192
if (xModifiableIdleTime &gt; xRegulatorOffIdleTime) {
193
/* A slightly lower power sleep mode with a longer wake up time. */
194
HAL_PWR_EnterSLEEPMode(PWR_LOWPOWERREGULATOR_ON, PWR_SLEEPENTRY_WFI);
195
} else {
196
/* A slightly higher power sleep mode with a faster wake up time. */
197
HAL_PWR_EnterSLEEPMode(PWR_MAINREGULATOR_ON, PWR_SLEEPENTRY_WFI);
198
}
199
}
```

## If the eTaskConfirmSleepModeStatus() returns eStandardSleep, then we can enter in sleep mode. The timer is stopped, and its Period is set (at line 171) to the value computed before (at line 164). The configPRE_SLEEP_PROCESSING() is a macro we can implement to perform operations preliminary to the sleep mode (for example, in some STM32 MCUs it is required to lower the clock speed, or we could use this macro to turn OFF unneeded peripherals). We can so enter in sleep mode or in low-power sleep mode, according to the computed sleep time (in some STM32 MCUs exiting from low-power sleep requires more time that would waste a lot of power uselessly if the sleeping period is too short).</pre></td>
<td><pre>```text
171
__HAL_TIM_SET_AUTORELOAD(&amp;htim2, ulCounterValue);
172
__HAL_TIM_SET_COUNTER(&amp;htim2, 0);
173
174
/* Restart the TIM2. */
175
HAL_TIM_Base_Start_IT(&amp;htim2);
176
177
/* Allow the application to define some pre-sleep processing.
This is
178
the standard configPRE_SLEEP_PROCESSING() macro as described on the
179
FreeRTOS.org website. */
180
xModifiableIdleTime = xExpectedIdleTime;
181
configPRE_SLEEP_PROCESSING( xModifiableIdleTime );
182
183
/* xExpectedIdleTime being set to 0 by configPRE_SLEEP_PROCESSING()
184
means the application defined code has already executed the wait/sleep
185
instruction. */
186
if (xModifiableIdleTime &gt; 0) {
187
/* The sleep mode used is dependent on the expected idle time
188
as the deeper the sleep the longer the wake up time.
See the
189
comments at the top of main_low_power.c.
Note xRegulatorOffIdleTime
190
is set purely for convenience of demonstration and is not intended
191
to be an optimized value. */
192
if (xModifiableIdleTime &gt; xRegulatorOffIdleTime) {
193
/* A slightly lower power sleep mode with a longer wake up time. */
194
HAL_PWR_EnterSLEEPMode(PWR_LOWPOWERREGULATOR_ON, PWR_SLEEPENTRY_WFI);
195
} else {
196
/* A slightly higher power sleep mode with a faster wake up time. */
197
HAL_PWR_EnterSLEEPMode(PWR_MAINREGULATOR_ON, PWR_SLEEPENTRY_WFI);
198
}
199
}
```

## 如果 eTaskConfirmSleepModeStatus() 返回 eStandardSleep，那么我们可以进入睡眠模式。定时器被停止，并且其 Period（周期）被设置为之前计算出的值（在第 171 行，基于第 164 行的计算）。configPRE_SLEEP_PROCESSING() 是一个我们可以实现的宏，用于执行进入睡眠模式前的预备操作（例如，在某些 STM32 微控制器中，需要降低时钟速度，或者我们可以使用此宏来关闭不需要的外设）。因此，我们可以根据计算出的睡眠时间进入睡眠模式或低功耗睡眠模式（在某些 STM32 微控制器中，从低功耗睡眠模式退出需要更多时间，如果睡眠周期过短，这会无用地浪费大量电力）。</pre></td>
</tr></tbody></table>

## PDF page 705 — Chapter 24: Advanced Debugging Techniques

Focus: `numbers=01, 0705, 0x2000, 1, 24.1, 705; negation=Not, not; conditions=when; identifiers=LR, R13, R14, SP`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>### 24.1.1 The Cortex-M Exception Entrance Sequence and the ARM Calling Convention

For high-level programmers², to invoke a routine seems an obvious thing. We just write down the name of the function we are going to call, passing to it a given number of parameters. And that’s it. However, from the processor point-of-view, what happens under the hood needs to be specified down to the finest details and it must match both the processor architecture and the programming language semantics. For this reason, it is common to talk about calling convention when describing the process of placing a new routine on the stack.

The ARM Architecture Procedure Call Standard (AAPCS) precisely defines the calling convention for ARM based architectures. In Chapter 1 we have seen that Cortex-M based microcontrollers provide several core registers, which are shown again in Figure 24.1 for your convenience. Not all those core registers are available in all Cortex-M cores: for example, FPU registers S0-S31 are only available in Cortex-M4F and Cortex-M7 cores, when the FPU unit is enabled and used.

![Image from PDF page 705](../images/page-0705-image-01.jpeg)

Figure 24.1: Cortex-M CPU core registers

Some core registers play a special role because they are used to carry out processor’s activities. R13 is the Stack Pointer (SP), that is the pointer in SRAM (so something similar to 0x2000 XXXX in an STM32) to the base of the most recent entry placed on the stack. This entry represents the local memory area of a given function and, in a full-descendent stack, SP coincides with the lowest address of the stack. R14 is the Link Register (LR), that is the address in FLASH³ (so something similar to 0x0800X XXXX in an STM32) of the instruction following the instruction that called the

²As C programmers, we are all “high level programmers”, whether you believe it or not. ³This is not entirely true, because CPU could execute code placed in SRAM as well as in other external memories. But it is ok to consider it true here.</pre></td>
<td><pre>### 24.1.1 Cortex-M 异常入口序列与 ARM 调用约定

对于高级语言程序员²来说，调用一个例程似乎是一件显而易见的事情。我们只需写下要调用的函数名称，并传递给定数量的参数。就这样结束了。然而，从处理器的角度来看，底层发生的事情需要被规定到最细微的细节，并且必须同时符合处理器架构和编程语言语义。因此，在描述将新例程压入堆栈的过程时，通常会提到调用约定（calling convention）。

ARM 架构过程调用标准（AAPCS）精确定义了基于 ARM 架构的调用约定。在第 1 章中，我们已经看到，基于 Cortex-M 的微控制器提供了多个内核寄存器，为了方便起见，这些寄存器再次在图 24.1 中展示。并非所有这些内核寄存器在所有 Cortex-M 内核中都可用：例如，FPU 寄存器 S0-S31 仅在启用并使用 FPU 单元时，才在 Cortex-M4F 和 Cortex-M7 内核中可用。

![Image from PDF page 705](../images/page-0705-image-01.jpeg)

图 24.1：Cortex-M CPU 内核寄存器

某些内核寄存器扮演着特殊角色，因为它们用于执行处理器的活动。R13 是堆栈指针（Stack Pointer, SP），即指向最近放置在堆栈上的条目基址的 SRAM 中的指针（因此在 STM32 中类似于 0x2000 XXXX）。该条目代表给定函数的局部内存区域，并且在全降序堆栈中，SP 与堆栈的最低地址重合。R14 是链接寄存器（Link Register, LR），即 FLASH³ 中（因此在 STM32 中类似于 0x0800X XXXX）调用堆栈上给定函数的指令之后的那条指令的地址。

²作为 C 程序员，无论你是否相信，我们都是“高级语言程序员”。³这并不完全正确，因为 CPU 也可以执行放置在 SRAM 以及其他外部存储器中的代码。但在这里将其视为真值是合理的。</pre></td>
</tr></tbody></table>

## PDF page 740 — Chapter 24: Advanced Debugging Techniques

Focus: `numbers=01, 0740, 24.30, 3, 740; negation=; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>![Image from PDF page 740](../images/page-0740-image-01.jpeg)

Figure 24.30: A SEGGER J-Link Ultra+ debug probe

SEGGER is a German company specialized in designing external debug probes for the ARM Cortex portfolio (including Cortex-M/R/A microprocessors and other modern MCUs like PIC32 and Renesas RX series). SEGGER J-Links (see Figure 24.30) are the most widely used line of debug probes available today, and they are often sold as OEM version for other vendors (IAR and Keil debug probes are nothing more than a J-Link).

The most relevant features offered by J-Link debuggers are:

- Up to 3 MByte/s download speed.
- Compatible with all popular tool-chains including the STM32CubeIDE.
- Supports an unlimited number of software breakpoints in flash memory.
- Allows setting breakpoints in external flash memory of Cortex-M systems through FMC controller.
- Cross platform support (Microsoft Windows, Linux, Mac OS X).
- Supports concurrent access to CPU by multiple applications.
- Support for multi core debugging.
- Remote Server included. Allows using J-Link remotely via TCP/IP.
- Software comes with free GDB server, allowing usage of J-Link with all GDB-based debug solutions.
- Production flash programming software (J-Flash) available.
- Debugger independent flash download (internal flash, CFI flash, SPIFI flash).
- Supports CPU/MCU internal trace buffer (ETB, MTB, etc.).</pre></td>
<td><pre>![Image from PDF page 740](../images/page-0740-image-01.jpeg)

图 24.30：SEGGER J-Link Ultra+ 调试探针

SEGGER 是一家德国公司，专门设计用于 ARM Cortex 系列（包括 Cortex-M/R/A 微处理器以及其他现代微控制器，如 PIC32 和瑞萨 RX 系列）的外部调试探针。SEGGER J-Links（参见图 24.30）是当今最广泛使用的调试探针系列，它们通常作为其他供应商的 OEM 版本出售（IAR 和 Keil 的调试探针只不过是 J-Link 而已）。

J-Link 调试器提供的最相关特性包括：

- 高达 3 MByte/s 的下载速度。
- 兼容所有流行的工具链，包括 STM32CubeIDE。
- 支持在闪存中设置无限数量的软件断点。
- 允许通过 FMC 控制器在 Cortex-M 系统的外部闪存中设置断点。
- 跨平台支持（Microsoft Windows、Linux、Mac OS X）。
- 支持多个应用程序并发访问 CPU。
- 支持多核调试。
- 包含远程服务器。允许通过 TCP/IP 远程使用 J-Link。
- 软件附带免费的 GDB 服务器，允许使用 J-Link 与所有基于 GDB 的调试解决方案配合使用。
- 提供生产级闪存编程软件（J-Flash）。
- 调试器独立的闪存下载（内部闪存、CFI 闪存、SPIFI 闪存）。
- 支持 CPU/MCU 内部跟踪缓冲区（ETB、MTB 等）。</pre></td>
</tr></tbody></table>

## PDF page 741 — Chapter 24: Advanced Debugging Techniques

Focus: `numbers=1.2V, 1100, 2016, 2022, 24.31, 24.6, 3.3V, 5V, 60, 61234; negation=no, not; conditions=If, When, if, when; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>- Supports ETM tracing (J-Trace Cortex-M, J-Trace ARM).
- Wide target voltage range: 1.2V - 3.3V, 5V tolerant.
- Supports multiple target interfaces (JTAG, SWD, FINE, SPD, etc.).

J-Link probes ranges from the EDU edition, which costs about 60$, up to the J-Trace PRO edition that costs about $1100. If you are a student or a low-budget hobbyist, the EDU edition worth spending since it supports all relevant features provided by professional J-Link probes. If you are a professional, then the Ultra+ is a good deal according to this author.

However, for owners of STM development boards (Nucleo, Discovery, Eval) there is a good and totally free alternative: in April 2016 SEGGER has released a firmware upgrade for the ST-LINK V2/V2.1¹³ interface that transforms it in a J-Link compatible debug probe. By downloading¹⁴ a dedicated software tool¹⁵, your ST-LINK is transformed in a J-Link OB compatible interface, and you can use the most important software tools by SEGGER¹⁶. Moreover, you can easily revert the interface to an ST-LINK if you want. In case you experience issue in switching the ST-LINK V2 debugger to J-Link OB, please follow the instructions in this blog post¹⁷.

When debugging with SEGGER debug probe, there is no need to use ST-LINK GDB Server, because SEGGER provides its own compatible GDB server, named JLinkGDBServer. This is one of the fundamental reasons to choose these tools, because the JLinkGDBServer is a faster and more reliable alternative to ST-LINK being cross-platform at the same time. The instructions to upgrade the ST- LINK interface to a J-Link compatible one are clearly reported on the SEGGER website. We will not repeat them here. Instead, we are now going to analyze how to use a J-Link debug probe with the GNU MCU Eclipse tool-chain.

You are not forced to install SEGGER software tools to start using SEGGER debug probes, since the JLinkGDBServer is already integrated in the STM32CubeIDE. To use the J-LINK with the STM32CubeIDE you need to select the corresponding debug probe in the Debug Configurations.

## 24.6 Debugging two Nucleo Boards Simultaneously

We may need to debug two STM32 based devices simultaneously. This is not uncommon, especially when dealing with communication protocols. STM32CubeIDE allows us to debug two or more boards on the same computer.

To launch two instances of the STLINK GDB Server we need to create two separated Debug Configurations, one for each board. In every configuration we need to configure two fundamental parameters: the S/N of the ST-LINK interface and the GDB Server port number (see Figure 24.31). Regarding the GSB Server port this is up to us to choose two or more separated port number (61234

¹³At the time of writing this chapter February 2022, SEGGER does not provide a tool to convert an ST-LINK V3 debug adapter to a SEGGER J-LINK. ¹⁴https://www.segger.com/jlink-st-link.html ¹⁵Unfortunately, at the time of writing this chapter, the upgrade tool is only available for the Windows OS. ¹⁶Please, take note that the license of this “free” upgrade to the ST-LINK interface prevents you from using it to debug custom and commercial devices. Look at the SEGGER website for the complete list of limitations. ¹⁷https://bit.ly/3ostIQ6</pre></td>
<td><pre>- 支持 ETM 跟踪（J-Trace Cortex-M、J-Trace ARM）。
- 宽目标电压范围：1.2V - 3.3V，5V 容忍。
- 支持多种目标接口（JTAG、SWD、FINE、SPD 等）。

J-Link 探针从 EDU 版（价格约为 60 美元）到 J-Trace PRO 版（价格约为 1100 美元）不等。如果你是学生或预算有限的爱好者，EDU 版值得购买，因为它支持专业 J-Link 探针提供的所有相关特性。如果你是专业人士，那么根据本作者的观点，Ultra+ 是一个不错的选择。

然而，对于 STM 开发板（Nucleo、Discovery、Eval）的所有者来说，有一个很好的且完全免费的替代方案：2016 年 4 月，SEGGER 发布了 ST-LINK V2/V2.1¹³ 接口的固件升级，将其转换为兼容 J-Link 的调试探针。通过下载¹⁴ 专用软件工具¹⁵，你的 ST-LINK 将被转换为兼容 J-Link OB 的接口，你可以使用 SEGGER¹⁶ 最重要的软件工具。此外，如果你愿意，可以轻松地将接口还原为 ST-LINK。如果你在将 ST-LINK V2 调试器切换到 J-Link OB 时遇到问题，请遵循此博客文章¹⁷中的说明。

在使用 SEGGER 调试探针进行调试时，无需使用 ST-LINK GDB Server，因为 SEGGER 提供了自己的兼容 GDB 服务器，名为 JLinkGDBServer。这是选择这些工具的基本原因之一，因为 JLinkGDBServer 是 ST-LINK 的更快、更可靠的替代方案，同时还是跨平台的。将 ST-LINK 接口升级为兼容 J-Link 接口的说明清楚地列在 SEGGER 网站上。我们不会在这里重复它们。相反，我们现在将分析如何使用 J-Link 调试探针与 GNU MCU Eclipse 工具链配合使用。

你不必安装 SEGGER 软件工具即可开始使用 SEGGER 调试探针，因为 JLinkGDBServer 已经集成在 STM32CubeIDE 中。要在 STM32CubeIDE 中使用 J-LINK，你需要在“调试配置”中选择相应的调试探针。

## 24.6 同时调试两块 Nucleo 开发板

我们可能需要同时调试两个基于 STM32 的设备。这种情况并不少见，尤其是在处理通信协议时。STM32CubeIDE 允许我们在同一台计算机上调试两块或更多开发板。

要启动两个 STLINK GDB Server 实例，我们需要创建两个独立的调试配置，每个开发板对应一个配置。在每个配置中，我们需要设置两个基本参数：ST-LINK 接口的 S/N 和 GDB Server 端口号（参见图 24.31）。关于 GSB Server 端口，由我们选择两个或更多不同的端口号（61234

¹³ 在撰写本章时（2 月 2022），SEGGER 尚未提供将 ST-LINK V3 调试适配器转换为 SEGGER J-LINK 的工具。¹⁴ https://www.segger.com/jlink-st-link.html ¹⁵ 不幸的是，在撰写本章时，升级工具仅适用于 Windows 操作系统。¹⁶ 请注意，此“免费”升级至 ST-LINK 接口的许可证禁止您将其用于调试自定义和商业设备。请查看 SEGGER 网站以获取完整的限制列表。¹⁷ https://bit.ly/3ostIQ6</pre></td>
</tr></tbody></table>

## PDF page 742 — Chapter 24: Advanced Debugging Techniques

Focus: `numbers=01, 0742, 1, 2, 24.31, 24.7, 3, 4, 5, 61235, 742; negation=; conditions=When, when; identifiers=HW_A, HW_B, PC`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>and 61235 is fine). Instead, to derive the ST-LINK S/N it is sufficient to click on Scan button close to the ST-LINK S/N field. STM32CubeIDE will list you the serial number of every board attached to the PC.

Let us suppose that two different boards/microcontrollers are used: HW_A and HW_B. When the debug configuration has been configured for both projects so that each board is associated to a specific probe, it is time to test and debug each board individually first. When it is confirmed that this is working, the debug of both targets at the same time can be started as follow:

1. Start to debug HW_A. 2. The perspective switches automatically to the Debug perspective in STM32CubeIDE when a debug session for HW_A is started. 3. Switch to the C/C++ perspective. 4. Select the project for HW_B and start debugging it. The Debug perspective opens again. 5. There are two application stacks/nodes in the Debug view, one for each project. When changing the selected node in the Debug view, the related editor, the Variable view and others views are updated to present information associated to the selected project.

![Image from PDF page 742](../images/page-0742-image-01.jpeg)

Figure 24.31: How to condigure Debug Configurations fields when using two ST-LINK simultaneously

## 24.7 ARM Semihosting

ARM semihosting is a distinctive feature of the Cortex-M platform, and it is extremely useful for testing and debug purpose. It is a mechanism that allows target boards to “exchange messages” from</pre></td>
<td><pre>并且 61235 即可）。相反，要获取 ST-LINK S/N，只需点击 ST-LINK S/N 字段附近的扫描按钮即可。STM32CubeIDE 会列出连接到 PC 的每块板卡的序列号。

假设使用了两个不同的 boards/microcontrollers：HW_A 和 HW_B。当两个项目的调试配置均已设置，且每块板卡都关联到特定的探针时，首先应分别测试和调试每块板卡。确认此操作正常后，即可按以下步骤同时调试两个目标：

1. 开始调试 HW_A。2。当 HW_A 的调试会话开始时，STM32CubeIDE 会自动切换到调试视图。3。切换到 C/C++ 视图。4。选择 HW_B 的项目并开始调试。调试视图再次打开。5。调试视图中有两个应用程序 stacks/nodes，每个项目各有一个。在调试视图中更改选中的节点时，相关的编辑器、变量视图以及其他视图会更新以显示与所选项目关联的信息。

![Image from PDF page 742](../images/page-0742-image-01.jpeg)

图 24.31：同时使用两个 ST-LINK 时如何配置调试配置字段

## 24.7 ARM 半主机

ARM 半主机是 Cortex-M 平台的一个独特功能，对于测试和调试目的极其有用。它是一种允许目标板卡“交换消息”的机制，从</pre></td>
</tr></tbody></table>

## PDF page 743 — Chapter 24: Advanced Debugging Techniques

Focus: `numbers=0, 1, 2, 24.32, 24.7, 3, 4, 5, 6; negation=no, not; conditions=if, when; identifiers=PC, initialise_monitor_handles, printf`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>the embedded firmware to a host computer running a debugger. In Cortex-M0/0+ core, where the ITM interface is not available, this mechanism enables printf() and scanf() functions if there is no way to use one of the integrated UARTs. However, the usage of the ARM semihosting is not limited to the message printout. Semihosting allows to access to other host PC I/O capabilities, such as terminals and files. This last feature is extremely useful when you have to transfer large amount of data between the target board and the host PC.

Semihosting requires additional runtime library code, and it can be implemented in several ways on Cortex-M architecture. However, the preferred one is using the bktp ARM assembly instruction, as we will see later. The next paragraph will give a quick explanation of how to configure our STM32CubeIDE project to use semihosting in our code. This will allow us to print messages on the OpenOCD console.

### 24.7.1 Enable Semihosting on a Project

To use semihosting with STM32CubeIDE some updates are needed to be done in the project. A debugger supporting semihosting is also required. This article guides on how to enable semihosting when using OpenOCD, ST-LINK and STM32 devices. Please note that ST-LINK GDB server does not support semihosting, and for this reason we will configure the Debug configuration to run OpenOCD.

To enable semihosting follow these steps:

1. Exclude from compilation (or delete it completely) the file Core/Src/syscalls.c. You can easily perform this task by right-clicking on the file in the Project Explorer pane and then selecting Resource Configuration-&gt;Exclude from Build…. 2. Add the following two lines in beginning of Core/Src/main.c to include &lt;stdio.h&gt; and to use initialise_monitor_handles() prototype and add a call to initialise_monitor_handles() function in the beginning of main() function.

```text
1
#include &lt;stdio.h&gt;
2
extern void initialise_monitor_handles(void);
3
...
4
int main(void) {
5
/* USER CODE BEGIN 1 */
6
initialise_monitor_handles();
```

3. Update GCC Linker project configuration adding rdimon library to the linked libraries, as shown in Figure 24.32.</pre></td>
<td><pre>嵌入式固件到运行调试器的主机计算机。在 Cortex-M0/0+ 内核中，由于 ITM 接口不可用，该机制可在无法使用任一集成 UART 的情况下启用 printf() 和 scanf() 功能。然而，ARM 半托管的使用并不局限于消息打印。半托管允许访问其他主机 PC I/O 功能，例如终端和文件。当需要在目标板和主机 PC 之间传输大量数据时，最后这一功能极其有用。

半托管需要额外的运行时库代码，并且可以在 Cortex-M 架构上以多种方式实现。然而，首选的方式是使用 bktp ARM 汇编指令，我们稍后会看到这一点。下一段将简要说明如何配置我们的 STM32CubeIDE 项目，以便在代码中使用半托管。这将允许我们在 OpenOCD 控制台上打印消息。

### 24.7.1 在项目中启用半主机

要在 STM32CubeIDE 中使用半主机功能，需要在项目中做一些更新。此外，还需要一个支持半主机功能的调试器。本文指导如何在配合 OpenOCD、ST-LINK 和 STM32 器件时启用半主机功能。请注意，ST-LINK GDB 服务器不支持半主机功能，因此我们将配置调试设置以运行 OpenOCD。

要启用半主机功能，请按照以下步骤操作：

1. 将该文件从编译中排除（或将其完全删除） Core/Src/syscalls.c. 您可以轻松完成此操作：在“项目资源管理器”窗格中右键单击该文件，然后选择“资源配置 -&gt; 从构建中排除…”。 2. 在开头添加以下两行 Core/Src/main.c 以包含 &lt;stdio.h&gt; 并使用 initialise_monitor_handles() 原型并添加一个对 initialise_monitor_handles() 函数在开头 main() 函数。

```text
1
#include &lt;stdio.h&gt;
2
extern void initialise_monitor_handles(void);
3
...
4
int main(void) {
5
/* USER CODE BEGIN 1 */
6
initialise_monitor_handles();
```

3。更新 GCC 链接器项目配置，将 rdimon 库添加到链接库中，如图 24.32 所示。</pre></td>
</tr></tbody></table>

## PDF page 744 — Chapter 24: Advanced Debugging Techniques

Focus: `numbers=01, 02, 0744, 24.32, 24.33, 24.34, 4, 5, 744; negation=; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>![Image from PDF page 744](../images/page-0744-image-01.jpeg)

Figure 24.32: Configure the project to link rdimon library

4. Update GCC Linker project configuration adding “-specs=rdimon.specs” flag In Miscellaneous as shown in Figure 24.33.

![Image from PDF page 744](../images/page-0744-image-02.jpeg)

Figure 24.33: Configure the project to link add rdimon.specs flag

5. Configure the current Debug configuration by selecting ST-LINK (OpenOCD) in the Debug probe field and add “monitor arm semihosting enable” initialization command in Debug Configurations - Startup tab, as shown in Figure 24.34. The Debug Console view is used for semihosting</pre></td>
<td><pre>![Image from PDF page 744](../images/page-0744-image-01.jpeg)

图 24.32：配置项目以链接 rdimon 库

4。在“其他”中更新 GCC 链接器项目配置，添加“-specs=rdimon.specs”标志，如图24.33所示。

![Image from PDF page 744](../images/page-0744-image-02.jpeg)

图 24.33：配置项目以链接 add rdimon.specs 标志

5。通过选择调试探针字段中的 ST-LINK (OpenOCD) 来配置当前的调试配置，并在“调试配置 - 启动”选项卡中添加“monitor arm semihosting enable”初始化命令，如图 24.34 所示。调试控制台视图用于半主机</pre></td>
</tr></tbody></table>

## PDF page 745 — Chapter 24: Advanced Debugging Techniques

Focus: `numbers=01, 02, 03, 0745, 2, 24.34, 24.35, 24.7, 745; negation=Never, not; conditions=If, if, when; identifiers=printf`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>input/output and when debugging, as shown in Figure 24.35.

![Image from PDF page 745](../images/page-0745-image-01.jpeg)

Figure 24.34: Configure the Debug Configuration to enable semihosting with OpenOCD

![Image from PDF page 745](../images/page-0745-image-02.jpeg)

Figure 24.35: The output messages by using semihosting in the Debug Console view

Read Carefully

![Image from PDF page 745](../images/page-0745-image-03.png)

Semihosting implementation in OpenOCD is designed so that every string must be terminated with the newline character (\n) before the string appears on the OpenOCD console. This is a quite common error, and it leads to a lot of frustration the first times programmers start using it. Never forget to terminate every string passed to printf() routine with the (\n).

### 24.7.2 Semihosting Drawbacks

Semihosting is an excellent feature, but it has also several drawbacks. First of all, it works only during a debug session, and it completely hangs the firmware if not running under the GDB control. For example, upload am example using semihosting on your Nucleo board and terminate the debug session. If you reset your board pressing the RESET button, you will see that the firmware hangs. This happens because the firmware is stuck in the printf() routine (more about why this happens in the next paragraph). This is a quite frequent issue that every novice encounters every time it starts working with the STM32 platform.</pre></td>
<td><pre>input/output 以及在调试时，如图 24.35 所示。

![Image from PDF page 745](../images/page-0745-image-01.jpeg)

图 24.34：配置调试设置以通过 OpenOCD 启用半主机模式

![Image from PDF page 745](../images/page-0745-image-02.jpeg)

图 24.35：在调试控制台视图中使用半主机模式输出的消息

请仔细阅读

![Image from PDF page 745](../images/page-0745-image-03.png)

OpenOCD 中的半主机模式实现要求每个字符串在显示到 OpenOCD 控制台之前，必须以换行符（\n）结尾。这是一个非常常见的错误，程序员初次使用时往往会因此感到沮丧。切勿忘记在传递给 printf() 例程的每个字符串末尾添加（\n）。

### 24.7.2 半主机（Semihosting）的缺点

半主机（Semihosting）是一个出色的功能，但它也有几个缺点。首先，它仅在调试会话期间有效，如果未在 GDB 控制下运行，固件将完全挂起。例如，在您的 Nucleo 开发板上上传一个使用半主机（Semihosting）的示例，然后终止调试会话。如果您按下 RESET 按钮重置开发板，您将看到固件挂起了。这是因为固件卡在 printf() 例程中（关于为什么会发生这种情况，将在下一段中详细说明）。这是一个相当常见的问题，每个初学者在开始使用 STM32 平台时都会遇到。</pre></td>
</tr></tbody></table>

## PDF page 748 — Chapter 24: Advanced Debugging Techniques

Focus: `numbers=0x01, 0x02, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0C, 0x0E, 0x0F, 0x10, 0x12, 0x13, 0x15, 0x16, 0x17, 0x18, 0x30, 0x31, 24.12; negation=disables, not; conditions=; identifiers=SYS_CLOCK, SYS_CLOSE, SYS_ELAPSED, SYS_ERRNO, SYS_FLEN, SYS_GET_CMDLINE, SYS_HEAPINFO, SYS_ISERROR, SYS_ISTTY, SYS_OPEN, SYS_READ, SYS_READC, SYS_REMOVE, SYS_RENAME, SYS_SEEK, SYS_SYSTEM, SYS_TICKFREQ`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>Table 24.12: Summary of semihosting operations

Semihosting operation immediate opcode Description EnterSVC 0x17 Sets the processor to Supervisor mode and disables all interrupts by setting both interrupt mask bits in the new CPSR. ReportException 0x18 This SVC can be called by an application to report an exception to the debugger directly. The most common use is to report that execution has completed, using ADP_Stopped_ApplicationExit. SYS_CLOSE 0x02 Closes a file on the host system. The handle must reference a file that was opened with SYS_OPEN. SYS_CLOCK 0x10 Returns the number of centiseconds since the execution started. SYS_ELAPSED 0x30 Returns the number of elapsed target ticks since execution started. Use SYS_TICKFREQ to determine the tick frequency. SYS_ERRNO 0x13 Returns the value of the C library errno variable associated with the host implementation of the semihosting SVCs. SYS_FLEN 0x0C Returns the length of a specified file. SYS_GET_CMDLINE 0x15 Returns the command line used to call the executable, that is, argc and argv. SYS_HEAPINFO 0x16 Returns the system stack and heap parameters. The values returned are typically those used by the C library during initialization. SYS_ISERROR 0x08 Determines whether the return code from another semihosting call is an error status or not. This call is passed a parameter block containing the error code to examine. SYS_ISTTY 0x09 Checks whether a file is connected to an interactive device. SYS_OPEN 0x01 Opens a file on the host system. The file path is specified either as relative to the current directory of the host process, or absolute, using the path conventions of the host operating system. SYS_READ 0x06 Reads the contents of a file into a buffer. SYS_READC 0x07 Reads a byte from the console. SYS_REMOVE 0x0E Deletes a specified file on the host filing system. SYS_RENAME 0x0F Renames a specified file. SYS_SEEK 0x0A Seeks to a specified position in a file using an offset specified from the start of the file. The file is assumed to be a byte array and the offset is given in bytes. SYS_SYSTEM 0x12 Passes a command to the host command-line interpreter. This enables you to execute a system command such as dir, ls, or pwd. The terminal I/O is on the host, and is not visible to the target. SYS_TICKFREQ 0x31 Returns the tick frequency.</pre></td>
<td><pre>表 24.12：半主机（Semihosting）操作摘要

半主机（Semihosting）操作 立即数操作码 描述 EnterSVC 0x17 将处理器设置为 Supervisor 模式，并通过设置新 CPSR 中的两个中断屏蔽位来禁用所有中断。 ReportException 0x18 应用程序可以调用此 SVC 直接向调试器报告异常。最常见的用途是使用 ADP_Stopped_ApplicationExit 报告执行已完成。 SYS_CLOSE 0x02 关闭主机系统上的文件。句柄必须引用使用 SYS_OPEN 打开的文件。 SYS_CLOCK 0x10 返回自执行开始以来的百分之一秒数。 SYS_ELAPSED 0x30 返回自执行开始以来经过的目标滴答数。使用 SYS_TICKFREQ 确定滴答频率。 SYS_ERRNO 0x13 返回与半主机（Semihosting）SVC 的主机实现相关的 C 库 errno 变量的值。 SYS_FLEN 0x0C 返回指定文件的长度。 SYS_GET_CMDLINE 0x15 返回用于调用可执行文件的命令行，即 argc 和 argv。 SYS_HEAPINFO 0x16 返回系统堆栈和堆参数。返回的值通常是 C 库在初始化期间使用的值。 SYS_ISERROR 0x08 确定来自另一个半主机（Semihosting）调用的返回码是否为错误状态。此调用传递一个包含要检查的错误代码的参数块。 SYS_ISTTY 0x09 检查文件是否连接到交互式设备。 SYS_OPEN 0x01 打开主机系统上的文件。文件路径指定为相对于主机进程当前目录的路径，或使用主机操作系统的路径约定指定为绝对路径。 SYS_READ 0x06 将文件内容读取到缓冲区中。 SYS_READC 0x07 从控制台读取一个字节。 SYS_REMOVE 0x0E 删除主机文件系统上的指定文件。 SYS_RENAME 0x0F 重命名指定文件。 SYS_SEEK 0x0A 使用从文件开头指定的偏移量在文件中查找指定位置。假设文件是字节数组，偏移量以字节为单位给出。 SYS_SYSTEM 0x12 将命令传递给主机命令行解释器。这使您可以执行系统命令，如 dir、ls 或 pwd。终端 I/O 在主机上，对目标不可见。 SYS_TICKFREQ 0x31 返回滴答频率。</pre></td>
</tr></tbody></table>

## PDF page 751 — Chapter 25: FAT Filesystem

Focus: `numbers=0, 01, 0751, 1, 10, 1024, 128, 16, 2, 2048, 37, 4, 4096, 512, 751; negation=disable, disabled, not; conditions=; identifiers=exFAT`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>- Supports FAT12, FAT16, FAT32(r0.0) and exFAT(r1.0) filesystems.
- Allows un unlimited number of open files (the only limit is the available SRAM memory).
- Supports up to 10 volumes each one with a size up to 2 TiB at 512 bytes/sector.
- Every file can grow up to 4 GiB on FAT volume and virtually unlimited on exFAT volume.
- The cluster goes up to 128 sectors on FAT volume and up to 16 MiB on exFAT volume.
- Supports 4 different sector sizes: 512, 1024, 2048 and 4096 bytes.

The FatFs library provides up to 37 APIs, and they can be selectively disabled thanks to several configuration macros. In fact, to reduce the flash memory footprint, it is possible to disable unneeded functionalities. FatFs library is coded in pure ANSI C and it is totally abstracted from the underlying hardware. The official library does not provide any support to specific memory technology devices, and it is up to the user to implement the necessary glue to interface the hardware.

![Image from PDF page 751](../images/page-0751-image-01.png)

Figure 1: How the FatFs library interfaces the underlying hardware

ST engineers have integrated the FatFs library in the CubeHAL. They have developed necessary adapters to use FatFs library with the following devices:

- SD memory cards using the SDIO peripheral: the Secure Digital Input Output (SDIO) is an extension of the SD specification that covers I/O functions related to SD and MMC cards. More advanced STM32 microcontrollers, such as some STM32F4 ones (for example, the STM32F401RE) and STM32F7 microcontrollers, provide a this dedicated peripheral. The SDIO</pre></td>
<td><pre>- 支持 FAT12、FAT16、FAT32(r0.0) 和 exFAT(r1.0) 文件系统。
- 允许打开无限数量的文件（唯一的限制是可用的 SRAM 内存）。
- 支持最多 10 个卷，每个卷的大小在 512 字节/扇区的情况下最大可达 2 TiB。
- 在 FAT 卷上，每个文件最大可增长至 4 GiB；在 exFAT 卷上则几乎无限制。
- 在 FAT 卷上，簇最大可达 128 个扇区；在 exFAT 卷上最大可达 16 MiB。
- 支持 4 种不同的扇区大小：512、1024、2048 和 4096 字节。

FatFs 库提供多达 37 个 API，并且可以通过多个配置宏选择性地禁用它们。事实上，为了减少闪存内存占用，可以禁用不需要的功能。FatFs 库使用纯 ANSI C 编写，并且完全与底层硬件抽象。官方库不提供对特定存储技术设备的支持，用户需要自行实现必要的胶水代码以接口硬件。

![Image from PDF page 751](../images/page-0751-image-01.png)

图 1：FatFs 库如何接口底层硬件

ST 工程师已将 FatFs 库集成到 CubeHAL 中。他们开发了必要的适配器，以便使用 FatFs 库与以下设备配合：

- 使用 SDIO 外设的 SD 存储卡：安全数字输入输出（Secure Digital Input Output，SDIO）是 SD 规范的扩展，涵盖了与 SD 和 MMC 卡相关的 I/O 功能。更先进的 STM32 微控制器，如某些 STM32F4 系列（例如 STM32F401RE）和 STM32F7 微控制器，提供了这种专用外设。SDIO</pre></td>
</tr></tbody></table>

## PDF page 752 — Chapter 25: FAT Filesystem

Focus: `numbers=0, 1, 4, 50MHz; negation=not; conditions=If, if, only if, when; identifiers=disk_initialize, disk_ioctl, disk_read, disk_status, disk_write, get_fattime`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>- interface can be configured to work in 1 bit mode (that is, data is transferred to the SD using just one output data port, named DO, plus two additional I/Os for the clock and commands transfer), or to work in 4-bit mode (that is data is transferred using 4 dedicated I/Os in addition to clock and command lines). This is the fastest way to use SD cards, and the maximum transfer rate of 50MHz can be reached in high-performing STM32 microcontrollers.
- Static as well as Dynamic RAM memories: two separated low-level drivers for SDRAM and SRAM memories allow to create filesystems in RAM. These two drivers work in combination with FMC and FSMC controllers. They allow to initialize RAM disks and this feature is especially useful when performances are critical for your application (SRAM are a lot faster than NVM memories).
- USB-based disks: a specific driver built upon the ST USB library allows to create USB Host devices supporting the Mass Storage Class (MSC) (that is a device that can interface USB disks).

Figure 1 shows the relation between the FatFs library and the CubeHAL. Unfortunately, ST engineers have not still developed a driver for SD cards when working in SPI mode. In fact, SD cards are designed to support, among the other protocols, commands exchanged through the SPI bus. However, I have arranged a complete SPI-compliant SD driver that I will introduce you later.

To integrate the FatFs library with a memory device we essentially need to implement the following six routines:

- disk_initialize(): this routine contains all the necessary code to initialize the hardware device. For example, for an SD card working in SPI mode this routine must contain all the necessary code to initialize the SPI interface and to place the SD in SPI mode (there exists a specific procedure to follow, as documented on Chan’s website³).
- disk_status(): this function is used by the library to get information about the device status (for example, if it is initialized, etc.).
- disk_read(): this routine is used to retrieve a given number of sectors from the memory device, starting from a specified sector.
- disk_write(): as its name suggests, this function is used to store a given number of sector on the device.
- disk_ioctl(): this function reads and configures some specific device parameters, such as the size of sectors, the device power state, and so on.
- get_fattime(): returns the current time so that files can have a valid timestamp. If the MCU does not provide an RTC unit, then this function can return 0.

Moreover, the last three routines are needed only if the FatFs library is compiled with the option _FS_READONLY == 0. That is, we can avoid providing a valid implementation for those functions if we use the FatFs read only mode.

³http://bit.ly/2dtWpWS</pre></td>
<td><pre>- 接口可以配置为工作在 1 位模式（即，数据仅通过一个名为 DO 的输出数据端口传输，另外两个额外的 I/O 用于时钟和命令传输），或者工作在 4 位模式（即，数据使用 4 个专用 I/O 传输，外加时钟和命令线）。这是使用 SD 卡的最快方式，在高性能 STM32 微控制器中可以达到 50MHz 的最大传输速率。
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

³http://bit.ly/2dtWpWS</pre></td>
</tr></tbody></table>

## PDF page 765 — Chapter 26: Develop IoT Applications

Focus: `numbers=169MHz, 2.4GHz, 3.0, 5.2, 64, 915MHz; negation=not; conditions=When; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>- TCP (Transmission Control Protocol) with congestion control, RTT estimation and fast recov- ery/fast retransmit
- Raw/native socket API for enhanced performance
- Optional Berkeley-like socket API
- DNS (Domain names resolver)

LwIP also provides complete implementation for the following application protocols:

- HTTP server with SSI and CGI
- SNMPv2c agent with MIB compiler (Simple Network Management Protocol)
- SNTP (Simple network time protocol)
- NetBIOS name service responder
- MDNS (Multicast DNS) responder
- iPerf server implementation

Due to the lack of a RMII interface in STM32 MCUs equipping the Nucleo-64 boards, I will not detail here the operations needed to setup LwIP in your applications. Refer to CubeHAL examples for more about this. Moreover, you can find some posts on my blog regarding this topic. Finally, the CubeMXImporter tool implements all the necessary logic to import the LwIP stack in a GNU MCU Eclipse project.

When it comes to IoT, the wireless protocols play an important role. And ST is aware of the key role of several wireless standards. For this reason, ST also entered in this market arena with two dedicated STM32 series: STM32WB and STM32WL. This first one is addressed to 2.4GHz radio application, and it support Bluetooth 5.2, Bluetooth Mesh as well as other protocols operating in that frequency band, such as the Zigbee 3.0. The second series, the STM32WL, is instead addressed to Sub-Ghz spectrum, ranging from 169MHz up to 915MHz. Moreover, ST has established a partnership with Semtech to develop custom solutions compatible with the Long Range Alliance (LoRa). Thanks to this partnership, the STM32WL series integrates a Semtech LoRa transceiver that supports the LoRaWANTM standardized protocol. ST provides a set of dedicated Nucleo boards for the development with STM32WL and STM32WB series.</pre></td>
<td><pre>- TCP（传输控制协议），具有拥塞控制、RTT 估计和快速恢复/快速重传
- 用于增强性能的原始/原生套接字 API
- 可选的类 Berkeley 套接字 API
- DNS（域名解析器）

LwIP 还为以下应用协议提供完整实现：

- 支持 SSI 和 CGI 的 HTTP 服务器
- 带有 MIB 编译器的 SNMPv2c 代理（简单网络管理协议）
- SNTP（简单网络时间协议）
- NetBIOS 名称服务响应器
- MDNS（多播 DNS）响应器
- iPerf 服务器实现

由于配备 Nucleo-64 板的 STM32 微控制器缺乏 RMII 接口，我将不会在此详细列出在应用中设置 LwIP 所需的步骤。有关此内容的更多信息，请参阅 CubeHAL 示例。此外，你可以在我的博客上找到一些关于此主题的文章。最后，CubeMXImporter 工具实现了所有必要的逻辑，以将 LwIP 协议栈导入 GNU MCU Eclipse 项目。

当谈到物联网时，无线协议起着重要作用。ST 意识到几个无线标准的关键作用。因此，ST 也带着两个专用的 STM32 系列进入了这个市场领域：STM32WB 和 STM32WL。前者面向 2.4GHz 射频应用，支持 Bluetooth 5.2、Bluetooth Mesh 以及在该频段运行的其他协议，如 Zigbee 3.0。后者，STM32WL 系列，则面向 Sub-Ghz 频谱，范围从 169MHz 到 915MHz。此外，ST 与 Semtech 建立了合作伙伴关系，以开发兼容 Long Range Alliance (LoRa) 的自定义解决方案。得益于这一合作伙伴关系，STM32WL 系列集成了支持 LoRaWANTM 标准化协议的 Semtech LoRa 收发器。ST 提供了一套专用的 Nucleo 板，用于 STM32WL 和 STM32WB 系列的开发。</pre></td>
</tr></tbody></table>

## PDF page 774 — Chapter 26: Develop IoT Applications

Focus: `numbers=0, 01, 0774, 0x00, 0x08, 0xab, 0xcd, 0xdc, 0xef, 1, 1.0, 12, 168, 192, 192.168, 2, 24, 255, 4, 4096, 48, 6, 64, 774, 800; negation=not; conditions=as long as, if; identifiers=wizchip_init, wizchip_setnetinfo`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>```text
uint8_t bufSize[] = {12, 4, 0, 0, 0, 0, 0, 0};
wizchip_init(bufSize, bufSize);
```

The above code simply allocates 12KB of TX and RX buffers to the first socket, and the remaining 4KB to the second socket. Clearly, we are free to arrange TX and RX buffer as long as we respect the total size of 16KB.

Once the chip is initialized, we can configure the network interface, by using the function:

```text
void wizchip_setnetinfo(wiz_NetInfo* pnetinfo);
```

where the wiz_NetInfo struct, used to pass to the library the network configuration parameters, is defined in the following way:

```text
typedef struct wiz_NetInfo_t {
uint8_t mac[6];
/* Source Mac Address */
uint8_t ip[4];
/* Source IP Address */
uint8_t sn[4];
/* Subnet Mask */
uint8_t gw[4];
/* Gateway IP Address (optional) */
uint8_t dns[4];
/* DNS server IP Address (optional) */
dhcp_mode dhcp;
/* 1 - Static, 2 - DHCP (optional) */
} wiz_NetInfo;
```

I will not detail those fields here because they are self-explaining. For example, to configure the W5500 so that it can connect to the 192.168.1.0/24 subnet, we can proceed in the following way:

```text
wiz_NetInfo netInfo = {.mac
= {0x00, 0x08, 0xdc, 0xab, 0xcd, 0xef}, // Mac address
.ip
= {192, 168, 1, 192},
// IP address
.sn
= {255, 255, 255, 0},
// Subnet mask
.gw
= {192, 168, 1, 1}};
// Gateway address
wizchip_setnetinfo(&amp;netInfo);
```

![Image from PDF page 774](../images/page-0774-image-01.png)

Please, take note that here we are using an arbitrary MAC address in this example. This procedure is permitted for a private and test environment, but it is completely forbidden if you are planning to sell your W5500 based product. In this case, you have to buy a valid pool of MAC address from IEEE (pools starts from batches of 4096 addresses for about 800 USD⁹). Alternatively, Microchip sells pre-programmed ICs¹⁰ with a valid IEEE EUI-48 and EUI-64 MAC addresses (they work like I²C EEPROM). For small volume productions they are a good alternative to buying custom MAC addresses.

⁹https://bit.ly/34HObty ¹⁰https://bit.ly/2dKLLhA</pre></td>
<td><pre>```text
uint8_t bufSize[] = {12, 4, 0, 0, 0, 0, 0, 0};
wizchip_init(bufSize, bufSize);
```

上述代码简单地将 12KB 的 TX 和 RX 缓冲区分配给第一个套接字，并将剩余的 4KB 分配给第二个套接字。显然，只要尊重 16KB 的总大小，我们可以自由安排 TX 和 RX 缓冲区。

一旦芯片初始化完成，我们就可以使用以下函数来配置网络接口：

```text
void wizchip_setnetinfo(wiz_NetInfo* pnetinfo);
```

其中，用于向库传递网络配置参数的 `wiz_NetInfo` 结构体定义如下：

```text
typedef struct wiz_NetInfo_t {
uint8_t mac[6];
/* Source Mac Address */
uint8_t ip[4];
/* Source IP Address */
uint8_t sn[4];
/* Subnet Mask */
uint8_t gw[4];
/* Gateway IP Address (optional) */
uint8_t dns[4];
/* DNS server IP Address (optional) */
dhcp_mode dhcp;
/* 1 - Static, 2 - DHCP (optional) */
} wiz_NetInfo;
```

这里我不详细解释这些字段，因为它们不言自明。例如，为了配置 W5500 使其能够连接到 192.168.1.0/24 子网，我们可以按以下方式操作：

```text
wiz_NetInfo netInfo = {.mac
= {0x00, 0x08, 0xdc, 0xab, 0xcd, 0xef}, // Mac address
.ip
= {192, 168, 1, 192},
// IP address
.sn
= {255, 255, 255, 0},
// Subnet mask
.gw
= {192, 168, 1, 1}};
// Gateway address
wizchip_setnetinfo(&amp;netInfo);
```

![Image from PDF page 774](../images/page-0774-image-01.png)

请注意，在这个例子中我们使用的是任意的 MAC 地址。这种操作在私有和测试环境中是被允许的，但如果你计划销售基于 W5500 的产品，则是完全禁止的。在这种情况下，你必须从 IEEE 购买有效的 MAC 地址池（地址池从 4096 个地址的批次开始，价格约为 800 美元⁹）。或者，Microchip 销售预编程的 IC¹⁰，具有有效的 IEEE EUI-48 和 EUI-64 MAC 地址（它们的工作方式类似于 I²C EEPROM）。对于小批量生产，它们是购买自定义 MAC 地址的良好替代方案。

⁹https://bit.ly/34HObty ¹⁰https://bit.ly/2dKLLhA</pre></td>
</tr></tbody></table>

## PDF page 808 — Chapter 27: Universal Serial Bus

Focus: `numbers=01, 0808, 1, 1024, 16, 2.0, 27.1, 4.1, 6, 7, 808; negation=not; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>an interrupt endpoint. The exchanged data contains relative coordinates that are used to move the pointer on the screen.

From the USB point-of-view, a message is a series of frames, as shown in Figure 6. Each frame consists of a Start of Frame (SOF) followed by one or more transactions. Each transaction is made up of a series of packets. A packet is preceded with a packet id and a sync pattern and ends with an End of Packet (EOP) pattern. Depending on the transaction type there may be one or more data packets and some transactions may or may not have a handshake packet. At a minimum, a transaction has a token packet.

![Image from PDF page 808](../images/page-0808-image-01.png)

Figure 6: USB communication in a given time-frame

Each packet can contain different pieces of information. What information is included depends on the packet type. The following is a list of the potential information that can be included with a packet:

- Packet ID (PID): declares a transaction type as an IN/OUT/SETUP/SOF.
- Optional Device Address: specifies the device which the message is addressed to.
- Optional Endpoint Address: specifies the endpoint address between 1 and 16 (between 1 and 7 for all STM32 MCUs).
- Optional Payload Data: depending on the packet type and USB version, this can contain up to 1024 bytes of data, whose mining is related to the packet type.
- Optional CRC.

#### 27.1.4.1 Packet Types

According to USB 2.0 specification, there exist four types of packets with a given fixed structure:

- Token packets

- – Initiate transaction – Identify device involved in transaction – Always sourced by the host
- Data packets</pre></td>
<td><pre>中断端点向主机发送多个数据消息。交换的数据包含用于在屏幕上移动指针的相对坐标。

从 USB 的角度来看，消息是一系列帧，如图 6 所示。每个帧由一个帧起始（SOF）后跟一个或多个事务组成。每个事务由一系列数据包组成。数据包前面有一个数据包 ID 和一个同步模式，并以数据包结束（EOP）模式结束。根据事务类型，可能有一个或多个数据包，某些事务可能有或没有握手包。至少，一个事务有一个令牌包。

![Image from PDF page 808](../images/page-0808-image-01.png)

图 6：给定时间帧内的 USB 通信

每个数据包可以包含不同的信息片段。包含哪些信息取决于数据包类型。以下是可以包含在数据包中的潜在信息列表：

- 数据包 ID（PID）：将事务类型声明为 IN/OUT/SETUP/SOF。
- 可选设备地址：指定消息所寻址的设备。
- 可选端点地址：指定 1 到 16 之间的端点地址（对于所有 STM32 MCU，为 1 到 7 之间）。
- 可选有效载荷数据：根据数据包类型和 USB 版本，这可以包含多达 1024 字节的数据，其挖掘与数据包类型相关。
- 可选 CRC。

#### 27.1.4.1 数据包类型

根据 USB 2.0 规范，存在四种具有固定结构的数据包类型：

- 令牌包

- – 启动事务 – 标识参与事务的设备 – 始终由主机发出
- 数据包</pre></td>
</tr></tbody></table>

## PDF page 809 — Chapter 27: Universal Serial Bus

Focus: `numbers=0, 01, 0809, 1, 1024, 16, 1ms, 2, 2.0, 3ms, 4, 5, 7, 809; negation=not, without; conditions=if; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>- – Deliver payload data – Sourced by host or device
- Handshake packets:

- – Acknowledge error-free data receipt – Sourced by host or device
- Special packets

– Facilitates speed differentials – Sourced by host-to-hub devices

Let us analyze these packet types in depth.

TOKEN PACKET Token packets always originate from the host and are used to control the traffic on the bus. The function of the token packet depends on the activity performed. IN tokens are used to request that devices send data to the host. OUT tokens are used to precede data from the host. SETUP tokens are used to precede control commands from the host. SOF tokens are used to mark time frames. In every IN, OUT, and SETUP token packet there is a 7-bit device address, 4-bit endpoint ID, and 5-bit CRC. Figure 7 shows the structure of the five types of token packets.

![Image from PDF page 809](../images/page-0809-image-01.png)

Figure 7: Types of Token packets in USB 2.0

SOF packets give a way for devices to identify the beginning of a frame and synchronize with the host. They are also used to prevent a device from entering suspend mode (which it must do if 3ms pass without an SOF). SOF packets are only seen on full- and high-speed devices and are sent every millisecond. A handshake packet does not occur for an SOF packet. High-speed communication goes a step further with microframes. With a High-Speed device, an SOF is sent out every 125µs and frame count is only incremented every 1ms.

DATA PACKET Data packets follow IN, OUT, and SETUP token packets. The size of the payload data ranges from 0 to 1024 bytes depending on the transfer type and the USB version. The Packet ID toggles between DATA0 and DATA1 for LS/FS devices, and DATA0/1/2/MDATA for HS devices. The packet closes with a 16-bit CRC. The composition of a data packet can be seen in Figure 7. The data toggle is updated at the host and the device for each successful data packet transfer. One advantage to the</pre></td>
<td><pre>- – 传输有效载荷数据 – 由主机或设备发出
- 握手数据包：

- – 确认无误地接收数据 – 由主机或设备发出
- 特殊数据包

– 协调速率差异 – 由主机至集线器的设备发出

让我们深入分析这些数据包类型。

令牌包 令牌包始终由主机发出，用于控制总线上的流量。令牌包的功能取决于所执行的操作。IN 令牌用于请求设备向主机发送数据。OUT 令牌用于在主机发送数据之前发出。SETUP 令牌用于在主机发送控制命令之前发出。SOF 令牌用于标记时间帧。在每个 IN、OUT 和 SETUP 令牌包中，都包含一个 7 位的设备地址、一个 4 位的端点 ID 和一个 5 位的 CRC。图 7 展示了五种令牌包的结构。

![Image from PDF page 809](../images/page-0809-image-01.png)

图 7：USB 2.0 中的令牌包类型

SOF 包为设备提供了一种识别帧起始并与主机同步的方法。它们还用于防止设备进入挂起模式（如果 3ms 内未收到 SOF，设备必须进入该模式）。SOF 包仅出现在全速和高速设备上，并且每毫秒发送一次。SOF 包不会伴随握手包。高速通信更进一步，引入了微帧。对于高速设备，每 125µs 发送一次 SOF，而帧计数仅每 1ms 递增一次。

数据包 数据包跟随 IN、OUT 和 SETUP 令牌包之后。有效载荷数据的大小根据传输类型和 USB 版本的不同，范围从 0 到 1024 字节。对于 LS/FS 设备，数据包 ID 在 DATA0 和 DATA1 之间切换，而对于 HS 设备，则为 DATA0/1/2/MDATA。数据包以一个 16 位的 CRC 结束。数据包的结构如图 7 所示。主机和设备会在每次成功的数据包传输后更新数据切换位。其优势之一是</pre></td>
</tr></tbody></table>

## PDF page 810 — Chapter 27: Universal Serial Bus

Focus: `numbers=0, 1, 27.1, 4.2, 8; negation=not; conditions=If, if; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>data toggle is that it acts as an additional error detection method. If a different packet ID is received than what is expected, the device will be able to know there was an error in the transfer and it can be handled appropriately. An example where the data toggle is used is if an ACK is sent but not received. In this instance, the sender updates the data toggle from 1 to 0 but the receiver does not. The receiver remains at 1. This causes the host and device to be out of sync on the next data stage, which indicates an error.

HANDSHAKE PACKETS Handshake packets conclude each transaction. Each handshake includes an 8-bit packet ID and is sent by the receiver of the transaction. Each USB speed has several options for a handshake response. Which ones are supported depend on the USB speed:

- ACK: acknowledges successful completion. (LS/FS/HS)
- NAK: negative acknowledgement. (LS/FS/HS)
- STALL: Error indication sent by a device. (LS/FS/HS)
- NYET: indicates the device is not ready to receive another data packet. (HS Only)

SPECIAL PACKETS The USB specification defines four special packets.

- PRE: it is issued to hubs by the host to indicate that the next packet is low speed.
- SPLIT: Precedes a token packet to indicate a split transaction. (HS Only)
- ERR: Returned by a hub to report an error in a split transaction. (HS Only)
- PING: Checks the status for a Bulk OUT or Control Write after receiving a NYET handshake. (HS Only)

#### 27.1.4.2 Transaction Types

SETUP, IN and OUT tokens determine three different transaction types. Let us briefly look at them.

##### 27.1.4.2.1 Control Transactions

Control transactions identify, configure, and control devices. They enable the host to read information about a device, set the device address, establish configuration, read an endpoint configuration, issue certain class-related commands and so on. In the enumeration phase, a control transfer is always directed to the control endpoint of a device (which is always the EP0). After the device is completely enumerated, control transfers can be addressed to other endpoints to interact with other device aspects, such as its class (but this is quite uncommon).</pre></td>
<td><pre>数据切换的作用在于它充当一种额外的错误检测方法。如果接收到的数据包 ID 与预期不符，设备便能知道传输过程中出现了错误，并可以对其进行适当处理。使用数据切换的一个示例是：发送方发送了 ACK（确认）但接收方未收到。在这种情况下，发送方会将数据切换从 1 更新为 0，但接收方不会更新。接收方仍保持在 1。这会导致主机和设备在下一个数据阶段失去同步，从而表明发生了错误。

握手数据包 握手数据包用于结束每个事务。每个握手都包含一个 8 位的数据包 ID，并由事务的接收方发送。每种 USB 速度都有几种握手响应选项。具体支持哪些选项取决于 USB 速度：

- ACK：确认成功完成。（LS/FS/HS）
- NAK：否定确认。（LS/FS/HS）
- STALL：由设备发送的错误指示。（LS/FS/HS）
- NYET：表示设备尚未准备好接收另一个数据包。（仅限高速）

特殊数据包 USB 规范定义了四种特殊数据包。

- PRE：由主机向集线器发出，以指示下一个数据包为低速。
- SPLIT：位于令牌数据包之前，以指示拆分事务。（仅限高速）
- ERR：由集线器返回，以报告拆分事务中的错误。（仅限高速）
- PING：在收到 NYET 握手后，检查批量 OUT 或控制写入的状态。（仅限高速）

#### 27.1.4.2 事务类型

SETUP、IN 和 OUT 令牌决定了三种不同的事务类型。让我们简要了解一下它们。

##### 27.1.4.2.1 控制事务

控制事务用于识别、配置和控制设备。它们使主机能够读取有关设备的信息、设置设备地址、建立配置、读取端点配置、发出某些与类相关的命令等。在枚举阶段，控制传输始终指向设备的控制端点（即始终为 EP0）。在设备完全枚举之后，控制传输可以指向其他端点，以与设备的其他方面（例如其类）进行交互（但这种情况相当少见）。</pre></td>
</tr></tbody></table>

## PDF page 811 — Chapter 27: Universal Serial Bus

Focus: `numbers=01, 0811, 0x0, 11, 12, 13, 14, 15, 16, 17, 8, 811; negation=no; conditions=; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>![Image from PDF page 811](../images/page-0811-image-01.png)

Figure 8: An example of a Control transaction

Control transactions have three stages: the setup stage (mandatory), the data stage (optional), and the status stage (mandatory). The status stage includes a single IN or OUT transaction that reports on the success or failure of the previous stages. The data packet for this stage is always DATA1 (unlike normal IN and OUT transactions that toggle between DATA0 and DATA1) and contains a zero-length data packet. The status stage ends with a handshake transaction that is sent by the receiver of the preceding packet.

Figure 8 shows a complete control transaction issued by the host to setup the device address. The packets 11, 12 and 13 identify the setup stage.

Packet 11 is the token packet with a PID equal to SETUP, a destination address equal to 0x0 (corresponding to the new device which is currently in DEFAULT state) and an endpoint ID corresponding to the control endpoint EP0.

Packet 12 is the data packet that contains the effective request to the device. It contains the SET_- ADDRESS command and the corresponding address ID.

Packet 13 is the ACK packet issued by the device. This control transaction has no data stage.

Finally, transaction 14 (made of packets 15, 16 and 17) corresponds to the status stage (see the empty DATA1 packet).</pre></td>
<td><pre>![Image from PDF page 811](../images/page-0811-image-01.png)

图 8：控制事务的示例

控制事务包含三个阶段：设置阶段（必需）、数据阶段（可选）和状态阶段（必需）。状态阶段包含一个 IN 或 OUT 事务，用于报告之前各阶段的执行成功或失败。该阶段的数据包始终为 DATA1（不同于在 DATA0 和 DATA1 之间切换的常规 IN 和 OUT 事务），并且包含一个零长度数据包。状态阶段以接收方针对前一个数据包发送的握手事务结束。

图 8 显示了主机发出的用于设置设备地址的完整控制事务。数据包 11、12 和 13 标识了设置阶段。

数据包 11 是令牌包，其 PID 等于 SETUP，目标地址等于 0x0（对应于当前处于 DEFAULT 状态的新设备），端点 ID 对应于控制端点 EP0。

数据包 12 是包含对设备有效请求的数据包。它包含 SET_ADDRESS 命令及相应的地址 ID。

数据包 13 是由设备发出的 ACK 包。此控制事务没有数据阶段。

最后，事务 14（由数据包 15、16 和 17 组成）对应于状态阶段（参见空 DATA1 包）。</pre></td>
</tr></tbody></table>

## PDF page 812 — Chapter 27: Universal Serial Bus

Focus: `numbers=0, 01, 0812, 2, 2.0, 3, 812; negation=no, not; conditions=When, if; identifiers=CLEAR_FEATURE, DEVICE_REMOTE_, GET_STATUS, SET_ADDRESS, SET_FEATURE, TEST_MODE`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>![Image from PDF page 812](../images/page-0812-image-01.png)

Table 2: Structure of a SETUP token

The content of the data packet right after the SETUP token packet has a well-defined structure which is reported in Table 2. As you can see, a SETUP packet can be sent to a device, an interface (more about this later) or an endpoint. When a SETUP packet is addressed to a device (bmRequestType.Type=0/bmRequestType.Recipient=0), we talk about a Standard Device Request, and the content of the fields bRequest, wValue, wIndex and wLength correspond to one of the rows in the Table 3. As you can see, the SET_ADDRESS request has this structure:

- wValue: it is the address assigned to the new device;
- wIndex: not used field and set to zero;
- wLength: not used field and set to zero;
- Data: the request has no data stage.

The rest of Standard Device Requests have the following usages:

- GET_STATUS: the request is directed at the device, which will return two bytes during the data stage indicating if the device is self-powered and if it has a remote wakeup feature and it can wake the host up during suspend (for example, a click on a mouse button can wake-up the host).
- CLEAR_FEATURE and SET_FEATURE: these requests can be used to set Boolean features. When the designated recipient is the device, the only two feature selectors available are DEVICE_REMOTE_- WAKEUP and TEST_MODE. Test mode allows the device to exhibit various conditions. These are further documented in the USB Specification Revision 2.0.</pre></td>
<td><pre>![Image from PDF page 812](../images/page-0812-image-01.png)

表 2：SETUP 令牌的结构

紧随 SETUP 令牌数据包之后的数据包内容具有明确定义的结构，如表 2 所示。可以看出，SETUP 数据包可以发送至设备、接口（稍后详述）或端点。当 SETUP 数据包寻址到设备（bmRequestType.Type=0/bmRequestType.Recipient=0）时，我们称之为标准设备请求，且字段 bRequest、wValue、wIndex 和 wLength 的内容对应表 3 中的一行。可以看出，SET_ADDRESS 请求具有如下结构：

- wValue：分配给新设备的地址；
- wIndex：未使用的字段，设置为零；
- wLength：未使用的字段，设置为零；
- Data：该请求没有数据阶段。

其余标准设备请求的用途如下：

- GET_STATUS：该请求指向设备，设备将在数据阶段返回两个字节，指示设备是否为自供电以及是否具有远程唤醒功能并能在挂起期间唤醒主机（例如，点击鼠标按钮可以唤醒主机）。
- CLEAR_FEATURE 和 SET_FEATURE：这些请求可用于设置布尔特征。当指定接收方为设备时，仅有的两个特征选择器是 DEVICE_REMOTE_WAKEUP 和 TEST_MODE。测试模式允许设备表现出各种状态。这些内容在 USB 规范修订版 2.0 中有进一步说明。</pre></td>
</tr></tbody></table>

## PDF page 813 — Chapter 27: Universal Serial Bus

Focus: `numbers=0, 01, 02, 0813, 1, 2, 3, 4, 5, 813; negation=not; conditions=When; identifiers=CLEAR_FEATURE, ENDPOINT_HALT, GET_CONFIGURATION, GET_DESCRIPTOR, GET_INTERFACE, GET_STATUS, SET_CONFIGURATION, SET_DESCRIPTOR, SET_FEATURE, SET_INTERFACE`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>- GET_DESCRIPTOR and SET_DESCRIPTOR: these requests are used to set/return the specified descriptor in wValue. A request for the configuration descriptor will return the device descriptor and all interface and endpoint descriptors in the one request. More about descriptors in a while.
- GET_CONFIGURATION and SET_CONFIGURATION: these requests are used to return or set the current device configuration. In the case of a GET_CONFIGURATION request, a byte will be returned during the data stage indicating the devices status. A zero value means the device is not configured and a non-zero value indicates the device is configured. SET_CONFIGURATION is used to enable a device. It should contain the value of bConfigurationValue of the desired configuration descriptor in the lower byte of wValue to select which configuration to enable.

![Image from PDF page 813](../images/page-0813-image-01.png)

Table 3: List of requests in a Standard Device Request

When a control transaction is addressed to an interface (bmRequestType.Type=0 / bmRequest- Type.Recipient=1), we talk about a Standard Interface Request. In this case, the fields of the request can assume the values reported in Table 4. Most of the requests reported in Table 4 are reserved for future usage, apart for the GET_INTERFACE and SET_INTERFACE requests that allows to switch between alternate interfaces configuration, a feature we will describe later.

![Image from PDF page 813](../images/page-0813-image-02.png)

Table 4: List of requests in a Standard Interface Request

When a control transaction is addressed to an endpoint (bmRequestType.Type=0 / bmRequest- Type.Recipient=2), we talk about a Standard Endpoint Request. In this case, the fields of the request can assume the values reported in Table 5. The GET_STATUS request returns two bytes indicating the status (Halted/Stalled) of an endpoint. CLEAR_FEATURE and SET_FEATURE are used to set Endpoint Features. The standard currently defines one endpoint feature selector, ENDPOINT_HALT</pre></td>
<td><pre>- GET_DESCRIPTOR 和 SET_DESCRIPTOR：这些请求用于设置/返回 wValue 中指定的描述符。对配置描述符的请求将在一次请求中返回设备描述符以及所有接口和端点描述符。稍后我们将详细介绍描述符。
- GET_CONFIGURATION 和 SET_CONFIGURATION：这些请求用于返回或设置当前设备配置。对于 GET_CONFIGURATION 请求，将在数据阶段返回一个字节以指示设备状态。零值表示设备未配置，非零值表示设备已配置。SET_CONFIGURATION 用于启用设备。它应在 wValue 的低字节中包含所需配置描述符的 bConfigurationValue 值，以选择要启用的配置。

![Image from PDF page 813](../images/page-0813-image-01.png)

表 3：标准设备请求列表

当控制事务指向接口（bmRequestType.Type=0 / bmRequestType.Recipient=1）时，我们称之为标准接口请求。在这种情况下，请求的字段可以取表 4 中报告的值。表 4 中报告的大多数请求保留供未来使用，除了 GET_INTERFACE 和 SET_INTERFACE 请求，它们允许在备用接口配置之间切换，这是一个我们稍后描述的功能。

![Image from PDF page 813](../images/page-0813-image-02.png)

表 4：标准接口请求列表

当控制事务指向端点（bmRequestType.Type=0 / bmRequestType.Recipient=2）时，我们称之为标准端点请求。在这种情况下，请求的字段可以取表 5 中报告的值。GET_STATUS 请求返回两个字节，指示端点的状态（Halted/Stalled）。CLEAR_FEATURE 和 SET_FEATURE 用于设置端点特性。当前标准定义了一个端点特性选择器，ENDPOINT_HALT</pre></td>
</tr></tbody></table>

## PDF page 860 — Chapter 27: Universal Serial Bus

Focus: `numbers=0, 0x1, 0xFF, 1, 2, 29, 3, 4, 48, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67; negation=; conditions=if; identifiers=CUSTOM_HID_DeInit_FS, CUSTOM_HID_GetData, CUSTOM_HID_Init_FS, CUSTOM_HID_ItfTypeDef, CUSTOM_HID_OutEvent_FS, DAC_ALIGN_12B_R, DAC_CHANNEL_2, HAL_DAC_GetValue, HAL_DAC_SetValue, HAL_GPIO_ReadPin, USBD_OK`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>```text
52
static int8_t CUSTOM_HID_OutEvent_FS(uint8_t *report, uint8_t report_len);
53
static int8_t CUSTOM_HID_GetData(uint8_t *report, uint8_t *report_len);
```

54

```text
55
USBD_CUSTOM_HID_ItfTypeDef USBD_CustomHID_fops_FS = {
56
CUSTOM_HID_ReportDesc_FS,
57
CUSTOM_HID_Init_FS,
58
CUSTOM_HID_DeInit_FS,
59
CUSTOM_HID_OutEvent_FS,
60
CUSTOM_HID_GetData
61
};
```

62

```text
63
static int8_t CUSTOM_HID_Init_FS(void) {
64
return (USBD_OK);
65
}
```

66

```text
67
static int8_t CUSTOM_HID_DeInit_FS(void) {
68
return (USBD_OK);
69
}
```

70

```text
71
static int8_t CUSTOM_HID_OutEvent_FS(uint8_t *report, uint8_t report_len) {
72
HAL_DAC_SetValue(&amp;hdac, DAC_CHANNEL_2, DAC_ALIGN_12B_R,
73
(uint32_t)((report[2] &lt;&lt; 8) | report[3]));
```

74

```text
75
return (USBD_OK);
76
}
```

77

```text
78
static int8_t CUSTOM_HID_GetData(uint8_t *report, uint8_t *report_len) {
79
uint32_t dacValue = 0;
```

80

```text
81
report[0] = 0x1;
82
report[1] = !HAL_GPIO_ReadPin(B1_GPIO_Port, B1_Pin);
```

83

```text
84
dacValue = HAL_DAC_GetValue(&amp;hdac, DAC_CHANNEL_2);
85
report[2] = dacValue &gt;&gt; 8;
86
report[3] = dacValue &amp; 0xFF;
```

87

```text
88
*report_len = 4;
```

89

```text
90
return (USBD_OK);
91
}
```

## The above code shows the modifications to the usbd_customhid-if.c file. Lines [29:48] correspond to the report descriptor described so far. At lines [55:61] there is an instance of the struct USBD_- CUSTOM_HID_ItfTypeDef (defined in the file usbd_customhid.h), which has been modified to add the pointer to an additional function to retrieve the report data: the function is implemented at lines [78:91] and it is self-explanatory. Finally, the callback CUSTOM_HID_OutEvent_FS() is modified so that</pre></td>
<td><pre>```text
52
static int8_t CUSTOM_HID_OutEvent_FS(uint8_t *report, uint8_t report_len);
53
static int8_t CUSTOM_HID_GetData(uint8_t *report, uint8_t *report_len);
```

54

```text
55
USBD_CUSTOM_HID_ItfTypeDef USBD_CustomHID_fops_FS = {
56
CUSTOM_HID_ReportDesc_FS,
57
CUSTOM_HID_Init_FS,
58
CUSTOM_HID_DeInit_FS,
59
CUSTOM_HID_OutEvent_FS,
60
CUSTOM_HID_GetData
61
};
```

62

```text
63
static int8_t CUSTOM_HID_Init_FS(void) {
64
return (USBD_OK);
65
}
```

66

```text
67
static int8_t CUSTOM_HID_DeInit_FS(void) {
68
return (USBD_OK);
69
}
```

70

```text
71
static int8_t CUSTOM_HID_OutEvent_FS(uint8_t *report, uint8_t report_len) {
72
HAL_DAC_SetValue(&amp;hdac, DAC_CHANNEL_2, DAC_ALIGN_12B_R,
73
(uint32_t)((report[2] &lt;&lt; 8) | report[3]));
```

74

```text
75
return (USBD_OK);
76
}
```

77

```text
78
static int8_t CUSTOM_HID_GetData(uint8_t *report, uint8_t *report_len) {
79
uint32_t dacValue = 0;
```

80

```text
81
report[0] = 0x1;
82
report[1] = !HAL_GPIO_ReadPin(B1_GPIO_Port, B1_Pin);
```

83

```text
84
dacValue = HAL_DAC_GetValue(&amp;hdac, DAC_CHANNEL_2);
85
report[2] = dacValue &gt;&gt; 8;
86
report[3] = dacValue &amp; 0xFF;
```

87

```text
88
*report_len = 4;
```

89

```text
90
return (USBD_OK);
91
}
```

## 上述代码展示了 usbd_customhid-if.c 文件的修改。第 [29:48] 行对应于前文所述的报告描述符。在第 [55:61] 行中，有一个 struct USBD_- CUSTOM_HID_ItfTypeDef 的实例（定义在文件 usbd_customhid.h 中），该实例已被修改以添加一个指向额外函数的指针，用于检索报告数据：该函数在第 [78:91] 行实现，其含义不言自明。最后，回调函数 CUSTOM_HID_OutEvent_FS() 被修改，以便</pre></td>
</tr></tbody></table>

## PDF page 863 — Chapter 27: Universal Serial Bus

Focus: `numbers=1, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662; negation=not; conditions=if; identifiers=CUSTOM_HID_EPOUT_ADDR, CUSTOM_HID_OutEvent_FS, GET_REPORT, USBD_CUSTOMHID_OUTREPORT_BUF_SIZE, USBD_CUSTOM_HID_DataOut, USBD_CUSTOM_HID_EP0_, USBD_CUSTOM_HID_EP0_RxReady, USBD_LL_PrepareReceive, USBD_OK, USB_DEVICE`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>## Next, we need to modify the functions USBD_CUSTOM_HID_DataOut() and USBD_CUSTOM_HID_EP0_- RxReady() so that we can pass to the CUSTOM_HID_OutEvent_FS() a report message with a length higher than two.

```text
Filename: Middlewares/ST/STM32_USB_Device_Library/Class/CustomHID/Src/usbd_customhid.c
649
static uint8_t
USBD_CUSTOM_HID_DataOut(USBD_HandleTypeDef *pdev, uint8_t epnum) {
650
USBD_CUSTOM_HID_HandleTypeDef *hhid = (USBD_CUSTOM_HID_HandleTypeDef *)pdev-&gt;pClassData;
651
652
((USBD_CUSTOM_HID_ItfTypeDef *)pdev-&gt;pUserData)-&gt;OutEvent(
653
hhid-&gt;Report_buf, USBD_CUSTOMHID_OUTREPORT_BUF_SIZE);
654
655
USBD_LL_PrepareReceive(pdev, CUSTOM_HID_EPOUT_ADDR, hhid-&gt;Report_buf,
656
USBD_CUSTOMHID_OUTREPORT_BUF_SIZE);
657
658
return USBD_OK;
659
}
660
661
static uint8_t USBD_CUSTOM_HID_EP0_RxReady(USBD_HandleTypeDef *pdev) {
662
USBD_CUSTOM_HID_HandleTypeDef
*hhid = (USBD_CUSTOM_HID_HandleTypeDef *)pdev-&gt;pClassData;
663
664
if (hhid-&gt;IsReportAvailable == 1U) {
665
((USBD_CUSTOM_HID_ItfTypeDef *)pdev-&gt;pUserData)-&gt;OutEvent(
666
hhid-&gt;Report_buf, USBD_CUSTOMHID_OUTREPORT_BUF_SIZE);
667
668
hhid-&gt;IsReportAvailable = 0U;
669
}
670
671
return USBD_OK;
672
}
```

## The example is fully working but with just one notably limitation: the only way to transfer data from the device to the host is by issuing a GET_REPORT request. This is a strong limitation that does not allow us to capture once the USER BUTTON is pressed. We can so modify the example so that a report message is sent to the host once the interrupt connected to GPIO13 fires.

```text
Filename: USB_DEVICE/App/usb_device.c
22
#include &quot;usb_device.h&quot;
23
#include &quot;usbd_core.h&quot;
24
#include &quot;usbd_desc.h&quot;
25
#include &quot;usbd_customhid.h&quot;
26
#include &quot;usbd_custom_hid_if.h&quot;
```

27

```text
28
/* Private variables ---------------------------------------------------------*/
29
volatile int8_t userBtnStatus = -1;
```

30

```text
31
/* USB Device Core handle declaration. */
```</pre></td>
<td><pre>## 接下来，我们需要修改函数 USBD_CUSTOM_HID_DataOut() 和 USBD_CUSTOM_HID_EP0_- RxReady()，以便我们可以向 CUSTOM_HID_OutEvent_FS() 传递长度大于 2 的报告消息。

```text
Filename: Middlewares/ST/STM32_USB_Device_Library/Class/CustomHID/Src/usbd_customhid.c
649
static uint8_t
USBD_CUSTOM_HID_DataOut(USBD_HandleTypeDef *pdev, uint8_t epnum) {
650
USBD_CUSTOM_HID_HandleTypeDef *hhid = (USBD_CUSTOM_HID_HandleTypeDef *)pdev-&gt;pClassData;
651
652
((USBD_CUSTOM_HID_ItfTypeDef *)pdev-&gt;pUserData)-&gt;OutEvent(
653
hhid-&gt;Report_buf, USBD_CUSTOMHID_OUTREPORT_BUF_SIZE);
654
655
USBD_LL_PrepareReceive(pdev, CUSTOM_HID_EPOUT_ADDR, hhid-&gt;Report_buf,
656
USBD_CUSTOMHID_OUTREPORT_BUF_SIZE);
657
658
return USBD_OK;
659
}
660
661
static uint8_t USBD_CUSTOM_HID_EP0_RxReady(USBD_HandleTypeDef *pdev) {
662
USBD_CUSTOM_HID_HandleTypeDef
*hhid = (USBD_CUSTOM_HID_HandleTypeDef *)pdev-&gt;pClassData;
663
664
if (hhid-&gt;IsReportAvailable == 1U) {
665
((USBD_CUSTOM_HID_ItfTypeDef *)pdev-&gt;pUserData)-&gt;OutEvent(
666
hhid-&gt;Report_buf, USBD_CUSTOMHID_OUTREPORT_BUF_SIZE);
667
668
hhid-&gt;IsReportAvailable = 0U;
669
}
670
671
return USBD_OK;
672
}
```

## 该示例完全可用，但存在一个明显的局限性：从设备向主机传输数据的唯一方式是发出 GET_REPORT 请求。这是一个严重的限制，导致我们无法在按下 USER 按钮时立即捕获事件。我们可以修改该示例，使得当连接到 GPIO13 的中断触发时，向主机发送一条报告消息。

```text
Filename: USB_DEVICE/App/usb_device.c
22
#include &quot;usb_device.h&quot;
23
#include &quot;usbd_core.h&quot;
24
#include &quot;usbd_desc.h&quot;
25
#include &quot;usbd_customhid.h&quot;
26
#include &quot;usbd_custom_hid_if.h&quot;
```

27

```text
28
/* Private variables ---------------------------------------------------------*/
29
volatile int8_t userBtnStatus = -1;
```

30

```text
31
/* USB Device Core handle declaration. */
```</pre></td>
</tr></tbody></table>

## PDF page 864 — Chapter 27: Universal Serial Bus

Focus: `numbers=0, 1, 10, 22, 32, 33, 34, 35, 36, 37, 38, 39, 4, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51; negation=; conditions=if; identifiers=DEVICE_FS, Error_Handler, HAL_Delay, HAL_GPIO_EXTI_Callback, HAL_GPIO_ReadPin, MX_USB_DEVICE_Init, USBD_CUSTOM_HID, USBD_CUSTOM_HID_RegisterInterface, USBD_CUSTOM_HID_SendReport, USBD_Init, USBD_OK, USBD_RegisterClass, USBD_Start`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>```text
32
USBD_HandleTypeDef hUsbDeviceFS;
```

33

```text
34
void MX_USB_DEVICE_Init(void) {
35
uint8_t report[4], reportLen;
```

36

```text
37
/* Init Device Library, add supported class and start the library. */
38
if (USBD_Init(&amp;hUsbDeviceFS, &amp;FS_Desc, DEVICE_FS) != USBD_OK) {
39
Error_Handler();
40
}
41
if (USBD_RegisterClass(&amp;hUsbDeviceFS, &amp;USBD_CUSTOM_HID) != USBD_OK) {
42
Error_Handler();
43
}
44
if (USBD_CUSTOM_HID_RegisterInterface(&amp;hUsbDeviceFS, &amp;USBD_CustomHID_fops_FS) != USBD_OK) {
45
Error_Handler();
46
}
47
if (USBD_Start(&amp;hUsbDeviceFS) != USBD_OK) {
48
Error_Handler();
49
}
```

50

```text
51
while(1) {
52
if(userBtnStatus &gt;= 0) {
53
HAL_Delay(10); //Adding a little bit of debouncing
54
if(HAL_GPIO_ReadPin(B1_GPIO_Port, B1_Pin) == userBtnStatus) {
55
USBD_CustomHID_fops_FS.GetData(report, &amp;reportLen);
56
USBD_CUSTOM_HID_SendReport(&amp;hUsbDeviceFS, report, reportLen);
57
}
58
userBtnStatus = -1;
59
}
60
}
61
}
```

62

```text
63
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {
64
if(GPIO_Pin == B1_Pin) {
65
userBtnStatus = HAL_GPIO_ReadPin(B1_GPIO_Port, B1_Pin);
66
}
67
}
```

## How to test the example? Well, we have several options depending on the HOST Operating System.

## - Windows: if you just want to perform a test of the sample firmware, then you can consider the

## SimpleHIDWrite²⁹ tool by Jan Axelson. This tool works very easily. First, you need to select the device you want to exchange data with. The tool will automatically show as much text boxes as many bytes are in the report message. In our case, it will show one byte for the Report ID and three bytes for the rest of the message (see Figure 22).

²⁹http://janaxelson.com/files/SimpleHIDWrite3.zip</pre></td>
<td><pre>```text
32
USBD_HandleTypeDef hUsbDeviceFS;
```

33

```text
34
void MX_USB_DEVICE_Init(void) {
35
uint8_t report[4], reportLen;
```

36

```text
37
/* Init Device Library, add supported class and start the library. */
38
if (USBD_Init(&amp;hUsbDeviceFS, &amp;FS_Desc, DEVICE_FS) != USBD_OK) {
39
Error_Handler();
40
}
41
if (USBD_RegisterClass(&amp;hUsbDeviceFS, &amp;USBD_CUSTOM_HID) != USBD_OK) {
42
Error_Handler();
43
}
44
if (USBD_CUSTOM_HID_RegisterInterface(&amp;hUsbDeviceFS, &amp;USBD_CustomHID_fops_FS) != USBD_OK) {
45
Error_Handler();
46
}
47
if (USBD_Start(&amp;hUsbDeviceFS) != USBD_OK) {
48
Error_Handler();
49
}
```

50

```text
51
while(1) {
52
if(userBtnStatus &gt;= 0) {
53
HAL_Delay(10); //Adding a little bit of debouncing
54
if(HAL_GPIO_ReadPin(B1_GPIO_Port, B1_Pin) == userBtnStatus) {
55
USBD_CustomHID_fops_FS.GetData(report, &amp;reportLen);
56
USBD_CUSTOM_HID_SendReport(&amp;hUsbDeviceFS, report, reportLen);
57
}
58
userBtnStatus = -1;
59
}
60
}
61
}
```

62

```text
63
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {
64
if(GPIO_Pin == B1_Pin) {
65
userBtnStatus = HAL_GPIO_ReadPin(B1_GPIO_Port, B1_Pin);
66
}
67
}
```

## 如何测试该示例？根据主机操作系统不同，我们有几种选择。

## - Windows：如果您只是想测试示例固件，可以考虑使用

## Jan Axelson 开发的 SimpleHIDWrite²⁹ 工具。该工具操作非常简单。首先，您需要选择要与其交换数据的设备。该工具会根据报告消息中的字节数自动显示相应数量的文本框。在我们的情况下，它将显示一个字节用于报告 ID，以及三个字节用于消息的其余部分（参见图 22）。

²⁹http://janaxelson.com/files/SimpleHIDWrite3.zip</pre></td>
</tr></tbody></table>

## PDF page 865 — Chapter 27: Universal Serial Bus

Focus: `numbers=00, 01, 02, 0865, 22, 3, 865; negation=; conditions=if; identifiers=GET_REPORT`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>By setting 01 as the Report ID, the tool will allow to retrieve the report message by clicking on Get Report button (the tool, will send a GET_REPORT request through the control EP0). The received message will have the form **rd** 01 00 00 00. Instead, if we press the USER BUTTON, then the tool will automatically display the report in the form **RD** 01 01 00 00. To set the DAC output we can setup the Report ID to 02 and the last two bytes to 0A 00.

![Image from PDF page 865](../images/page-0865-image-01.jpeg)

Figure 22: The SimpleHIDWrite utility

- Windows, MacOS and Linux: if you need to programmatically access to a HID device, then the hidapi³⁰ is one of the best option to consider, especially if you are making a cross-platform application. hidapi is a library part of the libusb project and it is dedicated to the handling of USB-HID devices. It works on the three major OSes offering the same API. Moreover, there exist several portings of the hidapi library to other languages. For example, the following snippet is written in Python 3 and it uses the cython-hidapi³¹ wrapper to interface our HID example.

³⁰https://github.com/libusb/hidapi ³¹https://github.com/trezor/cython-hidapi</pre></td>
<td><pre>通过将 01 设置为报告 ID，工具将允许通过点击“获取报告”按钮来检索报告消息（工具将通过控制端点 EP0 发送 GET_REPORT 请求）。接收到的消息形式为 **rd** 01 00 00 00。相反，如果我们按下 USER 按钮，工具将自动以 **RD** 01 01 00 00 的形式显示报告。要设置 DAC 输出，我们可以将报告 ID 设置为 02，并将最后两个字节设置为 0A 00。

![Image from PDF page 865](../images/page-0865-image-01.jpeg)

图 22：SimpleHIDWrite 实用工具

- Windows、MacOS 和 Linux：如果需要以编程方式访问 HID 设备，那么 hidapi³⁰ 是最佳选择之一，尤其是在开发跨平台应用程序时。hidapi 是 libusb 项目的一部分，专门用于处理 USB-HID 设备。它在这三大操作系统上均可运行，并提供相同的 API。此外，还存在将 hidapi 库移植到其他语言的多个版本。例如，以下代码片段是用 Python 3 编写的，并使用 cython-hidapi³¹ 封装器来接口我们的 HID 示例。

³⁰https://github.com/libusb/hidapi ³¹https://github.com/trezor/cython-hidapi</pre></td>
</tr></tbody></table>

## PDF page 866 — Chapter 27: Universal Serial Bus

Focus: `numbers=0, 0.05, 0x4, 0x483, 0x5750, 1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 2, 20, 2000, 21, 22, 23, 24, 25, 26; negation=No; conditions=If, if, otherwise; identifiers=get_manufacturer_string, get_product_string, get_serial_number_string, myT`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>```text
Filename: hid_test.py
1
import hid, time, threading, struct
```

2

```text
3
class myT(threading.Thread):
4
def run(self):
5
global hidhandle
6
while True:
7
report = hidhandle.read(0x4)
8
if report[1] == 1:
9
print(&quot;USER BUTTON PRESSED&quot;)
10
elif report[1] == 0:
11
print(&quot;USER BUTTON RELEASED&quot;)
```

12

```text
13
hidhandle = hid.device()
14
hidhandle.open(0x483, 0x5750)
```

15

```text
16
print(&quot;Manufacturer: %s&quot; % hidhandle.get_manufacturer_string())
17
print(&quot;Product: %s&quot; % hidhandle.get_product_string())
18
print(&quot;Serial No: %s&quot; % hidhandle.get_serial_number_string())
```

19

```text
20
t = myT()
21
t.start()
```

22

```text
23
STEP = 50
24
ledStatus = 2000
25
incr = STEP
26
while True:
27
p = tuple(struct.pack(&quot;&gt;H&quot;, ledStatus))
28
hidhandle.write((2,0)+p)
29
if ledStatus &gt;= 3500:
30
incr = -STEP;
31
elif ledStatus &lt;= 2000:
32
incr = STEP
33
ledStatus += incr
34
time.sleep(0.05)
```

## The code should be easy to understand. The class myT is a thread running in background that performs a blocking read() to the device: once the Nucleo’s USER BUTTON is pressed, a new report is issued through the IN endpoint. If the second byte in the report is equal to 1, then the USER BUTTON has been pressed, otherwise it has been released. The other part of the example is just a continuous writing to the OUT endpoint of an unsigned integer ranging from 2000 up to 3500, and vice versa: this will cause the LD2 LED to fade IN and OUT.

## Finally, another solution to test a HID device is to use the hidapitester tool³².

³²https://github.com/todbot/hidapitester/releases</pre></td>
<td><pre>```text
Filename: hid_test.py
1
import hid, time, threading, struct
```

2

```text
3
class myT(threading.Thread):
4
def run(self):
5
global hidhandle
6
while True:
7
report = hidhandle.read(0x4)
8
if report[1] == 1:
9
print(&quot;USER BUTTON PRESSED&quot;)
10
elif report[1] == 0:
11
print(&quot;USER BUTTON RELEASED&quot;)
```

12

```text
13
hidhandle = hid.device()
14
hidhandle.open(0x483, 0x5750)
```

15

```text
16
print(&quot;Manufacturer: %s&quot; % hidhandle.get_manufacturer_string())
17
print(&quot;Product: %s&quot; % hidhandle.get_product_string())
18
print(&quot;Serial No: %s&quot; % hidhandle.get_serial_number_string())
```

19

```text
20
t = myT()
21
t.start()
```

22

```text
23
STEP = 50
24
ledStatus = 2000
25
incr = STEP
26
while True:
27
p = tuple(struct.pack(&quot;&gt;H&quot;, ledStatus))
28
hidhandle.write((2,0)+p)
29
if ledStatus &gt;= 3500:
30
incr = -STEP;
31
elif ledStatus &lt;= 2000:
32
incr = STEP
33
ledStatus += incr
34
time.sleep(0.05)
```

## 代码应易于理解。类 myT 是一个在后台运行的线程，它对设备执行阻塞式 read()：一旦按下 Nucleo 的 USER 按钮，就会通过 IN 端点发出一个新报告。如果报告中的第二个字节等于 1，则表示 USER 按钮已被按下，否则表示已释放。示例的另一部分只是持续向 OUT 端点写入一个从 2000 到 3500 的无符号整数，并反向变化：这将导致 LD2 LED 逐渐变亮和变暗。

## 最后，测试 HID 设备的另一种解决方案是使用 hidapitester 工具³²。

³²https://github.com/todbot/hidapitester/releases</pre></td>
</tr></tbody></table>

## PDF page 875 — Chapter 28: Getting Started with a New Design

Focus: `numbers=0402, 0805, 1.65, 1.8V, 28.1, 28.2, 28.3, 3, 3.6, 4, 600; negation=no, not; conditions=If, if; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>### 28.1.3 Decoupling of Power-Supply Pins

An important design step is the decoupling of every power supply pair (VDD, VSS). The key aspects can be summarized here:

- Each power couple (VDD, VSS) should be connected to a parallel ceramic capacitor of about 100nF (which is a widespread proven value) plus one 4.7µF ceramic capacitor for the overall MCU. It is best to choose 0805 or smaller capacitors (the smaller is the better is, since smaller capacitors have less ESR - for an STM32F7, 0402 capacitors is an option to consider). These capacitors need to be placed as close as possible to the appropriate pins, or the underside of the PCB if a BGA package is used for the fastest STM32 MCUs. If a ground plane is used, it is safe to connect VSS pins directly to the ground plane if this is extensive around that pin.
- This author also uses a large electrolytic capacitor (typically 10µF - a tantalum capacitor is also OK if your budget allows it) no more than 3cm away from the chip. The purpose of this capacitor is to be a reservoir of charge to supply the instantaneous charge requirements of the circuits locally, so the charge need not come through the inductance of the power trace.
- A small ferrite bead (with an impedance ranging from 600 to 1000Ω) placed in series between the analog power supply (AVDD) and digital power supply (VDD)⁸. It is used to:

- – Localizes the noise in the system. – Keeps external high frequency noise from the IC. – Keeps internally generated noise from propagating to the rest of the system.
- If your STM32 MCU provides a VBAT pin, it can be connected to the external battery (1.65 V &lt; VBAT &lt; 3.6 V). If no external battery is used, it is recommended to connect this pin to VDD with a 100nF external ceramic decoupling capacitor.

Figure 28.2 shows the reference schematics of an STM32F030CC MCU, while Figure 28.3 shows the typical layout style used by this author to proper decouple power pins. As you can see, a solid ground plane ensures that decoupling capacitors are connected to the ground with the shortest possible path⁹.

This document¹⁰ from Texas Instruments is a good introduction to this topic.

⁸ST discourages the use of this ferrite if VDD is below 1.8V. ⁹However, keep in mind that the grounding scheme depends on the actual implementation. Some designs need a strong separation between analog and digital ground, plus some EMC-friendly devices (like ferrite beads) to connect them. Welcome to the “obscure” world of EMC :-) ¹⁰http://bit.ly/29pk0J9</pre></td>
<td><pre>### 28.1.3 电源引脚的去耦

一个重要的设计步骤是对每个电源对（VDD, VSS）进行去耦。关键要点可以总结如下：

- 每个电源对（VDD, VSS）应连接一个约 100nF 的并联陶瓷电容（这是一个广泛验证过的值），外加一个 4.7µF 的陶瓷电容用于整个 MCU。最好选择 0805 或更小的电容（越小越好，因为较小的电容具有更低的 ESR - 对于 STM32F7，0402 电容是一个值得考虑的选项）。这些电容需要尽可能靠近相应的引脚放置，或者如果使用 BGA 封装用于最快的 STM32 微控制器，则放置在 PCB 的底部。如果使用地平面，当该引脚周围有广泛的地平面时，可以安全地将 VSS 引脚直接连接到地平面。
- 本作者还在距离芯片不超过 3cm 的地方使用一个大电解电容（通常是 10µF - 如果预算允许，钽电容也可以）。这个电容的目的是作为电荷储备，以供应电路局部的瞬时电荷需求，从而无需通过电源走线的电感来获取电荷。
- 在模拟电源（AVDD）和数字电源（VDD）之间串联放置一个小铁氧体磁珠（阻抗范围从 600 到 1000Ω）⁸。它用于：

- – 将系统中的噪声局部化。 – 防止外部高频噪声进入 IC。 – 防止内部产生的噪声传播到系统的其余部分。
- 如果你的 STM32 微控制器提供 VBAT 引脚，它可以连接到外部电池（1.65 V &lt; VBAT &lt; 3.6 V）。如果没有使用外部电池，建议将此引脚通过一个 100nF 的外部陶瓷去耦电容连接到 VDD。

图 28.2 展示了 STM32F030CC 微控制器的参考原理图，而图 28.3 展示了本作者用于正确去耦电源引脚的典型布局风格。如你所见，完整的地平面确保去耦电容以尽可能短的路径连接到地⁹。

德州仪器（Texas Instruments）的这份文档¹⁰是该主题的良好入门介绍。

⁸ST 不鼓励在 VDD 低于 1.8V 时使用此铁氧体磁珠。⁹然而，请记住，接地方案取决于实际实现。一些设计需要在模拟地和数字地之间进行强隔离，并使用一些对 EMC 友好的器件（如铁氧体磁珠）来连接它们。欢迎来到“晦涩”的 EMC 世界 :-) ¹⁰http://bit.ly/29pk0J9</pre></td>
</tr></tbody></table>

## PDF page 885 — Chapter 28: Getting Started with a New Design

Focus: `numbers=01, 0885, 28.11, 28.12, 5, 885; negation=; conditions=if; identifiers=TX_EN`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>![Image from PDF page 885](../images/page-0885-image-01.jpeg)

Figure 28.11: Pre-visualizing the MCU can help you during board layout

Now you can update your schematics and hence complete the layout of this part. Once the layout is almost complete, you can assign the 5 GPIO to the MCU pins, deciding which one best fits your layout. This is the reason why CubeMX can be used iteratively.

Another important thing regarding CubeMX is the ability to give custom names to signals. This is simply accomplished going into Pinout-&gt;Pins/Signal Options (see Figure 28.12). CubeMX will use the custom labels to generate corresponding C macros inside the main.h file. For example, an I/O labeled “TX_EN” will generate a macro named TX_EN_Pin to indicate the pin and a macro named TX_EN_GPIO_Port to indicate the corresponding GPIO port. This is important especially if you keep synchronized the CAD documentation and the project source files. It will help you to write better and more portable code.

Finally, I prefer to prefix the name of all high-speed signals with “HS_”. This will guide you during the design process: if your CAD allows you to place constraints on nets, it will simplify the routing process, avoiding mistakes that would appear only during test phase.</pre></td>
<td><pre>![Image from PDF page 885](../images/page-0885-image-01.jpeg)

图 28.11：预可视化 MCU 可以帮助您在板级布局过程中

现在您可以更新原理图，从而完成该部分的布局。一旦布局几乎完成，您可以将 5 个 GPIO 分配给 MCU 引脚，决定哪一个最适合您的布局。这就是为什么 CubeMX 可以迭代使用的原因。

关于 CubeMX 的另一个重要方面是能够为信号提供自定义名称。这可以通过进入 Pinout-&gt;Pins/Signal Options 轻松完成（见图 28.12）。CubeMX 将使用自定义标签在 main.h 文件中生成相应的 C 宏。例如，标记为“TX_EN”的 I/O 将生成一个名为 TX_EN_Pin 的宏来指示引脚，以及一个名为 TX_EN_GPIO_Port 的宏来指示对应的 GPIO 端口。如果您保持 CAD 文档和项目源文件同步，这一点尤为重要。它将帮助您编写更好、更可移植的代码。

最后，我倾向于在所有高速信号名称前加上“HS_”前缀。这将在设计过程中为您提供指导：如果您的 CAD 工具允许对网络施加约束，它将简化布线过程，避免那些仅在测试阶段才会暴露的错误。</pre></td>
</tr></tbody></table>

## PDF page 886 — Chapter 28: Getting Started with a New Design

Focus: `numbers=01, 0886, 11, 28.1, 28.12, 886; negation=never, no; conditions=if, when; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>![Image from PDF page 886](../images/page-0886-image-01.jpeg)

Figure 28.12: How to assign custom names to PINs

### 28.1.11 Board Layout Strategies

The layout of the final board is a sort of “art”, a complex task that involves a deep knowledge of all modules used in your design. This is the reason why in large organizations this work is accomplished by specific engineers.

Here, I would like to provide a brief introduction to the whole process based on my personal experience.

- A good layout is all about component placing: if you are new to this task, remember that all starts from placing components on the final board. Every board can be logically and physically divided in sub-modules: power part, MCU and digital part, analog part and so no. Don’t start routing signals before you have placed all components on the final board. Moreover, a good subdivision in sub-modules allows you to reuse design for different boards.
- Follow these steps when doing the layout of an STM32 MCU:

– start placing the MCU; – if your board need external clock sources, place them immediately close to the MCU pins; – next place all decoupling capacitors needed; – connect power sources to the corresponding power lines or power planes if your layer stackup allows them; – never forget to tie to the ground BOOT0 pin if needed, and to decouple NRST pin; – if your design need an external SRAM or a fast flash memory, start placing them and route differential pair first; – route all high speed signals; – route remaining signals;</pre></td>
<td><pre>![Image from PDF page 886](../images/page-0886-image-01.jpeg)

图 28.12：如何为引脚分配自定义名称

### 28.1.11 电路板布局策略

最终电路板的布局是一种“艺术”，是一项复杂的任务，需要对设计中使用的各个模块有深入的了解。这就是为什么在大型组织中，这项工作通常由专门的工程师来完成。

在这里，我想基于个人经验，简要介绍一下整个流程。

- 良好的布局关键在于元器件的摆放：如果你是初学者，请记住一切始于在最终电路板上放置元器件。每块电路板都可以逻辑上和物理上划分为子模块：电源部分、微控制器和数字部分、模拟部分等。在将所有元器件放置到最终电路板之前，不要开始布线。此外，良好的子模块划分有助于你在不同的电路板上复用设计。
- 在对 STM32 微控制器进行布局时，请遵循以下步骤：

– 开始放置微控制器； – 如果你的电路板需要外部时钟源，请将其放置在紧邻微控制器引脚的位置； – 接下来放置所有所需的去耦电容； – 如果你的层叠结构允许，将电源连接到相应的电源走线或电源平面； – 如果需要，切勿忘记将 BOOT0 引脚接地，并对 NRST 引脚进行去耦； – 如果你的设计需要外部 SRAM 或高速闪存，先放置它们并优先布线差分对； – 布线所有高速信号； – 布线其余信号；</pre></td>
</tr></tbody></table>

## PDF page 887 — Chapter 28: Getting Started with a New Design

Focus: `numbers=1, 28.2, 3, 5, 6; negation=never; conditions=If, if; identifiers=USART_PERIPHERAL`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>– avoid using too many vias during the signal routing and use CubeMX looking for better alternatives (that is, use other equivalent signal I/Os if possible).

## 28.2 Software Design

Once you have completed the hardware design, you can start developing the firmware part. If you have used CubeMX to design the MCU section of your custom board, you should be able to start coding the firmware immediately. If the CubeMX project observes faithfully the actual board design, you can simply generate the project as we have done for the Nucleo development board, then you can import it inside a new STM32CubeIDE project and start working on your application. Nothing different from what described in Chapter 3.

If you have already developed the firmware using a development board, and you need to adapt it to your custom design, you may proceed in this way:

- Generate a fresh new CubeMX project both for your development board (e.g., the Nucleo-F030), enabling the needed peripherals, and for the custom board you have designed.
- Do a comparison between the initialization routines for the used peripherals: if they differ, start replacing them one by one in the project made for the development board, and do a complete project compilation before to continue with the next peripheral. This will allow you to keep the control of what is changing in your firmware.
- To simplify the porting process, never change the peripheral initialization code generated by CubeMX, but use CubeMX to change peripheral settings.
- Try to use macros to wrap peripheral handlers. Once you change them, you only need to redefine the macros (for example, if your firmware developed with the Nucleo uses the USART2 peripheral, define a global macro in this way: #define USART_PERIPHERAL huart2 and base your code on that macro; if your new design uses the USART1, then you have to redefine only that macro accordingly).

Remember that CubeMX essentially generates 5 or 6 files. If you reduce the modification to these files at minimum, it will be easy to rearrange the code.

Having a minimum viable firmware made with a development kit helps a lot during the debugging of your custom board. It happens often that, during the testing of a new board, you are in doubt if your issues arise from the hardware or the software. Knowing that the firmware works simplifies the hardware debugging stage.

### 28.2.1 Generating the binary image for production

In large organizations, who effectively loads the binary image of the firmware on the final board is a completely different person. As as engineer, you may be asked to generate an image of the final firmware in release mode. This is a way to indicate a binary image of the firmware compiled with</pre></td>
<td><pre>– 在信号布线过程中避免使用过多的过孔，并使用 CubeMX 寻找更优的替代方案（即，在可能的情况下，使用其他等效信号 I/Os）。

## 28.2 软件设计

完成硬件设计后，即可开始开发固件部分。如果您已使用 CubeMX 设计了自定义板卡上的微控制器部分，那么您应该能够立即开始编写固件代码。如果 CubeMX 项目忠实地遵循了实际的板卡设计，您可以像我们为 Nucleo 开发板所做的那样直接生成项目，然后将其导入到一个新的 STM32CubeIDE 项目中，并开始开发您的应用程序。这与第 3 章中描述的内容没有任何不同。

如果您已经使用开发板完成了固件开发，并且需要将其适配到您的自定义设计中，可以按照以下方式进行：

- 分别为您的开发板（例如 Nucleo-F030）和自行设计的定制板创建全新的 CubeMX 项目，并启用所需的外设。
- 比较所用外设的初始化例程：如果它们存在差异，请在为开发板创建的项目中逐一进行替换，并在继续处理下一个外设之前，先对整个项目进行一次完整编译。这将有助于您掌控固件中正在发生的变化。
- 为了简化移植过程，切勿修改由 CubeMX 生成的外设初始化代码，而应使用 CubeMX 来更改外设设置。
- 尝试使用宏来封装外设处理程序。一旦您更改了它们，只需重新定义这些宏即可（例如，如果您的固件在 Nucleo 上开发时使用了 USART2 外设，请按照以下方式定义一个全局宏：#define

USART_PERIPHERAL huart2，并基于该宏编写代码；如果你的新设计使用 USART1，则只需相应地重新定义该宏即可）。

请记住，CubeMX 基本上会生成 5 或 6 文件。如果您将对这些文件的修改降至最低，代码将更容易重新整理。

使用开发套件制作的最小可行固件在调试自定义电路板时非常有帮助。在测试新电路板时，经常会遇到不确定问题是由硬件还是软件引起的情况。确认固件能够正常工作可以简化硬件调试阶段。

### 28.2.1 生成用于生产的二进制镜像

在大型组织中，负责将固件的二进制映像加载到最终板卡上的人通常是另一个人。作为工程师，你可能会被要求以发布模式生成最终固件的映像。这是一种表明固件的二进制映像已使用</pre></td>
</tr></tbody></table>

## PDF page 888 — Chapter 28: Getting Started with a New Design

Focus: `numbers=01, 0888, 28.13, 6, 888; negation=never, no, without; conditions=if, when; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>the highest possible optimization level, in order to reduce the final size of the image, and without including any debug information. This last requirement is needed both to reduce the size of binary image and to protect the intellectual property (the ELF file of a firmware compiled with debug symbols usually contains the whole firmware source code, so that GDB can show you the original source code while debugging).

From the Eclipse/GCC point of view, generating a binary image in release mode is nothing more than to configure the project accordingly. You might have already noticed that every new Eclipse project comes with two Build Configurations (go to Project-&gt;Build Configurations-&gt;Manage menu if you have never used this feature before): one named Debug and one Release. A build configuration is nothing more than a project configuration, and you can have as many separated configurations as you want in a single project.

![Image from PDF page 888](../images/page-0888-image-01.jpeg)

Figure 28.13: The Eclipse project settings dialog allows to switch to another build configuration easily

Figure 28.13 shows the project settings dialog (go to Project-&gt;Properties menu to open it). The C/C++ Build-&gt;Settings pane allows to configure the build options. Moreover, as you can see in Figure 28.13, you can quickly move to another build configuration using the Configuration combobox. In the Cross ARM C++ Compiler-&gt;Optimization section we can setup the GCC optimization levels. GCC provides 6 optimization levels. Let us briefly introduce them:

- -O0: this corresponds to the no optimization level. It generates unoptimized code but usually has the fastest compilation time. Note that other compilers do extensive optimizations even if no optimization is specified. With GCC, it is very unusual to use -O0 for production if execution time is of any concern, since -O0 does mean no optimization at all. This difference between GCC and other compilers should be kept in mind when doing performance comparisons.</pre></td>
<td><pre>采用尽可能高的优化级别，以减小最终镜像的大小，并且不包含任何调试信息。最后这一项要求既是为了减小二进制镜像的体积，也是为了保护知识产权（使用调试符号编译的固件的 ELF 文件通常包含完整的固件源代码，这样 GDB 在调试时就能显示原始源代码）。

从 Eclipse/GCC 的角度来看，以发布模式生成二进制镜像只不过是相应地配置项目而已。您可能已经注意到，每个新的 Eclipse 项目都带有两个构建配置（如果您以前从未使用过此功能，请转到“项目 -&gt; 构建配置 -&gt; 管理”菜单）：一个名为 Debug（调试），另一个为 Release（发布）。构建配置只不过是项目配置，您可以在单个项目中拥有任意数量的独立配置。

![Image from PDF page 888](../images/page-0888-image-01.jpeg)

图 28.13：Eclipse 项目设置对话框允许轻松切换到另一个构建配置

图 28.13 显示了项目设置对话框（转到“项目 -&gt; 属性”菜单以打开它）。C/C++ 构建 -&gt; 设置窗格允许配置构建选项。此外，正如您在图 28.13 中所见，您可以使用“配置”组合框快速切换到另一个构建配置。在“交叉 ARM C++ 编译器 -&gt; 优化”部分，我们可以设置 GCC 的优化级别。GCC 提供 6 个优化级别。让我们简要介绍一下它们：

- -O0：这对应于无优化级别。它生成未优化的代码，但通常具有最快的编译时间。请注意，即使未指定优化，其他编译器也会进行大量优化。对于 GCC，如果执行时间有任何影响，在生产环境中使用 -O0 是非常不寻常的，因为 -O0 确实意味着完全没有优化。在进行性能比较时，应牢记 GCC 与其他编译器之间的这种差异。</pre></td>
</tr></tbody></table>

## PDF page 889 — Chapter 28: Getting Started with a New Design

Focus: `numbers=; negation=no, not, without; conditions=If, as long as, if, when; identifiers=`

<table><thead><tr><th>Original</th><th>Translation</th></tr></thead><tbody><tr>
<td><pre>- -O1: this corresponds to a moderate optimization. It optimizes reasonably well but does not degrade compilation time significantly.
- -O2: this corresponds to full optimization. It generates highly optimized code and has the slowest compilation time.
- -O3: this also corresponds to full optimization as in “-O2”, but it also uses more aggressive automatic inlining of subprograms within a unit and attempts to vectorize loops.
- -Os: this corresponds to optimization for space. It optimizes space usage (both code and data) of resulting program.
- -Ofast: this corresponds to optimization for speed. It optimizes code to increase its speed at expense fo the final binary size.
- -Og: this corresponds to optimization for debug. It enables optimizations that do not interfere with debugging. It should be the optimization level of choice for the standard edit-compile- debug cycle, offering a reasonable level of optimization while maintaining fast compilation and a good debugging experience.

By default, the GCC optimization level for the Release configuration is -Os. Higher optimization levels perform more global transformations on the program and apply more expensive analysis algorithms in order to generate faster and more compact code. However, in embedded programming is usually suggested to start the development using the no optimization (-O0) level. This because more aggressive optimizations my lead to different behavior of time-constrained routines. As a rule of thumb, develop your firmware with the -O0 or the -Og levels, and start increasing it as long as you test all its features. Sometimes, it also happens that a firmware working perfectly when compiled with the -O0 level stops working at all when a more aggressive optimization is chosen. This often happens we have not correctly declared shared and global variables as volatile, and they are optimized to the compilers causing wrong behavior of ISR routines or different threads if we are using an RTOS.

Another important configuration parameter for the Release configuration is related to Debug level. This feature is configured inside the Cross ARM C++ Compiler-&gt;Debugging view, and GCC offers four increasing levels: None, -g1, -g (the default in Release configuration) and -g3. If you want to generate a binary image without debug information, select the None level.</pre></td>
<td><pre>- -O1：这对应于中等程度的优化。它能较好地优化代码，但不会显著增加编译时间。
- -O2：这对应于完全优化。它生成高度优化的代码，但编译时间最长。
- -O3：这也对应于与“-O2”相同的完全优化，但它还使用更积极的自动内联技术来内联单元内的子程序，并尝试对循环进行向量化。
- -Os：这对应于针对空间的优化。它优化最终程序的代码和数据的空间占用。
- -Ofast：这对应于针对速度的优化。它优化代码以提高其速度，代价是最终二进制文件的大小。
- -Og：这对应于针对调试的优化。它启用不会干扰调试的优化。它应该是标准“编辑-编译-调试”循环的首选优化级别，在保持快速编译和良好调试体验的同时，提供合理的优化水平。

默认情况下，Release 配置的 GCC 优化级别为 -Os。更高的优化级别会对程序执行更多的全局转换，并应用更昂贵的分析算法，以生成更快且更紧凑的代码。然而，在嵌入式编程中，通常建议从无优化（-O0）级别开始开发。这是因为更激进的优化可能会导致受时间约束的例程出现不同的行为。作为经验法则，请使用 -O0 或 -Og 级别开发固件，并在测试其所有功能的同时逐步提高优化级别。有时，使用 -O0 级别编译时运行完美的固件，在选择更激进的优化后可能会完全停止工作。这通常发生在我们未正确地将共享变量和全局变量声明为 volatile 时，导致它们被编译器优化，从而引起 ISR 例程或在使用实时操作系统（RTOS）时的不同线程出现错误行为。

Release 配置的另一个重要配置参数与调试级别（Debug level）相关。此功能在 Cross ARM C++ Compiler-&gt;Debugging 视图中进行配置，GCC 提供四个递增的级别：None、-g1、-g（Release 配置中的默认值）和 -g3。如果您想生成不包含调试信息的二进制映像，请选择 None 级别。</pre></td>
</tr></tbody></table>
