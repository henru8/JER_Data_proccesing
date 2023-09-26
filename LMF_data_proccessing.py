import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
#import csv
import numpy as np
plot = 0
# Create the root Tkinter window
root = tk.Tk()

# Hide the root window
root.withdraw()

# Display the directory selection dialog box
file_path = filedialog.askdirectory()

# Change the current working directory to the selected path
os.chdir(file_path)

# current Folder name
folder_name = os.path.basename(file_path)
print("Folder name", folder_name)

# Print the current working directory
print("Current working directory:", file_path)

# Get a list of all files and directories in the current working directory
files = os.listdir(file_path)
print("all files in this directory", files)

# List all '.txt' files in the directory
txt_files = [file for file in files if file.lower().endswith('.txt')]

# Initialize an empty DataFrame
final_df = pd.DataFrame()

# Loop through each .txt file
for txt_file in txt_files:
    # Initialize an empty list to store columns for the DataFrame
    columns = []

    with open(txt_file, 'r') as file:
        print("working on ",txt_file)
        lines = file.readlines()

        # Read the 5th line and split by tabs
        header = lines[4].strip().split('\t')

        # Append the columns to the list
        columns.extend(header)

        # Create an empty list for each column
        column_data = [[] for _ in header]

        # Starting from the 6th line till the end of the file
        for line in lines[5:]:
            # Split each line by tabs
            values = line.strip().split('\t')

            # Ensure that each column has the same length by padding with None if necessary
            for i, value in enumerate(values):
                if i < len(column_data):
                    column_data[i].append(value)
                else:
                    column_data[i].append(None)

        # Pad columns with None if they are shorter than the header
        for i in range(len(column_data), len(header)):
            column_data.append([None] * len(column_data[0]))

    # Ensure that all columns have the same length by padding shorter columns with None
    max_length = max(len(col) for col in column_data)
    for i in range(len(column_data)):
        if len(column_data[i]) < max_length:
            column_data[i].extend([None] * (max_length - len(column_data[i])))

    # Create a DataFrame for this file
    file_df = pd.DataFrame({header[i]: column_data[i] for i in range(len(header))})

    # Append this DataFrame to the final DataFrame
    raw_df = final_df._append(file_df, ignore_index=True)

    # Print out the final DataFrame
    print("Raw ",txt_file," DataFrame:")
    print(raw_df)

    if plot == 1:
        # Get a list of column names excluding 'time'
        columns_to_plot = [col for col in raw_df.columns if col != 'time']

        # Create a single plot for all columns
        plt.figure(figsize=(10, 6))  # You can adjust the figure size as needed
        for column in columns_to_plot:
            plt.plot(raw_df['Time'], raw_df[column], label=column)

        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title(txt_file)
        plt.legend()  # Add a legend to differentiate the columns
        plt.grid(True)  # Add grid lines
        plt.show()
