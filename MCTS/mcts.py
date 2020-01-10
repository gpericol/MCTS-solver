import random
from .node import Node
from .calculator import Calculator
from .const import *
import sys

class MCTS:
    def __init__(self, op1, op2, variables, dataset):
        self.op1 = op1
        self.op2 = op2
        self.variables =  variables
        self.dataset = dataset

        self.root = Node("U")
        self.best = None

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
            
            available_nodes = [n for n in node.children if not n.is_terminal()]
            node = max(available_nodes, key=lambda x: x.uct())

    def expansion(self, node):
        node.expand(self.op1, self.op2, self.variables)

    def simulation(self, node):
        self.expansion(node)
        reward = None
        
        while reward == None:
            reward_nodes = [n for n in node.children if n.is_terminal()]
            if len(reward_nodes) > 0:
                score = 0
                for n in reward_nodes:
                    score += Calculator.score(self.dataset, n.grammar)
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
                if child.is_terminal() and child.w == sys.maxsize:
                    child.w = Calculator.score(self.dataset, child.grammar)
                if child.w != sys.maxsize:
                    score += child.w
                    total += 1
            node.w = score / total
            node = node.parent

    def find_best_solution(self, node):
        if node.is_terminal():
            return node

        selected = None

        for child in node.children:
            local = self.find_best_solution(child)
            if local != None:
                if selected == None:
                    selected = local
                else:
                    if local.w > selected.w:
                        selected = local
        
        return selected

    def iterate(self):
        selected_node = self.selection(self.root)
        self.expansion(selected_node)
        available_nodes = [n for n in selected_node.children if not n.is_terminal()]
        simulation_node = random.choice(available_nodes)
        simulation_node.w = self.simulation(simulation_node)
        simulation_node.prune()
        self.backpropagation(simulation_node)
        best_node = self.find_best_solution(self.root)
        
        if best_node.w == 1:
            print(best_node)
            return True
        return False