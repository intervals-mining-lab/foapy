# Bounded Intervals Chain

A _bounded intervals chain_ is an [_intervals chain_](index.md) produced with _Bounded Binding_.
_Bounded Binding_ treats a sequence as a finite and uses $0$ and $n+1$ positions (depedns of _Iterator_ direction)
as _corresponding position_ anytime there is no `next` matching element.
The approach simplifies implementation functions and enables obtaining _binding direction_ based on a given _bounded intervals chain_ due to its specific properties.
This comes with a cost of the intervals' consistency that depends on _binding direction_ and leads to different measure values.
_Bounded Binding_ identifies _Start_ and _End_ directions.


=== "$Start$ binding"

    ``` mermaid
    block-beta
      columns 8
      p0["0"]        p1["1"] space:3         p5["5"]                p6["n"] space
      inf["⊥"] s1["A"] s2["C"] s3["T"] s4["C"] s5["A"] s6["G"] space
      e0["0 = Iterator(1)"]:2 space:6
      space      t1["1 = Iterator(5)"]:5         space:2

      classDef imaginary fill:#526cfe09,color:#000,stroke-dasharray: 10 5;
      classDef position fill:#fff,color:#000,stroke-width:0px;
      class inf,sup imaginary
      class p0,p1,p5,p6,p7 position

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

      class s1,s5 c4
      class inf,t1,e0 c4a
      class pomn,p00,p01,p06,p07,p02n position
      class t1,t2,t5,e0,e1 position

    ```

=== "$End$ binding"

    ``` mermaid
    block-beta
      columns 8
      space        p1["1"] space:3         p5["5"]                p6["n"] p7["n + 1"]
      space s1["A"] s2["C"] s3["T"] s4["C"] s5["A"] s6["G"] sup["⊥"]
      space      t1["Iterator(1) = 5"]:5         space:2
      space:5 e0["Iterator(5) = n+1"]:3

      classDef imaginary fill:#526cfe09,color:#000,stroke-dasharray: 10 5;
      classDef position fill:#fff,color:#000,stroke-width:0px;
      class inf,sup imaginary
      class p0,p1,p5,p6,p7 position

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

      class s1,s5 c4
      class sup,t1,e0 c4a
      class pomn,p00,p01,p06,p07,p02n position
      class t1,t2,t5,e0,e1 position

    ```



## Mathematical Definition

Let $X$ is [_Carrier set_](../carrier_set.md#Mathematical Definition)

Let $S$ is [_Sequence_](../sequence.md#Mathematical Definition)  length of $n$ described as function $S : \{1,...,n\} \longrightarrow X$

Let $Binding$ is [Binding](./index.md#define-bindings)

### Define Bindings

=== "$Start$ binding"
    Define a set of terminal values - $\bot = \{0\}$

    Let $R : \{1,...,n\} \longrightarrow \{1,...,n\} \cup \bot,$ is a corresponding _references_

    Define

    $$Iterator : \big\{ S \big\} \longrightarrow \big\{ R \big\},$$

    $$Iterator(S)(i) = \Bigg\{\begin{array}{l} max \big\{j \in \{1,...,i\}\big|S(j) = S(i) \land j \ne i \big\} & if \ exists \\ 0 & otherwise  \end{array}$$

    $$Start = <Iterator, \bot> \in \{Binding\}$$

    $$\exists Start^{-1} = <Iterator^{-1}, \bot>  \in \{Binding^{-1}\},$$

    $$Iterator^{-1} : \big\{  R \big\} \longrightarrow \big\{  \{1,...,n\} \longrightarrow \{1,...,m\} | m \leq n \big\}$$

    $$Iterator^{-1}(R)(i) = \Bigg\{\begin{array}{l} \Big|<j \in \{1,...i\} | R(j) \in \bot >\Big|, & \ R(i) \in \bot \\ Iterator^{-1}(R, R(i)), &  R(i) \in \{1,...,n\}   \end{array}$$

    $$Iterator(S) = Iterator(Iterator^{-1}(Iterator(S)))$$


=== "$End$ binding"
    Define a set of terminal values - $\bot = \{n+1\}$

    Let $R : \{1,...,n\} \longrightarrow \{1,...,n\} \cup \bot,$ is a corresponding _references_

    Define

    $$Iterator : \big\{ S \big\} \longrightarrow \big\{ R \big\},$$

    $$Iterator(S)(i) = \Bigg\{\begin{array}{l} min \big\{j \in \{i,...,n\}\big|S(j) = S(i) \land j \ne i \big\} & if \ exists \\ n+1 & otherwise  \end{array}$$

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

    $$IC(1) = 1$$

    $$IC(i) \le i | \forall i \in \{1,...,n\}$$

    $$Follow(IC)(i) <> Follow(IC)(j) \lor Follow(IC)(i) \in \bot | \forall i != j$$

    $$Trace(IC)(i) = 0 | \forall i \in \{1,...,n\}$$

=== "$End$ binding"

    $$IC(n) = 1$$

    $$IC(i) \le n - i | \forall i \in \{1,...,n\}$$

    $$Follow(IC)(i) <> Follow(IC)(j) \lor Follow(IC)(i) \in \bot | \forall i != j$$

    $$Trace(IC)(i) = n + 1 | \forall i \in \{1,...,n\}$$


---

Let $B = \{Start, End\} \subset \{Binding\}$ is set of [_Bounded Binding_](./binding.md#Mathematical Definition)
