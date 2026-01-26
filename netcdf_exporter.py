"""
NetCDF Exporter Module
Converts water quality data from Excel/DataFrame to NetCDF format
following CF (Climate and Forecast) conventions.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional, Dict, Any
import os

try:
    import netCDF4 as nc
    HAS_NETCDF4 = True
except ImportError:
    HAS_NETCDF4 = False


# CF-compliant variable metadata
VARIABLE_METADATA = {
    'water_temp.C': {
        'standard_name': 'sea_water_temperature',
        'long_name': 'Water Temperature',
        'units': 'degree_Celsius',
        'valid_min': -5.0,
        'valid_max': 50.0,
    },
    'air_temp.C': {
        'standard_name': 'air_temperature',
        'long_name': 'Air Temperature',
        'units': 'degree_Celsius',
        'valid_min': -40.0,
        'valid_max': 50.0,
    },
    'dissolved_oxygen.mg_per_L': {
        'standard_name': 'mass_concentration_of_oxygen_in_sea_water',
        'long_name': 'Dissolved Oxygen',
        'units': 'mg/L',
        'valid_min': 0.0,
        'valid_max': 20.0,
    },
    'dissolved_oxygen.percent': {
        'long_name': 'Dissolved Oxygen Saturation',
        'units': 'percent',
        'valid_min': 0.0,
        'valid_max': 200.0,
    },
    'ph': {
        'standard_name': 'sea_water_ph_reported_on_total_scale',
        'long_name': 'pH',
        'units': '1',
        'valid_min': 0.0,
        'valid_max': 14.0,
    },
    'turbidity.ntu': {
        'long_name': 'Turbidity',
        'units': 'NTU',
        'valid_min': 0.0,
        'valid_max': 5000.0,
    },
    'compensated_conductivity.uS_per_cm': {
        'standard_name': 'sea_water_electrical_conductivity',
        'long_name': 'Electrical Conductivity (temperature compensated)',
        'units': 'uS/cm',
        'valid_min': 0.0,
        'valid_max': 100000.0,
    },
    'uncompensated_conductivity.uS_per_cm': {
        'long_name': 'Electrical Conductivity (uncompensated)',
        'units': 'uS/cm',
        'valid_min': 0.0,
        'valid_max': 100000.0,
    },
    'ecoli.CFU_per_100mL': {
        'long_name': 'Escherichia coli',
        'units': 'CFU/100mL',
        'valid_min': 0.0,
        'comment': 'Colony forming units per 100 milliliters',
    },
    'entero.CFU_per_100mL': {
        'long_name': 'Enterococcus',
        'units': 'CFU/100mL',
        'valid_min': 0.0,
        'comment': 'Colony forming units per 100 milliliters',
    },
    'total_coliforms.CFU_per_100mL': {
        'long_name': 'Total Coliforms',
        'units': 'CFU/100mL',
        'valid_min': 0.0,
        'comment': 'Colony forming units per 100 milliliters',
    },
    'fecal_coliform.MFT_per_100mL': {
        'long_name': 'Fecal Coliform',
        'units': 'MFT/100mL',
        'valid_min': 0.0,
        'comment': 'Membrane filter technique count per 100 milliliters',
    },
    'fecal_strep.MFT_per_100ml': {
        'long_name': 'Fecal Streptococcus',
        'units': 'MFT/100mL',
        'valid_min': 0.0,
        'comment': 'Membrane filter technique count per 100 milliliters',
    },
    'total_coliform.MFT_per_100ml': {
        'long_name': 'Total Coliform (MFT)',
        'units': 'MFT/100mL',
        'valid_min': 0.0,
    },
    'fc_to_fs.ratio': {
        'long_name': 'Fecal Coliform to Fecal Strep Ratio',
        'units': '1',
        'comment': 'Ratio used to distinguish human vs animal fecal contamination',
    },
    'chlorophyll_a.RFU_tot': {
        'long_name': 'Chlorophyll-a (total)',
        'units': 'RFU',
        'comment': 'Relative Fluorescence Units',
    },
    'chlorophyll_a.RFU_0.22': {
        'long_name': 'Chlorophyll-a (0.22um filtered)',
        'units': 'RFU',
    },
    'phycocyanin.RFU_tot': {
        'long_name': 'Phycocyanin (total)',
        'units': 'RFU',
        'comment': 'Cyanobacteria indicator',
    },
    'phycocyanin.RFU_0.22': {
        'long_name': 'Phycocyanin (0.22um filtered)',
        'units': 'RFU',
    },
    'CDOM.RFU_tot': {
        'long_name': 'Colored Dissolved Organic Matter (total)',
        'units': 'RFU',
    },
    'CDOM.RFU_0.22': {
        'long_name': 'Colored Dissolved Organic Matter (0.22um filtered)',
        'units': 'RFU',
    },
    'optical_brightness.RFU_tot': {
        'long_name': 'Optical Brightness (total)',
        'units': 'RFU',
    },
    'OB.RFU_0.22': {
        'long_name': 'Optical Brightness (0.22um filtered)',
        'units': 'RFU',
    },
    'rain7.in': {
        'long_name': 'Rainfall in Past 7 Days',
        'units': 'inches',
        'valid_min': 0.0,
    },
    'rain28.in': {
        'long_name': 'Rainfall in Past 28 Days',
        'units': 'inches',
        'valid_min': 0.0,
    },
    'rainmonthprior.in': {
        'long_name': 'Rainfall in Prior Month',
        'units': 'inches',
        'valid_min': 0.0,
    },
}


class NetCDFExporter:
    """Exports water quality data to NetCDF format."""
    
    def __init__(self, data_manager):
        """
        Initialize the exporter.
        
        Args:
            data_manager: DataManager instance with loaded data
        """
        self.data_manager = data_manager
        
        if not HAS_NETCDF4:
            raise ImportError(
                "netCDF4 package is required. Install with:\n"
                "python3 -m pip install netCDF4"
            )
    
    def export(
        self,
        output_path: str,
        title: str = "Water Quality Monitoring Data",
        institution: str = "Bard College",
        source: str = "Field measurements",
        comment: str = "",
        compress: bool = True
    ) -> str:
        """
        Export data to NetCDF file.
        
        Args:
            output_path: Path for output .nc file
            title: Dataset title
            institution: Institution name
            source: Data source description
            comment: Additional comments
            compress: Whether to compress variables
            
        Returns:
            Path to created file
        """
        df = self.data_manager.get_data()
        
        # Ensure output has .nc extension
        if not output_path.endswith('.nc'):
            output_path += '.nc'
        
        # Create NetCDF file
        with nc.Dataset(output_path, 'w', format='NETCDF4') as ds:
            # Add global attributes (CF conventions)
            ds.Conventions = 'CF-1.8'
            ds.title = title
            ds.institution = institution
            ds.source = source
            ds.history = f"Created {datetime.now().isoformat()} from Excel data"
            ds.references = ""
            ds.comment = comment
            ds.featureType = "timeSeries"
            
            # Get unique sites and times
            sites = sorted(df['site'].unique())
            times = pd.to_datetime(df['sample_date']).sort_values().unique()
            
            # Create dimensions
            ds.createDimension('time', len(times))
            ds.createDimension('site', len(sites))
            ds.createDimension('name_strlen', 50)  # For site names
            
            # Create time variable
            time_var = ds.createVariable('time', 'f8', ('time',), zlib=compress)
            time_var.standard_name = 'time'
            time_var.long_name = 'Sample Date'
            time_var.units = f'days since 1970-01-01 00:00:00'
            time_var.calendar = 'gregorian'
            time_var.axis = 'T'
            
            # Convert times to numeric
            time_numeric = (pd.to_datetime(times) - pd.Timestamp('1970-01-01')).days
            time_var[:] = time_numeric
            
            # Create site variable (as string)
            site_var = ds.createVariable('site', 'S1', ('site', 'name_strlen'))
            site_var.long_name = 'Monitoring Site Identifier'
            site_var.cf_role = 'timeseries_id'
            
            # Write site names
            for i, site in enumerate(sites):
                site_str = str(site).ljust(50)[:50]
                site_var[i] = nc.stringtochar(np.array([site_str], 'S50'))
            
            # Create a lookup for fast indexing
            site_to_idx = {s: i for i, s in enumerate(sites)}
            time_to_idx = {pd.Timestamp(t): i for i, t in enumerate(times)}
            
            # Create data variables
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            skip_cols = {'year', 'month', 'site'}  # These are dimensions/coordinates
            
            for col in numeric_cols:
                if col in skip_cols:
                    continue
                
                # Get metadata
                meta = VARIABLE_METADATA.get(col, {
                    'long_name': col.replace('_', ' ').replace('.', ' ').title(),
                    'units': 'unknown'
                })
                
                # Create variable (time, site)
                var = ds.createVariable(
                    col.replace('.', '_').replace(' ', '_'),  # NetCDF-safe name
                    'f4',
                    ('time', 'site'),
                    zlib=compress,
                    fill_value=np.nan
                )
                
                # Add attributes
                for attr, value in meta.items():
                    setattr(var, attr, value)
                
                # Fill data array
                data_array = np.full((len(times), len(sites)), np.nan, dtype=np.float32)
                
                for _, row in df.iterrows():
                    try:
                        t_idx = time_to_idx.get(pd.Timestamp(row['sample_date']))
                        s_idx = site_to_idx.get(row['site'])
                        if t_idx is not None and s_idx is not None and pd.notna(row[col]):
                            data_array[t_idx, s_idx] = row[col]
                    except (KeyError, TypeError):
                        continue
                
                var[:] = data_array
            
            # Add season as auxiliary coordinate
            if 'season' in df.columns:
                season_var = ds.createVariable('season', 'S1', ('time', 'name_strlen'), zlib=compress)
                season_var.long_name = 'Season'
                
                # Get season for each time
                time_to_season = df.groupby('sample_date')['season'].first().to_dict()
                for i, t in enumerate(times):
                    season = str(time_to_season.get(pd.Timestamp(t), '')).ljust(50)[:50]
                    season_var[i] = nc.stringtochar(np.array([season], 'S50'))
        
        print(f"[NetCDFExporter] Exported to {output_path}")
        print(f"  - {len(times)} time points")
        print(f"  - {len(sites)} sites")
        print(f"  - {len(numeric_cols) - len(skip_cols)} variables")
        
        return output_path
    
    def get_export_summary(self) -> Dict[str, Any]:
        """Get summary of what will be exported."""
        df = self.data_manager.get_data()
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        skip_cols = {'year', 'month', 'site'}
        data_vars = [c for c in numeric_cols if c not in skip_cols]
        
        return {
            'time_range': f"{df['sample_date'].min()} to {df['sample_date'].max()}",
            'num_samples': len(df),
            'num_sites': df['site'].nunique(),
            'num_time_points': df['sample_date'].nunique(),
            'variables': data_vars,
            'variables_with_metadata': [v for v in data_vars if v in VARIABLE_METADATA],
        }


def check_netcdf_available() -> bool:
    """Check if NetCDF4 is available."""
    return HAS_NETCDF4
