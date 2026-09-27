import os
import sys
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Add ai_engine to system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import AIVoiceAssistantRobot
from memory import RobotMemory

app = Flask(__name__, static_folder="../web_dashboard", static_url_path="")
CORS(app)

assistant = AIVoiceAssistantRobot()
memory = RobotMemory()

@app.route("/")
def serve_dashboard():
    return send_from_directory("../web_dashboard", "index.html")

@app.route("/<path:path>")
def serve_static(path):
    if os.path.exists(os.path.join("../web_dashboard", path)):
        return send_from_directory("../web_dashboard", path)
    if os.path.exists(os.path.join("../assets", path)):
        return send_from_directory("../assets", path)
    return "Not Found", 404

@app.route("/assets/<path:filename>")
def serve_assets(filename):
    return send_from_directory("../assets", filename)

@app.route("/image/<path:filename>")
def serve_user_images(filename):
    return send_from_directory("../image", filename)

@app.route("/api/command", methods=["POST"])
def process_command():
    data = request.get_json() or {}
    text_input = data.get("command", "").strip()
    
    if not text_input:
        return jsonify({"status": "error", "message": "No command provided"}), 400

    print(f"\n[API Received Command]: {text_input}")
    
    # Run Intent Classification
    intent = assistant.intent_classifier.classify(text_input)
    
    # Parse Command
    parsed_cmd = assistant.command_parser.parse(text_input, intent)
    
    # Generate Chatbot Response
    bot_response = assistant.chatbot.generate_response(text_input, intent, parsed_cmd)
    
    # Store in SQLite Memory
    memory.store_interaction(text_input, intent, bot_response)

    return jsonify({
        "status": "success",
        "user_input": text_input,
        "intent": intent,
        "parsed_command": parsed_cmd,
        "response": bot_response,
        "speak_text": bot_response
    })

@app.route("/api/history", methods=["GET"])
def get_history():
    conversations = memory.get_recent_conversations(limit=10)
    history = []
    for ts, u_in, b_res in conversations:
        history.append({
            "timestamp": ts,
            "user_input": u_in,
            "bot_response": b_res
        })
    return jsonify({"status": "success", "history": history})

@app.route("/api/status", methods=["GET"])
def get_status():
    return jsonify({
        "status": "online",
        "robot_name": "Jarvis",
        "battery": 95,
        "mode": "3D_Interactive_Voice_Assisted",
        "active_nodes": ["voice_node", "camera_node", "pid_controller"]
    })

def find_available_port(start_port=5000, max_attempts=10):
    import socket
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(("0.0.0.0", port))
                return port
            except OSError:
                continue
    return start_port

if __name__ == "__main__":
    requested_port = int(os.environ.get("PORT", 5000))
    port = find_available_port(requested_port)
    print(f"==================================================")
    print(f"  AI Voice Assistant Robot Server running on port {port}")
    print(f"  Open Web Dashboard: http://localhost:{port}")
    print(f"==================================================")
    app.run(host="0.0.0.0", port=port, debug=False)


