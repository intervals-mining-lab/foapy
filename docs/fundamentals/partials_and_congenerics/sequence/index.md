# Partial Sequence

_Partial sequence_ is a [_sequence_](../../order/sequence.md) where some elements are skipped.
The concept can be treated as equivalent to the _masked sequence_ that is used in bioinformatics and data science.
In FOA `-` symbol used as `empty` element.

``` mermaid
block-beta
columns 29

i1["1"] i2["2"] i3["3"] i4["4"] i5["5"] i6["6"] i7["7"] i8["8"] i9["9"] i10["10"] i11["11"] i12["12"]
i13["13"] i14["14"] i15["15"] i16["16"] i17["17"] i18["18"] i19["19"] i20["20"]
i21["21"] i22["12"] i23["23"] i24["24"] i25["25"] i26["26"] i27["27"]
i28["28"] i29["29"]

s1["I"] s2["N"] s3["T"] s4["E"] s5["L"] s6["L"] s7["I"] s8["G"] s9["E"] s10["N"]
s11["C"] s12["E"] s13[" "] s14["-"] s15["-"] s16[" "] s17["T"] s18["-"] s19["-"] s20[" "]
s21["-"] s22["B"] s23["-"] s24["L"] s25["-"] s26["T"] s27["-"] s28["-"] s29["T"]

classDef c1 fill:#ff7f0e,color:#fff;
classDef c2 fill:#ffbb78,color:#000;
classDef c3 fill:#2ca02c,color:#fff;
classDef c4 fill:#98df8a,color:#000;
classDef c5 fill:#d62728,color:#fff;
classDef c6 fill:#ff9896,color:#000;
classDef c7 fill:#9467bd,color:#fff;
classDef c8 fill:#c5b0d5,color:#000;
classDef c9 fill:#8c564b,color:#fff;
classDef c10 fill:#c49c94,color:#000;
classDef c11 fill:#e377c2,color:#fff;
classDef c12 fill:#f7b6d2,color:#000;
classDef c13 fill:#bcbd22,color:#fff;
classDef c14 fill:#dbdb8d,color:#000;
classDef c15 fill:#17becf,color:#fff;
classDef c16 fill:#9edae5,color:#000;

classDef skip fill:#ffffff
classDef index fill:#ffffff,stroke-width:0px

class s14,s15,s18,s19,s21,s23,s25,s27,s28 skip

class i1,i2,i3,i4,i5,i6,i7,i8,i9,i10 index
class i11,i12,i13,i14,i15,i16,i17,i18,i19,i20 index
class i21,i22,i23,i24,i25,i26,i27,i28,i29 index
```

## Mathematical Definition

