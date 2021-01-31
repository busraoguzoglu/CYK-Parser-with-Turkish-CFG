import numpy as np

class GrammarConverter:
    def __init__(self, CFG):
        with open(CFG, encoding = 'utf-8') as cfg:
            lines = cfg.readlines() # first line is dedicated for list of non-terminals
        CFG = [x.replace(" ->", "").split() for x in lines[1:]]
        CFG = np.unique(np.array(CFG, dtype = object)).tolist()

        self.CFG = CFG
        self.rules = {}
        self.CNF = None

    def convert_grammar(self):
        prods = []

        for r in self.CFG:
            p0 = r[0]
            p1 = r[1:]
            if len(p1) <= 2:
                if p0 not in self.rules.keys():
                    self.rules[p0] = []
                self.rules[p0].append(p1)
            else:
                prods.append([p0] + p1)


        while prods:
            for prod in prods:
                p0 = prod[0]
                p1 = prod[1:]
                for j in range(0, len(p1)-1, 1):
                    query = p1[j:j+2]
                    for key in list(self.rules.keys()):
                        for match in self.rules[key]:
                            if query == match:
                                potential_rule = replace(p1, query, [key])
                                if len(potential_rule) > 2:
                                    prods.append([p0] + potential_rule)
                                    if prod in prods:
                                        prods.remove(prod)
                                elif len(potential_rule) == 2:
                                    if prod in prods:
                                        prods.remove(prod)
                                    if p0 not in list(self.rules.keys()):
                                        self.rules[p0] = []
                                    self.rules[p0].append(potential_rule)
                                else:
                                    'problem'

        CNF = []
        for key in self.rules.keys():
            p0 = [key]
            for p1 in self.rules[key]:
                CNF.append(p0 + p1)
        self.CNF = CNF

        return CNF

def replace(lst, a, b):
    str_l = " ".join(lst)
    str_a = " ".join(a)
    str_b = " ".join(b)
    
    str_l = str_l.replace(str_a, str_b)
    return str_l.split()