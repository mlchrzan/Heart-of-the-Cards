import pandas as pd
import os

# Load the most recent combined_data
if os.path.exists("Data/combined_data.csv"):
    combined_data = pd.read_csv("Data/combined_data.csv", na_values="NA")
    print("Combined data loaded successfully.")
else:
    print("No previous combined data found, starting fresh.")
    # Load the first year data
    combined_data = pd.read_csv("Data/first year pulls.csv", na_values="NA")
    print("First year data loaded successfully.")

# Get the most recent date from the combined data
combined_data['date_pulled'] = pd.to_datetime(combined_data['date_pulled'], errors='coerce')
most_recent_date = combined_data['date_pulled'].max()
print(f"Most recent date in combined data: {most_recent_date}")

# DEBUG: Let's see what the last few dates look like
print("DEBUG: Last 10 unique dates in combined_data (sorted):")
unique_dates = sorted(combined_data['date_pulled'].dropna().unique())
print(unique_dates[-10:])

print(f"DEBUG: Total rows in combined_data before processing: {len(combined_data)}")

# Loop through every file in Data/Auto Pulls and combine them
file_names = [f for f in os.listdir("Data/Auto Pulls") if f.endswith(".csv")]
files_processed = 0

for file_name in file_names:
    # Skip files that are older than the most recent date in combined_data
    file_date_str = file_name.split('_')[2]  # [DATE] is the third element
    file_date = pd.to_datetime(file_date_str, errors='coerce')
    if file_date <= most_recent_date:
        print(f"Skipping {file_name} as it is older than the most recent date in combined_data.")
        continue
    
    print(f"Processing file: {file_name}")
    file_path = f"Data/Auto Pulls/{file_name}"
    auto_pull = pd.read_csv(file_path, na_values="NA")
    
    # DEBUG: Check what dates are actually in this file
    auto_pull['date_pulled'] = pd.to_datetime(auto_pull['date_pulled'], errors='coerce')
    file_dates = auto_pull['date_pulled'].dropna().unique()
    print(f"DEBUG: Dates in {file_name}: {sorted(file_dates)}")
    print(f"DEBUG: Rows in {file_name}: {len(auto_pull)}")
    
    # Combine the dataframes
    old_length = len(combined_data)
    combined_data = pd.concat([combined_data, auto_pull], ignore_index=True)
    new_length = len(combined_data)
    print(f"Combined {file_name} into data. Rows added: {new_length - old_length}")
    files_processed += 1

print(f"DEBUG: Total files processed: {files_processed}")
print(f"DEBUG: Total rows in combined_data after processing: {len(combined_data)}")

# DEBUG: Check the final most recent date
final_most_recent = combined_data['date_pulled'].max()
print(f"DEBUG: Final most recent date after all processing: {final_most_recent}")

# Save the combined dataframe to a new CSV file
combined_data.to_csv("Data/combined_data.csv", index=False)
print("Combined data up-to-date saved to Data/combined_data.csv")