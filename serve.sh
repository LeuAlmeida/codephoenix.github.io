#!/bin/bash

echo "🌐 Starting CodePhoenix Frontend..."
echo ""
echo "📝 Access: http://localhost:8080"
echo "⏹️  Press Ctrl+C to stop"
echo "==============================================="

# Change to frontend directory and start Python HTTP server
cd frontend
python3 -m http.server 8080 