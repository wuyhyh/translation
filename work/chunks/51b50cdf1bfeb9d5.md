<!-- page: 455 -->

# 16. Cyclic Redundancy Check

In digital systems it is perfectly possible that data gets corrupted, especially if it flows through a communication medium. In digital electronics, a message is a stream of bits either equal to 0 or 1 and it becomes corrupted when one of more of these bits accidentally change during transmission. For this reason, messages are always exchanged with some additional data used to detect if the original message was corrupted. In Chapter 8 we have analyzed an early form of error detection related to data transmission: the parity bit is an additional bit added to the message used to keep track if the number of bits equal to 1 is odd or even (depending on the type of parity). However, this method is not able to detect errors if two or more bits change at the same time.

The Cyclic Redundancy Check (CRC) is a widely used technique for detecting errors in digital data, both during transmission and storage. In the CRC method, several check bits, called the checksum¹, are appended to the message being transmitted. The receiver can determine whether the check bits agree with the data, to assert with a certain degree of probability if an error occurred in transmission. If so, the receiver can ask to the sender to retransmit the message again. This technique is also applied in some data storage devices, such as Hard Disk Drives. In this case each block on the disk would have certain check bits, and the hardware might automatically initiate a reread of the block when an error is detected, or it might report the error to software. It is important to underline that CRC is a good method to identify corrupted messages, but not for making corrections when errors are detected.

Being the CRC method used by a lot of communication peripherals and protocols (like the Ethernet, MODBUS, etc.), it is quite common to find in microcontrollers dedicated hardware peripherals able to compute CRC checksum of byte streams, freeing the CPU from performing this operation in software. All STM32 microcontrollers provide a dedicated CRC peripheral, and this chapter briefly explains how to use the corresponding CubeHAL module.

As usual, before going into the implementation details, we will first give a brief introduction to the math behind the CRC technique².

## 16.1 Introduction to CRC Computing

CRC technique is based on well-known properties of polynomial arithmetic. To compute the checksum of a stream of bits, the message is seen as a polynomial that is divided by another fixed polynomial, called generator polynomial. The remainder of this operation is the checksum, which is

¹The checksum is often called the CRC. This is not entirely correct, because the CRC is a specific error-detecting method, which uses a well-characterized algorithm plus a checksum sequence of bits to detect if a message is corrupted. However, it is quite common to refer to the checksum as the CRC, or the CRC code. ²An excellent dissertation of CRC algorithms is represented by this on-line document by Ross N. Williams (http://www.zlib.net/crc_v3.txt)

<!-- page: 456 -->

added to original message. The receiver will use it, together with the generator polynomial, to check if the message is correct.

In practice, all CRC methods use polynomials in GF(2ⁿ). GF(pⁿ) stands for Galois field, also known as finite field, that is a field with a finite number of elements. As with any field, a Galois field is a set on which the operations of multiplication, addition, subtraction and division are defined and satisfy certain basic rules. The most common examples of finite fields are given by the integers modulo p, where p is a prime number. In our case, p is equal to 2 and this implies that the GF(2ⁿ) field contains only two elements, when n=1: 0 and 1.

In GF(2ⁿ) addition and subtraction are performed modulo 2, that is they correspond to the XOR logical operation.

⊕ 0 1 0 0 1 1 1 0

The multiplication, instead, corresponds to the AND logical operation.

∧0 1 0 0 0 1 0 1

Polynomials in GF(2ⁿ) are polynomials in a single variable x whose coefficients are either 0 or 1. The CRC technique interprets the bits of a data message as coefficients of a polynomial in GF(2ⁿ) with a degree equal to n −1, where n is the length of the message. For example, assuming the message 111001102, whose length is equal to 8, this corresponds to the polynomial:

x7 · 1 + x6 · 1 + x5 · 1 + x4 · 0 + x3 · 0 + x2 · 1 + x1 · 1 + x0 · 0 = x7 + x6 + x5 + x2 + x

As said before, in GF(2ⁿ) addition and subtraction correspond to XOR logical operation. This means that the sum of the polynomials x4 + x3 + 1 and x3 + x + 1 is equal to x4 + x³. Clearly, this is also the same of the subtraction of the two polynomials.

Multiplication of polynomials in GF(2ⁿ) is, as usual, much like multiplying decimal integers keeping track of powers of x instead of decimal places. For example, multiplying the previous two polynomials we have:

³Instead, in normal algebra the addition would be equal to x4 + 2x3 + x + 2.

<!-- page: 457 -->

![Image from PDF page 457](../images/page-0457-image-01.png)

As you can see, each term in the first multiplies each term in the second, and then we add them following the addition rules in GF(2ⁿ).

Division of one polynomial by another in GF(2ⁿ) is analogous to long division (with remainder) of integers, except there is no borrowing nor carrying. For example, let us divide the polynomial x7 + x6 + x5 + x2 + x by the polynomial x3 + x + 1.

![Image from PDF page 457](../images/page-0457-image-02.png)

We start by dividing the first term of the dividend by the highest term of the divisor (meaning the one with the highest power of x, which in this case is x3). Next, we multiply the divisor by the result just obtained (the first term of the eventual quotient).

![Image from PDF page 457](../images/page-0457-image-03.png)

Now we subtract the product just obtained from the appropriate terms of the original dividend applying the rules of subtraction in GF(2ⁿ).

![Image from PDF page 457](../images/page-0457-image-04.png)

We repeat the previous steps, except this time use the two terms that have just been written as the dividend.

<!-- page: 458 -->

![Image from PDF page 458](../images/page-0458-image-01.png)

The process continues until the obtained dividend has a degree lower than the divisor. We have so obtained the remainder of the division, which represents the checksum to append to the original message.

![Image from PDF page 458](../images/page-0458-image-02.png)

There are two ways for the receiver to assess the correctness of the transmission. It can compute the checksum from the first n bits of the received data, and verify that it agrees with the last r received bits. Alternatively, and following usual practice, the receiver can divide all the received bits by the generator polynomial and check that the r-bit remainder is 0.

However, the exact algorithm of CRC calculation usually differs from the normal polynomial division. Moreover, the generator polynomial may define specific initial and final condition, as we will see soon. This means that the generator polynomial cannot be left to change, but it is kept from a portfolio⁴ of well-studied polynomials. For example, the widely adopted CRC-32 polynomial has the form:

x26 + x23 + x22 + x16 + x12 + x11 + x10 + x8 + x7 + x5 + x4 + x2 + x + 1

which can be represented in binary with the sequence 000001001100000100011101101101112 and in hexadecimal with the number 0x04C1 1DB7. It is adopted by many transmission and storage protocols, like Ethernet, Serial ATA, MPEG-2, BZip2 and PNG.
