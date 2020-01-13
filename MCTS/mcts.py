import random
from .node import Node
from .calculator import Calculator
from .const import *
import sys
import time

class MCTS:
    def __init__(self, op1, op2, variables, dataset):
        self.op1 = op1
        self.op2 = op2
        self.variables =  variables
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
            #print(node)
            if node.is_expanded() == False:
                return node
            
            available_nodes = [n for n in node.children if not n.is_terminal()]
            node = max(available_nodes, key=lambda x: x.uct())

    def expansion(self, node):
        node.expand(self.op1, self.op2, self.variables)
        # calculate reward for terminal nodes
        score = 0

        for child in node.children:
            if child.is_terminal():
                score = Calculator.score(self.dataset, child.grammar)
                child.w = score
                if score ==  1:
                    return child
        
        return None

    def simulation(self, node):
        self.expansion(node)
        reward = None
        
        while reward == None:
            reward_nodes = [n for n in node.children if n.is_terminal()]
            if len(reward_nodes) > 0:
                score = 0
                for reward_node in reward_nodes:
                    score += reward_node.w
                reward = score / len(reward_nodes)
            else: # no rewards - expand randomly
                available_nodes = [n for n in node.children if not n.is_terminal()]
                node = min(available_nodes, key=lambda x: len(x.grammar))
                self.expansion(node)        
        return reward

    def backpropagation(self, node):
        node.n += 1
        node = node.parent
        while node != None:
            node.n += 1
            score = 0
            total = 0
            for child in node.children:
                if child.w != sys.maxsize:
                    score += child.w
                    total += 1
            node.w = score / total
            node = node.parent

 
    def iterate(self):
        t = time.time()
        selected_node = self.selection(self.root)
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
        simulation_node = random.choice(available_nodes)
        simulation_node.w = self.simulation(simulation_node)
        simulation_node.prune()
        self.timers["sim"] += time.time() - t

        t = time.time()
        self.backpropagation(simulation_node)
        self.timers["bkp"] += time.time() - t

        return False