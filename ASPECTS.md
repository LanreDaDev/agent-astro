# Aspects Calculation Guide

## Overview

The Astrology API now supports **major and minor aspects** calculation! Calculate conjunctions, oppositions, trines, squares, sextiles, and 7 minor aspects between all celestial bodies in a chart.

## Supported Aspects

### The Five Major Aspects

| Aspect | Angle | Default Orb | Nature | Meaning |
|--------|-------|-------------|--------|---------|
| **Conjunction** | 0° | 8° | Neutral/Intense | Unity, blending of energies, emphasis |
| **Sextile** | 60° | 6° | Harmonious | Opportunity, talent, ease |
| **Square** | 90° | 7° | Challenging | Tension, conflict, growth through friction |
| **Trine** | 120° | 8° | Harmonious | Flow, ease, natural gifts |
| **Opposition** | 180° | 8° | Challenging | Polarity, awareness, balance needed |

### The Seven Minor Aspects (NEW!)

| Aspect | Angle | Default Orb | Nature | Meaning |
|--------|-------|-------------|--------|---------|
| **Semi-Sextile** | 30° | 3° | Mildly Challenging | Discomfort, "next-door neighbor" energy, requires adjustment |
| **Semi-Square** | 45° | 3° | Mildly Challenging | Minor friction, low-level stress, annoyance |
| **Septile** | 51.43° | 2° | Mystical/Fated | Destiny, occult, weird synchronicities |
| **Quintile** | 72° | 2° | Creative/Genius | Unique talents, specialized gifts, creative brilliance |
| **Sesquiquadrate** | 135° | 3° | Mildly Challenging | Persistent irritation, requires adjustment |
| **Biquintile** | 144° | 2° | Creative/Genius | Another genius aspect, double quintile energy |
| **Quincunx (Inconjunct)** | 150° | 3° | Very Challenging | The "blind spot," nothing in common, constant awkward adjustments |

## API Usage

### Calculate All Aspects

**Endpoint:** `POST /api/v1/aspects`

```bash
curl -X POST "http://localhost:8000/api/v1/aspects" \
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
    "include_all_bodies": false
  }'
```

### With Custom Orbs

You can override the default orbs:

```json
{
  "datetime": {...},
  "location": {...},
  "custom_orbs": {
    "conjunction": 10.0,
    "trine": 6.0,
    "square": 5.0
  }
}
```

### Include Minor Aspects

Set `include_minor_aspects: true` to include the 7 minor aspects:

```json
{
  "datetime": {...},
  "location": {...},
  "include_minor_aspects": true
}
```

### Include All Bodies

Set `include_all_bodies: true` to calculate aspects between all 32 bodies (planets, asteroids, nodes, calculated points):

```json
{
  "datetime": {...},
  "location": {...},
  "include_all_bodies": true
}
```

**Results:**
- 10 major planets, major aspects only: ~16 aspects
- 10 major planets, all aspects: ~23 aspects
- All 32 bodies, major aspects only: ~195 aspects
- All 32 bodies, all aspects: ~288 aspects 🤯

## Response Format

```json
{
  "aspects": [
    {
      "planet1": "Sun",
      "planet2": "Moon",
      "aspect": "trine",
      "angle": 120,
      "orb": 3.48,
      "planet1_longitude": 54.46,
      "planet2_longitude": 177.94
    }
  ],
  "total_aspects": 16,
  "request_datetime": {...},
  "request_location": {...},
  "calculated_at": "2026-06-06T17:45:00Z"
}
```

### Response Fields

- `planet1`, `planet2`: The two bodies forming the aspect
- `aspect`: Type of aspect (conjunction, sextile, square, trine, opposition)
- `angle`: The exact angle of this aspect type (0, 60, 90, 120, 180)
- `orb`: How many degrees away from exact (smaller = tighter/stronger)
- `planet1_longitude`, `planet2_longitude`: Ecliptic positions

## Orb Interpretation

**Orb** is the deviation from the exact aspect angle:

- **0-2° orb**: Very tight, very powerful
- **2-4° orb**: Strong, definitely significant
- **4-6° orb**: Moderate strength
- **6-8° orb**: Weak but still noticeable
- **>8° orb**: Too wide (not counted as aspect with defaults)

Tighter orbs = stronger aspects = more noticeable effects in the chart.

## Astrological Interpretation

### Nature of Aspects

**Harmonious (Flowing):**
- **Trine (120°)**: Natural talents, things come easily
- **Sextile (60°)**: Opportunities, requires some action

**Challenging (Dynamic):**
- **Square (90°)**: Friction, tension, motivation for growth
- **Opposition (180°)**: Awareness through contrast, need for balance

**Neutral (Intense):**
- **Conjunction (0°)**: Blended energies, emphasis, can be harmonious or challenging depending on planets

### Common Aspect Patterns

**T-Square**: Two planets in opposition, both square a third planet
- Creates significant tension and drive
- The apex planet (receiving both squares) is key to resolution

**Grand Trine**: Three planets all trine each other (triangle of 120° angles)
- Major talent/gift in that element
- Can be too easy - may lack motivation

