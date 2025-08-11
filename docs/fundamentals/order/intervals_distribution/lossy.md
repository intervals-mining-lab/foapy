# Lossy Intervals Distribution

A _lossy intervals distribution_ is an aggregation of two _interval distributions_ having only intervals existing in both.

_Lossy Interval Distribution_ is an intersection of two distributions.

Mostly, this distribution is used to solve measure dependence on _Binding direction_ with [_Bounded binding_](../intervals_chain/bounded.md).
In that case, this would be equivalent to excluding the first/last intervals from the distribution.

For example, there are 2 distributions for _Bounded Binding_ - one uses _Start binding direction_ and the other  _End binding direction_.

``` mermaid
block-beta
    columns 8
    p0["0"]        p1["1"] space:3         p5["5"]                p6["6"] p7["7"]
    inf["⊥"] s1["A"] s2["C"] s3["T"] s4["C"] s5["A"] s6["G"] sup["⊥"]
    space es0["Start(1) = 1"]:1 ts1["Start(5)=4"]:5 space
    space      te1["End(1) = 4"]:4 ee0["End(5) = 2"]:2 space

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
    class inf,sup,te1,ee0,ts1,es0 c4a
    class pomn,p00,p01,p06,p07,p02n position
```

_Lossy Interval Distribution_ will contain only interval `4` as it exists in both distributions.




## Mathematical Definition

Let $ID$ is [_Intervals distribution_](../intervals_distribution/index.md#mathematical-definition)

Define _Lossy Interval Distribution_

$$LID: \{ID\} \times \{ID\} \longrightarrow \{ID\}$$

$$LID(ID_1, ID_2)(i) = min \{ID_1(i), ID_2(i) \}$$
