"""
RYLR-896 connected to Raspberry Pi UART
"""

import serial
import time
import json

SERIAL_PORT = '/dev/ttyAMA0'
BAUD_RATE = 115200

def setup_lora(ser):
    # reset to defaults
    ser.write(b'AT+RESET\r\n')
    time.sleep(1)
    response = ser.read_add().decode()
    print(f"Reset: {response}")
    
    # set network ID (both must have same ID)
    ser.write(b'AT+NETWORKID=5\r\n')
    time.sleep(0.5)
    response = ser.read_all().decode()
    print(f"Network ID: {response}")
    
    # set address (sender = 1)
    ser.write(b'AT+ADRESS=1\r\n')
    time.sleep(0.5)
    response = ser.read_all().decode()
    print(f"Address: {response}")
    
    # get settings
    ser.write(b'AT+PARAMETER?\r\n')
    time.sleep(0.5)
    response = ser.read_all().decode()
    print(f"Parameters: {response}")
    
def send_message(ser, destination, message):
    data = message.encode()
    length = len(data)
    
    command = f'AT+SEND={destination},{length},{message}\r\n'
    
    ser.write(command.encode())
    
    time.sleep(0.5)
    response = ser.read_all().decode()
    print(f"Response: {response}")
    
def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Serial port {SERIAL_PORT} opened at {BAUD_RATE} baud\n")
        
        setup_lora(ser)
        
        send_message(ser, 2, "Hello LoRa!")
        time.sleep(2)
        
        weather_data = {
            "temperature": 72.5,
            "humidity": 55.9,
            "pressure": 1013.2,
            "wind_speed": 3.5,
            "wind_direction": 180,
            "rainfall": 0.2
        }
        
        send_message(ser, 2, json.dumps(weather_data))
        time.sleep(2)
        
        for i in range(3):
            test_data = {
                "temp": 70 + i,
                "humidity": 50 + i,
                "pressure": 1013,
                "wind_speed": 2 + i,
                "wind_direction": 90 * i,
                "rainfall": 0.0
            }
            send_message(ser, 2, json.dumps(test_data))
            time.sleep(3)
        
        print("\n test complete")
        
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\n\n Test interrupted by user")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("  Serial port closed")
if __name__ == "__main__":
    main()