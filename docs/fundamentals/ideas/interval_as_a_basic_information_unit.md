---
hide:
  - toc
---
# Interval as a Basic Information Unit

Intervals serve as a fundamental unit of information by measuring the number of different
items, events, or symbols that occur between reseated in a sequence.

The intervals for symbol `A` in the following sequence would be `[3, 3, 1, 1, 1, 2, 1]`
``` mermaid
block-beta
  columns 12
  s1["A"] s2["C"] s3["T"] s4["A"] s5["C"] s6["G"] s7["A"] s8["A"] s9["A"] s10["T"] s11["A"] s12["A"]
  i1["3"]:3 i2["3"]:3 i3["1"]:1 i4["1"]:1 i5["1"]:1 i6["2"]:2 i7["1"]:1
```

In general, a sequence does not necessarily end with the same symbol it begins with.
To cover all cases, we consider the sequence as a looped sequence representing an infinite pattern with the same characteristics as the original data
This cyclic approach corresponds to the idea of ​​representativeness heuristic.

The intervals for symbol `C` in the following cycled sequence would be `[3, 9]`
``` mermaid
block-beta
  columns 15
  s1["A"] s2["C"] s3["T"] s4["A"] s5["C"] s6["G"] s7["A"] s8["A"] s9["A"] s10["T"] s11["A"] s12["A"] space s13["T"] s14["C"]
  space i1["3"]:3 i2["9"]:10
  s12 --> s13
```

The circular pattern preserves both the statistical properties and the order of elements.
Moreover, the average interval length is the inverse of the probability of an event, which directly relates intervals to probability.

\begin{array}{|c|c|c|}
\hline
 & \Delta_a  & P \\
\hline
A & \frac{3 + 3 + 1 + 1 + 1 + 2 + 1}{7} = \frac{12}{7} \approx 1.7142; & \frac{7}{12} = (\frac{12}{7})^{-1} = \Delta_a^{-1} \\
\hline
C & \frac{3 + 9}{2} = \frac{12}{2} = 6 & \frac{2}{12} = \frac{1}{6} = 6^{-1} = \Delta_a^{-1} \\
\hline
\end{array}

This makes intervals a crucial informational unit that offers deeper insights into the sequence than individual occurrences alone.
