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
            print('estado ' + id, end=' ')
            if(estado.final):
                print('*', end=' ')
            print(':')
            if(len(estado.transicoes) == 0): print('-')
            for k, v in estado.transicoes.items():
                print(f'{k} -> {v}')


def criaAF(caminho, af:AF):
    # TODO: lista de simbolos
    with (open(caminho, 'r')) as entrada:
        for linha in entrada:
            nome_gramatica = re.search('^<[A-Z]>', linha)
            if nome_gramatica: # se for uma gramatica
                transicoes_term = re.findall('[|]?\s?([a-z]{1})[^<][|]', linha)
                transicoes_nterm = re.findall('[|]?\s?([a-z]<[A-Z]>)\s?[|]?', linha)
                print(transicoes_nterm, ', ', transicoes_term)
                novo_estado = Estado(id=nome_gramatica.group(0)[1])
                if(transicoes_term != None): novo_estado.final = True
                for t in transicoes_nterm:
                    simb_terminal = t[0]
                    simb_n_terminal = t[2]
                    novo_estado.adcTransicao(simb_terminal, simb_n_terminal)
                for t in transicoes_term:
                    simb_terminal = t[0]
                    novo_estado.transicoes[simb_terminal] = None
                af.estados[novo_estado.id] = novo_estado
            else: # se for um token
                token = re.search('[a-z]+', linha)[0]
                for i in range(len(token)):
                    if(i == 0): # Adiciona a transicao do primeiro simbolo do token no estado inicial
                        af.estados['S'].adcTransicao(token[0], str(Estado.seq_id))
                    else:
                        novo_estado = Estado()
                        novo_estado.adcTransicao(token[i], str(int(novo_estado.id) + 1))
                        af.estados[novo_estado.id] = novo_estado
                estado_aceita = Estado(final=True)
                af.estados[estado_aceita.id] = estado_aceita

def determiniza(af:AF):
    while True:
        novo_estado = None
        transicao_nd = None
        for estado in af.estados.values():
            nao_determinismo = False
            for transicao in estado.transicoes.values(): # para cada transicao por um simbolo
                if (transicao is not None and len(transicao) > 1): # se tiver >1 transicao por simbolo
                    transicao_nd = [t for t in transicao]
                    novo_estado = Estado(id=f"[{', '.join(transicao)}]")
                    transicao.clear()
                    transicao.append(novo_estado.id)
                    nao_determinismo = True
                    break
            if(nao_determinismo): break
        if (novo_estado is not None):
            af.estados[novo_estado.id] = novo_estado
        else: break # determinizado
        for estado in transicao_nd: # adiciona transicoes dos estados que compoem ao novo estado
            for simbolo, transicao in af.estados[estado].transicoes.items():
                for estado_destino in transicao:
                    af.estados[novo_estado.id].adcTransicao(simbolo, estado_destino)
            if (af.estados[estado].final):
                novo_estado.final = True
        for estado in transicao_nd:
            af.estados.pop(estado)

def removeMortos(af:AF):
    acessados = []
    nao_mortos = []
    alcancaveis = []
    inalcancaveis = []
    if(af.estados['S'].transicoes.values() is not None): nao_mortos.append('S')
    for estado in af.estados['S'].transicoes.values(): # p/ cada estado a partir do S
        if(estado is None): continue
        estado_atual = estado[0]
        acessados.append(estado_atual)
        while True:
            if (len(af.estados[estado_atual].transicoes.values()) > 0):
                prox_estado = [x for x in af.estados[estado_atual].transicoes.values()][0][0]
                acessados.append(prox_estado)
            else:
                alcancaveis.extend(acessados)
                if (af.estados[estado_atual].final):
                    nao_mortos.extend(acessados)
                acessados.clear()
                break
            estado_atual = prox_estado
    mortos = []
    for estado in af.estados.keys():
        if(estado not in nao_mortos):
            mortos.append(estado)
    for estado in mortos:
        af.estados.pop(estado)
    for estado in af.estados.values():
        if(estado.id not in alcancaveis):
            inalcancaveis.append(estado.id)
    for estado in inalcancaveis:
        af.estados.pop(estado)

af = AF()
criaAF("./teste.txt", af)
af.printa()
determiniza(af)

removeMortos(af)
