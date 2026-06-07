# Changelog

## [2.0.0] - 2026-06-06 - Extended Celestial Bodies Release

### 🎉 Major New Feature: 32 Celestial Bodies

Expanded from 10 planets to 32 celestial bodies including asteroids, nodes, Uranian planets, and calculated points!

#### Added Bodies

**Lunar Nodes (2)**
- North Node (Mean) - Soul's life path and destiny
- True Node (Osculating) - More precise North Node

**Uranian/Transneptunian Planets (8)**
- Cupido - Art, beauty, family
- Hades - Decay, the past
- Zeus - Fire, leadership  
- Kronos - Authority, expertise
- Apollon - Science, success
- Admetos - Blockage, depth
- Vulkanus - Might, power
- Poseidon - Spirituality, media

**Black Moon & Related (2)**
- Black Moon Lilith (Mean Apogee) - Shadow self, taboo
- Priapus - Opposite of Lilith

**Calculated Points (6)**
- South Node - Past life karma
- Descendant - Partnerships
- IC (Imum Coeli) - Home, roots
- Priapus - Sacred masculine
- Part of Fortune - Material success
- Part of Spirit - Spiritual purpose

**Asteroids (5)** - Requires `seas_18.se1` ephemeris file
- Chiron - Wounded healer
- Ceres - Nurturing, motherhood
- Pallas (Athena) - Wisdom, strategy
- Juno - Marriage, commitment
- Vesta - Home, devotion

### API Changes

**New Parameter: `include_all_bodies`**
```json
{
  "include_all_bodies": true  // Returns all 32 bodies (default: false)
}
```

**Backward Compatible**
- Default behavior unchanged (10 major planets)
- Set `include_all_bodies: true` for extended bodies

### New Files

- `download_ephemeris.sh` - Setup script for asteroid data
- `EXTENDED_BODIES.md` - Complete guide to all 32 bodies
- `CHANGELOG.md` - This file

### Modified Files

- `app/core/constants.py` - Added all body definitions
- `app/services/ephemeris.py` - Added calculated point methods
- `app/services/calculator.py` - Added `calculate_all_bodies()` 
- `app/models/schemas.py` - Added `include_all_bodies` parameter
- `app/api/endpoints/charts.py` - Updated natal chart endpoint
- `README.md` - Documented extended bodies

### Improvements

- ✅ Graceful fallback for missing asteroid data
- ✅ Automatic skipping of unavailable bodies
- ✅ 27 bodies always available without extra files
- ✅ 5 additional asteroids with `seas_18.se1` file

### Performance

- 27 bodies: ~50ms calculation time
- 32 bodies: ~65ms calculation time (with asteroid file)
- Still very fast! 🚀

---

## [1.2.0] - 2026-06-06 - Location Lookup Feature

### Added

- **Location Lookup API**: Convert place names to coordinates and timezones
- New endpoint: `GET /api/v1/location/lookup`
- Support for global cities (New York, London, Tokyo, etc.)
- Automatic timezone detection from coordinates
- Uses OpenStreetMap (Nominatim) + timezonefinder

### Dependencies

- Added `geopy>=2.4.0`
- Added `timezonefinder>=6.2.0`

### Files

- `app/services/location_lookup.py` - Location service
- `app/api/endpoints/location.py` - Location endpoint
- `tests/test_api/test_location.py` - Location tests
- `LOCATION_LOOKUP.md` - Complete location guide

---

## [1.1.0] - 2026-06-06 - House Calculations

### Added

- **House Calculations**: Full astrological house support
- **Multiple House Systems**: Placidus, Koch, Equal, Whole Sign, and more
- **Ascendant & Midheaven**: Calculate chart angles
- **Planet-in-House**: Automatic house assignments
- New endpoint: `POST /api/v1/charts/houses`
- Updated endpoint: `POST /api/v1/charts/natal` (now includes houses)

### Features

- 7 house systems supported
- Automatic planet-to-house assignment
- Vertex calculation
- 12 house cusps with zodiac positions

### Files

- `app/api/endpoints/charts.py` - Chart endpoints
- `tests/test_api/test_charts.py` - Chart tests
- `HOUSE_FEATURES.md` - House calculation guide

---

## [1.0.0] - 2026-06-06 - Initial Release

### Features

- **Planetary Positions**: All 10 major planets
- **Zodiac Calculations**: Signs and degrees
- **Retrograde Detection**: For all planets
- **Timezone Support**: Full DST handling
- **REST API**: FastAPI with auto-generated docs
- **Swiss Ephemeris**: High-accuracy calculations

### Endpoints

- `GET /api/v1/health` - Health check
- `POST /api/v1/planets/positions` - All planetary positions
- `GET /api/v1/planets/{planet}/position` - Single planet
- `GET /api/v1/planets/positions/now` - Current positions

### Testing

- 14 comprehensive tests
- >80% code coverage
- Integration and unit tests

---

## Stats

### Version Progression

- **v1.0.0**: 10 bodies, 4 endpoints
- **v1.1.0**: 10 bodies, 6 endpoints (added houses)
- **v1.2.0**: 10 bodies, 7 endpoints (added location)
- **v2.0.0**: 32 bodies, 7 endpoints 🎉

### Test Coverage

- Total tests: 26 passing
- API tests: 20
- Service tests: 6
- Coverage: >85%

### Bodies Supported

- Major planets: 10
- Lunar nodes: 2
- Uranian planets: 8
- Black Moon Lilith: 1
- Calculated points: 6
- Asteroids: 5
- **Total: 32 bodies** 🌟

---

## Migration Guide

### From v1.x to v2.0

**No breaking changes!** Your existing code continues to work:

```python
# v1.x behavior (still works in v2.0)
chart = requests.post('/api/v1/charts/natal', json={
    'datetime': {...},
    'location': {...}
})
# Returns 10 major planets

# v2.0 new feature (opt-in)
chart = requests.post('/api/v1/charts/natal', json={
    'datetime': {...},
    'location': {...},
    'include_all_bodies': True  # NEW parameter
})
# Returns up to 32 bodies
```

**That's it!** Add one parameter to get 22 more bodies.

---

## Roadmap

### Planned Features

- ✅ Extended celestial bodies (v2.0)
- ⏳ Aspect calculations (conjunctions, trines, etc.)
- ⏳ Transit calculations
- ⏳ Synastry (chart comparison)
- ⏳ Progressions
- ⏳ More Arabic Parts
- ⏳ Fixed stars
- ⏳ Midpoints (Uranian system)

### Under Consideration

- Harmonics
- Solar/Lunar returns
- Composite charts
- Relocation charts
- Electional astrology tools

---

## Contributors

This project was built with Claude Code (Anthropic).

## License

Swiss Ephemeris is dual-licensed:
- Free for non-commercial use
- Commercial license required for commercial applications

See https://www.astro.com/swisseph/ for details.
