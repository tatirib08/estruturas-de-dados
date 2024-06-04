import bisect
import json
from unidecode import unidecode
class Registro():
    def __init__(self, chave: any, dado: any) -> None:
        self.chave: any = chave
        self.dado: any = dado


class Pagina():
    def __init__(self, grau_arvore: int, pagina_cima = None) -> None:
        self.tam_max: int = grau_arvore - 1
        self.registros: list = []
        self.paginas: list = []
        self.pagina_cima = pagina_cima

    def inserir_registro(self, registro_para_inserir: Registro) -> bool:

        #verifica se a página atingiu o limite de registros
        atingiu_limite: bool = len(self.registros) + 1 > self.tam_max

        #se atingiu, retorna que não conseguiu inserir
        if atingiu_limite:
            return False
        #se nao atingiu, adiciona normalmente
        else:
            bisect.insort(self.registros, registro_para_inserir, key=lambda r: r.chave) #insere o registro ordenado pela sua chave dentro da lista de registros
            return True


    def dividir_no_meio(self, registro_que_seria_inserido: Registro) -> list:
        #insere nos registros
        bisect.insort(self.registros, registro_que_seria_inserido, key=lambda r: r.chave) #insere o registro ordenado pela sua chave dentro da lista de registros
        
        #pega a mediana (dado do meio)
        mediana_da_lista: Registro = self.registros[self.tam_max//2]
        
        #divide a parte da esquerda e da direita
        indice_da_mediana: int = self.registros.index(mediana_da_lista)
        registros_esquerda: list = self.registros[:indice_da_mediana] 
        paginas_esquerda: list = self.paginas[:indice_da_mediana + 1]
        registros_direita: list = self.registros[indice_da_mediana + 1:] 
        paginas_direita: list = self.paginas[indice_da_mediana + 1:]

        nova_pagina_esquerda: Pagina = Pagina(self.tam_max + 1)
        nova_pagina_esquerda.registros = registros_esquerda
        nova_pagina_esquerda.paginas = paginas_esquerda
        for pagina in nova_pagina_esquerda.paginas:
            pagina.pagina_cima = nova_pagina_esquerda

        nova_pagina_direita: Pagina = Pagina(self.tam_max + 1)
        nova_pagina_direita.registros = registros_direita
        nova_pagina_direita.paginas = paginas_direita
        for pagina in nova_pagina_direita.paginas:
            pagina.pagina_cima = nova_pagina_direita

        return nova_pagina_esquerda, mediana_da_lista, nova_pagina_direita

    def imprimir_registros(self):
        print('[',end='')
        
        for registro in self.registros:
            if(registro!=None):    
                print(registro.chave,end=';;; ')
        print(f'] - quantidade de filhos -> {len(self.paginas)}')
        
        
class ArvoreB():
    def __init__(self, grau: int = 1):
        self.grau = grau
        self.raiz = None

    def teste(self):
        
        print("Buscando")
        self.busca_por_intervalo(self.raiz, "e", "e", 1)


    def busca_por_intervalo(self,  paginaAtual : Pagina,inicio, fim, tipoBusca : int):
        # busca por nome: 1
        # busca por preço: 2
        # Verifica se a página é uma folha
        eh_folha = len(paginaAtual.paginas) == 0

        # Percorre todos os registros da página atual
        for i in range(len(paginaAtual.registros)):
            registro = paginaAtual.registros[i]
            # Se o registro estiver no intervalo add na lista
            if(tipoBusca == 1):
                if inicio <= unidecode(registro.chave[0].lower()) <= fim:
                    print(registro.chave)
            if(tipoBusca == 2): 
                if inicio <= registro.chave <= fim:
                    print(registro.chave)
            # Se a página não for folha, percorre a subárvore da esquerda antes de imprimir o registro
            if not eh_folha:
                self.busca_por_intervalo(paginaAtual.paginas[i], inicio, fim, tipoBusca)

        # Se a página não for folha, percorre a subárvore da direita após imprimir todos os registros
        if not eh_folha:
            self.busca_por_intervalo(paginaAtual.paginas[len(paginaAtual.registros)], inicio, fim, tipoBusca)


    def inserir(self, chave: any, dado: any) -> None:
        registro_para_inserir: Registro = Registro(chave, dado)
        pagina_que_vai_receber: Pagina = None
        
        #decide a pagina que vai inserir o registro

        #se a árvore está vazia, aloca página na raiz
        if self.raiz == None:
            self.raiz = Pagina(self.grau)
            pagina_que_vai_receber = self.raiz

        #se árvore não está vazia, procura a página certa para inserir
        else:
            chave_para_inserir: any = registro_para_inserir.chave
            pagina_que_vai_receber = self.__buscar_pagina_para_inserir(chave_para_inserir, self.raiz) #busca recursiva

        #insere o registro na pagina escolhida
        self.__inserir_registro_na_pagina(registro_para_inserir, pagina_que_vai_receber)

    def buscar(self, chave: any) -> None:
        if self.raiz != None:
            return self.__buscar_registro(chave, self.raiz)

    def imprimir_dados_em_ordem(self) -> None:
        if self.raiz != None:
            self.__imprimir_recursivo_dados_em_ordem(self.raiz)

    def imprimir_registros_em_ordem(self) -> None:
        if self.raiz != None:
            self.__imprimir_recursivo_registros_em_ordem(self.raiz)


    def imprimir_registros_pre_ordem(self) -> None:
        if self.raiz != None:
            self.__imprimir_recursivo_registros_pre_ordem(self.raiz)


    def imprimir_paginas_pre_ordem(self) -> None:
        nivel: int = 0
        if self.raiz != None:
            self.__imprimir_recursivo_paginas_pre_ordem(self.raiz, nivel)

    def __imprimir_recursivo_dados_em_ordem(self, pagina: Pagina):
        if len(pagina.paginas) > 0:
                self.__imprimir_recursivo_dados_em_ordem(pagina.paginas[0])
        for i in range(len(pagina.registros)):
            print(pagina.registros[i].dado)
            if len(pagina.paginas) > i + 1:
                self.__imprimir_recursivo_dados_em_ordem(pagina.paginas[i+1])


    def __imprimir_recursivo_registros_em_ordem(self, pagina: Pagina):
        if len(pagina.paginas) > 0:
                self.__imprimir_recursivo_registros_em_ordem(pagina.paginas[0])
        for i in range(len(pagina.registros)):
            print(pagina.registros[i].chave)
            if len(pagina.paginas) > i + 1:
                self.__imprimir_recursivo_registros_em_ordem(pagina.paginas[i+1])


    def __imprimir_recursivo_registros_pre_ordem(self, pagina: Pagina):
        for registro in pagina.registros:
            print(registro.chave)

        for pagina in pagina.paginas:
            self.__imprimir_recursivo_registros_pre_ordem(pagina)


    def __imprimir_recursivo_paginas_pre_ordem(self, pagina: Pagina, nivel: int):
        nivel += 1
        print(' '*nivel)
        print(f"nível {nivel}:", end='')

        pagina.imprimir_registros()

        for pagina in pagina.paginas:
            self.__imprimir_recursivo_paginas_pre_ordem(pagina, nivel)


    def __buscar_registro(self, chave: any, pag_atual: Pagina) -> Registro:
        indice_registro: int = 0
        #itera o vetor de registros procurando um registro maior que o atual (sai do loop quando achar um maior ou chegar no final)
        while indice_registro < len(pag_atual.registros) and chave > pag_atual.registros[indice_registro].chave:
            indice_registro += 1

        #checa se o índice encontrado é o desejado
        if indice_registro < len(pag_atual.registros) and chave == pag_atual.registros[indice_registro].chave:
            return pag_atual.registros[indice_registro]

        eh_folha: bool = len(pag_atual.paginas) == 0  #verifica se é uma folha
        if eh_folha:
            return None  #se for uma folha, o registro não existe na árvore
        else:
            #se a página atual tiver filhos, busca recursivamente no filho apropriado
            return self.__buscar_registro(chave, pag_atual.paginas[indice_registro])


    def __buscar_pagina_para_inserir(self, chave: any, pag_atual: Pagina):
        indice_registro: int = 0
        #itera o vetor de registros procurando um registro maior que o atual (sai do loop quando achar um maior ou chegar no final, indicando que é o maior)
        while indice_registro < len(pag_atual.registros) and chave > pag_atual.registros[indice_registro].chave:
            indice_registro += 1
        eh_folha: bool = len(pag_atual.paginas) == 0 #verifica se é uma folha
        if eh_folha:
            return pag_atual  #retorna a página atual se for uma folha
        else:
            return self.__buscar_pagina_para_inserir(chave, pag_atual.paginas[indice_registro]) #se a pagina atual tiver filhos, busca recursivamente


    def __inserir_registro_na_pagina(self, registro: Registro, pagina: Pagina) -> None:
        
        #tenta inserir o registro na página desejada
        conseguiu_inserir: bool = pagina.inserir_registro(registro)

        #se a página estiver cheia, será necessário dividir
        if not conseguiu_inserir:
            indice_que_vai_adicionar_paginas_divididas: int = 0

            #realiza divisão, recebendo os registros que ficarão na página da esquerda, o registro que irá subir, e os registros que ficarão na página da direita
            nova_pagina_esquerda, mediana, nova_pagina_direita = pagina.dividir_no_meio(registro) #a página atual irá sumir
            
            pagina_cima: Pagina = None

            #a página de cima deve receber a mediana. se a página atual for a raiz, não existe página atual. deve ser alocada uma nova página (nova raiz)
            if pagina == self.raiz:
                nova_pagina: Pagina = Pagina(self.grau)
                self.raiz = nova_pagina
                pagina_cima = nova_pagina
            else:
                pagina_cima = pagina.pagina_cima
                indice_que_vai_adicionar_paginas_divididas = pagina_cima.paginas.index(pagina)
                pagina_cima.paginas.remove(pagina) #remove a página atual, já que duas novas serão criadas a partir da divisão

            #atribui pagina de cima para as novas paginas criadas
            nova_pagina_esquerda.pagina_cima = pagina_cima
            nova_pagina_direita.pagina_cima = pagina_cima

            #insere as páginas e depois insere o registro na pagina que vai receber a mediana (talvez precise ser dividida)
            pagina_cima.paginas.insert(indice_que_vai_adicionar_paginas_divididas, nova_pagina_esquerda) # no vetor de paginas, o proprio indice do registro significa página menor que o registro
            pagina_cima.paginas.insert(indice_que_vai_adicionar_paginas_divididas + 1, nova_pagina_direita) # no vetor de paginas, o indice do registro + 1 significa página maior que o registro 
            self.__inserir_registro_na_pagina(mediana, pagina_cima)


def main():
    arvore: ArvoreB = ArvoreB(7)
    catalogo = {}
    with open("catalogo.json") as file:
        dr = json.load(file)

        for dicionario in dr.items():
            (id, linha) = dicionario
            catalogo[int(id)]={'id': int(id), 'nome': linha["nome"],'autor': linha["autor"], 'quantidade': linha["quantidade"], 'img': linha['img']}
            
    tamanho = len(catalogo)
    for i in range(tamanho):
        chave = catalogo[i]["nome"]
        dado = catalogo[i]["id"]
        # print(f'inserindo {chave}')
        arvore.inserir(chave, dado)
  
    # arvore.imprimir_registros_em_ordem()
    # arvore.imprimir_dados_em_ordem()
    # arvore.imprimir_paginas_pre_ordem()

    # registro: Registro = arvore.buscar("1984")
    # if registro == None:
    #     print("Registro não existe")
    # else:
    #     print(f"Chave -> {registro.chave}")
    #     print(f'Dado -> {registro.dado}')

    print("TESTANDO")
    arvore.teste()
 

if __name__ == "__main__":
    main()