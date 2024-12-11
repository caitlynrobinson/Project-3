"""
Project 3: ANS Evaluation
Authors: Kaelen Kenna & Caitlyn Robinson
BME 3000
MODULE

This module contains functions called in project3_script to analyze Autonomic Nervous System activity from ECG data. It plots raw ECG data, filters the data with a bandpass filter, and creates a template to analyze heart rate variability to interpolate the data and create a power ratio between parasympathetic and sympathetic activity.
"""

# Import packages
import numpy as np 
import matplotlib.pyplot as plt

#%% Part 1: Collect & Load Data
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
    plt.figure(figsize=(10, 6)) #set up figure
    
    # Rest subplot
    plt.subplot(2, 2, 1)
    plt.plot(rest_time, rest, color='blue')
    plt.title('Rest')
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (mV)')
    plt.xlim(xlim_rest) #set x-limits for the subplot
    plt.grid(True)

    # Relaxed subplot
    plt.subplot(2, 2, 2)
    plt.plot(relax_time, relax, color='red')
    plt.title('Relaxed')
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (mV)')
    plt.xlim(xlim_relax) #set x-limits for the subplot
    plt.grid(True)

    # Mental Stress subplot
    plt.subplot(2, 2, 3) 
    plt.plot(mental_stress_time, mental_stress, color='orange')
    plt.title('Mental Stress')
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (mV)')
    plt.xlim(xlim_mental_stress) #set x-limits for the subplot
    plt.grid(True)

    # Physical Stress subplot
    plt.subplot(2, 2, 4)
    plt.plot(physical_stress_time, physical_stress, color='green')
    plt.title('Physical Stress')
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (mV)')
    plt.xlim(xlim_physical_stress) #set x-limits for the subplot
    plt.grid(True)

    # Annotate figure
    plt.suptitle('Raw Data Plots')
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
    filtered_signal : array of float
        the filtered signal after applying the Fast Fourier Transform.
    bandpass_mask : array of bool
        identifies frequency measurements within the specified range.
    impulse_response : array of float (153720,)
        DESCRIPTION.
    freq_array : array of float
        represents discrete frequencies corresponding to Fourier transform of input signal.

    """
    # Find signal filter and frequency response
    freq_array = np.fft.rfftfreq(len(signal), 1/fs) #create frequency arrays
    bandpass_mask = (freq_array >= low_cutoff) & (freq_array <= high_cutoff) #create a bandpass mask using the high and low cutoff frequencies provided in the script
    fft_signal = np.fft.rfft(signal) #apply the FFT to the signal
    filtered_fft = fft_signal * bandpass_mask #apply the mask to the FFT
    filtered_signal = np.fft.irfft(filtered_fft) #inverse FFT
    
    # Find impulse response
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
        collected rest ECG data from Arduino
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
    filtered_rest : array of float (148814,)
        resultant rest data after filtering with a bandpass filter.
    filtered_relax : array of float (152552,)
        resultant relax data after filtering with a bandpass filter.
    filtered_mental : array of float (113492,)
       resultant mental stress data after filtering with a bandpass filter.
    filtered_physical : array of float (153720,)
       resultant physical stress data after filtering with a bandpass filter.
    freq_response : array of bool (76861,)
        the magnitude of the filter's response at corresponding frequencies.
    impulse_response : array of float (153720,)
        describes how the filter responds to a unit impulse input.
    x_axis : array of float (76861,)
        the x-axis values of the frequency response.

    """
    # Apply the filter to each dataset
    filtered_rest, freq_response, impulse_response, x_axis = apply_filter(rest, fs, low_cutoff, high_cutoff)
    filtered_relax, freq_response, impulse_response, x_axis = apply_filter(relax, fs, low_cutoff, high_cutoff)
    filtered_mental, freq_response, impulse_response, x_axis = apply_filter(mental_stress, fs, low_cutoff, high_cutoff)
    filtered_physical, freq_response, impulse_response, x_axis = apply_filter(physical_stress, fs, low_cutoff, high_cutoff)

    return filtered_rest, filtered_relax, filtered_mental, filtered_physical, freq_response, impulse_response, x_axis

#%% Part 3: Detect Heartbeats

