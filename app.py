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

# Empréstimo de livros
@app.route('/emprestar_livro', methods=['GET', 'POST'])
def emprestar_livro():
    if request.method == 'POST':

        id_livro = request.form['id_livro']
        data_emprestimo = request.form['data_emprestimo']
        cursor.execute("INSERT INTO emprestimos (id_livro, data_emprestimo) VALUES (%s, %s)",
                       (id_livro, data_emprestimo))
        cursor.execute("UPDATE livros SET disponivel = FALSE WHERE id = %s", (id_livro,))
        db.commit()
        return redirect('/')
    return render_template('emprestar_livro.html')

# Devolução de livros
@app.route('/devolver_livro', methods=['GET', 'POST'])
def devolver_livro():
    if request.method == 'POST':
        id_emprestimo = request.form['id_emprestimo']
        data_devolucao = request.form['data_devolucao']
        cursor.execute("UPDATE emprestimos SET data_devolucao = %s WHERE id = %s",
                       (data_devolucao, id_emprestimo))
        cursor.execute("UPDATE livros SET disponivel = TRUE WHERE id = (SELECT id_livro FROM emprestimos WHERE id = %s)", (id_emprestimo,))
        db.commit()
        return redirect('/')
    return render_template('devolver_livro.html')

if __name__ == '__main__':
    app.run(debug=True)
