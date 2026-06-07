#!/bin/bash
# Swiss Ephemeris Data Setup Guide
# This script helps you download ephemeris data files for asteroids and extended bodies

EPHEMERIS_DIR="./ephemeris_data"

echo "============================================"
echo "Swiss Ephemeris Data Setup"
echo "============================================"
echo ""
echo "This will enable calculations for:"
echo "  • The 5 main asteroids (Chiron, Ceres, Pallas, Juno, Vesta)"
echo "  • Extended date range (1800-2400)"
echo ""

# Create directory if it doesn't exist
mkdir -p "$EPHEMERIS_DIR"

echo "Current status:"
echo ""

# Check which files we have
check_file() {
    local filename=$1
    local description=$2
    if [ -f "$EPHEMERIS_DIR/$filename" ]; then
        local size=$(du -h "$EPHEMERIS_DIR/$filename" | cut -f1)
        echo "  ✓ $filename ($size) - $description"
        return 0
    else
        echo "  ✗ $filename - $description"
        return 1
    fi
}

# Check main files
check_file "sepl_18.se1" "Planets (built-in Moshier used if missing)"
check_file "semo_18.se1" "Moon (built-in Moshier used if missing)"

# Check asteroid files
echo ""
echo "Asteroid file:"
check_file "seas_18.se1" "Main asteroids (REQUIRED for Chiron, Ceres, Pallas, Juno, Vesta)"

echo ""
echo "============================================"
echo ""

# Count missing files
missing_main=0
missing_asteroids=0

[ ! -f "$EPHEMERIS_DIR/seas_18.se1" ] && missing_asteroids=1

if [ $missing_asteroids -eq 1 ]; then
    echo "⚠️  ASTEROIDS NOT AVAILABLE"
    echo ""
    echo "To enable asteroids, download the ephemeris files:"
    echo ""
    echo "Download the asteroid file:"
    echo ""
    echo "  wget https://github.com/aloistr/swisseph/raw/master/ephe/seas_18.se1 -P $EPHEMERIS_DIR/"
    echo ""
    echo "Required file:"
    echo "  • seas_18.se1 (~218 KB) - Main 5 asteroids"
    echo ""
else
    echo "✓ Asteroid file present!"
    echo ""
    echo "You can now calculate natal charts with all 32 celestial bodies!"
    echo "Use: include_all_bodies=true in your API requests"
    echo ""
fi

echo "============================================"
echo ""
echo "Bodies available WITHOUT asteroid file (27):"
echo "  • 10 major planets"
echo "  • 2 lunar nodes"
echo "  • 8 Uranian planets (Zeus, Apollon, etc.)"
echo "  • Black Moon Lilith & Priapus"
echo "  • 6 calculated points (Part of Fortune, etc.)"
echo ""
echo "Bodies available WITH asteroid file (+5 = 32 total):"
echo "  • All of the above PLUS"
echo "  • 5 main asteroids (Chiron, Ceres, Pallas, Juno, Vesta)"
echo ""
echo "Total ephemeris data size: $(du -sh $EPHEMERIS_DIR 2>/dev/null | cut -f1 || echo '0')"
echo ""
