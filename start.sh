#!/bin/bash
# Start script for the Astrology API

echo "Starting Astrology API..."
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting server..."
echo ""
echo "API will be available at:"
echo "  - Main API: http://localhost:8000"
echo "  - Interactive Docs: http://localhost:8000/docs"
echo "  - ReDoc: http://localhost:8000/redoc"
echo "  - Health Check: http://localhost:8000/api/v1/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
