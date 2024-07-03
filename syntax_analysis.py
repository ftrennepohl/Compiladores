import pandas as pd
from lexical_analyzer import LexicalAnalyzer
from symbol_table import Token

def syntactic_analyzer(output_tape, parsing_table_path):
    parsing_table = pd.read_csv(parsing_table_path, index_col=0)
    tokens = [token for token in output_tape]
    tokens.append('$')
    stack = [0]  # Initial stack with state 0
    idx = 0  # Index for the current token
    token = tokens[idx] if idx < len(tokens) else None
    
    while True:
        current_state = stack[-1]
        action = str(parsing_table.at[current_state, token]) if token else None
        
        print(stack, token)

        if action is None:
            return False, "Error: Unrecognized token or invalid syntax"
        
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
                goto_state = parsing_table.at[stack[-1], 'S']
                stack.append(int(goto_state))
            elif rule == 2:
                stack = stack[:-3]  # A -> BEGIN A END
                goto_state = parsing_table.at[stack[-1], 'A']
                stack.append(int(goto_state))
            elif rule == 3:
                stack = stack[:-6]  # A -> IF B THEN A ENDIF A
                goto_state = parsing_table.at[stack[-1], 'A']
                stack.append(int(goto_state))
            elif rule == 4:
                stack = stack[:-5]  # A -> LET C = D A
                goto_state = parsing_table.at[stack[-1], 'A']
                stack.append(int(goto_state))
            elif rule == 5:
                # A -> ε (epsilon)
                goto_state = parsing_table.at[stack[-1], 'A']
                stack.append(int(goto_state))
            elif rule == 6:
                stack = stack[:-3]  # B -> D == D
                goto_state = parsing_table.at[stack[-1], 'B']
                stack.append(int(goto_state))
            elif rule == 7:
                stack = stack[:-3]  # B -> D != D
                goto_state = parsing_table.at[stack[-1], 'B']
                stack.append(int(goto_state))
            elif rule == 8:
                stack.pop()  # C -> id
                goto_state = parsing_table.at[stack[-1], 'C']
                stack.append(int(goto_state))
            elif rule in [9, 10]:
                stack.pop()  # D -> id | const
                goto_state = parsing_table.at[stack[-1], 'D']
                stack.append(int(goto_state))
        elif action == 'acc':
            return True, "Success: Input is syntactically correct"
        else:
            return False, "Error: Unrecognized action in parsing table"



def convertTapeOutput(output_tape, symbol_table): # prepara a fita de saída para usar com o analisador sintatico
    aux_tape = [token for token in output_tape]
    for idx, token in enumerate(output_tape):
        for entry in symbol_table:
            if token == entry.identificador and (entry.rotulo == 'id' or entry.rotulo == 'const'): aux_tape[idx] = entry.rotulo
    return aux_tape
