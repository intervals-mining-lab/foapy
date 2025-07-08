# Volume

The Volume is a product of all intervals, which is sensitive to interval ratios and their count.
The volume value has exponential grow by increasing the interval count (length of the sequence).
This fact makes it useless in computational models due to overflow error.
Use [_Depth_](./depth.md) as an equivalent measure on a logarithmic scale.

## Mathematical Definition

The volume can be calculated

### from Intervals Chain

Let $IC$ is [_Intervals Chain_](../intervals_chain/index.md#mathematical-definition) described as n-tuple

$$IC = <\Delta_1, \Delta_2, ..., \Delta_n> | \forall j \in \{1,...,n\} \exists \Delta_j \in \{1,...,n\}$$

$$V=\prod_{i=1}^{n} \Delta_{i}$$

### from Intervals Distribution

Let $ID$ is [_Intervals Distribution_](../intervals_distribution/index.md#mathematical-definition) described as function

$$ID : \{1,...,n\} \longrightarrow \{1,...,n\}$$

$$V(ID)=\prod_{i=1}^{n} i^{ID(i)}$$

### Properties

__Volume can be calculated base of geometric mean__

$$V = (\Delta_{g})^{n}$$
