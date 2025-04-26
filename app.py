from flask import Flask, request, jsonify
from models import get_db_connection, create_table

app = Flask(__name__)
create_table()

@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    matricula = data.get('matricula')
    senha = data.get('senha')

    if not all([nome, email, matricula, senha]):
        return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO aluno (nome, email, matricula, senha) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (nome, email, matricula, senha))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'mensagem': 'Aluno cadastrado com sucesso'}), 201

@app.route('/alunos', methods=['GET'])
def listar_alunos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT nome, email, matricula FROM aluno")
    alunos = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(alunos), 200

if __name__ == '__main__':
    app.run(debug=True)