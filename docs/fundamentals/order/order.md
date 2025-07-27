# Order

An _order_ is a n-tuple of natural numbers starting from `1` with `max+1` constraint.

## Mathematical Definition

The _order_ $O$ is defined as a n-tuple with additional constraints:

$$O = <o_1, o_2, ..., o_n>,$$

$$\forall i \in \{1, ..., n\} \exists o_i \in N $$

$$ o_1 = 1, $$

$$\forall i \in \{1, ..., n\}, o_i \leq max(o_1, ..., o_{i-1}) + 1$$

Where:

- $n := |O|$ is called _length_ of the order, $n \in N$
- $o_i$​ is called the $i$-th _element_ (or coordinate) of the order

### Order of Sequence

Let $X$ is [_Carrier set_](./carrier_set.md#mathematical-definition)

Let $S$ is [_Sequence_](./sequence.md#mathematical-definition) described as function  $S : \{1,...,n\} \longrightarrow X$

Let $alphabet$ is [_Alphabet function_](./alphabet.md#alphabet-of-sequence)

$$alphabet : \big\{\{1,...,n\} \longrightarrow X \big\} \longrightarrow \big\{\{1,...,m\} \longrightarrow X \big\}$$

Define

$$ordert(S) :  \big\{\{1,...,n\} \longrightarrow X \big\} \longrightarrow \big\{\{1,...,n\} \longrightarrow \{1,...,n\} \big\}$$

$$A = alphabet(S)$$

$$order(S)(i) = j \big| j \in \{1,...,n\}, S(i)=A(j)$$

### Order product Alphabet

Let $X$ is a [_Carrier set_](./carrier_set.md)

Let $A$ is a [_Aphabet_](./alphabet.md) $A : \{1, ..., m\} \longrightarrow X,$

Let $S$ is a [_Sequenece_](./sequence.md) $S : \{1, ..., n\} \longrightarrow X,$

the following equations are true

$$O = order(S),$$

$$A = alphabet(S),$$

$$S = ( O \odot A),$$

$$S(i) = A(O(i))$$




## Examples

### Valid order

``` mermaid
block-beta
  columns 36
  i1["1"] i2["2"] i3["3"] i4["2"] i5["4"] i6["2"]
  i7["5"] i8["2"] i9["6"] i10["2"] i11["7"] i12["2"]
  i13["1"] i14["2"] i15["8"] i16["2"] i17["9"]

  classDef red fill:#d62728,color:#000;

```

### Invalid order - Start different from `1`


``` mermaid
block-beta
  columns 36
  i1["2"] i2["2"] i3["3"] i4["2"] i5["4"] i6["2"]
  i7["5"] i8["2"] i9["6"] i10["2"] i11["7"] i12["2"]
  i13["1"] i14["2"] i15["8"] i16["2"] i17["9"]

  classDef red fill:#d62728,color:#000;

  class i1 red
```

### Invalid order - Contains elements not in `N`

``` mermaid
block-beta
  columns 36
  i1["1"] i2["2"] i3["3"] i4["2"] i5["4"] i6["2"]
  i7["5"] i8["2"] i9["6"] i10["T"] i11["7"] i12["2"]
  i13["1"] i14["-2"] i15["8"] i16["2"] i17["9"]

  classDef red fill:#d62728,color:#000;

  class i10,i14 red
```

### Invalid order - Violates `max + 1` contstraint

``` mermaid
block-beta
  columns 36
  i1["1"] i2["2"] i3["3"] i4["2"] i5["4"] i6["2"]
  i7["5"] i8["2"] i9["6"] i10["2"] i11["7"] i12["2"]
  i13["1"] i14["9"] i15["8"] i16["2"] i17["9"]

  classDef red fill:#d62728,color:#000;

  class i14 red
```

### Binary Sequence
A binary sequence `0110100110`

represented as

$O = <1, 2, 2, 1, 2, 1, 1, 2, 2, 1>$

### Musical Chorus Sequence
A musical chorus for `Jingle bell rock`

```
D                Dmaj7        D6
Jingle-bell, Jingle-bell, Jingle-bell Rock.
  D                D#dim
Jingle-bell swing and
 Em           A7     Em               A7            Em A7
Jingle-bell ring. Snowin' and blowin' up bushels of fun.
Em  A9                  A7
Now the jingle-hop has begun.
```

$O = <1, 2, 3, 1, 4, 5, 6, 5, 6, 7, 5, 8, 6>$

### DNA Sequence
A DNA sequence `ATGCTAGCATGCTAGCATGCTAGC`

$O = <1, 2, 3, 4, 2, 1, 3, 4, 1, 2, 3, 4, 2, 1, 3, 4, 1, 2, 3, 4, 2, 1, 3, 4>$

### English Text Sequence as word sequence
An English text sentence `the quick brown fox jumps over the lazy dog`

$O = <1, 2, 3, 2, 4, 2, 5, 2, 6, 2, 7, 2, 1, 2, 8, 2, 9>$
