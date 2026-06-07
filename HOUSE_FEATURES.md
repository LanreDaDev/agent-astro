# House Calculation Features

## Overview

The Astrology API now includes complete house calculation support! Houses are one of the fundamental components of astrological charts, dividing the sky into 12 sections based on the Earth's daily rotation.

## What's New

### ✨ New Endpoints

1. **`POST /api/v1/charts/houses`** - Calculate astrological houses
2. **`POST /api/v1/charts/natal`** - Generate complete natal/birth charts

### ✨ New Features

- **12 House Cusps**: Calculate all 12 house boundaries
- **Multiple House Systems**: Support for 7 different house systems
- **Ascendant (Rising Sign)**: Your 1st house cusp
- **Midheaven (MC)**: Your 10th house cusp
- **Vertex**: Secondary angle point
- **Planet-in-House**: Automatic assignment of planets to houses

## House Systems Supported

| Code | Name | Description |
|------|------|-------------|
| `P` | **Placidus** | Most commonly used, time-based |
| `K` | **Koch** | Similar to Placidus, popular in Europe |
| `O` | **Porphyrius** | Space-based, older system |
| `R` | **Regiomontanus** | Medieval system, still widely used |
| `C` | **Campanus** | Prime vertical system |
| `E` | **Equal** | Each house is exactly 30 degrees |
| `W` | **Whole Sign** | Ancient system, each sign = one house |

## Usage Examples

### Calculate Houses Only

```bash
curl -X POST http://localhost:8000/api/v1/charts/houses \
  -H "Content-Type: application/json" \
  -d '{
    "datetime": {
      "year": 2026,
      "month": 6,
      "day": 6,
      "hour": 12,
      "minute": 0
    },
    "location": {
      "latitude": 40.7128,
      "longitude": -74.0060,
      "timezone": "America/New_York"
    },
    "house_system": "P"
  }'
```

**Response:**
```json
{
  "house_cusps": [
    {
      "house_number": 1,
      "longitude": 157.10,
      "zodiac_sign": "Virgo",
      "zodiac_degree": 7.10
    },
    // ... 11 more houses
  ],
  "ascendant": 157.10,
  "midheaven": 63.11,
  "vertex": 305.17,
  "house_system": "P",
  "house_system_name": "Placidus"
}
```

### Complete Natal Chart

```bash
curl -X POST http://localhost:8000/api/v1/charts/natal \
  -H "Content-Type: application/json" \
  -d '{
    "datetime": {
      "year": 1990,
      "month": 5,
      "day": 15,
      "hour": 14,
      "minute": 30
    },
    "location": {
      "latitude": 51.5074,
      "longitude": -0.1278,
      "timezone": "Europe/London"
    },
    "house_system": "P",
    "include_houses": true
  }'
```

**Response:**
```json
{
  "planets": [
    {
      "planet": "Sun",
      "longitude": 54.45,
      "zodiac_sign": "Taurus",
      "zodiac_degree": 24.45,
      "retrograde": false,
      "house": 9,  // ← Planet is in the 9th house!
      // ... other planet data
    },
    {
      "planet": "Moon",
      "longitude": 297.93,
      "zodiac_sign": "Capricorn",
      "zodiac_degree": 27.93,
      "retrograde": false,
      "house": 5,  // ← Moon is in the 5th house!
      // ... other planet data
    }
    // ... all 10 planets
  ],
  "houses": {
    "house_cusps": [ /* all 12 houses */ ],
    "ascendant": 274.24,
    "midheaven": 208.47,
    "vertex": 134.21
  }
}
```

## Understanding the Results

### House Cusps

Each house cusp tells you where that house begins:
- **House 1** (Ascendant): Your rising sign, how others see you
- **House 4**: Home, family, roots
- **House 7** (Descendant): Partnerships, relationships
- **House 10** (Midheaven): Career, public life, reputation

### Ascendant (Rising Sign)

The Ascendant is the zodiac degree rising on the eastern horizon at your birth time. It's the cusp of your 1st house and represents:
- Your outward personality
- First impressions you make
- Physical appearance
- Approach to life

**Example:** Ascendant at 157.10° = 7° Virgo rising

### Midheaven (MC)

The Midheaven is the highest point in your chart (10th house cusp) and represents:
- Career and vocation
- Public image
- Life goals and aspirations
- Authority and achievement

**Example:** Midheaven at 63.11° = 3° Gemini

### Planet-in-House

When you get a natal chart, each planet shows which house it occupies:
- **Sun in 9th house**: Focus on philosophy, travel, higher education
- **Moon in 5th house**: Emotional connection to creativity, children, romance
- **Venus in 7th house**: Love and beauty expressed through partnerships

