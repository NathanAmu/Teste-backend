from flask import Flask, jsonify, request

app = Flask(__name__)

# Estoque inicial
estoque = {"quantidade": 10}

@app.route('/api/estoque', methods=['GET'])
def obter_estoque():
    return jsonify(estoque)

@app.route('/api/comprar', methods=['POST'])
def comprar_produto():
    if estoque["quantidade"] > 0:
        estoque["quantidade"] -= 1
        return jsonify({"success": True, "estoque": estoque["quantidade"]})
    return jsonify({"success": False, "message": "Estoque esgotado!"}), 400

if __name__ == '__main__':
    app.run(debug=True)
