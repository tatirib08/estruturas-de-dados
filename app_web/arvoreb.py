import bisect
import json
class Registro():
    def __init__(self, chave: any, elemento: any) -> None:
        self.chave: any = chave
        self.elemento: any = elemento



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
            #se a pagina esta vazia, adiciona direto
            if len(self.registros) == 0:
                self.registros.append(registro_para_inserir)
            #se não estiver vazia, adiciona o registro na ordem correta dentro da página
            else:
                bisect.insort(self.registros, registro_para_inserir, key=lambda r: r.chave) #insere o registro ordenado pela sua chave dentro da lista de registros
            return True


    def dividir_no_meio(self, registro_que_seria_inserido: Registro) -> list:
        #insere nos registros
        bisect.insort(self.registros, registro_que_seria_inserido, key=lambda r: r.chave) #insere o registro ordenado pela sua chave dentro da lista de registros
        
        #pega a mediana (elemento do meio)
        mediana_da_lista: Registro = self.registros[self.tam_max//2]
        
        #divide a parte da esquerda e da direita
        indice_da_mediana: int = self.registros.index(mediana_da_lista)
        registros_esquerda: list = self.registros[:indice_da_mediana] 
        registros_direita: list = self.registros[indice_da_mediana + 1:] 

        return registros_esquerda, mediana_da_lista, registros_direita

class ArvoreB():
    def __init__(self, grau: int = 1):
        self.grau = grau
        self.raiz = None


    def inserir(self, chave: any, elemento: any) -> None:
        registro_para_inserir: Registro = Registro(chave, elemento)
        pagina_que_vai_receber: Pagina = None
        
        #decide a pagina que vai inserir o registro

        #se a árvore está vazia, aloca página na raiz
        if self.raiz == None:
            self.raiz = Pagina(self.grau)
            pagina_que_vai_receber = self.raiz

        #se árvore não está vazia, procura a página certa para inserir
        else:
            chave_a_inserir: any = registro_para_inserir.chave
            pagina_que_vai_receber = self.__buscar_pagina_para_inserir(chave_a_inserir, self.raiz) #busca recursiva

        #insere o registro na pagina escolhida
        self.__inserir_registro_na_pagina(registro_para_inserir, pagina_que_vai_receber)


    def imprimir(self) -> None:
        nivel: int = 0
        if self.raiz != None:
            self.__imprimir_recursivo(self.raiz, nivel)


    # def __imprimir_recursivo(self, pagina: Pagina):
        # print('[',end='')
        # for registro in pagina.registros:    
        #     print(registro.chave,end=';')
        # print(']')

        # for pagina in pagina.paginas:
        #     self.__imprimir_recursivo(pagina)

    def __imprimir_recursivo(self, pagina: Pagina, nivel: int):
        if(pagina==None):
            return

        nivel += 1
        print(f"nível {nivel}:", end='')
        print('[',end='')
        
        for registro in pagina.registros:
            if(registro!=None):    
                print(registro.chave,end=';')
        print(f'] - quantidade de filhos -> {len(pagina.paginas)}')

        for pagina in pagina.paginas:
            self.__imprimir_recursivo(pagina, nivel)

    def __buscar_pagina_para_inserir(self, chave: any, pag_atual: Pagina):
        i: int = 0
        #itera o vetor de registros procurando um registro menor que o atual (sai do loop quando achar um maior ou chegar no final, indicando que é o maior)
        while i < len(pag_atual.registros) and chave > pag_atual.registros[i].chave:
            i += 1
        eh_folha: bool = len(pag_atual.paginas) == 0 #verifica se é uma folha
        if eh_folha:
            return pag_atual  #retorna a página atual se for uma folha
        else:
            return self.__buscar_pagina_para_inserir(chave, pag_atual.paginas[i]) #se a pagina atual tiver filhos, busca recursivamente


    def __inserir_registro_na_pagina(self, registro: Registro, pagina: Pagina) -> None:
        
        #tenta inserir o registro na página desejada
        conseguiu_inserir: bool = pagina.inserir_registro(registro)

        #se a página estiver cheia, será necessário dividir
        if not conseguiu_inserir:
            #realiza divisão, recebendo os registros que ficarão na página da esquerda, o registro que irá subir, e os registros que ficarão na página da direita
            registros_esquerda, mediana, registros_direita = pagina.dividir_no_meio(registro) #a página atual irá sumir
            
            pagina_que_vai_receber_mediana: Pagina = None

            indice_que_vai_adicionar_paginas_divididas: Pagina = 0

            #a página de cima deve receber a mediana. se a página atual for a raiz, não existe página atual. deve ser alocada uma nova página (nova raiz)
            if pagina == self.raiz:
                nova_pagina: Pagina = Pagina(self.grau)
                self.raiz = nova_pagina
                pagina_que_vai_receber_mediana = nova_pagina
            else:
                pagina_que_vai_receber_mediana = pagina.pagina_cima
                indice_que_vai_adicionar_paginas_divididas = pagina_que_vai_receber_mediana.paginas.index(pagina)
                pagina_que_vai_receber_mediana.paginas.remove(pagina) #remove a página atual, já que duas novas serão criadas a partir da divisão

            #cria as novas paginas divididas, serão filhas da página que irá receber a mediana
            #esquerda
            pagina_esquerda: Pagina = Pagina(grau_arvore = self.grau, pagina_cima = pagina_que_vai_receber_mediana)
            pagina_esquerda.registros = registros_esquerda

            #direita
            pagina_direita: Pagina = Pagina(grau_arvore = self.grau, pagina_cima = pagina_que_vai_receber_mediana)
            pagina_direita.registros = registros_direita

            #insere o registro e logo em seguida insere as paginas divididas 
            self.__inserir_registro_na_pagina(mediana, pagina_que_vai_receber_mediana)
            print(indice_que_vai_adicionar_paginas_divididas)
            pagina_que_vai_receber_mediana.paginas.insert(indice_que_vai_adicionar_paginas_divididas, pagina_esquerda) # no vetor de paginas, o proprio indice do registro significa página menor que o registro
            pagina_que_vai_receber_mediana.paginas.insert(indice_que_vai_adicionar_paginas_divididas + 1, pagina_direita) # no vetor de paginas, o indice do registro + 1 significa página maior que o registro 


def main():
    arvore: ArvoreB = ArvoreB(4)
    catalogo = {}
    with open("catalogo.json") as file:
        dr = json.load(file)

        for dicionario in dr.items():
            (id, linha) = dicionario
            catalogo[int(id)]={'id': int(id), 'nome': linha["nome"],'autor': linha["autor"], 'quantidade': linha["quantidade"], 'img': linha['img']}
            
    # tamanho = len(catalogo)
    # for i in range(tamanho):
    #     chave = int(catalogo[i]["id"])
    #     elemento = catalogo[i]["nome"]
    #     # arvore.inserir(chave,"")
    #     print(f"inserindo {chave}")

    
    arvore.inserir(1, "")
    arvore.inserir(2, "")
    arvore.inserir(3, "")
    arvore.inserir(4, "")
    arvore.inserir(5, "")
    arvore.inserir(6, "")
    arvore.inserir(7, "")
    arvore.inserir(8, "")
    arvore.inserir(9, "")
    arvore.inserir(10, "")
    # arvore.inserir(11, "")
    # arvore.inserir(12, "")
    arvore.imprimir() 


if __name__ == "__main__":
    main()