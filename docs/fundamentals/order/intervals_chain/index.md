# Intervals Chain

An _intervals chain_ is an n-tuple of natural numbers that represents the distance between equal elements in a sequence,
if and only if there is an operation that takes as an input _current_ $(index, interval)$ and returns the next _index_.
The operation makes the intervals chained to each other, which is a required condition for the existence reverse function
that restores by _intervals chain_ a sequence with the same with the original sequence [order](../order.md).

The idea of _intervals chain_ is easy to explain by a concrete example:


=== "From a sequence"

    ``` mermaid
    block-beta
        columns 8
        space        p1["1"] space:3         p5["5"]                p6["n"] space
        space s1["A"] s2["C"] s3["T"] s4["C"] s5["A"] s6["G"] space

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
    ```

    Let there be a sequence length of $n=6$ (indexed from 1 to n=6)

=== "with a binding"

    ``` mermaid
    block-beta
      columns 7
      p0["0"]        p1["1"] space:3         p5["5"]                p6["6"]
      inf["⊥"] s1["A"] s2["C"] s3["T"] s4["C"] s5["A"] s6["G"]
      e0["0 = Iterator(1)"]:2 space:5
      space      t1["1 = Iterator(5)"]:5         space

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

    Define _Binding_ as a pair of an _Iterator_ function, that seeks a corresponding referenced element, and
    set of _terminate states_, to determine the interval when there is no matching element in the sequence.

    In the example, _Iterator_ seeks a position of a previous equivalent element as a matching reference.
    If there is no such element, it returns $0$. That means _terminate states_ set is $\bot = {0}$.
    This particular method is called - _Start binding_.

=== "get correspoding indexes"

    ``` mermaid
    block-beta
      columns 7
      p0["0"]  p1["1"] p2["2"] p3["3"] p4["4"] p5["5"] p6["6"]
      inf["⊥"] s1["A"] s2["C"] s3["T"] s4["C"] s5["A"] s6["G"]
      space i1["0"] i2["0"] i3["0"] i4["2"] i5["1"] i6["0"]

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

      class s1,s5,i1,i5 c4
      class s2,s4,i2,i4 c1
      class s3,i3 c5
      class s6,i6 c7
      class pomn,p00,p01,p06,p07,p02n position
      class t1,t2,t5,e0,e1 position

    ```

    With _Binding_ we can get a sequence of corresponding indexes.
    For all first appearances of the elements it would be $0$,
    and for `C` at position `4` corresponding index would be `2`, for `A` at position `5` - `1`.

=== "and calculate intervals chain"

    ``` mermaid
    block-beta
      columns 7
      p0["0"]  p1["1"] p2["2"] p3["3"] p4["4"] p5["5"] p6["6"]
      space i1["0"] i2["0"] i3["0"] i4["2"] i5["1"] i6["0"]
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

      class s1,s5,i1,i5 c4
      class s2,s4,i2,i4 c1
      class s3,i3 c5
      class s6,i6 c7
      class pomn,p00,p01,p06,p07,p02n position
      class t1,t2,t5,e0,e1 position

    ```

    Calculated interval by $Intervals$ function is the [absolute value](https://en.wikipedia.org/wiki/Absolute_value)
    of difference the _corresponding index_ and the _index_. For example, for index `5` interval would be $|5-1|=4$


---

There should exists an inverse function that restores by _interval chain_ a sequence with the original [order](../order.md)

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

=== "calculate correspoding indexes"

    ``` mermaid
    block-beta
      columns 7
      p0["0"]  p1["1"] p2["2"] p3["3"] p4["4"] p5["5"] p6["6"]
      space s1["1"] s2["2"] s3["3"] s4["2"] s5["4"] s6["6"]
      space i1["0"] i2["0"] i3["0"] i4["2"] i5["1"] i6["0"]

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

    The $Intervals^{-1}$ function for calculating _corresponding index_ based on the current _index_ and _interval_ is closly coupled
    with direction in selected _Binding_. The function has to be defined for each particular _Binding_ method.
    Whether it is possible to obtain direction of _Binding_ given an _interval chain_, and whether there are two equivalent _interval chains_
    obtained by different _Binding_ methods, are open questions that need to be investigated.

    In the example $Intervals^{-1}(IC)(i) = IC(i)-i$

