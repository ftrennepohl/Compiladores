import re
from prettytable import PrettyTable
from dataclasses import dataclass

class Estado:

    def __init__(self, id, final=False) -> None:
        self.id = id
        self.final = final
        self.transicoes = {}

    def adcTransicao(self, simbolo, estado):
        if(simbolo not in self.transicoes.keys()):
            self.transicoes[simbolo] = []
        self.transicoes[simbolo].append(estado)

class Gerador_Ids:

    def __iter__(self):
        self.id = 0
        self.id_atual = str(self.id)
        return self

    def __next__(self):
        self.id_atual = str(self.id)
        self.id += 1
        return str(self.id_atual)
          

class AF:
    
    def __init__(self) -> None:
        self.estados = {}
        self.alfabeto = set()
        caracteres = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for i in caracteres: self.alfabeto.add(i)
        
    def criaAF(self, cadeia, gerador_ids):
        nome_gramatica = re.search('^<([a-zA-Z\\d]+)> ::=', cadeia)
        if nome_gramatica: # se for uma gramatica
            existe_transicoes_term = re.search('[|]?\\s([a-z]{1})[^<][|]?', cadeia)
            transicoes_term = re.finditer('[|]?\\s([a-z]{1})[^<][|]?', cadeia)
            transicoes_nterm = re.finditer('[|]?\\s([a-zA-Z\\d]+)(<[a-zA-Z\\d]+>)\\s?[|]?', cadeia)
            if(nome_gramatica not in self.estados.keys()):
                novo_estado = Estado(id=nome_gramatica[1])
            else:
                novo_estado = self.estados[nome_gramatica]
            for i in transicoes_term: print(i.group(1))
            #print('terminais', transicoes_term)
            if(existe_transicoes_term): novo_estado.final = True
            for t in transicoes_nterm:
                simb_transicao = t[1]
                estado_destino = t[2]
                self.alfabeto.add(simb_transicao)
                novo_estado.adcTransicao(simb_transicao, estado_destino)
            for t in transicoes_term:
                simb_transicao = t[1]
                self.alfabeto.add(simb_transicao)
                novo_estado.transicoes[simb_transicao] = None
            self.estados[novo_estado.id] = novo_estado
        else: # se for um token
            #token = re.search('[a-zA-Z]+', cadeia)[0]
            token = cadeia
            qtd_simbolos = len(token)
            for i in range(qtd_simbolos):
                self.alfabeto.add(token[i])
                if(i == 0): # Adiciona a transicao do primeiro simbolo do token no estado inicial
                    if('S' in self.estados.keys()):
                        next(gerador_ids)
                        self.estados['S'].adcTransicao(token[0], gerador_ids.id_atual)
                    else:
                        next(gerador_ids)
                        self.estados['S'] = Estado('S')
                        self.estados['S'].adcTransicao(token[0], gerador_ids.id_atual)
                elif(i == qtd_simbolos-1):
                    novo_estado = Estado(gerador_ids.id_atual, final=True)
                    self.estados[novo_estado.id] = novo_estado
                else:
                    novo_estado = Estado(gerador_ids.id_atual)
                    novo_estado.adcTransicao(token[i], next(gerador_ids))
                    self.estados[novo_estado.id] = novo_estado
    
    def imprimir(self):
        tabela = PrettyTable()
        tabela.align = 'l'
        cabecalho = [simbolo for simbolo in self.alfabeto]
        cabecalho.insert(0, 'Est/Simb')
        tabela.field_names = cabecalho
        for estado in self.estados.values():
            if(not estado.final): linha = [estado.id]
            else: linha = [estado.id + ' *']
            for simbolo in self.alfabeto:
                if(simbolo in estado.transicoes.keys() and estado.transicoes[simbolo] is not None):
                    linha.append(estado.transicoes[simbolo])
                else:
                    linha.append('-')
            tabela.add_row(linha)
        print(tabela)
        with open("out.txt", "w+") as arq:
            arq.write(str(tabela))

    def determiniza(self):
        while True:
            novo_estado = None
            transicao_nd = None
            for estado in self.estados.values():
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
                self.estados[novo_estado.id] = novo_estado
            else: break # determinizado
            for estado in transicao_nd: # adiciona transicoes dos estados que compoem ao novo estado
                for simbolo, transicao in self.estados[estado].transicoes.items():
                    for estado_destino in transicao:
                        self.estados[novo_estado.id].adcTransicao(simbolo, estado_destino)
                if (self.estados[estado].final):
                    novo_estado.final = True
            for estado in transicao_nd:
                self.estados.pop(estado)

    def minimiza(self):
        acessados = []
        nao_mortos = []
        alcancaveis = []
        inalcancaveis = []
        if(self.estados['S'].transicoes.values() is not None): nao_mortos.append('S')
        for estado in self.estados['S'].transicoes.values(): # p/ cada estado a partir do S
            if(estado is None): continue
            estado_atual = estado[0]
            acessados.append(estado_atual)
            while True:
                if (len(self.estados[estado_atual].transicoes.values()) > 0):
                    prox_estado = [x for x in self.estados[estado_atual].transicoes.values()][0][0]
                    acessados.append(prox_estado)
                else:
                    alcancaveis.extend(acessados)
                    if (self.estados[estado_atual].final):
                        nao_mortos.extend(acessados)
                    acessados.clear()
                    break
                estado_atual = prox_estado
        mortos = []
        for estado in self.estados.keys():
            if(estado not in nao_mortos):
                mortos.append(estado)
        for estado in mortos:
            self.estados.pop(estado)
        for estado in self.estados.values():
            if(estado.id not in alcancaveis):
                inalcancaveis.append(estado.id)
        for estado in inalcancaveis:
            self.estados.pop(estado)

