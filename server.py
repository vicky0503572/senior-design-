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

# Box locations 
box_locations = {
    # example: "box1": {"lat": 32.755, "lon": -97.330}
}

# Historical data storage [last 24 hours per box]
historical_data = {}
MAX_HISTORY_HOURS = 24
MAX_HISTORY_POINTS = 288 # 5 min intervals

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
        
        timestamp = datetime.now().isoformat()
        
        # Build reading object
        reading = {
            "box_id": box_id,
            "temperature": payload.get("temperature"),
            "humidity": payload.get("humidity"),
            "pressure": payload.get("pressure"),
            "wind_speed": payload.get("wind_speed"),
            "wind_direction": payload.get("wind_direction"),
            "rainfall": payload.get("rainfall"),
            "timestamp": timestamp,
            "status": "online", #default status
            "raw_data": payload #for debugging
        }
        
        # Add location if configured
        if box_id in box_locations:
            reading["location"] = box_locations[box_id]
        
        # Store as latest reading
        
        latest_readings[box_id] = reading
        
        # Add to historical data
        if box_id not in historical_data:
            historical_data[box_id] = []
        
        historical_data[box_id].append({
            "timestamp": timestamp,
            "temperature": payload.get("temperature"),
            "humidity": payload.get("humidity"),
            "pressure": payload.get("pressure"),
            "wind_speed": payload.get("wind_speed"),
            "wind_direction": payload.get("wind_direction"),
            "rainfall": payload.get("rainfall")
        })
        
        # Keep only last 24 hours
        if len(historical_data[box_id]) > MAX_HISTORY_POINTS:
            historical_data[box_id] = historical_data[box_id][-MAX_HISTORY_POINTS:]

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Box {box_id}: Temp={payload.get('temperature')}°F, Humidity={payload.get('humidity')}%")
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
        "temperature": data.get("temperature"),
        "humidity": data.get("humidity"),
        "pressure": data.get("pressure"),
        "wind_speed": data.get("wind_speed"),
        "wind_direction": data.get("wind_direction"),
        "rainfall": data.get("rainfall"),
        "timestamp": datetime.now().isoformat(),
        "raw_data": data
    }
    # Add location if configured
    if box_id in box_locations:
        latest_readings[box_id]["location"] = box_locations[box_id]
    return jsonify({"status": "ok", "box_id": box_id})

@app.route('/api/location/<box_id>', methods=['POST'])
def set_location(box_id):
    """Set the physical location of a box"""
    data = request.get_json()
    
    if not data.get("lat") or not data.get("lon"):
        return jsonify({"error": "Latitude and longitude are required"}), 400
    
    box_locations[box_id] = {
        "lat": data.get("lat"),
        "lon" : data.get("lon"),
        "name": data.get("name", f"Box {box_id}")
    }
    
    # Update existing reading if exists
    if box_id in latest_readings:
        latest_readings[box_id]["location"] = box_locations[box_id]
        
    return jsonify({
        "status": "ok",
        "box_id": box_id,
        "location": box_locations[box_id]
    })

@app.route('/api/location/<box_id>', methods=['GET'])
def get_location(box_id):
    """Get the physical location of a box"""
    if box_id in box_locations:
        return jsonify(box_locations[box_id])
    return jsonify({"error": f"No location data for box '{box_id}'"}), 404

@app.route('/api/locations', methods=['GET'])
def get_all_locations():
    """Get all configured box locations"""
    return jsonify(box_locations)

@app.route('/api/history/<box_id>', methods=['GET'])
def get_history(box_id):
    """Get historical data for a box"""
    if box_id not in historical_data:
        return jsonify({"error": f"No historical data for box '{box_id}'"}), 404
    
    # Optional: filter by time range
    hours = request.args.get('hours', 24, type=int)
    
    # Return all or filtered history
    return jsonify({
        "box_id": box_id,
        "data_points": len(historical_data[box_id]),
        "history": historical_data[box_id]
    })
    
@app.route('/api/status', methods=['GET'])
def get_system_status():
    """Get overall system status - for dashboard overview"""
    total_boxes = len(latest_readings)
    online_boxes = sum(1 for box in latest_readings.values() if box.get('status') == 'online')
    
    return jsonify({
        "total_boxes": total_boxes,
        "online_boxes": online_boxes,
        "offline_boxes": total_boxes - online_boxes,
        "last_update": datetime.now().isoformat()
    })
    
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