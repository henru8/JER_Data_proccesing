import csv
import numpy as np
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
file_path = filedialog.askdirectory()

# Change the current working directory to the selected path
os.chdir(file_path)

# Get the updated current working directory
path = os.getcwd()

# current Folder name
folder_name = os.path.basename(file_path)
print("Folder name",folder_name)

# Print the current working directory
print("Current working directory:", path)
# Get a list of all files and directories in the current working directory
files = os.listdir(path)
print("all files in this directory", files)

# Create empty data frames to store the data
df_440 = pd.DataFrame()
df_580 = pd.DataFrame()

# Loop over each file in the directory
for file in files:
    # Check if the file is a CSV file
    if file.endswith('.CSV'):
        # Open the CSV file
        with open(file, 'r') as f:
            # Create a CSV reader object
            csv_reader = csv.reader(f)

            # Initialize an empty nested list
            nested_list = []

            # Loop over each row in the CSV file
            for row in csv_reader:
                # Initialize an empty list for the row
                row_list = []
                # Loop over each element in the row and append it to the row list
                for element in row:
                    row_list.append(float(element))
                # Append the row list to the nested list
                nested_list.append(row_list)

            # Convert the nested list to a numpy array with four dimensions
        input1 = np.array(nested_list).reshape(-1, 4)

        # find the index for the first value of 630 and the first value of 780 in the input array
        indexfor630 = np.where(input1[:, 0] == 630)[0]
        indexfor780 = np.where(input1[:, 0] == 780)[0]

        # check if index arrays are empty
        if indexfor630.size == 0 or indexfor780.size == 0:
            print("Error: Could not find indices for",file)
        else:
            # select rows 630 till 780 (inclusive) using array slicing
            new_array = input1[indexfor630[0]:indexfor780[0] + 1, :]
            # Remove the first, second, and fourth columns
            new_array = np.delete(new_array, [0, 1, 3], axis=1)



        # Convert the NumPy array to a pandas DataFrame
        df = pd.DataFrame(new_array)

        # Set the file name as the column name of the data frame
        file_name = file[:-6]  # Remove the .CSV extension from the file name
        df.columns = [file_name] * len(df.columns)

        # Append the data frame to the appropriate data frame based on the file name
        if '440' in file_name:
            df_440 = pd.concat([df_440, df], axis=1)
        else:
            df_580 = pd.concat([df_580, df], axis=1)

# group columns with the same name and average them
df_440 = df_440.groupby(df_440.columns, axis=1).mean()
df_580 = df_580.groupby(df_580.columns, axis=1).mean()

# plot the dataframe as a line graph
plt.plot(df_440)
plt.legend(df_440.columns)
plt.show()


i_col = 0
# zero the measurments and normlise to peak at 95
for columns in df_440:
    first_num = df_440.iloc[0, i_col]
    last_num = df_440.iloc[150, i_col]
    difer = first_num - last_num

    i_rows = 0
    while i_rows < 151:
        #(df_440.iloc[i_rows, i_col]-last_num)
        decay_curve = difer - ((difer/150)*(1+i_rows))
        df_440.iloc[i_rows, i_col] = (df_440.iloc[i_rows, i_col]-last_num)-decay_curve
        i_rows += 1

    #normlise to peak at 95
    peak_at_725 = df_440.iloc[95, i_col]
    i_rows = 0
    while i_rows < 151:
        df_440.iloc[i_rows, i_col] = (df_440.iloc[i_rows, i_col])/peak_at_725
        i_rows = i_rows + 1

    i_col = i_col + 1



# zero the measurments for 580 and normlise to peak at 95
i_col = 0
for columns in df_580:
    first_num = df_580.iloc[0, i_col]
    last_num = df_580.iloc[150, i_col]
    difer = first_num - last_num

    i_rows = 0
    while i_rows < 151:
        decay_curve = difer - ((difer/150)*(1+i_rows))
        df_580.iloc[i_rows, i_col] = (df_580.iloc[i_rows, i_col]-last_num)-decay_curve
        i_rows += 1

    #normilise to peak at 725
    peak_at_725 = df_580.iloc[95, i_col]
    i_rows = 0
    while i_rows < 151:
        df_580.iloc[i_rows, i_col] = (df_580.iloc[i_rows, i_col])/peak_at_725
        i_rows = i_rows + 1

    i_col = i_col + 1


# plot the dataframe as a line graph
plt.plot(df_440)
plt.legend(df_440.columns)
plt.show()


# plot the dataframe as a line graph
plt.plot(df_580)
plt.legend(df_580.columns)
plt.show()


### appends wavelnghts onto excel spread for 'human' legiability
    # create a new column with the list of values
new_col = np.array([])
for i in range (630,781):
    new_col = np.append(new_col,i)

df_440['Wave Lenghts']= new_col
df_580['Wave Lenghts']= new_col


# Export the data frames to Excel files
df_440.to_excel('dataExport_440 '+folder_name+'.xlsx', index=True)
df_580.to_excel('dataExport_580 '+folder_name+'.xlsx', index=True)