@dataclass
class Token:
    
    linha:int
    rotulo:str
    identificador:str


def analisadorLexico(caminho):

    # Definicao dos tokens:
    palavras_reservadas = ("BEGIN", "END", "IF", "ELSE", "if", "true", "let", "false")
    # identificadores: devem iniciar com uma letra, seguida de letras ou dígitos
    # símbolos
    constantes = ("Hello World!", "HEITOR", "LUCAS", "ALEX", "RIAN", "NEWGUY")

    gerador_ids = iter(Gerador_Ids())

    analisador = AF() # AF que vai juntar os AFs de cada token
    analisador.estados['S'] = Estado('S')

    tem_variavel = False # flag que indica se e necessario um estado que aceite ids

    with (open(caminho, 'r')) as entrada:
        afs_tokens = {}
        atributos_tokens = []
        i = 0
        for token in entrada:
            token = token.strip()
            linha = i
            identificador = token
            i += 1
            for char in token:
                analisador.alfabeto.add(char)
            if(token in palavras_reservadas):
                rotulo = "Palavra reservada"
            elif(re.match("[a-zA-z][a-zA-Z\\d]*", token)):
                rotulo = "Id"
                tem_variavel = True
                atributos_tokens.append(Token(linha, rotulo, identificador))
                continue
            elif(re.match("[+-=;:{}]+", token)):
                rotulo = "Simbolo"
            elif(token in constantes):
                rotulo = "Constante"
            atributos_tokens.append(Token(linha, rotulo, identificador))
            af = AF()
            af.criaAF(token, gerador_ids)
            afs_tokens[token] = af
    print('Fita:', end=' ')
    for af in afs_tokens.values(): # Forma novo autômato juntando todos os outros
        for estado in af.estados.values():
            if(estado.id != 'S'): analisador.estados[estado.id] = Estado(estado.id)
            if(estado.final):
                print(estado.id, end=', ')
                analisador.estados[estado.id].final = True
            for simb, lista_destinos in estado.transicoes.items():
                for destino in lista_destinos:
                    analisador.estados[estado.id].adcTransicao(simb, destino)
    if(tem_variavel): # tem
        novo_estado = Estado("V", final=True)
        analisador.estados[novo_estado.id] = novo_estado
        for simbolo in analisador.alfabeto:
            if re.match("[A-Z]", simbolo):
                analisador.estados[novo_estado.id].adcTransicao(simbolo, novo_estado.id)
                analisador.estados['S'].adcTransicao(simbolo, novo_estado.id)
        print(novo_estado.id)
    analisador.estados['F'] = Estado(id='F')
    print()
    analisador.imprimir()
    tabela_simbolos = PrettyTable()
    tabela_simbolos.field_names = ['Identificador', 'Rótulo', 'Linha']
    tabela_simbolos.add_rows([(token.identificador, token.rotulo, token.linha) for token in atributos_tokens])
    tabela_simbolos.align = 'l'
    print(tabela_simbolos)


analisadorLexico("teste.txt")

#analisadorLexico("teste.txt")
