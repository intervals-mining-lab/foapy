---
hide:
  - toc
---
# Geometric Mean as Alternative to Probability

At first glance, introducing the concept of [intervals](interval_as_a_basic_information_unit.md) may seem like an unnecessary complication.
After all, if the ultimate goal is to estimate the probability of a symbol, there are much simpler methods - counting the frequency of occurrence of a symbol relative to the total.

However, this perspective begins to shift when we consider other types of aggregate functions beyond the arithmetic mean.
One particularly insightful example is the geometric mean of intervals.
While the arithmetic mean smooths out the "structure" of the data and bring us back to probability
(since the average interval between identical symbols is simply the inverse of their probability),
the geometric mean responds to the diversity of intervals in a fundamentally different way.

If the intervals between repeated elements are uniform, the geometric mean and the arithmetic mean will be the same.
But as the intervals become more irregular — because symbols appear in bursts or clusters — [the geometric mean begins
to diverge from the arithmetic mean](https://en.wikipedia.org/wiki/AM%E2%80%93GM_inequality).
This makes it a sensitive indicator of the order within the sequence, not just the frequency.

![AM-GM inequality visual proof](https://upload.wikimedia.org/wikipedia/commons/d/d9/AM_GM_inequality_visual_proof.svg)

*Visual proof of the arithmetic mean - geometric mean inequality. Source: [wikipedia.org](https://en.wikipedia.org/wiki/File:AM_GM_inequality_visual_proof.svg)*

Building on this idea, Former Order Analysis explored the potential of reinterpreting classical probabilistic and information-theoretic measures in terms of these intervals.
Instead of relying solely on symbol frequencies, it reformulated the measures using the geometric mean instead of probability (arithmetic mean).

\begin{array}{|c|c|}
\hline
Entropy & Average \ remoteness \\
\hline
H= - \sum_{j=1}^{m}{p_j \log_2{p_j}} = \frac {1} {n} * \sum_{j=1}^{m}{n_j \log_2 \Delta_{a_j}} & g = \frac{1}{n} * \sum_{j=1}^{m}{n_j \log_2{\Delta_{g_j}}} = \frac{1}{n} * \sum_{j=1}^{m}{\sum_{i=1}^{n_j} \log_2 \Delta_{ij}} \\
\hline
\end{array}

*Example of Shennon's Entropy analog - Average remoteness. Where $n$ - seqeunce length, $m$ - alphabet power, $n_j$ - count of element $j$-th, $\Delta_{a_j}$ - average mean of intervals for element $j$-th, $\Delta_{g_j}$ - geometric mean of intervals for element $j$-th, $\Delta_{ij}$ - $i$-th interval for element $j$-thg*

These measures are fine-grained and sensitive to the temporal or spatial order of elements in a sequence.
Allows us to distinguish between sequences of symbols that may have identical probability distributions
but differ in the way those symbols are arranged - insight that traditional measures completely miss.
