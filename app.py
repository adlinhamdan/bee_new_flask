import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests

# Load env variables (make sure .env file has OPENAI_API_KEY=sk-xxxx)
load_dotenv()

AGENTIVE_API_KEY = os.environ.get("AGENTIVE_API_KEY") 
AGENTIVE_ASSISTANT_ID = os.environ.get("AGENTIVE_ASSISTANT_ID") 

app = Flask(__name__)
CORS(app)
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/forecast')
def forecast():
    return render_template('forecast.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/map')
def map():
    return render_template('map.html')


def get_chat_session():
    resp = requests.post(
        'https://agentivehub.com/api/chat/session',
        json={
            "api_key": AGENTIVE_API_KEY,
            "assistant_id": AGENTIVE_ASSISTANT_ID,
        }
    )
    resp.raise_for_status()
    return resp.json()["session_id"]

@app.route("/api", methods=["POST"])
def api():
    message = request.json.get("message")
    if not message:
        return jsonify({"response": "No message provided."}), 400

    try:
        session_id = get_chat_session()
    except Exception as e:
        print("AgentiveHub session error:", e)
        return jsonify({"response": f"Failed to get chat session! {str(e)}"}), 500

    try:
        chat_payload = {
            "api_key": AGENTIVE_API_KEY,
            "session_id": session_id,
            "type": "custom_code",
            "assistant_id": AGENTIVE_ASSISTANT_ID,
            "messages": [{"role": "user", "content": message}]
        }
        chat_resp = requests.post(
            'https://agentivehub.com/api/chat',
            json=chat_payload
        )
        chat_resp.raise_for_status()
        reply = chat_resp.json()
        print("AGENTIVE RAW REPLY:", reply)   # <--- Add this line


        # Adjust this if AgentiveHub's response structure is different
        agentive_reply = reply.get("content", "No reply received.")
        return jsonify({"response": agentive_reply})

    except Exception as e:
        print("AgentiveHub chat error:", e)
        return jsonify({"response": f"Failed to get response! {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=9000)
    
    

