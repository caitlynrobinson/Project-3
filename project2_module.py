#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 13:24:48 2024

@author: kaelen
"""



#Import modules
import numpy as np
from matplotlib import pyplot as plt

#%% Part 1

#Reuse Proj1 module to load ecg data
def load_data(input_file):
        '''
    This functions loads the file named in input_file. Then uses loop to index through 
    and obtain each key stored in the file. Then it indexs the file with each unique key
    to store the data for each key in a seperate variable.

    Parameters
    ----------
    input_file : 'NpzFile' 
        object

    Returns
    -------
    ecg_voltage : Array of float, size: (900000, 0)
        The raw readings of the voltage. 
    fs : int
        A set value of the number of times the data was sampled per second.
    label_samples : Array of int, size: (3661, 0)
        An array of values where each value is the index of the symbol for the data.
    label_symbols : Array of str, size: (3661, 0)
        A str value dispalying wether the voltage was normal or abnormal.
    subject_id : int: e0103
        Id of the subject used in the test.
    electrode : str: V4
        The electrode the ECG data was gathered from.
    units : str: mV
        The units voltage is measured in .

    '''  

        data = np.load(input_file)
        for field_name_index in data.files:
            print(field_name_index)
        ecg_voltage = data['ecg_voltage']
        fs = data['fs']
        label_samples = data['label_samples']
        label_symbols = data['label_symbols']
        subject_id = data['subject_id']
        electrode = data['electrode']
        units = data['units']
        return ecg_voltage, fs, label_samples, label_symbols, subject_id, electrode, units

def load_means(input_file):
    """
    This function loads the file in input_file_means. It then defines four variables by 
    indexing the file.

    Parameters
    ----------
    input_file : 'NpzFile' 
        object

    Returns
    -------
    symbols : Array of str, size: (0,2)
        An array of possible symbols for beats in the ecg.
    trial_time : Arry of float, size: (0,250)
        An array of the ecg values at given times.
    mean_trial_voltages : Array of float, size: (2, 250)
        An array describing the ecg values of normal beats vs arrhythmic beats.

    """
    data_means = np.load(input_file)
    symbols = data_means['symbols']
    trial_time = data_means['trial_time']
    mean_trial_voltages = data_means['mean_trial_signal']
    return symbols, trial_time, mean_trial_voltages
        
#%% Part 2
def decimate_data(original_signal, decimation_factor):
    '''
    This function reduces the sampling frequency of a given signal by selecting only signal values 
    that correspond with a given decimation factor.
    
    Parameters
    ----------
    original_signal : Array of float, size: (n,)
        Array of signal sample values
    decimation_factor : int
        The factor by which the given signal is being downsampled
    
    Returns
    -------
    decimated_signal : Array of float, size:(n,)
        Array containing the decimated signal values only
    
    '''
        # decimation factor is loaded in the module, should it be loaded in script and called here for more flexibility?
    decimated_signal = original_signal[::decimation_factor]
    return decimated_signal

#%% Part 3
def normalize_template(trial_mean):
    '''
    This function normalizes a given signal by subtracting the signal mean from each signal value,
    then dividing by the energy of the demeaned signal.
    
    Parameters
    ----------
    trial_mean : Array of float, size: (n,)
        Array of beat means for an event
    
    Returns
    -------
    template : Array of float, size: (n,)
        Normalized array of trial_mean signal values
    
    '''
    demeaned_signal = trial_mean- np.mean(trial_mean)
    energy = np.square(demeaned_signal)
    energy = np.sum(energy)
    template = demeaned_signal / energy
    return template

#%% Part 4
def get_template_match(signal_voltage, template):
    '''
     This function quantifies how well a signal matches a signal template using convolution and discrete cross correlation
    
     Parameters
     ----------
     signal_voltage : Array of float, size: (n,)
         Array of voltage signal (or other signal) that the template will be cross-correlated with
     template : Array of float, size: (n,)
         Normalized array of trial mean signal values
    
     Returns
     -------
     template_match : Array of float, size: (n,)
         Array resulting from cross correlation of signal_voltage and template in which high values indicate similarity between the two arrays

     '''
    flipped_template = np.flip(template)
    template_match = np.convolve(signal_voltage, flipped_template, 'same')
    return template_match

#%% Part 5
def predict_beat_times(template_match, threshold):
    """
    This function identifies beat occurence in a signal by identifying times when the sample value exceeds a specified threshold
 
    Parameters
    ----------
    template_match : Array of float, size: (n,)
        Array in which high values indicate similarity between a given signal and a signal template at a sample
    threshold : int
        The minimum value a sample must have in order to be considered a beat
 
    Returns
    -------
    beat_samples : Array of float, size: (n,)
        Array of times in template_match when beats (values above threshold) are detected
 
    """
    # Create a boolean mask for template_match values that exceed the threshold
    above_threshold = template_match > threshold
    # Create a mask for values that are below the threshold, but exclude the last element
    before_threshold = template_match[:-1] < threshold
    # Shift `before_threshold` to the right by one element to align with `above_threshold`
    before_threshold = np.concatenate(([False], before_threshold)) 
    # Find beats by checking where the condition holds true: above_threshold followed by below_threshold
    mask = above_threshold & before_threshold
    # Find the indices where the mask is True (where beats are detected) and add 1 to shift from 0-based to 1-based index
    beat_samples = np.where(mask)[0] + 1
    return beat_samples
    

#%% Part 6
def run_beat_detection(trial_mean, signal_voltage, threshold):
    """
    The function detects arrhythmic beats by normalizing a template based on trial mean, comparing the template based on the signal voltage, and setting a threshold minimum value for the beats.
    
    Parameters
    ----------
    trial_mean : Array of float, size: (n,)
        Array of beat means for an event
    signal_voltage : Array of float, size: (n,)
        Array of voltage signal
    threshold : int
        The minimum value a sample must have in order to be considered a beat
    
    Returns
    -------
    beat_samples : Array of float, size: (n,)
        Array of samples identified as beats because they are at or above threshold value
    template_match : Array of float, size: (n,)
        Array in which high values indicate similarity between a signal and the signal template at a sample
    
    """
    
    template = normalize_template(trial_mean)
    template_match = get_template_match(signal_voltage, template)
    beat_samples = predict_beat_times(template_match, threshold)
    return beat_samples, template_match

def plot_events(label_samples, label_symbols, signal_time, signal_voltage):
    """
    
    Parameters
    ----------
    features: for-loop, plot function
        This function contains a for-loop to go sort label_symbols_unique and assign it to an event_time when that label was identified. 
        It then plots those labels above those timestamps. Input arrays must be the same size.
    labels: int, str, float
        Each array that is input contains either float, integer, or string values.
    label_samples : 1D numpy array of ints
        Array with value labeling of each data sample. 
    label_symbols : 1D numpy array of strings
        Array with symbol labeling of each data sample. 
    signal_time : 1D numpy array of floats or ints
        Placeholder array for time values. 1D numpy array containing numerical data.
    signal_voltage : 1D numpy array of floats or ints
        Placeholder array for ecg_voltage values. 1D numpy array containing numerical data.

    Returns
    -------
    None.

    """
    label_symbols_unique = np.unique(label_symbols)
    #establish for loop
    for event in label_symbols_unique:
      event_samples = label_samples[label_symbols == event]
      event_time = signal_time[event_samples]
      event_voltage = signal_voltage[event_samples]
      plt.scatter(event_time, event_voltage, marker = 'o', label = event)
 
    
    