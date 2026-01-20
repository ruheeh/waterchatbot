"""
Data Manager Module
Handles loading Excel data from FieldData sheet, managing site registry and query examples.
Uses simple in-memory storage with JSON persistence.
"""

import os
import pandas as pd
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from difflib import SequenceMatcher


class DataManager:
    """Manages water quality data from Excel and site metadata."""
    
    SHEET_NAME = "FieldData"  # Only use this sheet
    
    def __init__(self, excel_path: str, metadata_path: str = "./metadata"):
        """
        Initialize the data manager.
        
        Args:
            excel_path: Path to the Excel file with water data
            metadata_path: Path for metadata storage
        """
        self.excel_path = excel_path
        self.metadata_path = metadata_path
        self.df = None
        self.last_modified = None
        
        # In-memory storage
        self.sites_registry: List[Dict] = []
        self.query_examples: List[Dict] = []
        self.column_metadata: List[Dict] = []
        
        # Load data immediately
        self._load_excel()
    
    def _load_excel(self) -> pd.DataFrame:
        """Load or reload Excel data if file has changed."""
        current_modified = os.path.getmtime(self.excel_path)
        
        if self.df is None or current_modified != self.last_modified:
            self.df = pd.read_excel(self.excel_path, sheet_name=self.SHEET_NAME)
            self.last_modified = current_modified
            
            # Parse dates
            if 'sample_date' in self.df.columns:
                self.df['sample_date'] = pd.to_datetime(self.df['sample_date'])
            
            # Convert site to string to avoid mixed type issues
            if 'site' in self.df.columns:
                self.df['site'] = self.df['site'].astype(str)
            
            print(f"[DataManager] Loaded {len(self.df)} rows from '{self.SHEET_NAME}' sheet")
        
        return self.df
    
    def get_data(self) -> pd.DataFrame:
        """Get current dataframe, reloading if file changed."""
        return self._load_excel()
    
    def _similarity(self, query: str, text: str) -> float:
        """Calculate string similarity for simple search."""
        query_lower = query.lower()
        text_lower = text.lower()
        
        # Check for word matches
        query_words = set(query_lower.split())
        text_words = set(text_lower.split())
        
        # Count matching words
        matches = len(query_words & text_words)
        if matches > 0:
            return 0.5 + (matches / len(query_words)) * 0.5
        
        # Check for substring match
        if query_lower in text_lower or text_lower in query_lower:
            return 0.7
        
        # Use sequence matcher for fuzzy matching
        return SequenceMatcher(None, query_lower, text_lower).ratio()
    
    def initialize_chroma(self, force_refresh: bool = False):
        """Initialize metadata collections (in-memory with JSON persistence)."""
        os.makedirs(self.metadata_path, exist_ok=True)
        
        # Try to load existing metadata only if not forcing refresh
        if not force_refresh:
            self._load_metadata()
        
        # Populate with initial data if empty
        self._populate_site_registry()
        self._populate_column_metadata()
        self._populate_query_examples()
        
        # Save to disk
        self._save_metadata()
        
        print("[DataManager] Metadata initialized")
    
    def _save_metadata(self):
        """Save metadata to disk."""
        data = {
            "sites": self.sites_registry,
            "examples": self.query_examples,
            "columns": self.column_metadata
        }
        with open(os.path.join(self.metadata_path, "metadata.json"), "w") as f:
            json.dump(data, f, indent=2, default=str)
    
    def _load_metadata(self):
        """Load metadata from disk."""
        path = os.path.join(self.metadata_path, "metadata.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
                self.sites_registry = data.get("sites", [])
                self.query_examples = data.get("examples", [])
                self.column_metadata = data.get("columns", [])
    
    def _populate_site_registry(self):
        """Populate site registry from Excel data."""
        if self.df is None:
            return
        
        # Check if already populated
        if len(self.sites_registry) > 0:
            print(f"[DataManager] Site registry already has {len(self.sites_registry)} entries")
            return
        
        # Get unique sites with their date ranges
        for site_id in self.df['site'].unique():
            site_data = self.df[self.df['site'] == site_id]
            
            min_date = site_data['sample_date'].min()
            max_date = site_data['sample_date'].max()
            sample_count = len(site_data)
            
            # Get years active
            years = sorted(site_data['year'].dropna().unique())
            year_range = f"{int(min(years))}-{int(max(years))}" if len(years) > 0 else "unknown"
            
            description = f"Site {site_id}, monitored {year_range}, {sample_count} samples"
            
            self.sites_registry.append({
                "site_id": str(site_id),
                "description": description,
                "first_sample": str(min_date),
                "last_sample": str(max_date),
                "sample_count": sample_count,
                "years_active": year_range
            })
        
        print(f"[DataManager] Added {len(self.sites_registry)} sites to registry")
    
    def _populate_column_metadata(self):
        """Populate column descriptions to help LLM understand the data."""
        if len(self.column_metadata) > 0:
            return
        
        # Column descriptions for water quality parameters
        column_descriptions = {
            "sample_date": "Date when the water sample was collected",
            "site": "Site identifier/number where sample was taken",
            "year": "Year of sample collection",
            "month": "Month of sample collection (1-12)",
            "season": "Season (Winter, Spring, Summer, Fall)",
            "time": "Time of day when sample was collected",
            "air_temp.c": "Air temperature in degrees Celsius",
            "water_temp.c": "Water temperature in degrees Celsius",
            "dissolved_oxygen.percent": "Dissolved oxygen as percentage saturation",
            "dissolved_oxygen.mg_per_l": "Dissolved oxygen in milligrams per liter",
            "uncompensated_conductivity.us_per_cm": "Uncompensated electrical conductivity in microsiemens per cm",
            "compensated_conductivity.us_per_cm": "Temperature-compensated conductivity in microsiemens per cm",
            "ph": "pH level (acidity/alkalinity, scale 0-14)",
            "turbidity.ntu": "Turbidity in Nephelometric Turbidity Units (water clarity)",
            "phycocyanin.rfu_tot": "Phycocyanin total relative fluorescence units (cyanobacteria indicator)",
            "cdom.rfu_tot": "Colored Dissolved Organic Matter total RFU",
            "optical_brightness.rfu_tot": "Optical brightness total RFU",
            "chlorophyll_a.rfu_tot": "Chlorophyll-a total RFU (algae indicator)",
            "phycocyanin.rfu_0.22": "Phycocyanin RFU filtered at 0.22 microns",
            "cdom.rfu_0.22": "CDOM RFU filtered at 0.22 microns",
            "ob.rfu_0.22": "Optical brightness RFU filtered at 0.22 microns",
            "chlorophyll_a.rfu_0.22": "Chlorophyll-a RFU filtered at 0.22 microns",
            "entero.cfu_per_100ml": "Enterococcus colony forming units per 100mL (fecal indicator bacteria)",
            "total_coliforms.cfu_per_100ml": "Total coliform bacteria CFU per 100mL",
            "ecoli.cfu_per_100ml": "E. coli colony forming units per 100mL (fecal contamination indicator)",
            "fecal_coliform.mft_per_100ml": "Fecal coliform by membrane filtration per 100mL",
            "fecal_strep.mft_per_100ml": "Fecal streptococcus by membrane filtration per 100mL",
            "fc_to_fs.ratio": "Fecal coliform to fecal strep ratio (human vs animal source indicator)",
            "total_coliform.mft_per_100ml": "Total coliform by membrane filtration per 100mL",
            "weather_obs": "Weather observations at time of sampling",
            "cloud_cover_obs": "Cloud cover observations",
            "rain7.in": "Rainfall in past 7 days (inches)",
            "rain28.in": "Rainfall in past 28 days (inches)",
            "rainmonthprior.in": "Rainfall in prior month (inches)",
            "observations and notes": "Field observations and notes"
        }
        
        for col in self.df.columns:
            col_lower = col.lower()
            description = column_descriptions.get(col_lower, f"Data column: {col}")
            dtype = str(self.df[col].dtype)
            non_null = self.df[col].notna().sum()
            
            self.column_metadata.append({
                "column_name": col,
                "data_type": dtype,
                "non_null_count": int(non_null),
                "description": description
            })
        
        print(f"[DataManager] Added {len(self.column_metadata)} column descriptions")
    
    def _populate_query_examples(self):
        """Populate example queries to help LLM generate better code."""
        if len(self.query_examples) > 0:
            return
        
        self.query_examples = [
            {
                "question": "coldest january water temperature",
                "code": "result = df[df['month'] == 1].groupby('year')['water_temp.C'].mean().idxmin()"
            },
            {
                "question": "which january had the coldest water temperature between 1981 and 1995",
                "code": "jan_data = df[(df['month'] == 1) & (df['year'] >= 1981) & (df['year'] <= 1995)]\nresult = jan_data.groupby('year')['water_temp.C'].mean().sort_values()"
            },
            {
                "question": "highest ecoli reading",
                "code": "result = df.loc[df['ecoli.CFU_per_100mL'].idxmax()][['sample_date', 'site', 'ecoli.CFU_per_100mL']]"
            },
            {
                "question": "average dissolved oxygen by year",
                "code": "result = df.groupby('year')['dissolved_oxygen.mg_per_L'].mean().reset_index()"
            },
            {
                "question": "water quality trends over time",
                "code": "result = df.groupby('year')[['water_temp.C', 'dissolved_oxygen.mg_per_L', 'ph', 'turbidity.ntu']].mean()"
            },
            {
                "question": "sites with highest bacteria levels",
                "code": "result = df.groupby('site')['ecoli.CFU_per_100mL'].mean().nlargest(5)"
            },
            {
                "question": "seasonal water temperature patterns",
                "code": "result = df.groupby('season')['water_temp.C'].agg(['mean', 'min', 'max'])"
            },
            {
                "question": "compare summer and winter dissolved oxygen",
                "code": "result = df[df['season'].isin(['Summer', 'Winter'])].groupby('season')['dissolved_oxygen.mg_per_L'].describe()"
            },
            {
                "question": "data for specific site",
                "code": "result = df[df['site'] == 2][['sample_date', 'water_temp.C', 'dissolved_oxygen.mg_per_L', 'ph', 'ecoli.CFU_per_100mL']].tail(10)"
            },
            {
                "question": "correlation between temperature and dissolved oxygen",
                "code": "result = df[['water_temp.C', 'dissolved_oxygen.mg_per_L']].corr()"
            },
            {
                "question": "monthly averages for a parameter",
                "code": "result = df.groupby('month')['turbidity.ntu'].mean().reset_index()"
            },
            {
                "question": "samples collected in specific year",
                "code": "result = df[df['year'] == 2020][['sample_date', 'site', 'water_temp.C', 'dissolved_oxygen.mg_per_L']]"
            },
            {
                "question": "rainy vs dry period water quality",
                "code": "df['high_rain'] = df['rain7.in'] > df['rain7.in'].median()\nresult = df.groupby('high_rain')[['turbidity.ntu', 'ecoli.CFU_per_100mL']].mean()"
            },
            {
                "question": "how many samples per site",
                "code": "result = df.groupby('site').size().reset_index(name='sample_count').sort_values('sample_count', ascending=False)"
            },
            {
                "question": "date range of data",
                "code": "result = pd.DataFrame({'First Sample': [df['sample_date'].min()], 'Last Sample': [df['sample_date'].max()], 'Total Samples': [len(df)]})"
            }
        ]
        
        print(f"[DataManager] Added {len(self.query_examples)} query examples")
    
    def search_sites(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search for sites by natural language description."""
        if not self.sites_registry:
            return []
        
        # Score each site by similarity to query
        scored = []
        for site in self.sites_registry:
            score = self._similarity(query, site['description'])
            # Check for site number in query
            if str(site['site_id']) in query:
                score += 0.5
            scored.append((score, site))
        
        # Sort by score and return top n
        scored.sort(key=lambda x: x[0], reverse=True)
        return [s[1] for s in scored[:n_results]]
    
    def get_similar_examples(self, query: str, n_results: int = 3) -> List[Dict]:
        """Get similar query examples for few-shot prompting."""
        if not self.query_examples:
            return []
        
        # Score each example by similarity
        scored = []
        for ex in self.query_examples:
            score = self._similarity(query, ex['question'])
            scored.append((score, ex))
        
        # Sort by score and return top n
        scored.sort(key=lambda x: x[0], reverse=True)
        return [s[1] for s in scored[:n_results]]
    
    def get_relevant_columns(self, query: str, n_results: int = 10) -> List[Dict]:
        """Get column descriptions relevant to the query."""
        if not self.column_metadata:
            return []
        
        # Score each column by similarity
        scored = []
        for col in self.column_metadata:
            search_text = f"{col['column_name']} {col['description']}"
            score = self._similarity(query, search_text)
            scored.append((score, col))
        
        # Sort by score and return top n
        scored.sort(key=lambda x: x[0], reverse=True)
        return [s[1] for s in scored[:n_results]]
    
    def add_monthly_data(self, new_data: pd.DataFrame, month: str):
        """
        Add new monthly data to the Excel file.
        
        Args:
            new_data: DataFrame with new rows (typically ~15 sites)
            month: Month identifier (e.g., "2025-01")
        """
        # Load current data
        master_df = self.get_data()
        
        # Verify sites exist in registry
        new_sites = set(new_data['site'].unique())
        self._verify_sites(new_sites, month)
        
        # Append new data
        updated_df = pd.concat([master_df, new_data], ignore_index=True)
        
        # Read all sheets to preserve them
        with pd.ExcelFile(self.excel_path) as xls:
            all_sheets = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}
        
        # Update FieldData
        all_sheets[self.SHEET_NAME] = updated_df
        
        # Write all sheets back
        with pd.ExcelWriter(self.excel_path, engine='openpyxl') as writer:
            for sheet_name, sheet_df in all_sheets.items():
                sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Reload
        self.df = None
        self._load_excel()
        
        # Update site registry if new sites found
        self.sites_registry = []  # Reset
        self._populate_site_registry()
        self._save_metadata()
        
        print(f"[DataManager] Added {len(new_data)} rows for {month}")
    
    def _verify_sites(self, site_ids: set, month: str):
        """Check if all sites are in the registry."""
        known_sites = {s['site_id'] for s in self.sites_registry}
        
        for site_id in site_ids:
            if str(site_id) not in known_sites:
                print(f"⚠️  Warning: New site '{site_id}' in {month} data - will be added to registry")
    
    def register_new_site(self, site_id: str, description: str = ""):
        """Register a new site manually."""
        doc = f"Site {site_id}, {description}" if description else f"Site {site_id}"
        
        self.sites_registry.append({
            "site_id": str(site_id),
            "description": doc,
            "added_date": datetime.now().isoformat()
        })
        
        self._save_metadata()
        print(f"[DataManager] Registered new site: {site_id}")
    
    def get_schema_description(self) -> str:
        """Generate a schema description for the LLM."""
        if self.df is None:
            return "No data loaded"
        
        # Get date range
        date_range = ""
        if 'sample_date' in self.df.columns:
            min_date = self.df['sample_date'].min()
            max_date = self.df['sample_date'].max()
            date_range = f"Date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}"
        
        schema_lines = [
            f"DataFrame with {len(self.df)} rows and {len(self.df.columns)} columns.",
            date_range,
            f"Sites: {sorted(self.df['site'].unique())}",
            "",
            "Columns:"
        ]
        
        for col in self.df.columns:
            dtype = str(self.df[col].dtype)
            non_null = self.df[col].notna().sum()
            
            # Sample values
            samples = self.df[col].dropna().head(3).tolist()
            sample_str = ", ".join([str(s)[:20] for s in samples])
            
            schema_lines.append(f"  - {col} ({dtype}): {non_null} non-null, samples: [{sample_str}]")
        
        return "\n".join(schema_lines)
    
    def get_data_summary(self) -> Dict:
        """Get a summary of the data for display."""
        if self.df is None:
            return {}
        
        return {
            "total_samples": len(self.df),
            "total_sites": self.df['site'].nunique(),
            "date_range": f"{self.df['sample_date'].min()} to {self.df['sample_date'].max()}",
            "years_covered": sorted(self.df['year'].dropna().unique().astype(int).tolist()),
            "columns": len(self.df.columns)
        }
