#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project 3: ANS Evaluation
Authors: Kaelen Kenna & Caitlyn Robinson
BME 3000
SCRIPT

DESCRIPTION
"""

# Import packages
import numpy as np 
import matplotlib.pyplot as plt
from project3_module import load_data, separate_datasets

#%% Part 1: Collect & Load Data

# Load the data from the Arduino program
input_files = ['/Users/caitlynrobinson/Desktop/rest.txt', '/Users/caitlynrobinson/Desktop/relax.txt', '/Users/caitlynrobinson/Desktop/mentalstress.txt', '/Users/caitlynrobinson/Desktop/wallsit.txt']
contents = load_data(input_files)

# Separate each row in contents to have each dataset as individual variables
datasets = separate_datasets(contents)
rest, relax, mental_stress, wall_sit = datasets

# Make each list into an array
rest = np.array(rest)
relax = np.array(relax)
mental_stress = np.array(mental_stress)
wall_sit = np.array(wall_sit)

# Convert from Arduino freqency to seconds for graphing

# Need to come back and do this, was having issues with frequency conversion
# fs = 16000000 #Hz

# time = len(rest)/fs
# rest_time = np.linspace(0, time, len(rest), endpoint=False)


# #time_rest = np.arange(len(rest)) / fs
# time_relax = np.arange(len(relax)) / fs
# time_mental_stress = np.arange(len(mental_stress)) / fs
# time_wall_sit = np.arange(len(wall_sit)) / fs

# Plot concatenated data
concatenated_datasets = np.concatenate([rest, relax, mental_stress, wall_sit])
plt.figure(1, clear=True)
plt.plot(concatenated_datasets) # time for this?
plt.xlabel('Time (s)')
plt.ylabel('Voltage (mV)')
plt.title('Concatenated Activity Data')
plt.grid(True)
plt.show()

# Plot rest data
plt.figure(2, clear=True)
plt.plot(rest)
plt.xlim(1000, 1005) #only plot 5 sec of data
plt.xlabel('Time (s)')
plt.ylabel('Voltage (mV)')
plt.title('Rest Data')
plt.grid(True)
plt.show()

# Plot relax data
plt.figure(3, clear=True)
plt.plot(relax)
plt.xlim(1000, 1005) #only plot 5 sec of data
plt.xlabel('Time (s)')
plt.ylabel('Voltage (mV)')
plt.title('Relaxed Data')
plt.grid(True)
plt.show()

# Plot mental stress data
plt.figure(4, clear=True)
plt.plot(mental_stress)
plt.xlim(1000, 1005) #only plot 5 sec of data
plt.xlabel('Time (s)')
plt.ylabel('Voltage (mV)')
plt.title('Mental Stress Data')
plt.grid(True)
plt.show()

# Plot wall sit data
plt.figure(5, clear=True)
plt.plot(wall_sit)
plt.xlim(1000, 1005) #only plot 5 sec of data
plt.xlabel('Time (s)')
plt.ylabel('Voltage (mV)')
plt.title('Wall Sit Data')
plt.grid(True)
plt.show()

#%% Part 2: Filter Your Data


# Compare one with before filter on same plot
# Plot rest data with filter

# Plot relaxed data with filter

# Plot mental stress data with filter

# Plot wall sit data with filter

# Plot filter's impulse response

# Plot filter's frequency response


#%% Part 3: Detect Heartbeats

# Detect time of each heartbeat in seconds from start of recording
# (simple thresholding, template matching like proj 2)
# apply to all datasets

# Plot data with heartbeat times


#%% Part 4: Calculate Heart Rate Variability (HRV)

# Calculate inter-beat intervals from detected heartbeats found in Part 2

# Calculate one HRV measure for each activity

# Plot HRVs as a bar plot

# Calculate an interpolated timecourse of IBI at regular intervals of dt = 0.1 seconds

#%% Part 5: Get HRV Frequency Band Power

# Calculate frequency domain magnitude of each activity's IBI timecourse signal

# Plot in power units (not normalize, convert to dB). Zoom in to show LF and HF bands

# Extract mean power in LF and HF frequency bands

# Calculate LF/HF ratio in each activity

# Plot these ratios as a bar plot



































