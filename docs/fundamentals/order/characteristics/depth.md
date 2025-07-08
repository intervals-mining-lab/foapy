# Depth

The Depth is equivalent of [Volume](./volume.md) on  on a logarithmic scale.
It is sensitive to interval ratios and their count (length of the sequence).
The Depth is better then Volume from [computational point of view](https://en.wikipedia.org/wiki/Log_probability)

## Mathematical Definition

The depth can be calculated

### from Intervals Chain

Let $IC$ is [_Intervals Chain_](../intervals_chain/index.md#mathematical-definition) described as n-tuple

$$IC = <\Delta_1, \Delta_2, ..., \Delta_n> | \forall j \in \{1,...,n\} \exists \Delta_j \in \{1,...,n\}$$

$$G=\sum_{i=1}^{n} \log_2 \Delta_{i}$$

### from Intervals Distribution

Let $ID$ is [_Intervals Distribution_](../intervals_distribution/index.md#mathematical-definition) described as function

$$ID : \{1,...,n\} \longrightarrow \{1,...,n\}$$

$$V(ID)=\prod_{i=1}^{n} i^{ID(i)}$$

$$G(ID)=\sum_{i=1}^{n} \big(i \times \log_2 ID(i)\big)$$

### Properties

__Volume equals 2 power depth__

$$V = 2^{G}$$
