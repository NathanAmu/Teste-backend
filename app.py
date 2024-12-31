import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def init_db():
    try:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS estoque (id INTEGER PRIMARY KEY, quantidade INTEGER)')
        cursor.execute('INSERT OR IGNORE INTO estoque (id, quantidade) VALUES (1, 10)')
        conn.commit()
        conn.close()
        print("Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")

@app.route('/api/estoque', methods=['GET'])
def obter_estoque():
    try:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        cursor.execute('SELECT quantidade FROM estoque WHERE id = 1')
        quantidade = cursor.fetchone()[0]
        conn.close()
        return jsonify({"quantidade": quantidade})
    except Exception as e:
        print(f"Erro ao obter estoque: {e}")
        return jsonify({"error": "Erro ao obter estoque!"}), 500

@app.route('/api/comprar', methods=['POST'])
def comprar_produto():
    try:
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
        else:
            conn.close()
            return jsonify({"success": False, "message": "Estoque esgotado!"}), 400
    except Exception as e:
        print(f"Erro ao processar compra: {e}")
        return jsonify({"error": "Erro ao processar compra!"}), 500

@app.route('/api/adicionar', methods=['POST'])
def adicionar_estoque():
    try:
        dados = request.json
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
        print(f"Erro ao adicionar estoque: {e}")
        return jsonify({"error": "Erro ao adicionar estoque!"}), 500

if __name__ == '__main__':
    print("Iniciando servidor...")
    init_db()
    app.run(debug=True)
