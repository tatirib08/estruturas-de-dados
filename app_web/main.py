from flask import Flask, url_for, render_template 

app = Flask(__name__)

@app.route('/')
def principal():
    return render_template('index.html')

@app.route('/Catalogo')
def sobre1():
    # titulo= "Catalogo"
    # catalogo = [
    #     {"nome": "Cadeira", "quantidade": 8},
    #     {"nome": "Cafeteira", "quantidade": 4},
    #     {"nome": "Mixer", "quantidade": 6},
    # ]
    # return render_template('catalogo.html', titulo = titulo, catalogo = catalogo)
    return render_template('catalogo.html')


app.run(debug = True)