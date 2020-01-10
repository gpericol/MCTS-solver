from collections import deque
from .const import *
from .score import Score

class Calculator():
    @staticmethod
    def _calc(values, expression):
        stack = deque() 
        for c in expression:
            if ord(c) in range(ord('a'), ord('z')):
                stack.append(values[c])
            # op1
            elif c == '!':
                value_1 = stack.pop()
                stack.append(-value_1)
            elif c == '~':
                value_1 = stack.pop()
                stack.append(~value_1)
            # op2
            elif c == '+':
                value_2 = stack.pop() 
                value_1 = stack.pop()
                stack.append(value_1 + value_2)
            elif c == '-':
                value_2 = stack.pop() 
                value_1 = stack.pop()
                stack.append(value_1 - value_2)
            elif c == '*':
                value_2 = stack.pop() 
                value_1 = stack.pop()
                stack.append(value_1 * value_2)
            elif c == '&':
                value_2 = stack.pop() 
                value_1 = stack.pop()
                stack.append(value_1 & value_2)
            elif c == '|':
                value_2 = stack.pop() 
                value_1 = stack.pop()
                stack.append(value_1 | value_2)
            elif c == '^':
                value_2 = stack.pop() 
                value_1 = stack.pop()
                stack.append(value_1 ^ value_2)
            
        return stack.pop()
    
    @staticmethod
    def score(dataset, expression):
        distances = []
        for data in dataset:
            result = Calculator._calc(data, expression)
            distances.append(Score.distance_metric(data['result'], result, BIT_SIZE))
        return sum(distances) / len(distances) 