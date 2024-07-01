from afd import AFD
from afnd import AFND
from lexical_analyzer import Lexer

afd = AFD('input.txt')  # Convert NFA to DFA

lexer = Lexer(afd)

input_text = "your input text here"
tokens = lexer.tokenize(input_text)

print("Tokens:", tokens)
#afnd.printStates()
#afd.printWithError()
