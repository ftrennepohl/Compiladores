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
        tape = []
        st = SymbolTable()
        with open(path, 'r') as file:
            for line_idx, line in enumerate(file):
                current_state = 'S'
                character_buffer = ''
                for symbol_idx, symbol in enumerate(line):
                    if (symbol == ' ' or symbol == '\n') and current_state is not None: # se for separador e estado for final adiciona na TS
                        if self.afd.states[current_state].final:
                            st.table.append(Token(line_idx + 1, current_state, character_buffer))
                            tape.append(character_buffer)
                            current_state = 'S'
                            character_buffer = ''
                            continue
                    elif symbol_idx == len(line)-1: # gambiarra sinistra pq nao tem como detectar final de arquivo
                        character_buffer += symbol
                        current_state = self.goToNextState(self.afd, current_state, symbol)
                        if current_state is not None:
                            if self.afd.states[current_state].final:
                                st.table.append(Token(line_idx, current_state, character_buffer))
                                tape.append(character_buffer)
                                current_state = 'S'
                                character_buffer = ''
                                continue
                    current_state = self.goToNextState(self.afd, current_state, symbol)
                    if(current_state is None):
                        continue
                    character_buffer += symbol
        st.print()
        print(tape)
        
lex = LexicalAnalyzer(AFD('input.txt'))
lex.createSymbolTable('input2.txt')
