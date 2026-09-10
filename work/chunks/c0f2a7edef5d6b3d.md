<!-- page: 383 -->

### 12.2.2 Channel Selection

Depending on the STM32 family and package used, ADCs in STM32 MCUs can convert signals from a variable number of channels. In F0 and L0 families the allocation of channel is fixed: the first one is always IN0, the second IN1 and so on. User can decide only if a channel is enabled or not. This means that in scan mode the first sampled channel will be always IN0, the second IN1 and so on. Other

⁷https://bit.ly/39EFUpk

<!-- page: 384 -->

STM32 MCUs, instead, offer the notion of group. A group consists of a sequence of conversions that can be done on any channel and in any order. While input channels are fixed and bound to specific MCU pins (that is, IN0 is the first channel, IN1 the second and so on), they can be logically reordered to form custom sampling sequences. The reordering of channels is performed by assigning to them an index ranging from 1 to 16. This index is called rank in the CubeHAL.

![Image from PDF page 384](../images/page-0384-image-01.jpeg)

Figure 12.10: How input channels can be reordered using ranks

The Figure 12.10 shows this concept. Although the IN4 channel is fixed (for example, it is connected to PA4 pin in an STM32F401RE MCU), it can be logically assigned to the rank 1 so that it will be the first channel to be sampled. Those MCUs offering this possibility also allow to select the sampling speed of each channel individually, differently from F0/L0 MCUs where the configuration is ADCwide.

The channel/rank configuration is performed by using an instance of the C struct ADC_Channel- ConfTypeDef, which is defined in the following way:

```text
typedef struct {
uint32_t Channel;
/* Specifies the channel to configure into ADC rank */
uint32_t Rank;
/* Specifies the rank ID */
uint32_t SamplingTime;
/* Sampling time value for the selected channel */
uint32_t Offset;
/* Reserved for future use, can be set to 0 */
} ADC_ChannelConfTypeDef;
```

- Channel: specifies the channel ID. It can assume the value ADC_CHANNEL_0, ADC_CHANNEL_- 1…ADC_CHANNEL_N, depending on the effective number of available channels.
- Rank: correspond to the rank associated to the channel. It can assume a value from 1 to 16, which is the maximum number of user-definable ranks.
- SamplingTime: specifies the sampling time value to be set for the selected channel, and it corresponds to the number or ADC cycles. This number cannot be arbitrary, but it is part of a selected list of values. As we will see later, CubeMX helps a lot offering the list of admissible values for the specific MCU you are considering.

There exist two groups for each ADC:

<!-- page: 385 -->

- A regular group, made of up to 16 channels, which corresponds to the sequence of sampled channels during a scan conversion.
- An injected group, made of up to 4 channels, which corresponds to the sequence of injected channel if an injected conversion is performed.

The CubeHAL and its non-linear evolution

![Image from PDF page 385](../images/page-0385-image-01.png)

When working with the CubeHAL, especially if you are new to it and you are following this book’s samples to start learning it, you have to pay close attention while porting some code made for a given STM32 family to another one. For example, consider the ADC_ChannelConfTypeDef.Rank field that in many STM32 MCUs can assume the values 1..16. For those MCUs, it is ok to indicate the rank with the decimal number. But for more recent STM32 MCUs, that value is a result of a computed value that needs to follow a precise scheme. This happens, for example, for the G474RE MCU, where the rank must be specified with the CubeHAL_LL LL_ADC_REG_RANK_1 macro, otherwise the configuration is totally broken. ST should increase the effort in standardizing several things inside the CubeHAL. Unless totally sure, it is always a good thing to start generating the initialization code with CubeMX before re-using other code. This author spent a whole night and the day after before realizing this paramount thing while migrating this chapter’s examples. Sad story.

### 12.2.3 ADC Resolution and Conversion Speed

It is possible to perform faster conversions by reducing the ADC resolution⁸. The sampling time, in fact, is defined by a fixed number of cycles (usually 3) plus a variable number of cycles depending on the A/D resolution. The minimum conversion time for each resolution is then as follows:

- 12 bits: 3 + ∼12 = 15 ADCCLK cycles
- 10 bits: 3 + ∼10 = 13 ADCCLK cycles
- 8 bits: 3 + ∼8 = 11 ADCCLK cycles
- 6 bits: 3 + ∼6 = 9 ADCCLK cycles

By reducing the resolution is so possible to increase the number of maximum samples per seconds, reaching even more then 15Msps in some STM32 MCUs. Remember that the ADCCLK is derived from the peripheral clock: this means that SYSCLK and PCLK speeds impact on the maximum number of samples per second.

⁸This is not possible in STM32F1 MCUs.

<!-- page: 386 -->
