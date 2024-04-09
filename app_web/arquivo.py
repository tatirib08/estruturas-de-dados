import pandas as pd
import numpy as np  
import time 
from datetime import datetime 
import os

class Livros():

    def __init__(self):
        self.lista_livros = dict()
        if os.path.exists("livros.csv"):
            file = open("dict.json", "r")
            self.dicionario = json.load(file)

    def addLivro(self):

    def eliminarLivro(self):


    def buscarLivro(self):
        
        print("\nInforme o funcionário que deseja buscar.\n")
        nome = input()
        if (nome in self.lista_livros):
            print(self.lista_livros[nome])
        else:
            print("\nO funcionário não está no dicionário.\n")


    def listarLivros(self): 
        