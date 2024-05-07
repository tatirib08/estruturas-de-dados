from flask import Flask, url_for, render_template, jsonify, send_from_directory, request
from arquivo import Livros
import zipfile

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
        livros.salvarArquivo()
    else:
        del livros.catalogo[livro_id]
    return render_template('catalogo.html')


@app.route('/download', methods=['GET'])
def baixarCatalogo():
    zipfile.ZipFile('temp/catalogo.zip', mode='w').write("catalogo.json")
    return send_from_directory('temp', 'catalogo.zip', as_attachment=True)

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


app.run(debug = True)