from afd import AFD
from symbol_table import SymbolTable, Token

class LexicalAnalyzer:

    def __init__(self, afd) -> None:
        self.afd = afd
        self.afd.printWithError()

    @staticmethod
    def goToNextState(afd:AFD, currentState, symbol):
        return afd.states[currentState].transitions[symbol][0].id if currentState in afd.states.keys() and symbol in afd.states[currentState].transitions.keys() else None

    def createSymbolTable(self, path):
        st = SymbolTable()
        with open(path, 'r') as file:
            recognised_tokens = []
            for line_idx, line in enumerate(file):
                current_state = 'S'
                character_buffer = ''
                for symbol_idx, symbol in enumerate(line):
                    print(current_state)
                    if symbol == ' ' or symbol_idx == '\n': # se for separador e estado for final adiciona na TS
                        if self.afd.states[current_state].final:
                            st.table.append(Token(line_idx, current_state, character_buffer))
                            current_state = 'S'
                            character_buffer = ''
                    current_state = self.goToNextState(self.afd, current_state, symbol)
                    if(current_state is None):
                        continue
                    character_buffer += symbol
        st.print()

lex = LexicalAnalyzer(AFD('input2.txt'))
lex.createSymbolTable('input2.txt')