def load_file (input_file, fs, lower_time, upper_time):
    """
    This function loads the selected input file to be used in a module imported from Project 2.

    Parameters
    ----------
    input_file : string
        the name of the file being loaded.

    Returns
    -------
    template : array of float (274,)
        template of signal values after applying Boolean mask.

    """
    data = np.loadtxt(input_file)
    time = np.arange(0, len(data)/fs, 1/fs)
    voltage = data
    
    # Create a Boolean mask to define template
     boolean_mask = (time > lower_time) & (time < upper_time)
    template = voltage[boolean_mask]
    return template

#%% Part 4: Calculate Heart Rate Variability

def calculate_hrv (ibi_data_series):
    """
    This function calculates heart rate variation by analyzing R-R values. It finds the variance between these values to estimate average HRV.

    Parameters
    ----------
    ibi_data_series : array of float (ndarray)
        the inter-beat interval calulations for each dataset.

    Returns
    -------
    hrv : float
        heart rate variation for each dataset.

    """
    rr_deviations = ibi_data_series - np.mean(ibi_data_series)
    rr_variance = np.mean(rr_deviations ** 2)
    hrv = np.sqrt(rr_variance)
    return hrv

def interpolate_data (beat_times, ibi_data, dt):
    """
    This function uses HRV, calculated in calculate_hrv, to interpolate to estimate inter-beat intervals (IBIs) at unknown times.

    Parameters
    ----------
    beat_times : array of float (ndarray)
        the times at which heartbeats occurred for each dataset.
    ibi_data : array of float (ndarray)
        the data that contaisn inter-beat intervals for each datset.
    dt : float
        1/fs, time between sampling points.

    Returns
    -------
    interpolated_data : array of float (ndarray)
        the predicted IBIs calculated by interpolating from the data template.

    """
    # Create new time array for interpolated values
    new_time_array = np.arange(0, beat_times[-1], dt)
    
    # Interpolate ibi values
    interpolated_data = np.interp(new_time_array, beat_times[1:], ibi_data)
    return interpolated_data

#%% Part 5: Get HRV Frequency Band Power

def get_freq_power (interpolated_data, dt):
    """
    This function calclates the frequency domain and frequency power by using interpolated data found in Part 4. It is then used to graph each type of activity data to identify nervous system activity.

    Parameters
    ----------
    interpolated_data : array of float (ndarray)
        the predicted IBIs calculated by interpolating from the data template.
    dt : int
        the time step (s).

    Returns
    -------
    freq_power : array of float (ndarray)
        the intensity of each signal in a dataset.
    freq_domain : array of float (ndarray)
        the frequency values corresponding to the Fourier transform of the interpolated data.

    """
    # normalize interpolated data by subtracting mean
    mean_interp_data = interpolated_data - np.mean(interpolated_data)
    
    # calculate x and y values for freqeuency vs. power graphs
    freq_amplitude = np.fft.rfft(mean_interp_data)
    freq_domain = np.fft.rfftfreq(len(interpolated_data), dt) # x values
    freq_power = (np.abs(freq_amplitude)) ** 2 # y values
    return freq_power, freq_domain

def get_power_ratio (freq_domain, freq_power, parasympathetic_low, parasympathetic_high, sympathetic_low, sympathetic_high):
    """
    This function calculates the power ratio between low frequency and high frequency signals in the parasympathetic and sympathetic nervous system.

    Parameters
    ----------
    freq_domain : array of float (ndarray)
        the frequency values corresponding to the Fourier transform of the interpolated data.
    freq_power : array of float (ndarray)
        the intensity of each signal in a dataset.

    Returns
    -------
    power_ratio : float
        the ratio of power between the low-frequency band and the high-frequency band in the ANS.

    """
    # Make low and high frequency boolean masks to separate ANS activity
    low_freq_mask = (freq_domain > parasympathetic_low) & (freq_domain < parasympathetic_high)
    high_freq_mask = (freq_domain > sympathetic_low) & (freq_domain < sympathetic_high)
    
    # Calculate mean low and high power
    low_freq_power = freq_power[low_freq_mask]
    high_freq_power = freq_power[high_freq_mask]
    mean_low_power = np.mean(low_freq_power)
    mean_high_power = np.mean(high_freq_power)
    
    # Calculate power ratio lf/hf
    power_ratio = mean_low_power / mean_high_power
    return power_ratio

