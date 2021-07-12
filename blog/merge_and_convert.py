'''
Adam Huybers
Written for: PolySense Solutions Inc.
Project Number: SH21001
Customer: Orthopaedic Innovation Centre
Created: 2021-06-09
Updated: 2021-06-20
 
Project TODO - Merge four .txt, then convert .txt to .csv


WIP NOTES:  -Delete original .txt files?
            -Requires pandas library to be installed.
            -Improve list checker.


 
@author Adam Huybers [ahuybers@polysensesolutions.com]
@version 1.3
'''

import pandas
import os
import glob

def convert():

    # Collects the files names of all .txt files in a given directory.
    file_names = glob.glob("media/*.txt")       #File path to directory here.

    # Checks if list is empty.
    if not file_names:
        print("empty")

    else: # Merges the text files into a single file titled 'output_file'. Name shouldn't matter as it is a temporary file.
        with open('output_file.txt', 'w') as outfile:
            for i in file_names:
                with open(i) as infile:
                    for j in infile:
                        outfile.write(j)

        # Reading the merged file and creating dataframe.
        data = pandas.read_csv("output_file.txt",
                            delimiter = '/')     #Column delimiter here.
        
        # Store dataframe into csv file.
        data.to_csv("media/convert_sample.csv",       #Rename output .csv file here.
                    index = None)

        # Removes the merged .txt file.
        if os.path.exists("output_file.txt"):
            os.remove("output_file.txt")

        # Removes the orignal .txt files
        for i in file_names:
            os.remove(i)