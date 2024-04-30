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
        self.caminho = "livros.csv"
        self.df = pd.read_csv(self.caminho)
        # self.dados = pd.DataFrame(self.df)
        self.dados = {}
        self.catalogo = dict()

        self.criarDic()
        self.salvarArquivo()

    def criarDic(self):
        with open(self.caminho) as file:
            id = 0
            dr = csv.DictReader(file)

            for linha in dr:
                self.catalogo[id]={'nome': linha["nome"],'autor': linha["autor"], 'quantidade': random.randint(1,50), 'img': linha['img']}
                id+=1 

    def addLivro(self, id, novoLivro):
        self.catalogo[id] = novoLivro
        self.salvarArquivo()

    def salvarArquivo(self):
        
        print("\nGravando arquivo.\n")

        file = open("catalogo.json", "w")
        json.dump(self.catalogo, file, indent=4, ensure_ascii=False)
        file.close()



        
