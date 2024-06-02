import pandas as pd
import numpy as np  
import time 
from datetime import datetime 
import os
import json
import csv
import random

class Arvore():

    def __init__(self):
        
        self.catalogo = dict()
        

    def readFile(self, filename):
        print("lendo arquivo")
        df = pd.read_json(filename)

        with open(filename) as file:
           
            dr = json.load(file)

            for dicionario in dr.items():
                (id, linha) = dicionario
                self.catalogo[int(id)]={'nome': linha["nome"],'autor': linha["autor"], 'quantidade': linha["quantidade"], 'img': linha['img']}
                
                
        print(self.catalogo)


        return df
    
    def buildTree(self, dataframe):
        pass 

    def insert(self): 
        pass
    
def main():

    arvore = Arvore()

    dataframe = arvore.readFile("catalogo.json")
    print("\n\nDictionary\n\n")
    # print(dataframe.to_string()) #ok

if __name__ == '__main__':
    main()