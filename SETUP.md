# 🔧 Setup & Installation Guide

Complete guide for setting up and distributing the Water Quality Chatbot.

---

## Table of Contents

1. [Quick Start (Personal Use)](#quick-start-personal-use)
2. [Team Distribution](#team-distribution)
3. [Configuration](#configuration)
4. [Troubleshooting](#troubleshooting)

---

## Quick Start (Personal Use)

### Prerequisites

- Python 3.9 or newer
- Your water quality Excel file

### Installation

```bash
# 1. Navigate to project folder
cd ~/Downloads/waterchatbotproject

# 2. Install dependencies
python3 -m pip install -r requirements.txt

# 3. Run the app
python3 -m streamlit run app.py
```

Or simply double-click `run_app.sh` (Mac) or `run_app.bat` (Windows) - it does everything automatically!

---

## Team Distribution

### Overview

```
You (Admin)                         Team Members
     │                                   │
     ▼                                   │
Run build_app.py                         │
     │                                   │
     ▼                                   │
Creates Distribution Folder ───────► Receive Folder
                                         │
                                         ▼
                                   Double-click run_app
                                         │
                                         ▼
                                   Auto-installs packages
                                         │
                                         ▼
                                   Prompts for Excel path
                                         │
                                         ▼
                                   App opens in browser!
```

### Step 1: Create Distribution (You Do This Once)

```bash
python3 build_app.py
```

This creates a folder called `WaterQualityChatbot_Distribution/` containing:

```
WaterQualityChatbot_Distribution/
├── run_app.sh          ← Mac users double-click this
├── run_app.bat         ← Windows users double-click this
├── README.md           ← Simple instructions for team
├── app.py
├── data_manager.py
├── query_engine_free.py
├── netcdf_exporter.py
├── requirements.txt
└── data/               ← Empty folder for exports
```

### Step 2: Share with Team

Share the `WaterQualityChatbot_Distribution/` folder via:
- Google Drive
- Dropbox
- USB drive
- Email (zip it first)

### Step 3: Team Member Setup

**What team members do:**

1. **Install Python** (one-time)
   - Mac: Download from https://www.python.org/downloads/
   - Windows: Download from https://www.python.org/downloads/
     - ⚠️ **Check "Add Python to PATH"** during installation!

2. **Double-click to run**
   - Mac: `run_app.sh`
   - Windows: `run_app.bat`

3. **First run only:** Enter path to Excel file when prompted
   ```
   Where is your water quality Excel file?
   Enter full path to Excel file: /Users/jane/Documents/water_data.xlsx
   ```

4. **Done!** App opens in browser.

### What the Scripts Do Automatically

| Task | Manual Way | Script Does It |
|------|-----------|----------------|
| Install packages | `pip install streamlit pandas...` | ✅ Auto |
| Create config | Edit JSON file | ✅ Prompts user |
| Start app | `python3 -m streamlit run app.py` | ✅ Auto |

---

## Configuration

### config.json

After first run, a `config.json` file is created:

```json
{
  "data_file": "/path/to/your/water_data.xlsx",
  "export_folder": "./data"
}
```

### Configuration Options

| Setting | Description | Example |
|---------|-------------|---------|
| `data_file` | Path to Excel or NetCDF file | `/Users/jane/water_data.xlsx` |
| `export_folder` | Where NetCDF exports are saved | `./data` |

### Changing the Data File Path

**Option 1:** Edit `config.json` directly

**Option 2:** Delete `config.json` and run the app again - it will prompt for a new path

### Using a Shared Network Drive

Point everyone to the same file:

```json
{
  "data_file": "/Volumes/SharedDrive/Research/water_data.xlsx"
}
```

This way, when the Excel file is updated, everyone sees the new data!

---

## Platform-Specific Notes

### Mac

- Double-click `run_app.sh` to run
- If it won't open: Right-click → Open → Open
- Or run in Terminal: `./run_app.sh`

### Windows

- Double-click `run_app.bat` to run
- Use double backslashes in paths: `C:\\Users\\name\\file.xlsx`
- Or forward slashes work too: `C:/Users/name/file.xlsx`

### Linux

- Same as Mac: `./run_app.sh`
- May need: `chmod +x run_app.sh` first

---

## Troubleshooting

### "Python not found"

**Mac:**
```bash
# Install via Homebrew
brew install python3

# Or download from python.org
```

**Windows:**
- Reinstall Python from python.org
- ☑️ CHECK "Add Python to PATH" during installation

### "streamlit: command not found"

The scripts handle this automatically, but if you run manually:
```bash
python3 -m streamlit run app.py
```

### "File not found" error

- Check the path in `config.json`
- Make sure the file exists
- Use absolute paths (starting with `/` on Mac or `C:\` on Windows)

### App won't start / Port in use

```bash
# Kill any existing Streamlit processes
pkill -f streamlit

# Or use a different port
python3 -m streamlit run app.py --server.port 8502
```

### Packages won't install

```bash
# Upgrade pip first
python3 -m pip install --upgrade pip

# Then install
python3 -m pip install -r requirements.txt
```

### "Permission denied" on Mac

```bash
chmod +x run_app.sh
./run_app.sh
```

---

## Updating the App

When you receive updated code files:

1. Replace the Python files (`.py`) in your folder
2. Double-click run script as usual
3. No reinstallation needed!

---

## Uninstalling

Simply delete the `waterchatbotproject` folder. 

To remove Python packages (optional):
```bash
python3 -m pip uninstall streamlit pandas openpyxl netCDF4
```
