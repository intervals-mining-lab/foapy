# Sequence as a whole object

Symbol sequences are a common model in theoretical and applied science.
This prevalence is since almost any object of study can be represented as a sequence of elements or events.

However, if we set aside our knowledge of the essence of the elements in a specific case and
consider the sequence itself as a separate object of study, then it turns out that methods used
to study them are almost exclusively statistical.
With the only exception being methods for comparison / alignment of two or more sequences
(for example, the Levenshtein distance).

None of these methods describe a sequence as a holistic object.
The Levenshtein distance requires another sequence to compare with the original one, which makes
the measures of this approach "relative". The probabilistic approach decomposes the sequence into
elements and calculates their probabilities (frequencies). Thus, the sequence is replaced, as an object of study,
by a probability distribution. In turn, a specific probability distribution corresponds to an infinite
number of sequences with a ratio of elements "close" to the one in the original sequence.
Moments, conditional probabilities, Shannon entropy, and Markov chains allow us to more accurately
model the object under study, but they still essentially rely on the idea of decomposing a sequence
into independent elements, ignoring the sequence as a holistic object. Practically all existing approaches
to the study and description of symbolic sequences originate from the set-theoretic approach.

Formal order analysis is based on the belief that a symbolic sequence can be considered as a holistic object
with emergent properties, which corresponds to systems thinking. In addition to the distribution
of elements this method studies arrangement of its components - the internal structure (pattern) of the sequence,
which determines its uniqueness among others, including those consisting of the same set of elements.
