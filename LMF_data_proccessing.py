import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
#import csv
import numpy as np
plot = 0

def plot_data(plot_df, txt_file):
    # Get a list of column names excluding 'Time'
    columns_to_plot = [col for col in plot_df.columns if col != 'Time']

    # Create a single plot for all columns
    plt.figure(figsize=(10, 6))  # You can adjust the figure size as needed
    for column in columns_to_plot:
        plt.plot(plot_df['Time'], plot_df[column], label=column)

    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title(txt_file)
    plt.legend()  # Add a legend to differentiate the columns
    plt.grid(True)  # Add grid lines
    plt.show()


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
        plot_data(raw_df,txt_file)

    # Create a new dataframe F0
    Fo_df = pd.DataFrame()
    Measuring_Flash_df = pd.DataFrame()
    Pre_Flash = pd.DataFrame()

    Time_Corrected_dp = raw_df.apply(pd.to_numeric, errors='coerce')
    Time_Corrected_dp['Time'] = Time_Corrected_dp['Time'] - 0.001
    #print(Time_Corrected_dp)

    # Iterate through every second row in raw_df and add it to Fo_df
    for i in range(0, 8, 2):
        Fo_df = Fo_df._append(raw_df.iloc[i+1], ignore_index=True)

    # Display the resulting F0 dataframe
    print("F0 DataFrame:")
    #print(Fo_df)

    # Iterate through every second row from the 8th onwards in time_corrected and add it to Pre_Flash
    for i in range(8, len(Time_Corrected_dp["Time"]), 2):
        Pre_Flash = Pre_Flash._append(Time_Corrected_dp.iloc[i], ignore_index=True)

    # Display the resulting Pre_Flash dataframe
    #print("Pre_Flash DataFrame:")

    # Iterate through every second row from the 9th row onwards in time_corrected and add it to Measuring_Flash_df
    for i in range(9, len(Time_Corrected_dp["Time"]), 2):
        Measuring_Flash_df = Measuring_Flash_df._append(Time_Corrected_dp.iloc[i], ignore_index=True)

    # Display the resulting Pre_Flash dataframe
    print("Measuring_Flash_df DataFrame:")


    #populate




    if plot == 1:
        plot_data(Fo_df,txt_file)

