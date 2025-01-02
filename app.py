# app.py - Backend

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuração do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Juliano@1@db.wekvcdbfakqkqreltclx.supabase.co:5432/postgres")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo da tabela produtos
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

@app.route('/estoque', methods=['GET'])
def listar_estoque():
    produtos = Produto.query.all()
    estoque = [{"id": p.id, "nome": p.nome, "quantidade": p.quantidade} for p in produtos]
    return jsonify(estoque)

@app.route('/comprar/<int:produto_id>', methods=['POST'])
def comprar(produto_id):
    produto = Produto.query.get(produto_id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    if produto.quantidade > 0:
        produto.quantidade -= 1
        db.session.commit()
        return jsonify({"mensagem": "Compra realizada com sucesso"})
    else:
        return jsonify({"erro": "Produto esgotado"}), 400

@app.route('/adicionar', methods=['POST'])
def adicionar_estoque():
    dados = request.json
    nome = dados.get("nome")
    quantidade = dados.get("quantidade")

    if not nome or not isinstance(quantidade, int) or quantidade <= 0:
        return jsonify({"erro": "Dados inválidos"}), 400

    produto = Produto(nome=nome, quantidade=quantidade)
    db.session.add(produto)
    db.session.commit()
    return jsonify({"mensagem": "Produto adicionado com sucesso"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados se não existirem
    app.run(debug=True)
