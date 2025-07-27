# Partials and congenerics

_Partial sequence_ is a sequence with skips (empty positions, spaces). FOA uses the special symbol `-` as _empty_ element.
_Partial sequence_ where all _non-empty_ elements are equals _Congeneric sequence_.

=== "Sequence"

    ``` mermaid
    block-beta
    columns 36
    s1["I"] s2["N"] s3["T"] s4["E"] s5["L"] s6["L"] s7["I"] s8["G"] s9["E"] s10["N"]
    s11["C"] s12["E"] s13[" "] s14["I"] s15["S"] s16[" "] s17["T"] s18["H"] s19["E"] s20[" "]
    s21["A"] s22["B"] s23["I"] s24["L"] s25["I"] s26["T"] s27["Y"] s28[" "] s29["T"] s30["O"]
    s31[" "] s32["A"] s33["D"] s34["A"] s35["P"] s36["T"]

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

    ```

=== "Partial"

    ``` mermaid
    block-beta
    columns 36
    s1["I"] s2["N"] s3["T"] s4["E"] s5["L"] s6["L"] s7["I"] s8["G"] s9["E"] s10["N"]
    s11["C"] s12["E"] s13[" "] s14["-"] s15["-"] s16[" "] s17["T"] s18["-"] s19["-"] s20[" "]
    s21["-"] s22["B"] s23["-"] s24["L"] s25["-"] s26["T"] s27["-"] s28["-"] s29["T"] s30["-"]
    s31["-"] s32["-"] s33["D"] s34["-"] s35["P"] s36["T"]

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
    ```

=== "Congeneric"

    ``` mermaid
    block-beta
    columns 36
    s1["-"] s2["-"] s3["T"] s4["-"] s5["-"] s6["-"] s7["-"] s8["-"] s9["-"] s10["-"]
    s11["-"] s12["-"] s13["-"] s14["-"] s15["-"] s16["-"] s17["T"] s18["-"] s19["-"] s20["-"]
    s21["-"] s22["-"] s23["-"] s24["-"] s25["-"] s26["T"] s27["-"] s28["-"] s29["T"] s30["-"]
    s31["-"] s32["-"] s33["-"] s34["-"] s35["-"] s36["T"]

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

    class s1,s2,s4,s5,s6,s7,s8,s9,s10 skip
    class s11,s12,s13,s14,s15,s16,s18,s19,s20 skip
    class s21,s22,s23,s24,s25,s27,s28,s30 skip
    class s31,s32,s33,s34,s35 skip
    ```

Every operation and statement described in [_Order and its measures_](../order/index.md) that can be applied to _Sequence_ are also valid for Partial sequence, keeping in mind that only non-empty elements are involved.
Read the following documentation to clarify the differences that appear for  Partial [_Sequence_](./sequence/index.md), [_Order_](./order/index.md), and [_Intervals Chain_](./intervals_chain/index.md).
