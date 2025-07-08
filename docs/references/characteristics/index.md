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


The table below summarizes the available characteristics that depend on cogeneric intervals ( grouped by element of the alphabet):

| Characteristics   |                                                                                      |
|-------------------------------|---------------------------------------------------------------------------------------------------------|
| [Descriptive Information](descriptive_information.md) | $D=\prod_{j=1}^{m}{\left(\sum_{i=1}^{n_j}{\frac{\Delta_{ij}}{n_j}}\right)^{\frac{n_j}{n}}}$                          |
| [Identifying Information](identifying_information.md) | $H=\frac {1} {n} * \sum_{j=1}^{m}{(n_j * \log_2 \sum_{i=1}^{n_j} \frac{\Delta_{ij}}{n_j})}$ |
| [Regularity](regularity.md)                     | $r= \sqrt[n]{\prod_{j=1}^{m} \frac{\prod_{j=1}^{n_j} \Delta_{ij}}{{\left(\frac{1}{n_j}\sum_{i=1}^{n_j}{\Delta_{ij}}\right)^{n_j}}}}$  |
| [Uniformity](uniformity.md)                     | $u = \frac {1} {n} * \sum_{j=1}^{m}{\log_2 \frac{ (\sum_{i=1}^{n_j} \frac{\Delta_{ij}}{n_j})^{n_j} } { \prod_{i=1}^{n_j} \Delta_{ij}}}$                            |


[ma](ma/index.md) subpackage provides characteristics for cogeneric intervals ( grouped by element).
