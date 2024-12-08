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
# from project3_module import load_data, separate_datasets

#%% Part 1: Collect & Load Data


# Load the data from the Arduino program
rest_file = '/Users/caitlynrobinson/Desktop/rest.txt'
relax_file = '/Users/caitlynrobinson/Desktop/relax.txt'
mental_stress_file = '/Users/caitlynrobinson/Desktop/mentally_stressful.txt'
physical_stress_file = '/Users/caitlynrobinson/Desktop/physical_stress.txt'
rest = np.loadtxt(rest_file)
relax = np.loadtxt(relax_file)
mental_stress = np.loadtxt(mental_stress_file)
physical_stress = np.loadtxt(physical_stress_file)

# Convert frequency data to seconds so it can be graphed in 5-second intervals
fs = 500 #Hz
dt = 1/fs
rest_time = len(rest)/fs
rest_time = np.arange(0, len(rest)/fs, dt)
relax_time = len(relax)/fs
relax_time = np.arange(0, len(relax)/fs, dt)
mental_stress_time = len(mental_stress)/fs
mental_stress_time = np.arange(0, len(mental_stress)/fs, dt)
physical_stress_time = len(physical_stress)/fs
physical_stress_time = np.arange(0, len(physical_stress)/fs, dt)

# By zooming in/analyzing raw activity plots, x-limits were chosen for each individual subplot to show beats. This allows for more flexibility in the code
xlim_low_rest = 10
xlim_high_rest = 15
xlim_low_relax = 20
xlim_high_relax = 25
xlim_low_mental_stress = 0
xlim_high_mental_stress = 5
xlim_low_physical_stress = 40
xlim_high_physical_stress = 45

# Index each dataset to only get 5 minutes of data for concatenation
duration = fs * 300 #to cut all of the data down to 5 minutes
five_min_rest = rest[:duration]
five_min_relax = relax[:duration]
five_min_mental_stress = mental_stress[:duration]
five_min_physical_stress = physical_stress[:duration]

# Index each time array so x and y have same dimensions for plotting
five_min_rest_time = rest_time[:duration]
five_min_relax_time = relax_time[:duration]
five_min_mental_stress_time = mental_stress_time[:duration]
five_min_physical_stress_time = physical_stress_time[:duration]

# Plot concatenated data
concatenated_datasets = np.concatenate([five_min_rest, five_min_relax, five_min_mental_stress, five_min_physical_stress])
concatenated_time = np.concatenate([five_min_rest_time, five_min_relax_time, five_min_mental_stress_time, five_min_physical_stress_time])
plt.figure(1, clear=True)
plt.plot(concatenated_time, concatenated_datasets)
plt.xlabel('Time (s)')
plt.ylabel('Voltage (mV)')
plt.title('Concatenated Activity Data')
plt.grid(True)
plt.show()

# Call function from module to plot raw data
plot_raw_data(rest_time, rest, xlim_low_rest, xlim_high_rest, relax_time, relax, xlim_low_relax, xlim_high_relax, mental_stress_time, mental_stress, xlim_low_mental_stress, xlim_high_mental_stress, physical_stress_time, physical_stress, xlim_low_physical_stress, xlim_high_physical_stress)

#%% Part 2: Filter Your Data
ecg_data = [rest, relax, mental_stress, physical_stress, concatenated_datasets]

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





