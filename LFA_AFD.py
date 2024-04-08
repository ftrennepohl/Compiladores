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

class AF:
    
    def __init__(self) -> None:
        self.estados = {}
        self.simbolos = []

def criaAF(caminho):
    # TODO: lista de simbolos
    af = AF()
    with (open(caminho, 'r')) as entrada:
        for linha in entrada:
            nome_gramatica = re.search('^<[A-Z]>', linha)
            if nome_gramatica: # se for uma gramatica
                transicoes_term = re.findall('\|? [a-z]{1} \|?', linha)
                transicoes_nterm = re.findall('[a-z]<[A-Z]>', linha)
                novo_estado = Estado(id=nome_gramatica.group(0)[1])
                if(transicoes_term != None): novo_estado.final = True
                for t in transicoes_nterm:
                    novo_estado.transicoes[t[0]] = t[2]
                for t in transicoes_term:
                    novo_estado.transicoes[t[0]] = None
                af.estados[novo_estado.id] = novo_estado
            else: # se for um token
                token = re.search('[a-z]+', linha)[0]
                for i in range(len(token)):
                    novo_estado = Estado()
                    novo_estado.transicoes[token[i]] = str(int(novo_estado.id) + 1)
                    af.estados[novo_estado.id] = novo_estado
                    # Adiciona a transicao do primeiro simbolo do token no estado inicial
                    if(i == 0):
                        if(token[i] not in af.estados['S'].transicoes):
                            af.estados['S'].transicoes[token[i]] = novo_estado.id
                        else:
                            af.estados['S'].transicoes[token[i]] += f', {novo_estado.id}'
                estado_aceita = Estado(final=True)
                af.estados[estado_aceita.id] = estado_aceita

    # Printa
    for id, estado in af.estados.items():
        if(estado.final):
            print('*', end=' ')
        print('estado ' + str(estado.id) + ':')
        if(len(estado.transicoes) == 0): print('-')
        for k, v in estado.transicoes.items():
            print(f'{k} -> {v}')

criaAF("./teste.txt")