Let $X_{-}$ is [_Partial Carrier set_](../carrier_set.md#mathematical-definition)

A _Partial sequence_ $S_{p}$ is a l-tuple defined as

$$S_{p} = <s_1, s_2, ..., s_l>,$$

$$\forall i \in \{1, ..., l\} \exists s_i \in X_{-}$$

where:

- $s_i$​ is called the $i$-th _element_ (or coordinate) of the sequence.
- $l := |S_p|$ is _length_, $l \in N$
- $n := |\{ S_p(i) | S_p(i) \ne - \}|$ is _non-empty elements count_, $n \in N$

The _sequence_ $S$ can be also defined as a function

$$S_p : \{1, ..., l\} \longrightarrow X_{-},$$

$$S_p(i)=s_i | i \in \{1, ..., l\}$$


### Compatibility

Two _Partial Sequences_ are called compatible if there are no _non-empty_ elements in the same position in both sequences.

=== "Сompatible"

    ``` mermaid
    block-beta
    columns 36
    s1["I"] s2["N"] s3["T"] s4["E"] s5["L"] s6["L"] s7["I"] s8["G"] s9["E"] s10["N"]
    s11["C"] s12["E"] s13[" "] s14["-"] s15["-"] s16[" "] s17["T"] s18["-"] s19["-"] s20[" "]
    s21["-"] s22["B"] s23["-"] s24["L"] s25["-"] s26["T"] s27["-"] s28["-"] s29["T"] s30["-"]
    s31["-"] s32["-"] s33["D"] s34["-"] s35["P"] s36["T"]

    q1["-"] q2["-"] q3["-"] q4["-"] q5["-"] q6["-"] q7["-"] q8["-"] q9["-"] q10["-"]
    q11["-"] q12["-"] q13["-"] q14["I"] q15["S"] q16["-"] q17["-"] q18["H"] q19["E"] q20["-"]
    q21["A"] q22["-"] q23["I"] q24["-"] q25["I"] q26["-"] q27["I"] q28[" "] q29["-"] q30["O"]
    q31[" "] q32["A"] q33["-"] q34["A"] q35["-"] q36["-"]


    classDef c1 fill:#ff7f0e,color:#fff;
    classDef c2 fill:#ffbb78,color:#000;
    classDef c3 fill:#2ca02c,color:#fff;
    classDef c4 fill:#98df8a,color:#000;
    classDef c5 fill:#d62728,color:#fff;
    classDef c6 fill:#ff9896,color:#000;
    classDef c7 fill:#9467bd,color:#fff;
    classDef c8 fill:#c5b0d5,color:#000;
    classDef c9 fill:#8c564b,color:#fff;
    classDef c10 fill:#c49c94,color:#000;
    classDef c11 fill:#e377c2,color:#fff;
    classDef c12 fill:#f7b6d2,color:#000;
    classDef c13 fill:#bcbd22,color:#fff;
    classDef c14 fill:#dbdb8d,color:#000;
    classDef c15 fill:#17becf,color:#fff;
    classDef c16 fill:#9edae5,color:#000;

    classDef skip fill:#ffffff

    class s14,s15,s18,s19,s21,s23,s25,s27,s28,s30,s31,s32,s34 skip

    class q1,q2,q3,q4,q5,q6,q7,q8,q9,q10 skip
    class q11,q12,q13,q16,q17,q20 skip
    class q22,q24,q26,q29 skip
    class q33,q35,q36 skip

    ```

=== "Incompatible"

    ``` mermaid
    block-beta
    columns 36
    s1["I"] s2["N"] s3["T"] s4["E"] s5["L"] s6["L"] s7["I"] s8["G"] s9["E"] s10["N"]
    s11["C"] s12["E"] s13[" "] s14["-"] s15["-"] s16[" "] s17["T"] s18["-"] s19["-"] s20[" "]
    s21["-"] s22["B"] s23["-"] s24["L"] s25["-"] s26["T"] s27["-"] s28["-"] s29["T"] s30["-"]
    s31["-"] s32["-"] s33["D"] s34["-"] s35["P"] s36["T"]

    q1["I"] q2["-"] q3["-"] q4["-"] q5["-"] q6["-"] q7["I"] q8["-"] q9["-"] q10["-"]
    q11["-"] q12["-"] q13[" "] q14["I"] q15["S"] q16["-"] q17["-"] q18["H"] q19["E"] q20["-"]
    q21["A"] q22["-"] q23["I"] q24["-"] q25["I"] q26["-"] q27["I"] q28[" "] q29["-"] q30["O"]
    q31[" "] q32["A"] q33["-"] q34["A"] q35["-"] q36["-"]


    classDef c1 fill:#ff7f0e,color:#fff;
    classDef c2 fill:#ffbb78,color:#000;
    classDef c3 fill:#2ca02c,color:#fff;
    classDef c4 fill:#98df8a,color:#000;
    classDef c5 fill:#d62728,color:#fff;
    classDef c6 fill:#ff9896,color:#000;
    classDef c7 fill:#9467bd,color:#fff;
    classDef c8 fill:#c5b0d5,color:#000;
    classDef c9 fill:#8c564b,color:#fff;
    classDef c10 fill:#c49c94,color:#000;
    classDef c11 fill:#e377c2,color:#fff;
    classDef c12 fill:#f7b6d2,color:#000;
    classDef c13 fill:#bcbd22,color:#fff;
    classDef c14 fill:#dbdb8d,color:#000;
    classDef c15 fill:#17becf,color:#fff;
    classDef c16 fill:#9edae5,color:#000;

    classDef skip fill:#ffffff

    classDef conflict fill:#ff0000,color:#fff

    class s14,s15,s18,s19,s21,s23,s25,s27,s28,s30,s31,s32,s34 skip

    class q2,q3,q4,q5,q6,q8,q9,q10 skip
    class q11,q12,q13,q16,q17,q20 skip
    class q22,q24,q26,q29 skip
    class q33,q35,q36 skip

    class s1,q1,s7,q7 conflict
    ```


Let $S1_p$ and $S2_p$ are _Partial sequences_

Define


$$compatible(S1_p, S2_p) = \forall i \in \{1,...,l\}\ S1_p(i) \notin \{-\} \lor S2_p(i) \notin \{-\} $$
