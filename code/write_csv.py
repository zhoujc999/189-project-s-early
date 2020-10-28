#!/usr/bin/env python3
import csv
import datetime
import sys

# Open the text file containing the data
with open(sys.argv[1], 'r') as inputFile:
    # Read the file line by line
    lines = inputFile.readlines()

# Set the start date and time
time = datetime.datetime.strptime(lines[0][1:18], '%Y-%b-%d %H:%M')
# Account for the time difference
time = time.replace(hour=7)
# Set the time increment to be 12 hours
timeDelta = datetime.timedelta(hours=12)
# Create output list
resList = list()

for line in lines:
    # Create a new list for every line
    temp = list()
    # Append the date and time to the list
    temp.append(str(time))
    # Append the right ascension of Venus
    temp.append(line[23:34])
    # Append the declination of Venus
    temp.append(line[35:46])
    # Append the list to the output list
    resList.append(temp)
    # Increment the time
    time = time + timeDelta

# Set the output csv file name
outputFileName = sys.path[0] + '/' + lines[0][1:5] + '.csv'

# Write the output list in csv format to a new file
with open(outputFileName, mode='w') as outputFile:
    writer = csv.writer(outputFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Date', 'Right ascension', 'Declination'])
    writer.writerows(resList[:-1])

print('Output file name: ' + outputFileName)

