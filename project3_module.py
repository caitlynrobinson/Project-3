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

#%% Part 1: Collect & Load Data
def plot_raw_data(rest_time, rest, xlim_low_rest, xlim_high_rest, relax_time, relax, xlim_low_relax, xlim_high_relax, mental_stress_time, mental_stress, xlim_low_mental_stress, xlim_high_mental_stress, physical_stress_time, physical_stress, xlim_low_physical_stress, xlim_high_physical_stress):
    """
    This function plots the raw data of each of the 4 collected activities. 

    Parameters
    ----------
    rest_time : array of float (148815,)
       the time in seconds corresponding to each collected rest datapoint.
    rest : array of float (148815,)
        collected rest ECG data from Arduino.
    xlim_low_rest : int
        the lower x-limit for rest data plot, chosen from analyzing the raw plot.
    xlim_high_rest : int
        the upper x-limit for the rest data plot, chosen from analyzing the raw plot.
    relax_time : array of float (152552,)
        the time in seconds corresponding to each collected relax datapoint.
    relax : array of float (152552,)
        collected relax ECG data from Arduino.
    xlim_low_relax : int
        the lower x-limit for relax data plot, chosen from analyzing the raw plot.
    xlim_high_relax : int
        the upper x-limit for the relax data plot, chosen from analyzing the raw plot.
    mental_stress_time : array of float (113492,)
        the time in seconds corresponding to each collected mental stress datapoint.
    mental_stress : array of float (113492,)
        collected mental stress ECG data from Arduino.
    xlim_low_mental_stress : int
        the lower x-limit for mental stress data plot, chosen from analyzing the raw plot.
    xlim_high_mental_stress : int
        the upper x-limit for the mental stress data plot, chosen from analyzing the raw plot.
    physical_stress_time : array of float (153721,)
        the time in seconds corresponding to each collected physical stress datapoint.
    physical_stress : array of float (153721,)
        collected physical stress ECG data from Arduino.
    xlim_low_physical_stress : int
        the lower x-limit for physical stress data plot, chosen from analyzing the raw plot.
    xlim_high_physical_stress : int
        the upper x-limit for the physical stress data plot, chosen from analyzing the raw plot.

    Returns
    -------
    None.

    """
    fig, axes = plt.subplots(2, 2, figsize=(10,6)) #set up full figure
    axes[0,0].plot(rest_time, rest, color='blue') #assign rest subplot
    axes[0, 0].set_title('Rest')
    axes[0, 0].set_xlabel('Time (s)')
    axes[0, 0].set_ylabel('Voltage (mV)')
    axes[0, 0].set_xlim(xlim_low_rest, xlim_high_rest)
    axes[0, 0].grid(True)
    
    axes[0,1].plot(relax_time, relax, color='red') #assign relaxed subplot
    axes[0, 1].set_title('Relaxed')
    axes[0, 1].set_xlabel('Time (s)')
    axes[0, 1].set_ylabel('Voltage (mV)')
    axes[0, 1].set_xlim(xlim_low_relax, xlim_high_relax)
    axes[0, 1].grid(True)
    
    axes[1,0].plot(mental_stress_time, mental_stress, color='orange') #assign third subplot
    axes[1, 0].set_title('Mental Stress')
    axes[1, 0].set_xlabel('Time (s)')
    axes[1, 0].set_ylabel('Voltage (mV)')
    axes[1, 0].set_xlim(xlim_low_mental_stress, xlim_high_mental_stress)
    axes[1, 0].grid(True)
    
    axes[1,1].plot(physical_stress_time, physical_stress, color='green') #assign fourth subplot
    axes[1, 1].set_title('Physical Stress')
    axes[1, 1].set_xlabel('Time (s)')
    axes[1, 1].set_ylabel('Voltage (mV)')
    axes[1, 1].set_xlim(xlim_low_physical_stress, xlim_high_physical_stress)
    axes[1, 1].grid(True)
    
    fig.suptitle('Raw Data Plots') #annotate full figure
    plt.tight_layout()
    plt.show()
 
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
