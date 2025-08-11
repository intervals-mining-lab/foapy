# Order and its measures

Formal Order Analysis identifies [Order](./order.md) as a sequence's property that could be extracted by replacing elements with their indexes in an [Alphabet](./alphabet.md).

A pair of Alphabet and Order determines a [Sequence](./sequence.md).

=== "Alphabet"

    ``` mermaid
    block-beta
    columns 36
    s1["I"] s2["N"] s3["T"] s4["E"] s5["L"] s6["L"] s7["I"] s8["G"] s9["E"] s10["N"]
    s11["C"] s12["E"] s13[" "] s14["I"] s15["S"] s16[" "] s17["T"] s18["H"] s19["E"] s20[" "]
    s21["A"] s22["B"] s23["I"] s24["L"] s25["I"] s26["T"] s27["Y"] s28[" "] s29["T"] s30["O"]
    s31[" "] s32["A"] s33["D"] s34["A"] s35["P"] s36["T"]

    space:36

    i1_1["1"] i2_1["2"] i3_1["3"] i4_1["4"] i5_1["5"] space:2 i6_1["6"] space:2 i7_1["7"] space
    i8_1["8"] space i9_1["9"] space:2 i10_1["10"] space:2
    i11_1["11"] i12_1["12"] space:4 i13_1["13"]
    space:2 i14_1["14"] space:2
    i15_1["15"] space i16_1["16"]

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

    class s1,i1_1 c1
    class s2,i2_1 c2
    class s3,i3_1 c3
    class s4,i4_1 c4
    class s5,i5_1 c5
    class s8,i6_1 c6
    class s11,i7_1 c7
    class s13,i8_1 c8
    class s15,i9_1 c9
    class s18,i10_1 c10
    class s21,i11_1 c11
    class s22,i12_1 c12
    class s27,i13_1 c13
    class s30,i14_1 c14
    class s33,i15_1 c15
    class s35,i16_1 c16

    s1 --> i1_1
    s2 --> i2_1
    s3 --> i3_1
    s4 --> i4_1
    s5 --> i5_1
    s8 --> i6_1
    s11 --> i7_1
    s13 --> i8_1
    s15 --> i9_1
    s18 --> i10_1
    s21 --> i11_1
    s22 --> i12_1
    s27 --> i13_1
    s30 --> i14_1
    s33 --> i15_1
    s35 --> i16_1

    i1_1  --> s1
    i2_1  --> s2
    i3_1  --> s3
    i4_1  --> s4
    i5_1  --> s5
    i6_1  --> s8
    i7_1  --> s11
    i8_1  --> s13
    i9_1  --> s15
    i10_1 --> s18
    i11_1 --> s21
    i12_1 --> s22
    i13_1 --> s27
    i14_1 --> s30
    i15_1 --> s33
    i16_1 --> s35

    ```

=== "Order"
    ``` mermaid
    block-beta
    columns 36
    s1["I"] s2["N"] s3["T"] s4["E"] s5["L"] s6["L"] s7["I"] s8["G"] s9["E"] s10["N"]
    s11["C"] s12["E"] s13[" "] s14["I"] s15["S"] s16[" "] s17["T"] s18["H"] s19["E"] s20[" "]
    s21["A"] s22["B"] s23["I"] s24["L"] s25["I"] s26["T"] s27["Y"] s28[" "] s29["T"] s30["O"]
    s31[" "] s32["A"] s33["D"] s34["A"] s35["P"] s36["T"]

    space:36

    i1_1["1"] i2_1["2"] i3_1["3"] i4_1["4"] i5_1["5"] i5_2["5"] i1_2["1"] i6_1["6"] i4_2["4"] i2_2["2"] i7_1["7"] i4_3["4"]
    i8_1["8"] i1_3["1"] i9_1["9"] i8_2["8"] i3_2["3"] i10_1["10"] i4_4["4"] i8_3["8"]
    i11_1["11"] i12_1["12"] i1_4["1"] i5_3["5"] i1_5["1"] i3_3["3"] i13_1["13"]
    i8_4["8"] i3_4["3"] i14_1["14"] i8_5["8"] i11_2["11"]
    i15_1["15"] i11_3["11"] i16_1["16"] i3_5["3"]

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

    class s1,s7,s14,s23,s25,i1_1,i1_2,i1_3,i1_4,i1_5 c1
    class s2,s10,i2_1,i2_2 c2
    class s3,s17,s26,s29,s36,i3_1,i3_2,i3_3,i3_4,i3_5 c3
    class s4,s9,s12,s19,i4_1,i4_2,i4_3,i4_4 c4
    class s5,s6,s24,i5_1,i5_2,i5_3 c5
    class s8,i6_1 c6
    class s11,i7_1 c7
    class s13,s16,s20,s28,s31,i8_1,i8_2,i8_3,i8_4,i8_5 c8
    class s15,i9_1 c9
    class s18,i10_1 c10
    class s21,s32,s34,i11_1,i11_2,i11_3 c11
    class s22,i12_1 c12
    class s27,i13_1 c13
    class s30,i14_1 c14
    class s33,i15_1 c15
    class s35,i16_1 c16


    s1 --> i1_1
    s7 --> i1_2
    s14 --> i1_3
    s23 --> i1_4
    s25 --> i1_5

    s2 --> i2_1
    s10 --> i2_2

    s3 --> i3_1
    s17 --> i3_2
    s26 --> i3_3
    s29 --> i3_4
    s36 --> i3_5

    s4 --> i4_1
    s9 --> i4_2
    s12 --> i4_3
    s19--> i4_4

    s5 --> i5_1
    s6 --> i5_2
    s24 --> i5_3

    s8 --> i6_1

    s11 --> i7_1

    s13 --> i8_1
    s16 --> i8_2
    s20 --> i8_3
    s28 --> i8_4
    s31 --> i8_5

    s15 --> i9_1
    s18 --> i10_1

    s21 --> i11_1
    s32 --> i11_2
    s34 --> i11_3

    s22 --> i12_1
    s27 --> i13_1
    s30 --> i14_1
    s33 --> i15_1
    s35 --> i16_1
    ```

