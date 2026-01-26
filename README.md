# 💧 Water Quality Data Chatbot (Free Version)

A simple chatbot for querying water monitoring data using natural language. **Runs completely offline with no API costs!**

---

## 📚 Documentation

| Guide | For Who | Description |
|-------|---------|-------------|
| **This file (README.md)** | Developers/Admins | Full technical documentation |
| [SETUP.md](SETUP.md) | Developers/Admins | Installation & team distribution guide |
| [README_TEAM.md](README_TEAM.md) | Team Members | Simple "just run it" instructions |

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🆓 **100% Free** | No paid AI/API subscriptions needed |
| 📴 **Offline** | Works without internet after setup |
| 🧠 **Pattern Matching** | Understands natural language questions |
| 💧 **Water Quality Focused** | Knows DO, pH, E. coli, turbidity, etc. |
| 📁 **Dual Format Input** | Reads both Excel (.xlsx) and NetCDF (.nc) |
| 📤 **NetCDF Export** | Export to CF-compliant NetCDF for GIS tools |
| 👥 **Team Ready** | Easy distribution with auto-setup scripts |
| ⚙️ **Configurable** | Data file path stored in config.json |

---

## 🚀 Quick Start

### Option 1: Double-Click (Easiest)

**Mac:** Double-click `run_app_mac.command`  
**Windows:** Double-click `run_app_windows.bat`

