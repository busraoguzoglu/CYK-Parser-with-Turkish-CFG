from grammar_converter import *

# Şimdilik our parser değil
# Rob un parseri üzerinden
# Devam ediyoruz..


class Node:
    """
    Used for storing information about a non-terminal symbol. A node can have a maximum of two
    children because of the CNF of the grammar.
    It is possible though that there are multiple parses of a sentence. In this case information
    about an alternative child is stored in self.child1 or self.child2 (the parser will decide
    where according to the ambiguous rule).
    Either child1 is a terminal symbol passed as string, or both children are Nodes.
    """

    def __init__(self, symbol, child1, child2=None):
        self.symbol = symbol
        self.child1 = child1
        self.child2 = child2

    """
    def __repr__(self):

        #:return: the string representation of a Node object.

        return self.symbol
    """


class Parser:
    """
    A CYK parser which is able to parse any grammar in CNF. The grammar can be read from a file or
    passed as a string. It either returns a string representation of the parse tree(s) or prints it
    to standard out.
    """

    def __init__(self, grammar_file):
        """
        Creates a new parser object which will read in the grammar and transform it into CNF and
        then parse the given sentence with that grammar.
        :param grammar: the file path to the grammar/the string repr. of the grammar to read in
        :param sentence: the file path to the sentence/the string repr. of the sentence to read in
        """
        self.parse_table = None
        gc = grammar_converter(grammar_file)
        self.grammar = gc.convert_grammar()

    def parse(self, input_sentence):
        """
        Does the actual parsing according to the CYK algorithm. The parse table is stored in
        self.parse_table.
        """

        # At first, we need to split the sentence to tokens
        tokenized_sentence = input_sentence.split()

        # Get how many tokens there are
        length = len(tokenized_sentence)

        # self.parse_table[y][x] is the list of nodes in the x+1 cell of y+1 row in the table.
        # That cell covers the word below it and y more words after.

        # As an example: [S [NP 'astronomers'] [VP [V 'saw'] [NP [NP 'stars'] [PP [P 'with'] [NP 'telescope']]]]]
        # Burada tüm kelimeler için '[]' açıyor.
        self.parse_table = [[[] for x in range(length - y)] for y in range(length)]

        for i, word in enumerate(tokenized_sentence):
            # Find out which non terminals can generate the terminals in the input string
            # and put them into the parse table. One terminal could be generated by multiple
            # non terminals, therefore the parse table will contain a list of non terminals.
            for rule in self.grammar:
                # Terminal kısmı baktığımız kelime ise, tüm kelimeler için check ediyoruz.
                if f"{word}" == rule[1]:
                    # i. kelime için olan [] kısmına rule'u append ediyoruz.
                    self.parse_table[0][i].append(Node(rule[0], word))

        # Bu kısmı pek anlamadım..
        for words_to_consider in range(2, length + 1):
            for starting_cell in range(0, length - words_to_consider + 1):
                for left_size in range(1, words_to_consider):
                    right_size = words_to_consider - left_size

                    left_cell = self.parse_table[left_size - 1][starting_cell]
                    right_cell = self.parse_table[right_size - 1][starting_cell + left_size]

                    for rule in self.grammar:
                        left_nodes = [n for n in left_cell if n.symbol == rule[1]]
                        if left_nodes:
                            right_nodes = [n for n in right_cell if n.symbol == rule[2]]
                            self.parse_table[words_to_consider - 1][starting_cell].extend(
                                [Node(rule[0], left, right) for left in left_nodes for right in right_nodes]
                            )

    def print_tree(self, output=True):
        """
        Print the parse tree starting with the start symbol. Alternatively it returns the string
        representation of the tree(s) instead of printing it.
        """
        start_symbol = self.grammar[0][0]
        print(start_symbol)

        final_nodes = []
        #final_nodes = [n for n in self.parse_table[-1][0] if n.symbol == start_symbol]

        for node in self.parse_table[-1][0]:
            if node.symbol == start_symbol:
                final_nodes.append(node)
                #print(node.symbol)

        # Meaning it could find a parse tree
        if final_nodes:
            if output:
                print("The given sentence is contained in the language produced by the given grammar!")
                print("\nPossible parse(s):")
                trees = [generate_tree(node) for node in final_nodes]
                for tree in trees:
                    print(tree)
                return trees
        else:
            print("The given sentence is not contained in the language produced by the given grammar!")


def generate_tree(node):
    """
    Generates the string representation of the parse tree.
    :param node: the root node.
    :return: the parse tree in string form.
    """
    if node.child2 is None:
        return f"[{node.symbol} '{node.child1}']"
    return f"[{node.symbol} {generate_tree(node.child1)} {generate_tree(node.child2)}]"

def main():

    CYK = Parser('Grammar/turkish_grammar_for_rob2.txt')

    print(CYK.grammar)

    CYK.parse('dün ben arkadaşıma hediye aldım')
    CYK.print_tree()

    #CYK.parse('ağır romanları yediler')
    #CYK.print_tree()

if __name__ == '__main__':
    main()