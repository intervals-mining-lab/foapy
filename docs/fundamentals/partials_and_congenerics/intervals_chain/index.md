# Partial Intervals Chain

_Partial Intervals Chain_ is an [_Intervals chain_](../../order/intervals_chain/index.md#mathematical-definition) that could contains `-` [_empty_](../carrier_set.md#mathematical-definition) elements. All statements valid for an _intervals chain elements_  should be valid for _non-empty_ elements of _partial intervals chain_

The idea of _partial intervals chain_ is easy to explain by a concrete example:


=== "From a partial sequence"

    ``` mermaid
    block-beta
        columns 8
        space        p1["1"] space:3         p5["5"]                p6["l"] space
        space s1["-"] s2["C"] s3["T"] s4["C"] s5["-"] s6["G"] space

        classDef imaginary fill:#526cfe09,color:#000,stroke-dasharray: 10 5;
        classDef position fill:#fff,color:#000,stroke-width:0px;
        class inf,sup imaginary
        class p0,p1,p5,p6,p7 position

        classDef skip fill:#ffffff

        class s1,s5 skip

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
    ```

    Let there be a partial sequence length of $l=6$ (indexed from 1 to l=6)

=== "with a binding"

    ``` mermaid
    block-beta
      columns 7
      p0["0"]        p1["1"] p2["2"] space  p4["4"]       p5["5"]                p6["6"]
      inf["⊥"] s1["-"] s2["C"] s3["T"] s4["C"] s5["-"] s6["G"]
      e0["0 = Iteratorₚ(2)"]:3 space:4
      space:2      t1["2 = Iteratorₚ(4)"]:3         space:2

      classDef imaginary fill:#526cfe09,color:#000,stroke-dasharray: 10 5;
      classDef position fill:#fff,color:#000,stroke-width:0px;
      class inf,sup imaginary
      class p0,p1,p2,p4,p5,p6,p7 position

      classDef skip fill:#ffffff
      class s1,s5 skip

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

      class s2,s4 c4
      class inf,t1,e0 c4a
      class pomn,p00,p01,p06,p07,p02n position
      class t1,t2,t5,e0,e1 position

    ```

    Define $Binding_p$ as a pair of an $Iterator_p$ function, that seeks a corresponding referenced element, and
    set of _terminate states_, to determine the interval when there is no matching element in the sequence.
    For `-` _empty_ elements, we do not search for matching elements - just put `-` instead of matching value.

=== "get correspoding indexes"

    ``` mermaid
    block-beta
      columns 7
      p0["0"]  p1["1"] p2["2"] p3["3"] p4["4"] p5["5"] p6["6"]
      inf["⊥"] s1["-"] s2["C"] s3["T"] s4["C"] s5["-"] s6["G"]
      space i1["-"] i2["0"] i3["0"] i4["2"] i5["-"] i6["0"]

      classDef imaginary fill:#526cfe09,color:#000,stroke-dasharray: 10 5;
      classDef position fill:#fff,color:#000,stroke-width:0px;
      class inf,sup imaginary
      class p0,p1,p2,p3,p4,p5,p6,p7 position

      classDef skip fill:#ffffff
      class s1,s5 skip

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

      class s1,s5,i1,i5 skip
      class s2,s4,i2,i4 c1
      class s3,i3 c5
      class s6,i6 c7
      class pomn,p00,p01,p06,p07,p02n position
      class t1,t2,t5,e0,e1 position

    ```

    With $Binding_p$ we can get a sequence of corresponding indexes.
    For all first appearances of the elements it would be $0$,
    and for `C` at position `4` corresponding index would be `2`.

=== "and calculate partial intervals chain"

    ``` mermaid
    block-beta
      columns 7
      p0["0"]  p1["1"] p2["2"] p3["3"] p4["4"] p5["5"] p6["6"]
      space i1["-"] i2["0"] i3["0"] i4["2"] i5["-"] i6["0"]
      space s1["-"] s2["2"] s3["3"] s4["2"] s5["-"] s6["6"]

      classDef imaginary fill:#526cfe09,color:#000,stroke-dasharray: 10 5;
      classDef position fill:#fff,color:#000,stroke-width:0px;
      class inf,sup imaginary
      class p0,p1,p2,p3,p4,p5,p6,p7 position

      classDef skip fill:#ffffff

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

      class s1,s5,i1,i5 skip
      class s2,s4,i2,i4 c1
      class s3,i3 c5
      class s6,i6 c7
      class pomn,p00,p01,p06,p07,p02n position
      class t1,t2,t5,e0,e1 position

    ```

    Calculated interval by $Intervals_p$ function is the [absolute value](https://en.wikipedia.org/wiki/Absolute_value)
    of difference the _corresponding index_ and the _index_. For example, for index `4` interval would be $|4-2|=2$


---

There should exists an inverse function that restores by _interval chain_ a sequence with the original [order](../order/index.md)

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

      classDef skip fill:#ffffff
      class s1,s5 skip

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

=== "calculate correspoding indexes"

    ``` mermaid
    block-beta
      columns 7
      p0["0"]  p1["1"] p2["2"] p3["3"] p4["4"] p5["5"] p6["6"]
      space s1["-"] s2["2"] s3["3"] s4["2"] s5["-"] s6["6"]
      space i1["-"] i2["0"] i3["0"] i4["2"] i5["-"] i6["0"]

      classDef imaginary fill:#526cfe09,color:#000,stroke-dasharray: 10 5;
      classDef position fill:#fff,color:#000,stroke-width:0px;
      class inf,sup imaginary
      class p0,p1,p2,p3,p4,p5,p6,p7 position

      classDef skip fill:#ffffff
      class s1,s5,i1,i5 skip


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

    The $Intervals_p^{-1}$ function for calculating _corresponding index_ based on the current _index_ and _interval_ is closly coupled
    with direction in selected _Binding_. For `-` _empty_ element it just put `-` instead of calculating the index

=== "and use binding⁻¹"

    ``` mermaid
    block-beta
      columns 6
      p1["1"] p2["2"] space p4["4"]         p5["5"]                p6["6"]
      s1["-"] s2["0"] s3["0"] s4["2"] s5["-"] s6["0"]
      e0["Iteratorₚ⁻¹(2) = 2"]:2 space:4
      space t1["Iteratorₚ⁻¹(4) = 2"]:3         space:2

      classDef imaginary fill:#526cfe09,color:#000,stroke-dasharray: 10 5;
      classDef position fill:#fff,color:#000,stroke-width:0px;
      class inf,sup imaginary
      class p0,p1,p2,p4,p5,p6,p7 position

      classDef skip fill:#ffffff
      class s1,s5,i1,i5 skip

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

      class s2,s4 c4
      class inf,t1,e0 c4a
      class pomn,p00,p01,p06,p07,p02n position
      class t1,t2,t5,e0,e1 position

    ```

    For each $Binding_p$  should exists $Binding_p^{-1}$ with an $Iterator_p^{-1}$ that allows
    to relabel elements of _interval chain_ with a unique number of the traversed path that it belongs to.

=== "to partial sequence"

    ``` mermaid
    block-beta
      columns 6
      p1["1"] p2["2"] p3["3"] p4["4"] p5["5"] p6["6"]
      i1["-"] i2["0"] i3["0"] i4["2"] i5["-"] i6["0"]
      s1["-"] s2["2"] s3["3"] s4["2"] s5["-"] s6["4"]

      classDef imaginary fill:#526cfe09,color:#000,stroke-dasharray: 10 5;
      classDef position fill:#fff,color:#000,stroke-width:0px;
      class inf,sup imaginary
      class p0,p1,p2,p3,p4,p5,p6,p7 position

      classDef skip fill:#ffffff
      class s1,s5,i1,i5 skip

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

      class s2,s4,i2,i4 c1
      class s3,i3 c5
      class s6,i6 c7
      class pomn,p00,p01,p06,p07,p02n position
      class t1,t2,t5,e0,e1 position

    ```

    The reconstructed partial sequence is not equal to the original one, but it preserves the same [partial order](../order/index.md) of elements
    and its _partial intervals chain_ would be equal to the _partial interval chain_ of the original sequence.

    ``` mermaid
    block-beta
      columns 6
      p1["1"] p2["2"] p3["3"] p4["4"] p5["5"] p6["6"]
      s1["-"] s2["2"] s3["3"] s4["2"] s5["-"] s6["4"]
      i1["-"] i2["C"] i3["T"] i4["C"] i5["-"] i6["G"]

      classDef imaginary fill:#526cfe09,color:#000,stroke-dasharray: 10 5;
      classDef position fill:#fff,color:#000,stroke-width:0px;
      class inf,sup imaginary
      class p0,p1,p2,p3,p4,p5,p6,p7 position

      classDef skip fill:#ffffff

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

      class s1,s5,i1,i5 skip
      class s2,s4,i2,i4 c1
      class s3,i3 c5
      class s6,i6 c7
      class pomn,p00,p01,p06,p07,p02n position
      class t1,t2,t5,e0,e1 position

    ```

---

$Bindings_p$, $Intervals_p$ and its inverse functions could be produced from functions defined for regular [_Bindings_, _Intervals chains_](../../order/intervals_chain/index.md#mathematical-definition) by adding condition that returns `-` for input `-` elements.

## Mathematical Definition

Let $X$ is [_Carrier set_](../../order/carrier_set.md#mathematical-definition)

Let $X_{-}$ is [_Partial Carrier set_](../carrier_set.md#mathematical-definition)

Let $-$ is [_Empty element_](../carrier_set.md#mathematical-definition)

Let $S$ is [_Sequence_](../../order/sequence.md#mathematical-definition) length of $l$ described as function $S : \{1,...,l\} \longrightarrow X$

Let $S_p$ is [_Partial Sequence_](../sequence/index.md#mathematical-definition) length of $l$ described as function $S_p : \{1,...,l\} \longrightarrow X_{-}$

Let $IC = <\Delta_1, \Delta_2, ..., \Delta_l> | \forall j \in \{1,...,l\} \exists \Delta_j \in \{1,...,l\}$ is [_Interval chain_](../../order/intervals_chain/index.md#define-intervals-chain)

Let $Binding = <Iterator, \bot>$ is [_Binding_](../../order/intervals_chain/index.md#define-bindings)

Let $R : \{1,...,l\} \longrightarrow \{1,...,l\} \cup \bot,$ is a corresponding [_references_](../../order/intervals_chain/index.md#define-bindings)

Then _Iterator_ defined as $Iterator \big\{  S \big\} \longrightarrow \big\{ R \big\},$

### Define Partial Bindings

Let $R_p : \{1,...,l\} \longrightarrow \{1,...,l\} \cup \bot \cup \{-\},$ is a corresponding _partial references_

Then

$$X \subset X_{-},$$

$$\{S\} \subset \{S_p\},$$

$$\{R\} \subset \{R_p\},$$

Define

$$Iterator_p : \big\{  S_p \big\} \longrightarrow \big\{ R_p \big\},$$

$$\{Iterator_p\} \supset \{Iterator\},$$

$$Iterator_p(S_p)(i) = \Bigg \{ \begin{array}{l} Intertor(S_p)(i) , &  S_p(i) \notin \{-\} \\ -, & S_p(i) \in \{-\} \end{array},$$

and

$$Binding_p = <Iterator_p, \bot>,$$

$$\{Binding_p\} \supset \{Binding\}$$

the same way

$$\exists Binding_p^{-1} = <Iterator_p^{-1}, \bot>,$$

$$\{Binding_p^{-1}\} \supset \{Binding^{-1}\},$$

where

$$Iterator_p^{-1} : \big\{  R_p \big\} \longrightarrow \big\{  \{1,...,l\} \longrightarrow \{1,...,m\} \cup \{-\} | m \leq l \big\},$$

$$\{Iterator_p^{-1}\} \supset \{Iterator^{-1}\},$$

$$Iterator_p^{-1}(R_p)(i) = \Bigg \{ \begin{array}{l} Intertor^{-1}(R_p)(i) , &  R_p(i) \notin \{-\} \\ -, & R_p(i) \in \{-\} \end{array}$$

The condition $Iterator_p(S_p) = Iterator_p(Iterator_p^{-1}(Iterator_p(S_p)))$ is valid.

### Define Partial Intervals Chain

as l-tuple of natural numbers and `-` empty elements

$$IC_p = <\Delta_1, \Delta_2, ..., \Delta_l> | \forall j \in \{1,...,l\} \exists \Delta_j \in \{1,...,l\} \cup \{-\},$$

Then

$$\{IC_p\} \supset \{IC\},$$

$$\exists \ Intervals_p : \big\{Binding_p\big\} \times \big\{S_p\}  \longrightarrow \big\{ IC_p \big\},$$

$$\{Intervals_p\} \supset \{Intervals\},$$

$$Intervals_p(b_p, S_p)(i) = \Bigg \{ \begin{array}{l} Intervals(b_p, S_p)(i) , &  S_p(i) \notin \{-\} \\ -, & S_p(i) \in \{-\} \end{array},$$

$$\exists \ Intervals_p^{-1} : \big\{Binding_p^{-1}\big\} \times \big\{ IC_p \big\}  \longrightarrow \big\{ \{1,...,l\} \longrightarrow \{1,...,m\} \cup \{-\} | m \leq l \big\},$$

$$\{Intervals_p^{-1}\} \supset \{Intervals^{-1}\},$$

$$Intervals_p^{-1}(b_p^{-1}, IC_p)(i) = \Bigg \{ \begin{array}{l} Intervals^{-1}(b_p^{-1}, IC_p)(i) , &  IC_p(i) \notin \{-\} \\ -, & IC_p(i) \in \{-\} \end{array},$$

The condition would be true

$$Intervals_p(b_p, S_p) = Intervals_p(b_p, Intervals_p^{-1}(b_p^{-1}, Intervals_p(b_p, S_p)))$$

Let $Follow$ is the [_follow function of interval chain_](../../order/intervals_chain/index.md#define-intervals-chain) described as function $Follow : \big\{Binding\big\} \times \big\{ IC \big\}  \longrightarrow \big\{ R \big\},$

$$\exists \ Follow_p : \big\{Binding_p\big\} \times \big\{ IC_p \big\}  \longrightarrow \big\{ R_p \big\},$$

$$\{Binding\} \subset \{Binding_p\},$$

$$\{IC\} \subset \{IC_p\},$$

$$\{R\} \subset \{R_p\},$$

then

$$\{Follow_p\} \supset \{Follow\}.$$

$$Follow_p(b_p, IC_p)(i) = \Bigg \{ \begin{array}{l} Follow(b_p, IC_p)(i) , &  IC_p(i) \notin \{-\} \\ -, & IC_p(i) \in \{-\} \end{array},$$

The condition would be true

$$f = Follow_p(b_p, IC_p),$$

$$f(i) <> f(j) \lor f(i) \in \bot | \forall i != j \land IC_p(i) \notin \{-\}.$$

Let $Trace$ is the [_trace function of interval chain_](../../order/intervals_chain/index.md#define-intervals-chain) described as function $Trace : \big\{Binding\big\} \times \big\{ IC \big\} \longrightarrow \big\{ R \big\},$

$$\exists \ Trace_p : \big\{Binding_p\big\} \times \big\{ IC_p \big\} \longrightarrow \big\{ R_p \big\},$$

$$\{Binding\} \subset \{Binding_p\},$$

$$\{IC\} \subset \{IC_p\},$$

$$\{R\} \subset \{R_p\},$$

then

$$\{Trace_p\} \supset \{Trace\}.$$

$$Trace_p(b_p, IC_p)(i) = \Bigg \{ \begin{array}{l} Trace_p(b_p, IC_p)(i) , &  IC_p(i) \notin \{-\} \\ -, & IC_p(i) \in \{-\} \end{array}.$$

The condition would be true

$$Trace_p(IC_p)(i) \in \bot | \forall i \in \{1,...,n\} \land IC_p(i) \notin \{-\}$$

Where:

- $l := |IC_p|$ is called _length_ of the _partial intervals chained_, $l \in N$
- $n := |\{ IC_p(i) | IC_p(i) \ne - \}|$ is _non-empty elements count_, $n \in N$
- $\Delta_i$​ is called the $i$-th _element_ (or interval) of the _partial intervals chained_
