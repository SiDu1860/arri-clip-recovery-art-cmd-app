#!/bin/bash
# Launch script for ARRI MXF Recovery Tool (macOS/Linux)

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3 to run this tool"
    exit 1
fi

# Change to script directory
cd "$SCRIPT_DIR"

# Run the tool
python3 main.py