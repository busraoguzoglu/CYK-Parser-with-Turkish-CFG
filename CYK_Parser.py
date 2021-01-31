import numpy as np
from tabulate import tabulate
from grammar_converter import GrammarConverter

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
class CYKParser(object):

    def __init__(self, filename):

        cg = GrammarConverter(filename)
        cnf = np.unique(np.array(cg.convert_grammar(), dtype = object)).tolist()
        """
        with open(filename, encoding = 'utf-8') as cfg:
            lines = cfg.readlines() # first line is dedicated for list of non-terminals
        cnf = [x.replace(" ->", "").split() for x in lines[1:]]
        """
        self.grammar_rules = {}
        self.parse_table = None
        self.length = 0
        self.num_of_trees = 0
        self.sentence = None

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
        self.sentence = sentence
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
                                    self.parse_table[l-1][s-1].add_production(w,a,b)
                               
        self.num_of_trees = len(self.parse_table[self.length-1][0].get_prods)
        if  self.num_of_trees > 0:
            print('Given sentence is gramatically CORRECT')
            print(self.sentence)
            print(self.get_terminals())
        else:
            print('Given sentence is gramatically INCORRECT')

    # Prints the parsed tabe           
    def print_parsed_table(self):
        lines = []

        for r in reversed(self.parse_table):
            l = []
            for p in r:
                tmp_s = []
                prods = p.get_prods
                for item in prods:
                    #s = ''.join([i for i in item if not i.isdigit()]) in case we want to remove digits
                    tmp_s.append(item)
                l.append(np.unique(tmp_s).tolist())  # list(set()) operations drop the duplicates
            lines.append(l)
        lines[-1] = [[item[-1]] for item in lines[-1]]
        
        lines.append(self.tokens)
        print('')
        print(tabulate(lines))
        print('')

    def get_terminals(self):
        terminals = []
        for i in range(len(self.parse_table[0])):
            terminals.append(self.parse_table[0][i].productions[0].terminal)
        return terminals


