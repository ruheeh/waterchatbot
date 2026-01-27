#!/bin/bash
# ================================================
# 💧 Water Quality Chatbot - Mac Setup & Run
# ================================================
# Just double-click this file to run!
# First run will install packages automatically.
#
# ⚠️ FIRST TIME SECURITY NOTE:
# If Mac shows "cannot be opened" warning:
#   1. Right-click this file → Open → Open
#   OR
#   2. System Settings → Privacy & Security → Open Anyway
# ================================================

cd "$(dirname "$0")"

# Try to remove quarantine flag (helps future runs)
xattr -d com.apple.quarantine "$0" 2>/dev/null

echo ""
echo "💧 =================================="
echo "   Water Quality Chatbot"
echo "==================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    echo ""
    echo "Please install Python 3 first:"
    echo "  1. Go to https://www.python.org/downloads/"
    echo "  2. Download and install Python 3.9 or newer"
    echo "  3. Run this script again"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check/Install dependencies
echo ""
echo "📦 Checking dependencies..."

if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "   Installing required packages (one-time)..."
    python3 -m pip install --upgrade pip --quiet
    python3 -m pip install streamlit pandas openpyxl netCDF4 --quiet
    echo "   ✅ Packages installed!"
else
    echo "   ✅ All packages ready"
fi

# Create data folder if needed
mkdir -p data

# Run the app
echo ""
echo "🚀 Starting app..."
echo "   Opening in browser at http://localhost:8501"
echo ""
echo "   ⚠️  Keep this window open while using the app!"
echo "   Press Ctrl+C to stop"
echo ""

python3 -m streamlit run app.py --server.headless=true
