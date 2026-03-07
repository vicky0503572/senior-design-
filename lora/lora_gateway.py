import serial
import time
import json
import paho.mqtt.client as mqtt
from datetime import datetime

# Configuration
SERIAL_PORT = '/dev/ttyAMA0'
BAUD_RATE = 115200
MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
LORA_NETWORK_ID = 5
LORA_ADDRESS = 2  # Gateway address

def setup_lora(ser):
    ser.write(b'AT+RESET\r\n')
    time.sleep(1)
    ser.read_all()
    
    ser.write(f'AT+NETWORKID={LORA_NETWORK_ID}\r\n'.encode())
    time.sleep(0.5)
    ser.read_all()
    
    ser.write(f'AT+ADDRESS={LORA_ADDRESS}\r\n'.encode())
    time.sleep(0.5)
    ser.read_all()
    
    print("LoRa gateway configured")

def parse_lora_message(raw_data):
    """Parse RYLR-896 receive format: +RCV=<address>,<length>,<data>,<RSSI>,<SNR>"""
    if not raw_data.startswith('+RCV='):
        return None
    
    try:
        data = raw_data[5:]
        parts = data.split(',', 2)
        
        if len(parts) < 3:
            return None
        
        address = parts[0]
        remaining = parts[2].rsplit(',', 2)
        
        if len(remaining) == 3:
            message = remaining[0]
            rssi = remaining[1]
            snr = remaining[2].strip()
        else:
            message = parts[2]
            rssi = "N/A"
            snr = "N/A"
        
        return {
            "address": address,
            "message": message,
            "rssi": rssi,
            "snr": snr
        }
    except Exception as e:
        print(f"Parse error: {e}")
        return None

def on_mqtt_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print(f"MQTT connection failed with code {rc}")

def main():
    
    # Connect to MQTT broker
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_mqtt_connect
    
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()
    except Exception as e:
        print(f"MQTT connection error: {e}")
        return
    
    # Open serial connection to LoRa module
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Serial port {SERIAL_PORT} opened\n")
        
        setup_lora(ser)
        
        print("Gateway running - forwarding LoRa → MQTT")
        print("   Press Ctrl+C to stop\n")
        
        buffer = ""
        message_count = 0
        
        while True:
            if ser.in_waiting > 0:
                chunk = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
                buffer += chunk
                
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()
                    
                    if not line:
                        continue
                    
                    # Parse LoRa message
                    parsed = parse_lora_message(line)
                    
                    if parsed:
                        message_count += 1
                        timestamp = datetime.now().strftime('%H:%M:%S')
                        
                        print(f"[{timestamp}] 📥 LoRa message #{message_count}")
                        print(f"   From: Address {parsed['address']}")
                        print(f"   Signal: RSSI={parsed['rssi']} dBm, SNR={parsed['snr']} dB")
                        
                        # Map address to box_id
                        # You can customize this mapping
                        box_id = f"box{parsed['address']}"
                        
                        try:
                            # Parse JSON payload
                            data = json.loads(parsed['message'])
                            
                            # Publish to MQTT
                            topic = f"weather/{box_id}/readings"
                            payload = json.dumps(data)
                            
                            result = mqtt_client.publish(topic, payload)
                            
                            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                                print(f"   Published to MQTT: {topic}")
                                print(f"      {payload}")
                            else:
                                print(f"   MQTT publish failed: {result.rc}")
                            
                        except json.JSONDecodeError:
                            print(f"    Invalid JSON: {parsed['message']}")
                        
                        print()
            
            time.sleep(0.1)
    
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\n\n Gateway stopped by user")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        print(" Connections closed")

if __name__ == "__main__":
    main()