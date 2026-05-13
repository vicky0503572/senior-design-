from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

mock_data = {
    "box1": {
        "box_id": "box1",
        "temperature_f": 72.5,
        "temperature_c": 22.5,
        "humidity": 45.0,
        "pressure": 1013.2,
        "wind_speed": 3.2,
        "wind_direction": 180,
        "rainfall": 0.0,
        "timestamp": "2026-05-13T01:00:00.000000",
        "status": "online",
        "location": {"lat": 32.7555, "lon": -97.3308, "name": "Backyard Station"}
    }
}

@app.route("/api/latest")
def latest():
    return jsonify(mock_data)

@app.route("/api/status")
def status():
    return jsonify({"total_boxes": 1, "online_boxes": 1, "last_update": "2026-05-13T01:00:00.000000"})

@app.route("/api/locations")
def locations():
    return jsonify({"box1": {"lat": 32.7555, "lon": -97.3308, "name": "Backyard Station"}})

if __name__ == "__main__":
    app.run(port=3001)
