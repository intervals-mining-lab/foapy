# Congeneric Intervals Distributions

_Congeneric Intervals Distributions_ is a stack of [_Partials Intervals Distribution_](../partials_and_congenerics/intervals_distribution.md)
that represents [_Intervals Distribution_](../order/intervals_distribution/index.md).

``` mermaid
block-beta
columns 30

space i1["1"] i2["2"] i3["3"] i4["4"] i5["5"] i6["6"] i7["7"] i8["8"] i9["9"] i10["10"] i11["11"] i12["12"]
i13["13"] i14["14"] i15["15"] i16["16"] i17["17"] i18["18"] i19["19"] i20["20"]
i21["21"] i22["22"] i23["23"] i24["24"] i25["25"] i26["26"] i27["27"]
i28["28"] i29["29"]

j1["1"] s1["0"] s2["0"] s3["0"] s4["0"] s5["0"] s6["1"] s7["0"] s8["0"] s9["0"] s10["0"]
s11["0"] s12["0"] s13["0"] s14["0"] s15["0"] s16["0"] s17["0"] s18["0"] s19["0"] s20["0"]
s21["0"] s22["0"] s23["1"] s24["0"] s25["0"] s26["0"] s27["0"] s28["0"] s29["0"]

j2["2"] n1["0"] n2["0"] n3["0"] n4["0"] n5["0"] n6["0"] n7["0"] n8["1"] n9["0"] n10["0"]
n11["0"] n12["0"] n13["0"] n14["0"] n15["0"] n16["0"] n17["0"] n18["0"] n19["0"] n20["0"]
n21["1"] n22["0"] n23["0"] n24["0"] n25["0"] n26["0"] n27["0"] n28["0"] n29["0"]

j3["3"] t1["0"] t2["0"] t3["2"] t4["0"] t5["0"] t6["0"] t7["0"] t8["0"] t9["1"] t10["0"]
t11["0"] t12["0"] t13["0"] t14["1"] t15["0"] t16["0"] t17["0"] t18["0"] t19["0"] t20["0"]
t21["0"] t22["0"] t23["0"] t24["0"] t25["0"] t26["0"] t27["0"] t28["0"] t29["0"]

j4["4"] e1["0"] e2["0"] e3["1"] e4["0"] e5["1"] e6["0"] e7["0"] e8["0"] e9["0"] e10["0"]
e11["0"] e12["0"] e13["0"] e14["0"] e15["0"] e16["0"] e17["0"] e18["0"] e19["0"] e20["0"]
e21["1"] e22["0"] e23["0"] e24["0"] e25["0"] e26["0"] e27["0"] e28["0"] e29["0"]

j5["5"] l1["1"] l2["0"] l3["0"] l4["0"] l5["0"] l6["0"] l7["0"] l8["0"] l9["0"] l10["1"]
l11["0"] l12["0"] l13["0"] l14["0"] l15["0"] l16["0"] l17["0"] l18["1"] l19["0"] l20["0"]
l21["0"] l22["0"] l23["0"] l24["0"] l25["0"] l26["0"] l27["0"] l28["0"] l29["0"]

j6["6"] g1["0"] g2["0"] g3["0"] g4["0"] g5["0"] g6["0"] g7["0"] g8["0"] g9["0"] g10["0"]
g11["0"] g12["0"] g13["0"] g14["0"] g15["0"] g16["0"] g17["0"] g18["0"] g19["0"] g20["0"]
g21["0"] g22["0"] g23["0"] g24["0"] g25["0"] g26["0"] g27["0"] g28["0"] g29["1"]

j7["7"] c1["0"] c2["0"] c3["0"] c4["0"] c5["0"] c6["0"] c7["0"] c8["0"] c9["0"] c10["0"]
c11["0"] c12["0"] c13["0"] c14["0"] c15["0"] c16["0"] c17["0"] c18["0"] c19["0"] c20["0"]
c21["0"] c22["0"] c23["0"] c24["0"] c25["0"] c26["0"] c27["0"] c28["0"] c29["1"]

j8["8"] sp1["0"] sp2["0"] sp3["1"] sp4["1"] sp5["0"] sp6["0"] sp7["0"] sp8["0"] sp9["0"] sp10["0"]
sp11["0"] sp12["0"] sp13["0"] sp14["0"] sp15["0"] sp16["0"] sp17["0"] sp18["0"] sp19["0"] sp20["0"]
sp21["0"] sp22["1"] sp23["0"] sp24["0"] sp25["0"] sp26["0"] sp27["0"] sp28["0"] sp29["0"]

j9["9"] b1["0"] b2["0"] b3["0"] b4["0"] b5["0"] b6["0"] b7["0"] b8["0"] b9["0"] b10["0"]
b11["0"] b12["0"] b13["0"] b14["0"] b15["0"] b16["0"] b17["0"] b18["0"] b19["0"] b20["0"]
b21["0"] b22["0"] b23["0"] b24["0"] b25["0"] b26["0"] b27["0"] b28["0"] b29["1"]


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

class s1,s2,s3,s4,s5,s7,s8,s9,s10 index
class s11,s12,s13,s14,s15,s16,s17,s18,s19,s20 index
class s21,s22,s24,s25,s26,s27,s28,s29 index

class n1,n2,n3,n4,n5,n6,n7,n9,n10 index
class n11,n12,n13,n14,n15,n16,n17,n18,n19,n20 index
class n22,n23,n24,n25,n26,n27,n28,n29 index

class t1,t2,t4,t5,t6,t7,t8,t10 index
class t11,t12,t13,t15,t16,t17,t18,t19,t20 index
class t21,t22,t23,t24,t25,t26,t27,t28,t29 index

class e1,e2,e4,e6,e7,e8,e9,e10 index
class e11,e12,e13,e14,e15,e16,e17,e18,e19,e20 index
class e22,e23,e24,e25,e26,e27,e28,e29 index

class l2,l3,l4,l5,l6,l7,l8,l9 index
class l11,l12,l13,l14,l15,l16,l17,l19,l20 index
class l21,l22,l23,l24,l25,l26,l27,l28,l29 index

class g1,g2,g3,g4,g5,g6,g7,g8,g9,g10 index
class g11,g12,g13,g14,g15,g16,g17,g18,g19,g20 index
class g21,g22,g23,g24,g25,g26,g27,g28 index

class c1,c2,c3,c4,c5,c6,c7,c8,c9,c10 index
class c11,c12,c13,c14,c15,c16,c17,c18,c19,c20 index
class c21,c22,c23,c24,c25,c26,c27,c28 index

class sp1,sp2,sp5,sp6,sp7,sp8,sp9,sp10 index
class sp11,sp12,sp13,sp14,sp15,sp16,sp17,sp18,sp19,sp20 index
class sp21,sp23,sp24,sp25,sp26,sp27,sp28,sp29 index

class b1,b2,b3,b4,b5,b6,b7,b8,b9,b10 index
class b11,b12,b13,b14,b15,b16,b17,b18,b19,b20 index
class b21,b22,b23,b24,b25,b26,b27,b28 index


class i1,i2,i3,i4,i5,i6,i7,i8,i9,i10 index
class i11,i12,i13,i14,i15,i16,i17,i18,i19,i20 index
class i21,i22,i23,i24,i25,i26,i27,i28,i29 index

class j1,j2,j3,j4,j5,j6,j7,j8,j9 index
```

