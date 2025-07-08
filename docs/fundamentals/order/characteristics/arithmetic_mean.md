# Arithmetic mean interval

Arithmetic mean interval is an additive measure indifferent to interval ratios.
The arithmetic mean could be used as a reference for comparing with the geometric mean.
The geometric mean and the arithmetic mean are equal when all intervals are equal,
which is true only for the periodic appearance of the elements in the sequence.

## Mathematical Definition

The arithmetic mean interval can be calculated

### from Intervals Chain

Let $IC$ is [_Intervals Chain_](../intervals_chain/index.md#mathematical-definition) described as n-tuple

$$IC = <\Delta_1, \Delta_2, ..., \Delta_n> | \forall j \in \{1,...,n\} \exists \Delta_j \in \{1,...,n\}$$

$$\Delta_a = \frac{1}{n} \times \sum_{i=1}^{n} \Delta_{i}$$

### from Intervals Distribution

Let $ID$ is [_Intervals Distribution_](../intervals_distribution/index.md#mathematical-definition) described as function

$$ID : \{1,...,n\} \longrightarrow \{1,...,n\}$$

$$\Delta_a(ID) = \frac{\sum_{i=1}^{n} \big(i \times ID(i)\big)}{\sum_{i=1}^{n} ID(i)}$$

### Properties

__With Cycle Bindings, the arithmetic mean interval equals the cardinality of an alphabet__

=== "Intervals chain based"
    $IC$ produced by [_Cycled Binding_](../intervals_chain/cycled.md#mathematical-definition)

    $\Delta_a = |alphabet(Intervals^{-1}(IC))|$

=== "Sequence based"
    <!-- is full chain -->
    Let [Sequence](../sequence.md#mathematical-definition) $S$

    $A=alphabet(S)$ is [Alpabet](../alphabet.md#mathematical-definition)

    $IC = Intervals(S)$ produced by [_Cycled Binding_](../intervals_chain/cycled.md#mathematical-definition)

    then $\Delta_a = |A|$
