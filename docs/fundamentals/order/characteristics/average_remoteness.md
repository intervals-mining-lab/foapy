# Average Remoteness

The Average Remoteness is equivalent of the [geometric mean interval](./geometric_mean.md) on a logarithmic scale.
It is sensitive to interval ratios and is preferable from [computational point of view](https://en.wikipedia.org/wiki/Log_probability).

## Mathematical Definition

The Average Remoteness interval can be calculated

### from Intervals Chain

Let $IC$ is [_Intervals Chain_](../intervals_chain/index.md#mathematical-definition) described as n-tuple

$$IC = <\Delta_1, \Delta_2, ..., \Delta_n> | \forall j \in \{1,...,n\} \exists \Delta_j \in \{1,...,n\}$$

$$g = \frac{1}{n} * \sum_{i=1}^{n} \log_2 \Delta_{i}$$

### from Intervals Distribution

Let $ID$ is [_Intervals Distribution_](../intervals_distribution/index.md#mathematical-definition) described as function

$$ID : \{1,...,n\} \longrightarrow \{1,...,n\}$$

$$g(ID) = \frac{\sum_{i=1}^{n} \big(i \times \log_2 ID(i)\big)}{\sum_{i=1}^{n} ID(i)}$$

### Properties

__Geometric mean equals 2 power average remotness__

$$\Delta_g = 2^{g}$$
