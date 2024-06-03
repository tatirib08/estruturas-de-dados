from flask import Flask, url_for, render_template, jsonify, send_from_directory, request
from arquivo import Livros
from lempel_ziv_welch import LempelZivWelch
from arvoreb import ArvoreB
import zipfile
import json


app = Flask(__name__)

livros = Livros()

@app.route('/')
def principal():
    return render_template('index.html')

@app.route('/Catalogo')
def catalogo():

    return render_template('catalogo.html')

@app.route('/getcatalogo', methods=['GET'])
def get_catalogo():
    return jsonify(livros.catalogo), 201

@app.route('/removerlivro/<int:livro_id>', methods=['GET'])
def removerLivro(livro_id):
    del livros.catalogo[livro_id]
    livros.salvarArquivo()
    return render_template('catalogo.html')

@app.route('/addEstoque/<int:livro_id>', methods=['GET'])
def addEstoque(livro_id):

    livros.catalogo[livro_id]['quantidade'] += 1
    livros.salvarArquivo()
    return render_template('catalogo.html')

@app.route('/subEstoque/<int:livro_id>', methods=['GET'])
def subEstoque(livro_id):

    if(int(livros.catalogo[livro_id]['quantidade']) > 0):
        livros.catalogo[livro_id]['quantidade'] -= 1
    else:
        del livros.catalogo[livro_id]
        
    livros.salvarArquivo()
    return render_template('catalogo.html')


@app.route('/download', methods=['GET'])
def baixarCatalogo():
    with open("catalogo.json") as file:
        LempelZivWelch.compress(str(json.load(file)), "temp/catalogo.pkl", True, False)
        return send_from_directory('temp', 'catalogo.pkl', as_attachment=True)

@app.route('/addLivro')
def addLivro():
    return render_template('adicionar_livro.html')

@app.route('/novoLivro', methods=['POST'])
def novoLivro():
    print(request.form)
    livro = {'nome': request.form['fnome'], 'autor': request.form['fautor'] , 'quantidade': int(request.form['festoque']) , 'img': request.form['furl']}
    id = len(livros.catalogo)
    livros.addLivro(id, livro)
    # return jsonify(livros.catalogo), 201
    return render_template('catalogo.html')

@app.route('/mostrarBusca')
def mostrarBusca():

    return render_template('busca_livro_intervalo.html')

@app.route('/buscaIntervalo', methods=['POST'])
def buscaIntervalo():
    # print(request.form)

    if(request.form["options"] == "1"):
        primeira_letra = request.form["fprimeiraletra"]
        ultima_letra = request.form["fultimaletra"]
        print("\nPrimeira letra: ", primeira_letra)
        print("\nUltima letra: ", ultima_letra)
        buscaIntervaloNome(primeira_letra, ultima_letra)
    if(request.form["options"]== "2"): 
        valor_min = request.form["fmin"]
        valor_max = request.form["fmax"]
        print("Valor min: ", valor_min)
        print("Valor max: ", valor_max)
        buscaIntervaloPreco(valor_min, valor_max)
    return render_template('catalogo.html')

app.run(debug = True)

def buscaIntervaloNome(primeira_letra: str, ultima_letra: str) -> dict:
    #criar a arvore com os dados do dicionario
    grau: int = 5
    arvore = ArvoreB(grau)

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
        arvore.inserir(chave, dado)
    
    #chamar a função da arvore de buscar por intervalo (vai retornar lista com todos os ids)

    '''
    intervalo = arvore.buscaPorIntervalo(primeira_letra, ultima_letra)
    '''
    
    #retornar a lista com todos os ids ou o dicionario só com os elementos desses ids

def buscaIntervaloPreco(valor_min: float, valor_max: float) -> dict:

    #criar a arvore com os dados do dicionario
    grau: int = 5
    arvore = ArvoreB(grau)

    catalogo = {}
    with open("catalogo.json") as file:
        dr = json.load(file)

        for dicionario in dr.items():
            (id, linha) = dicionario
            catalogo[int(id)]={'id': int(id), 'nome': linha["nome"],'autor': linha["autor"], 'quantidade': linha["quantidade"], 'img': linha['img']}
            
    tamanho = len(catalogo)
    for i in range(tamanho):
        chave = catalogo[i]["preco"]
        dado = catalogo[i]["id"]
        arvore.inserir(chave, dado)
    
    #chamar a função da arvore de buscar por intervalo (vai retornar lista com todos os ids)

    '''
    intervalo = arvore.buscaPorIntervalo(primeira_letra, ultima_letra)
    '''
    
    #retornar a lista com todos os ids ou o dicionario só com os elementos desses ids