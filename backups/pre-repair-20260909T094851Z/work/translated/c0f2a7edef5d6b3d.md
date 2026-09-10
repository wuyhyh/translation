<!-- page: 383 -->

### 12.2.2 通道选择

根据所使用的 STM32 系列和封装，STM32 微控制器中的 ADC 可以转换来自可变数量通道的信号。在 F0 和 L0 系列中，通道的分配是固定的：第一个始终是 IN0，第二个是 IN1，依此类推。用户只能决定某个通道是否启用。这意味着在扫描模式下，第一个被采样的通道将始终是 IN0，第二个是 IN1，依此类推。其他

⁷https://bit.ly/39EFUpk

<!-- page: 384 -->

STM32 微控制器则提供了“组”的概念。一个组由一系列转换组成，这些转换可以在任何通道上以任意顺序执行。虽然输入通道是固定的，并绑定到特定的微控制器引脚（即 IN0 是第一个通道，IN1 是第二个通道，依此类推），但可以在逻辑上重新排序以形成自定义的采样序列。通道的重新排序是通过为它们分配一个从 1 到 16 的索引来完成的。在 CubeHAL 中，这个索引被称为 rank（排名）。

![Image from PDF page 384](../images/page-0384-image-01.jpeg)

图 12.10：如何使用 rank 重新排序输入通道

图 12.10 展示了这一概念。尽管 IN4 通道是固定的（例如，在 STM32F401RE 微控制器中，它连接到 PA4 引脚），但可以在逻辑上将其分配给 rank 1，使其成为第一个被采样的通道。提供此功能的微控制器还允许单独选择每个通道的采样速度，这与 F0/L0 微控制器不同，后者的配置是 ADC 全局的。

通道/rank 配置通过使用 C 结构体 ADC_ChannelConfTypeDef 的实例来完成，其定义如下：

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

- Channel：指定通道 ID。它可以取值为 ADC_CHANNEL_0、ADC_CHANNEL_1…ADC_CHANNEL_N，具体取决于实际可用的通道数量。
- Rank：对应于与通道关联的 rank。它可以取 1 到 16 之间的值，这是用户可定义 rank 的最大数量。
- SamplingTime：指定要为所选通道设置的采样时间值，它对应于 ADC 周期的数量。这个数字不能任意设定，而是属于选定值列表的一部分。正如我们稍后所见，CubeMX 通过提供针对您正在考虑的特定微控制器的允许值列表，提供了很大的帮助。

每个 ADC 存在两个组：

<!-- page: 385 -->

- 一个规则组（regular group），由最多 16 个通道组成，对应于扫描转换期间被采样通道的序列。
- 一个注入组（injected group），由最多 4 个通道组成，对应于执行注入转换时注入通道的序列。

CubeHAL 及其非线性演变

![Image from PDF page 385](../images/page-0385-image-01.png)

在使用 CubeHAL 时，特别是如果您是初学者并且正在跟随本书的示例开始学习它，在将针对某个 STM32 系列编写的代码移植到另一个系列时，必须格外小心。例如，考虑 ADC_ChannelConfTypeDef.Rank 字段，在许多 STM32 微控制器中它可以取 1..16 的值。对于这些微控制器，使用十进制数字表示 rank 是没问题的。但对于较新的 STM32 微控制器，该值是一个计算结果，需要遵循精确的方案。例如，对于 G474RE 微控制器，必须使用 CubeHAL_LL 宏 LL_ADC_REG_RANK_1 来指定 rank，否则配置将完全损坏。ST 应该增加在 CubeHAL 内部标准化多项工作的力度。除非完全确定，否则在重用其他代码之前，始终建议先使用 CubeMX 生成初始化代码。作者在迁移本章示例时，花了一整晚和第二天才意识到这一至关重要的事情。悲惨的故事。

### 12.2.3 ADC 分辨率和转换速度

通过降低 ADC 分辨率⁸，可以执行更快的转换。事实上，采样时间由固定数量的周期（通常为 3）加上取决于 A/D 分辨率的可变数量周期定义。每种分辨率的最小转换时间如下：

- 12 位：3 + ∼12 = 15 ADCCLK 周期
- 10 位：3 + ∼10 = 13 ADCCLK 周期
- 8 位：3 + ∼8 = 11 ADCCLK 周期
- 6 位：3 + ∼6 = 9 ADCCLK 周期

通过降低分辨率，可以增加每秒最大采样数，在某些 STM32 微控制器中甚至可以达到 15Msps 以上。请记住，ADCCLK 派生自外设时钟：这意味着 SYSCLK 和 PCLK 速度会影响每秒最大采样数。

⁸这在 STM32F1 微控制器中是不可能的。

<!-- page: 386 -->
