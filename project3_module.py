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

#%% Part 1: Collect and Load Data
def load_data(input_files):
    """
    This function works to load the four datasets collected with the Arduino.

    Parameters
    ----------
    input_files : list of strings
        The paths of each of the four input files which correspond to Arduino activity datasets.

    Returns
    -------
    contents : list of strings
        The data that corresponds to each Ardunio dataset, separated by row.

    """
    contents = [open(path).read() for path in input_files]
    return contents


def separate_datasets(contents):
    """
    This function separates each dataset that was loaded with load_data, so each activity corresponds to its own list

    Parameters
    ----------
    contents : list of strings
        The data that corresponds to each Ardunio dataset, separated by row.

    Returns
    -------
    list
        DESCRIPTION.

    """
    return [content.split('\n') for content in contents]

#%% Part 2: Filter Your Data

#%% Part 3: Detect Heartbeats

#%% Part 4: Calculate Heart Rate Variability

#%% Part 5: Get HRV Frequency Band Power

















