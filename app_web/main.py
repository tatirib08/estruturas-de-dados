from flask import Flask, url_for, render_template, jsonify, send_from_directory
from arquivo import Livros
app = Flask(__name__)

livros = Livros()

@app.route('/')
def principal():
    return render_template('index.html')

@app.route('/Catalogo')
def sobre1():

    return render_template('catalogo.html')

@app.route('/getcatalogo', methods=['GET'])
def get_catalogo():
    return jsonify(livros.catalogo), 201

@app.route('/removerlivro/<int:livro_id>', methods=['DELETE'])
def removerLivro(livro_id):
    del livros.catalogo[livro_id]
    return jsonify(livros.catalogo), 201

@app.route('/download', methods=['GET'])
def baixarCatalogo():
    return send_from_directory('temp', 'catalogo.json', as_attachment=True)

app.run(debug = True)