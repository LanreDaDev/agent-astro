# Transit Aspects Guide

## Overview

**Transits** show how current planetary positions aspect your natal chart. This is one of the most practical astrology tools for understanding what energies are active in your life right now!

## What Are Transits?

In astrology, transits are the current positions of planets in the sky and how they aspect (interact with) the planets in your birth chart. Transits trigger natal chart potentials and show timing for events and experiences.

### Key Concepts

- **Natal Chart**: Your birth chart - fixed positions at your birth time
- **Transiting Planets**: Current positions of planets in the sky
- **Transit Aspects**: When transiting planets form aspects to your natal planets

## Why Transits Matter

Transits answer the question: **"Why is this happening NOW?"**

- Your natal chart shows **potential** and **character**
- Transits show **timing** and **activation**
- They explain why certain themes come up at certain times

Example: You may have natal Mars square Saturn (disciplined action as a life theme), but when **transiting Mars squares your natal Saturn**, that exact tension becomes **active right now** - you might feel blocked, need to push through resistance, or face authority figures.

## API Usage

### Calculate Current Transits

**Endpoint:** `POST /api/v1/transits`

```bash
curl -X POST "http://localhost:8000/api/v1/transits" \
  -H "Content-Type: application/json" \
  -d '{
    "natal_datetime": {
      "year": 1990,
      "month": 5,
      "day": 15,
      "hour": 14,
      "minute": 30
    },
    "natal_location": {
      "latitude": 51.5074,
      "longitude": -0.1278,
      "timezone": "Europe/London"
    }
  }'
```

This uses **current time** as the transit time automatically!

### Calculate Transits for Specific Date

Want to see what transits were active on a specific date, or plan ahead?

```json
{
  "natal_datetime": {...},
  "natal_location": {...},
  "transit_datetime": {
    "year": 2026,
    "month": 12,
    "day": 25,
    "hour": 12,
    "minute": 0
  },
  "include_minor_aspects": true
}
```

### Include All Bodies

Set `include_all_bodies: true` to see transits from asteroids, nodes, and calculated points:

```json
{
  "natal_datetime": {...},
  "natal_location": {...},
  "include_all_bodies": true
}
```

## Response Format

```json
{
  "aspects": [
    {
      "planet1": "Sun (Transit)",
      "planet2": "Mars (Natal)",
      "aspect": "square",
      "angle": 90,
      "orb": 2.33,
      "planet1_longitude": 345.67,
      "planet2_longitude": 75.34,
      "applying": true,
      "planet1_retrograde": false,
      "planet2_retrograde": false
    }
  ],
  "total_aspects": 36,
  "natal_datetime": {...},
  "transit_datetime": {...}
}
```

**Labels:**
- `planet1` always has `(Transit)` - the current planet
- `planet2` always has `(Natal)` - your birth chart planet
- `applying`: `true` = aspect getting tighter (more powerful), `false` = separating (fading)
- `planet1_retrograde`: Whether transiting planet is retrograde (RE-doing, RE-working)
- `planet2_retrograde`: Whether natal planet was retrograde at birth

## Applying vs Separating

**APPLYING (⏩)** - Aspect is getting tighter
- The transit is building in intensity
- Effects are INCREASING
- Most powerful when exact (orb = 0)
- Use this time to PREPARE and WORK WITH the energy

**SEPARATING (⏪)** - Aspect is getting wider  
- The transit is fading
- Effects are DECREASING
- Time to INTEGRATE and REFLECT on lessons
- The peak has passed

💡 **Pro Tip**: Applying transits are usually more intense and noticeable than separating ones. Focus your attention on tight applying aspects (< 2° orb).

## Retrograde Transits (🔄)

When a transiting planet is **retrograde**, it means:

**The "RE-" Principle:**
- **RE-visit** old issues
- **RE-work** unfinished business  
- **RE-evaluate** past decisions
- **RE-connect** with old people/places
- **RE-do** what wasn't done right the first time

**Retrograde Transit Cycle (Triple Pass):**
1. **Direct Pass** - First encounter with the transit energy (new)
2. **Retrograde Pass** - RE-visiting the transit energy (review/redo)
3. **Direct Pass Again** - Final resolution (integration)

Example: **Saturn Retrograde conjunct Natal Sun**
- Not just a Saturn-Sun lesson, but a RE-EXAMINATION of identity and authority
- Likely to trigger the same issues 2-3 times before resolution
- The universe is making SURE you get the lesson!

