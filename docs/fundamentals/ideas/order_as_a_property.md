---
hide:
  - toc
---
# Order as a Property

Formal order analysis defines a special property of symbolic sequences - an Order.
The order is a sequence of natural numbers obtained from the original symbolic sequence by replacing each
of its elements with a natural number corresponding to the index of this element in the alphabet
sorted by the appearance of the elements in the original sequence [1, 2, 3].

The concept of an Order can be conveniently demonstrated using an example:


Let's assume there is a symbolic sequence `INTELLIGENCE IS THE ABILITY TO ADAPT TO CHANGE`

Find and enumirate the first appearance of each element

| I | N | T | E | L | L | I | G | E | N | C | E | &nbsp;&nbsp;  | I | S |  &nbsp;&nbsp;  | T | H | E |  &nbsp;&nbsp;  | A | B | I | L | I | T | Y |  &nbsp;&nbsp;  | T | O |  &nbsp;&nbsp;  | A | D | A | P | T |  &nbsp;&nbsp;  | T | O |  &nbsp;&nbsp;  | C | H | A | N | G | E |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2 | 3 | 4 | 5 |   |   | 6 |   |   | 7 |   | 8 |   | 9 |   |   | 10 |   |   | 11 | 12 |   |   |   |   | 13 |   |   | 14 |   |   | 15 |   | 16 |   |   |   |   |   |   |   |   |   |   |  |

The alphabet for the sequence would be sequence of unique elements:

| I | N | T | E | L | G | C |   | S | H  | A  | B  | Y  | O  | D  | P  |
|---|---|---|---|---|---|---|---|---|----|----|----|----|----|----|----|
| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |


Determine the order of the sequence by replacing each element of the sequence with its corresponding alphabet index


| I | N | T | E | L | L | I | G | E | N | C | E | &nbsp;&nbsp;  | I | S |  &nbsp;&nbsp;  | T | H | E |  &nbsp;&nbsp;  | A | B | I | L | I | T | Y |  &nbsp;&nbsp;  | T | O |  &nbsp;&nbsp;  | A | D | A | P | T |  &nbsp;&nbsp;  | T | O |  &nbsp;&nbsp;  | C | H | A | N | G | E |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2 | 3 | 4 | 5 | 5 | 1 | 6 | 4 | 2 | 7 | 4 | 8 | 1 | 9 | 8 | 3 | 10 | 4 | 8 | 11 | 12 | 1 | 5 | 1 | 3 | 13 | 8 | 3 | 14 | 8 | 11 | 15 | 11 | 16 | 3 | 8 | 3 | 14 | 8 | 7 | 10 | 11 | 2 | 6 | 4 |

The order of symbolic sequence `INTELLIGENCE IS THE ABILITY TO ADAPT TO CHANGE` is

| 1 | 2 | 3 | 4 | 5 | 5 | 1 | 6 | 4 | 2 | 7 | 4 | 8 | 1 | 9 | 8 | 3 | 10 | 4 | 8 | 11 | 12 | 1 | 5 | 1 | 3 | 13 | 8 | 3 | 14 | 8 | 11 | 15 | 11 | 16 | 3 | 8 | 3 | 14 | 8 | 7 | 10 | 11 | 2 | 6 | 4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|



Despite the triviality of the concept Order, it allows us to separate the elements and composition of a sequence and to define the compositional equivalence of different sequences.

Example of sequences with equals orders:

```pyodide exec="on" install="foapy,numpy"
import foapy
import numpy as np

seqA = list("INTELLIGENCE IS THE ABILITY TO ADAPT TO CHANGE")
seqB = list("1N73LL1G3NC321527H324B1L17Y27024D4P72702CH4NG3")
orderA = foapy.order(seqA)
orderB = foapy.order(seqB)
print("SeqA and SeqB orders are equals -", np.all(orderA == orderB))
print("Order =", orderA)
```

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

# References:

1. Curtis Cooper and Robert E. Kennedy. 1992. Patterns, automata, and Stirling numbers of the second kind. Math. Comput. Educ. 26, 2 (Spring 1992), 120–124.
2. Gumenjuk A., Kostyshin A., Simonova S. An approach to the research of the structure of linguistic and musical texts. Glottometrics. 2002. № 3. P. 61–89.
3. (In russian) V.I. Arnold, Complexity of finite sequences of zeros and ones and geometry of finite function spaces: el. print, 2005. http://mms.mathnet.ru/meetings/2005/arnold.pdf