---

Studying the Order FOA developed methods of measuring the Order that are very sensitive to the composition of the elements in a sequence.

The following diagrams give a hand in understanding how the Objects and Methods defined in FOA relates to each other.

=== "Order as a property"
    ```mermaid
    flowchart TB
        Start@{ shape: sm-circ, label: "" }-- Sequence -->fork1@{ shape: sm-circ, label: "" }
        fork1-- Sequence -->alphabet
        alphabet-- Alphabet -->OA@{ shape: sm-circ }
        fork1-- Sequence -->order
        order-- Order -->OA
        OA-- Sequence -->End@{ shape: sm-circ }

        click alphabet "./alphabet" "Alphabet"
        click order "./order" "Order"
    ```

=== "Interval-based characteristics"
    ```mermaid
    flowchart TB
        Start@{ shape: sm-circ, label: "" }-- Sequence -->fork1@{ shape: sm-circ, label: "" }
        fork1-- Sequence -->alphabet
        alphabet-- Alphabet -->OA@{ shape: cross-circ }
        order-- Order -->OA@{ shape: sm-circ }
        OA-- Sequence -->End@{ shape: sm-circ }

        fork1@{ shape: sm-circ, label: "" }-- Sequence -->intervals
        intervals-- Intervals Chain -->fork@{ shape: sm-circ, label: "" }
        fork@{ shape: sm-circ, label: "" }-- Intervals Chain -->inverseIntervals@{ label: "intervals⁻¹" }
        fork@{ shape: sm-circ, label: "" }-- Intervals Chain -->distribution
        inverseIntervals@{ label: "intervals⁻¹" }-- Reconstructed Sequence --> order
        distribution-- Intervals Distribution --> M@{ shape: sm-circ, label: "order + alphabet" }
        M --> da@{ label: "Δa" }
        M --> dg@{ label: "Δg" }
        M --> g@{ label: "g" }
        M --> V@{ label: "V" }
        M --> G@{ label: "G" }
        da -- float --> EndMeasureda@{ shape: sm-circ }
        dg -- float --> EndMeasuredg@{ shape: sm-circ }
        g -- float --> EndMeasureg@{ shape: sm-circ }
        V -- int --> EndMeasureV@{ shape: sm-circ }
        G -- float --> EndMeasureG@{ shape: sm-circ }


        click alphabet "./alphabet" "Alphabet"
        click order "./order" "Order"
        click intervals "./intervals_chain/#define-intervals-chain" "Intervals"
        click inverseIntervals "./intervals_chain/#define-intervals-chain" "Intervals⁻"
        click distribution "./intervals_distribution" "Distribution"
        click distribution "./intervals_distribution" "Distribution"
        click dg "./characteristics/geometric_mean" "Geomteric mean"
        click da "./characteristics/arithmetic_mean" "Arithmetic mean"
        click g "./characteristics/average_remoteness" "Average remoteness"
        click G "./characteristics/depth" "Depth"
        click V "./characteristics/volume" "Volume"
    ```
