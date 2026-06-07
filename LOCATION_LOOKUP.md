# Location Lookup Feature

## Overview

The Location Lookup feature makes it incredibly easy to use the Astrology API - no need to manually find coordinates or timezone strings! Just enter a city name and get everything automatically.

## Why This Feature?

Before:
```json
{
  "location": {
    "latitude": 40.7127281,    // ❌ Had to look this up
    "longitude": -74.0060152,   // ❌ Had to look this up
    "timezone": "America/New_York"  // ❌ Had to look this up
  }
}
```

After:
```bash
# Just enter the city name!
curl "http://localhost:8000/api/v1/location/lookup?query=New%20York"
```

## How It Works

The API uses two powerful libraries:
1. **geopy** with OpenStreetMap's Nominatim - Converts place names to coordinates
2. **timezonefinder** - Determines IANA timezone from coordinates

Both are open-source and free to use!

## Basic Usage

### Simple City Lookup

```bash
curl "http://localhost:8000/api/v1/location/lookup?query=Tokyo"
```

Response:
```json
{
  "address": "東京都, 日本",
  "latitude": 35.6768601,
  "longitude": 139.7638947,
  "timezone": "Asia/Tokyo"
}
```

### City with Country

```bash
curl "http://localhost:8000/api/v1/location/lookup?query=London,%20UK"
```

Response:
```json
{
  "address": "Greater London, England, United Kingdom",
  "latitude": 51.5074456,
  "longitude": -0.1277653,
  "timezone": "Europe/London"
}
```

### City with State

```bash
curl "http://localhost:8000/api/v1/location/lookup?query=Austin,%20TX"
```

Response:
```json
{
  "address": "Austin, Texas, United States",
  "latitude": 30.2711286,
  "longitude": -97.7436995,
  "timezone": "America/Chicago"
}
```

## Complete Workflow

### Python Example

```python
import requests

# Step 1: Look up location
location = requests.get(
    'http://localhost:8000/api/v1/location/lookup',
    params={'query': 'Paris, France'}
).json()

print(f"Found: {location['address']}")
print(f"Coordinates: {location['latitude']}, {location['longitude']}")
print(f"Timezone: {location['timezone']}")

# Step 2: Calculate natal chart
chart = requests.post(
    'http://localhost:8000/api/v1/charts/natal',
    json={
        "datetime": {
            "year": 1990,
            "month": 5,
            "day": 15,
            "hour": 14,
            "minute": 30
        },
        "location": {
            "latitude": location['latitude'],
            "longitude": location['longitude'],
            "timezone": location['timezone']
        },
        "house_system": "P",
        "include_houses": True
    }
).json()

# Show results
sun = next(p for p in chart['planets'] if p['planet'] == 'Sun')
print(f"\nSun: {sun['zodiac_sign']} {sun['zodiac_degree']:.1f}° in House {sun['house']}")
print(f"Ascendant: {chart['houses']['house_cusps'][0]['zodiac_sign']}")
```

### JavaScript Example

```javascript
// Step 1: Look up location
const locationResponse = await fetch(
  'http://localhost:8000/api/v1/location/lookup?query=Sydney,%20Australia'
);
const location = await locationResponse.json();

console.log(`Found: ${location.address}`);
console.log(`Timezone: ${location.timezone}`);

// Step 2: Calculate chart
const chartResponse = await fetch(
  'http://localhost:8000/api/v1/charts/natal',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      datetime: { year: 1990, month: 5, day: 15, hour: 14, minute: 30 },
      location: {
        latitude: location.latitude,
        longitude: location.longitude,
        timezone: location.timezone
      },
      house_system: 'P',
      include_houses: true
    })
  }
);
const chart = await chartResponse.json();

console.log('Sun:', chart.planets[0].zodiac_sign, chart.planets[0].house);
```

### Bash Script Example

```bash
#!/bin/bash

# Look up location
LOCATION=$(curl -s "http://localhost:8000/api/v1/location/lookup?query=Berlin,%20Germany")

# Extract values
LAT=$(echo $LOCATION | jq -r '.latitude')
LON=$(echo $LOCATION | jq -r '.longitude')
TZ=$(echo $LOCATION | jq -r '.timezone')
ADDR=$(echo $LOCATION | jq -r '.address')

echo "Location: $ADDR"
echo "Coordinates: $LAT, $LON"
echo "Timezone: $TZ"
echo ""

# Calculate chart
curl -X POST http://localhost:8000/api/v1/charts/natal \
  -H "Content-Type: application/json" \
  -d "{
    \"datetime\": {\"year\": 1990, \"month\": 5, \"day\": 15, \"hour\": 14, \"minute\": 30},
    \"location\": {\"latitude\": $LAT, \"longitude\": $LON, \"timezone\": \"$TZ\"},
    \"house_system\": \"P\",
    \"include_houses\": true
  }"
```

## Supported Location Formats

The API accepts various formats:

| Format | Example | Works? |
|--------|---------|--------|
| City only | `Tokyo` | ✅ |
| City, Country | `London, UK` | ✅ |
| City, State | `Austin, TX` | ✅ |
| City, State, Country | `Portland, OR, USA` | ✅ |
| Famous place | `Eiffel Tower` | ✅ |
| Address | `1600 Pennsylvania Ave, Washington DC` | ✅ |
| Coordinates | `40.7128,-74.0060` | ✅ |

