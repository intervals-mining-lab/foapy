---
hide:
  - toc
---
# Characteristics

Formal Order Analysis defines several interval-based measures sensitive to the composition of elements in the original sequence.
All those characteristics are based on two main ideas.
The first one is - the geometric mean of two numbers depends on the ratio of them.
The arithmetic mean takes the same value `3` for `1, 5` and `2, 4` pairs, while the geometric mean will be different.

The second is that the intervals we extract from the sequence depend on each other,
replacing two different neighboring elements in the original sequence will affect two intervals and affect the measure results.
We need to highlight that intervals, by definition, are measured between the same event appearances
implicitly encapsulate `information` about the event frequencies and the number of different event types.

In practice, multiplication quickly leads to a stack overflow error. That makes using _linear-scaled_ measures really hard.
To address that problem, FOA uses _logarithmic-scaled_ measure that replaces multiplication of the intervals with the sum of their logarithms.

All characteristics could be calculated based on [_Intervals Chain_](../intervals_chain/index.md) or [_Intervals Distribution_](../intervals_distribution/index.md).
The following table provides _Intervals Chain_ based formulas.

| Linear scale | || Logarithmic scale | |
|------------- |-||-|-----------------|
| [Arithmetic Mean](arithmetic_mean.md) | $\Delta_a = \frac{1}{n} * \sum_{i=1}^{n} \Delta_{i}$ || | |
| [Geometric Mean](geometric_mean.md) | $\Delta_g=\sqrt[n]{\prod_{i=1}^{n} \Delta_{i}}$ || $g = \frac{1}{n} * \sum_{i=1}^{n} \log_2 \Delta_{i}$ | [Average Remoteness](average_remoteness.md) |
| [Volume](volume.md) | $V=\prod_{i=1}^{n} \Delta_{i}$ || $G=\sum_{i=1}^{n} \log_2 \Delta_{i}$ | [Depth](depth.md) |
