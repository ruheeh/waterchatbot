"""
Query Engine Module (Free - No AI Dependency)
Uses pattern matching and keyword extraction to interpret natural language queries
and generate pandas code. Runs completely offline with no API costs.
"""

import pandas as pd
import re
from typing import Tuple, Optional, Dict, List, Any
from datetime import datetime


class QueryEngine:
    """Processes natural language queries using pattern matching."""
    
    def __init__(self, data_manager):
        """
        Initialize the query engine.
        
        Args:
            data_manager: DataManager instance with loaded data
        """
        self.data_manager = data_manager
        self._build_patterns()
    
    def _build_patterns(self):
        """Build regex patterns for query matching."""
        
        # Column name mappings (user-friendly -> actual column name)
        self.column_aliases = {
            # Temperature
            'water temperature': 'water_temp.C',
            'water temp': 'water_temp.C',
            'temperature': 'water_temp.C',
            'temp': 'water_temp.C',
            'air temperature': 'air_temp.C',
            'air temp': 'air_temp.C',
            
            # Dissolved oxygen
            'dissolved oxygen': 'dissolved_oxygen.mg_per_L',
            'do': 'dissolved_oxygen.mg_per_L',
            'oxygen': 'dissolved_oxygen.mg_per_L',
            
            # Bacteria
            'ecoli': 'ecoli.CFU_per_100mL',
            'e coli': 'ecoli.CFU_per_100mL',
            'e. coli': 'ecoli.CFU_per_100mL',
            'enterococcus': 'entero.CFU_per_100mL',
            'entero': 'entero.CFU_per_100mL',
            'total coliform': 'total_coliforms.CFU_per_100mL',
            'coliform': 'total_coliforms.CFU_per_100mL',
            'fecal coliform': 'fecal_coliform.MFT_per_100mL',
            'bacteria': 'ecoli.CFU_per_100mL',
            
            # Other parameters
            'ph': 'ph',
            'turbidity': 'turbidity.ntu',
            'conductivity': 'compensated_conductivity.uS_per_cm',
            'chlorophyll': 'chlorophyll_a.RFU_tot',
            'rainfall': 'rain7.in',
            'rain': 'rain7.in',
        }
        
        # Month mappings
        self.month_names = {
            'january': 1, 'jan': 1,
            'february': 2, 'feb': 2,
            'march': 3, 'mar': 3,
            'april': 4, 'apr': 4,
            'may': 5,
            'june': 6, 'jun': 6,
            'july': 7, 'jul': 7,
            'august': 8, 'aug': 8,
            'september': 9, 'sep': 9, 'sept': 9,
            'october': 10, 'oct': 10,
            'november': 11, 'nov': 11,
            'december': 12, 'dec': 12,
        }
        
        # Season mappings
        self.season_names = ['winter', 'spring', 'summer', 'fall', 'autumn']
        
        # Aggregation keywords
        self.agg_keywords = {
            'average': 'mean',
            'avg': 'mean',
            'mean': 'mean',
            'maximum': 'max',
            'max': 'max',
            'highest': 'max',
            'minimum': 'min',
            'min': 'min',
            'lowest': 'min',
            'coldest': 'min',
            'warmest': 'max',
            'hottest': 'max',
            'total': 'sum',
            'sum': 'sum',
            'count': 'count',
        }
    
    def query(self, question: str) -> Tuple[str, Optional[pd.DataFrame]]:
        """
        Process a natural language query and return results.
        
        Args:
            question: Natural language question about the data
            
        Returns:
            Tuple of (explanation text, optional result DataFrame)
        """
        question_lower = question.lower().strip()
        df = self.data_manager.get_data()
        
        try:
            # Try different query patterns (ORDER MATTERS - more specific first)
            
            # Pattern 1: Correlation between parameters (check early)
            result = self._handle_correlation_query(question_lower, df)
            if result:
                return result
            
            # Pattern 2: Compare [parameter] between [seasons/sites]
            result = self._handle_comparison_query(question_lower, df)
            if result:
                return result
            
            # Pattern 3: Coldest/warmest/highest/lowest [month] [parameter] [year range]
            result = self._handle_extreme_query(question_lower, df)
            if result:
                return result
            
            # Pattern 4: Average/mean [parameter] by [grouping]
            result = self._handle_aggregation_query(question_lower, df)
            if result:
                return result
            
            # Pattern 5: Show/get data for site X
            result = self._handle_site_query(question_lower, df)
            if result:
                return result
            
            # Pattern 6: Data in year X or date range
            result = self._handle_time_query(question_lower, df)
            if result:
                return result
            
            # Pattern 7: Count/how many queries
            result = self._handle_count_query(question_lower, df)
            if result:
                return result
            
            # Pattern 8: Trend/over time queries
            result = self._handle_trend_query(question_lower, df)
            if result:
                return result
            
            # Pattern 9: Summary/describe queries
            result = self._handle_summary_query(question_lower, df)
            if result:
                return result
            
            # Pattern 10: List sites/parameters
            result = self._handle_list_query(question_lower, df)
            if result:
                return result
            
            # Default: Show help
            return self._show_help()
            
        except Exception as e:
            return f"Error processing query: {str(e)}", None
    
    def _extract_parameter(self, text: str) -> Optional[str]:
        """Extract the parameter/column name from text."""
        text_lower = text.lower()
        
        for alias, column in self.column_aliases.items():
            if alias in text_lower:
                return column
        
        return None
    
    def _extract_month(self, text: str) -> Optional[int]:
        """Extract month number from text."""
        text_lower = text.lower()
        
        for name, num in self.month_names.items():
            if name in text_lower:
                return num
        
        return None
    
    def _extract_year_range(self, text: str) -> Tuple[Optional[int], Optional[int]]:
        """Extract year range from text."""
        # Pattern: "from 1981 to 1995" or "between 1981 and 1995" or "1981-1995"
        
        patterns = [
            r'from\s+(\d{4})\s+to\s+(\d{4})',
            r'between\s+(\d{4})\s+and\s+(\d{4})',
            r'(\d{4})\s*[-–]\s*(\d{4})',
            r'(\d{4})\s+to\s+(\d{4})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return int(match.group(1)), int(match.group(2))
        
        # Single year
        match = re.search(r'\b(19\d{2}|20\d{2})\b', text)
        if match:
            year = int(match.group(1))
            return year, year
        
        return None, None
    
    def _extract_site(self, text: str) -> Optional[Any]:
        """Extract site identifier from text."""
        # Pattern: "site 2" or "site 2.5"
        match = re.search(r'site\s+(\d+\.?\d*)', text.lower())
        if match:
            site_str = match.group(1)
            return float(site_str) if '.' in site_str else int(site_str)
        
        return None
    
    def _extract_aggregation(self, text: str) -> str:
        """Extract aggregation type from text."""
        text_lower = text.lower()
        
        for keyword, agg_func in self.agg_keywords.items():
            if keyword in text_lower:
                return agg_func
        
        return 'mean'  # Default
    
    def _extract_season(self, text: str) -> Optional[str]:
        """Extract season from text."""
        text_lower = text.lower()
        
        for season in self.season_names:
            if season in text_lower:
                if season == 'autumn':
                    return 'Fall'
                return season.capitalize()
        
        return None
    
    def _handle_extreme_query(self, question: str, df: pd.DataFrame) -> Optional[Tuple[str, pd.DataFrame]]:
        """Handle queries like 'coldest january water temperature from 1981 to 1995'."""
        
        # Check for extreme keywords
        agg_type = None
        for keyword, agg in self.agg_keywords.items():
            if keyword in question:
                if agg in ['min', 'max']:
                    agg_type = agg
                    break
        
        if not agg_type:
            return None
        
        # Extract components
        param = self._extract_parameter(question)
        if not param or param not in df.columns:
            return None
        
        month = self._extract_month(question)
        year_start, year_end = self._extract_year_range(question)
        season = self._extract_season(question)
        
        # Build query
        filtered_df = df.copy()
        filter_desc = []
        
        if month:
            filtered_df = filtered_df[filtered_df['month'] == month]
            month_name = [k for k, v in self.month_names.items() if v == month][0].capitalize()
            filter_desc.append(f"month = {month_name}")
        
        if season:
            filtered_df = filtered_df[filtered_df['season'] == season]
            filter_desc.append(f"season = {season}")
        
        if year_start and year_end:
            filtered_df = filtered_df[(filtered_df['year'] >= year_start) & (filtered_df['year'] <= year_end)]
            filter_desc.append(f"years {year_start}-{year_end}")
        
        if len(filtered_df) == 0:
            return "No data found matching your criteria.", None
        
        # Calculate by year
        yearly = filtered_df.groupby('year')[param].mean()
        
        if agg_type == 'min':
            result_year = yearly.idxmin()
            result_value = yearly.min()
            extreme_word = "lowest"
        else:
            result_year = yearly.idxmax()
            result_value = yearly.max()
            extreme_word = "highest"
        
        # Build result dataframe
        result_df = yearly.reset_index()
        result_df.columns = ['Year', f'Avg {param}']
        result_df = result_df.sort_values(f'Avg {param}')
        
        filter_str = " with " + ", ".join(filter_desc) if filter_desc else ""
        explanation = f"The {extreme_word} average {param}{filter_str} was in {int(result_year)} with a value of {result_value:.2f}."
        
        return explanation, result_df
    
    def _handle_aggregation_query(self, question: str, df: pd.DataFrame) -> Optional[Tuple[str, pd.DataFrame]]:
        """Handle queries like 'average dissolved oxygen by year'."""
        
        agg_type = self._extract_aggregation(question)
        param = self._extract_parameter(question)
        
        if not param or param not in df.columns:
            return None
        
        # Determine grouping
        if 'by year' in question or 'per year' in question or 'yearly' in question:
            group_col = 'year'
        elif 'by month' in question or 'per month' in question or 'monthly' in question:
            group_col = 'month'
        elif 'by season' in question or 'per season' in question or 'seasonal' in question:
            group_col = 'season'
        elif 'by site' in question or 'per site' in question:
            group_col = 'site'
        else:
            # Overall aggregation
            result_value = getattr(df[param].dropna(), agg_type)()
            explanation = f"The {agg_type} {param} across all data is {result_value:.2f}"
            result_df = pd.DataFrame({param: [result_value], 'Aggregation': [agg_type]})
            return explanation, result_df
        
        # Group and aggregate
        result = df.groupby(group_col)[param].agg(agg_type).reset_index()
        result.columns = [group_col.capitalize(), f'{agg_type.capitalize()} {param}']
        
        explanation = f"{agg_type.capitalize()} {param} grouped by {group_col}:"
        
        return explanation, result
    
    def _handle_site_query(self, question: str, df: pd.DataFrame) -> Optional[Tuple[str, pd.DataFrame]]:
        """Handle queries like 'show data for site 2'."""
        
        if 'site' not in question:
            return None
        
        site = self._extract_site(question)
        if site is None:
            return None
        
        site_df = df[df['site'] == site]
        
        if len(site_df) == 0:
            return f"No data found for site {site}.", None
        
        # Select relevant columns
        display_cols = ['sample_date', 'site', 'water_temp.C', 'dissolved_oxygen.mg_per_L', 
                       'ph', 'turbidity.ntu', 'ecoli.CFU_per_100mL']
        display_cols = [c for c in display_cols if c in site_df.columns]
        
        # Check for year filter
        year_start, year_end = self._extract_year_range(question)
        if year_start:
            site_df = site_df[(site_df['year'] >= year_start) & (site_df['year'] <= year_end)]
        
        result_df = site_df[display_cols].tail(20)
        
        explanation = f"Data for site {site} ({len(site_df)} total samples, showing last 20):"
        
        return explanation, result_df
    
    def _handle_comparison_query(self, question: str, df: pd.DataFrame) -> Optional[Tuple[str, pd.DataFrame]]:
        """Handle queries like 'compare summer vs winter temperature' or 'compare january 2026 and november 2023'."""
        
        if 'compare' not in question and ' vs ' not in question and 'versus' not in question and 'between' not in question:
            return None
        
        param = self._extract_parameter(question)
        if not param or param not in df.columns:
            # Try to find a parameter mentioned
            for alias, col in self.column_aliases.items():
                if alias in question and col in df.columns:
                    param = col
                    break
            if not param:
                param = 'water_temp.C'  # Default
        
        # Check for two month-year combinations (e.g., "january 2026 and november 2023")
        month_year_pattern = r'(\w+)\s+(\d{4})'
        matches = re.findall(month_year_pattern, question)
        
        if len(matches) >= 2:
            # Extract two time periods
            periods = []
            for month_str, year_str in matches[:2]:
                month_num = self.month_names.get(month_str.lower())
                if month_num:
                    periods.append((month_num, int(year_str), f"{month_str.capitalize()} {year_str}"))
            
            if len(periods) == 2:
                results = []
                for month, year, label in periods:
                    period_df = df[(df['month'] == month) & (df['year'] == year)]
                    if len(period_df) > 0:
                        stats = {
                            'Period': label,
                            'Mean': period_df[param].mean(),
                            'Min': period_df[param].min(),
                            'Max': period_df[param].max(),
                            'Count': period_df[param].notna().sum()
                        }
                        results.append(stats)
                
                if results:
                    result_df = pd.DataFrame(results)
                    explanation = f"Comparison of {param} between {periods[0][2]} and {periods[1][2]}:"
                    return explanation, result_df
                else:
                    return f"No data found for the specified time periods.", None
        
        # Check for season comparison
        seasons_found = []
        for season in self.season_names:
            if season in question:
                seasons_found.append('Fall' if season == 'autumn' else season.capitalize())
        
        if len(seasons_found) >= 2:
            result = df[df['season'].isin(seasons_found)].groupby('season')[param].agg(['mean', 'min', 'max', 'count'])
            result = result.reset_index()
            explanation = f"Comparison of {param} between {' and '.join(seasons_found)}:"
            return explanation, result
        
        # Check if asking about seasons generally
        if 'season' in question or any(s in question for s in self.season_names):
            result = df.groupby('season')[param].agg(['mean', 'min', 'max', 'count']).reset_index()
            explanation = f"Comparison of {param} across all seasons:"
            return explanation, result
        
        return None
    
    def _handle_time_query(self, question: str, df: pd.DataFrame) -> Optional[Tuple[str, pd.DataFrame]]:
        """Handle queries like 'data from 2020' or 'samples in january 2019'."""
        
        year_start, year_end = self._extract_year_range(question)
        month = self._extract_month(question)
        
        if not year_start and not month:
            return None
        
        filtered_df = df.copy()
        filter_desc = []
        
        if year_start and year_end:
            if year_start == year_end:
                filtered_df = filtered_df[filtered_df['year'] == year_start]
                filter_desc.append(f"year {year_start}")
            else:
                filtered_df = filtered_df[(filtered_df['year'] >= year_start) & (filtered_df['year'] <= year_end)]
                filter_desc.append(f"years {year_start}-{year_end}")
        
        if month:
            filtered_df = filtered_df[filtered_df['month'] == month]
            month_name = [k for k, v in self.month_names.items() if v == month][0].capitalize()
            filter_desc.append(month_name)
        
        if len(filtered_df) == 0:
            return f"No data found for {', '.join(filter_desc)}.", None
        
        # Select display columns
        display_cols = ['sample_date', 'site', 'water_temp.C', 'dissolved_oxygen.mg_per_L', 'ph', 'ecoli.CFU_per_100mL']
        display_cols = [c for c in display_cols if c in filtered_df.columns]
        
        result_df = filtered_df[display_cols].head(30)
        
        explanation = f"Data for {', '.join(filter_desc)} ({len(filtered_df)} samples, showing first 30):"
        
        return explanation, result_df
    
    def _handle_correlation_query(self, question: str, df: pd.DataFrame) -> Optional[Tuple[str, pd.DataFrame]]:
        """Handle queries about correlation between parameters."""
        
        if 'correlation' not in question and 'correlate' not in question and 'relationship' not in question:
            return None
        
        # Try to find two parameters
        params_found = []
        for alias, column in self.column_aliases.items():
            if alias in question and column not in params_found:
                params_found.append(column)
        
        if len(params_found) < 2:
            # Default to temperature and dissolved oxygen
            params_found = ['water_temp.C', 'dissolved_oxygen.mg_per_L']
        
        # Calculate correlation
        corr_df = df[params_found].corr()
        corr_value = corr_df.iloc[0, 1]
        
        explanation = f"Correlation between {params_found[0]} and {params_found[1]}: {corr_value:.3f}"
        if corr_value > 0.7:
            explanation += " (strong positive correlation)"
        elif corr_value > 0.3:
            explanation += " (moderate positive correlation)"
        elif corr_value > -0.3:
            explanation += " (weak/no correlation)"
        elif corr_value > -0.7:
            explanation += " (moderate negative correlation)"
        else:
            explanation += " (strong negative correlation)"
        
        return explanation, corr_df
    
    def _handle_count_query(self, question: str, df: pd.DataFrame) -> Optional[Tuple[str, pd.DataFrame]]:
        """Handle queries like 'how many samples per site'."""
        
        if 'how many' not in question and 'count' not in question and 'number of' not in question:
            return None
        
        if 'site' in question:
            result = df.groupby('site').size().reset_index(name='sample_count')
            result = result.sort_values('sample_count', ascending=False)
            explanation = "Number of samples per site:"
        elif 'year' in question:
            result = df.groupby('year').size().reset_index(name='sample_count')
            explanation = "Number of samples per year:"
        elif 'month' in question:
            result = df.groupby('month').size().reset_index(name='sample_count')
            explanation = "Number of samples per month:"
        else:
            total = len(df)
            result = pd.DataFrame({'Total Samples': [total]})
            explanation = f"Total number of samples in the dataset: {total}"
        
        return explanation, result
    
    def _handle_trend_query(self, question: str, df: pd.DataFrame) -> Optional[Tuple[str, pd.DataFrame]]:
        """Handle queries about trends over time."""
        
        if 'trend' not in question and 'over time' not in question and 'change' not in question:
            return None
        
        param = self._extract_parameter(question)
        if not param or param not in df.columns:
            param = 'water_temp.C'
        
        # Calculate yearly averages
        yearly = df.groupby('year')[param].agg(['mean', 'min', 'max', 'count']).reset_index()
        yearly.columns = ['Year', 'Mean', 'Min', 'Max', 'Sample Count']
        
        # Calculate overall trend
        if len(yearly) > 1:
            first_val = yearly['Mean'].iloc[0]
            last_val = yearly['Mean'].iloc[-1]
            change = last_val - first_val
            change_pct = (change / first_val) * 100 if first_val != 0 else 0
            
            trend_desc = "increased" if change > 0 else "decreased"
            explanation = f"Trend of {param} over time: {trend_desc} by {abs(change):.2f} ({abs(change_pct):.1f}%) from {yearly['Year'].iloc[0]:.0f} to {yearly['Year'].iloc[-1]:.0f}"
        else:
            explanation = f"Yearly statistics for {param}:"
        
        return explanation, yearly
    
    def _handle_summary_query(self, question: str, df: pd.DataFrame) -> Optional[Tuple[str, pd.DataFrame]]:
        """Handle queries for summary statistics."""
        
        if 'summary' not in question and 'describe' not in question and 'statistics' not in question and 'stats' not in question:
            return None
        
        param = self._extract_parameter(question)
        
        if param and param in df.columns:
            result = df[param].describe().reset_index()
            result.columns = ['Statistic', param]
            explanation = f"Summary statistics for {param}:"
        else:
            # Overall summary
            numeric_cols = ['water_temp.C', 'dissolved_oxygen.mg_per_L', 'ph', 'turbidity.ntu', 'ecoli.CFU_per_100mL']
            numeric_cols = [c for c in numeric_cols if c in df.columns]
            result = df[numeric_cols].describe().T.reset_index()
            result.columns = ['Parameter', 'Count', 'Mean', 'Std', 'Min', '25%', '50%', '75%', 'Max']
            explanation = "Summary statistics for key water quality parameters:"
        
        return explanation, result
    
    def _handle_list_query(self, question: str, df: pd.DataFrame) -> Optional[Tuple[str, pd.DataFrame]]:
        """Handle queries to list sites, columns, etc."""
        
        if 'list' not in question and 'show all' not in question and 'what' not in question:
            return None
        
        if 'site' in question:
            sites = sorted(df['site'].unique())
            result = pd.DataFrame({'Sites': sites})
            explanation = f"All {len(sites)} sites in the dataset:"
            return explanation, result
        
        if 'column' in question or 'parameter' in question or 'variable' in question:
            cols = list(df.columns)
            result = pd.DataFrame({'Columns': cols})
            explanation = f"All {len(cols)} columns in the dataset:"
            return explanation, result
        
        if 'year' in question:
            years = sorted(df['year'].dropna().unique().astype(int))
            result = pd.DataFrame({'Years': years})
            explanation = f"All {len(years)} years in the dataset:"
            return explanation, result
        
        return None
    
    def _show_help(self) -> Tuple[str, pd.DataFrame]:
        """Show help message with example queries."""
        
        help_text = """I couldn't understand that query. Here are some examples of questions I can answer:

**Extreme values:**
- "What was the coldest January water temperature from 1981 to 1995?"
- "Highest E. coli reading"
- "Warmest summer on record"

**Averages and aggregations:**
- "Average dissolved oxygen by year"
- "Mean turbidity by season"
- "Average water temperature per site"

**Site queries:**
- "Show data for site 2"
- "Data for site 4 in 2020"

**Comparisons:**
- "Compare summer vs winter temperature"
- "Compare dissolved oxygen between seasons"

**Time-based queries:**
- "Data from 2020"
- "Samples in January 2019"

**Trends and correlations:**
- "Temperature trend over time"
- "Correlation between temperature and dissolved oxygen"

**Counts and summaries:**
- "How many samples per site?"
- "Summary statistics for pH"
- "List all sites"
"""
        
        examples = pd.DataFrame({
            'Example Questions': [
                'coldest january water temperature 1981 to 1995',
                'average dissolved oxygen by year',
                'show data for site 2',
                'compare summer vs winter temperature',
                'how many samples per site',
                'correlation between temperature and oxygen',
            ]
        })
        
        return help_text, examples
