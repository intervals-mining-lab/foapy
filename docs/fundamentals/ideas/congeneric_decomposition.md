---
hide:
  - toc
---
# Congeneric Decomposition

Cogeneric decomposition is a method for decomposing symbolic sequences from a systems thinking perspective,
emphasizing the importance of order. It decomposes a sequence into a tuple of cogeneric sequences,
each of which consists of equivalent elements at certain positions, while all other positions are empty.
This reversible process preserves the order of the sequence and allows the original sequence to be fully reconstructed.

The concept of Cogeneric decomposition can be demonstrated using an example:

Let's assume there is a symbolic sequence `INTELLIGENCE IS THE ABILITY TO ADAPT` congeneric decomposition
could be presented by the following table, where each row is a congeneric sequence and  `-` is an empty position in a congeneric sequence.


\begin{equation}
\scriptsize
\begin{array}{|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|}
\hline
\cellcolor{#ff7f0e}I & \cellcolor{#ffbb78}N & \cellcolor{#2ca02c}T & \cellcolor{#98df8a}E & \cellcolor{#d62728}L & \cellcolor{#d62728}L & \cellcolor{#ff7f0e}I & \cellcolor{#ff9896}G & \cellcolor{#98df8a}E & \cellcolor{#ffbb78}N & \cellcolor{#9467bd}C & \cellcolor{#98df8a}E & \cellcolor{#c5b0d5}\text{ } & \cellcolor{#ff7f0e}I & \cellcolor{#8c564b}S & \cellcolor{#c5b0d5}\text{ } & \cellcolor{#2ca02c}T & \cellcolor{#c49c94}H & \cellcolor{#98df8a}E & \cellcolor{#c5b0d5}\text{ } & \cellcolor{#e377c2}A & \cellcolor{#f7b6d2}B & \cellcolor{#ff7f0e}I & \cellcolor{#d62728}L & \cellcolor{#ff7f0e}I & \cellcolor{#2ca02c}T & \cellcolor{#bcbd22}Y & \cellcolor{#c5b0d5}\text{ } & \cellcolor{#2ca02c}T & \cellcolor{#dbdb8d}O & \cellcolor{#c5b0d5}\text{ } & \cellcolor{#e377c2}A & \cellcolor{#17becf}D & \cellcolor{#e377c2}A & \cellcolor{#9edae5}P & \cellcolor{#2ca02c}T \\
\hline
\cellcolor{#ff7f0e}I & - & - & - & - & - & \cellcolor{#ff7f0e}I & - & - & - & - & - & - & \cellcolor{#ff7f0e}I & - & - & - & - & - & - & - & - & \cellcolor{#ff7f0e}I & - & \cellcolor{#ff7f0e}I & - & - & - & - & - & - & - & - & - & - & - \\
\hline
- & \cellcolor{#ffbb78}N & - & - & - & - & - & - & - & \cellcolor{#ffbb78}N & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - \\
\hline
- & - & \cellcolor{#2ca02c}T & - & - & - & - & - & - & - & - & - & - & - & - & - & \cellcolor{#2ca02c}T & - & - & - & - & - & - & - & - & \cellcolor{#2ca02c}T & - & - & \cellcolor{#2ca02c}T & - & - & - & - & - &- & \cellcolor{#2ca02c}T \\
\hline
- & - & - & \cellcolor{#98df8a}E & - & - & - & - & \cellcolor{#98df8a}E & - & - & \cellcolor{#98df8a}E & - & - & - & - & - & - & \cellcolor{#98df8a}E & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - \\
\hline
- & - & - & - & \cellcolor{#d62728}L & \cellcolor{#d62728}L & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & \cellcolor{#d62728}L & - & - & - & - & - & - & - & - & - & - & - & - \\
\hline
- & - & - & - & - & - & - & \cellcolor{#ff9896}G & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - \\
\hline
- & - & - & - & - & - & - & - & - & - & \cellcolor{#9467bd}C & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - \\
\hline
- & - & - & - & - & - & - & - & - & - & - & - & \cellcolor{#c5b0d5}\text{ } & - & - & \cellcolor{#c5b0d5}\text{ } & - & - & - & \cellcolor{#c5b0d5}\text{ } & - & - & - & - & - & - & - & \cellcolor{#c5b0d5}\text{ } & - & - & \cellcolor{#c5b0d5}\text{ } & - & - & - & - & - \\
\hline
- & - & - & - & - & - & - & - & - & - & - & - & - & - & \cellcolor{#8c564b}S & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - \\
\hline
- & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & \cellcolor{#c49c94}H & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - \\
\hline
- & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & \cellcolor{#e377c2}A & - & - & - & - & - & - & - & - & - & - & \cellcolor{#e377c2}A & - & \cellcolor{#e377c2}A & - & - \\
\hline
- & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & \cellcolor{#f7b6d2}B & - & - & - & - & - & - & - & - & - & - & - & - & - & - \\
\hline
- & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & \cellcolor{#bcbd22}Y & - & - & - & - & - & - & - & - & - \\
\hline
- & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & \cellcolor{#dbdb8d}O & - & - & - & - & - & - \\
\hline
- & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & \cellcolor{#17becf}D & - & - & - \\
\hline
- & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & - & \cellcolor{#9edae5}P & - \\
\hline
\end{array}
\end{equation}



Congeneric sequence for `E`
``` mermaid
block-beta
  columns 36
  e1["-"] e2["-"] e3["-"] e4["E"] e5["-"] e6["-"] e7["-"] e8["-"] e9["E"] e10["-"]
  e11["-"] e12["E"] e13["-"] e14["-"] e15["-"] e16["-"] e17["-"] e18["-"] e19["E"] e20["-"]
  e21["-"] e22["-"] e23["-"] e24["-"] e25["-"] e26["-"] e27["-"] e28["-"] e29["-"] e30["-"]
  e31["-"] e32["-"] e33["-"] e34["-"] e35["-"] e36["-"]
```


could be a part of multiple symbol sequences that have the same order of `E` element.

While keeping the main idea, the congeneric decomposition could be applied, with a flavor, to any type of special case symbolic sequences, such as Order.

<!-- TODO: Add example of congeneric decomposition code -->

<style>
.md-typeset table:not([class]) th {
    min-width: 0 !important;
}

.md-typeset td:not([class]):not(:last-child), .md-typeset th:not([class]):not(:last-child) {
    border-right: .05rem solid var(--md-typeset-table-color);
}

.md-typeset td, .md-typeset th {
    padding-left: 0.4em !important;
    padding-right: 0.4em !important;
    padding-top: 0.1em !important;
    padding-bottom: 0.1em !important;
    text-align: center !important;
}
</style>
