#!/bin/bash
# Script para executar o GitHub Scanner

show_loading() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\\'
    local text="$2"
    
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf "\r%s [%c]" "$text" "$spinstr"
        local spinstr=$temp${spinstr%$temp}
        sleep $delay
    done
    printf "\r%s [✔]\n" "$text"
}

run_with_loading() {
    local command="$1"
    local message="$2"
    
    echo "$message"
    $command &
    local pid=$!
    show_loading $pid "$message"
    wait $pid
    return $?
}

# Get the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 GitHub Scanner - Iniciando..."
echo ""

# Check if scanner directory exists
if [ ! -d "$PROJECT_ROOT/scanner" ]; then
    echo "❌ Error: scanner directory not found!"
    echo "Run this script from the project root directory."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    run_with_loading "python3 -m venv venv" "Creating virtual environment..."
    echo ""
fi

run_with_loading "source $PROJECT_ROOT/venv/bin/activate" "Activating virtual environment..."
echo ""

run_with_loading "pip install -r $PROJECT_ROOT/requirements.txt" "Checking and installing dependencies..."
echo ""

if [ ! -f "$PROJECT_ROOT/.env" ]; then
    echo "❌ .env file not found!"
    echo "📝 Copy .env.example to .env and configure your variables"
    exit 1
fi

run_with_loading "python -m scanner.core.github_scan" "🔍 Running GitHub Scanner..."
local_exit_code=$?

echo ""
if [ $local_exit_code -eq 0 ]; then
    echo "✅ Scanner executed successfully!"
else
    echo "❌ Error during scanner execution"
    echo "💡 Check if your GitHub token is properly configured in .env"
fi

echo "�� Process finished!" 