import serial
import time
import json

# Configure serial port
SERIAL_PORT = '/dev/ttyAMA0'
BAUD_RATE = 115200

def setup_lora(ser):
    # Reset to defaults
    ser.write(b'AT+RESET\r\n')
    time.sleep(1)
    response = ser.read_all().decode()
    print(f"Reset: {response}")
    
    # Set network ID (must match transmitter)
    ser.write(b'AT+NETWORKID=5\r\n')
    time.sleep(0.5)
    response = ser.read_all().decode()
    print(f"Network ID: {response}")
    
    # Set address (receiver = 2)
    ser.write(b'AT+ADDRESS=2\r\n')
    time.sleep(0.5)
    response = ser.read_all().decode()
    print(f"Address: {response}")
    
    # Get settings
    ser.write(b'AT+PARAMETER?\r\n')
    time.sleep(0.5)
    response = ser.read_all().decode()
    print(f"Parameters: {response}")
    
    print("✅ LoRa receiver ready!\n")

def parse_lora_message(raw_data):
   
    if not raw_data.startswith('+RCV='):
        return None
    
    try:
        # Remove +RCV= prefix
        data = raw_data[5:]
        
        # Split by comma (first 2 commas separate address and length)
        parts = data.split(',', 2)
        
        if len(parts) < 3:
            return None
        
        address = parts[0]
        length = parts[1]
        
        # The rest contains: <data>,<RSSI>,<SNR>
        # Find the last two commas for RSSI and SNR
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
            "length": length,
            "message": message,
            "rssi": rssi,
            "snr": snr
        }
    except Exception as e:
        print(f"Parse error: {e}")
        return None

def main():
    print("=" * 60)
    print("RYLR-896 LoRa Receiver Test")
    print("=" * 60)
    
    try:
        # Open serial connection
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Serial port {SERIAL_PORT} opened at {BAUD_RATE} baud\n")
        
        # Setup module
        setup_lora(ser)
        
        print("Listening for LoRa messages...")
        print("   (Press Ctrl+C to stop)\n")
        
        buffer = ""
        
        while True:
            if ser.in_waiting > 0:
                # Read available data
                chunk = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
                buffer += chunk
                
                # Process complete lines
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()
                    
                    if line:
                        print(f"Raw: {line}")
                        
                        # Parse LoRa message
                        parsed = parse_lora_message(line)
                        
                        if parsed:
                            print(f"   From: Address {parsed['address']}")
                            print(f"   Signal: RSSI={parsed['rssi']} dBm, SNR={parsed['snr']} dB")
                            print(f"   Message: {parsed['message']}")
                            
                            # Try to parse as JSON
                            try:
                                data = json.loads(parsed['message'])
                                print(f"      Weather Data:")
                                print(f"      Temp: {data.get('temperature')}°F")
                                print(f"      Humidity: {data.get('humidity')}%")
                                print(f"      Pressure: {data.get('pressure')} hPa")
                                print(f"      Wind: {data.get('wind_speed')} m/s @ {data.get('wind_direction')}°")
                                print(f"      Rain: {data.get('rainfall')} mm")
                            except json.JSONDecodeError:
                                pass  # Not JSON, just show raw message
                            
                            print()
            
            time.sleep(0.1)
    
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\n\n  Receiver stopped by user")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print(" Serial port closed")

if __name__ == "__main__":
    main()