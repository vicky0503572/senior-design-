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

Returns data from all active weather boxes.

**Response:**
```json
{
  "box1": {
    "box_id": "box1",
    "temperature": 72.5,
    "humidity": 45,
    "pressure": 1013.2,
    "wind_speed": 3.2,
    "wind_direction": 180,
    "rainfall": 0.0,
    "timestamp": "2026-02-11T20:45:32.123456"
  },
  "box2": {
    "box_id": "box2",
    "temperature": 68.3,
    "humidity": 52,
    "pressure": 1015.1,
    "wind_speed": 2.1,
    "wind_direction": 225,
    "rainfall": 0.5,
    "timestamp": "2026-02-11T20:45:35.987654"
  }
}
```

---

### 2. Get Specific Box Data
**GET** `/api/latest/<box_id>`

Returns data from a single weather box.

**Example:** `GET /api/latest/box1`

**Response:**
```json
{
  "box_id": "box1",
  "temperature": 72.5,
  "humidity": 45,
  "pressure": 1013.2,
  "wind_speed": 3.2,
  "wind_direction": 180,
  "rainfall": 0.0,
  "timestamp": "2026-02-11T20:45:32.123456"
}
```

**Error Response (box not found):**
```json
{
  "error": "No data for this box"
}
```
Status Code: `404`

---

### 3. Health Check
**GET** `/`

Check if backend is running and see active boxes.

**Response:**
```json
{
  "status": "running",
  "mqtt_broker": "localhost:1883",
  "active_boxes": ["box1", "box2"],
  "total_readings": 2
}
```

---

## Data Field Definitions

| Field | Type | Unit | Description |
|-------|------|------|-------------|
| `box_id` | string | - | Unique identifier for weather box |
| `temperature` | float | °F | Temperature reading |
| `humidity` | float | % | Relative humidity percentage |
| `pressure` | float | hPa | Atmospheric pressure |
| `wind_speed` | float | m/s | Wind speed |
| `wind_direction` | float | degrees | Wind direction (0-360°, where 0=North) |
| `rainfall` | float | mm | Rainfall amount |
| `timestamp` | string | ISO 8601 | When reading was taken |

---

## Auto-Refresh Strategy

**Option: Polling**
```javascript
// Fetch new data every 5 seconds
setInterval(() => {
  fetch('http://localhost:3001/api/latest')
    .then(res => res.json())
    .then(data => updateDashboard(data));
}, 5000);
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