## Mathematical Definition

Let $ID_p$ is [_Partial Interval Distribution_](../partials_and_congenerics/intervals_distribution.md#mathematical-definition)

Define a _Congeric intervals distributions_

### as m-tuple of congeneric intervals distributions

$CID$ is m-tuple of $ID_c$ _intervals distributions_

$$CID = <cid_1, cid_2, ..., cid_m>,$$

$$\forall j \in \{1, ..., m\} \exists cid_j \in \{ID_c\}, $$

where:

- $cid_j$​ is called the $j$-th _congeneric intervals distribution_.
- $l := |CID(1)|$ is _length_, $l \in N$
- $m := |CID|$ is _power_, $m \in N$

### as matrix (m,l)

$CID$ is (m,l) matrix of $\{0,..,, l\}$

$$
CID =
\begin{pmatrix}
cid_{1,1} & cid_{1,2} & \cdots & cid_{1,l} \\
cid_{2,1} & cid_{2,2} & \cdots & cid_{2,l} \\
\vdots   & \vdots   & \ddots & \vdots   \\
cid_{m,1} & cid_{m,2} & \cdots & cid_{m,l}
\end{pmatrix}
$$

$$\forall j \in \{1, ..., m\}, i \in \{1, ..., l\} \exists cid_{j,i} \in \{0,..,, l\}, $$

where:

- $cid_j$​ is called the $j$-th _congeneric intervals distribution_ or $j$-th _row_.
- $cid_{j,i}$​ is called the $i$-th element of $j$-th _congeneric intervals distribution_.
- $l$ is _length_, $l \in N$
- $m$ is _power_, $m \in N$


### from Congeneric Intervals Chains

Let $IC_{p}$ is [_Partial Interval Chain_](../partials_and_congenerics/intervals_chain/index.md#define-partial-intervals-chain)

Let $ID_p$ is [_Partial Intervals distribution_](../partials_and_congenerics/intervals_distribution.md#mathematical-definition) described as function

$$ID_p : \big\{  IC_p \big\} \longrightarrow \big\{ \{1,...,l\} \longrightarrow  N_0 \big\},$$

Let $CIC$ is [_Congeneric Intervals Chains_](./intervals_chains.md#as-matrix-ml) - (m,l) matrix of $\{1,...,l\} \cup \{-\}$

$$
CIC =
\begin{pmatrix}
\Delta_{1,1} & \Delta_{1,2} & \cdots & \Delta_{1,l} \\
\Delta_{2,1} & \Delta_{2,2} & \cdots & \Delta_{2,l} \\
\vdots   & \vdots   & \ddots & \vdots   \\
\Delta_{m,1} & \Delta_{m,2} & \cdots & \Delta_{m,l}
\end{pmatrix}
$$

Define

$$congenerics\_intervals\_distributions : \{CIC\} \longrightarrow \{CID\}$$

$$congenerics\_intervals\_distributions(CIC)(j)(i) = ID_p(CIC(j))(i) $$
