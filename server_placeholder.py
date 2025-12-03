from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    data = request.json
    print("Received data:", data)
    return {"status": "ok", "received": data}

@app.route('/')
def home():
    return "Placeholder endpoint running."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