> ⚠️ **Mac First-Time Security Warning:** If Mac says "cannot be opened", right-click the file → **Open** → **Open**. See [Mac Security Note](#-mac-security-note) below.

The script automatically:
- ✅ Installs dependencies (first run)
- ✅ Prompts for your Excel file path (first run)
- ✅ Creates config.json
- ✅ Opens the app in your browser

### Option 2: Manual

```bash
cd ~/Downloads/waterchatbotproject
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```

---

## 🔄 How It Works

```
                        ┌─────────────────────┐
                        │   Upload Data File  │
                        └──────────┬──────────┘
                                   │
                                   ▼
                          ┌───────────────┐
                          │ Check Format  │
                          └───────┬───────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
            ┌──────────────┐            ┌──────────────┐
            │ Excel (.xlsx)│            │ NetCDF (.nc) │
            │  FieldData   │            │              │
            │    sheet     │            │              │
            └──────┬───────┘            └──────┬───────┘
                   │                           │
                   └─────────────┬─────────────┘
                                 │
                                 ▼
                      ┌─────────────────────┐
                      │  Pandas DataFrame   │
                      │   (unified format)  │
                      └──────────┬──────────┘
                                 │
            ┌────────────────────┼────────────────────┐
            │                    │                    │
            ▼                    ▼                    ▼
    ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
    │  Ask Question │   │ View Summary  │   │Export NetCDF  │
    └───────┬───────┘   └───────────────┘   └───────────────┘
            │
            ▼
    ┌───────────────┐
    │Extract Keywords│
    │ (temperature,  │
    │  january, avg) │
    └───────┬───────┘
            │
            ▼
    ┌───────────────┐
    │ Build Pandas  │
    │    Query      │
    └───────┬───────┘
            │
            ▼
    ┌───────────────┐
    │  Execute &    │
    │ Show Results  │
    └───────────────┘
```

---

## 💬 Example Questions

| Question Type | Examples |
|--------------|----------|
| **Extremes** | "coldest january water temperature from 1981 to 1995" |
| **Averages** | "average dissolved oxygen by year" |
| **Site Data** | "show data for site 2" |
| **Comparisons** | "compare summer vs winter temperature" |
| **Time Comparisons** | "compare total coliform between january 2026 and november 2023" |
| **Counts** | "how many samples per site?" |
| **Correlations** | "correlation between temperature and oxygen" |
| **Trends** | "temperature trend over time" |
| **Summaries** | "summary statistics for pH" |

---

## 🔬 Supported Parameters

| You can say... | Actual column |
|----------------|---------------|
| temperature, water temp | water_temp.C |
| dissolved oxygen, DO | dissolved_oxygen.mg_per_L |
| ph | ph |
| turbidity | turbidity.ntu |
| ecoli, e. coli, bacteria | ecoli.CFU_per_100mL |
| enterococcus | entero.CFU_per_100mL |
| coliform, total coliform | total_coliforms.CFU_per_100mL |
| conductivity | compensated_conductivity.uS_per_cm |
| chlorophyll | chlorophyll_a.RFU_tot |
| rain, rainfall | rain7.in |

---

## 📁 Data Format

The chatbot reads **either**:
- **Excel (.xlsx)** - reads the **FieldData** sheet only
- **NetCDF (.nc)** - reads files exported by this app or similar structure

Expected columns: `sample_date`, `site`, `year`, `month`, `season`, `water_temp.C`, `dissolved_oxygen.mg_per_L`, `ph`, `turbidity.ntu`, `ecoli.CFU_per_100mL`, and more.

---

## 📂 Project Structure

```
waterchatbotproject/
├── run_app_mac.command    # 🍎 Mac: Double-click to run
├── run_app_windows.bat    # 🪟 Windows: Double-click to run
├── config.json            # ⚙️ Data file path (auto-created)
├── app.py                 # Streamlit frontend
├── data_manager.py        # Excel/NetCDF data loading
├── query_engine_free.py   # Pattern matching engine
├── netcdf_exporter.py     # NetCDF export module
├── build_app.py           # Creates distribution folder
├── manage.py              # CLI for monthly data updates
├── requirements.txt       # Dependencies
├── README.md              # This file
├── README_TEAM.md         # Simple guide for team members
├── SETUP.md               # Detailed setup instructions
└── data/
    └── water_data.xlsx    # Your data file
```

---

## ⚙️ Configuration

On first run, `config.json` is created:

```json
{
  "data_file": "/path/to/your/water_data.xlsx",
  "export_folder": "./data"
}
```

**To change the data file:** Edit `config.json` or delete it and run again.

**For shared team data:** Point to a network drive:
```json
{
  "data_file": "/Volumes/SharedDrive/Research/water_data.xlsx"
}
```

---

## 📤 NetCDF Export

Export your data to CF-compliant NetCDF format for GIS and scientific tools:

1. Load your data in the app
2. Find **"📦 Export to NetCDF"** in the sidebar
3. Enter title and institution
4. Click **"📥 Export to NetCDF"**

**NetCDF structure:**
```
Dimensions: time × site
Variables: water_temp, dissolved_oxygen, ph, ecoli, etc.
Attributes: CF-1.8 compliant metadata with units
```

---

## 👥 Team Distribution

### Create Distribution Package

```bash
python3 build_app.py
```

This creates `WaterQualityChatbot_Distribution/` folder.

### Share with Team

Share the folder via Google Drive, USB, or email (zipped).

### Team Member Experience

```
Double-click run_app.sh/bat
         │
         ▼
   Auto-installs packages
         │
         ▼
   "Enter Excel path:" (first run only)
         │
         ▼
   App opens in browser ✅
```

See [SETUP.md](SETUP.md) for detailed distribution instructions.

---

## 🔧 Adding Monthly Data

When the Excel file is updated:
1. Click **"🔄 Load/Reload Data"** in the app
2. Done! New data is loaded.

Or via CLI:
```bash
python3 manage.py add new_monthly_data.xlsx --month 2025-02
```

---

## ❓ Troubleshooting

### 🍎 Mac Security Note

When you first double-click `run_app_mac.command`, Mac may show:

> "run_app_mac.command" cannot be opened because Apple cannot verify it is free from malware.

**To fix (do once):**

1. **Right-click** the file → **Open** → **Open**

**OR**

1. Go to **System Settings** → **Privacy & Security**
2. Scroll down and click **Open Anyway**

**OR (Terminal method):**
```bash
xattr -d com.apple.quarantine run_app_mac.command
```

After doing this once, double-click will work normally.

---

| Problem | Solution |
|---------|----------|
| "Python not found" | Install from python.org |
| "streamlit not found" | Run: `python3 -m pip install streamlit` |
| "File not found" | Check path in config.json |
| Question not understood | Try rephrasing with supported keywords |
| No data found | Check if date range has data |

See [SETUP.md](SETUP.md) for detailed troubleshooting.

---

## 📜 License

MIT License - Built for watershed monitoring research
