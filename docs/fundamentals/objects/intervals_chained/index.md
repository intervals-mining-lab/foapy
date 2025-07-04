# Intervals Chained

An _intervals chained is an n-tuple of natural numbers that represents the distance between equal elements in a sequence.

## Mathematical Definition

Let $X$ is [_Carrier set_](./carrier_set.md#Mathematical Definition)

Let $S$ is [_Sequence_](./sequence.md#Mathematical Definition)  length of $n$ described as function $S : \{1,...,n\} \longrightarrow X$

Define

$$IntervalsChained = <io_1, io_2, ..., io_n> | \forall j \in \{1,...,n\} \exists io_j \in \{1,...,n\},$$

if exists

$$Intervals : \big\{S\}  \longrightarrow \big\{ IntervalsChained \big\},$$

$$Intervals^{-1} : \big\{ IntervalsChained \big\}  \longrightarrow \big\{ \{1,...,n\} \longrightarrow \{1,...,m\} \big\},$$


$$Intervals(S) = Intervals(Intervals^{-1}(Intervals(S)))$$

and exists

$$Follow : B \times \big\{ IntervalsChained \big\}  \longrightarrow \big\{ \{1,...,n\} \longrightarrow \{1,...,n\} \big\}$$


<!-- $$Follow : B \times \big\{ \{1,...,n\} \longrightarrow \{1,...,n\} \big\}  \longrightarrow \big\{ \{1,...,n\} \longrightarrow \{0,...,n+1\} \big\}$$

$$Traceble : B \times \big\{ \{1,...,n\} \longrightarrow \{1,...,n\} \big\}  \longrightarrow \big\{ \{1,...,n\} \longrightarrow \{0, 1\} \big\}$$
 -->
<!-- Define `follow` $F : B \times M \times J^n \longrightarrow (J)^n$

Define `traceble` $T : B \times M \times J^n \longrightarrow (\{True, False\})^n$ -->






<!-- is called `Intervals chain` if and only if

$$\exists (b, m) \in B \times M$$

that makes these statments true:

1. Tracebility criteria - $\forall i \ Traceble(b, m)(IO)(i)$
2. Chained criteria - $f=Follow(b,m)(IO),\ \forall i \forall j \ne i  | f(i) \neq f(j) \lor f(i) \in \{0, n+1\}$

 -->


Where:

- $n := |O|$ is called _length_ of the order, $n \in N$
- $o_i$​ is called the $i$-th _element_ (or coordinate) of the order

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

### Invalid order - Contains elements not in $N$

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
