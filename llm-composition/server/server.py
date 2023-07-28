"""
Socket Io
"""
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/addedge', methods=['POST'])
def add_edge():
    edge_data = request.get_json()
    socketio.emit("addEdge", {"type": "addEdge", "edge": edge_data})
    return jsonify({"status": "success", "message": "Edge added"}), 200

@app.route('/action', methods=['POST'])
def add_action():
    action_data = request.get_json()
    socketio.emit("action", {"type": "action", "action": action_data})
    return jsonify({"status": "success", "message": "Action added"}), 200

@app.route('/setInitialAsk', methods=['POST'])
def set_initial_ask():
    ask_data = request.get_json()
    socketio.emit("initialAsk", {"type": "initialAsk", "ask": ask_data['ask']})
    return jsonify({"status": "success", "message": "Initial ask set"}), 200

@app.route('/askFinished', methods=['POST'])
def ask_finished():
    socketio.emit("askFinished", {"type": "askFinished"})
    return jsonify({"status": "success", "message": "Ask finished"}), 200



if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)