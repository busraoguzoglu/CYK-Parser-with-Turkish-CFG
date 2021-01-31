"""
Usage:
    gc = GrammarConverter('grammar_file.txt')
    print(gc.CFG)
    CNF = gc.convert_grammar()
    print(CNF)
"""

class GrammarConverter:

    def __init__(self, grammar_file):
        with open(grammar_file, encoding = 'utf-8') as cfg:
            lines = cfg.readlines() # first line is dedicated for list of non-terminals
            
        self.CFG = [x.replace(" ->", "").split() for x in lines[1:]]
        self.dict_of_rules = {}
        self.non_terminals = lines[0].rstrip().strip().split()


    def add_rule(self, rule):
        if rule[0] not in self.dict_of_rules:
            self.dict_of_rules[rule[0]] = []
        self.dict_of_rules[rule[0]].append(rule[1:])
        # Burası dogru geliyor.
        #print(self.dict_of_rules)

    def convert_grammar(self):
        grammar = self.CFG
        unit_productions = []
        result = []
        idx = 0

        for rule in grammar:
            new_rules = []
            if len(rule) == 2 and rule[1] in self.non_terminals:  #  
                # This is VP -> V form
                unit_productions.append(rule)
                self.add_rule(rule)
                #print(self.dict_of_rules)

                # Burda append etmeyince terminalleri kaybediyoruz.
                result.append(rule)

                continue
            elif len(rule) > 2:
                # This is S -> PP NP VP ... form, or A -> X a.
                terminals = [(item, i) for i, item in enumerate(rule) if item not in self.non_terminals]
                #print(terminals)
                if terminals:
                    for item in terminals:
                        # Create a new non terminal symbol and replace the terminal symbol with it.
                        # The non terminal symbol derives the replaced terminal symbol.
                        rule[item[1]] = rule[0] + str(idx)
                        new_rules += [rule[0] + str(idx), item[0]]
                    idx += 1
                while len(rule) > 3:
                    new_rules.append([rule[0] + str(idx), rule[1], rule[2]])
                    rule = [rule[0]] + [rule[0] + str(idx)] + rule[3:]
                    idx += 1
            # Adds the modified or unmodified (in case of A -> x i.e.) rules.
            self.add_rule(rule)
            result.append(rule)
            if new_rules:
                result += new_rules
                #print('modfiying rules:', self.dict_of_rules)

        # Handle the unit productions (A -> X)
        while unit_productions:
            rule = unit_productions.pop()
            if rule[1] in self.dict_of_rules:
                #print('true', rule[1])
                # Buraya hiç girmiyor nedense
                for item in self.dict_of_rules[rule[1]]:
                    new_rule = [rule[0]] + item
                    if len(new_rule) > 2 or new_rule[1] not in self.non_terminals:
                        result.append(new_rule)
                    else:
                        unit_productions.append(new_rule)
                    self.add_rule(new_rule)
                    result.append(new_rule)

        return result