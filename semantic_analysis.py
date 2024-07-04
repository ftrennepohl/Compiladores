from symbol_table import *
from syntax_analysis import *
from lexical_analyzer import LexicalAnalyzer
from afd import AFD

PATH = 'input3.txt'
AFD_PATH = 'input.txt'

lex = LexicalAnalyzer(AFD(AFD_PATH))

lex.createSymbolTable(PATH)

print(lex.tape)

sa = syntactic_analyzer(lex.tape, 'parsing_table.csv', lex.symbol_table)

class SemanticAnalyzer:

    def __init__(self, symbol_table:SymbolTable) -> None:
        self.symbol_table = symbol_table
        pass

    def analysis(self, output_tape):
        for idx, token in enumerate(output_tape):
            if(token == '=='):
                self.equality(output_tape[idx-1], output_tape[idx+1])
            if(token == '!='):
                self.inequality(output_tape[idx-1], output_tape[idx+1])
            if(token == '='):
                self.attribuition(output_tape[idx-1], output_tape[idx+1])

    def equality(self, a, b):
        for entry in self.symbol_table.table:
            if entry.identificador == a:
                a_type = entry.tipo
                a_value = entry.valor
            if entry.identificador == b:
                b_type = entry.tipo
                b_value = entry.valor
        if a_type != b_type:
            print("Erro semântico, comparação de tipos diferentes")
        return a_value == b_value
    
    def inequality(self, a, b):
        for entry in self.symbol_table.table:
            if entry.identificador == a:
                a_type = entry.tipo
                a_value = entry.valor
            if entry.identificador == b:
                b_type = entry.tipo
                b_value = entry.valor
        if a_type != b_type:
            print("Erro semântico, comparação de tipos diferentes")
        return a_value != b_value
    
    def attribuition(self, a, b):
        for entry in self.symbol_table.table:
            if entry.identificador == b:
                self.symbol_table.setValue(a, entry.valor)
                self.symbol_table.setType(a, entry.tipo)
                self.symbol_table.setSize(a, entry.tamanho)

semantico = SemanticAnalyzer(lex.symbol_table)

semantico.analysis(lex.tape)
semantico.symbol_table.print()