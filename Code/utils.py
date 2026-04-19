import os
import glob
import pandas as pd 

FRAME_COLORS = {
    "Spell Card": "#228B22",                    # Forest Green

    # Monster categories grouped by type similarity and common frame colors
    "Normal Monster": "#F5F1DA",                # Beige/cream - Normal monsters
    "Effect Monster": "#D2691E",                # Brown-orange
    "Flip Effect Monster": "#D97A25",           # Slightly lighter brown-orange, related to Effect Monster
    "Union Effect Monster": "#C2691E",          # Related brown-orange shade
    "Pendulum Effect Monster": "#CC7A32",       # Related to Effect Monster, with distinct slightly lighter tone
    "Pendulum Effect Fusion Monster": "#803080", # Purplish, fusion related
    "Pendulum Normal Monster": "#E9DCC9",       # Very light beige, near normal
    "Synchro Monster": "#FFFFFF",                # White
    "Synchro Tuner Monster": "#E6E6E6",          # Near white, related to Synchro Monster
    "Synchro Pendulum Effect Monster": "#F0F0F0", # Slightly off white, pendulum synchro
    "Tuner Monster": "#CCCCCC",                   # Gray, related to Synchro Tuner
    "Normal Tuner Monster": "#DDDDDD",            # Light gray, normal tuner
    "Gemini Monster": "#D0C5A2",                   # Slightly darker beige, related to Normal/Effect
    "Spirit Monster": "#D0B983",                   # Light goldish, related but distinct
    "Ritual Effect Monster": "#4169E1",            # Royal blue, ritual
    "Ritual Monster": "#3A5FCD",                   # Slightly darker blue, related ritual
    "Toon Monster": "#FFB6C1",                      # Light Pink, cartoonish theme

    # Trap Card
    "Trap Card": "#C71585",                      # Medium Violet Red (pinkish purple)

    # Other monster special frames
    "Link Monster": "#1E90FF",                    # Dodger Blue
    "XYZ Monster": "#000000",                     # Black
    "XYZ Pendulum Effect Monster": "#222222",     # Dark gray, similar to XYZ but distinct
    "Pendulum Effect Ritual Monster": "#3C50B4", # Related to Ritual, pendulum effect
    "Pendulum Flip Effect Monster": "#DB8B3A",    # Orangish, related to pendulum effect
    "Flip Tuner Effect Monster": "#B97416",       # Brownish, closer to tuner effect

    # Less common or specialized cards
    "Skill Card": "#6B8E23",                      # Olive green, distinct from spell cards
    "Token": "#808080",                           # Gray
}


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

def last_full_pull(level='printing'):
    """
    Load the most recent full pull file from the Full Pulls folder.
    
    Returns:
        pd.DataFrame: DataFrame containing the most recent full pull data.
    """
    print("Loading most recent full pull file...")

    # Find all full pull files in the Full Pulls folder
    full_pulls_dir = "../Data/Full Pulls/"
    files = glob.glob(os.path.join(full_pulls_dir, "ygo_full_*.csv"))

    if not files:
        raise FileNotFoundError("No ygo_full_*.csv files found in Full Pulls folder.")

    # Get the most recent file by modification time
    most_recent_file = max(files, key=os.path.getmtime)
    print(f"Loading file: {most_recent_file}")

    data = pd.read_csv(most_recent_file)

    if level == 'card':
        # Write code to filter data to the oldest tcg_date for each card_id
        data_all = data.copy()
        data_all['tcg_date_dt'] = pd.to_datetime(data_all['tcg_date'], errors='coerce')
        oldest_dates = data_all.groupby('card_id')['tcg_date_dt'].min().reset_index()
        oldest_dates.columns = ['card_id', 'oldest_tcg_date']
        data_all = data_all.merge(oldest_dates, on='card_id')
        data = data_all[data_all['tcg_date_dt'] == data_all['oldest_tcg_date']]
        data = data.drop(columns=['oldest_tcg_date'])
        # Now for any card_id with multiple entries (e.g. multiple printings on the same day), keep only the first one
        data = data.drop_duplicates(subset=['card_id'], keep='first')
        print(f"Data shape after filtering to oldest tcg_date per card_id: {data.shape}")

    return data