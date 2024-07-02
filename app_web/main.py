from flask import Flask, url_for, render_template, jsonify, send_from_directory, request
from arquivo import Livros
from lempel_ziv_welch import LempelZivWelch
from arvoreb import ArvoreB
import zipfile
import json
from grafo_lib import Grafos

livros = Livros()

def buscarNoDicionario(lista_ids: list) -> dict:
    retorno: dict = {}

    for id in lista_ids:
        retorno[str(id)] = livros.catalogo[id]

    print(retorno)

    return retorno

def buscaIntervaloNome(primeira_letra: str, ultima_letra: str) -> dict:
    #criar a arvore com os dados do dicionario
    grau: int = 5
    arvore = ArvoreB(grau)

    for dicionario in livros.catalogo.items():
            (id, linha) = dicionario
            chave = linha["nome"]
            dado = id
            arvore.inserir(chave, dado)

    #chamar a função da arvore de buscar por intervalo (vai retornar lista com todos os ids)
    registrosNoIntervalo = arvore.busca_por_intervalo(arvore.raiz, primeira_letra, ultima_letra, 1)

    lista_ids: list = []

    for registro in registrosNoIntervalo:
        lista_ids.append(registro["dado"])

    #retornar a lista com todos os ids ou o dicionario só com os elementos desses ids
    return buscarNoDicionario(lista_ids)

def buscaIntervaloPreco(valor_min: float, valor_max: float) -> dict:

    #criar a arvore com os dados do dicionario
    grau: int = 5
    arvore = ArvoreB(grau)

    for dicionario in livros.catalogo.items():
        (id, linha) = dicionario
        chave = linha["preco"]
        dado = id
        arvore.inserir(chave, dado)

    #chamar a função da arvore de buscar por intervalo (vai retornar lista com todos os ids)
    registrosNoIntervalo = arvore.busca_por_intervalo(arvore.raiz,valor_min,valor_max, 2)

    lista_ids: list = []

    for registro in registrosNoIntervalo:
        lista_ids.append(registro["dado"])

    #retornar a lista com todos os ids ou o dicionario só com os elementos desses ids
    return buscarNoDicionario(lista_ids)


app = Flask(__name__)

@app.route('/')
def principal():
    return render_template('index.html')

@app.route('/administrador')
def administrador():
    return render_template('administrador.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html')

@app.route('/carrinho')
def carrinho():
    return render_template('carrinho.html')

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

@app.route('/showMap')
def showMap(): 
    return render_template('map.html')

@app.route('/novoLivro', methods=['POST'])
def novoLivro():
    print(request.form)
    livro = {'nome': request.form['fnome'], 'autor': request.form['fautor'] , 'quantidade': int(request.form['festoque']), 'preco': str(float(request.form['fpreco'])),  'img': request.form['furl']}
    id = len(livros.catalogo)
    livros.addLivro(id, livro)
    return render_template('catalogo.html')

@app.route('/mostrarBusca')
def mostrarBusca():

    return render_template('busca_livro_intervalo.html')

@app.route('/buscaIntervalo', methods=['POST'])
def buscaIntervalo():

    dicionario: dict = {}

    if(request.form["options"] == "1"):
        primeira_letra = request.form["fprimeiraletra"]
        ultima_letra = request.form["fultimaletra"]
        print("\nPrimeira letra: ", primeira_letra)
        print("\nUltima letra: ", ultima_letra)
        dicionario = buscaIntervaloNome(primeira_letra, ultima_letra)
    if(request.form["options"]== "2"): 
        valor_min = request.form["fmin"]
        valor_max = request.form["fmax"]
        print("Valor min: ", valor_min)
        print("Valor max: ", valor_max)
        dicionario = buscaIntervaloPreco(valor_min, valor_max)

    return jsonify(dicionario), 201

@app.route('/calcularFrete')
def calcularFrete(): 
    return render_template('calcula_frete.html')

@app.route('/mapa',  methods=['POST'])
def mapa():

    # cria o grafo
    grafo = Grafos()
    grafo.criaGrafo()

    endereco_selecionado = request.get_json()["options"]

    custo = grafo.caminhoMinimo(1,int(endereco_selecionado))
    print('CUSTO CALCULADO ',custo)
    frete = grafo.calculaFrete(custo)
    print('FRETE CALCULADO', frete)

    return jsonify({"frete": frete}), 201

@app.route('/comprafinalizada')
def compraFinalizada(): 
    return render_template('comprafinalizada.html')

app.run(debug = True)

