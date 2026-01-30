# 💧 Sawkill Water Chatbot - Team User Guide

**Just double-click to run! Everything installs automatically.**

---

## First Time Setup (One-Time)

### Step 1: Install Python (if not already installed)

**Mac:**
1. Go to https://www.python.org/downloads/
2. Download Python 3.9 or newer
3. Run the installer

**Windows:**
1. Go to https://www.python.org/downloads/
2. Download Python 3.9 or newer
3. Run installer - **☑️ CHECK "Add Python to PATH"** (important!)

### Step 2: Download the release 1.0

### Step 3: Run the App

**Mac:** Double-click `run_app_mac.command`

**Windows:** Double-click `run_app_windows.bat`

#### ⚠️ Mac First Time Setup (Required Once)

Mac blocks downloaded scripts. **Open Terminal** (Cmd+Space, type "Terminal") and run:

```bash
cd ~/Downloads/waterchatbot-1.0
chmod +x run_app_mac.command
```

Then:
1. **Right-click** `run_app_mac.command`
2. Click **Open**
3. Click **Open** again in the dialog

**If double-click still doesn't work, run in Terminal:**
```bash
cd ~/Downloads/waterchatbotproject
bash run_app_mac.command
```

### Step 4: Upload Your Data File (First Run Only)

1. The app opens in your browser
2. In the sidebar, click **"Browse files"**
3. Select your Excel file (e.g., `water_data.xlsx`)
4. Data loads automatically!

Your file is saved - no need to upload again next time.

---

## Daily Use

Just double-click `run_app_mac.command` (Mac) or `run_app_windows.bat` (Windows).

Your data is remembered automatically!

---

## Using the App

### Asking Questions

Just type natural questions like:

| What you want | What to type |
|---------------|--------------|
| Coldest January | "coldest january water temperature 1981 to 1995" |
| Compare seasons | "compare summer vs winter temperature" |
| Site data | "show data for site 2" |
| Bacteria levels | "highest ecoli reading" |
| Trends | "dissolved oxygen trend over time" |
| Counts | "how many samples per site" |

### Exporting to NetCDF
1. Scroll down in sidebar to **"📦 Export to NetCDF"**
2. Enter title and institution
3. Click **"📥 Export to NetCDF"**
4. File saves to `data/water_quality_data.nc`

---

## Updating the Data File

**When monthly data is added to Excel:**

**Option 1:** Upload the updated file again in the browser

**Option 2:** Click **"🔄 Reload Data"** if the file was updated in the same location

---

## Troubleshooting

### App won't start
- Make sure Python is installed
- Try restarting your computer

### Data not loading
- Make sure you uploaded a valid Excel file
- Check that it has the "FieldData" sheet

### Browser shows blank page
- Wait a few seconds, the app takes time to start
- Try refreshing the page (Cmd+R or F5)

---

## Getting Help

If you have issues:
1. Check this guide first
2. Ask the team member who set up the app
3. Check the main [README.md](README.md) for technical details

---

## What the App Does (Simple Explanation)

```
Upload Excel file (once)
      ↓
  App remembers it
      ↓
  Ask Question ──→ "coldest january water temp?"
      ↓
App understands ──→ Finds: january + coldest + water temp
      ↓
  Shows Answer ──→ "1985 had coldest January at 2.3°C"
      ↓
 (Optional) Export to NetCDF for GIS software
```

---

*No Python knowledge needed! Just double-click and use the browser.*
