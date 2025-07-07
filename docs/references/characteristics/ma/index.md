---
hide:
  - toc
---
# foapy.characteristics.ma

The package provides a comprehensive set of vector characteristics for measuring the properties of a cogeneric order.

The table below summarizes vector representation of the characteristics that depend only on intervals:

| Linear scale | |Logarifmic scale | |
|------------- |-||-----------------|
| [Arithmetic Mean](arithmetic_mean.md) | $\left[ \Delta_{a_j} \right]_{1 \le j \le m} = \left[ \frac{1}{n_j} * \sum_{i=1}^{n_j} \Delta_{ij} \right]_{1 \le j \le m}$ || |
| [Geometric Mean](geometric_mean.md) | $\left[ \Delta_{g_j} \right]_{1 \le j \le m} = \left[ \left( \prod_{i=1}^{n_j} \Delta_{ij} \right)^{1/n_j} \right]_{1 \le j \le m}$ | $\left[ g_j \right]_{1 \le j \le m} = \left[ \frac{1}{n_j} * \sum_{i=1}^{n_j} \log_2 \Delta_{ij} \right]_{1 \le j \le m}$ | [Average Remoteness](average_remoteness.md) |
| [Volume](volume.md) | $\left[ V_j \right]_{1 \le j \le m} = \left[ \prod_{i=1}^{n_j} \Delta_{ij} \right]_{1 \le j \le m}$  |$\left[ G_j \right]_{1 \le j \le m} = \left[  \sum_{i=1}^{n_j} \log_2 \Delta_{ij} \right]_{1 \le j \le m}$|  [Depth](depth.md) |


The table below summarizes the advanced characteristics of cogeneric intervals:

| Characteristics   |                                                                                      |
|-------------------------------|---------------------------------------------------------------------------------------------------------|
| [Identifying Information](identifying_information.md) | $\left[ H_j \right]_{1 \le j \le m} = \left[ \log_2 { \left(\frac{1}{n_j} * \sum_{i=1}^{n_j} \Delta_{ij} \right) } \right]_{1 \le j \le m}$ |
| [Periodicity](periodicity.md)                     | $\left[ \tau_j \right]_{1 \le j \le m} = \left[ \left( \prod_{i=1}^{n_j} \Delta_{ij} \right)^{1/n_j} * \frac{ n_j }{ \sum_{i=1}^{n_j} \Delta_{ij} } \right]_{1 \le j \le m}$  |
| [Uniformity](uniformity.md)                     | $\left[ u_j \right]_{1 \le j \le m} = \left[ \log_2 { \left(\frac{1}{n_j} * \sum_{i=1}^{n_j} \Delta_{ij} \right) } - \frac{1}{n_j} * \sum_{i=1}^{n_j} \log_2 \Delta_{ij} \right]_{1 \le j \le m}$                            |
