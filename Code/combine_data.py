import pandas as pd
import os

def combine():
    # Load the first year data
    first_year = pd.read_csv("Data/first year pulls.csv", na_values="NA")
    print("First year data loaded successfully.")

    # Loop through every file in Data/Auto Pulls and combine them
    file_names = [f for f in os.listdir("Data/Auto Pulls") if f.endswith(".csv")]
    for file_name in file_names:
        print(f"Processing file: {file_name}")
        file_path = f"Data/Auto Pulls/{file_name}"
        auto_pull = pd.read_csv(file_path, na_values="NA")

        # Combine the dataframes
        first_year = pd.concat([first_year, auto_pull], ignore_index=True)
        print(f"Combined {file_name} into data.")

    # Save the combined dataframe to a new CSV file
    first_year.to_csv("Data/combined_data.csv", index=False)

if __name__ == "__main__":
    combine()