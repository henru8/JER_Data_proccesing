import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os
import numpy as np

def normalize_columns(df):
    # Ask for the value of Satt and De_Satt
    Satt = float(input("Enter the value of Satt: "))
    De_Satt = float(input("Enter the value of De_Satt: "))

    # Normalize each column of the DataFrame
    normalized_df = pd.DataFrame()

    for column in df.columns:
        current_column = df[column]
        #asks for the chlorphyl-a conc for each column
        print("please enter Chlorphyl-a conc for ", column)
        chl_a_conc = float(input("Enter the value for chl_a_conc: "))
        normalized_column = (1000 * 0.235 * ((current_column - De_Satt) / (Satt - De_Satt)) / chl_a_conc)
        t_start = normalized_column[60]
        normalized_column = normalized_column - t_start
        normalized_df[column] = normalized_column

    return normalized_df

# Create the root Tkinter window
root = tk.Tk()

# Hide the root window
root.withdraw()

# Display the directory selection dialog box
folder_path = filedialog.askdirectory(title="Select Folder")

# Get the name of the folder
folder_name = os.path.basename(folder_path)

# Create an empty DataFrame to store the aggregated data
aggregated_data = pd.DataFrame()

# Iterate over all files in the selected folder
for file_name in os.listdir(folder_path):
    # Construct the file path
    file_path = os.path.join(folder_path, file_name)

    # Read the CSV file
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading file '{file_name}': {e}")
        continue

    # Check if the file has at least 300 rows
    if len(df) < 300:
        print(f"Skipping file '{file_name}': Insufficient data rows.")
        continue

    # Extract the last 300 rows from the DataFrame
    column_name = os.path.splitext(file_name)[0]  # Extract the name of the CSV file
    data = df.iloc[-300:]

    # Add the data to the aggregated DataFrame with the column name
    aggregated_data[column_name] = data.iloc[:, 1].reset_index(drop=True)

# Average columns with the same name after removing the last two characters
aggregated_data.columns = aggregated_data.columns.str[:-2]
aggregated_data = aggregated_data.groupby(aggregated_data.columns, axis=1).mean()

# Plot all the data
aggregated_data.plot()
plt.legend(aggregated_data.columns)
plt.show()

# Normalize the columns of the aggregated data
normalized_df = normalize_columns(aggregated_data)
normalized_df = pd.DataFrame(normalized_df, columns=aggregated_data.columns)

# Plot the normalized data
normalized_df.plot()
plt.legend(normalized_df.columns)
plt.show()

# Export the normalized data to an Excel file
output_file = os.path.join(folder_path, f"O2_normalized_data_{folder_name}.xlsx")
normalized_df.to_excel(output_file, engine="openpyxl", index=False)
print(f"Normalized data exported to {output_file}.")
