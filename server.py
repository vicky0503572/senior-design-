from flask import Flask, jsonify, request
from flask_cors import CORS 
import paho.mqtt.client as mqtt 
import json
import threading 
from datetime import datetime
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__)
CORS(app)

# store latest readings in memory
latest_readings = {}

# MQTT setup
BROKER = "localhost" 
PORT = 1883
TOPIC = "weather/+/readings" 

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT broker at {BROKER}:{PORT}")
        client.subscribe(TOPIC)
        print(f"Subscribed to: {TOPIC}")
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        box_id = msg.topic.split('/')[1] # extract box id from topic

        # store with timestamp
        latest_readings[box_id] = {
            "box_id": box_id,
            "temperature": payload.get("temp"),
            "humidity": payload.get("humidity"),
            "pressure": payload.get("pressure"),
            "wind_speed": payload.get("wind_speed"),
            "wind_direction": payload.get("wind_direction"),
            "rainfall": payload.get("rainfall"),
            "timestamp": datetime.now().isoformat(),
            "raw_data": payload #for debugging
        }

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Box {box_id}: Temp={payload.get('temp')}°F, Humidity={payload.get('humidity')}%")
    except Exception as e:
        print(f"Error parsing message: {e}")

# start mqtt in background thread
def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(BROKER, PORT, 60)
        client.loop_forever()
    except Exception as e:
        print(f"MQTT connection error: {e}")
        print("Make sure Mosquitto is running: sudo service mosquitto start")

mqtt_thread = threading.Thread(target=start_mqtt, daemon=True)
mqtt_thread.start()

# API endpoints
@app.route('/', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "running",
        "mqtt_broker": f"{BROKER}:{PORT}",
        "active_boxes": list(latest_readings.keys()),
        "total_readings": len(latest_readings)
    })

@app.route('/api/latest', methods=['GET'])
def get_all_latest():
    """Return all latest readings from all boxes"""
    return jsonify(latest_readings)

@app.route('/api/latest/<box_id>', methods=['GET'])
def get_latest_by_id(box_id):
    """Return latest reading for specific box"""
    if box_id in latest_readings:
        return jsonify(latest_readings[box_id])
    return jsonify({"error": f"No data for box '{box_id}'"}), 404

@app.route('/api/mock/<box_id>', methods=['POST'])
def mock_data(box_id):
    """Manual test enpoint"""
    data = request.get_json()
    latest_readings[box_id] = {
        "box_id": box_id,
        "temperature": data.get("temp"),
        "humidity": data.get("humidity"),
        "pressure": data.get("pressure"),
        "wind_speed": data.get("wind_speed"),
        "wind_direction": data.get("wind_direction"),
        "rainfall": data.get("rainfall"),
        "timestamp": datetime.now().isoformat(),
        "raw_data": data
    }
    return jsonify({"status": "ok", "box_id": box_id})

if __name__ == '__main__':
    print("=" * 60)
    print("Weather Box Backend Starting")
    print("=" * 60)
    print(f"API Server: http://localhost:3001")
    print(f"MQTT Broker: {BROKER}:{PORT}")
    print(f"Listening to: {TOPIC}")
    print("=" * 60)
    print("\n Test endpoints:")
    print("  GET  http://localhost:3001/")
    print("  GET  http://localhost:3001/api/latest")
    print("  GET  http://localhost:3001/api/latest/box1")
    print("  POST http://localhost:3001/api/mock/box1")
    print("\n Press Ctrl+C to stop\n")

    app.run(host='0.0.0.0', port=3001, debug=True, use_reloader=False)