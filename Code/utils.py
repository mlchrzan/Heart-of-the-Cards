import os
import glob
import pandas as pd 

# List of every banlist date
banlist_dates_tcg = ["2002-05-01", "2002-07-01", "2002-10-01", "2002-12-01", "2003-04-01",
                     "2003-05-08", "2003-07-08", "2003-08-25", "2003-11-17", "2004-04-19",
                     "2004-08-25", "2004-10-01", "2005-04-01", "2005-10-01", "2006-04-01", 
                     "2006-09-01", "2007-03-01", "2007-06-01", "2007-09-01", "2008-03-01",
                     "2008-05-09", "2008-09-01", "2009-03-01", "2009-09-01", "2010-03-01",
                     "2010-09-01", "2011-03-01", "2011-09-01", "2012-03-01", "2012-09-01",
                     "2013-03-01", "2013-09-01", "2013-11-11", "2014-01-01", "2014-04-01",
                     "2014-07-14", "2014-10-01", "2015-01-01", "2015-04-01", "2015-07-16",
                     "2015-11-09", "2016-04-11", "2016-08-29", "2017-03-31", "2017-06-12",
                     "2017-09-18", "2017-11-06", "2018-02-05", "2018-05-21", "2018-09-17",
                     "2018-12-03", "2019-01-28", "2019-04-29", "2019-07-15", "2019-10-14",
                     "2020-01-20", "2020-04-01", "2020-06-15", "2020-09-11", "2020-12-10",
                     "2021-03-15", "2021-07-01", "2021-10-01", "2022-02-07", "2022-05-23",
                     "2022-10-03", "2022-12-01", "2023-02-13", "2022-06-05", "2023-09-25",
                     "2024-01-01", "2024-04-22", "2024-09-02", "2024-12-06", "2025-04-07"]

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