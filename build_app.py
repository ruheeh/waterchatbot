"""
Build Script - Creates distribution folder for team sharing

Usage:
    python3 build_app.py

Output:
    WaterQualityChatbot_Distribution/ folder ready to share
"""

import os
import shutil


def create_distribution():
    """Create a clean distribution folder for sharing with team."""
    
    dist_folder = "WaterQualityChatbot_Distribution"
    
    # Remove if exists
    if os.path.exists(dist_folder):
        shutil.rmtree(dist_folder)
    
    os.makedirs(dist_folder)
    os.makedirs(os.path.join(dist_folder, "data"))
    
    # Files to include
    files_to_copy = [
        "app.py",
        "data_manager.py",
        "query_engine_free.py",
        "netcdf_exporter.py",
        "requirements.txt",
        "run_app.sh",
        "run_app.bat",
    ]
    
    for f in files_to_copy:
        if os.path.exists(f):
            shutil.copy(f, dist_folder)
            print(f"  ✅ Copied {f}")
    
    # Copy README_TEAM.md as README.md
    if os.path.exists("README_TEAM.md"):
        shutil.copy("README_TEAM.md", os.path.join(dist_folder, "README.md"))
        print(f"  ✅ Copied README_TEAM.md → README.md")
    
    # Make shell script executable
    sh_path = os.path.join(dist_folder, "run_app.sh")
    if os.path.exists(sh_path):
        os.chmod(sh_path, 0o755)
    
    # Summary
    print("\n" + "=" * 50)
    print(f"✅ Distribution folder created: {dist_folder}/")
    print("=" * 50)
    print("\nContents:")
    for f in sorted(os.listdir(dist_folder)):
        print(f"  📄 {f}")
    
    print("\n" + "=" * 50)
    print("📦 HOW TO SHARE WITH YOUR TEAM")
    print("=" * 50)
    print(f"""
1. Share the '{dist_folder}' folder via:
   - Google Drive
   - USB drive
   - Email (zip it first)

2. Team members just:
   - Download/copy the folder
   - Double-click run_app.sh (Mac) or run_app.bat (Windows)
   - First run auto-installs everything!
   - First run prompts for Excel file path!

That's it! No manual setup needed.
""")


if __name__ == "__main__":
    print("=" * 50)
    print("💧 Water Quality Chatbot - Build Distribution")
    print("=" * 50)
    print()
    
    create_distribution()
