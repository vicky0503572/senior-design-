# Weather Station Backend API Documentation
**For Frontend Integration**

## Base URL
```
http://localhost:3001
```

---

## Endpoints

### 1. Get All Weather Boxes
**GET** `/api/latest`

Returns latest data from all active weather boxes.

**Response:**
```json
{
  "box1": {
    "box_id": "box1",
    "temperature_f": 72.5,
    "temperature_c": 22.5,
    "humidity": 45.0,
    "pressure": 1013.2,
    "wind_speed": 3.2,
    "wind_direction": 180,
    "rainfall": 0.0,
    "timestamp": "2026-02-13T14:30:00.000000",
    "status": "online",
    "location": {
      "lat": 32.7555,
      "lon": -97.3308,
      "name": "Backyard Station"
    }
  }
}
```

---

### 2. Get Specific Box Data
**GET** `/api/latest/<box_id>`

Returns data from a single weather box.

**Example:** `GET /api/latest/box1`

### 3. Get Historical Data (24 Hours)
**GET** `/api/history/<box_id>`

Returns timestamped sensor readings for the last 24 hours.

**Response:**
```json
{
  "box_id": "box1",
  "data_points": 144,
  "history": [
    {
      "timestamp": "2026-02-13T14:30:00.000000",
      "temperature_f": 72.5,
      "temperature_c": 22.5,
      "humidity": 45.0,
      "pressure": 1013.2,
      "wind_speed": 3.2,
      "wind_direction": 180,
      "rainfall": 0.0
    }
  ]
}
```

---

### 4. Get System Status
**GET** `/api/status`

Returns overall system health.

**Response:**
```json
{
  "total_boxes": 5,
  "online_boxes": 5,
  "last_update": "2026-02-13T14:30:00.000000"
}
```

---

### 5. Set Box Location
**POST** `/api/location/<box_id>`

Configure the physical location (lat/lon) where a weather box is installed.

**Request Body:**
```json
{
  "lat": 32.7555,
  "lon": -97.3308,
  "name": "My Backyard"
}
```

**Response:**
```json
{
  "status": "ok",
  "box_id": "box1",
  "location": {
    "lat": 32.7555,
    "lon": -97.3308,
    "name": "My Backyard"
  }
}
```

---

### 5. Get Box Location
**GET** `/api/location/<box_id>`

Get the configured location for a specific box.

**Response:**
```json
{
  "lat": 32.7555,
  "lon": -97.3308,
  "name": "My Backyard"
}
```

---

### 6. Get All Locations
**GET** `/api/locations`

Get all configured box locations (for map markers).

**Response:**
```json
{
  "box1": {
    "lat": 32.7555,
    "lon": -97.3308,
    "name": "My Backyard"
  },
  "box2": {
    "lat": 32.7600,
    "lon": -97.3400,
    "name": "Front Yard"
  }
}
```

---

## Data Field Reference

| Field | Type | Unit | Description |
|-------|------|------|-------------|
| `box_id` | string | - | Unique box identifier |
| `temperature_f` | float | °F | Temperature in Fahrenheit |
| `temperature_c` | float | °C | Temperature in Celsius |
| `humidity` | float | % | Relative humidity |
| `pressure` | float | hPa | Atmospheric pressure (hectopascals) |
| `wind_speed` | float | m/s | Wind speed |
| `wind_direction` | integer | degrees | Wind direction (0-360°, 0=North) |
| `rainfall` | float | mm | Rainfall amount |
| `timestamp` | string | ISO 8601 | When reading was taken |
| `status` | string | - | Box status (always "online") |

---
## Unit Conversions Reference

### **Temperature:**
- **Frontend displays:** Both F and C (user preference or toggle)
- **Conversion:** Already done by backend - no frontend math needed!

### **Pressure:**
- **hPa (hectopascals)** = standard weather unit
- 1013.25 hPa = normal sea level pressure
- Range: 300-1250 hPa (covers CDR requirement of 30-125 kPa)
- **If you need kPa:** Divide by 10 (e.g., 1013.2 hPa = 101.32 kPa)
- **If you need Pa:** Multiply by 100 (e.g., 1013.2 hPa = 101320 Pa)

## Auto-Refresh Strategy

**Option: Polling**
```javascript
// Poll for updates every 5 seconds
useEffect(() => {
  const fetchData = async () => {
    const response = await fetch('http://localhost:3001/api/latest');
    const data = await response.json();
    setWeatherData(data);
  };

  fetchData(); // Initial fetch
  const interval = setInterval(fetchData, 5000);

  return () => clearInterval(interval);
}, []);
```

---

## Testing the API

### Test with curl:
```bash
# Get all boxes
curl http://localhost:3001/api/latest

# Get specific box
curl http://localhost:3001/api/latest/box1

# Health check
curl http://localhost:3001/
```

### Test with browser:
Just visit: `http://localhost:3001/api/latest`

---

## CORS Enabled
The backend has CORS enabled, so your frontend can run on a different port (like `localhost:8080`) and still call the API.

---

**Note:** Locations are configured manually (not from GPS sensor). Users set lat/lon once when deploying a box.
