import sys
from .const import *
from .grammar import Grammar
import math

class Node(object):
    def  __init__(self, grammar, parent=None):
        # state
        self.grammar = grammar
        
        self.n = 0
        self.w = sys.maxsize

        self._is_terminal = "U" not in grammar
        self._is_fully_extended = False
        self.children = []
        self.parent = parent

    def is_terminal(self):
        return self._is_terminal

    def is_fully_extended(self):
        return self._is_fully_extended

    def is_expanded(self):
        return len(self.children) > 0

    def uct(self):
        # root
        if self.parent == None:
            return sys.maxsize
        
        # never visited
        if self.n == 0:
            return sys.maxsize

        return self.w + UTC_CONST * math.sqrt(math.log(self.parent.n) / self.n)

    def expand(self, op1, op2, variables, constants):
        grammars = Grammar.generate(self.grammar, variables, constants, op1, op2)                
        for grammar in grammars:
            if len(grammar) <= NODE_SYNTAX_LIMIT:
                self.children.append(Node(grammar, self))

    def prune(self):
        for child in self.children:
            child.prune()
            del child
        self.children = []
    
    def __repr__(self):
        return f"{self.grammar} [{self.w}]"
