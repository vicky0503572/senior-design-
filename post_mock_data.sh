#!/bin/bash

# Weather Station Mock Data Script
# Creates 10 weather boxes with locations around Fort Worth, TX area

API_URL="http://localhost:3001"

echo "🌤️  Posting mock data for 10 weather boxes around Fort Worth..."
echo ""

# Box 1 - TCU Campus
echo "📍 Box 1: TCU Campus"
curl -X POST "$API_URL/api/location/box1" \
  -H "Content-Type: application/json" \
  -d '{"lat": 32.7095, "lon": -97.3635, "name": "TCU Campus"}'
echo ""

curl -X POST "$API_URL/api/mock/box1" \
  -H "Content-Type: application/json" \
  -d '{"temperature_f": 72.5, "temperature_c": 22.5, "humidity": 55.2, "pressure": 1013.2, "wind_speed": 3.8, "wind_direction": 180, "rainfall": 0.5}'
echo -e "\n"

# Box 2 - Downtown Fort Worth
echo "📍 Box 2: Downtown Fort Worth"
curl -X POST "$API_URL/api/location/box2" \
  -H "Content-Type: application/json" \
  -d '{"lat": 32.7555, "lon": -97.3308, "name": "Downtown"}'
echo ""

curl -X POST "$API_URL/api/mock/box2" \
  -H "Content-Type: application/json" \
  -d '{"temperature_f": 74.2, "temperature_c": 23.4, "humidity": 52.1, "pressure": 1012.8, "wind_speed": 5.2, "wind_direction": 225, "rainfall": 0.0}'
echo -e "\n"

# Box 3 - Fort Worth Botanic Garden
echo "📍 Box 3: Botanic Garden"
curl -X POST "$API_URL/api/location/box3" \
  -H "Content-Type: application/json" \
  -d '{"lat": 32.7356, "lon": -97.3619, "name": "Botanic Garden"}'
echo ""

curl -X POST "$API_URL/api/mock/box3" \
  -H "Content-Type: application/json" \
  -d '{"temperature_f": 71.8, "temperature_c": 22.1, "humidity": 58.5, "pressure": 1013.5, "wind_speed": 2.1, "wind_direction": 90, "rainfall": 1.2}'
echo -e "\n"

# Box 4 - Fort Worth Zoo
echo "📍 Box 4: Fort Worth Zoo"
curl -X POST "$API_URL/api/location/box4" \
  -H "Content-Type: application/json" \
  -d '{"lat": 32.7195, "lon": -97.3539, "name": "FW Zoo"}'
echo ""

curl -X POST "$API_URL/api/mock/box4" \
  -H "Content-Type: application/json" \
  -d '{"temperature_f": 73.1, "temperature_c": 22.8, "humidity": 54.8, "pressure": 1013.0, "wind_speed": 4.5, "wind_direction": 135, "rainfall": 0.3}'
echo -e "\n"

# Box 5 - Stockyards
echo "📍 Box 5: Stockyards"
curl -X POST "$API_URL/api/location/box5" \
  -H "Content-Type: application/json" \
  -d '{"lat": 32.7896, "lon": -97.3469, "name": "Stockyards"}'
echo ""

curl -X POST "$API_URL/api/mock/box5" \
  -H "Content-Type: application/json" \
  -d '{"temperature_f": 75.6, "temperature_c": 24.2, "humidity": 49.3, "pressure": 1012.5, "wind_speed": 6.8, "wind_direction": 270, "rainfall": 0.0}'
echo -e "\n"

# Box 6 - Trinity Park
echo "📍 Box 6: Trinity Park"
curl -X POST "$API_URL/api/location/box6" \
  -H "Content-Type: application/json" \
  -d '{"lat": 32.7467, "lon": -97.3542, "name": "Trinity Park"}'
echo ""

curl -X POST "$API_URL/api/mock/box6" \
  -H "Content-Type: application/json" \
  -d '{"temperature_f": 70.9, "temperature_c": 21.6, "humidity": 61.2, "pressure": 1013.8, "wind_speed": 1.8, "wind_direction": 45, "rainfall": 2.1}'
echo -e "\n"

# Box 7 - University of North Texas Health Science Center
echo "📍 Box 7: UNTHSC"
curl -X POST "$API_URL/api/location/box7" \
  -H "Content-Type: application/json" \
  -d '{"lat": 32.7351, "lon": -97.3642, "name": "UNTHSC"}'
echo ""

curl -X POST "$API_URL/api/mock/box7" \
  -H "Content-Type: application/json" \
  -d '{"temperature_f": 72.3, "temperature_c": 22.4, "humidity": 56.7, "pressure": 1013.1, "wind_speed": 3.2, "wind_direction": 315, "rainfall": 0.8}'
echo -e "\n"

# Box 8 - Cultural District
echo "📍 Box 8: Cultural District"
curl -X POST "$API_URL/api/location/box8" \
  -H "Content-Type: application/json" \
  -d '{"lat": 32.7478, "lon": -97.3711, "name": "Cultural District"}'
echo ""

curl -X POST "$API_URL/api/mock/box8" \
  -H "Content-Type: application/json" \
  -d '{"temperature_f": 73.8, "temperature_c": 23.2, "humidity": 53.4, "pressure": 1012.9, "wind_speed": 4.1, "wind_direction": 200, "rainfall": 0.2}'
echo -e "\n"

# Box 9 - Ridglea
echo "📍 Box 9: Ridglea"
curl -X POST "$API_URL/api/location/box9" \
  -H "Content-Type: application/json" \
  -d '{"lat": 32.7389, "lon": -97.4021, "name": "Ridglea"}'
echo ""

curl -X POST "$API_URL/api/mock/box9" \
  -H "Content-Type: application/json" \
  -d '{"temperature_f": 71.2, "temperature_c": 21.8, "humidity": 59.8, "pressure": 1013.4, "wind_speed": 2.9, "wind_direction": 160, "rainfall": 1.5}'
echo -e "\n"

# Box 10 - Arlington Heights
echo "📍 Box 10: Arlington Heights"
curl -X POST "$API_URL/api/location/box10" \
  -H "Content-Type: application/json" \
  -d '{"lat": 32.7221, "lon": -97.3412, "name": "Arlington Heights"}'
echo ""

curl -X POST "$API_URL/api/mock/box10" \
  -H "Content-Type: application/json" \
  -d '{"temperature_f": 74.5, "temperature_c": 23.6, "humidity": 51.9, "pressure": 1012.7, "wind_speed": 5.5, "wind_direction": 250, "rainfall": 0.1}'
echo -e "\n"

echo ""
echo "✅ Done! 10 weather boxes with data posted."
echo ""
echo "📍 Verify locations:"
curl -s "$API_URL/api/locations"
echo ""
echo ""
echo "🌐 View on dashboard: http://localhost:5173"
echo "📊 API data: $API_URL/api/latest"