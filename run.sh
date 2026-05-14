#!/bin/bash

# Exit on error
set -e

# Function to kill processes on exit
cleanup() {
    echo "Shutting down services..."
    kill $API_PID $FRONTEND_PID
    exit
}

# Trap exit signals
trap cleanup SIGINT SIGTERM

# Set PYTHONPATH to project root
export PYTHONPATH=$PYTHONPATH:.

# Start the FastAPI backend in the background
echo "Starting FastAPI backend..."
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
API_PID=$!

# Wait a moment for the API to initialize
sleep 5

# Start the Streamlit frontend
echo "Starting Streamlit frontend..."
python3 -m streamlit run app/dashboard.py --server.port 8501 --server.address 0.0.0.0 --server.headless true --browser.gatherUsageStats false &
FRONTEND_PID=$!

echo ""
echo "🎉 Application is running!"
echo "- API Docs: http://localhost:8000/docs"
echo "- Dashboard: http://localhost:8501"
echo ""
echo "Press Ctrl+C to shut down."

# Wait for both processes to complete
wait $API_PID $FRONTEND_PID
