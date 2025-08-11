# Intervals Distribution

An _intervals distribution_ is an n-tuple of natural numbers where the index represents the interval length and the value is a count of its appearances in the _interval chain_.


=== "From an interval chain"

    ``` mermaid
    block-beta
      columns 7
      space  p1["1"] p2["2"] p3["3"] p4["4"] p5["5"] p6["6"]
      space s1["1"] s2["2"] s3["3"] s4["2"] s5["4"] s6["6"]

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

    Let there be an _interval chain_.

=== "calculate intervals distribution"

    ``` mermaid
    block-beta
      columns 7
      space  p1["1"] p2["2"] p3["3"] p4["4"] p5["5"] p6["6"]
      space s1["1"] s2["2"] s3["3"] s4["2"] s5["4"] s6["6"]
      space:7
      space i1["1"] i2["2"] i3["1"] i4["1"] i5["0"] i6["1"]

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

      s1 --> i1
      s2 --> i2
      s3 --> i3
      s4 --> i2
      s5 --> i4
      s6 --> i6


    ```

---

_Intervals distribution_ used as an input data in calculating [characteristics](../characteristics/index.md).
While characteristics could be calculated based on the _itervals chain_ _intervals distribution_ highlights that intervals themselves are enough to measure the [order](../order.md) of a sequence
and intervals connectivity in _intervals chain_ does not affect measure values.
Whether it is possible in general to reconstruct distinctly an _interval chain_ by the given _interval distribution_ is an open question.



_Interval distribution_ is useful in comparing intervals produced from the same sequence with different [_Binding_](../intervals_chain/index.md#define-bindings).
In the interest of studying how _intervals_ depend on _Binding direction_ for [_Bounded Binding_](../intervals_chain/bounded.md) FOA introduce two operations on distributions:

- [Lossy](./lossy.md) - takes two _intervals distribution_ and produce new one only with _intervals_ exists in both distributions.
- [Redundant](./redundant.md) - extends _intervals distribution_ `A` with _intervals_ that appears only in _intervals distrubution_ `B`.

## Mathematical Definition

Let $IC$ is [_Interval Chain_](../intervals_chain/index.md#define-intervals-chain) length of $n$ described as function $IC : \{1,...,n\} \longrightarrow  \{1,...,n\}$

Define

$$ID : \big\{  IC \big\} \longrightarrow \big\{ \{1,...,n\} \longrightarrow  N_0 \big\},$$

$$ID(IC)(i) = \Big| \big\{ j \in \{1,...,n\} | IC(j) = i \big\} \Big|$$
