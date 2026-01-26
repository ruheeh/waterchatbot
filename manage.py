"""
Monthly Data Update Utility
Use this script to add new monthly monitoring data to the system.
"""

import argparse
import pandas as pd
from data_manager import DataManager
from datetime import datetime


def add_monthly_data(data_file: str, month: str = None):
    """
    Add new monthly data from an Excel file.
    
    Args:
        data_file: Path to Excel file with new rows
        month: Month identifier (defaults to current month)
    """
    if month is None:
        month = datetime.now().strftime("%Y-%m")
    
    print(f"Adding data for {month}...")
    
    # Initialize data manager
    dm = DataManager("data/water_data.xlsx")
    dm.initialize_chroma()
    
    # Load new data
    new_data = pd.read_excel(data_file)
    print(f"Loaded {len(new_data)} new rows")
    
    # Show preview
    print("\nPreview of new data:")
    print(new_data[['site', 'basin', 'gpsx', 'gpsy']].head())
    
    # Confirm
    response = input(f"\nAdd these {len(new_data)} rows? (y/n): ")
    if response.lower() == 'y':
        dm.add_monthly_data(new_data, month)
        print("✅ Data added successfully!")
    else:
        print("❌ Cancelled")


def register_site(site_id: str, description: str, basin: str = "", 
                  gpsx: float = 0, gpsy: float = 0, old_site: str = ""):
    """Register a new site in the system."""
    dm = DataManager("data/water_data.xlsx")
    dm.initialize_chroma()
    
    dm.register_new_site(
        site_id=site_id,
        description=description,
        basin=basin,
        gpsx=gpsx,
        gpsy=gpsy,
        old_site=old_site
    )
    print(f"✅ Registered site {site_id}")


def list_sites():
    """List all registered sites."""
    dm = DataManager("data/water_data.xlsx")
    dm.initialize_chroma()
    
    df = dm.get_data()
    print("\nRegistered Sites:")
    print("-" * 60)
    print(df[['site', 'oldsite', 'basin', 'gpsx', 'gpsy']].to_string())


def search_sites(query: str):
    """Search for sites by description."""
    dm = DataManager("data/water_data.xlsx")
    dm.initialize_chroma()
    
    results = dm.search_sites(query)
    
    print(f"\nSearch results for '{query}':")
    print("-" * 60)
    for site in results:
        print(f"Site {site['site_id']} - Basin {site['basin']} ({site['gpsx']}, {site['gpsy']})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Water Data Management Utility")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Add monthly data command
    add_parser = subparsers.add_parser("add", help="Add monthly data")
    add_parser.add_argument("file", help="Excel file with new data")
    add_parser.add_argument("--month", help="Month identifier (YYYY-MM)")
    
    # Register site command
    reg_parser = subparsers.add_parser("register", help="Register a new site")
    reg_parser.add_argument("site_id", help="Site identifier")
    reg_parser.add_argument("description", help="Site description")
    reg_parser.add_argument("--basin", default="", help="Basin identifier")
    reg_parser.add_argument("--gpsx", type=float, default=0, help="GPS X coordinate")
    reg_parser.add_argument("--gpsy", type=float, default=0, help="GPS Y coordinate")
    reg_parser.add_argument("--old-site", default="", help="Previous site ID")
    
    # List sites command
    subparsers.add_parser("list", help="List all sites")
    
    # Search sites command
    search_parser = subparsers.add_parser("search", help="Search sites")
    search_parser.add_argument("query", help="Search query")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_monthly_data(args.file, args.month)
    elif args.command == "register":
        register_site(
            args.site_id, args.description,
            basin=args.basin, gpsx=args.gpsx, gpsy=args.gpsy,
            old_site=args.old_site
        )
    elif args.command == "list":
        list_sites()
    elif args.command == "search":
        search_sites(args.query)
    else:
        parser.print_help()
