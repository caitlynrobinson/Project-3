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
import project3_module as p3m
import project2_module as p2m

#%% Part 1: Collect & Load Data

# Load the data from the Arduino program
rest_file = 'rest.txt'
relax_file = 'relax.txt'
mental_stress_file = 'mentally_stressful.txt'
physical_stress_file = 'physical_stress.txt'
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
xlim_rest = (10, 15)
xlim_relax = (20, 25)
xlim_mental_stress = (0, 5)
xlim_physical_stress = (40,45)

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
p3m.plot_raw_data(rest_time, rest, xlim_rest, relax_time, relax, xlim_relax, mental_stress_time, mental_stress, xlim_mental_stress, physical_stress_time, physical_stress, xlim_physical_stress)

#%% Part 2: Filter Your Data
# Assign variables for cutoffs and sampling frequency
low_cutoff = 5
high_cutoff = 70
fs = 500

# Call the function to apply bandpass filter to datasets
filtered_rest, filtered_relax, filtered_mental, filtered_physical, freq_response, impulse_response, x_axis = p3m.bandpass_filter(fs, rest, relax, mental_stress, physical_stress, low_cutoff, high_cutoff)

# Plot data with filter and compare one activity with raw data
plt.figure(figsize=(12, 10))

# Subplot 1: Filtered Rest
time_rest = np.arange(0, len(filtered_rest)/fs, 1/fs)
plt.subplot(2, 2, 1)
plt.plot(time_rest, filtered_rest)
plt.title('Filtered Rest')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (mV)')
plt.xlim(10,15)
plt.grid(True)

# Subplot 2: Filtered and Raw Relax
time_relax = np.arange(0, len(filtered_relax)/fs, 1/fs)
plt.subplot(2, 2, 2)
plt.plot(time_relax, filtered_relax, label='Filtered Relax', color='green')
plt.plot(time_relax, relax, label='Raw Relax', color='red', alpha=0.5)
plt.title('Filtered and Raw Relax')  #compare raw and filtered data for relax dataset
plt.xlabel('Time (s)')
plt.ylabel('Voltage (mV)')
plt.xlim(20,25)
plt.legend()
plt.grid(True)

# Subplot 3: Filtered Mental Stress
time_mental = np.arange(0, len(filtered_mental)/fs, 1/fs)
plt.subplot(2, 2, 3)
plt.plot(time_mental, filtered_mental)
plt.title('Filtered Mental Stress')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (mV)')
plt.xlim(0,5)
plt.grid(True)

# Subplot 4: Filtered Physical Stress
time_physical = np.arange(0, len(filtered_physical)/fs, 1/fs)
plt.subplot(2, 2, 4)
plt.plot(time_physical, filtered_physical)
plt.title('Filtered Physical Stress')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (mV)')
plt.xlim(40,45)
plt.grid(True)

plt.tight_layout()
plt.show()

# Create time array with dimensions for impulse response
impulse_time_array = np.arange(0, len(impulse_response)/fs, 1/fs)

# Plot filter's impulse response
plt.figure(4, clear=True)
plt.plot(impulse_time_array, impulse_response)
plt.title('Impulse Response')
plt.xlabel('Time (s)')
plt.ylabel('Gain')
plt.grid(True)

# Plot filter's frequency response
plt.figure(5, clear=True)
plt.plot(x_axis, freq_response)
plt.title('Frequency Response')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.grid(True)


#%% Part 3: Detect Heartbeats

# Use Project 2 Module to create a template for matching
template = p3m.load_file('rest.txt')
template = p2m.normalize_template(template)

# Use Project 2 Module template-matching to detect rest beats
template_match_rest = p2m.get_template_match(filtered_rest, template)
beat_samples_rest = p2m.predict_beat_times(template_match_rest, threshold = 0.28)
beat_times_rest = beat_samples_rest / fs
filtered_rest_beat = filtered_rest[beat_samples_rest]

# Plot rest data with heartbeat times
plt.figure(6, clear=True)
plt.plot(time_rest, filtered_rest)
plt.plot(beat_times_rest, filtered_rest_beat, '.')
plt.title('Rest data (mV) with heartbeats identified vs. time (s)')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (mV)')
plt.xlim(145,150)
plt.grid(True)

# Use Project 2 Module template-matching to detect relax beats
template_match_relax = p2m.get_template_match(filtered_relax, template)
beat_samples_relax = p2m.predict_beat_times(template_match_relax, threshold = 0.28)
beat_times_relax = beat_samples_relax / fs
filtered_relax_beat = filtered_relax[beat_samples_relax]

