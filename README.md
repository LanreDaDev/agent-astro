# Astrology API with FastAPI and Swiss Ephemeris

A modern REST API for astrological calculations using FastAPI and the Swiss Ephemeris library (Pyswisseph). Calculate accurate planetary positions for the major planets with support for timezones and historical/future dates.

## Features

- **Transit Aspects**: See how current planets aspect your natal chart - perfect for timing! (NEW!)
- **Aspects**: Major aspects (conjunction, trine, square, sextile, opposition) + 7 minor aspects (quintile, septile, quincunx, etc.)
- **32 Celestial Bodies**: Major planets, asteroids, nodes, Uranian planets, calculated points
- **Planetary Positions**: Calculate positions for all 10 major planets (Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto)
- **Asteroids**: Chiron, Ceres, Pallas, Juno, Vesta (the 5 main asteroids)
- **Lunar Nodes**: North Node (Mean & True), South Node
- **Uranian Planets**: Zeus, Apollon, Vulkanus, and 5 others (Hamburg School)
- **Calculated Points**: Part of Fortune, Part of Spirit, IC, Descendant, Priapus (with traditional sect-based formulas)
- **Black Moon Lilith**: Mean Apogee calculation
- **House Calculations**: Full support for astrological houses with multiple house systems
- **Complete Natal Charts**: Generate birth charts with all bodies, houses, and assignments
- **Location Lookup**: Convert place names to coordinates and timezones automatically
- **Ascendant & Midheaven**: Calculate important chart angles
- **Multiple House Systems**: Placidus, Koch, Porphyrius, Equal, Whole Sign, and more
- **Timezone Support**: Proper handling of timezones including DST transitions
- **Zodiac Positions**: Automatic conversion to zodiac signs and degrees
- **Retrograde Detection**: Identifies retrograde motion for all bodies
- **REST API**: Clean, well-documented API with automatic OpenAPI/Swagger documentation
- **High Accuracy**: Uses Swiss Ephemeris for astronomical calculations

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd agent-astro
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up ephemeris data (optional but recommended):**
   
   The Swiss Ephemeris library can work with built-in approximations (Moshier ephemeris) but for higher accuracy, download the ephemeris data files:
   
   ```bash
   # Create ephemeris data directory (already exists)
   mkdir -p ephemeris_data
   
   # Download Swiss Ephemeris files (covers 1800-2400)
   # Visit: https://www.astro.com/ftp/swisseph/ephe/
   # Download these files to ephemeris_data/:
   # - sepl_18.se1 (planets)
   # - semo_18.se1 (moon)
   # - seas_18.se1 (asteroids, optional)
   ```
   
   Or use curl:
   ```bash
   cd ephemeris_data
   curl -O https://www.astro.com/ftp/swisseph/ephe/sepl_18.se1
   curl -O https://www.astro.com/ftp/swisseph/ephe/semo_18.se1
   cd ..
   ```

5. **Create environment file (optional):**
   ```bash
   cp .env.example .env
   # Edit .env if you need to customize settings
   ```

## Running the API

Start the development server with uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API Base**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check

Check API status and ephemeris data availability:

```bash
curl http://localhost:8000/api/v1/health
```

### Location Lookup

**GET** `/api/v1/location/lookup`

Convert place names to coordinates and timezones:

```bash
curl "http://localhost:8000/api/v1/location/lookup?query=New%20York"
```

Response:
```json
{
  "address": "New York, United States",
  "latitude": 40.7127281,
  "longitude": -74.0060152,
  "timezone": "America/New_York"
}
```

This is perfect for when you don't know the exact coordinates! Just enter a city name and get everything you need for chart calculations.

**Try these locations:**
- `London, UK`
- `Paris, France`
- `Tokyo, Japan`
- `Sydney, Australia`
- `Los Angeles, CA`

### Calculate All Planetary Positions

**POST** `/api/v1/planets/positions`

Calculate positions for all major planets:

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

Response:
```json
{
  "planets": [
    {
      "planet": "Sun",
      "longitude": 75.123,
      "latitude": 0.0,
      "distance": 1.014,
      "speed": 0.958,
      "zodiac_sign": "Gemini",
      "zodiac_degree": 15.123,
      "retrograde": false,
      "house": null
    },
    ...
  ],
  "calculated_at": "2026-06-06T12:00:00Z",
  "request_datetime": {...},
  "request_location": {...}
}
```

### Get Single Planet Position

**GET** `/api/v1/planets/{planet_name}/position`

Calculate position for a specific planet:

```bash
curl "http://localhost:8000/api/v1/planets/Sun/position?year=2026&month=6&day=6&hour=12&minute=0&latitude=40.7128&longitude=-74.0060&timezone=America/New_York"
```

Valid planet names: `Sun`, `Moon`, `Mercury`, `Venus`, `Mars`, `Jupiter`, `Saturn`, `Uranus`, `Neptune`, `Pluto`

### Get Current Planetary Positions

**GET** `/api/v1/planets/positions/now`

Calculate positions for the current moment:

```bash
curl "http://localhost:8000/api/v1/planets/positions/now?latitude=40.7128&longitude=-74.0060&timezone=America/New_York"
```

### Calculate Houses

**POST** `/api/v1/charts/houses`

Calculate astrological houses for a specific time and location:

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

Response includes:
- All 12 house cusps with zodiac positions
- Ascendant (1st house cusp)
- Midheaven (10th house cusp)
- Vertex point