## Astrological Interpretation

### The 12 Houses

1. **1st House (Self)**: Identity, appearance, first impressions
2. **2nd House (Values)**: Money, possessions, self-worth
3. **3rd House (Communication)**: Siblings, learning, local travel
4. **4th House (Home)**: Family, roots, emotional foundation
5. **5th House (Creativity)**: Romance, children, self-expression
6. **6th House (Health)**: Work, routine, wellness
7. **7th House (Partnerships)**: Marriage, business partners, open enemies
8. **8th House (Transformation)**: Death, rebirth, shared resources
9. **9th House (Philosophy)**: Higher education, travel, beliefs
10. **10th House (Career)**: Public life, reputation, authority
11. **11th House (Community)**: Friends, groups, hopes and dreams
12. **12th House (Spirituality)**: Subconscious, isolation, hidden matters

## Technical Details

### How Houses Are Calculated

1. **Time & Location**: Houses require both birth time and geographic location
2. **Ecliptic Division**: Different systems divide the ecliptic differently
3. **House System**: The mathematical method used (Placidus, Koch, etc.)
4. **Planet Assignment**: Planets are assigned to houses based on their ecliptic longitude

### Planet-to-House Algorithm

The API automatically determines which house each planet occupies by:
1. Taking the planet's ecliptic longitude (0-360°)
2. Comparing it to the house cusp longitudes
3. Finding which house "slice" the planet falls into
4. Handling the wraparound at 0° Aries correctly

### Accuracy

- Uses Swiss Ephemeris for maximum accuracy
- Handles all edge cases (polar regions, midnight births, etc.)
- Supports historical dates (1900-2100)
- Proper timezone and DST handling

## Common Use Cases

### Birth Chart Analysis

Get a complete snapshot of someone's astrological makeup:
```python
import requests

chart = requests.post('http://localhost:8000/api/v1/charts/natal', json={
    "datetime": {"year": 1990, "month": 5, "day": 15, "hour": 14, "minute": 30},
    "location": {"latitude": 51.5074, "longitude": -0.1278, "timezone": "Europe/London"},
    "house_system": "P",
    "include_houses": True
}).json()

# Find which house the Sun is in
sun = next(p for p in chart['planets'] if p['planet'] == 'Sun')
print(f"Sun in {sun['zodiac_sign']} in the {sun['house']}th house")

# Get the rising sign
asc_sign = chart['houses']['house_cusps'][0]['zodiac_sign']
print(f"Ascendant in {asc_sign}")
```

### Compare House Systems

See how different house systems affect the chart:
```bash
for system in P K O E W; do
  echo "House System: $system"
  curl -s -X POST http://localhost:8000/api/v1/charts/houses \
    -H "Content-Type: application/json" \
    -d "{\"datetime\":{\"year\":2000,\"month\":1,\"day\":1,\"hour\":12,\"minute\":0},\"location\":{\"latitude\":40.7128,\"longitude\":-74.0060,\"timezone\":\"America/New_York\"},\"house_system\":\"$system\"}" \
    | jq '.ascendant, .midheaven'
done
```

### Solar Return Chart

Calculate your solar return (when Sun returns to birth position):
```bash
# Use your birth time and current year
curl -X POST http://localhost:8000/api/v1/charts/natal \
  -H "Content-Type: application/json" \
  -d '{
    "datetime": {"year": 2026, "month": 5, "day": 15, "hour": 14, "minute": 30},
    "location": {"latitude": 40.7128, "longitude": -74.0060, "timezone": "America/New_York"},
    "house_system": "P",
    "include_houses": true
  }'
```

## Testing

Run house calculation tests:
```bash
pytest tests/test_api/test_charts.py -v
```

All 5 new tests should pass:
- ✅ test_calculate_houses
- ✅ test_calculate_natal_chart
- ✅ test_natal_chart_without_houses
- ✅ test_different_house_systems
- ✅ test_invalid_house_system

## What's Next?

With houses now implemented, future features could include:
- **Aspects** between planets (conjunctions, trines, squares, etc.)
- **Aspect patterns** (T-squares, Grand Trines, Yods)
- **Transits** (current planets vs natal planets)
- **Progressions** (secondary progressions, solar arc)
- **Synastry** (relationship compatibility between two charts)
- **Composite charts** (midpoint charts for relationships)

## Support

For more information:
- **API Docs**: http://localhost:8000/docs
- **Full README**: See [README.md](README.md)
- **Quick Start**: See [QUICKSTART.md](QUICKSTART.md)