# Plot relax data with heartbeat times
plt.figure(7, clear=True)
plt.plot(time_relax, filtered_relax)
plt.plot(beat_times_relax, filtered_relax_beat, '.')
plt.title('Relax data (mV) with heartbeats identified vs. time (s)')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (mV)')
plt.xlim(145,150)
plt.grid(True)

# Use Project 2 Module template-matching to detect mental stress beats
template_match_mental = p2m.get_template_match(filtered_mental, template)
beat_samples_mental = p2m.predict_beat_times(template_match_mental, threshold = 0.55)
beat_times_mental = beat_samples_mental / fs
filtered_mental_beat = filtered_mental[beat_samples_mental]

# Plot mental stress data with heartbeat times
plt.figure(8, clear=True)
plt.plot(time_mental, filtered_mental)
plt.plot(beat_times_mental, filtered_mental_beat, '.')
plt.title('Mental stress data (mV) with heartbeats identified vs. time (s)')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (mV)')
plt.xlim(145, 150)
plt.grid(True)

# Use Project 2 Module template-matching to detect physical stress beats
template_match_physical = p2m.get_template_match(filtered_physical, template)
beat_samples_physical = p2m.predict_beat_times(template_match_physical, threshold = 0.5)
beat_times_physical = beat_samples_physical / fs
filtered_physical_beat = filtered_physical[beat_samples_physical]

# Plot physical stress data with heartbeat times
plt.figure(9, clear=True)
plt.plot(time_physical, filtered_physical)
plt.plot(beat_times_physical, filtered_physical_beat, '.')
plt.title('Physical stress data (mV) with heartbeats identified vs. time (s)')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (mV)')
plt.xlim(145,150)
plt.grid(True)

#%% Part 4: Calculate Heart Rate Variability (HRV)

# Calculate inter-beat intervals and HRV for rest data
ibi_rest_data = np.diff(beat_times_rest)
hrv_rest = p3m.calculate_hrv(ibi_rest_data)

# Calculate inter-beat intervals and HRV for relax data
ibi_relax_data = np.diff(beat_times_relax)
hrv_relax = p3m.calculate_hrv(ibi_relax_data)

# Calculate inter-beat intervals and HRV for mental stress data
ibi_mental_data = np.diff(beat_times_mental)
hrv_mental = p3m.calculate_hrv(ibi_mental_data)

# Calculate inter-beat intervals and HRV for physical stress data
ibi_physical_data = np.diff(beat_times_physical)
hrv_physical = p3m.calculate_hrv(ibi_physical_data)

# Declare bar plot values and labels
hrv_values = [hrv_rest, hrv_relax, hrv_mental, hrv_physical]
hrv_labels = ["Rest", "Relax", "Mental Stress", "Physical Stress"]

# Plot HRVs as a bar plot
plt.figure(10, clear=True)
plt.bar(hrv_labels, hrv_values, color = ['blue', 'yellow', 'green', 'orange'])
plt.title('HRV (ms) as a function of activity type')
plt.xlabel('Activity type')
plt.ylabel('HRV (ms)')
plt.grid(True)

# Calculate an interpolated timecourse of each IBI datasetat regular intervals of dt = 0.1 seconds
dt= 0.1
interpolated_rest_data = p3m.interpolate_data(beat_times_rest, ibi_rest_data, dt)
interpolated_relax_data = p3m.interpolate_data(beat_times_relax, ibi_relax_data, dt)
interpolated_mental_data = p3m.interpolate_data(beat_times_mental, ibi_mental_data, dt)
interpolated_physical_data = p3m.interpolate_data(beat_times_physical, ibi_physical_data, dt)


#%% Part 5: Get HRV Frequency Band Power

# Calculate frequency domain magnitude and power of each activity's IBI timecourse signal
dt = 0.1
rest_freq_power, rest_freq_domain = p3m.get_freq_power(interpolated_rest_data, dt)
relax_freq_power, relax_freq_domain = p3m.get_freq_power(interpolated_relax_data, dt)
mental_freq_power, mental_freq_domain = p3m.get_freq_power(interpolated_mental_data, dt)
physical_freq_power, physical_freq_domain = p3m.get_freq_power(interpolated_physical_data, dt)

