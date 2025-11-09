"""
server.app
-----------
Aplicação Flask que expõe a API do labirinto e serve a interface estática.
Fica dentro da pasta `server/` para facilitar apresentação e empacotamento (Docker).
"""
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from uuid import uuid4
from .engine import Game

app = Flask(__name__, static_folder='../static', template_folder='../templates')
CORS(app)

# armazenamento simples em memória (suficiente para demo/local)
games = {}


@app.route('/')
def index():
    # Página inicial (landing). A interface do jogo fica em /labirinto
    return render_template('landing.html')


@app.route('/labirinto')
def labirinto():
    return render_template('index.html')


@app.route('/api/new', methods=['POST'])
def new_game():
    data = request.get_json() or {}
    cols = int(data.get('cols', 20))
    rows = int(data.get('rows', 15))
    loops = int(data.get('loops', 20))
    game = Game(cols=cols, rows=rows, loops=loops)
    game_id = uuid4().hex
    games[game_id] = game
    return jsonify({'game_id': game_id, 'state': game.to_dict()})


@app.route('/api/state/<game_id>', methods=['GET'])
def get_state(game_id):
    game = games.get(game_id)
    if not game:
        return jsonify({'error': 'game not found'}), 404
    return jsonify({'game_id': game_id, 'state': game.to_dict()})


@app.route('/api/move', methods=['POST'])
def move():
    data = request.get_json() or {}
    game_id = data.get('game_id')
    direction = data.get('direction')
    if not game_id or not direction:
        return jsonify({'error': 'game_id and direction required'}), 400
    game = games.get(game_id)
    if not game:
        return jsonify({'error': 'game not found'}), 404
    moved = game.move(direction)
    return jsonify({'moved': moved, 'state': game.to_dict()})


@app.route('/api/solve', methods=['POST'])
def solve():
    data = request.get_json() or {}
    game_id = data.get('game_id')
    algorithm = data.get('algorithm', 'bfs')
    game = games.get(game_id)
    if not game:
        return jsonify({'error': 'game not found'}), 404
    # computa (se necessário) e armazena no game.solutions
    result = game.solve(algorithm)
    # retornar resultado + estado atualizado para simplicidade no frontend
    return jsonify({'result': result, 'state': game.to_dict()})


if __name__ == '__main__':
    # Usado apenas para desenvolvimento local
    app.run(host='0.0.0.0', port=5000, debug=True)
