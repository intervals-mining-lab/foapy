# Cycled Intervals Chain

A _cycled intervals chain_ is an [_intervals chain_](index.md) produced with _Cycled Binding_.
_Cycled Binding_ treats a sequence as a subsequence representing an infinite sequence.

The approach alignged with [Representativeness heuristic](https://en.wikipedia.org/wiki/Representativeness_heuristic) idea,
connects FOA with [Necklace](https://en.wikipedia.org/wiki/Necklace_(combinatorics)) problem and
makes intervals based measures indeferent to _binding direction_.

_Cycled Binding_ identifies _Start_ and _End_ directions.

_Cycled Binding_ extends the sequence by copying itself as a prefix and suffix.
This is enough to mock it as a cycled sequence (also known as a periodic sequence or an orbit) and
use the prefix and suffix to find the corresponding position for the element in edge cases.


=== "$Start$ binding"

    ``` mermaid
    block-beta
      columns 18
      pomn["-n+1"]    space:4  p00["0"]    p01["1"] space:4                                     p06["n"] p07["n + 1"]  space:4 p02n["n + n"]
      p1["A"] p2["C"] p3["T"] p4["C"] p5["A"] p6["G"] s1["A"] s2["C"] s3["T"] s4["C"] s5["A"] s6["G"] f1["A"] f2["C"] f3["T"] f4["C"] f5["A"] f6["G"]
      space:5 ia1["2"]:2 space:11
      space:4 ic1["4"]:4 space:10
      space:3 it1["6"]:6 space:9
      space:6 ig1["6"]:6 space:6

      classDef imaginary fill:#526cfe09,color:#000,stroke-dasharray: 10 5;
      classDef position fill:#fff,color:#000,stroke-width:0px;

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

      class s1,ia1 c2
      class p5 c2a
      class s2,ic1 c4
      class p4 c4a
      class s3,it1 c6
      class p3 c6a
      class s6,ig1 c14
      class p6 c14a
      class p1,p2,p3,p4,p5,p6,p7,p8,p9,f1,f2,f3,f4,f5,f6,f7,f8,f9 imaginary
      class pomn,p00,p01,p06,p07,p02n position

    ```

=== "$End$ binding"

    ``` mermaid
    block-beta
      columns 18
      pomn["-n+1"]    space:4  p00["0"]    p01["1"] space:4                                     p06["n"] p07["n + 1"]  space:4 p02n["n + n"]
      p1["A"] p2["C"] p3["T"] p4["C"] p5["A"] p6["G"] s1["A"] s2["C"] s3["T"] s4["C"] s5["A"] s6["G"] f1["A"] f2["C"] f3["T"] f4["C"] f5["A"] f6["G"]
      space:10 ia1["2"]:2 space:6
      space:9 ic1["4"]:4 space:5
      space:8 it1["6"]:6 space:5
      space:10 ig1["6"]:6 space:1

      classDef imaginary fill:#526cfe09,color:#000,stroke-dasharray: 10 5;
      classDef position fill:#fff,color:#000,stroke-width:0px;

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

      class s5,ia1 c2
      class f1 c2a
      class s4,ic1 c4
      class f2 c4a
      class s3,it1 c6
      class f3 c6a
      class s6,ig1 c14
      class f6 c14a
      class p1,p2,p3,p4,p5,p6,p7,p8,p9,f1,f2,f3,f4,f5,f6,f7,f8,f9 imaginary
      class pomn,p00,p01,p06,p07,p02n position

    ```

## Mathematical Definition

Let $X$ is [_Carrier set_](../carrier_set.md#mathematical-definition)

Let $S$ is [_Sequence_](../sequence.md#mathematical-definition)  length of $n$ described as function $S : \{1,...,n\} \longrightarrow X$

Let $Binding$ is [Binding](./index.md#define-bindings)

Let $S_{cycled} : \big\{ \{1,...,n\} \longrightarrow X \big\} \longrightarrow \big\{ Z \longrightarrow X \big\}$ is a cycled sequence

$$S_{cycled}(S)(i) = S\big( i - n \times \lfloor ( i - 1) \div n \rfloor \big)$$


### Define Bindings

=== "$Start$ binding"
    Define a set of terminal values - $\bot = \{-n+1,...,0\}$

    Let $R : \{1,...,n\} \longrightarrow \{1,...,n\} \cup \bot,$ is a corresponding _references_

    Define

    $$Iterator : \big\{ S \big\} \longrightarrow \big\{ R \big\},$$

    $$Iterator(S)(i) = max \big\{j \in \{-n+1,...,i\}\big|S_{cycled}(j) = S(i) \land j \ne i \big\} $$

    $$Start = <Iterator, \bot> \in \{Binding\}$$

    $$\exists Start^{-1} = <Iterator^{-1}, \bot>  \in \{Binding^{-1}\},$$

    $$Iterator^{-1} : \big\{  R \big\} \longrightarrow \big\{  \{1,...,n\} \longrightarrow \{1,...,m\} | m \leq n \big\}$$

    $$Iterator^{-1}(R)(i) = \Bigg\{\begin{array}{l} \Big|<j \in \{1,...i\} | R(j) \in \bot >\Big|, & \ R(i) \in \bot \\ Iterator^{-1}(R, R(i)), &  R(i) \in \{1,...,n\}   \end{array}$$

    $$Iterator(S) = Iterator(Iterator^{-1}(Iterator(S)))$$


=== "$End$ binding"
    Define a set of terminal values - $\bot = \{n+1,...,2n\}$

    Let $R : \{1,...,n\} \longrightarrow \{1,...,n\} \cup \bot,$ is a corresponding _references_

    Define

    $$Iterator : \big\{ S \big\} \longrightarrow \big\{ R \big\},$$

    $$Iterator(S)(i) = min \big\{j \in \{i,...,2n\}\big|S_{cycled}(j) = S(i) \land j \ne i \big\}$$

    $$End = <Iterator, \bot> \in \{Binding\}$$

    $$\exists End^{-1} = <Iterator^{-1}, \bot>  \in \{Binding^{-1}\},$$

    $$Iterator^{-1} : \big\{  R \big\} \longrightarrow \big\{  \{1,...,n\} \longrightarrow \{1,...,m\} | m \leq n \big\}$$

    $$Iterator^{-1}(R)(i) = \Bigg\{\begin{array}{l} \Big|<j \in \{i,...n\} | R(j) \in \bot >\Big|, & \ R(i) \in \bot \\ Iterator^{-1}(R, R(i)), &  R(i) \in \{1,...,n\} \end{array}$$

    $$Iterator(S) = Iterator(Iterator^{-1}(Iterator(S)))$$

---

### Define Intervals Chain

=== "$Start$ binding"

    Define

    $$IC = <ic_1, ic_2, ..., ic_n> | \forall j \in \{1,...,n\} \exists ic_j \in \{1,...,n\},$$

    $$\exists \ Intervals : \big\{S\}  \longrightarrow \big\{ IC \big\},$$

    $$Intervals(S)(i) = | i - Iterator(S)(i)|,$$

    $$\exists \ Follow : \big\{ IC \big\}  \longrightarrow \big\{ R \big\},$$

    $$Follow(IC)(i) = i - IC(i),$$

    $$\exists Intervals^{-1} : \big\{ IC \big\}  \longrightarrow \big\{ \{1,...,n\} \longrightarrow \{1,...,m\} | m \leq n \big\},$$

    $$Intervals^{-1}(IC)(i) = Iterator^{-1}(Follow(IC))(i),$$

    $$Intervals(S) = Intervals(Intervals^{-1}(Intervals(S)))$$

    $$\exists Trace : \big\{ IC \big\} \longrightarrow \big\{ R \big\}$$

    $$Trace(IC)(i) = \Bigg\{\begin{array}{l} i, & \ i \in \bot \\ Trace\big(IC\big)\big(Follow(IC, i)\big) &  i \in \{1,...,n\} \end{array}$$


    Where:

    - $n := |IC|$ is called _length_ of the _intervals chained_, $n \in N$
    - $ic_i$​ is called the $i$-th _element_ (or interval) of the _intervals chained_


=== "$End$ binding"

    Define

    $$IC = <ic_1, ic_2, ..., ic_n> | \forall j \in \{1,...,n\} \exists ic_j \in \{1,...,n\},$$

    $$\exists \ Intervals : \big\{S\}  \longrightarrow \big\{ IC \big\},$$

    $$Intervals(S)(i) = | i - Iterator(S)(i)|,$$

    $$\exists \ Follow : \big\{ IC \big\}  \longrightarrow \big\{ R \big\},$$

    $$Follow(IC)(i) = i + IC(i),$$

    $$\exists Intervals^{-1} : \big\{ IC \big\}  \longrightarrow \big\{ \{1,...,n\} \longrightarrow \{1,...,m\} | m \leq n \big\},$$

    $$Intervals^{-1}(IC)(i) = Iterator^{-1}(Follow(IC))(i),$$

    $$Intervals(S) = Intervals(Intervals^{-1}(Intervals(S)))$$

    $$\exists Trace : \big\{ IC \big\} \longrightarrow \big\{ R \big\}$$

    $$Trace(IC)(i) = \Bigg\{\begin{array}{l} i, & \ i \in \bot \\ Trace\big(IC\big)\big(Follow(IC, i)\big) &  i \in \{1,...,n\} \end{array}$$


    Where:

    - $n := |IC|$ is called _length_ of the _intervals chained_, $n \in N$
    - $ic_i$​ is called the $i$-th _element_ (or interval) of the _intervals chained_


---

#### Special properties

_Intervals chain_ $IC$ have been calculated with _Bounded binding_ have a special properties

=== "$Start$ binding"

    $$IC(i) \le n | \forall i \in \{1,...,n\}$$

    $$Follow(IC)(i) <> Follow(IC)(j) | \forall i != j$$

    $$j < 1 \land j = Trace(IC)(n + j) | \forall i \in \{1,...,n\} \exists j = Trace(IC)(i)$$

=== "$End$ binding"

    $$IC(i) \le n | \forall i \in \{1,...,n\}$$

    $$Follow(IC)(i) <> Follow(IC)(j) | \forall i != j$$

    $$j > n+1 \land j = Trace(IC)(j - n) | \forall i \in \{1,...,n\} \exists j = Trace(IC)(i)$$


---

Let $B = \{Start, End\} \subset \{Binding\}$ is set of _Cycled Binding_
