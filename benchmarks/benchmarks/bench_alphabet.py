import numpy

from foapy.alphabet import alphabet


class TimeSuite:
    """
    An example benchmark that times the performance of various kinds
    of iterating over dictionaries in Python.
    """

    def setup(self):
        self.xxs = numpy.random.rand(5)
        self.xs = numpy.random.rand(50)
        self.s = numpy.random.rand(500)
        self.m = numpy.random.rand(5000)
        self.large = numpy.random.rand(50000)
        self.xl = numpy.random.rand(500000)

    def time_alphabet_xxs(self):
        alphabet(self.xxs)

    def time_alphabet_xs(self):
        alphabet(self.xs)

    def time_alphabet_s(self):
        alphabet(self.s)

    def time_alphabet_m(self):
        alphabet(self.m)

    def time_alphabet_l(self):
        alphabet(self.large)

    def time_alphabet_xl(self):
        alphabet(self.xl)


class MemSuite:
    def setup(self):
        self.xxs = numpy.random.rand(5)
        self.xs = numpy.random.rand(50)
        self.s = numpy.random.rand(500)
        self.m = numpy.random.rand(5000)
        self.large = numpy.random.rand(50000)
        self.xl = numpy.random.rand(500000)

    def mem_alphabet_xxs(self):
        return alphabet(self.xxs)

    def mem_alphabet_xs(self):
        return alphabet(self.xs)

    def mem_alphabet_s(self):
        return alphabet(self.s)

    def mem_alphabet_m(self):
        return alphabet(self.m)

    def mem_alphabet_l(self):
        return alphabet(self.large)

    def mem_alphabet_xl(self):
        return alphabet(self.xl)

    def peakmem_alphabet_xxs(self):
        return alphabet(self.xxs)

    def peakmem_alphabet_xs(self):
        return alphabet(self.xs)

    def peakmem_alphabet_s(self):
        return alphabet(self.s)

    def peakmem_alphabet_m(self):
        return alphabet(self.m)

    def peakmem_alphabet_l(self):
        return alphabet(self.large)

    def peakmem_alphabet_xl(self):
        return alphabet(self.xl)
