#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to cleanup background processes on script exit
cleanup() {
    echo -e "\n${RED}Shutting down servers...${NC}"
    kill $(jobs -p) 2>/dev/null
    exit
}

# Set up trap for cleanup on script exit
trap cleanup EXIT

# Start the simulator in the background
echo -e "${GREEN}Starting PyBullet simulator...${NC}"
PYTHONPATH=$PROJECT_ROOT python src/simulator/simulator.py &
SIMULATOR_PID=$!

# Wait a moment for the simulator to initialize
sleep 2

# Start the web server in the background
echo -e "${GREEN}Starting web server...${NC}"
PYTHONPATH=$PROJECT_ROOT python src/web/server.py &
WEB_SERVER_PID=$!

# Wait for both processes
echo -e "${GREEN}All servers started. Press Ctrl+C to stop.${NC}"
wait 