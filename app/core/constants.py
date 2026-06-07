"""Astrological constants used throughout the application."""

import swisseph as swe

# Major planets with their Swiss Ephemeris IDs
MAJOR_PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
}

# Nodes
NODES = {
    "North Node": swe.MEAN_NODE,  # Mean Node
    "True Node": swe.TRUE_NODE,   # True/Osculating Node
}

# Major asteroids (Chiron has special ID, others use asteroid numbers)
ASTEROIDS = {
    "Chiron": swe.CHIRON,
    "Ceres": 1,
    "Pallas": 2,
    "Juno": 3,
    "Vesta": 4,
}

# Uranian/Transneptunian planets (hypothetical planets)
URANIAN_PLANETS = {
    "Cupido": swe.CUPIDO,
    "Hades": swe.HADES,
    "Zeus": swe.ZEUS,
    "Kronos": swe.KRONOS,
    "Apollon": swe.APOLLON,
    "Admetos": swe.ADMETOS,
    "Vulkanus": swe.VULKANUS,  # Note: Swiss Ephemeris spells it VULKANUS
    "Poseidon": swe.POSEIDON,
}

# Black Moon Lilith and related
LUNAR_APOGEE = {
    "Black Moon Lilith": swe.MEAN_APOG,  # Mean Apogee
}

# Calculated points (these are derived from other calculations)
CALCULATED_POINTS = [
    "South Node",      # North Node + 180°
    "Descendant",      # Ascendant + 180°
    "IC",              # From houses or MC + 180°
    "Priapus",         # Black Moon Lilith + 180°
    "Part of Fortune", # Asc + Moon - Sun
    "Part of Spirit",  # Asc + Sun - Moon
]

# All celestial bodies combined (for reference)
ALL_BODIES = {
    **MAJOR_PLANETS,
    **NODES,
    **ASTEROIDS,
    **URANIAN_PLANETS,
    **LUNAR_APOGEE,
}

# Zodiac signs in order
ZODIAC_SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

# House systems
HOUSE_SYSTEMS = {
    "P": "Placidus",
    "K": "Koch",
    "O": "Porphyrius",
    "R": "Regiomontanus",
    "C": "Campanus",
    "E": "Equal",
    "W": "Whole Sign",
}

# Major aspect types and their angles
MAJOR_ASPECTS = {
    "conjunction": 0,
    "sextile": 60,
    "square": 90,
    "trine": 120,
    "opposition": 180,
}

# Minor aspect types and their angles
MINOR_ASPECTS = {
    "semi-sextile": 30,
    "semi-square": 45,
    "septile": 51.43,  # 360/7 - the "fated" aspect
    "quintile": 72,  # 360/5 - the "genius" aspect
    "sesquiquadrate": 135,
    "biquintile": 144,  # 2×72 - another "genius" aspect
    "quincunx": 150,  # Also called "inconjunct"
}

# All aspect types combined
ASPECT_TYPES = {
    **MAJOR_ASPECTS,
    **MINOR_ASPECTS,
}

# Default orbs for aspects
DEFAULT_ORBS = {
    # Major aspects (wider orbs)
    "conjunction": 8.0,
    "opposition": 8.0,
    "trine": 8.0,
    "square": 7.0,
    "sextile": 6.0,
    # Minor aspects (tighter orbs)
    "semi-sextile": 3.0,
    "semi-square": 3.0,
    "septile": 2.0,  # Very tight for fated aspect
    "quintile": 2.0,  # Very tight for genius aspect
    "sesquiquadrate": 3.0,
    "biquintile": 2.0,  # Very tight for genius aspect
    "quincunx": 3.0,  # The blind spot
}
