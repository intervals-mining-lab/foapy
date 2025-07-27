# Alphabet

An alphabet is a m-tuple of unique elements.

## Mathematical Definition

Let $X$ is [_Carrier set_](./carrier_set.md#mathematical-definition)

The _alphabet_ $A$ is a m-tuple with a uniqueness constraint, can be defined:

$$A = <a_1, a_2, ..., a_m>,$$

$$\forall i,j \in \{1, ... ,m\}, i \neq j \implies a_i \neq a_j,$$

$$\forall i \in \{1, ... ,m\} \exists a_i \in X $$

Where:

- $m := |A|$ is called _power_ of the alphabet, $m \in N$
- $a_i$​ is called the $i$-th _element_ (or coordinate) of the alphabet.

### Alphabet of Sequence

Let $X$ is [_Carrier set_](./carrier_set.md#mathematical-definition)

Let $S$ is [_Sequence_](./sequence.md#mathematical-definition) described as function  $S : \{1,...,n\} \longrightarrow X$

$$alphabet(S) :  \big\{\{1,...,n\} \longrightarrow X \big\} \longrightarrow \big\{\{1,...,m\} \longrightarrow X \big\}$$

$$alphabet(S) = \big<S(i) \big| i \in \{1,...,n\}, \forall k < i,  S(i) \neq S(k)\big>$$


Where:

- $m \leq n$ - power of the alphabet is not greater than length of the sequence

## Examples

### Binary Sequence
A binary sequence `0110100110`

represented as

$X = \{0,1\}$

$A = <0,1>$

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

$X = \{A7, A9, D, D6, Dmaj7, D\#dim, Em\}$

$A = <D,Dmaj7,D6,D,D\#dim,Em,A7,A9>$

### DNA Sequence
A DNA sequence `ATGCTAGCATGCTAGCATGCTAGC`

$X = \{A,C,T,G\}$

$A = <A,T,G,C>$

### English Text Sequence as char sequence
An English text sentence `the quick brown fox jumps over the lazy dog`

$X = \{\ ,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z\}$

$A = <t,h,e,\ ,q,u,i,c,k,b,r,o,w,n,f,x,j,m,p,s,v,l,a,z,y,d,g>$

### English Text Sequence as word sequence
An English text sentence `the quick brown fox jumps over the lazy dog`

$X = \{\ ,quick, fox, brown, the, over, dog, fox, lazy\}$

$A = <the,\ ,quick,brown,fox,jumps,over,lazy,dog>$