**Available House Systems:**
- `P` - Placidus (default)
- `K` - Koch
- `O` - Porphyrius
- `R` - Regiomontanus
- `C` - Campanus
- `E` - Equal
- `W` - Whole Sign

### Calculate Complete Natal Chart

**POST** `/api/v1/charts/natal`

Generate a complete birth chart with planets and houses:

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

Response includes:
- All planetary positions with house assignments
- Complete house information
- Ascendant and Midheaven
- Each planet shows which house it occupies

### Complete Workflow Example

Combine location lookup with chart calculation:

```bash
# Step 1: Look up the location
LOCATION=$(curl -s "http://localhost:8000/api/v1/location/lookup?query=Paris,%20France")
LAT=$(echo $LOCATION | jq -r '.latitude')
LON=$(echo $LOCATION | jq -r '.longitude')
TZ=$(echo $LOCATION | jq -r '.timezone')

# Step 2: Calculate natal chart for that location
curl -X POST http://localhost:8000/api/v1/charts/natal \
  -H "Content-Type: application/json" \
  -d "{
    \"datetime\": {\"year\": 1990, \"month\": 5, \"day\": 15, \"hour\": 14, \"minute\": 30},
    \"location\": {\"latitude\": $LAT, \"longitude\": $LON, \"timezone\": \"$TZ\"},
    \"house_system\": \"P\",
    \"include_houses\": true
  }"
```

This workflow lets users just enter "Paris" instead of finding coordinates manually!

### Extended Celestial Bodies

**NEW!** The API now supports 38 celestial bodies:

**Get chart with ALL bodies** (27 available, 38 with asteroid files):
```bash
curl -X POST http://localhost:8000/api/v1/charts/natal \
  -H "Content-Type: application/json" \
  -d '{
    "datetime": {"year": 1990, "month": 5, "day": 15, "hour": 14, "minute": 30},
    "location": {"latitude": 51.5074, "longitude": -0.1278, "timezone": "Europe/London"},
    "house_system": "P",
    "include_houses": true,
    "include_all_bodies": true
  }'
```

**Bodies included:**
- ✅ 10 major planets (always available)
- ✅ 2 lunar nodes (always available)
- ✅ 8 Uranian planets - Zeus, Apollon, Vulkanus, etc. (always available)
- ✅ Black Moon Lilith & Priapus (always available)
- ✅ 6 calculated points - Part of Fortune, IC, Descendant, etc. (always available)
- ⚠️ 11 asteroids - Chiron, Ceres, Pallas, Juno, Vesta, etc. (requires ephemeris files)

**To enable asteroids:**
```bash
./download_ephemeris.sh  # Shows setup instructions
```

See [EXTENDED_BODIES.md](EXTENDED_BODIES.md) for complete details on all 38 bodies.

## Testing

Run the test suite:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api/test_planets.py -v
```

View coverage report:
```bash
open htmlcov/index.html  # On macOS
# or
xdg-open htmlcov/index.html  # On Linux
```

## Configuration

Configuration can be set via environment variables or `.env` file:

- `API_V1_PREFIX`: API route prefix (default: `/api/v1`)
- `EPHEMERIS_PATH`: Path to ephemeris data files (default: `./ephemeris_data`)
- `ENABLE_CORS`: Enable CORS middleware (default: `true`)
- `ALLOWED_ORIGINS`: CORS allowed origins (default: `*`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

## Project Structure

```
agent-astro/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── models/
│   │   └── schemas.py       # Pydantic models
│   ├── api/
│   │   └── endpoints/
│   │       ├── health.py    # Health check
│   │       └── planets.py   # Planetary endpoints
│   ├── services/
│   │   ├── ephemeris.py     # Swiss Ephemeris wrapper
│   │   └── calculator.py    # Calculation service
│   ├── core/
│   │   ├── constants.py     # Astrological constants
│   │   └── exceptions.py    # Custom exceptions
│   └── utils/
│       └── time_converter.py # Time utilities
├── tests/                   # Test suite
├── ephemeris_data/          # Swiss Ephemeris data files
└── requirements.txt         # Python dependencies
```

## Architecture

- **FastAPI**: Modern web framework with automatic OpenAPI documentation
- **Pydantic**: Data validation and settings management
- **Swiss Ephemeris**: High-accuracy astronomical calculations
- **Service Layer**: Separation of business logic from API handlers
- **Timezone Handling**: All calculations in UTC, timezone-aware inputs

## Future Enhancements

This MVP is designed to be extended with:

- **House Calculations**: Support for multiple house systems (Placidus, Koch, etc.)
- **Aspect Calculations**: Conjunctions, trines, squares, sextiles, oppositions
- **Complete Birth Charts**: Full natal chart generation
- **Transit Tracking**: Current and future planetary transits
- **Caching**: Redis cache for frequently requested calculations
- **Rate Limiting**: API rate limiting for production use

## License

This project uses the Swiss Ephemeris library, which is dual-licensed:
- Free for non-commercial use
- Commercial license required for commercial applications

See https://www.astro.com/swisseph/ for details.

## Troubleshooting

### Ephemeris data not available

If you see "ephemeris data may not be available" in the health check, the API will still work using the built-in Moshier ephemeris (less accurate). Download the Swiss Ephemeris data files to `ephemeris_data/` for better accuracy.

### Import errors

Make sure you've activated your virtual environment and installed all dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Timezone errors

Ensure you're using valid IANA timezone strings (e.g., `America/New_York`, `Europe/London`, `Asia/Tokyo`). You can find a list at https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

## Support

For issues or questions, please check:
- Interactive API docs at `/docs`
- This README
- Test files for usage examples
