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

        self.csv = "livros.csv"
        self.json = "catalogo.json"

        self.catalogo = dict()

        self.criarDic()
        self.salvarArquivo()
        # self.lerJson()

    def criarDic(self):
        with open(self.csv) as file:
            id = 0
            dr = csv.DictReader(file)

            precos: list = []

            for linha in dr:
                preco = f'{random.randint(19,50)}.{random.randint(80,99)}'
                while preco in precos:
                    preco = f'{random.randint(19,50)}.{random.randint(80,99)}'

                precos.append(preco)

                self.catalogo[id]={'nome': linha["nome"],'autor': linha["autor"], 'quantidade': random.randint(1,50), 'preco': preco, 'img': linha['img']}
                id+=1



    def lerJson(self):
        with open(self.json) as file:
            dr = json.load(file)
        
            for dicionario in dr.items():
                (id, linha) = dicionario
                self.catalogo[int(id)]={'nome': linha["nome"],'autor': linha["autor"], 'quantidade': linha["quantidade"], 'img': linha['img']}
                

    def addLivro(self, id, novoLivro):
        self.catalogo[id] = novoLivro
        self.salvarArquivo()

    def salvarArquivo(self):
        
        print("\nGravando arquivo.\n")

        file = open("catalogo.json", "w")
        json.dump(self.catalogo, file, indent=4, ensure_ascii=False)
        file.close()



        
