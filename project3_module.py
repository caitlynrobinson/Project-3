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
    freq_array = np.fft.rfftfreq(len(signal), 1/fs) #create frequency arrays
    bandpass_mask = (freq_array >= low_cutoff) & (freq_array <= high_cutoff) #create a bandpass mask using the high and low cutoff frequencies provided in the script
    fft_signal = np.fft.rfft(signal) #apply the FFT to the signal
    filtered_fft = fft_signal * bandpass_mask #apply the mask to the FFT
    filtered_signal = np.fft.irfft(filtered_fft) #inverse FFT
    
    return filtered_signal

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
    filtered_rest = apply_filter(rest, fs, low_cutoff, high_cutoff)
    filtered_relax = apply_filter(relax, fs, low_cutoff, high_cutoff)
    filtered_mental = apply_filter(mental_stress, fs, low_cutoff, high_cutoff)
    filtered_physical = apply_filter(physical_stress, fs, low_cutoff, high_cutoff)

    return filtered_rest, filtered_relax, filtered_mental, filtered_physical

# #  #
#   for signal in ecg_data:
#    freq_array = np.fft.rfftfreq(len(signal), 1/fs)

# #  #
#   low_cutoff =
#   high_cutoff = 
#   filter = np.ones(len(freq_array))
#   filter[(f<=low_cutoff) & (f>=high_cutoff)] = 0

# # # 
#  ecg_fft = np.fft.fft(ecg_data)
#  filtered_freq = filter * ecg_fft
#  filtered_time = np.fft.irfft(filtered_freq)

#  return filtered_freq, filtered_time
 
#%% Part 3: Detect Heartbeats
def normalize_template (trial_mean):
    demeaned_signal = trial_mean - np.mean(trial_mean)
    energy = np.square(demeaned_signal)
    energy = np.sum(energy)
    template = demeaned_signal / energy
    return template

def get_template_match (signal_voltage, template):
    flipped_template = np.flip(template)
    template_match = np.convolve(signal_voltage, flipped_template)
    return template_match

def predict_beat_times (template_match, threshold = ):
    above_threshold = template_match > threshold
    before_threshold = template_match[:-1] < threshold
    before_threshold = np.concatenate(([False], before_threshold))
    mask = above_threshold & before_threshold
    beat_samples = np.where(mask)[0] + 1
    return beat_samples
    
def detect_beats (trial_mean, signal_voltage, threshold):
    template = normalize_template(trial mean)
    template_match = get_template_match (signal_voltage, template)
    beat_samples = predict_beat_times(template_match, threshold)
    return beat_samples, template match

#%% Part 4: Calculate Heart Rate Variability

#%% Part 5: Get HRV Frequency Band Power