# plot lf/hf bands in frequency vs. power of rest IBI
plt.figure(11, clear=True)
plt.plot(rest_freq_domain, rest_freq_power)
plt.title('Frequency (Hz) vs. Power (s^2) of Rest IBI')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power (s^2)')
# fill in low frequency/parasympathetic section of graph
x_low_rest = rest_freq_domain[(rest_freq_domain > 0.04) & (rest_freq_domain < 0.15)]
y_low_rest = rest_freq_power[(rest_freq_domain > 0.04) & (rest_freq_domain < 0.15)]
plt.fill_between(x_low_rest, y_low_rest, 0, color='b')
# fill in high frequency/sympathetic section of graph
x_high_rest = rest_freq_domain[(rest_freq_domain > 0.15) & (rest_freq_domain < 0.4)]
y_high_rest = rest_freq_power[(rest_freq_domain > 0.15) & (rest_freq_domain < 0.4)]
plt.fill_between(x_high_rest, y_high_rest, 0, color='r')
plt.xlim(0.04,0.4)

# plot lf/hf bands in frequency vs. power of relaxed IBI
plt.figure(12, clear=True)
plt.plot(relax_freq_domain, relax_freq_power)
plt.title('Frequency (Hz) vs. Power (s^2) of Relax IBI')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power (s^2)')
# fill in low frequency/parasympathetic section of graph
x_low_relax = relax_freq_domain[(relax_freq_domain > 0.04) & (relax_freq_domain < 0.15)]
y_low_relax = relax_freq_power[(relax_freq_domain > 0.04) & (relax_freq_domain < 0.15)]
plt.fill_between(x_low_relax, y_low_relax, 0, color='b')
# fill in high frequency/sympathetic section of graph
x_high_relax = relax_freq_domain[(relax_freq_domain > 0.15) & (relax_freq_domain < 0.4)]
y_high_relax = relax_freq_power[(relax_freq_domain > 0.15) & (relax_freq_domain < 0.4)]
plt.fill_between(x_high_relax, y_high_relax, 0, color='r')
plt.xlim(0.04,0.4)

# plot lf/hf bands in frequency vs. power of mental stress IBI
plt.figure(13, clear=True)
plt.plot(mental_freq_domain, mental_freq_power)
plt.title('Frequency (Hz) vs. Power (s^2) of Mental IBI')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power (s^2)')
# fill in low frequency/parasympathetic section of graph
x_low_mental = mental_freq_domain[(mental_freq_domain > 0.04) & (mental_freq_domain < 0.15)]
y_low_mental = mental_freq_power[(mental_freq_domain > 0.04) & (mental_freq_domain < 0.15)]
plt.fill_between(x_low_mental, y_low_mental, 0, color='b')
# fill in high frequency/sympathetic section of graph
x_high_mental = mental_freq_domain[(mental_freq_domain > 0.15) & (mental_freq_domain < 0.4)]
y_high_mental = mental_freq_power[(mental_freq_domain > 0.15) & (mental_freq_domain < 0.4)]
plt.fill_between(x_high_mental, y_high_mental, 0, color='r')
plt.xlim(0.04,0.4)

# plot lf/hf bands in frequency vs. power of physical stress IBI
plt.figure(14, clear=True)
plt.plot(physical_freq_domain, physical_freq_power)
plt.title('Frequency (Hz) vs. Power (s^2) of Physical IBI')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power (s^2)')
# fill in low frequency/parasympathetic section of graph
x_low_physical = physical_freq_domain[(physical_freq_domain > 0.04) & (physical_freq_domain < 0.15)]
y_low_physical = physical_freq_power[(physical_freq_domain > 0.04) & (physical_freq_domain < 0.15)]
plt.fill_between(x_low_physical, y_low_physical, 0, color='b')
# fill in high frequency/sympathetic section of graph
x_high_physical = physical_freq_domain[(physical_freq_domain > 0.15) & (physical_freq_domain < 0.4)]
y_high_physical = physical_freq_power[(physical_freq_domain > 0.15) & (physical_freq_domain < 0.4)]
plt.fill_between(x_high_physical, y_high_physical, 0, color='r')
plt.xlim(0.04,0.4)

# calculate power ratios of LF/HF
rest_power_ratio = p3m.get_power_ratio(rest_freq_domain, rest_freq_power)
relax_power_ratio = p3m.get_power_ratio(relax_freq_domain, relax_freq_power)
mental_power_ratio = p3m.get_power_ratio(mental_freq_power, mental_freq_power)
physical_power_ratio = p3m.get_power_ratio(physical_freq_domain, physical_freq_power)

# make bar plot of power ratios
ratio_labels = ['Rest', 'Relax', 'Mental Stress', 'Physical Stress']
ratio_values = [rest_power_ratio, relax_power_ratio, mental_power_ratio, physical_power_ratio]

plt.figure(15, clear=True)
plt.bar(ratio_labels, ratio_values, color = ['blue', 'yellow', 'green', 'orange'])
plt.title('Power ratios as a function of activity type')
plt.xlabel('Activity type')
plt.ylabel('Power ratio')
plt.grid(True)

