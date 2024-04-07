import numpy

from foapy.alphabet import alphabet


class TimeSuite:
    """
    An example benchmark that times the performance of various kinds
    of iterating over dictionaries in Python.
    """

    def setup(self):
        self.s10_0 = numpy.random.rand(5)
        self.s10_1 = numpy.random.rand(50)
        self.s10_2 = numpy.random.rand(500)
        self.s10_3 = numpy.random.rand(5000)
        self.s10_4 = numpy.random.rand(50000)
        self.s10_5 = numpy.random.rand(500000)
        self.s10_6 = numpy.random.rand(5000000)
        self.s10_7 = numpy.random.rand(50000000)

    def time_alphabet_s10_0(self):
        alphabet(self.s10_0)

    def time_alphabet_s10_1(self):
        alphabet(self.s10_1)

    def time_alphabet_s10_2(self):
        alphabet(self.s10_2)

    def time_alphabet_s10_3(self):
        alphabet(self.s10_3)

    def time_alphabet_s10_4(self):
        alphabet(self.s10_4)

    def time_alphabet_s10_5(self):
        alphabet(self.s10_5)

    def time_alphabet_s10_6(self):
        alphabet(self.s10_6)

    def time_alphabet_s10_7(self):
        alphabet(self.s10_7)


class MemSuite:
    def setup(self):
        self.s10_0 = numpy.random.rand(5)
        self.s10_1 = numpy.random.rand(50)
        self.s10_2 = numpy.random.rand(500)
        self.s10_3 = numpy.random.rand(5000)
        self.s10_4 = numpy.random.rand(50000)
        self.s10_5 = numpy.random.rand(500000)
        self.s10_6 = numpy.random.rand(5000000)
        self.s10_7 = numpy.random.rand(50000000)

    def mem_alphabet_s10_0(self):
        return alphabet(self.s10_0)

    def mem_alphabet_s10_1(self):
        return alphabet(self.s10_1)

    def mem_alphabet_s10_2(self):
        return alphabet(self.s10_2)

    def mem_alphabet_s10_3(self):
        return alphabet(self.s10_3)

    def mem_alphabet_s10_4(self):
        return alphabet(self.s10_4)

    def mem_alphabet_s10_5(self):
        return alphabet(self.s10_5)

    def mem_alphabet_s10_6(self):
        return alphabet(self.s10_6)

    def mem_alphabet_s10_7(self):
        return alphabet(self.s10_7)

    def peakmem_alphabet_s10_0(self):
        return alphabet(self.s10_0)

    def peakmem_alphabet_s10_1(self):
        return alphabet(self.s10_1)

    def peakmem_alphabet_s10_2(self):
        return alphabet(self.s10_2)

    def peakmem_alphabet_s10_3(self):
        return alphabet(self.s10_3)

    def peakmem_alphabet_s10_4(self):
        return alphabet(self.s10_4)

    def peakmem_alphabet_s10_5(self):
        return alphabet(self.s10_5)

    def peakmem_alphabet_s10_6(self):
        return alphabet(self.s10_6)

    def peakmem_alphabet_s10_7(self):
        return alphabet(self.s10_7)
