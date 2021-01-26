import numpy as np
from tabulate import tabulate
from grammar_converter import *

# Class of Node for Binary Tree building
class Node(object):
    def __init__(self, terminal, child1, child2):
        self.terminal = terminal
        self.child1 = child1
        self.child1 = child2

# Class of Production rules
class Production(object):
    def __init__(self, productions = None):
        if productions is None:
            self.productions = []
        else:
            self.productions = productions
            
    def add_production(self, terminal, child1, child2):
        self.productions.append(Node(terminal, child1, child2))

    @property
    def get_prods(self):
        return [p.terminal for p in self.productions ]

# Class of Grammar
class Grammar(object):

    def __init__(self, filename):

        cg = grammar_converter(filename)
        cnf = np.unique(np.array(cg.convert_grammar(), dtype = object)).tolist()

        self.grammar_rules = {}
        self.parse_table = None
        self.length = 0
        self.num_of_trees = 0
        for line in cnf:
            a = line[0]
            b = " ".join(line[1:])

            if b not in self.grammar_rules.keys():
                self.grammar_rules[b] = []
            self.grammar_rules[b].append(a)
        
    def check_rule(self, token):
        if token in self.grammar_rules.keys():
            return self.grammar_rules[token]
        else:
            return None
 
    def parse(self, sentence):
        self.tokens = sentence.split()
        self.length = len(self.tokens)
        self.parse_table = [[Production() for x in range(self.length - y)] for y in range(self.length) ]

        for idx, token in enumerate(self.tokens):
            
            r = self.check_rule(token)
            if r == None:
                raise ValueError("Word " + token + " does not exist in provided grammar.")
            else:
                for w in r: 
                    self.parse_table[0][idx].add_production(w, Node(token, None, None),None)
        
        # CYK Parser
        for l in range(2, self.length + 1):
            for s in range(1, self.length-l + 2):
                for p in range(1, l-1 + 1):
                    pr1 = self.parse_table[p-1][s-1].productions
                    pr2 = self.parse_table[l-p-1][s+p-1].productions
                            
                    for a in pr1:
                        for b in pr2:
                            r = self.check_rule(str(a.terminal) + " " + str(b.terminal))
                                    
                            if r is not None:
                                for w in r:
                                    #print('Applied Rule: ' + str(w) + '[' + str(l) + ',' + str(s) + ']' + ' --> ' + str(a.terminal) + '[' + str(p) + ',' + str(s) + ']' + ' ' + str(b.terminal)+ '[' + str(l-p) + ',' + str(s+p) + ']')
                                    self.parse_table[l-1][s-1].add_production(w,a,b)
                               
        self.num_of_trees = len(self.parse_table[self.length-1][0].get_prods)
        if  self.num_of_trees > 0:
            print('Given sentence is gramatically CORRECT')
            print('Number of possible trees: ' + str(self.num_of_trees))
        else:
            print('Given sentence is gramatically INCORRECT')
        

    # Prints the parsed tabe           
    def print_parsed_table(self):
        lines = [] 
        for row in reversed(self.parse_table):
            l = []
            for p in row:
                l.append(p.get_prods)  # list(set()) operations drop the duplicates
            lines.append(l)
        
        lines.append(self.tokens)
        print('')
        print(tabulate(lines))
        print('')
