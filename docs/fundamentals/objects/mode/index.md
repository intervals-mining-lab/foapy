# Mode

The _mode_ determines the method for computing intervals for the first or last appearances of the element.
There is uncertainty about how to count the interval for the first appearance with $start$ binding and
for the last appearance with $end$ binding, as there is no previous or following element appearance in the corresponding cases.

This interval can be skipped or counted to some `imaginary` appearance of the element.

The skipping option leads to cons that make reverse operation impossible in the general case -
count of intervals less than the count of elements in the initial sequence,
and/or intervals n-tuple contains `empty` elements. That's why the _mode_ does not have any value
corresponding to any kind of skip first/last interval.
<!-- TODO: Add lossy definition and reference -->
You can use `lossy` function defined in [Interval Order to Interval Tuple](./intervals_distribution.md) section to exclude the first/last interval that would be equivalent to the skipping approach.

The _mode_ defines values that assume different ways of `imaginary` elements - $boundary$ and $cycle$.
The `imaginary` elements can be used as  `previous` or `following` reference for any element of the sequence,
but do not produce any interval for their own. However, you can use `redundant` function defined in
<!-- TODO: Add redundant definition and reference -->
[Interval Order to Interval Tuple](./intervals_distribution.md) section to count intervals produced for `imaginary` elements.

## Boundary

The $boundary$ mode extends the sequence with `imaginary` elements - `Infimum` ($Inf$) and `Supremum` ($Sup$ ),
which are equal to any element of the sequence. `Infimum` element placed on $0$ position and `Supremum` on $n+1$ position of the sequence.

=== "$Start$ binding"

    ``` mermaid
    block-beta
      columns 8
      p0["0"]        p1["1"] space:4                         p6["n"] p7["n + 1"]
      inf["⊥"] s1["A"] s2["C"] s3["T"] s4["C"] s5["A"] s6["G"] sup["⊥"]
      infa["⊥"] ia1["1"]:1 space:6
      infc["⊥"] ic1["2"]:2 space:5
      inft["⊥"] it1["3"]:3 space:4
      infg["⊥"] ig1["6"]:6 space:1

      classDef imaginary fill:#526cfe09,color:#000,stroke-dasharray: 10 5;
      classDef position fill:#fff,color:#000,stroke-width:0px;
      class inf,sup imaginary
      class p0,p1,p6,p7 position

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
      class infa c2a
      class s2,ic1 c4
      class infc c4a
      class s3,it1 c6
      class inft c6a
      class s6,ig1 c14
      class infg c14a
      class p1,p2,p3,p4,p5,p6,p7,p8,p9,f1,f2,f3,f4,f5,f6,f7,f8,f9 imaginary
      class pomn,p00,p01,p06,p07,p02n position

    ```

=== "$End$ binding"

    ``` mermaid
    block-beta
      columns 8
      p0["0"]        p1["1"] space:4                         p6["n"] p7["n + 1"]
      inf["Infimum"] s1["A"] s2["C"] s3["T"] s4["C"] s5["A"] s6["G"] sup["Supremum"]
      space:5 ia1["2"]:2 supa["Supremum"]
      space:4 ic1["3"]:3 supc["Supremum"]
      space:3 it1["4"]:4 supt["Supremum"]
      space:6 ig1["1"]:1 supg["Supremum"]

      classDef imaginary fill:#526cfe09,color:#000,stroke-dasharray: 10 5;
      classDef position fill:#fff,color:#000,stroke-width:0px;
      class inf,sup imaginary
      class p0,p1,p6,p7 position

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
      class supa c2a
      class s4,ic1 c4
      class supc c4a
      class s3,it1 c6
      class supt c6a
      class s6,ig1 c14
      class supg c14a
      class p1,p2,p3,p4,p5,p6,p7,p8,p9,f1,f2,f3,f4,f5,f6,f7,f8,f9 imaginary
      class pomn,p00,p01,p06,p07,p02n position
    ```


## Cycle

In the $cycle$ mode, the sequence is extended by copying itself as an `imaginary` prefix/suffix to mock a cycled sequence (also known as a periodic sequence or an orbit). The first/last interval counts to the previous/following element in `imaginary` prefix/suffix.


=== "$Start$ binding"

    ``` mermaid
    block-beta
      columns 18
      pomn["-n"]    space:4  p00["0"]    p01["1"] space:4                                     p06["n"] p07["n + 1"]  space:4 p02n["n + n"]
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
      pomn["-n"]    space:4  p00["0"]    p01["1"] space:4                                     p06["n"] p07["n + 1"]  space:4 p02n["n + n"]
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

The $cycle$ mode is inspired and aligned with the idea of representativeness heuristic, which is fundamental in probability and statistics, and the Necklace problems in combinatorics.

At the same time, the $boundary$ mode looks like related to tree structures and graph theory.

## Mathematical Definition

Let $X$ is [_Carrier set_](./carrier_set.md#Mathematical Definition)

Let $S$ is [_Sequence_](./sequence.md#Mathematical Definition)  length of $n$ described as function $S : \{1,...,n\} \longrightarrow X$

Let $\bot \notin X$ is a special _sentinel_ value.

Define $X_\bot = X \cup \{ \bot \}$ set

$\forall S \ \exists \ S_{\bot} : J \longrightarrow X_{\bot} \Big| \{1,...,n\} \subset J$

Define $Mode : S \longrightarrow S_{\bot}$

$\forall S \exists S_{boundary} : \{0,...,n+1\} \longrightarrow X_\bot$

Define $boundary : S \longrightarrow S_{boundary}, boundary(s)(i) = \Biggl\{ \begin{array}{l} Inf, i=0 \\ s(i),  1 \le i \le n \\ Sup, i = n+1\end{array}$


$\forall S \exists S_{cycle} : Z \longrightarrow X_\bot$


<!-- ```python
low = 0
high = 6

def index(x):
  return x - (high - low + 1) * ((x - low) // (high - low + 1))
``` -->


Define $cycle : S \longrightarrow S_{cycle}, cycle(s)(i) = s\big( i - n \times \lfloor ( i - 1) \div n \rfloor \big) \Big| n = |s|$

Define _mode_ $M = \{ boundary, cycle \}$
