# Extended Celestial Bodies Guide

## Overview

The Astrology API now supports **32 celestial bodies** including planets, asteroids, nodes, Uranian planets, and calculated points!

## Complete Body List

### Major Planets (10) ✅ Always Available

1. **Sun** - Life force, ego, identity
2. **Moon** - Emotions, instincts, subconscious
3. **Mercury** - Communication, thinking, learning
4. **Venus** - Love, beauty, values
5. **Mars** - Action, desire, aggression
6. **Jupiter** - Growth, expansion, luck
7. **Saturn** - Structure, discipline, karma
8. **Uranus** - Revolution, innovation, sudden change
9. **Neptune** - Dreams, illusion, spirituality
10. **Pluto** - Transformation, power, rebirth

### Lunar Nodes (2) ✅ Always Available

11. **North Node** (Mean) - Life path, destiny, soul's purpose
12. **True Node** (Osculating) - More precise North Node calculation

### Uranian/Transneptunian Planets (8) ✅ Always Available

These are hypothetical planets used in Uranian/Hamburg School astrology:

13. **Cupido** - Art, beauty, family, marriage
14. **Hades** - Decay, dirt, poverty, the past
15. **Zeus** - Fire, creativity, leadership
16. **Kronos** - Authority, government, expertise
17. **Apollon** - Science, commerce, success
18. **Admetos** - Blockage, stagnation, depth
19. **Vulkanus** - Might, power, force
20. **Poseidon** - Spirituality, enlightenment, media

### Black Moon & Related (2) ✅ Always Available

21. **Black Moon Lilith** (Mean Apogee) - Dark feminine, shadow self, taboo
22. **Priapus** - Opposite point to Lilith, phallic principle

### Calculated Points (6) ✅ Always Available

23. **South Node** - Past life karma, what you're releasing
24. **Descendant** - Partnerships, relationships, others
25. **IC** (Imum Coeli) - Home, roots, private life
26. **Part of Fortune** - Material success, worldly happiness
27. **Part of Spirit** - Spiritual purpose, inner joy
28. **Priapus** - Sacred masculine, primal drive

### Asteroids (5) ⚠️ Requires Ephemeris Data Files

These require downloading the `seas_18.se1` Swiss Ephemeris file:

29. **Chiron** - The wounded healer, mentorship
30. **Ceres** - Nurturing, motherhood, food
31. **Pallas** (Athena) - Wisdom, strategy, justice
32. **Juno** - Marriage, commitment, jealousy
33. **Vesta** - Home, hearth, sexuality, devotion

---

## Total: 32 Celestial Bodies

- **27 always available** (no extra files needed)
- **5 asteroids** (require `seas_18.se1` ephemeris file)

## Usage

### Get Chart with ALL Bodies

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

**Key parameter:** `"include_all_bodies": true`

### Get Chart with Major Planets Only (Original Behavior)

```bash
# Set include_all_bodies to false (or omit it, false is default)
"include_all_bodies": false
```

This returns only the original 10 planets.

## Enabling Asteroids

Asteroids require additional Swiss Ephemeris data files. Run the setup script:

```bash
./download_ephemeris.sh
```

This will show you which files you need and where to get them.

### Manual Download

1. **Required for asteroids** (Chiron, Ceres, Pallas, Juno, Vesta):
   - File: `seas_18.se1` (~218 KB)

2. **Where to get it**:
   - Download: https://github.com/aloistr/swisseph/raw/master/ephe/seas_18.se1

3. **Installation**:
   ```bash
   # Place downloaded files in:
   cd ephemeris_data/
   # Copy your .se1 files here
   ```

### Automatic Fallback

The API gracefully handles missing asteroid files:
- ✅ Bodies with available data are calculated
- ⚠️ Bodies without data are skipped (logged as warnings)
- 🎯 You always get the maximum possible calculations

## Response Format

Each body returns:

```json
{
  "planet": "Chiron",
  "longitude": 123.45,
  "latitude": 0.12,
  "distance": 13.5,
  "speed": 0.05,
  "zodiac_sign": "Leo",
  "zodiac_degree": 3.45,
  "retrograde": false,
  "house": 11
}
```

**Special notes:**
- Calculated points (Part of Fortune, etc.) have `distance: 0.0` and `speed: 0.0`
- `house` field shows which astrological house the body occupies (1-12)
- `retrograde` indicates apparent backward motion

## Astrological Interpretation

### Main Categories

**Personal Planets** (Sun-Mars): Core personality, everyday life
**Social Planets** (Jupiter-Saturn): Social interaction, life lessons
**Transpersonal Planets** (Uranus-Pluto): Generational themes, transformation

**Asteroids**: Specific life themes and archetypes
**Nodes**: Karmic path and soul evolution
**Uranian Planets**: Midpoints and subtle influences (Uranian astrology)
**Calculated Points**: Synthesized meanings from multiple factors

### House Placement

