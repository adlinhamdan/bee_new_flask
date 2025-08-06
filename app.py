import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from flask_cors import CORS

# Load env variables (make sure .env file has OPENAI_API_KEY=sk-xxxx)
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

# Create OpenAI client (new API)
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/forecast')
def forecast():
    return render_template('forecast.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route("/api", methods=["POST"])
def api():
    message = request.json.get("message")
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": message}
            ]
        )
        response_text = completion.choices[0].message.content
        return jsonify({"response": response_text})
    except Exception as e:
        print("OpenAI error:", e)  # This will print the exact error in your terminal
        return jsonify({"response": f"Failed to generate response! {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=9000)