**Common Retrograde Transits:**
- **Mercury Rx** (3x per year, 3 weeks): Communication/tech issues, RE-thinking
- **Venus Rx** (every 18 months): Relationship RE-evaluation, old loves return
- **Mars Rx** (every 2 years): Action RE-direction, anger RE-surfacing  
- **Outer Planets Rx** (yearly, 4-5 months): Deep RE-structuring of life themes

## Interpreting Transit Aspects

### Speed of Transits

Different planets move at different speeds, affecting how long their transits last:

**Fast-Moving (Personal) Transits:**
- **Moon**: 2-3 hours per aspect (fleeting moods)
- **Sun**: 2-3 days per aspect (daily events)
- **Mercury/Venus**: 1-2 days per aspect (thoughts, relationships)
- **Mars**: 3-4 days per aspect (actions, energy)

**Medium Transits:**
- **Jupiter**: 1-2 weeks (opportunities, growth)
- **Saturn**: 2-4 weeks (tests, responsibilities)

**Slow-Moving (Outer Planet) Transits:**
- **Uranus**: Several months (breakthroughs, changes)
- **Neptune**: 6-12 months (spiritual awakening, confusion)
- **Pluto**: 1-2 years (deep transformation, power shifts)

💡 **Pro Tip**: Slow transits are more significant! A Pluto transit can reshape your entire life, while a Moon transit just affects your mood for a few hours.

## Common Transit Interpretations

### Personal Planet Transits

**☉ Transiting Sun aspecting Natal Planets**
- **Conjunction/Trine**: Highlights that part of yourself, energy flows
- **Square/Opposition**: Tension, need to integrate solar will with that planet
- Duration: 2-3 days

**☽ Transiting Moon aspecting Natal Planets**
- **Any aspect**: Emotional triggers, mood shifts related to that planet
- Changes every 2-3 hours - use for timing specific activities
- Example: Moon trine natal Venus = good time for socializing

**☿ Transiting Mercury aspecting Natal Planets**
- **Any aspect**: Thoughts, communications, decisions involving that planet
- Example: Mercury square natal Saturn = mental blocks, serious thinking

### Social Planet Transits

**♃ Transiting Jupiter aspecting Natal Planets**
- **Conjunction/Trine**: Expansion, luck, opportunities in that area
- **Square/Opposition**: Over-expansion, excess, learning through overdoing
- Duration: 1-2 weeks
- Example: Jupiter conjunct natal Venus = great time for relationships/money

**♄ Transiting Saturn aspecting Natal Planets**
- **Conjunction**: Major life lesson beginning, new structure
- **Square/Opposition**: Tests, limitations, responsibility in that area
- **Trine**: Rewards for past work, stable progress
- Duration: 2-4 weeks
- Example: Saturn square natal Sun = identity crisis, authority issues

### Outer Planet Transits (MAJOR LIFE EVENTS)

**♅ Transiting Uranus aspecting Natal Planets**
- Sudden changes, breakthroughs, rebellions
- **Conjunction**: Total reinvention of that planet's energy
- **Square/Opposition**: Shocking disruptions, liberation
- Duration: Several months (due to retrograde)
- Example: Uranus conjunct natal Moon = emotional awakening, home changes

**♆ Transiting Neptune aspecting Natal Planets**
- Dissolution, spirituality, confusion, idealization
- **Conjunction**: Spiritual awakening OR major illusions
- **Square/Opposition**: Confusion, deception, or transcendence
- Duration: 6-12 months
- Example: Neptune square natal Mercury = unclear thinking, artistic inspiration

**♇ Transiting Pluto aspecting Natal Planets**
- Deep transformation, death/rebirth, power struggles
- **Conjunction**: Complete transformation of that planet's meaning in your life
- **Square/Opposition**: Intense crisis leading to empowerment
- Duration: 1-2 years
- Example: Pluto opposite natal Venus = relationship transformation, values overhaul

## Real-Life Examples

### Example 1: Career Breakthrough
```json
{
  "planet1": "Jupiter (Transit)",
  "planet2": "Sun (Natal)",
  "aspect": "conjunction",
  "orb": 0.5
}
```
**Interpretation**: Jupiter conjunct natal Sun - MAJOR expansion of identity and life direction. Classic "big opportunity" transit. Confidence is high, luck is strong. Great time to launch projects, ask for promotions, or take risks.

