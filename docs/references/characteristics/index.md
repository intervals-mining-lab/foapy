---
hide:
  - toc
---
# foapy.characteristics


The package provides a comprehensive set of characteristics for measuring the properties of an order.

The table below summarizes the available characteristics that depend only on intervals:

| Linear scale | || Logarifmic scale | |
|------------- |-||-|-----------------|
| [Arithmetic Mean](/references/characteristics/arithmetic_mean/) | $\Delta_a = \frac{1}{n} * \sum_{i=1}^{n} \Delta_{i}$ || | |
| [Geometric Mean](/references/characteristics/geometric_mean/) | $\Delta_g=\sqrt[n]{\prod_{i=1}^{n} \Delta_{i}}$ || $g = \frac{1}{n} * \sum_{i=1}^{n} \log_2 \Delta_{i}$ | [Average Remoteness](/references/characteristics/average_remoteness/) |
| [Volume](/references/characteristics/volume/) | $V=\prod_{i=1}^{n} \Delta_{i}$ || $G=\sum_{i=1}^{n} \log_2 \Delta_{i}$ | [Depth](/references/characteristics/depth/) |


The table below summarizes the available characteristics that depend on cogeneric intervals ( grouped by element):

| Characteristics   |                                                                                      |
|-------------------------------|---------------------------------------------------------------------------------------------------------|
| [Descriptive Information](/references/characteristics/descriptive_information/) | $D=\prod_{j=1}^{m}{\left(\sum_{i=1}^{n_j}{\frac{\Delta_{ij}}{n_j}}\right)^{\frac{n_j}{n}}}$                          |
| [Identifying Information](/references/characteristics/identifying_information/) | $H=\frac {1} {n} * \sum_{j=1}^{m}{(n_j * \log_2 \sum_{i=1}^{n_j} \frac{\Delta_{ij}}{n_j})}$ |
| [Regularity](/references/characteristics/regularity/)                     | $r= \sqrt[n]{\prod_{j=1}^{m} \frac{\prod_{j=1}^{n_j} \Delta_{ij}}{{\left(\frac{1}{n_j}\sum_{i=1}^{n_j}{\Delta_{ij}}\right)^{n_j}}}}$  |
| [Uniformity](/references/characteristics/uniformity/)                     | $u = \frac {1} {n} * \sum_{j=1}^{m}{\log_2 \frac{ (\sum_{i=1}^{n_j} \frac{\Delta_{ij}}{n_j})^{n_j} } { \prod_{i=1}^{n_j} \Delta_{ij}}}$                            |


[ma](/references/characteristics/ma/) subpackage provides characteristics for cogeneric intervals ( grouped by element).
