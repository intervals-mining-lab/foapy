# Congeneric Sequence

_Congeneric sequence_ is an extreme case of [_Parial sequence_](./index.md) where all _non-empty_ elements are equals.

 $S_{c|T}$ is _Congeneric sequence_ for `T`

``` mermaid
block-beta
columns 29

i1["1"] i2["2"] i3["3"] i4["4"] i5["5"] i6["6"] i7["7"] i8["8"] i9["9"] i10["10"] i11["11"] i12["12"]
i13["13"] i14["14"] i15["15"] i16["16"] i17["17"] i18["18"] i19["19"] i20["20"]
i21["21"] i22["12"] i23["23"] i24["24"] i25["25"] i26["26"] i27["27"]
i28["28"] i29["29"]

s1["-"] s2["-"] s3["T"] s4["-"] s5["-"] s6["-"] s7["-"] s8["-"] s9["-"] s10["-"]
s11["-"] s12["-"] s13["-"] s14["-"] s15["-"] s16["-"] s17["T"] s18["-"] s19["-"] s20["-"]
s21["-"] s22["-"] s23["-"] s24["-"] s25["-"] s26["T"] s27["-"] s28["-"] s29["T"]

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

class s1,s2,s4,s5,s6,s7,s8,s9,s10 skip
class s11,s12,s13,s14,s15,s16,s18,s19,s20 skip
class s21,s22,s23,s24,s25,s27,s28,s30 skip
class s31,s32,s33,s34,s35 skip

class i1,i2,i3,i4,i5,i6,i7,i8,i9,i10 index
class i11,i12,i13,i14,i15,i16,i17,i18,i19,i20 index
class i21,i22,i23,i24,i25,i26,i27,i28,i29 index
```

## Mathematical Definition

Let $X$ is [_Carrier Set_](../../order/carrier_set.md#mathematical-definition)

Let $X_{-}$ is [_Partial Carrier Set_](../carrier_set.md#mathematical-definition)

$$X \subset X_{-}$$

Let $S_p$ is [_Partial sequence_](index.md#mathematical-definition) $S_p : \{1, ..., l\} \longrightarrow X_{-},$

$S_p$ is called $S_{c|e}$ - _Congeneric sequence_ of $e$ element - if $\exists e \in X\Big|\forall i, S_{p}(i) \in \{-, e\}$