### Example 2: Relationship Crisis
```json
{
  "planet1": "Uranus (Transit)",
  "planet2": "Venus (Natal)",
  "aspect": "square",
  "orb": 1.2
}
```
**Interpretation**: Uranus square natal Venus - Need for freedom in relationships. Could bring sudden breakups, new attractions, or liberation from relationship patterns. Exciting but unstable. Lasts several months due to retrograde.

### Example 3: Emotional Day
```json
{
  "planet1": "Moon (Transit)",
  "planet2": "Mars (Natal)",
  "aspect": "opposition",
  "orb": 0.8
}
```
**Interpretation**: Moon opposite natal Mars - Emotional vs action. Might feel irritable, impulsive, or need to express feelings through action. Only lasts 2-3 hours. Good awareness for timing conversations.

## Multiple Transit Aspects

When several transits hit at once, they combine effects:

**Easy Period**: Multiple trines and sextiles = flow, ease, good timing
**Challenging Period**: Multiple squares and oppositions = stress, growth, major decisions
**Mixed Period**: Some easy, some hard = ups and downs

Example of a **transformative period**:
- Saturn square natal Sun (identity test)
- Uranus trine natal Moon (emotional awakening)
- Jupiter opposite natal Mercury (big ideas, travel)
= Major life restructuring with support

## Advanced: Return Charts

When a transiting planet returns to its natal position, it's called a "return":

**Solar Return** (Sun return natal Sun): Birthday! Annual chart for the year ahead
**Lunar Return** (Moon return natal Moon): Every ~28 days, emotional reset
**Saturn Return** (~29 years): Major life initiation/restructuring
**Jupiter Return** (~12 years): Growth cycle completion

The API calculates these automatically when you see conjunction aspects!

## Combining Applying/Separating + Retrograde

**Most Intense Transits (Pay Close Attention!):**

1. **Applying + Direct** ⏩
   - Normal, building intensity
   - Example: Saturn square Sun, applying, direct = challenge incoming

2. **Applying + Retrograde** ⏩🔄 **[VERY POWERFUL]**
   - Intensifying AND going back over old ground
   - Example: Pluto Rx square Venus, applying = deep relationship transformation RE-surfacing and getting MORE intense
   - This is often the MIDDLE pass of a triple transit

3. **Separating + Retrograde** ⏪🔄 **[REVIEW PHASE]**
   - Moving away but in reverse - the "looking back" phase
   - Example: Saturn Rx conjunct Sun, separating = RE-examining identity lessons as the pressure releases
   - Integration time, less intense but still important

4. **Separating + Direct** ⏪
   - Fading, moving forward
   - Time to integrate lessons learned
   - Example: Jupiter trine Moon, separating = opportunities fading, time to make use of what you got

**Priority Guide:**
- **Tight applying aspects (< 2° orb)**: ACT NOW, energy is building
- **Tight separating aspects (< 2° orb)**: INTEGRATE, make final moves
- **Retrograde + applying**: PREPARE for intensity and review
- **Retrograde + separating**: REFLECT and complete old business

## Results Summary

**10 major planets:**
- Major aspects only: ~30-40 transit aspects
- All aspects: ~45-55 transit aspects

**32 all bodies:**
- Major aspects only: ~180-220 transit aspects
- All aspects: ~270-320 transit aspects

## Performance

Transit calculations are very fast:
- Current transits (10 planets): ~15ms
- Specific date (32 bodies, all aspects): ~40ms

## Use Cases

1. **Daily Guidance**: "What energies are active today?"
2. **Event Timing**: "When should I launch this project?"
3. **Relationship Timing**: "Why is this relationship intense right now?"
4. **Yearly Planning**: Check Saturn/Jupiter transits for the year
5. **Crisis Understanding**: "Why is everything changing?"

## What's Next?

Future features:
- **Transit timeline**: See all transits for next 30/60/90 days
- **Exact dates**: When will Saturn square my Sun? (Calculate exact transit dates)
- **Return charts**: Automatic Solar/Lunar return chart generation
- **Electional astrology**: Find best dates for important events

---

**Pro Tip**: Focus on slow-moving outer planet transits (Uranus, Neptune, Pluto) and Saturn/Jupiter for major life themes. Use fast transits (Moon, Mercury, Venus, Mars) for day-to-day timing and mood awareness.