## Tips for Best Results

### Be Specific

❌ Bad: `Portland` (which Portland?)
✅ Good: `Portland, OR` or `Portland, Maine`

### Use Country Codes

Common country codes:
- `UK` - United Kingdom
- `USA` or `US` - United States
- `FR` - France
- `DE` - Germany
- `JP` - Japan
- `AU` - Australia

### Common Cities

For major cities, just the name works:
- `Tokyo` ✅
- `Paris` ✅
- `London` ✅
- `New York` ✅
- `Berlin` ✅

### Ambiguous Names

If you get unexpected results, add more detail:
- `Cambridge` → Could be UK or MA
- `Cambridge, UK` → Better!
- `Cambridge, Massachusetts` → Even better!

## Error Handling

### Location Not Found

```bash
curl "http://localhost:8000/api/v1/location/lookup?query=NOTAPLACE12345"
```

Response (404):
```json
{
  "detail": "Location not found: NOTAPLACE12345"
}
```

### Empty Query

```bash
curl "http://localhost:8000/api/v1/location/lookup?query="
```

Response (422):
```json
{
  "detail": [
    {
      "loc": ["query", "query"],
      "msg": "ensure this value has at least 2 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

### Timeout

If the geocoding service is slow:
```json
{
  "detail": "Location lookup timed out. Please try again."
}
```

## Rate Limits

The API uses OpenStreetMap's Nominatim service, which has a rate limit:
- **1 request per second**
- Be respectful of the free service

For production use with higher volume, consider:
1. **Caching** - Store common locations in a database
2. **Rate limiting** - Implement your own rate limiting
3. **Commercial service** - Google Maps API, MapBox, etc.

## World Cities Coverage

The location lookup works globally:

### Americas
- 🇺🇸 New York, Los Angeles, Chicago, Houston, Miami
- 🇨🇦 Toronto, Vancouver, Montreal
- 🇲🇽 Mexico City, Guadalajara
- 🇧🇷 São Paulo, Rio de Janeiro
- 🇦🇷 Buenos Aires

### Europe
- 🇬🇧 London, Manchester, Birmingham
- 🇫🇷 Paris, Lyon, Marseille
- 🇩🇪 Berlin, Munich, Hamburg
- 🇮🇹 Rome, Milan, Florence
- 🇪🇸 Madrid, Barcelona, Valencia

### Asia
- 🇯🇵 Tokyo, Osaka, Kyoto
- 🇨🇳 Beijing, Shanghai, Hong Kong
- 🇮🇳 Mumbai, Delhi, Bangalore
- 🇰🇷 Seoul, Busan
- 🇹🇭 Bangkok

### Oceania
- 🇦🇺 Sydney, Melbourne, Brisbane
- 🇳🇿 Auckland, Wellington

### Africa
- 🇿🇦 Cape Town, Johannesburg
- 🇪🇬 Cairo
- 🇰🇪 Nairobi
- 🇳🇬 Lagos

And many more!

## Technical Details

### Libraries Used

**geopy (2.4.0+)**
- Geocoding library for Python
- Uses OpenStreetMap's Nominatim by default
- Free and open-source
- https://geopy.readthedocs.io/

**timezonefinder (6.2.0+)**
- Fast timezone lookup from coordinates
- Uses H3 spatial indexing
- Offline database, no API calls
- https://github.com/jannikmi/timezonefinder

### Data Sources

- **Geocoding**: OpenStreetMap (community-maintained)
- **Timezones**: IANA Time Zone Database

### Accuracy

- **Coordinates**: Typically accurate to ~10 meters for cities
- **Timezones**: 100% accurate using IANA database
- **Address formatting**: Varies by region

## Common Use Cases

### Birth Chart Applications

Users enter their birth city instead of coordinates:
```
"Where were you born?" → "Chicago"
→ API returns coordinates + timezone
→ Calculate exact birth chart
```

### Astrology Report Generator

```python
def generate_report(birth_city, birth_date, birth_time):
    # Look up location
    loc = lookup_location(birth_city)
    
    # Calculate chart
    chart = calculate_natal_chart(birth_date, birth_time, loc)
    
    # Generate report
    return create_report(chart)
```

### Multi-Location Charts

Compare charts for different locations:
```python
cities = ['New York', 'London', 'Tokyo']
for city in cities:
    loc = lookup_location(city)
    chart = calculate_chart(date, time, loc)
    print(f"{city}: {chart['ascendant']}")
```

## Privacy & Security

- **No data stored**: Location lookups are not logged or stored
- **No API keys required**: Uses free OpenStreetMap service
- **No tracking**: No user tracking or analytics
- **Open source**: All code is transparent and auditable

## Future Enhancements

Potential improvements:
- **Caching**: Store popular locations
- **Autocomplete**: Suggest locations as you type
- **Nearest city**: Find closest major city to coordinates
- **Multiple results**: Return top 5 matches when ambiguous
- **Historical locations**: Support ancient cities and changed borders

## Support

For issues or questions:
- **API Docs**: http://localhost:8000/docs
- **Full README**: [README.md](README.md)
- **Test it**: Try different cities in the interactive docs!
