#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project 3: ANS Evaluation
Authors: Kaelen Kenna & Caitlyn Robinson
BME 3000
MODULE

DESCRIPTION
"""

# Import packages
import numpy as np 
import matplotlib.pyplot as plt

#def plot_raw_data(rest, relax, mental_stress, wall_sit):

#%% Part 2: Filter Your Data
def bandpass_filter(ecg_signal, freq_array, low_cutoff, high_cutoff):

 #
 for signal in ecg_data:
  freq_array = np.fft.rfftfreq(len(signal), 1/fs)

 #
 low_cutoff =
 high_cutoff = 
 filter = np.ones(len(freq_array))
 filter[(f<=low_cutoff) & (f>=high_cutoff)] = 0

# 
ecg_fft = np.fft.fft(ecg_data)
filtered_freq = filter * ecg_fft
filtered_time = np.fft.irfft(filtered_freq)

return filtered_freq, filtered_time
 
#%% Part 3: Detect Heartbeats

#%% Part 4: Calculate Heart Rate Variability

#%% Part 5: Get HRV Frequency Band Power
