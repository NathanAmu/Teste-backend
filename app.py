import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Função para inicializar o banco de dados
def init_db():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS estoque (id INTEGER PRIMARY KEY, quantidade INTEGER)')
    # Insere o estoque inicial, se ainda não estiver no banco
    cursor.execute('INSERT OR IGNORE INTO estoque (id, quantidade) VALUES (1, 10)')
    conn.commit()
    conn.close()

# Rota para obter o estoque
@app.route('/api/estoque', methods=['GET'])
def obter_estoque():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    cursor.execute('SELECT quantidade FROM estoque WHERE id = 1')
    quantidade = cursor.fetchone()[0]
    conn.close()
    return jsonify({"quantidade": quantidade})

# Rota para comprar produto
@app.route('/api/comprar', methods=['POST'])
def comprar_produto():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    cursor.execute('SELECT quantidade FROM estoque WHERE id = 1')
    quantidade = cursor.fetchone()[0]

    if quantidade > 0:
        nova_quantidade = quantidade - 1
        cursor.execute('UPDATE estoque SET quantidade = ? WHERE id = 1', (nova_quantidade,))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "estoque": nova_quantidade})
    
    conn.close()
    return jsonify({"success": False, "message": "Estoque esgotado!"}), 400

# Rota para adicionar estoque
@app.route('/api/adicionar', methods=['POST'])
def adicionar_estoque():
    try:
        dados = request.json  # Recebe os dados enviados no corpo da requisição
        quantidade_para_adicionar = dados.get('quantidade', 0)

        if quantidade_para_adicionar <= 0:
            return jsonify({"success": False, "message": "Quantidade inválida para adicionar!"}), 400

        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        cursor.execute('SELECT quantidade FROM estoque WHERE id = 1')
        quantidade_atual = cursor.fetchone()[0]

        nova_quantidade = quantidade_atual + quantidade_para_adicionar
        cursor.execute('UPDATE estoque SET quantidade = ? WHERE id = 1', (nova_quantidade,))
        conn.commit()
        conn.close()

        return jsonify({"success": True, "estoque": nova_quantidade})
    except Exception as e:
        return jsonify({"success": False, "message": "Erro ao adicionar estoque!"}), 500

if __name__ == '__main__':
    init_db()  # Inicializa o banco de dados ao iniciar o app
    app.run(debug=True)
