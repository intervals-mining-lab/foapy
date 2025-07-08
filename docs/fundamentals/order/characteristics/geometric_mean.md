# Geometric mean interval

The geometric mean interval is a multiplicative measure that is sensitive to interval ratios.
This property makes it a cornerstone in measuring [Order](../order.md).

## Mathematical Definition

The geometric mean interval can be calculated

### from Intervals Chain

Let $IC$ is [_Intervals Chain_](../intervals_chain/index.md#mathematical-definition) described as n-tuple

$$IC = <\Delta_1, \Delta_2, ..., \Delta_n> | \forall j \in \{1,...,n\} \exists \Delta_j \in \{1,...,n\}$$

$$\Delta_g=\sqrt[n]{\prod_{i=1}^{n} \Delta_{i}}$$

### from Intervals Distribution

Let $ID$ is [_Intervals Distribution_](../intervals_distribution/index.md#mathematical-definition) described as function

$$ID : \{1,...,n\} \longrightarrow \{1,...,n\}$$

$$\Delta_g(ID)=\sqrt[l]{\prod_{i=1}^{n} i^{ID(i)}}, l = \sum_{i=1}^{n} ID(i)$$

### Properties

__Geometric mean is less or equals arithmetic mean__

$$\Delta_g \le \Delta_a$$
