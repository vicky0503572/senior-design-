from flask import Flask, jsonify, request
from flask_cors import CORS 
import paho.mqtt.client as mqtt 
import json
import threading 
from datetime import datetime
from collections import deque
import time
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

# Packet Loss tracking
packet_stats = {
}

# network resilience
message_queue = deque(maxlen=1000)
mqtt_connected = False

def degrees_to_compass(degree):
    if degree is None:
        return None
    directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                  'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    index = round(degrees / 22.5) % 16
    return directions[index]

# MQTT setup
BROKER = "localhost" 
PORT = 1883
TOPIC = "weather/+/readings" 

def calculate_packet_loss(box_id):
    if box_id not in packet_stats:
        return 0.0
    
    stats = packet_stats[box_id]
    total_expected = stats.get("total_expected", 0)
    total_received = stats.get("total_received", 0)
    
    if total_expected == 0:
        return 0.0
    
    lost = total_expected - total_received
    loss_percentage = (lost / total_expected) * 100
    return round(loss_percentage, 2)

def process_queued_messages():
    global mqt_connected
    
    if not mqtt_connected or len(message_queue) == 0:
        return
    
    print(f"\n Processing {len(message_queue)} queued message")
    
    while len(message_queue) > 0:
        try:
            queued_msg = message_queue.popleft()
            process_message(queued_msg["topic"], queued_msg["payload"])
            print(f" Processed queued message from {queued_msg['box_id']}")
        except Exception as e:
            print(f"Error processing queued message: {e}")

    print(f"Queue cleared:\n")

def process_message(topic, payload_str):
    try:
        payload = json.loads(payload_str)
        box_id = topic.split('/')[1]
        
        timstamp = datetime.now().isoformat()
        
        # packet loss tracking
        if "sequence" in payload:
            seq = payload["sequence"]
            
            if box_id not in packet_stats:
                packet_stats[box_id] = {
                    "total_expected": 0,
                    "total_received": 0,
                    "last_sequence": seq - 1
                } 
                
            stats = packet_stats[box_id]
            expected_seq = stats["last_sequence"] + 1
            
            # calculate expected packets
            if seq > expected_seq:
                # packet were lost
                lost_packets = seq - expected_seq
                stats["total_expected"] += lost_packets
                print(f"Box {box_id}: Lost {lost_packet} packet(s) (expected seq {expected_seq}, got {seq})")
                
            stats["total_expected"] += 1
            stats["total_received"] += 1
            stats["last_sequence'"] = seq
            
        # build reading object
        reading = {
            "box_id": box_id,
            "temperature_f": payload.get("temperature_f"),
            "temperature_c": payload.get("temperature_c"),
            "humidity": payload.get("humidity"),
            "pressure": payload.get("pressure"),
            "wind_speed": payload.get("wind_speed"),
            "wind_direction": payload.get("wind_direction"),
            "rainfall": payload.get("rainfall"),
            "timestamp": timestamp,
            "status": "online",
            "packet_loss": calculate_packet_loss(box_id),
            "raw_data": payload
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
            "temperature_f": payload.get("temperature_f"),
            "temperature_c": payload.get("temperature_c"),
            "humidity": payload.get("humidity"),
            "pressure": payload.get("pressure"),
            "wind_speed": payload.get("wind_speed"),
            "wind_direction": payload.get("wind_direction"),
            "rainfall": payload.get("rainfall")
        })
        
        # Keep only last 24 hours
        if len(historical_data[box_id]) > MAX_HISTORY_POINTS:
            historical_data[box_id] = historical_data[box_id][-MAX_HISTORY_POINTS:]
            
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Box {box_id}: {payload.get('temperature_f')}°F, Loss: {calculate_packet_loss(box_id)}%")
    except Exception as e:
        print(f"Error procesing message: {e}")
        
def on_connect(client, userdata, flags, rc):
    global mqtt_connected
    
    if rc == 0:
        mqtt_connected = True
        print(f"Connected to MQTT broker at {BROKER}:{PORT}")
        client.subscribe(TOPIC)
        print(f"Subscribed to: {TOPIC}")
        
        process_queued_messages()
    else:
        mqtt_connected = False
        print(f"Connection failed with code {rc}")

def on_disconnect(client, userdata, rc):
    global mqtt_connected
    mqtt_connected = False
    
    if rc != 0:
        print(f"Unexpected MQTT disconnect (code {rc})")
        print(f"Queuing messages until reconnection")
        
def on_message(client, userdata, msg):
    try:
        box_id = msg.topic.split('/')[1]
        payload_str = msg.payload.decode()
        
        # Process immediately if connected
        if mqtt_connected:
            process_message(msg.topic, payload_str)
        else:
            # Queue for later if disconnected
            message_queue.append({
                "topic": msg.topic,
                "payload": payload_str,
                "box_id": box_id,
                "queued_at": datetime.now().isoformat()
            })
            print(f"📦 Queued message from {box_id} (queue size: {len(message_queue)})")
            
    except Exception as e:
        print(f"Error in on_message: {e}")
        
# start mqtt in background thread
def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    
    # enable auto_reconnect
    client.reconnect_delay_set(min_delay=1, max_delay=120)

    try:
        client.connect(BROKER, PORT, 60)
        client.loop_forever()
    except Exception as e:
        print(f"MQTT connection error: {e}")
        print(f"Entering queue mode...")

mqtt_thread = threading.Thread(target=start_mqtt, daemon=True)
mqtt_thread.start()

# API endpoints
@app.route('/', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "running",
        "mqtt_broker": f"{BROKER}:{PORT}",
        "mqtt_connected": mqtt_connected,
        "queued_messages": len(message_queue),
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

@app.route('/api/stats/<box_id>', methods=['GET'])
def get_packet_stats(box_id):
    if box_id not in packet_stats:
        return jsonify({"error": "No statistics available for this box"}), 404
    
    stats = packet_stats[box_id]
    loss_pct = calculate_packet_loss(box_id)
    
    return jsonify({
        "box_id": box_id,
        "total_expected": stats["total_expected"],
        "total_received": stats["total_received"],
        "packets_lost": stats["total_expected"] - stats["total_received"],
        "packet_loss_percentage": loss_pct,
        "last_sequence": stats["last_sequence"],
        "status": "PASS" if loss_pct < 5.0 else "FAIL"
    })

@app.route('/api/stats', methods=['GET'])
def get_all_stats():
    all_stats = {}
    
    for box_id in packet_stats:
        stats = packet_stats[box_id]
        loss_pct = calculate_packet_loss(box_id)
        
        all_stats[box_id] = {
            "total_expected": stats["total_expected"],
            "total_received": stats["total_received"],
            "packet_lost": stats["total_expected"] - stats["total_received"],
            "packet_loss_percentage": loss_pct,
            "status": "PASS" if loss_pct < 5.0 else "FAIL"
        }
    
    return jsonify(all_stats)

@app.route('/api/mock/<box_id>', methods=['POST'])
def mock_data(box_id):
    """Manual test enpoint"""
    data = request.get_json()
    latest_readings[box_id] = {
        "box_id": box_id,
        "temperature_f": data.get("temperature_f"),
        "temperature_c": data.get("temperature_c"),
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