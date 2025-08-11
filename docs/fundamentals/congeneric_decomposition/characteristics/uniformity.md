# Uniformity

The Uniformity

## Mathematical Definition

The uniformity can be calculated

### from Congeneric Intervals Chains

Let $CIC$ is [_Congenerics Intervals Chains_](../intervals_chains.md#as-matrix-ml) defined as matrix

$$
CIC =
\begin{pmatrix}
\Delta_{1,1} & \Delta_{1,2} & \cdots & \Delta_{1,l} \\
\Delta_{2,1} & \Delta_{2,2} & \cdots & \Delta_{2,l} \\
\vdots   & \vdots   & \ddots & \vdots   \\
\Delta_{m,1} & \Delta_{m,2} & \cdots & \Delta_{m,l}
\end{pmatrix}
$$

$$u = \frac {1} {n} * \sum_{j=1}^{m}{\log_2 \frac{ \left(\sum_{i=1}^{l}{\Bigg\{\begin{array}{l}
    \Delta_{i,j}, & \Delta_{i,j} \notin \{-\} \\
    0, &   \Delta_{i,j} \in \{ - \}
\end{array}}\right)^{n_j} } { \prod_{j=1}^{l} \Bigg\{\begin{array}{l}
    \Delta_{i,j}, & \Delta_{i,j} \notin \{-\} \\
    1, &   \Delta_{i,j} \in \{ - \}
\end{array}} }$$

where $m$ the _power_, $n_j = \sum_{i=1}^{l}{\Bigg\{\begin{array}{l}
    1, & \Delta_{i,j} \notin \{-\} \\
    0, &   \Delta_{i,j} \in \{ - \}
\end{array}}$ is count of _non-empty_ elements in $j$ _congeneric intervals chain_,
$\Delta_{i,j}$ the $i$-th element of $j$-th _congeneric intervals chain_.

$$n=\sum_{j=1}^{m}{n_j}$$


### from Congenerics Intervals Distributions

Let $CID$ is [_Congenerics Intervals Distributions_](../intervals_distribution.md#as-matrix-ml) defined as matrix

$$
CID =
\begin{pmatrix}
cid_{1,1} & cid_{1,2} & \cdots & cid_{1,l} \\
cid_{2,1} & cid_{2,2} & \cdots & cid_{2,l} \\
\vdots   & \vdots   & \ddots & \vdots   \\
cid_{m,1} & cid_{m,2} & \cdots & cid_{m,l}
\end{pmatrix}
$$

$$u = \frac {1} {n} * \sum_{j=1}^{m}{\log_2 \Bigg(\frac{ \sum_{i=1}^{l}{(i \times cid_{i,j})}^{n_j} } { \prod_{j=1}^{l} \Bigg\{\begin{array}{l}
    i \times cid_{i,j}, & cid_{i,j} \neq 0 \\
    1, &   cid_{i,j} = 0
\end{array}} }\Bigg)$$


where $m$ the _power_, $n_j = \sum_{i=1}^{l}{cid_{i,j}}$ is count of _non-empty_ elements in $j$ _congeneric intervals distribution_,
$cid_{i,j}$ the $i$-th element of $j$-th _congeneric intervals distribution_.

$$n=\sum_{j=1}^{m}{n_j}$$
