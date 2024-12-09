#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project 3: ANS Evaluation
Authors: Kaelen Kenna & Caitlyn Robinson
BME 3000
MODULE

DESCRIPTION
"""


#%% Part 1: Collect & Load Data
# Import packages
import numpy as np 
import matplotlib.pyplot as plt

def plot_raw_data(rest_time, rest, xlim_rest, relax_time, relax, xlim_relax, mental_stress_time, mental_stress, xlim_mental_stress, physical_stress_time, physical_stress, xlim_physical_stress):
    """
    This function plots the raw data of each of the 4 collected activities. 

    Parameters
    ----------
    rest_time : array of float (148815,)
       the time in seconds corresponding to each collected rest datapoint.
    rest : array of float (148815,)
        collected rest ECG data from Arduino.
    xlim_rest : tuple
        the x-limits for rest data plot, chosen from analyzing the raw plot.
    relax_time : array of float (152552,)
        the time in seconds corresponding to each collected relax datapoint.
    relax : array of float (152552,)
        collected relax ECG data from Arduino.
    xlim_relax : tuple
        the x-limits for relax data plot, chosen from analyzing the raw plot.
    mental_stress_time : array of float (113492,)
        the time in seconds corresponding to each collected mental stress datapoint.
    mental_stress : array of float (113492,)
        collected mental stress ECG data from Arduino.
    xlim_mental_stress : tuple
        the x-limits for rest data plot, chosen from analyzing the raw plot.
    physical_stress_time : array of float (153721,)
        the time in seconds corresponding to each collected physical stress datapoint.
    physical_stress : array of float (153721,)
        collected physical stress ECG data from Arduino.
    xlim_physical_stress : tuple
        the x-limits for rest data plot, chosen from analyzing the raw plot.

    Returns
    -------
    None.
    """

    fig, axes = plt.subplots(2, 2, figsize=(10,6)) #set up full figure
    axes[0,0].plot(rest_time, rest, color='blue') #assign rest subplot
    axes[0, 0].set_title('Rest') #annotate subplot
    axes[0, 0].set_xlabel('Time (s)')
    axes[0, 0].set_ylabel('Voltage (mV)')
    axes[0, 0].set_xlim(xlim_rest) #set x-limits for subplot
    axes[0, 0].grid(True)
    
    axes[0,1].plot(relax_time, relax, color='red') #assign relaxed subplot
    axes[0, 1].set_title('Relaxed') #annotate subplot
    axes[0, 1].set_xlabel('Time (s)')
    axes[0, 1].set_ylabel('Voltage (mV)')
    axes[0, 1].set_xlim(xlim_relax) #set x-limits for subplot
    axes[0, 1].grid(True)
    
    axes[1,0].plot(mental_stress_time, mental_stress, color='orange') #assign third subplot
    axes[1, 0].set_title('Mental Stress') #annotate subplot
    axes[1, 0].set_xlabel('Time (s)')
    axes[1, 0].set_ylabel('Voltage (mV)')
    axes[1, 0].set_xlim(xlim_mental_stress) #set x-limits for subplot
    axes[1, 0].grid(True)
    
    axes[1,1].plot(physical_stress_time, physical_stress, color='green') #assign fourth subplot
    axes[1, 1].set_title('Physical Stress') #annotate subplot
    axes[1, 1].set_xlabel('Time (s)')
    axes[1, 1].set_ylabel('Voltage (mV)')
    axes[1, 1].set_xlim(xlim_physical_stress) #set x-limits for subplot
    axes[1, 1].grid(True)
    
    fig.suptitle('Raw Data Plots') #annotate full figure
    plt.tight_layout()
    plt.show()
    
#%% Part 2: Filter Your Data
def apply_filter(signal, fs, low_cutoff, high_cutoff):
    """
    This function applies the discrete Fast Fourier Transform to the datasets. It creates frequency arrays of the signals before applying a mask that uses the cutoff frequencies.

    Parameters
    ----------
    signal : array
        contains raw data to be filtered (rest, relax, mental_stress, physical_stress).
    fs : int
        frequency with which signals were collected from Arduino (Hz).
    low_cutoff : int
        the frequency below which signals are blocked (Hz).
    high_cutoff : int
        the frequency above which signals are blocked (Hz).

    Returns
    -------
    filtered_signal : array
        the filtered signal after applying the Fast Fourier Transform.

    """
    # define low and high cutoff frequencies
    low_cutoff = 5 # Hz
    high_cutoff = 70 # Hz
    
    # find signal filter and frequency response
    freq_array = np.fft.rfftfreq(len(signal), 1/fs) #create frequency arrays
    bandpass_mask = (freq_array >= low_cutoff) & (freq_array <= high_cutoff) #create a bandpass mask using the high and low cutoff frequencies provided in the script
    fft_signal = np.fft.rfft(signal) #apply the FFT to the signal
    filtered_fft = fft_signal * bandpass_mask #apply the mask to the FFT
    filtered_signal = np.fft.irfft(filtered_fft) #inverse FFT
    
    # find impulse response
    impulse_response = np.fft.irfft(bandpass_mask) # find impulse response from frequency response
    impulse_response = np.fft.fftshift(impulse_response) #flip first and second half of impulse response
    
    return filtered_signal, bandpass_mask, impulse_response, freq_array

def bandpass_filter(fs, rest, relax, mental_stress, physical_stress, low_cutoff, high_cutoff):
    """
    This function applies a bandpass filter to all the signals in each dataset by calling the apply_filter function.

    Parameters
    ----------
    fs : int
        frequency with which signals were collected from Arduino (Hz).
    rest : array of float (148815,)
        collected rest ECG data from Arduino.
    relax : array of float (152552,)
        collected relax ECG data from Arduino.
    mental_stress : array of float (113492,)
        collected mental stress ECG data from Arduino.
    physical_stress : array of float (153721,)
        collected physical stress ECG data from Arduino.
    low_cutoff : int
        the frequency below which signals are blocked (Hz).
    high_cutoff : int
        the frequency above which signals are blocked (Hz).

    Returns
    -------
    filtered_rest : array of float (SIZE)
        resultant rest data after filtering with a bandpass filter.
    filtered_relax : array of float (SIZE)
        resultant relax data after filtering with a bandpass filter.
    filtered_mental : array of float (SIZE)
        resultant mental stress data after filtering with a bandpass filter.
    filtered_physical : array of float (SIZE)
        resultant physical stress data after filtering with a bandpass filter.

    """
    # Apply the filter to each dataset
    filtered_rest, freq_response, impulse_response, x_axis = apply_filter(rest, fs, low_cutoff, high_cutoff)
    filtered_relax, freq_response, impulse_response, x_axis = apply_filter(relax, fs, low_cutoff, high_cutoff)
    filtered_mental, freq_response, impulse_response, x_axis = apply_filter(mental_stress, fs, low_cutoff, high_cutoff)
    filtered_physical, freq_response, impulse_response, x_axis = apply_filter(physical_stress, fs, low_cutoff, high_cutoff)

    return filtered_rest, filtered_relax, filtered_mental, filtered_physical, freq_response, impulse_response, x_axis
 
    
#%% Part 3: Detect Heartbeats
def load_file (input_file):
    data = np.loadtxt(input_file)
    time = np.arange(0, len(data)/500, 1/500)
    voltage = data
    boolean_mask = (time > 10.55) & (time < 11.1)
    template = voltage[boolean_mask]
    return template

#%% Part 4: Calculate Heart Rate Variability
def calculate_hrv (ibi_data_series):
    rr_deviations = ibi_data_series - np.mean(ibi_data_series)
    rr_variance = np.mean(rr_deviations ** 2)
    hrv = np.sqrt(rr_variance)
    return hrv

#%% Part 5: Get HRV Frequency Band Power
