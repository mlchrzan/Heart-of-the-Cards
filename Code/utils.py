import os
import glob
import pandas as pd 

def load_most_recent_pull():
    """
    Load the most recent ygo_daily file from the Auto Pulls folder.
    
    Returns:
        pd.DataFrame: DataFrame containing the most recent ygo_daily data.
    """
    # 1. Load data
    print("Loading most recent ygo_daily file...")

    # Find all ygo_daily files in the Auto Pulls folder
    auto_pulls_dir = "../Data/Auto Pulls/"
    files = glob.glob(os.path.join(auto_pulls_dir, "ygo_daily_*.csv"))

    if not files:
        raise FileNotFoundError("No ygo_daily_*.csv files found in Auto Pulls folder.")

    # Get the most recent file by modification time
    most_recent_file = max(files, key=os.path.getmtime)
    print(f"Loading file: {most_recent_file}")

    docs = pd.read_csv(most_recent_file)

    docs['time_pulled'] = pd.to_datetime(docs['time_pulled'], errors='coerce')

    # If you still want to filter by the most recent date in the file:
    most_recent = docs['time_pulled'].max()
    docs = docs[docs['time_pulled'] == most_recent]

    return docs