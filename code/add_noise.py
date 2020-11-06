#!/usr/bin/env python3
import sys
import random
import csv

rows = list()
# Open the csv file containing the data
with open(sys.argv[1], 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    # Store the csv data in a list
    rows = list(csv_reader)

data = rows[1:]

# Separate the columns
time, ra_data, dec_data = zip(*data)

ra_in_sec = list()

# Parse the right ascension data in seconds
for ra in ra_data:
    hour = int(ra[0:2])
    minute = int(ra[3:5])
    sec = float(ra[6:])
    ra_in_sec.append(hour * 60 * 60 + minute * 60 + sec)

# Estimate the standard deviation for the gaussian noise
average_ra_diff = 0
for i in range(len(ra_in_sec) - 1):
    average_ra_diff += ra_in_sec[i + 1] - ra_in_sec[i]
average_ra_diff /= (len(ra_in_sec) - 1)


sigma_ra = 0.5 * average_ra_diff

# Add gaussian noise with 0 mean and sigma_ra std to the right ascension values
noisy_ra_in_sec = list()
for ra in ra_in_sec:
    noisy_ra = round(ra + random.gauss(0, sigma_ra), 2)
    if noisy_ra < 0:
        noisy_ra_in_sec.append(24 * 60 * 60 + noisy_ra)
    elif noisy_ra >= 24 * 60 * 60:
        noisy_ra_in_sec.append(noisy_ra - 24 * 60 * 60)
    else:
        noisy_ra_in_sec.append(noisy_ra)


dec_in_arcsec = list()
# Parse the declination data in arc seconds
for dec in dec_data:
    positive = dec[0] == '+'
    degree = int(dec[1:3])
    minute = int(dec[4:6])
    sec = float(dec[7:])
    if positive:
        dec_in_arcsec.append(degree * 3600 + minute * 60 + sec)
    else:
        dec_in_arcsec.append(-1 * (degree * 3600 + minute * 60 + sec))

# Estimate the standard deviation for the gaussian noise
average_dec_diff = 0
for i in range(len(dec_in_arcsec) - 1):
    average_dec_diff += dec_in_arcsec[i + 1] - dec_in_arcsec[i]
average_dec_diff /= (len(dec_in_arcsec) - 1)


sigma_dec = 0.5 * average_dec_diff

# Add gaussian noise with 0 mean and sigma_dec std to the declination values
noisy_dec_in_arcsec = list()
for dec in dec_in_arcsec:
    noisy_dec = round(dec + random.gauss(0, sigma_dec), 1)
    noisy_dec_in_arcsec.append(noisy_dec)


csv_list = zip(time, noisy_ra_in_sec, noisy_dec_in_arcsec)


# Set the output csv file name
outputFileName = sys.path[0] + '/' + time[0][0:4] + '.csv'

# Write the output list in csv format to a new csv file
with open(outputFileName, mode='w') as outputFile:
    writer = csv.writer(outputFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Date', 'Right ascension (in seconds)', 'Declination (in arc seconds)'])
    writer.writerows(csv_list)

print('Output file name: ' + outputFileName)