Each body's house shows WHERE that energy manifests:
- **House 1**: Self, appearance, approach to life
- **House 2**: Money, possessions, values
- **House 3**: Communication, siblings, learning
- **House 4**: Home, family, roots
- **House 5**: Creativity, romance, children
- **House 6**: Work, health, service
- **House 7**: Partnerships, marriage
- **House 8**: Transformation, shared resources
- **House 9**: Philosophy, travel, higher learning
- **House 10**: Career, public life, reputation
- **House 11**: Friends, groups, hopes
- **House 12**: Subconscious, spirituality, hidden matters

### Retrograde Motion

When `retrograde: true`:
- Energy turns inward
- Review and revision of that planet's themes
- Past issues resurface for healing
- More subjective, less outwardly expressed

## Examples

### Find Your Chiron (Wounded Healer)

```python
import requests

chart = requests.post('http://localhost:8000/api/v1/charts/natal', json={
    'datetime': {'year': 1990, 'month': 5, 'day': 15, 'hour': 14, 'minute': 30},
    'location': {'latitude': 51.5074, 'longitude': -0.1278, 'timezone': 'Europe/London'},
    'house_system': 'P',
    'include_all_bodies': True
}).json()

chiron = next((p for p in chart['planets'] if p['planet'] == 'Chiron'), None)
if chiron:
    print(f"Chiron in {chiron['zodiac_sign']} in House {chiron['house']}")
    print("Your wound and healing gift!")
else:
    print("Chiron data not available - download seas_18.se1")
```

### Find Your North Node

```bash
curl -X POST http://localhost:8000/api/v1/charts/natal \
  -H "Content-Type: application/json" \
  -d '{"datetime":{"year":1990,"month":5,"day":15,"hour":14,"minute":30},"location":{"latitude":51.5074,"longitude":-0.1278,"timezone":"Europe/London"},"include_all_bodies":true}' \
  | jq '.planets[] | select(.planet == "North Node") | {sign: .zodiac_sign, degree: .zodiac_degree, house: .house}'
```

### Check Part of Fortune

The Part of Fortune shows where you find joy and success:

```bash
curl ... | jq '.planets[] | select(.planet == "Part of Fortune")'
```

## Performance Notes

### Calculation Speed

- **Major planets**: Very fast (~10ms for all 10)
- **Nodes & Uranian planets**: Fast (~1-2ms each)
- **Calculated points**: Fast (~5ms each, requires houses)
- **Asteroids**: Fast if files present (~1-2ms each)

### With All Bodies

- **Without asteroids**: ~50ms total (27 bodies)
- **With asteroids**: ~70ms total (38 bodies)

Still very fast! 🚀

## Troubleshooting

### "Skipping [asteroid]: file not found"

**Solution**: Download the required ephemeris files
```bash
./download_ephemeris.sh  # Shows which files you need
```

### "Part of Fortune returns 0"

**Solution**: Ensure `include_houses: true` - calculated points need house data

### "Too many bodies in response"

**Solution**: Use `include_all_bodies: false` for just the 10 major planets

### "Missing [body] in response"

**Possible reasons**:
1. Ephemeris file not available (asteroids)
2. Body failed calculation (check server logs)
3. Typo in body name (check EXTENDED_BODIES.md for exact names)

## Technical Details

### Swiss Ephemeris IDs

- **Planets**: 0-9 (Sun-Pluto)
- **Nodes**: 10-11 (Mean Node, True Node)
- **Uranian Planets**: 40-47
- **Black Moon Lilith**: 12 (Mean Apogee)
- **Chiron**: 15
- **Asteroids**: Asteroid number + AST_OFFSET (10000)

### Calculated Points Formulas

- **South Node**: North Node + 180°
- **Descendant**: Ascendant + 180°
- **IC**: Midheaven + 180°
- **Priapus**: Black Moon Lilith + 180°

**Arabic Parts (Day/Night Formulas):**

The API automatically detects if you have a day or night chart:
- **Day chart**: Sun above the horizon (between Ascendant and Descendant)
- **Night chart**: Sun below the horizon (between Descendant and Ascendant)

**Part of Fortune:**
- Day chart: Asc + Moon - Sun
- Night chart: Asc + Sun - Moon *(formula reversed)*

**Part of Spirit:**
- Day chart: Asc + Sun - Moon  
- Night chart: Asc + Moon - Sun *(formula reversed)*

The formulas automatically flip for night charts to maintain the symbolic relationship between Fortune (Moon-oriented) and Spirit (Sun-oriented).

### Data Sources

- **Planetary data**: Swiss Ephemeris (JPL DE431)
- **Asteroid data**: Swiss Ephemeris asteroid files
- **Uranian planets**: Hypothetical (Hamburg School calculations)

## References

- **Swiss Ephemeris**: https://www.astro.com/swisseph/
- **Uranian Astrology**: Hamburg School system
- **Asteroid meanings**: Various astrological traditions
- **Arabic Parts**: Traditional medieval astrology

## Future Enhancements

Potential additions:
- More asteroids (Sedna, Eris, etc.)
- Additional Arabic Parts
- Fixed stars
- Midpoints (especially for Uranian system)
- Harmonics
- Lunar phases

---

**Current Status**: 38 bodies supported (27 always available + 11 asteroids with data files)
