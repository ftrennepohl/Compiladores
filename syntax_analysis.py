import pandas as pd
from lexical_analyzer import LexicalAnalyzer
from symbol_table import *
from afd import AFD



tokens_values = []

def syntactic_analyzer(output_tape, parsing_table_path, symbol_table:SymbolTable):
    parsing_table = pd.read_csv(parsing_table_path, index_col=0)
    tokens = [token for token in output_tape]
    tokens.append('$')
    stack = [0]  # Initial stack with state 0
    idx = 0  # Index for the current token
    token = tokens[idx] if idx < len(tokens) else None
    id_stack = []
    result_stack = []
    
    while True:

        print(stack, token)

        current_state = stack[-1]
        try:
            for entry in symbol_table.table:
                if token == entry.identificador and (entry.rotulo == 'id' or entry.rotulo == 'const'):
                    action = str(parsing_table.at[current_state, entry.rotulo]) if token else None
                    break
            else:
                action = str(parsing_table.at[current_state, token]) if token else None
        except KeyError:
            print("Token rejeitado")

        if action is None:
            return False, f"Error: Invalid syntax"
        
        if action.startswith('s'):
            # Shift operation
            new_state = int(action[1:])
            stack.append(new_state)
            idx += 1
            token = tokens[idx] if idx < len(tokens) else None
        elif action.startswith('r'):
            # Reduce operation
            rule = int(action[1:])
            # Define reduction rules based on the grammar
            if rule == 1:
                stack = stack[:-3]  # S -> BEGIN A END
                try:
                    goto_state = parsing_table.at[stack[-1], 'S']
                except KeyError:
                    print("Erro na produção S -> BEGIN A END", stack, token)
                stack.append(int(goto_state))
            elif rule == 2:
                stack = stack[:-3]  # A -> BEGIN A END
                try:
                    goto_state = parsing_table.at[stack[-1], 'A']
                except KeyError:
                    print("Erro na produção A -> BEGIN A END", stack, token)
                stack.append(int(goto_state))
            elif rule == 3:
                stack = stack[:-6]  # A -> IF B THEN A ENDIF A
                print(stack[-1])
                try:
                    goto_state = parsing_table.at[stack[-1], 'A']
                except KeyError:
                    print("Erro na produção A -> IF B THEN A ENDIF A", stack, token)
                stack.append(int(goto_state))
            elif rule == 4:
                stack = stack[:-5]  # A -> LET C = D A
                try:
                    goto_state = parsing_table.at[stack[-1], 'A']
                except KeyError:
                    print("Erro na produção A -> LET C = D A", stack, token)
                stack.append(int(goto_state))
                print(id_stack[-1], result_stack[-1])
                if result_stack[-1] == 'TRUE' or result_stack[-1] == 'FALSE':
                    var_type = 'bool'
                    size = 1
                else:
                    var_type = 'int'
                    size = 4
                symbol_table.setValue(id_stack[-1], result_stack[-1])
                symbol_table.setType(id_stack[-1], var_type)
                symbol_table.setSize(id_stack[-1], size)
                id_stack.pop()
                result_stack.pop()
            elif rule == 5:
                # A -> ε (epsilon)
                try:
                    goto_state = parsing_table.at[stack[-1], 'A']
                except KeyError:
                    print("Erro na produção A -> ε", stack, token)
                stack.append(int(goto_state))
            elif rule == 6:
                stack = stack[:-3]  # B -> D == D
                try:
                    goto_state = parsing_table.at[stack[-1], 'B']
                except KeyError:
                    print("Erro na produção B -> D == D", stack, token)
                stack.append(int(goto_state))
            elif rule == 7:
                stack = stack[:-3]  # B -> D != D
                try:
                    goto_state = parsing_table.at[stack[-1], 'B']
                except KeyError:
                    print("Erro na produção B -> D != D", stack, token)
                stack.append(int(goto_state))
            elif rule == 8:
                stack.pop()  # C -> id
                id_stack.append(tokens[idx-1])
                try:
                    goto_state = parsing_table.at[stack[-1], 'C']
                except KeyError:
                    print("Erro na produção C -> id", stack, token)
                stack.append(int(goto_state))
            elif rule in [9, 10]:
                if (len(tokens_values) > 0): symbol_table.setValue(tokens[idx-1], tokens_values.pop())
                stack.pop()  # D -> id | const
                result_stack.append(tokens[idx-1])
                try:
                    goto_state = parsing_table.at[stack[-1], 'D']
                except KeyError:
                    print("Erro na produção D -> id | const", stack, token)
                stack.append(int(goto_state))
                if result_stack[-1] == 'TRUE' or result_stack[-1] == 'FALSE':
                    var_type = 'bool'
                    size = 1
                else:
                    var_type = 'int'
                    size = 4
                symbol_table.setType(tokens[idx-1], var_type)
                symbol_table.setSize(tokens[idx-1], size)

        elif action == 'acc':
            return True, "Success: Input is syntactically correct"
        else:
            return False, "Error: Unrecognized action in parsing table"


def convertTapeOutput(output_tape, symbol_table): # prepara a fita de saída para usar com o analisador sintatico
    aux_tape = [token for token in output_tape]
    for idx, token in enumerate(output_tape):
        for entry in symbol_table.table:
            if token == entry.identificador and (entry.rotulo == 'id' or entry.rotulo == 'const'): 
                aux_tape[idx] = entry.rotulo
                tokens_values.append(token)
    return aux_tape

lex = LexicalAnalyzer(AFD('input.txt'))

lex.createSymbolTable('input3.txt')


print(tokens_values)

print(input)

sa = syntactic_analyzer(lex.tape, 'parsing_table.csv', lex.symbol_table)
print(sa)
print(lex.symbol_table.table)