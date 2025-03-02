---
hide:
  - toc
---
# foapy.characteristics.ma

The package provides a comprehensive set of vector characteristics for measuring the properties of a cogeneric order.

The table below summarizes vector representation of the characteristics that depend only on intervals:

| Linear scale | |Logarifmic scale | |
|------------- |-||-----------------|
| [Arithmetic Mean](/references/characteristics/ma/arithmetic_mean/) | $\left[ \Delta_{a_j} \right]_{1 \le j \le m} = \left[ \frac{1}{n_j} * \sum_{i=1}^{n_j} \Delta_{ij} \right]_{1 \le j \le m}$ || |
| [Geometric Mean](/references/characteristics/ma/geometric_mean/) | $\left[ \Delta_{g_j} \right]_{1 \le j \le m} = \left[ \left( \prod_{i=1}^{n_j} \Delta_{ij} \right)^{1/n_j} \right]_{1 \le j \le m}$ | $\left[ g_j \right]_{1 \le j \le m} = \left[ \frac{1}{n_j} * \sum_{i=1}^{n_j} \log_2 \Delta_{ij} \right]_{1 \le j \le m}$ | [Average Remoteness](/references/characteristics/ma/average_remoteness/) |
| [Volume](/references/characteristics/ma/volume/) | $\left[ V_j \right]_{1 \le j \le m} = \left[ \prod_{i=1}^{n_j} \Delta_{ij} \right]_{1 \le j \le m}$  |$\left[ G_j \right]_{1 \le j \le m} = \left[  \sum_{i=1}^{n_j} \log_2 \Delta_{ij} \right]_{1 \le j \le m}$|  [Depth](/references/characteristics/ma/depth/) |


The table below summarizes the advanced characteristics of cogeneric intervals:

| Characteristics   |                                                                                      |
|-------------------------------|---------------------------------------------------------------------------------------------------------|
| [Identifying Information](/references/characteristics/ma/identifying_information/) | $\left[ H_j \right]_{1 \le j \le m} = \left[ \log_2 { \left(\frac{1}{n_j} * \sum_{i=1}^{n_j} \Delta_{ij} \right) } \right]_{1 \le j \le m}$ |
| [Periodicity](/references/characteristics/ma/periodicity/)                     | $\left[ \tau_j \right]_{1 \le j \le m} = \left[ \left( \prod_{i=1}^{n_j} \Delta_{ij} \right)^{1/n_j} * \frac{ n_j }{ \sum_{i=1}^{n_j} \Delta_{ij} } \right]_{1 \le j \le m}$  |
| [Uniformity](/references/characteristics/ma/uniformity/)                     | $\left[ u_j \right]_{1 \le j \le m} = \left[ \log_2 { \left(\frac{1}{n_j} * \sum_{i=1}^{n_j} \Delta_{ij} \right) } - \frac{1}{n_j} * \sum_{i=1}^{n_j} \log_2 \Delta_{ij} \right]_{1 \le j \le m}$                            |
