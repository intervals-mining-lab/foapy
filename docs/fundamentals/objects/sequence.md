# Sequence

A sequence is a fundamental concept in formal order analysis that is defined as a finite, enumerated collection of objects in which repetitions are allowed and order matters.
This is the basic object for analyzing patterns, relationships, and structural properties in ordered data.

## Mathematical Definition

Let $X$ is [_Carrier set_](./carrier_set.md#Mathematical Definition)

A _sequence_ $S$ is a n-tuple defined as

$$S = <s_1, s_2, ..., s_n>,$$

$$\forall i \in \{1, ..., n\} \exists s_i \in X$$

where:

- $s_i$​ is called the $i$-th _element_ (or coordinate) of the sequence.
- $n := |S|$ is _length_, $n \in N$

The _sequence_ $S$ can be also defined as a function

$$S : \{1, ..., n\} \longrightarrow X,$$

$$S(i)=s_i | i \in \{1, ..., n\}$$

## Examples

### Binary Sequence
A binary sequence `0110100110`

represented as

$X = \{0,1\}$

$S = <0,1,1,0,1,0,0,1,1,0>$

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

$S = <D,Dmaj7,D6,D,D\#dim,Em,A7,Em,A7,Em,A7,Em,A9,A7>$

### DNA Sequence
A DNA sequence `ATGCTAGCATGCTAGCATGCTAGC`

$X = \{A,C,T,G\}$

$S = <A,T,G,C,T,A,G,C,A,T,G,C,T,A,G,C,A,T,G,C,T,A,G,C>$

### English Text Sequence as char sequence
An English text sentence `the quick brown fox jumps over the lazy dog`

$X = \{\ ,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z\}$

$S = <t,h,e,\ ,q,u,i,c,k,\ ,b,r,o,w,n,\ ,f,o,x,\ ,j,u,m,p,s,\ ,o,v,e,r,\ ,t,h,e,\ ,l,a,z,y,\ ,d,o,g>$

### English Text Sequence as word sequence
An English text sentence `the quick brown fox jumps over the lazy dog`

$X = \{\ ,quick, fox, brown, the, over, dog, fox, lazy\}$

$S = <the,\ ,quick,\ ,brown,\ ,fox,\ ,jumps,\ ,over,\ ,the,\ ,lazy,\ ,dog>$
