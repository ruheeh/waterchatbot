# 💧 Water Quality Chatbot - Team User Guide

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

### Step 2: Run the App

**Mac:** Double-click `run_app_mac.command`

**Windows:** Double-click `run_app_windows.bat`

#### ⚠️ Mac Security Warning (First Time Only)

If Mac shows "cannot be opened because Apple cannot verify":

1. **Right-click** the file
2. Click **Open**
3. Click **Open** again in the dialog

After this, double-click works normally.

### Step 3: Enter Your Data File Path (First Run Only)

The script will ask:
```
Where is your water quality Excel file?
Enter full path to Excel file: 
```

Type the full path, for example:
- Mac: `/Users/jane/Documents/water_data.xlsx`
- Windows: `C:\Users\jane\Documents\water_data.xlsx`

**Done!** The app opens in your browser.

---

## Daily Use

Just double-click `run_app.sh` (Mac) or `run_app.bat` (Windows).

That's it!

---

## Changing the Data File Path Later

Open `config.json` in any text editor and change the path:

```json
{
  "data_file": "/new/path/to/water_data.xlsx"
}
```

---

## Using the App

### Loading Data
1. Click **"🔄 Load/Reload Data"** in the sidebar
2. You should see "✅ Loaded XXXX samples"

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

When new monthly data is added to the Excel file:
1. Just click **"🔄 Load/Reload Data"** again
2. The app will load the updated data

No need to restart anything!

---

## Troubleshooting

### "File not found" error
- Check the path in `config.json` is correct
- Make sure the file exists at that location
- On Windows, use double backslashes: `C:\\Users\\...`

### App won't start
- Make sure no other app is using port 8501
- Try restarting your computer

### Data not updating
- Click **"🔄 Load/Reload Data"** button
- Check if Excel file was actually saved

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
Your Excel file
      ↓
   Load Data
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

*No Python knowledge needed! Just edit config.json and double-click to run.*
