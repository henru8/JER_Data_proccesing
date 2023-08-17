import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os

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

# Export the aggregated data to an Excel file in the same directory
output_file = os.path.join(folder_path, f"O2_aggregated_data_{folder_name}.xlsx")
aggregated_data.to_excel(output_file, engine="openpyxl", index=False)
print(f"Aggregated data exported to {output_file}.")
