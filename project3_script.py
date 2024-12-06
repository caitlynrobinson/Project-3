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

# Make a time array so the data can be graphed in a 5 second interval
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

# Index to only get duration for concatenation
duration = fs * 300 #to cut all of the data down to 5 minutes
# five_min_rest = rest[:duration]
# five_min_relax = relax[:duration]
# five_min

# Plot concatenated data
# concatenated_datasets = np.concatenate([rest, relax, mental_stress, wall_sit])
# plt.figure(1, clear=True)
# #plt.plot(relax_time, concatenated_datasets) # using relaxed time for this time because it has the shortest length
# plt.xlabel('Time (s)')
# plt.ylabel('Voltage (mV)')
# plt.title('Concatenated Activity Data')
# plt.grid(True)
# plt.show()

# Plot rest data
plt.figure(2, clear=True)
plt.plot(rest_time, rest)
plt.xlim(0,5)
plt.xlabel('Time (s)')
plt.ylabel('Voltage (mV)')
plt.title('Rest Data')
plt.grid(True)
plt.show()

# Plot relax data
plt.figure(3, clear=True)
plt.plot(relax_time, relax)
plt.xlim(0,5)
plt.xlabel('Time (s)')
plt.ylabel('Voltage (mV)')
plt.title('Relaxed Data')
plt.grid(True)
plt.show()

# Plot mental stress data
plt.figure(4, clear=True)
plt.plot(mental_stress_time, mental_stress)
plt.xlim(0,5)
plt.xlabel('Time (s)')
plt.ylabel('Voltage (mV)')
plt.title('Mental Stress Data')
plt.grid(True)
plt.show()

# Plot physical stress data
plt.figure(5, clear=True)
plt.plot(physical_stress_time, physical_stress)
plt.xlim(100,105)
plt.xlabel('Time (s)')
plt.ylabel('Voltage (mV)')
plt.title('Physical Stress Data')
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





