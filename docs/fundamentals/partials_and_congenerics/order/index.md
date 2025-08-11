# Partial Order

A _Partial order_ is an [_Order_](../../order/order.md) having _empty_ elements.


``` mermaid
block-beta
columns 29

i1["1"] i2["2"] i3["3"] i4["4"] i5["5"] i6["6"] i7["7"] i8["8"] i9["9"] i10["10"] i11["11"] i12["12"]
i13["13"] i14["14"] i15["15"] i16["16"] i17["17"] i18["18"] i19["19"] i20["20"]
i21["21"] i22["22"] i23["23"] i24["24"] i25["25"] i26["26"] i27["27"]
i28["28"] i29["29"]

s1["1"] s2["2"] s3["3"] s4["4"] s5["5"] s6["5"] s7["1"] s8["6"] s9["4"] s10["2"]
s11["7"] s12["4"] s13["8"] s14["-"] s15["-"] s16["8"] s17["3"] s18["-"] s19["-"] s20["8"]
s21["-"] s22["9"] s23["-"] s24["5"] s25["-"] s26["3"] s27["-"] s28["-"] s29["3"]

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

Let $-$ is [_Empty element_](../carrier_set.md#mathematical-definition)

Let $- \notin N$

Define $N_{-} = N \cup \{-\}$

The _Partial order_ $O_p$ is defined as an l-tuple with additional constraints:

$$O_p = <o_1, o_2, ..., o_l>,$$

$$\forall i \in \{1, ..., l\} \exists o_i \in N_{-} $$

$$ \exists j \in \{1, ..., l\}, \forall i < j | O_p(i) \in \{ -\} \land O_p(j) = 1  $$

$$\forall i \in \{1, ..., l\}, O_p(i) \in \{-\} \lor O_p(i) \leq max(o_1, ..., o_{i-1}) + 1 \big| max(\{-\})=0$$

Where:

- $o_i$​ is called the $i$-th _element_ (or coordinate) of the partial order
- $l := |O_p|$ is called _length_ of the partial order, $l \in N$
- $n := |\{ O_p(i) | O_p(i) \ne - \}|$ is _non-empty elements count_, $n \in N$

### Order of Partial Sequence

Let $X$ is [_Carrier Set_](../../order/carrier_set.md#mathematical-definition)

Let $X_{-}$ is [_Partial Carrier Set_](../carrier_set.md#mathematical-definition)

$$X \subset X_{-}$$

Let $-$ is [_Empty element_](../carrier_set.md#mathematical-definition) of _Partial Carrier Set_

Let $S_p$ is [_Partial Sequence_](../sequence/index.md#mathematical-definition) described as function  $S_p : \{1,...,l\} \longrightarrow X_{-}$

Let $alphabet_p$ is [_Alphabet of Partial Sequence function_](../alphabet/index.md#mathematical-definition)

$$alphabet_p : \big\{\{1,...,l\} \longrightarrow X_{-} \big\} \longrightarrow \big\{\{1,...,m\} \longrightarrow X \big\}$$

Define

$$order_p(S_p) :  \big\{\{1,...,l\} \longrightarrow X_{-} \big\} \longrightarrow \big\{\{1,...,l\} \longrightarrow \{1,...,l\} \big\},$$

$$A = alphabet_p(S_p),$$

$$order_p(S_p)(i) = \Bigg\{\begin{array}{l} j \ \big| j \in \{1,...,l\}, S_p(i)=A(j), &  S_p(i) \notin \{-\} \\ -, & S_p(i) \in \{-\} \end{array}$$


### Order product Alphabet

Let $X$ is a [_Carrier set_](../../order/carrier_set.md)

Let $A$ is a [_Aphabet_](../../order/alphabet.md) $A : \{1, ..., m\} \longrightarrow X,$

Let $S_p$ is a [_Partial sequenece_](../sequence/index.md) $S : \{1, ..., l\} \longrightarrow X_{-},$

the following equations are true

$$O_p = order_p(S_p),$$

$$A = alphabet_p(S_p),$$

$$S_p = ( O_p \odot A),$$

$$S_p(i) = \Bigg\{\begin{array}{l} A(O_p(i)) , &  O_p(i) \notin \{-\} \\ -, & O_p(i) \in \{-\} \end{array}$$
