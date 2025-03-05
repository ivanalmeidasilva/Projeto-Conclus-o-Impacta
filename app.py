from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Conexão com o banco de dados
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Buch_159753",
    database="sistema_biblioteca"
)

cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

# Cadastro de livros
@app.route('/cadastrar_livro', methods=['GET', 'POST'])
def cadastrar_livro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano_publicacao = request.form['ano_publicacao']
        cursor.execute("INSERT INTO livros (titulo, autor, ano_publicacao) VALUES (%s, %s, %s)",
                       (titulo, autor, ano_publicacao))
        db.commit()
        return redirect('/')
    return render_template('cadastrar_livro.html')


if __name__ == '__main__':
    app.run(debug=True)
