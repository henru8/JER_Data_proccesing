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
    plt.xscale('log')
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
    if "MF" in txt_file:
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
            Fo_df = Fo_df._append(Time_Corrected_dp.iloc[i+1], ignore_index=True)

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

        #step 13, subtract measuring from pre flash
        Subtracted_Flash_dp = Measuring_Flash_df.copy()
        columns_to_exclude = ['Time']  # Add any other columns you want to exclude here

        for column in Subtracted_Flash_dp.columns:
                if column not in columns_to_exclude:
                    Subtracted_Flash_dp[column] = Measuring_Flash_df[column] - Pre_Flash[column]

        #Subtracted_Flash_dp = Measuring_Flash_df-Pre_Flash
        print("Subtracted Flash \n",Subtracted_Flash_dp)

        if plot == 1:
            plot_data(Subtracted_Flash_dp,txt_file)

        #WORKS UP TO HERE

        # Calculate the mean of each column in Fo_df and keep the same column names
        Fo_Mean_df = Fo_df.mean().to_frame().T
        print(Fo_Mean_df)

        Subtracted_Flash_SubFo_df = Subtracted_Flash_dp
        for column in Subtracted_Flash_SubFo_df.columns:
            if column not in columns_to_exclude:
                Subtracted_Flash_SubFo_df[column] = Subtracted_Flash_SubFo_df[column] - Fo_Mean_df[column].values[0]
        print(Subtracted_Flash_SubFo_df)

        Final_df = Subtracted_Flash_SubFo_df.copy()
        # Create a dictionary to store columns and their averages
        averaged_columns = {}
        # Average columns with the same name after removing the last two characters
        for column in Final_df.columns:
            if column not in columns_to_exclude:
                column_name = column[:-2]  # Remove the last two characters
                if column_name not in averaged_columns:
                    averaged_columns[column_name] = []
                averaged_columns[column_name].append(column)

        # Calculate the mean for each set of columns with the same name
        for new_column, old_columns in averaged_columns.items():
            Final_df[new_column] = Subtracted_Flash_SubFo_df[old_columns].mean(axis=1)

        # Remove the original columns except "Time"
        columns_to_remove = [col for col in Subtracted_Flash_SubFo_df.columns if
                             col not in columns_to_exclude and col != "Time"]
        Final_df = Final_df.drop(columns=columns_to_remove)

        print(Final_df)

        if plot == 0:
            plot_data(Final_df,txt_file)

        # Create a directory in the current file_path if it doesn't exist
        file_name = os.path.splitext(os.path.basename(txt_file))[0]
        output_directory = os.path.join(file_path, "Output")
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        Final_df.to_excel((os.path.join(output_directory, file_name + '_Final_df ' +'.xlsx')), index=True)

        # Create a directory in the current file_path if it doesn't exist
        output_directory = os.path.join(file_path, "Proccessing_checks")
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Export the data frames to Excel files
        Final_df.to_excel((os.path.join(output_directory, file_name +'_Final_df ' + '.xlsx')), index=True)
        Subtracted_Flash_SubFo_df.to_excel((os.path.join(output_directory, file_name +'_Subtracted_Flash_SubFo_df ' +'.xlsx')), index=True)
        Fo_df.to_excel((os.path.join(output_directory, file_name +'_Fo_df ' +'.xlsx')), index=True)
        Measuring_Flash_df.to_excel((os.path.join(output_directory, file_name +'_Measuring_Flash_df ' +'.xlsx')), index=True)
        Pre_Flash.to_excel((os.path.join(output_directory, file_name +'_Pre_Flash ' + '.xlsx')),index=True)