=== "and use binding⁻¹"

    ``` mermaid
    block-beta
      columns 6
      p1["1"] space:3         p5["5"]                p6["6"]
      s1["0"] s2["0"] s3["0"] s4["2"] s5["1"] s6["0"]
      e0["Iterator⁻¹(1) = 1"] space:5
      t1["Iterator⁻¹(5) = 1"]:5         space

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

    For each _Binding_  should exists $Binding^{-1}$ with an $Iterator^{-1}$ that allows
    to relabel elements of _interval chain_ with a unique number of the traversed path that it belongs to.

    $$Iterator^{-1}(P)(i) = \Bigg\{\begin{array}{l} \big|<j \in \{1,...i\} | P(j)=0 >\big| & if \ P(i)=0 \\ Iterator^{-1}(P, P(i)) & otherwise   \end{array}$$

=== "to reconstruct sequence"

    ``` mermaid
    block-beta
      columns 6
      p1["1"] p2["2"] p3["3"] p4["4"] p5["5"] p6["6"]
      i1["0"] i2["0"] i3["0"] i4["2"] i5["1"] i6["0"]
      s1["1"] s2["2"] s3["3"] s4["2"] s5["1"] s6["4"]

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

      class s1,s5,i1,i5 c4
      class s2,s4,i2,i4 c1
      class s3,i3 c5
      class s6,i6 c7
      class pomn,p00,p01,p06,p07,p02n position
      class t1,t2,t5,e0,e1 position

    ```

    The reconstructed sequence is not equal to the original one, but it preserves the same [order](../order.md) of elements
    and its _intervals chain_ would be equal to the _interval chain_ of the original sequence.

    ``` mermaid
    block-beta
      columns 6
      p1["1"] p2["2"] p3["3"] p4["4"] p5["5"] p6["6"]
      s1["1"] s2["2"] s3["3"] s4["2"] s5["1"] s6["4"]
      i1["A"] i2["C"] i3["T"] i4["C"] i5["A"] i6["G"]

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

      class s1,s5,i1,i5 c4
      class s2,s4,i2,i4 c1
      class s3,i3 c5
      class s6,i6 c7
      class pomn,p00,p01,p06,p07,p02n position
      class t1,t2,t5,e0,e1 position

    ```

---

Formal order analysis identifies two groups of _Bindings_:

- [Bounded](./bounded.md) - consider a sequence to be finite and bounded. Operates with the minimum data required to determine _intervals chains_ and _sequence_.
- [Cycled](./cycled.md) - treats a sequence as a subsequence representing an infinite sequence. Connects FOA with the fundamental ideas underlying statistics and probability theory.

## Mathematical Definition

Let $X$ is [_Carrier set_](../carrier_set.md#mathematical-definition)

Let $S$ is [_Sequence_](../sequence.md#mathematical-definition)  length of $n$ described as function $S : \{1,...,n\} \longrightarrow X$

### Define Bindings

Define a set of terminal values - $\bot \subset N \setminus \{1,..,n\}$

Let $R : \{1,...,n\} \longrightarrow \{1,...,n\} \cup \bot,$ is a corresponding _references_

Define

$$Iterator : \big\{  S \big\} \longrightarrow \big\{ R \big\},$$

$$Binding = <Iterator, \bot>$$

$$\exists Binding^{-1} = <Iterator^{-1}, \bot>,$$

$$Iterator^{-1} : \big\{  R \big\} \longrightarrow \big\{  \{1,...,n\} \longrightarrow \{1,...,m\} | m \leq n \big\}$$

$$Iterator(S) = Iterator(Iterator^{-1}(Iterator(S)))$$

### Define Intervals Chain

as n-tuple of natural numbers

$$IC = <ic_1, ic_2, ..., ic_n> | \forall j \in \{1,...,n\} \exists ic_j \in \{1,...,n\},$$

if and only if

$$\exists \ Intervals : \big\{Binding\big\} \times \big\{S\}  \longrightarrow \big\{ IC \big\},$$

$$Intervals(<iterator, \bot>, S)(i) = | i - iterator(S)(i)|,$$

$$\exists \ Intervals^{-1} : \big\{Binding^{-1}\big\} \times \big\{ IC \big\}  \longrightarrow \big\{ \{1,...,n\} \longrightarrow \{1,...,m\} | m \leq n \big\},$$

$$Intervals(b, S) = Intervals(b, Intervals^{-1}(b^{-1}, Intervals(b, S)))$$

$$\exists \ Follow : \big\{Binding\big\} \times \big\{ IC \big\}  \longrightarrow \big\{ R \big\},$$

$$Follow(b, IC)(i) <> Follow(b, IC)(j) \lor Follow(b, IC)(i) \in \bot | \forall i != j $$

$$\exists \ Trace : \big\{Binding\big\} \times \big\{ IC \big\} \longrightarrow \big\{ R \big\}$$

$$Trace(<iterator, \bot>, IC)(i) = \Bigg\{\begin{array}{l} i, & \ i \in \bot \\ Trace\big(Follow(IC, i)\big) &  i \in \{1,...,n\} \end{array}$$

$$Trace(IC)(i) \in \bot | \forall i \in \{1,...,n\}$$

Where:

- $n := |IC|$ is called _length_ of the _intervals chained_, $n \in N$
- $ic_i$​ is called the $i$-th _element_ (or interval) of the _intervals chained_
