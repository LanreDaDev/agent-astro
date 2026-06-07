# Quick Start Guide

## Get Started in 3 Steps

### 1. Install Dependencies

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Start the API

```bash
# Easy way - use the start script
./start.sh

# Or manually
source venv/bin/activate
uvicorn app.main:app --reload
```

The API will start at **http://localhost:8000**

### 3. Try it Out

**Option A: Visit the Interactive Docs**
- Open your browser to http://localhost:8000/docs
- Click on any endpoint to try it out interactively

**Option B: Use curl**

Check health:
```bash
curl http://localhost:8000/api/v1/health
```

Look up a location (NEW!):
```bash
curl "http://localhost:8000/api/v1/location/lookup?query=London,%20UK"
```

Get planetary positions:
```bash
curl -X POST http://localhost:8000/api/v1/planets/positions \
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
    }
  }'
```

Get current positions:
```bash
curl "http://localhost:8000/api/v1/planets/positions/now?latitude=40.7128&longitude=-74.0060&timezone=America/New_York"
```

Get single planet:
```bash
curl "http://localhost:8000/api/v1/planets/Sun/position?year=2026&month=6&day=6&hour=12&minute=0&latitude=40.7128&longitude=-74.0060&timezone=America/New_York"
```

Calculate houses:
```bash
curl -X POST http://localhost:8000/api/v1/charts/houses \
  -H "Content-Type: application/json" \
  -d '{
    "datetime": {"year": 2026, "month": 6, "day": 6, "hour": 12, "minute": 0},
    "location": {"latitude": 40.7128, "longitude": -74.0060, "timezone": "America/New_York"},
    "house_system": "P"
  }'
```

Get complete natal chart:
```bash
curl -X POST http://localhost:8000/api/v1/charts/natal \
  -H "Content-Type: application/json" \
  -d '{
    "datetime": {"year": 1990, "month": 5, "day": 15, "hour": 14, "minute": 30},
    "location": {"latitude": 51.5074, "longitude": -0.1278, "timezone": "Europe/London"},
    "house_system": "P",
    "include_houses": true
  }'
```

## Available Planets

Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto

## Common Timezones

- `America/New_York` (Eastern)
- `America/Chicago` (Central)
- `America/Denver` (Mountain)
- `America/Los_Angeles` (Pacific)
- `Europe/London` (UK)
- `Europe/Paris` (Central Europe)
- `Asia/Tokyo` (Japan)
- `Australia/Sydney` (Australia)

Full list: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

## Response Format

Each planet position includes:
- **planet**: Name of the planet
- **longitude**: Absolute longitude (0-360 degrees)
- **latitude**: Ecliptic latitude
- **distance**: Distance from Earth in AU
- **speed**: Daily motion in degrees
- **zodiac_sign**: Current zodiac sign (Aries, Taurus, etc.)
- **zodiac_degree**: Degree within the sign (0-30)
- **retrograde**: true if planet is in retrograde motion
- **house**: House number (1-12) if houses are calculated

## House Systems

- **P** - Placidus (default, most common)
- **K** - Koch
- **O** - Porphyrius
- **R** - Regiomontanus
- **C** - Campanus
- **E** - Equal
- **W** - Whole Sign

## Testing

Run the test suite:
```bash
source venv/bin/activate
pytest tests/ -v
```

## Optional: Higher Accuracy

For better accuracy, download Swiss Ephemeris data files:

```bash
cd ephemeris_data
curl -O https://www.astro.com/ftp/swisseph/ephe/sepl_18.se1
curl -O https://www.astro.com/ftp/swisseph/ephe/semo_18.se1
cd ..
```

The API works without these files using built-in approximations, but the files provide more accurate results.

## Need Help?

- Full documentation: See [README.md](README.md)
- Interactive API docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc
