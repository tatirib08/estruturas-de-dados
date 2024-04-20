import pandas as pd
import numpy as np  
import time 
from datetime import datetime 
import os
import json
import csv
import random

class Livros():

    def __init__(self):

        # lendo o dataframe do csv 
        self.caminho = "/home/tati/ed2/app_web/livros.csv"
        self.df = pd.read_csv(self.caminho)
        # self.dados = pd.DataFrame(self.df)
        self.dados = {}
        self.catalogo = dict()
            

    def criarDic(self):
        with open(self.caminho) as file:

            dr = csv.DictReader(file)
            for linha in dr:

                self.catalogo[linha["nome"]]={'autor': linha["autor"], 'quantidade': random.randint(1,50)}

    def addLivro(self):
        print("Nome do livro: ")
        livro = input()
        print("Autor:")
        autor = input()
        print("Quantidade no estoque:")
        estoque = input()

        # add
        self.catalogo[livro] = {'autor': autor, 'quantidade': estoque}
        self.salvarArquivo()

    # def eliminarLivro(self):

    def salvarArquivo(self):
        
        print("\nGravando arquivo.\n")

        file = open("/home/tati/ed2/app_web/catalogo.json", "w")
        json.dump(self.catalogo, file, indent=4, ensure_ascii=False)
        file.close()


    def buscarLivro(self):
        
        print("\nInforme o funcionário que deseja buscar.\n")
        nome = input()
        if (nome in self.lista_livros):
            print(self.lista_livros[nome])
        else:
            print("\nO funcionário não está no dicionário.\n")


    # def listarLivros(self): 
        
def main():
    livros = Livros()
    # livros.addLivro()
    livros.criarDic()
    livros.salvarArquivo()
    

if __name__ == '__main__':
    main()