# 💧 Water Quality Data Chatbot (Free Version)

A simple chatbot for querying water monitoring data using natural language. **Runs completely offline with no API costs!**

## Features

- **100% Free**: No paid AI/API subscriptions needed
- **Offline**: Works without internet after setup
- **Pattern Matching**: Understands natural language questions about your data
- **Water Quality Focused**: Knows about DO, pH, E. coli, turbidity, etc.
- **NetCDF Export**: Export to CF-compliant NetCDF for GIS/scientific tools

## Quick Start

### 1. Install Dependencies

```bash
cd ~/Downloads/waterchatbotproject
python3 -m pip install -r requirements.txt
```

### 2. Run the App

```bash
python3 -m streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 3. Load Your Data

- Click "Load/Reload Data" in the sidebar
- Or upload a different Excel file

## Example Questions

The chatbot understands questions like:

| Question Type | Examples |
|--------------|----------|
| **Extremes** | "coldest january water temperature from 1981 to 1995" |
| **Averages** | "average dissolved oxygen by year" |
| **Site Data** | "show data for site 2" |
| **Comparisons** | "compare summer vs winter temperature" |
| **Counts** | "how many samples per site?" |
| **Correlations** | "correlation between temperature and oxygen" |
| **Trends** | "temperature trend over time" |
| **Summaries** | "summary statistics for pH" |

## Supported Parameters

The chatbot recognizes these water quality terms:

| You can say... | Actual column |
|----------------|---------------|
| temperature, water temp | water_temp.C |
| dissolved oxygen, DO | dissolved_oxygen.mg_per_L |
| ph | ph |
| turbidity | turbidity.ntu |
| ecoli, e. coli, bacteria | ecoli.CFU_per_100mL |
| enterococcus | entero.CFU_per_100mL |
| coliform | total_coliforms.CFU_per_100mL |
| conductivity | compensated_conductivity.uS_per_cm |
| chlorophyll | chlorophyll_a.RFU_tot |
| rain, rainfall | rain7.in |

## Data Format

The chatbot reads the **FieldData** sheet from your Excel file. Expected columns:

- `sample_date` - Date of sample
- `site` - Site identifier
- `year`, `month`, `season` - Time info
- `water_temp.C` - Water temperature
- `dissolved_oxygen.mg_per_L` - DO levels
- `ph` - pH
- `turbidity.ntu` - Turbidity
- `ecoli.CFU_per_100mL` - E. coli count
- ... and more

## Project Structure

```
waterchatbotproject/
├── app.py                 # Streamlit frontend
├── data_manager.py        # Excel data handling
├── query_engine_free.py   # Pattern matching engine
├── netcdf_exporter.py     # NetCDF export module
├── manage.py              # CLI for data updates
├── requirements.txt       # Dependencies
└── data/
    └── water_data.xlsx    # Your data file
```

## Adding Monthly Data

```bash
python3 manage.py add new_monthly_data.xlsx --month 2025-02
```

## NetCDF Export

The chatbot can export your data to NetCDF format (CF-compliant) for use with GIS and scientific tools.

### To use NetCDF export:
1. Load your data in the app
2. Find "Export to NetCDF" in the sidebar
3. Enter title and institution
4. Click "Export to NetCDF"

The exported file will be saved as `data/water_quality_data.nc`

### NetCDF structure:
```
Dimensions: time × site
Variables: water_temp, dissolved_oxygen, ph, ecoli, etc.
Attributes: CF-1.8 compliant metadata with units
```

### Install NetCDF support:
```bash
python3 -m pip install netCDF4
```

## How It Works

Instead of using AI, this chatbot uses **pattern matching**:

1. Extracts keywords from your question (temperature, january, average, etc.)
2. Maps them to actual column names and pandas operations
3. Builds and executes the appropriate query
4. Returns results in a readable format

This means:
- ✅ Free forever
- ✅ Fast (no API calls)
- ✅ Works offline
- ⚠️ Must phrase questions in recognizable patterns

## Troubleshooting

**"No data found matching your criteria"**
- Check if your date range has data
- Try a different time period

**Question not understood**
- Try rephrasing using supported keywords
- Check the example questions for patterns

**Streamlit not found**
```bash
python3 -m pip install streamlit
# Then run with:
python3 -m streamlit run app.py
```

## License

MIT License - Built for watershed monitoring research
