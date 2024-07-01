from dataclasses import dataclass

@dataclass
class Token:
    
    linha:int
    rotulo:str
    identificador:str

class SymbolTable:

    def __init__(self) -> None:
        self.id = 0
        self.table = []

    def print(self):
        print(self.table)