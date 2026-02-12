# Weather Boxes Backend

Flask backend for receiving MQTT sensor data from weather boxes.

## Quick Start

### Install Dependencies
```bash
pip3 install -r requirements.txt --break-system-packages
```

### Install Mosquitto
```bash
sudo apt install mosquitto mosquitto-clients -y
sudo systemctl start mosquitto
```

### Run Server
```bash
python3 server.py
```

### Test
```bash
mosquitto_pub -h localhost -t "weather/box1/readings" -m '{"temp":72.5, "humidity":45, "pressure":1013.2, "wind_speed":3.2, "wind_direction":180, "rainfall":0.0}'
curl http://localhost:3001/api/latest
```

## API Documentation

See `API_DOCS.md`
