"""
Water Quality Data Chatbot (Free Version - No AI Dependency)
A simple chatbot that answers questions about water monitoring data
using pattern matching. Runs completely offline with no API costs.
"""

import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
from data_manager import DataManager
from query_engine_free import QueryEngine


def load_config():
    """Load configuration from config.json"""
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    default_config = {
        "data_file": "./data/water_data.xlsx",
        "export_folder": "./data"
    }
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                # Merge with defaults
                return {**default_config, **config}
        except Exception as e:
            print(f"Error loading config: {e}")
    
    return default_config


# Load config
config = load_config()

# Page config
st.set_page_config(
    page_title="Water Quality Chatbot",
    page_icon="💧",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .example-btn {
        margin: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "data_manager" not in st.session_state:
    st.session_state.data_manager = None

if "query_engine" not in st.session_state:
    st.session_state.query_engine = None

if "auto_loaded" not in st.session_state:
    st.session_state.auto_loaded = False


def load_data_from_config():
    """Auto-load data from config.json on startup."""
    data_file = config.get("data_file", "")
    
    # Resolve relative paths
    if data_file and not os.path.isabs(data_file):
        data_file = os.path.join(os.path.dirname(__file__), data_file)
    
    if data_file and os.path.exists(data_file):
        try:
            dm = DataManager(data_file)
            dm.sites_registry = []
            dm.query_examples = []
            dm.column_metadata = []
            dm.initialize_chroma()
            st.session_state.data_manager = dm
            st.session_state.query_engine = QueryEngine(dm)
            return True, len(dm.df)
        except Exception as e:
            return False, str(e)
    return False, "File not found"


# Auto-load on first run
if not st.session_state.auto_loaded and st.session_state.data_manager is None:
    success, result = load_data_from_config()
    st.session_state.auto_loaded = True
    if success:
        st.toast(f"✅ Loaded {result} samples from config")

# Sidebar
with st.sidebar:
    st.title("💧 Water Quality Chatbot")
    st.markdown("*Free version - runs offline*")
    st.markdown("---")
    
    # File upload
    st.markdown("### 📂 Data Source")
    
    # Get default file from config
    default_file = config.get("data_file", "")
    if default_file and not os.path.isabs(default_file):
        default_file = os.path.join(os.path.dirname(__file__), default_file)
    
    # Show current status
    if st.session_state.data_manager is not None:
        st.success(f"✅ Data loaded: {len(st.session_state.data_manager.df)} samples")
        st.caption(f"📁 `{config.get('data_file', 'N/A')}`")
    elif config.get("data_file"):
        st.warning(f"⚠️ File not found: {config.get('data_file')}")
    else:
        st.info("👆 Upload your Excel or NetCDF file to get started")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload data file",
        type=["xlsx", "xls", "nc"],
        help="Upload Excel (.xlsx) or NetCDF (.nc) water quality data"
    )
    
    # Handle file upload - save to data folder and update config
    if uploaded_file:
        os.makedirs("data", exist_ok=True)
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        save_filename = f"water_data{file_ext}"
        save_path = os.path.join("data", save_filename)
        
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # Update config.json
        config["data_file"] = f"./data/{save_filename}"
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        
        # Load the data
        try:
            dm = DataManager(save_path)
            dm.sites_registry = []
            dm.query_examples = []
            dm.column_metadata = []
            dm.initialize_chroma()
            st.session_state.data_manager = dm
            st.session_state.query_engine = QueryEngine(dm)
            st.success(f"✅ Loaded {len(dm.df)} samples")
            st.rerun()
        except Exception as e:
            st.error(f"Error loading file: {e}")
    
    # Reload button (for when Excel file is updated externally)
    if st.session_state.data_manager is not None:
        if st.button("🔄 Reload Data", help="Reload if Excel file was updated"):
            try:
                data_path = config.get("data_file", "")
                if data_path and not os.path.isabs(data_path):
                    data_path = os.path.join(os.path.dirname(__file__), data_path)
                
                if data_path and os.path.exists(data_path):
                    dm = DataManager(data_path)
                    dm.sites_registry = []
                    dm.query_examples = []
                    dm.column_metadata = []
                    dm.initialize_chroma()
                    st.session_state.data_manager = dm
                    st.session_state.query_engine = QueryEngine(dm)
                    st.success(f"✅ Reloaded {len(dm.df)} samples")
                    st.rerun()
                else:
                    st.error("Data file not found")
            except Exception as e:
                st.error(f"Error loading data: {e}")
    
    st.markdown("---")
    
    # Data overview
    if st.session_state.data_manager is not None:
        dm = st.session_state.data_manager
        summary = dm.get_data_summary()
        
        st.markdown("### 📊 Data Overview")
        st.metric("Total Samples", summary.get('total_samples', 0))
        st.metric("Sites Monitored", summary.get('total_sites', 0))
        st.metric("Parameters", summary.get('columns', 0))
        
        # Show date range
        if 'sample_date' in dm.df.columns:
            st.markdown(f"**Date Range:**")
            st.markdown(f"{dm.df['sample_date'].min().strftime('%Y-%m-%d')} to {dm.df['sample_date'].max().strftime('%Y-%m-%d')}")
    
    st.markdown("---")
    st.markdown("### 💡 Example Questions")
    st.markdown("""
    - Coldest January water temp 1981-1995
    - Average dissolved oxygen by year
    - Show data for site 2
    - Compare summer vs winter temperature
    - How many samples per site?
    - Correlation between temp and oxygen
    - Trend of pH over time
    - Summary statistics for turbidity
    """)
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This chatbot uses **pattern matching** to understand your questions - no AI/API required!
    
    It recognizes:
    - Parameter names (temperature, pH, ecoli, etc.)
    - Time periods (months, years, seasons)
    - Aggregations (average, maximum, minimum)
    - Comparisons and trends
    """)
    
    # NetCDF Export Section
    st.markdown("---")
    st.markdown("### 📦 Export to NetCDF")
    
    if st.session_state.data_manager is not None:
        try:
            from netcdf_exporter import NetCDFExporter, check_netcdf_available
            
            if check_netcdf_available():
                export_title = st.text_input("Dataset Title", value="Water Quality Monitoring Data")
                export_institution = st.text_input("Institution", value="Bard College")
                
                if st.button("📥 Export to NetCDF"):
                    try:
                        exporter = NetCDFExporter(st.session_state.data_manager)
                        output_path = os.path.join("data", "water_quality_data.nc")
                        exporter.export(
                            output_path=output_path,
                            title=export_title,
                            institution=export_institution
                        )
                        st.success(f"✅ Exported to {output_path}")
                        
                        # Show summary
                        summary = exporter.get_export_summary()
                        st.markdown(f"**Exported:** {summary['num_samples']} samples, {summary['num_sites']} sites, {len(summary['variables'])} variables")
                    except Exception as e:
                        st.error(f"Export error: {e}")
            else:
                st.warning("NetCDF4 not installed. Run:\n`python3 -m pip install netCDF4`")
        except ImportError:
            st.warning("NetCDF export module not found.")
    else:
        st.info("Load data first to enable export")

# Main content
st.title("💧 Water Quality Data Assistant")
st.markdown("Ask questions about your water monitoring data in natural language. **Free & offline!**")

# Quick example buttons
if st.session_state.query_engine is not None:
    st.markdown("**Try these examples:**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Yearly temp trend"):
            st.session_state.messages.append({"role": "user", "content": "temperature trend over time"})
            st.rerun()
    with col2:
        if st.button("🦠 Highest E. coli"):
            st.session_state.messages.append({"role": "user", "content": "highest ecoli reading"})
            st.rerun()
    with col3:
        if st.button("🌡️ Summer vs Winter"):
            st.session_state.messages.append({"role": "user", "content": "compare summer vs winter temperature"})
            st.rerun()
    with col4:
        if st.button("📈 Site counts"):
            st.session_state.messages.append({"role": "user", "content": "how many samples per site"})
            st.rerun()

st.markdown("---")

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "data" in message and message["data"] is not None:
            st.dataframe(message["data"], use_container_width=True)

# Chat input
if prompt := st.chat_input("Ask a question about your water data..."):
    # Check if system is ready
    if st.session_state.data_manager is None:
        st.warning("⚠️ Please load data first using the sidebar")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            try:
                response, result_df = st.session_state.query_engine.query(prompt)
                st.markdown(response)
                
                if result_df is not None and len(result_df) > 0:
                    st.dataframe(result_df, use_container_width=True)
                
                # Save to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "data": result_df
                })
            except Exception as e:
                error_msg = f"Error processing query: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "data": None
                })

# Process any pending messages from button clicks
if st.session_state.messages and st.session_state.query_engine:
    last_msg = st.session_state.messages[-1]
    if last_msg["role"] == "user" and len(st.session_state.messages) >= 1:
        # Check if we need to generate a response
        if len(st.session_state.messages) == 1 or st.session_state.messages[-2]["role"] != "user":
            pass  # Response will be generated on next rerun

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col2:
    st.markdown(
        "<p style='text-align: center; color: gray;'>Built for watershed monitoring research • Free & Open Source</p>",
        unsafe_allow_html=True
    )
