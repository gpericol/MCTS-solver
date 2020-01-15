import random
from .node import Node
from .calculator import Calculator
from .grammar import Grammar
from .const import *
import sys
import time

class MCTS:
    def __init__(self, op1, op2, variables, constants, dataset):
        self.op1 = op1
        self.op2 = op2
        self.variables =  variables
        self.constants =  constants
        self.dataset = dataset

        self.root = Node("U")
        self.best = None

        self.timers = {
            "sel": 0,
            "exp": 0,
            "sim": 0,
            "bkp": 0
        }

    def get_tree(self, node = None):
        if node == None:
            node = self.root
        
        values = {}
        values['state'] = node.grammar
        values['n'] = node.n
        values['w'] = node.w
        values['uct'] = node.uct()
        values['children'] = []
        for c in node.children:
            values["children"].append(self.get_tree(c))
        
        return values

    def selection(self, node):
        while True:
            if node.is_expanded() == False:
                return node
            
            available_nodes = [n for n in node.children if not n.is_terminal() and not n.is_fully_extended()]
            if len(available_nodes) == 0:
                print(node)
                for c in node.children:
                    print(c)
                
            node = max(available_nodes, key=lambda x: x.uct())

    def expansion(self, node):
        node.expand(self.op1, self.op2, self.variables, self.constants)
        # calculate reward for terminal nodes
        score = 0

        for child in node.children:
            if child.is_terminal():
                score = Calculator.score(self.dataset, child.grammar)
                child.w = score
                if score ==  1:
                    return child
                
                if self.best == None or self.best.w < child.w:
                    self.best = child
                    print(child)
        
        return None
    
    def simulation(self, node):
        grammars = Grammar.generate_nop(node.grammar, self.variables, self.constants, self.op1, self.op2)
        reward = None
        while reward == None:
            reward_grammars = [g for g in grammars if "U" not in g]
            if len(reward_grammars) > 0:
                score = 0
                for reward_grammar in reward_grammars:
                    score += Calculator.score(self.dataset, reward_grammar)
                reward = score / len(reward_grammars)
            else: # no rewards - expand less U
                available_grammars = [g for g in grammars if "U" in g]
                grammar = min(available_grammars, key=lambda x: x.count("U"))
                grammars = Grammar.generate_nop(grammar, self.variables, self.constants, self.op1, self.op2)       
        return reward

    def backpropagation(self, node):
        node.n += 1
        node = node.parent
        while node != None:
            node.n += 1
            score = 0
            total = 0
            extended = 0
            for child in node.children:
                if child.w != sys.maxsize:
                    score += child.w
                    total += 1
                if child.is_terminal() or child.is_fully_extended():
                    extended +=1
            node.w = score / total
            if len(node.children) == extended:
                node._is_fully_extended = True
                node.prune()
            node = node.parent

    def iterate(self, verbose=False):
        t = time.time()
        
        selected_node = self.selection(self.root)
        if verbose:
            print(selected_node)
        
        self.timers["sel"] += time.time() - t

        t = time.time()

        solution = self.expansion(selected_node)
        if solution:
            print(solution)
            print(self.timers)
            return True

        self.timers["exp"] += time.time() - t

        t = time.time()
        
        available_nodes = [n for n in selected_node.children if not n.is_terminal()]
        # syntax limit reached -> just backpropagate from a random child
        if len(available_nodes) == 0:
            #print(f"Fully Extended: {selected_node}")
            selected_node._is_fully_extended = True
            simulation_node = random.choice(selected_node.children)
        else:
            simulation_node = random.choice(available_nodes)
            simulation_node.w = self.simulation(simulation_node)
        
        self.timers["sim"] += time.time() - t

        t = time.time()
        
        self.backpropagation(simulation_node)
        
        self.timers["bkp"] += time.time() - t

        return False