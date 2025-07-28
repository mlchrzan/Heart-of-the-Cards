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
combined_data['date_pulled'] = pd.to_datetime(combined_data['date_pulled'], errors='coerce') # Make sure 'date' column is in datetime format
most_recent_date = combined_data['date_pulled'].max()
print(f"Most recent date in combined data: {most_recent_date}")

# Loop through every file in Data/Auto Pulls and combine them
file_names = [f for f in os.listdir("Data/Auto Pulls") if f.endswith(".csv")]
for file_name in file_names:
    
    # Skip files that are older than the most recent date in combined_data
    file_date_str = file_name.split('_')[2]  # [DATE] is the third element
    file_date = pd.to_datetime(file_date_str, errors='coerce')
    if file_date < most_recent_date:
        print(f"Skipping {file_name} as it is older than the most recent date in combined_data.")
        continue

    print(f"Processing file: {file_name}")
    file_path = f"Data/Auto Pulls/{file_name}"
    auto_pull = pd.read_csv(file_path, na_values="NA")

    # Combine the dataframes
    combined_data = pd.concat([combined_data, auto_pull], ignore_index=True)
    print(f"Combined {file_name} into data.")

# Save the combined dataframe to a new CSV file
combined_data.to_csv("Data/combined_data.csv", index=False)
print("Combined data up-to-date saved to Data/combined_data.csv")

# def combine():
# if __name__ == "__main__":
#    combine()