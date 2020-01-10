from random import seed
from random import randint
import sys

class Oracle:
    @staticmethod
    def phi(a, b, c):
        return ( a - b ) * a + b

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