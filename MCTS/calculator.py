from collections import deque
from .const import *
from .score import Score

class Calculator():
    @staticmethod
    def _calc(values, expression, constants={}):
        stack = deque() 
        for c in expression:
            # variables
            if ord(c) in range(ord('a'), ord('z')):
                stack.append(values[c])
            # constants
            if ord(c) in range(ord('A'), ord('Z')):
                stack.append(constants[c])
            # op1
            elif c == '!':
                value_1 = stack.pop()
                stack.append(-value_1)
            elif c == '~':
                value_1 = stack.pop()
                stack.append(~value_1)
            elif c == '#':
                value_1 = stack.pop()
                stack.append(
                    ((value_1 << 56) & 0xFF00000000000000) |
                    ((value_1 << 40) & 0x00FF000000000000) |
                    ((value_1 << 24) & 0x0000FF0000000000) |
                    ((value_1 <<  8) & 0x000000FF00000000) |
                    ((value_1 >>  8) & 0x00000000FF000000) |
                    ((value_1 >> 24) & 0x0000000000FF0000) |
                    ((value_1 >> 40) & 0x000000000000FF00) |
                    ((value_1 >> 56) & 0x00000000000000FF)) 
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