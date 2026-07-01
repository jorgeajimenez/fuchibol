#!/bin/bash
# Exit on any error
set -e

echo "🚀 Starting Static Publish Build..."

# Check if uv is available, fallback to python3
if command -v uv &> /dev/null; then
    echo "Using 'uv' to run compilation script..."
    uv run python3 publish.py
else
    echo "Using system 'python3' to run compilation script..."
    python3 publish.py
fi
