# Congeneric Intervals Chains

_Congeneric Intervals Chains_ is a stack of a [_compatible_](../partials_and_congenerics/sequence/index.md#compatibility) [_congeric interval chain_](../partials_and_congenerics/intervals_chain/congeneric.md)
that represents [_Intervals Chain_](../order/intervals_chain/index.md) or [_Partial Intervals Chain_](../partials_and_congenerics/intervals_chain/index.md). The _congeneric intervals chains_ are sorted in the stack by the first position with a _non-empty_ element in it.

``` mermaid
block-beta
columns 30

space i1["1"] i2["2"] i3["3"] i4["4"] i5["5"] i6["6"] i7["7"] i8["8"] i9["9"] i10["10"] i11["11"] i12["12"]
i13["13"] i14["14"] i15["15"] i16["16"] i17["17"] i18["18"] i19["19"] i20["20"]
i21["21"] i22["22"] i23["23"] i24["24"] i25["25"] i26["26"] i27["27"]
i28["28"] i29["29"]

j1["1"] s1["23"] s2["-"] s3["-"] s4["-"] s5["-"] s6["-"] s7["6"] s8["-"] s9["-"] s10["-"]
s11["-"] s12["-"] s13["-"] s14["-"] s15["-"] s16["-"] s17["-"] s18["-"] s19["-"] s20["-"]
s21["-"] s22["-"] s23["-"] s24["-"] s25["-"] s26["-"] s27["-"] s28["-"] s29["-"]

j2["2"] n1["-"] n2["21"] n3["-"] n4["-"] n5["-"] n6["-"] n7["-"] n8["-"] n9["-"] n10["8"]
n11["-"] n12["-"] n13["-"] n14["-"] n15["-"] n16["-"] n17["-"] n18["-"] n19["-"] n20["-"]
n21["-"] n22["-"] n23["-"] n24["-"] n25["-"] n26["-"] n27["-"] n28["-"] n29["-"]

j3["3"] t1["-"] t2["-"] t3["3"] t4["-"] t5["-"] t6["-"] t7["-"] t8["-"] t9["-"] t10["-"]
t11["-"] t12["-"] t13["-"] t14["-"] t15["-"] t16["-"] t17["14"] t18["-"] t19["-"] t20["-"]
t21["-"] t22["-"] t23["-"] t24["-"] t25["-"] t26["9"] t27["-"] t28["-"] t29["3"]

j4["4"] e1["-"] e2["-"] e3["-"] e4["21"] e5["-"] e6["-"] e7["-"] e8["-"] e9["5"] e10["-"]
e11["-"] e12["3"] e13["-"] e14["-"] e15["-"] e16["-"] e17["-"] e18["-"] e19["-"] e20["-"]
e21["-"] e22["-"] e23["-"] e24["-"] e25["-"] e26["-"] e27["-"] e28["-"] e29["-"]

j5["5"] l1["-"] l2["-"] l3["-"] l4["-"] l5["10"] l6["1"] l7["-"] l8["-"] l9["-"] l10["-"]
l11["-"] l12["-"] l13["-"] l14["-"] l15["-"] l16["-"] l17["-"] l18["-"] l19["-"] l20["-"]
l21["-"] l22["-"] l23["-"] l24["18"] l25["-"] l26["-"] l27["-"] l28["-"] l29["-"]

j6["6"] g1["-"] g2["-"] g3["-"] g4["-"] g5["-"] g6["-"] g7["-"] g8["29"] g9["-"] g10["-"]
g11["-"] g12["-"] g13["-"] g14["-"] g15["-"] g16["-"] g17["-"] g18["-"] g19["-"] g20["-"]
g21["-"] g22["-"] g23["-"] g24["-"] g25["-"] g26["-"] g27["-"] g28["-"] g29["-"]

j7["7"] c1["-"] c2["-"] c3["-"] c4["-"] c5["-"] c6["-"] c7["-"] c8["-"] c9["-"] c10["-"]
c11["29"] c12["-"] c13["-"] c14["-"] c15["-"] c16["-"] c17["-"] c18["-"] c19["-"] c20["-"]
c21["-"] c22["-"] c23["-"] c24["-"] c25["-"] c26["-"] c27["-"] c28["-"] c29["-"]

j8["8"] sp1["-"] sp2["-"] sp3["-"] sp4["-"] sp5["-"] sp6["-"] sp7["-"] sp8["-"] sp9["-"] sp10["-"]
sp11["-"] sp12["-"] sp13["22"] sp14["-"] sp15["-"] sp16["3"] sp17["-"] sp18["-"] sp19["-"] sp20["4"]
sp21["-"] sp22["-"] sp23["-"] sp24["-"] sp25["-"] sp26["-"] sp27["-"] sp28["-"] sp29["-"]

j9["9"] b1["-"] b2["-"] b3["-"] b4["-"] b5["-"] b6["-"] b7["-"] b8["-"] b9["-"] b10["-"]
b11["-"] b12["-"] b13["-"] b14["-"] b15["-"] b16["-"] b17["-"] b18["-"] b19["-"] b20["-"]
b21["-"] b22["29"] b23["-"] b24["-"] b25["-"] b26["-"] b27["-"] b28["-"] b29["-"]


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

class s2,s3,s4,s5,s6,s8,s9,s10 index
class s11,s12,s13,s14,s15,s16,s17,s18,s19,s20 index
class s21,s22,s23,s24,s25,s26,s27,s28,s29 index

class n1,n3,n4,n5,n6,n7,n8,n9 index
class n11,n12,n13,n14,n15,n16,n17,n18,n19,n20 index
class n21,n22,n23,n24,n25,n26,n27,n28,n29 index

class t1,t2,t4,t5,t6,t7,t8,t9,t10 index
class t11,t12,t13,t14,t15,t16,t18,t19,t20 index
class t21,t22,t23,t24,t25,t27,t28 index

class e1,e2,e3,e5,e6,e7,e8,e10 index
class e11,e13,e14,e15,e16,e17,e18,e19,e20 index
class e21,e22,e23,e24,e25,e26,e27,e28,e29 index

class l1,l2,l3,l4,l7,l8,l9,l10 index
class l11,l12,l13,l14,l15,l16,l17,l18,l19,l20 index
class l21,l22,l23,l25,l26,l27,l28,l29 index

class g1,g2,g3,g4,g5,g6,g7,g9,g10 index
class g11,g12,g13,g14,g15,g16,g17,g18,g19,g20 index
class g21,g22,g23,g24,g25,g26,g27,g28,g29 index

class c1,c2,c3,c4,c5,c6,c7,c8,c9,c10 index
class c12,c13,c14,c15,c16,c17,c18,c19,c20 index
class c21,c22,c23,c24,c25,c26,c27,c28,c29 index

class sp1,sp2,sp3,sp4,sp5,sp6,sp7,sp8,sp9,sp10 index
class sp11,sp12,sp14,sp15,sp17,sp18,sp19 index
class sp21,sp22,sp23,sp24,sp25,sp26,sp27,sp28,sp29 index

class b1,b2,b3,b4,b5,b6,b7,b8,b9,b10 index
class b11,b12,b13,b14,b15,b16,b17,b18,b19,b20 index
class b21,b23,b24,b25,b26,b27,b28,b29 index


class i1,i2,i3,i4,i5,i6,i7,i8,i9,i10 index
class i11,i12,i13,i14,i15,i16,i17,i18,i19,i20 index
class i21,i22,i23,i24,i25,i26,i27,i28,i29 index

class j1,j2,j3,j4,j5,j6,j7,j8,j9 index
```

## Mathematical Definition

Let $IC_{c}$ is [_Congeneric Interval Chain_](../partials_and_congenerics/intervals_chain/congeneric.md#mathematical-definition)

Define a _Congeric intervals chains_

### as m-tuple of congeneric intervals chain

Let $compatible(IC1_c, IC2_c)$ is [_compatibility of Partial Sequences function_](../partials_and_congenerics/sequence/index.md#compatibility)

$CIC$ is m-tuple of $IC_c$ _intervals chain_

$$CIC = <cic_1, cic_2, ..., cic_m>,$$

$$\forall j \in \{1, ..., m\} \exists cic_j \in \{IC_c\}, $$

all _congeneric intervals chains_ are _compatible_

$$compatible(CIC(k), CIC(j)) \bigg| \forall k,j \in \{1, ..., m\}, k \ne j,$$

and sorted by first apperance of _non-empty_ element

$$\forall k > j \in \{1,...,m\},\ x < i \in \{1,...,l\}, CIC(k)(x) \ne 1 \bigg| CIC(j)(i) \notin \{-\} \land CIC(j)(x) \in \{-\}$$

where:

- $cic_j$​ is called the $j$-th _congeneric intervals chain_.
- $l := |CIC(1)|$ is _length_, $l \in N$
- $m := |CIC|$ is _power_, $m \in N$

### as matrix (m,l)

$CIC$ is (m,l) matrix of $\{1,..,, l\} \cup \{-\}$

$$
CIC =
\begin{pmatrix}
\Delta_{1,1} & \Delta_{1,2} & \cdots & \Delta_{1,l} \\
\Delta_{2,1} & \Delta_{2,2} & \cdots & \Delta_{2,l} \\
\vdots   & \vdots   & \ddots & \vdots   \\
\Delta_{m,1} & \Delta_{m,2} & \cdots & \Delta_{m,l}
\end{pmatrix}
$$

$$\forall j \in \{1, ..., m\}, i \in \{1, ..., l\} \exists \Delta_{j,i} \in \{1,..,, l\} \cup \{-\}, $$

columns are _compatible_

$$\ \Delta_{k,i} \in \{-\} \big | \forall i \in \{1,...,l\}, \forall j \in \{1,...,m\}, \forall  k \ne j,\ \Delta_{j,i} \in \{1,...,l\} $$

and sorted by first apperance of _non-empty_ element

$$\forall k > j \in \{1,...,m\},\ x < i \in \{1,...,l\}, \Delta_{k,x} \in \{-\} \bigg| \Delta_{j,i} \in \{1,...,l\} \land \Delta_{j,x} \in \{-\}$$

where:

- $\Delta_j$​ is called the $j$-th _congeneric intervals chain_ or $j$-th _row_.
- $\Delta_{j,i}$​ is called the $i$-th element of $j$-th _congeneric intervals chain_.
- $l$ is _length_, $l \in N$
- $m$ is _power_, $m \in N$


### from Congeneric Sequences

Let $X_{-}$ is a [_Parial carrier set_](../partials_and_congenerics/carrier_set.md#mathematical-definition)

Let $CS$ is [_Congeneric Sequences_](./sequences.md#mathematical-definition) - (m,l) matrix of $X_{-}$

Let $Binging_p$ is [_Partial Binding_](../partials_and_congenerics/intervals_chain/index.md#define-partial-bindings)

Let $Intervals_p$ is [_Partial Intervals function_](../partials_and_congenerics/intervals_chain/index.md#define-partial-intervals-chain) described as function

$$Intervals_p : \big\{Binding_p\big\} \times \big\{S_p\}  \longrightarrow \big\{ IC_p \big\}$$

$$
CS =
\begin{pmatrix}
cs_{1,1} & cs_{1,2} & \cdots & cs_{1,l} \\
cs_{2,1} & cs_{2,2} & \cdots & cs_{2,l} \\
\vdots   & \vdots   & \ddots & \vdots   \\
cs_{m,1} & cs_{m,2} & \cdots & cs_{m,l}
\end{pmatrix}
$$

Define

$$congenerics\_intervals\_chains : \{CS\} \longrightarrow \{CIC\}$$

$$congenerics\_intervals\_chains(CS)(j)(i) = Intervals_p(CS(j))(i) $$

$$\exists congenerics\_intervals\_chain^{-1} : \{CIC\} \longrightarrow \{CS\},$$

$$congenerics\_intervals\_chains^{-1}(CIC)(i) = \Bigg\{\begin{array}{l}
    j, & \exists j \in \{1,...,m\}, CIC(j)(i) \notin \{-\} \\
    -, &   otherwise
\end{array}$$


### from Congeneric Orders

Let $CO$ is [_Congeneric Orders_](./orders.md#mathematical-definition) - (m,l) matrix of $\{1,...,l\} \cup \{-\}$

Let $Binging_p$ is [_Partial Binding_](../partials_and_congenerics/intervals_chain/index.md#define-partial-bindings)

Let $Intervals_p$ is [_Partial Intervals function_](../partials_and_congenerics/intervals_chain/index.md#define-partial-intervals-chain) described as function

$$Intervals_p : \big\{Binding_p\big\} \times \big\{S_p\}  \longrightarrow \big\{ IC_p \big\}$$

$$
CO =
\begin{pmatrix}
co_{1,1} & co_{1,2} & \cdots & co_{1,l} \\
co_{2,1} & co_{2,2} & \cdots & co_{2,l} \\
\vdots   & \vdots   & \ddots & \vdots   \\
co_{m,1} & co_{m,2} & \cdots & co_{m,l}
\end{pmatrix}
$$

Define

$$congenerics\_intervals\_chains : \{CO\} \longrightarrow \{CIC\}$$

$$congenerics\_intervals\_chains(CO)(j)(i) = Intervals_p(CO(j))(i) $$

$$\exists congenerics\_intervals\_chain^{-1} : \{CIC\} \longrightarrow \{CO\},$$

$$congenerics\_intervals\_chains^{-1}(CIC)(i) = \Bigg\{\begin{array}{l}
    1, & \exists j \in \{1,...,m\}, CIC(j)(i) \notin \{-\} \\
    -, &   otherwise
\end{array}$$
