#!/bin/bash

echo "🌐 Starting CodePhoenix Frontend..."
echo ""

# Get the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Check if frontend directory exists
if [ ! -d "$PROJECT_ROOT/frontend" ]; then
    echo "❌ Error: frontend directory not found!"
    echo "Run this script from the project root directory."
    exit 1
fi

# Check if scanner is available
if [ ! -d "$PROJECT_ROOT/scanner" ]; then
    echo "⚠️  Warning: Scanner directory not found at ./scanner"
    echo "Please ensure the scanner package is properly installed:"
    echo "1. Create scanner directory: mkdir -p scanner"
    echo "2. Copy scanner files to scanner/core"
    echo ""
fi

echo "🌐 Starting server..."
echo "📝 Access: http://localhost:8080"
echo "⏹️  Press Ctrl+C to stop"
echo "==============================================="

# Start Python HTTP server
cd "$PROJECT_ROOT/frontend"
python3 -m http.server 8080 