# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 08:59:05 2024

@author: danny


It comes from audio chatting with ChatGPt in my phone. I asked about statistical methods for analysis uneven spaced time series and this new method for me was
mentioned "Detrended Fluctuation Analysis"

-Mudelsee book Detrended Fluctuation Analysis, 44–48, 55
"""

#%%Detrended fluctuation Analysis 

# Import spectral variance functions
from neurodsp.spectral import compute_spectral_hist, compute_scv, compute_scv_rs

# Import function to compute power spectra
from neurodsp.spectral import compute_spectrum

# Import utilities for loading and plotting data
from neurodsp.utils import create_times
from neurodsp.utils.download import load_ndsp_data
from neurodsp.plts.time_series import plot_time_series
from neurodsp.plts.spectral import (plot_spectral_hist, plot_scv,
                                    plot_scv_rs_lines, plot_scv_rs_matrix)



# Download, if needed, and load example data files
sig = load_ndsp_data('sample_data_2.npy', folder='data')

# Set sampling rate, and create a times vector for plotting
fs = 1000
times = create_times(len(sig)/fs, fs)

# Plot the loaded signal
plot_time_series(times, sig, xlim=[0, 3])


# Calculate the spectral histogram
freqs, bins, spect_hist = compute_spectral_hist(sig, fs, nbins=50, f_range=(0, 80),
                                                cut_pct=(0.1, 99.9))

# Calculate a power spectrum, with median Welch
freq_med, psd_med = compute_spectrum(sig, fs, method='welch',avg_type='median', nperseg=fs*2)

# Plot the spectral histogram
plot_spectral_hist(freqs, bins, spect_hist, freq_med, psd_med)