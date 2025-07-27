# Partial Intervals Distribution

A _Partial intervals distribution_ is an [_Interval distribution_](../order/intervals_distribution/index.md) produced from [_Partial intervals chain_](./intervals_chain/index.md) by counting all _non-empty_ elements (intervals) in distribution


=== "From a partial interval chain"

    ``` mermaid
    block-beta
      columns 7
      space  p1["1"] p2["2"] p3["3"] p4["4"] p5["5"] p6["6"]
      space s1["-"] s2["2"] s3["3"] s4["2"] s5["-"] s6["6"]

      classDef imaginary fill:#526cfe09,color:#000,stroke-dasharray: 10 5;
      classDef position fill:#fff,color:#000,stroke-width:0px;
      class inf,sup imaginary
      class p0,p1,p2,p3,p4,p5,p6,p7 position

      classDef c1 fill:#ff7f0e,color:#fff;
      classDef c2 fill:#ffbb78,color:#000;
      classDef c2a fill:#ffbb788a,color:#000;
      classDef c3 fill:#2ca02c,color:#fff;
      classDef c4 fill:#98df8a,color:#000;
      classDef c4a fill:#98df8a8a,color:#000;
      classDef c5 fill:#d62728,color:#fff;
      classDef c6 fill:#ff9896,color:#000;
      classDef c6a fill:#ff98968a,color:#000;
      classDef c7 fill:#9467bd,color:#fff;
      classDef c8 fill:#c5b0d5,color:#000;
      classDef c9 fill:#8c564b,color:#fff;
      classDef c10 fill:#c49c94,color:#000;
      classDef c11 fill:#e377c2,color:#fff;
      classDef c12 fill:#f7b6d2,color:#000;
      classDef c13 fill:#bcbd22,color:#fff;
      classDef c14 fill:#dbdb8d,color:#000;
      classDef c14a fill:#dbdb8d8a,color:#000;
      classDef c15 fill:#17becf,color:#fff;
      classDef c16 fill:#9edae5,color:#000;

      class pomn,p00,p01,p06,p07,p02n position
      class t1,t2,t5,e0,e1 position

    ```

    Let there be a _partial interval chain_.

=== "calculate intervals distribution"

    ``` mermaid
    block-beta
      columns 7
      space  p1["1"] p2["2"] p3["3"] p4["4"] p5["5"] p6["6"]
      space s1["-"] s2["2"] s3["3"] s4["2"] s5["-"] s6["6"]
      space:7
      space i1["0"] i2["2"] i3["1"] i4["0"] i5["0"] i6["1"]

      classDef imaginary fill:#526cfe09,color:#000,stroke-dasharray: 10 5;
      classDef position fill:#fff,color:#000,stroke-width:0px;
      class inf,sup imaginary
      class p0,p1,p2,p3,p4,p5,p6,p7 position

      classDef c1 fill:#ff7f0e,color:#fff;
      classDef c2 fill:#ffbb78,color:#000;
      classDef c2a fill:#ffbb788a,color:#000;
      classDef c3 fill:#2ca02c,color:#fff;
      classDef c4 fill:#98df8a,color:#000;
      classDef c4a fill:#98df8a8a,color:#000;
      classDef c5 fill:#d62728,color:#fff;
      classDef c6 fill:#ff9896,color:#000;
      classDef c6a fill:#ff98968a,color:#000;
      classDef c7 fill:#9467bd,color:#fff;
      classDef c8 fill:#c5b0d5,color:#000;
      classDef c9 fill:#8c564b,color:#fff;
      classDef c10 fill:#c49c94,color:#000;
      classDef c11 fill:#e377c2,color:#fff;
      classDef c12 fill:#f7b6d2,color:#000;
      classDef c13 fill:#bcbd22,color:#fff;
      classDef c14 fill:#dbdb8d,color:#000;
      classDef c14a fill:#dbdb8d8a,color:#000;
      classDef c15 fill:#17becf,color:#fff;
      classDef c16 fill:#9edae5,color:#000;

      class pomn,p00,p01,p06,p07,p02n position
      class t1,t2,t5,e0,e1 position

      s2 --> i2
      s3 --> i3
      s4 --> i2
      s6 --> i6


    ```

---

_Partial Intervals distribution_, as any _Intervals distribution_, used as an input data in calculating [characteristics](../order/characteristics/index.md).

## Mathematical Definition

Let $-$ is [_empty element_](./carrier_set.md#mathematical-definition).

Let $IC_p$ is [_Partial Interval Chain_](./intervals_chain/index.md#define-intervals-chain) length of $l$ described as function $IC_p : \{1,...,l\} \longrightarrow  \{1,...,l\} \cup \{-\}$

Let $ID$ is [_Interval Distribution_](../order/intervals_distribution/index.md) length of $l$ described as function $ID : \big\{  IC \big\} \longrightarrow \big\{ \{1,...,l\} \longrightarrow  N_0 \big\},$

Define

$$ID_p : \big\{  IC_p \big\} \longrightarrow \big\{ \{1,...,l\} \longrightarrow  N_0 \big\},$$

$$ID_p(IC_p)(i) = ID(IC_p)(i) \bigg|  IC_p(i) \notin \{-\}$$
