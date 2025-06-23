# Binding

A __binding__ determines the way of reading the sequence when computing intervals.
Two binding values ​​are defined - $start$ and $end$.
$start$ binding counts intervals back to the previous occurrence of the element and the $end$ binding forward to the next occurrence.
In other words, you can think of $start$ as looking for `right-to-left` and $end$ as looking for `left-to-right`.
In practice, there is no good reason to prefer one binding over the other.
We define `binding` in the interests of a consistent and fully encompassing mathematical theory.

## Mathematical Definition

Define _binding_ $B = \{ start, end \}$


## Examples

The interval for the second appearance of the symbol `A` in the following sequence would be `3` for $start$ bidning and `4` for $end$.
``` mermaid
block-beta
  columns 9
  space l1["<-- start --"]:3 space:5
  space start1["3"]:3 space:5
  s1["A"] s2["C"] s3["T"] s4["A"] s5["C"] s6["G"] s7["G"] s8["A"] s9["G"]
  space:3 end1["4"]:4 space:2
  space:3 l3["-- end -->"]:4

  classDef c3 fill:#2ca02c,color:#fff;
  classDef c4 fill:#98df8a,color:#000;
  classDef active fill:#98df8a,color:#000,stroke-width:4px;
  classDef label fill:#fff,color:#000,stroke-width:0px;
  class s1,s8 c3
  class s4 active
  class start1,end1 c4
  class l1,l2,l3 label
```
