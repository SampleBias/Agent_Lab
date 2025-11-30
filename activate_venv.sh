#!/bin/bash
# Helper script to activate the virtual environment

cd "$(dirname "$0")"
source venv/bin/activate

echo "✓ Virtual environment activated!"
echo "Python: $(which python)"
echo "VIRTUAL_ENV: $VIRTUAL_ENV"
echo ""
echo "To deactivate, run: deactivate"

