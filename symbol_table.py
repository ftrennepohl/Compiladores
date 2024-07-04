from dataclasses import dataclass

@dataclass
class Token:
    
    linha:int
    rotulo:str
    identificador:str
    valor:any = None
    tipo:str = None
    tamanho:int = None

class SymbolTable:

    def __init__(self) -> None:
        self.id = 0
        self.table = []

    def print(self):
        print(self.table)

    def setValue(self, id, value):
        for entry in self.table:
            if entry.identificador == id:
                entry.valor = value

    def setType(self, id, value):
        for entry in self.table:
            if entry.identificador == id:
                entry.tipo = value

    def setSize(self, id, value):
        for entry in self.table:
            if entry.identificador == id:
                entry.tamanho = value