**Grand Cross**: Four planets forming two oppositions and four squares
- Major life challenges requiring constant balancing
- High energy and potential for achievement

**Yod (Finger of God)**: Two planets sextile each other, both quincunx a third
- Karmic adjustment, special mission
- Requires integration of very different energies

## Examples

### Sun Trine Moon (Harmonious)
```json
{
  "planet1": "Sun",
  "planet2": "Moon",
  "aspect": "trine",
  "orb": 2.5
}
```
**Meaning**: Inner harmony between conscious will (Sun) and emotions (Moon). Ease in self-expression.

### Venus Square Mars (Challenging)
```json
{
  "planet1": "Venus",
  "planet2": "Mars",
  "aspect": "square",
  "orb": 3.2
}
```
**Meaning**: Tension between desires/values (Venus) and action/drive (Mars). Dynamic but can create conflict in relationships.

### Mercury Conjunction Uranus (Intense)
```json
{
  "planet1": "Mercury",
  "planet2": "Uranus",
  "aspect": "conjunction",
  "orb": 1.8
}
```
**Meaning**: Mind (Mercury) fused with innovation (Uranus). Original thinking, sudden insights, unconventional communication.

### Moon Septile Mars (Mystical/Fated) - Minor Aspect
```json
{
  "planet1": "Moon",
  "planet2": "Mars",
  "aspect": "septile",
  "orb": 0.98
}
```
**Meaning**: The septile (360°/7) is a mystical aspect associated with fate, destiny, and occult connections. Moon-Mars septile suggests an unusual or "fated" relationship between emotions and action. May indicate psychic sensitivity or synchronistic events related to emotional drives.

### Mercury Quintile Neptune (Genius/Creative) - Minor Aspect
```json
{
  "planet1": "Mercury",
  "planet2": "Neptune",
  "aspect": "quintile",
  "orb": 1.5
}
```
**Meaning**: The quintile (360°/5) represents specialized talent and creative genius. Mercury-Neptune quintile indicates unique gifts in creative communication, imagination, or intuitive thinking. Potential for artistic or mystical writing.

### Sun Quincunx Pluto (Blind Spot) - Minor Aspect
```json
{
  "planet1": "Sun",
  "planet2": "Pluto",
  "aspect": "quincunx",
  "orb": 2.1
}
```
**Meaning**: The quincunx/inconjunct (150°) is the "blind spot" aspect. Two energies that have nothing in common must constantly adjust. Sun-Pluto quincunx requires ongoing recalibration between ego/identity and power/transformation. Feels awkward, like something you never quite "get right."

## Technical Details

### Aspect Calculation Method

1. **Calculate angular distance** between two longitudes
2. **Take the shorter arc** (max 180°)
3. **Compare to aspect angles** with orb tolerance
4. **Return first matching aspect** (checked in order: conjunction, opposition, trine, square, sextile)

### Default Orb Logic

**Major Aspects (wider orbs):**
- Conjunctions and oppositions: 8° (most important)
- Trines: 8° (very harmonious)
- Squares: 7° (challenging)
- Sextiles: 6° (milder harmonious)

**Minor Aspects (tighter orbs):**
- Semi-sextile, semi-square, sesquiquadrate, quincunx: 3°
- Septile, quintile, biquintile: 2° (very tight - these are subtle)

Minor aspects use tighter orbs because they're more subtle and need to be close to exact to have noticeable effects. The genius aspects (quintile/biquintile) and mystical aspects (septile) especially need tight orbs.

Luminaries (Sun/Moon) traditionally get wider orbs in classical astrology, but this API uses consistent orbs for all bodies. You can override with `custom_orbs`.

## What's NOT Included (Yet)

- **Applying vs Separating**: Whether aspect is forming or separating (requires speed analysis)
- **Aspect patterns**: Automatic detection of T-squares, Grand Trines, etc.
- **Aspect strength weighting**: By planet importance (Luminaries vs outer planets)
- **Harmonic aspects**: Novile (40°), decile (36°), etc.

These may be added in future versions!

## Performance

- **10 planets, major only**: ~45 comparisons, finds ~16 aspects in ~10ms
- **10 planets, all aspects**: ~45 comparisons, finds ~23 aspects in ~12ms
- **32 bodies, major only**: ~496 comparisons, finds ~195 aspects in ~30ms
- **32 bodies, all aspects**: ~496 comparisons, finds ~288 aspects in ~35ms

Very fast! 🚀

## Use Cases

1. **Natal Chart Analysis**: See all aspects at birth
2. **Compatibility (Synastry)**: Compare aspects between two charts (coming soon)
3. **Transits**: Current planets aspecting natal planets (coming soon)
4. **Progressions**: Progressed planets aspecting natal (coming soon)

---

**Next Steps:**
- Learn about [Extended Bodies](EXTENDED_BODIES.md) to include asteroids in aspects
- Read the [House Guide](HOUSE_FEATURES.md) for house interpretations
- Check the [API Documentation](http://localhost:8000/docs) for interactive testing
