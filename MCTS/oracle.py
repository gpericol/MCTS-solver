from random import seed
from random import randint
from .calculator import Calculator
import sys

class Oracle:
    @staticmethod
    def phi(a, b, c):
        return ( a + b ) * (c - a)

    @staticmethod
    def dataset(size=10):
        dataset = []
        seed(42)
        for i in range(size):
            a =  randint(0, sys.maxsize)
            b =  randint(0, sys.maxsize)
            c =  randint(0, sys.maxsize)
            dataset.append({'a': a, 'b': b, 'c': c, 'result': Oracle.phi(a, b, c) })
        return dataset

class OracleRPN:
    @staticmethod
    def phi(a):
        A = 11111111111111111111
        B = 12121212121212121212
        C = 31313131313131313131
        #expression = "BaA&#-a|C+"
        expression = "BaA&-a|C+"
        return Calculator._calc({'a': a}, expression, {'A': A, 'B': B, 'C':C})

    @staticmethod
    def dataset(size=10):
        dataset = []
        seed(42)
        for i in range(size):
            a =  randint(0, sys.maxsize)
            dataset.append({'a': a, 'result': OracleRPN.phi(a) })
        return dataset