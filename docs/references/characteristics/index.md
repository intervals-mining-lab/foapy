---
hide:
  - toc
---
# foapy.characteristics


The package provides a comprehensive set of characteristics for measuring the properties of given order.

The table below summarizes the available characteristics that depend only on intervals:

| Linear scale | || Logarithmic scale | |
|------------- |-||-|-----------------|
| [Arithmetic Mean](arithmetic_mean.md) | $\Delta_a = \frac{1}{n} * \sum_{i=1}^{n} \Delta_{i}$ || | |
| [Geometric Mean](geometric_mean.md) | $\Delta_g=\sqrt[n]{\prod_{i=1}^{n} \Delta_{i}}$ || $g = \frac{1}{n} * \sum_{i=1}^{n} \log_2 \Delta_{i}$ | [Average Remoteness](average_remoteness.md) |
| [Volume](volume.md) | $V=\prod_{i=1}^{n} \Delta_{i}$ || $G=\sum_{i=1}^{n} \log_2 \Delta_{i}$ | [Depth](depth.md) |


Congeneric characteristics (grouped by element of the alphabet) are available in the `foapy.congenerics.characteristics` package.
