import re
import itertools
from prettytable import PrettyTable as pt

class State:
    iterator = itertools.count()
    
    def __init__(self, id=None) -> None:
        self.id = id if id is not None else next(State.iterator)
        self.transitions = {}
        self.final = False

    def addTransition(self, symbol, state):
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(state)

    def printTransitions(self):
        for symbol, states in self.transitions.items():
            state_ids = [state.id for state in states]
            print(f"{symbol} -> {state_ids}")

    def isFinal(self):
        return(self.final)

class AFND:
    def __init__(self) -> None:
        self.states = {}
        self.alphabet = set()
        self.initial_state = self.addState(State('S'))

    def addState(self, state):
        self.states[state.id] = state
        return state

    def getState(self, id):
        return self.states.get(id, None)

    def printStates(self):
        for state in self.states.values():
            print(f"State {state.id}:")
            state.printTransitions()

    def fromFile(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        grammar_pattern = re.compile(r'<(\w+)> ::= (.+)')

        for line in lines:
            line = line.strip()
            if '::=' in line:
                match = grammar_pattern.match(line)
                if match:
                    left_side = match.group(1)
                    right_side = match.group(2).split('|')
                    for production in right_side:
                        self.addProduction(left_side, production.strip())
            else:
                self.addToken(line)
    
    def addProduction(self, left, production):
        #não terminal que será adicionada como alvo
        goal_grammar = ''
        #verifica se o estado é final
        final_pattern = re.compile(r'&')
        is_final = final_pattern.findall(production)
        #cria o estado, caso não exista
        if left not in self.states:
            self.states[left] = State(left)
        current_state = self.states[left]

        #procura o nome do não terminal
        nt_pattern = re.compile(r'<(.*?)>')
        matches = nt_pattern.findall(production)

        #verifica se não é estado final, se for, só muda para final
        if not is_final:
            goal_grammar = matches[0]
        else:
            self.states[left].final = True

        if goal_grammar not in self.states and goal_grammar != '':
            self.states[goal_grammar] = State(goal_grammar)
        for symbol in production:
            if symbol == '<':
                continue
            if symbol == '>':
                continue
            
            if symbol.islower():
                self.alphabet.add(symbol)
                #new_state_id = next(State.iterator)
                #new_state = State(new_state_id)
                #self.states[new_state_id] = new_state
                #self.states[new_state_id].final = True
                current_state.addTransition(symbol, self.states[goal_grammar])
            else:
                continue

    def addToken(self, token):
        current_state = self.initial_state
        for symbol in token:
            self.alphabet.add(symbol)
            new_state_id = next(State.iterator)
            new_state = State(new_state_id)
            self.states[new_state_id] = new_state
            
            current_state.addTransition(symbol, new_state)
            current_state = new_state
            if symbol == token[-1]:
                current_state.final = True

    def printWithError(self):
        table = pt()
        table.align = 'l'
        header = [symbol for symbol in self.alphabet]
        header.insert(0, 'Est/Simb')
        table.field_names = header
        for state in self.states:
            linha = [str(state) + ' *'] if self.states[state].final else [state]
            for key in self.alphabet:
                if key in self.states[state].transitions:
                    fragmento = ''
                    for x in self.states[state].transitions[key]:
                        if x != self.states[state].transitions[key][-1]: fragmento = fragmento + str(x.id) + ', '
                        else: fragmento = fragmento + str(x.id)
                    linha.append(fragmento)
                else:
                    linha.append('-')
            table.add_row(linha)
        print(table)
        with open("out.txt", "w+") as arq:
            arq.write(str(table))

'''afnd = AFND()
afnd.fromFile('input.txt')
#afnd.printStates()
afnd.printWithError()'''
'''
for state in afnd.states:
    print(str(state) + '->')
    for transition in afnd.states[state].transitions:
        print(transition)
'''