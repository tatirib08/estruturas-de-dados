import pandas as pd
import numpy as np  
import time 
from datetime import datetime 
import os
import json
import csv
import random

class Registro():
    def __init__(self):
        self.chave = None
        self.elemento = None 

class PaginaNode():
    def __init__(self, ordem):
        self.ordem = ordem
        self.registro = [None for i in range(self.ordem) ] #lista com o número de filhos possíveis
        self.apontador = [None for i in range(self.ordem + 1)]
        self.n = 0
        
class Arvore():

    def __init__(self):
        
        self.catalogo = dict()
        self.Order= 4 #ordem da árvore 
        self.Apontador = PaginaNode(self.Order)
        self.Chave = 0


    def readFile(self, filename):
        print("lendo arquivo")

        with open(filename) as file:
           
            dr = json.load(file)

            for dicionario in dr.items():
                (id, linha) = dicionario
                self.catalogo[int(id)]={'id': int(id), 'nome': linha["nome"],'autor': linha["autor"], 'quantidade': linha["quantidade"], 'img': linha['img']}
                
        # print(self.catalogo)
        # Ap, chave = _InserirElementos(Ap, ordem, dataframe, chave)
        Ap, chave =  self.buildTree(self.catalogo, self.Apontador,self.Order, self.Chave)

        self.printTree(Ap)
        
    def buildTree(self, dicionario, Ap, ordem, chave):
        # pass 
        tamanho = len(dicionario)
        # print(tamanho) # tam = 50 ok
        
        ''' Cria os registros a partir do dicionário '''
        for i in range(tamanho):
            register = Registro()
            register.chave = dicionario[i]["nome"]
            register.elemento = dicionario[i]["id"]
            # print(register.chave, " : ", register.elemento)
            
            # Ap = self.insertRegister(register, self.Order, Ap)
            Ap = self._Insere(register, Ap, ordem)
            
            chave+=1

        return Ap, chave

    def _InsereNaPagina(self,Ap, Reg, ApDir):
        k = Ap.n
        NaoAchouPosicao = (k > 0)
        while (NaoAchouPosicao):
            if ( Reg.chave >= Ap.r[k - 1].chave ):
                NaoAchouPosicao = False
                break
            Ap.registro[k] = Ap.registro[k - 1]
            Ap.apontador[k + 1] = Ap.apontador[k]
            k-= 1
            if (k < 1):
                NaoAchouPosicao = False

        Ap.registro[k] = Reg
        Ap.apontador[k + 1] = ApDir
        Ap.n += 1


    def _Ins(self, Reg, Ap, Cresceu, RegRetorno, ApRetorno, Ordem ):
        i = 1
        J = None
        if (Ap == None):
            Cresceu = True
            RegRetorno = Reg
            ApRetorno = None
            return Cresceu, RegRetorno, ApRetorno

        while ( i < Ap.n and Reg.chave > Ap.r[i - 1].chave ):
            i+= 1

        if(Reg.chave == Ap.registro[i - 1].chave):
            print(" Erro: Registro já está presente\n")
            Cresceu = False
            return Cresceu, RegRetorno, ApRetorno

        if(Reg.chave < Ap.r[i - 1].chave):
            i-= 1

        Cresceu, RegRetorno, ApRetorno = self._Ins(Reg, Ap.apontador[i], Cresceu, RegRetorno, ApRetorno, Ordem)

        if(not Cresceu):
            return Cresceu, RegRetorno, ApRetorno
        if (Ap.n < Ordem): # Página tem espaco
            self._InsereNaPagina(Ap, RegRetorno, ApRetorno)
            Cresceu = False
            return Cresceu, RegRetorno, ApRetorno
        
        # Overflow: Página tem que ser dividida /
        ApTemp = PaginaNode(Ordem)
        ApTemp.n = 0
        ApTemp.apontador[0] = None

        if (i < (Ordem//2) + 1):
            self._InsereNaPagina(ApTemp, Ap.registro[Ordem - 1], Ap.apontador[Ordem])
            Ap.n-= 1
            self._InsereNaPagina(Ap, RegRetorno, ApRetorno)
        else:
            self._InsereNaPagina(ApTemp, RegRetorno, ApRetorno)
        for J in range((Ordem//2) + 2, Ordem + 1):
            self._InsereNaPagina(ApTemp, Ap.registro[J - 1], Ap.apontador[J])
        Ap.n = (Ordem//2)
        ApTemp.apontador[0] = Ap.apontador[(Ordem//2) + 1]
        RegRetorno = Ap.registro[(Ordem//2)]
        ApRetorno = ApTemp
        return Cresceu, RegRetorno, ApRetorno


    def _Insere(self,Reg, Ap, Ordem):
        Cresceu = False
        RegRetorno = Registro()
        ApRetorno = PaginaNode(Ordem)
        Cresceu, RegRetorno, ApRetorno = self._Ins(Reg, Ap, Cresceu, RegRetorno, ApRetorno, Ordem)
        if (Cresceu):
            ApTemp = PaginaNode(Ordem)
            ApTemp.n = 1
            ApTemp.registro[0] = RegRetorno
            ApTemp.apontador[1] = ApRetorno
            ApTemp.apontador[0] = Ap
            Ap = ApTemp
        return Ap
    
    # def _InserirElementos(self,Ap, ordem, dataframe, chave):
    #     tam_lin, tam_col = dataframe.shape
    #     for i in range(tam_lin):
    #         reg = Registro()
    #         reg.Chave = dataframe.iloc[i, 0]
    #         reg.Elemento = i
    #         Ap = self._Insere(reg, Ap, ordem)
    #         chave += 1
    #     return Ap, chave

    def printTree(self, Ap):

        if (Ap != None):
            i = 0
            while i < Ap.n:
                self.printTree(Ap.apontador[i])
                print(Ap.registro[i].chave, "-", Ap.registro[i].elemento)
                i += 1
                self.printTree(Ap.apontador[i])

def main():

    arvore = Arvore()

    arvore.readFile("catalogo.json")
    print("\n\nDictionary\n\n")
    # print(dataframe.to_string()) #ok

if __name__ == '__main__':
    main()