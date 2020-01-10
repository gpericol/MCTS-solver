import sys
from .const import *
import math

class Node(object):
    def  __init__(self, grammar, parent=None):
        # state
        self.grammar = grammar
        
        self.n = 0
        self.w = sys.maxsize

        self._is_terminal = "U" not in grammar
        self.children = []
        self.parent = parent

    def is_terminal(self):
        return self._is_terminal

    def is_expanded(self):
        return len(self.children) > 0

    def uct(self):
        # root
        if self.parent == None:
            return sys.maxsize
        
        # never visited
        if self.n == 0:
            return sys.maxsize

        return self.w + C * math.sqrt(math.log(self.parent.n) / self.n)

    def expand(self, op1, op2, variables):
        grammars = []
        for i in range(len(self.grammar)):
            if self.grammar[i] == "U":
                before_grammar = self.grammar[:i]
                after_grammar = self.grammar[(i+1):]
                for variable in variables:
                    new_grammar = before_grammar + variable + after_grammar
                    grammars.append(new_grammar)
                for op in op1:
                    new_grammar = before_grammar + "U" + op + after_grammar
                    grammars.append(new_grammar)
                for op in op2:
                    new_grammar = before_grammar + "UU" + op + after_grammar
                    grammars.append(new_grammar)
                
        for grammar in grammars:
            self.children.append(Node(grammar, self))

    def prune(self):
        for child in self.children:
            child.prune()
            del child
        self.children = []
    
    def __repr__(self):
        return f"{self.grammar} [{self.w}]"
