import re

class Estado:
    
    seq_id = 0

    def __init__(self, id=None, final=False) -> None:
        if(id == None):
            self.id = str(self.seq_id)
            Estado.seq_id +=1
        else: self.id = id
        self.final = final
        self.transicoes = {}

    def adcTransicao(self, simbolo, estado):
        if(simbolo not in self.transicoes.keys()):
            self.transicoes[simbolo] = []
        self.transicoes[simbolo].append(estado)

class AF:
    
    def __init__(self) -> None:
        self.estados = {}
        self.simbolos = []

    def printa(self):
        for id, estado in self.estados.items():
            if(estado.final):
                print('*', end=' ')
            print('estado ' + id + ':')
            if(len(estado.transicoes) == 0): print('-')
            for k, v in estado.transicoes.items():
                print(f'{k} -> {v}')


def criaAF(caminho, af:AF):
    # TODO: lista de simbolos
    with (open(caminho, 'r')) as entrada:
        for linha in entrada:
            nome_gramatica = re.search('^<[A-Z]>', linha)
            if nome_gramatica: # se for uma gramatica
                transicoes_term = re.findall('[|]? [a-z]{1} [|]?', linha)
                transicoes_nterm = re.findall('[a-z]<[A-Z]>', linha)
                novo_estado = Estado(id=nome_gramatica.group(0)[1])
                if(transicoes_term != None): novo_estado.final = True
                for t in transicoes_nterm:
                    novo_estado.adcTransicao(t[0], t[2])
                for t in transicoes_term:
                    novo_estado.transicoes[t[0]] = None
                af.estados[novo_estado.id] = novo_estado
            else: # se for um token
                token = re.search('[a-z]+', linha)[0]
                for i in range(len(token)):
                    novo_estado = Estado()
                    novo_estado.adcTransicao(token[i], str(int(novo_estado.id) + 1))
                    af.estados[novo_estado.id] = novo_estado
                    # Adiciona a transicao do primeiro simbolo do token no estado inicial
                    if(i == 0):
                        if(token[i] not in af.estados['S'].transicoes.keys()):
                            af.estados['S'].transicoes[token[i]] = []
                        af.estados['S'].transicoes[token[i]].append(novo_estado.id)
                estado_aceita = Estado(final=True)
                af.estados[estado_aceita.id] = estado_aceita

def determiniza(af:AF):
    while True:
        novo_estado = None
        transicao_nd = None
        for estado in af.estados.values():
            for transicao in estado.transicoes.values(): # para cada transicao por um simbolo
                if len(transicao) > 1: # se tiver >1 transicao por simbolo
                    transicao_nd = [t for t in transicao]
                    novo_estado = Estado(id=f"[{', '.join(transicao)}]")
                    transicao.clear()
                    transicao.append(novo_estado.id)
        if (novo_estado is not None):
            af.estados[novo_estado.id] = novo_estado
        else: break # determinizado
        for estado in transicao_nd: # adiciona transicoes dos estados que compoem ao novo estado
            for simbolo, transicao in af.estados[estado].transicoes.items():
                for estado in transicao:
                    af.estados[novo_estado.id].adcTransicao(simbolo, estado)


af = AF()
criaAF("./teste.txt", af)
determiniza(af)
