from itertools import product
import random

class Grammar:
    @staticmethod
    def generate(grammar, variables, constants, op1, op2):
        grammars = []
        for i in range(len(grammar)):
            if grammar[i] == "U":
                before_grammar = grammar[:i]
                after_grammar = grammar[(i+1):]
                for variable in variables:
                    new_grammar = before_grammar + variable + after_grammar
                    grammars.append(new_grammar)
                for constant in constants:
                    if constant not in grammar:
                        new_grammar = before_grammar + constant + after_grammar
                        grammars.append(new_grammar)
                for op in op1:
                    if len(after_grammar) > 0 and op == after_grammar[0]:
                        continue
                    new_grammar = before_grammar + "U" + op + after_grammar
                    grammars.append(new_grammar)
                for op in op2:
                    new_grammar = before_grammar + "UU" + op + after_grammar
                    grammars.append(new_grammar)
        return grammars     


    @staticmethod
    def generate_nop(grammar, variables, constants, op1, op2):
        grammars = []
        elements = []
        elements += variables
        elements += constants
        
        tot = grammar.count("U")

        for j in range(5):
            for i in range(tot):
                grammar = grammar.replace("U", random.choice(elements), 1)

        grammars.append(grammar)

        return grammars     