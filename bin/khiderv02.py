#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 09:02:52 2024

@author: danny
"""
#This script comes from https://github.com/khider/pyleoGPT/blob/main/Pyleoclim%20and%20ChatGPT.ipynb 
#and the use of chatgpt and pyleoclim

import pyleoclim as pyleo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
os.chdir('C:/Users/danny/OneDrive/IKER Speleothems/Dino Spelo/bin')
print("Current Working Directory:", os.getcwd())

#%%

# Read the record
df = pd.read_table('..\data\GDD1_d18O_CopraSpline_2mm.txt')
df.head()


'''
Plot the record
'''
series = pyleo.Series(time =  df.iloc[:, 0] , value = df.iloc[:, 1], label = 'Dino1 speleothem',
                  time_name = 'Age', value_name = 'd18O',
                  time_unit = 'Years BP',   value_unit = 'VPDB', verbose=False)            


fig, ax = series.plot(invert_yaxis=False)


'''
Plot warming stripe
'''
fig, ax = series.stripes(ref_period=(5400,7000), show_xaxis=True)



'''
Perform spectral analysis
'''
#spec_result = series.spectral(method='lomb_scargle')

spec_result = series.spectral(method='wwz')
spec_result.plot()


#From Khider
spec_result = series.standardize().interp().spectral(method='periodogram')
fig, ax=spec_result.plot(label='Periodogram')
series.standardize().interp().spectral(method='welch').plot(ax=ax,label='Welch')
series.standardize().interp().spectral(method='mtm').plot(ax=ax,label='MTM')
series.standardize().spectral(method='lomb_scargle').plot(ax=ax,label='Lomb Scargle')
series.standardize().spectral(method='wwz').plot(ax=ax,label='WWZ',lgd_kwargs={'bbox_to_anchor':(1.05, 1)})


#From Climatch
fig, ax = plt.subplots()
# basic periodogram
series.interp(step=0.5).standardize().spectral(method="periodogram").plot(
    ax=ax, xlim=[1000, 5], ylim=[0.001, 1000], label="periodogram")
# Welch's periodogram
series.interp(step=0.5).standardize().spectral(method="welch").plot(
    ax=ax, xlim=[1000, 5], ylim=[0.001, 1000], label="welch")
# Multi-taper Method
series.interp(step=0.5).standardize().spectral(method="mtm").plot(
    ax=ax, xlim=[1000, 5], ylim=[0.001, 1000], label="mtm")
# Lomb-Scargle periodogram
series.standardize().spectral(method="lomb_scargle").plot(
    ax=ax, xlim=[1000, 5], ylim=[0.001, 1000], label="lomb_scargle")
# weighted wavelet Z-transform (WWZ)
series.standardize().spectral(method="wwz").plot(
    ax=ax, xlim=[1000, 5], ylim=[0.001, 1000], label="wwz")




# Lomb-Scargle periodogram seems robust, so I choose it
series_ls = series.standardize().spectral(method="lomb_scargle")
series_ls.plot(xlim=[1000, 5], ylim=[0.001, 1000], label="lomb_scargle")

#Finding significant peaks
series_ls_sig = series_ls.signif_test()
series_ls_sig.plot(xlabel="Period [years]")



fig, ax = plt.subplots()
ax.plot(series_ls_sig.frequency, series_ls_sig.amplitude)
ax.set_xlim([0.005, 0.07])
ax.set_ylim([0, 200])
ax.set_xlabel("Frequency [1/yr]")
ax.set_ylabel("Spectra Amplitude")




#Full with wavelet
# create a scalogram
scal = series.standardize().wavelet(method="wwz")
series.summary_plot(psd=series_ls_sig, scalogram=scal, psd_label="Amplitude")






#Scalogram
scal = series.wavelet(method='wwz')
fig, ax = scal.plot()



scal = series.interp().wavelet()
scal.plot()

#Scal significant
scal_sig = scal.signif_test(method='wwz')
scal_sig.plot()






''' 
Wavelet coherence 2024.03.14 based on 067_Grinsted et al.2004; SSA048_Vaughan et al.2011; 
In Grinsted's paper, it is stated that performing the WWZ is slow, and sometimes interpolation can be used for preliminary analysis using the XWT

This is a preliminary test to evaluate WTC between the Dino1 ts from high and low resolution
'''
din2 = pd.read_table('..\data\GDD1_d18O_CopraSpline_2mm.txt')
din5 = pd.read_table('..\data\GDD1_d18O_CopraSpline_5mm.txt')

din2.head()
din5.head()


din2ts = pyleo.Series(time =  din2.iloc[:, 0] , value = din2.iloc[:, 1], label = 'Dino1_2mm',
                  time_name = 'Age', value_name = 'd18O',
                  time_unit = 'Years BP',   value_unit = 'VPDB', verbose=False)   


din5ts = pyleo.Series(time =  din5.iloc[:, 0] , value = din5.iloc[:, 1], label = 'Dino1_5mm',
                  time_name = 'Age', value_name = 'd18O',
                  time_unit = 'Years BP',   value_unit = 'VPDB', verbose=False)     


din5ts.plot(color='C1')
din2ts.plot(color='C2')



# MultipleSeries plot
ms = pyleo.MultipleSeries([din2ts,din5ts])
ms.plot()
ms.standardize().plot()



# WTC using WWZ for unevenly speced time series
coh = din2ts.wavelet_coherence(din5ts,method='wwz')
fig, ax = coh.plot()

coh_sig = coh.signif_test(number=10)
fig, ax = coh_sig.plot()


# For visualizing the WTC and XWT 
coh_sig.dashboard()

plt.savefig(r'..\results\dinos_XWT.png', format='png', dpi=300)
plt.close()





#fast

cnb = pd.read_table('..\data\CNB_d18O.txt')
cuy = pd.read_table('..\data\CUY_d18O.txt')


cnbts = pyleo.Series(time =  cnb.iloc[:, 0] , value = cnb.iloc[:, 1], label = 'Cneb-Mera',
                  time_name = 'Age', value_name = 'd18O',
                  time_unit = 'Years BP',   value_unit = 'VPDB', verbose=False)   


cuyts = pyleo.Series(time =  cuy.iloc[:, 0] , value = cuy.iloc[:, 1], label = 'Codo-Cuyuja',
                  time_name = 'Age', value_name = 'd18O',
                  time_unit = 'Years BP',   value_unit = 'VPDB', verbose=False) 



cnbts.plot(color='C1')
cuyts.plot(color='C2')


# Histogram from Astropy
from astropy.visualization import hist
#bin_Scott = hist(cuyts, bins='scott')
hist(cuy.iloc[:, 1], bins='scott')
plt.show()
# Using pyleoclim
fig, ax = cnbts.histplot()
fig, ax = cnbts.stripes(show_xaxis=True)







wavelet_result = cuyts.wavelet.cwt(cuy.iloc[:, 2], cuy.iloc[:, 1], freq=None, freq_method='log', detrend=False, standardize=True, pad=False, mother='MORLET', param=None)




ms = pyleo.MultipleSeries([cnbts,cuyts])
ms.standardize().plot()


coh = cnbts.wavelet_coherence(cuyts,method='wwz')
fig, ax = coh.plot()
coh_sig.dashboard()



#utilities
import pyleoclim as pyleo

ts_18 = pyleo.utils.load_dataset('cenogrid_d18O')
ts_13 = pyleo.utils.load_dataset('cenogrid_d13C')
ms = pyleo.MultipleSeries([ts_18, ts_13], label='Cenogrid', time_unit='ma BP')

fig, ax = ms.stackplot(linewidth=0.5, fill_between_alpha=0)

ax=pyleo.utils.plotting.make_annotation_ax(fig, ax, ax_name = 'highlighted_intervals', zorder=-1)
intervals = [[3, 8], [12, 18], [30, 31], [40,43], [49, 60], [60, 65]]
ax['highlighted_intervals'] = pyleo.utils.plotting.hightlight_intervals(ax['highlighted_intervals'], intervals,
    color='g', alpha=.1)



#%% Comparison with Tropical caves to observe if there is a synchrony on the ICTZ shift, as T306 d18O rainwater values seems to show similar pattern like in Ecuador

## Garganta del Dino cave, Ecuador
din2 = pd.read_table('..\data\GDD1_d18O_CopraSpline_2mm.txt')
din5 = pd.read_table('..\data\GDD1_d18O_CopraSpline_5mm.txt')

ts_din2 = pyleo.Series(
    time =  din2.iloc[:, 0] , 
    value = din2.iloc[:, 1],
    time_name = 'Age',
    time_unit = 'Years BP',
    value_name = 'd18O',
    value_unit = 'VPDB',
    label = 'GDD Cave, Ecuador d18Ocalc', verbose=False)

ts_din5 = pyleo.Series(
    time =  din5.iloc[:, 0] , 
    value = din5.iloc[:, 1],
    time_name = 'Age',
    time_unit = 'Years BP',
    value_name = 'd18O',
    value_unit = 'VPDB',
    label = 'GGD Cave, Ecuador d18Ocalc-5mm res', verbose=False)

## Santiago cave, Ecuador
sant = pd.read_table('..\data\santiago2012.txt', comment='#')
sant.head()
ts_sant = pyleo.Series(
    time=sant["age_calBP"],
    value=sant["d18OcarbVPDB"],
    time_name="Age",
    time_unit="years BP",
    value_name="d18O",
    value_unit="per mil",
    label="Santiago Cave, Ecuador d18Ocalc")

ts_sant.plot(color="C1", invert_yaxis=False)

## Tigre Perdido, Peru Alt+Shift in Notepad
tig = pd.read_table(r'..\data\tigre-perdido2008.txt', comment='#')
tig.head()
ts_tig = pyleo.Series(
    time=tig["Age"],
    value=tig["d18O PDB"],
    time_name="Age",
    time_unit="years BP",
    value_name="d18O",
    value_unit="per mil",
    label="Tigre Perdido Cave, Peru d18Ocalc")

ts_tig.plot(color="C1", invert_yaxis=False)

ts_tigmh = ts_tig.sel(time=slice(4000,8000))
ts_tigmh.plot(marker='o', color='gray')


## Tangga cave, Indonesia 2024.03.16
# Ignore lines that start with a specific character, for example, '#'
tang = pd.read_table(r'..\data\tangga2018d18o.txt', comment='#')
tang.head()

ts_tang = pyleo.Series(
    time=tang["age_calkaBP"]*1000,
    value=tang["d18O-raw"],
    time_name="Age",
    time_unit="years BP",
    value_name="d18O",
    value_unit="per mil",
    label="Tangga Cave, Sumatra d18Ocalc")

ts_tang.plot(color="C1", invert_yaxis=False)
fig, ax = ts_tang.histplot()



#%% 1.1. Use the Climate Data Operators (CDO) in Python for extracting the climatology from 
#RAIN4PE_daily_0.1d_1981_2015_v1.0.nc and save the extracted .txt time-series without spaces to be read by pyleoclim

import subprocess
import os
import pandas as pd

# Define the list of locations with names, latitudes, and longitudes
locations = [
    {"name": "dinocave", "lat": -1.425, "lon": -78.040},
    {"name": "tayuntscave", "lat": -3.022283, "lon": -78.13590},
    {"name": "porvenircave", "lat": -4.537983, "lon": -79.068583},
    {"name": "tigrecave", "lat": -5.9406, "lon": -77.308},
    {"name": "shatucacave", "lat": -5.70, "lon": -77.90}
]

# Define the directory path inside WSL, with spaces properly handled
source_directory_path = '/mnt/c/Users/danny/"OneDrive - Universidad Politecnica Salesiana"/Research/RAIN4PE'
destination_directory_path = 'C:/Users/danny/OneDrive/IKER Speleothems/Dino Spelo/data/r4pe'
input_filename = "RAIN4PE_daily_0.1d_1981_2015_v1.0.nc"

# Ensure the destination directory exists
os.makedirs(destination_directory_path, exist_ok=True)

for location in locations:
    name = location["name"]
    lon = location["lon"]
    lat = location["lat"]
    
    # Define filenames for the CDO output and the cleaned output
    output_nc_filename = f"{name}.nc"
    output_txt_filename = f"{name}.txt"
    cleaned_txt_filename = f"{name}_r4pe.txt"  # Output as .txt for consistency
    
    # Construct CDO commands for remapping and exporting to text
    remap_command = f'cd {source_directory_path} && cdo remapnn,lon={lon}_lat={lat} {input_filename} {output_nc_filename}'
    export_command = f'cd {source_directory_path} && cdo outputtab,date,lon,lat,value {output_nc_filename} > {output_txt_filename}'
    
    # Execute CDO commands
    try:
        subprocess.run(["wsl", "bash", "-c", remap_command], check=True, capture_output=True, text=True)
        subprocess.run(["wsl", "bash", "-c", export_command], check=True, capture_output=True, text=True)
        print(f"CDO commands executed successfully for {name}.")
    except subprocess.CalledProcessError as e:
        print(f"Error running CDO command for {name}: {e.stderr}")

    original_file_path = os.path.join(source_directory_path.replace('/mnt/c', 'C:').replace('"', ''), output_txt_filename)
    new_file_path = os.path.join(destination_directory_path, cleaned_txt_filename)

    # Read the file, excluding the last line (CDO summary), and process the data
    with open(original_file_path, 'r') as file:
        lines = file.readlines()[:-1]  # Exclude the last summary line
    with open(new_file_path, 'w') as new_file:
        for line in lines:
            new_file.write(line)

    # Load, format, and save the cleaned data with pandas
    df = pd.read_csv(new_file_path, delim_whitespace=True, header=None, skiprows=1, names=['date', 'lon', 'lat', 'value'])
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%d/%m/%Y')

    # Save the DataFrame back to a .txt file, using tabs as the separator, and including a clean header
    df.to_csv(new_file_path, sep='\t', index=False, header=True)

    print(f"Processed data and {cleaned_txt_filename} has been created in {destination_directory_path}.")


#%% 1.2. Extract txt files from Brazilian BR-DWGD pr_19810101_20001231_BR-DWGD_UFES_UTEXAS_v_3.2.2 

import subprocess
import os
import pandas as pd

# Define the list of locations with names, latitudes, and longitudes
locations = [
    {"name": "paraisocave", "lat": -4.07, "lon": -55.45},
    {"name": "lapagrandecave", "lat": -14.4227, "lon": -44.3656},
    {"name": "tocadaboavistacave", "lat": -10.1602, "lon": -40.8605},
    {"name": "curupiracave", "lat": -15.2003, "lon": -56.7839},
    {"name": "tamborilcave", "lat": -16.364, "lon": -46.904}
]

# Define the directory path inside WSL, with spaces properly handled
source_directory_path = '/mnt/c/Users/danny/"OneDrive - Universidad Politecnica Salesiana"/Research/BR-DWGD'
destination_directory_path = 'C:/Users/danny/OneDrive/IKER Speleothems/Dino Spelo/data/brdwgd'
input_filename = "pr_19810101_20001231_BR-DWGD_UFES_UTEXAS_v_3.2.2.nc"

# Ensure the destination directory exists
os.makedirs(destination_directory_path, exist_ok=True)

for location in locations:
    name = location["name"]
    lon = location["lon"]
    lat = location["lat"]
    
    # Define filenames for the CDO output and the cleaned output
    output_nc_filename = f"{name}.nc"
    output_txt_filename = f"{name}.txt"
    cleaned_txt_filename = f"{name}_brdwgd.txt"  # Output as .txt for consistency
    
    # Construct CDO commands for remapping and exporting to text
    remap_command = f'cd {source_directory_path} && cdo remapnn,lon={lon}_lat={lat} {input_filename} {output_nc_filename}'
    export_command = f'cd {source_directory_path} && cdo outputtab,date,lon,lat,value {output_nc_filename} > {output_txt_filename}'
    
    # Execute CDO commands
    try:
        subprocess.run(["wsl", "bash", "-c", remap_command], check=True, capture_output=True, text=True)
        subprocess.run(["wsl", "bash", "-c", export_command], check=True, capture_output=True, text=True)
        print(f"CDO commands executed successfully for {name}.")
    except subprocess.CalledProcessError as e:
        print(f"Error running CDO command for {name}: {e.stderr}")

    original_file_path = os.path.join(source_directory_path.replace('/mnt/c', 'C:').replace('"', ''), output_txt_filename)
    new_file_path = os.path.join(destination_directory_path, cleaned_txt_filename)

    # Read the file, excluding the last line (CDO summary), and process the data
    with open(original_file_path, 'r') as file:
        lines = file.readlines()[:-1]  # Exclude the last summary line
    with open(new_file_path, 'w') as new_file:
        for line in lines:
            new_file.write(line)

    # Load, format, and save the cleaned data with pandas
    df = pd.read_csv(new_file_path, delim_whitespace=True, header=None, skiprows=1, names=['date', 'lon', 'lat', 'value'])
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%d/%m/%Y')

    # Save the DataFrame back to a .txt file, using tabs as the separator, and including a clean header
    df.to_csv(new_file_path, sep='\t', index=False, header=True)

    print(f"Processed data and {cleaned_txt_filename} has been created in {destination_directory_path}.")



#%% 2.1. Import the generated _R4PE.txt files from different paleorecords for comparison in a loop

import pandas as pd
import pyleoclim as pyleo

# List of file names to process
file_names = [
    "dinocave_r4pe.txt",
    "tayuntscave_r4pe.txt",
    "shatucacave_r4pe.txt",
    "porvenircave_r4pe.txt",
    "tigrecave_r4pe.txt",
    "tayuntscave_r4pe.txt"
]

# Directory where the files are located
data_dir = '../data/r4pe/'

def format_label(file_name):
    """Format file name into a proper label."""
    # Remove the suffix and split by "cave"
    name_parts = file_name.split('_')[0].split("cave")
    # Capitalize the first part and reassemble the label
    label = name_parts[0].capitalize() + " cave"
    return label

# Loop through each file name
for file_name in file_names:
    # Construct the full file path
    file_path = data_dir + file_name
    
    # Read the data file
    df = pd.read_table(file_path)
    
    # Convert date to 'DD/MM/YYYY' format recognizable in Pyleoclim
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
    
    # Convert to "Year CE" as floating-point years correctly
    df['year_ce'] = df['date'].dt.year + (df['date'].dt.dayofyear - 1) / 365.25

    # Format the label using the helper function
    label = format_label(file_name)

    # Create a Pyleoclim Series object
    ts = pyleo.Series(
        time=df["year_ce"],
        value=df["value"],
        time_name="Date",
        time_unit="days",
        value_name="Rainfall",
        value_unit="mm",
        label=f"Daily Rainfall {label} 1981-2015 (mm)"
    )
    
    # Plot the series
    ts.plot()

#%% 2.2. Import the generated _BRDWGD.txt files from different paleorecords for comparison in a loop

# List of file names to process
file_names = [
    "lapagrandecave_brdwgd.txt",
    "paraisocave_brdwgd.txt",
    "tamborilcave_brdwgd.txt",
    "tocadaboavistacave_brdwgd.txt",
    "curupiracave_brdwgd.txt"
]

# Directory where the files are located
data_dir = '../data/brdwgd/'

def format_label(file_name):
    """Format file name into a proper label."""
    # Remove the suffix and split by "cave"
    name_parts = file_name.split('_')[0].split("cave")
    # Capitalize the first part and reassemble the label
    label = name_parts[0].capitalize() + " cave"
    return label

# Loop through each file name
for file_name in file_names:
    # Construct the full file path
    file_path = data_dir + file_name
    
    # Read the data file
    df = pd.read_table(file_path)
    
    # Convert date to 'DD/MM/YYYY' format recognizable in Pyleoclim
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
    
    # Convert to "Year CE" as floating-point years correctly
    df['year_ce'] = df['date'].dt.year + (df['date'].dt.dayofyear - 1) / 365.25

    # Format the label using the helper function
    label = format_label(file_name)

    # Create a Pyleoclim Series object
    ts = pyleo.Series(
        time=df["year_ce"],
        value=df["value"],
        time_name="Date",
        time_unit="days",
        value_name="Rainfall",
        value_unit="mm",
        label=f"Daily Rainfall {label} 1981-2000 (mm)"
    )
    
    # Plot the series
    ts.plot()


#%% 3.1. Create monthly ts for daily precipitation for r4pe datasets

import pandas as pd
import os

# List of file paths to process
file_paths = [
    '../data/r4pe/dinocave_r4pe.txt',
    '../data/r4pe/tayuntscave_r4pe.txt',
    '../data/r4pe/shatucacave_r4pe.txt',
    '../data/r4pe/porvenircave_r4pe.txt',
    '../data/r4pe/tigrecave_r4pe.txt',
    '../data/r4pe/tayuntscave_r4pe.txt',  
]


for file_path in file_paths:
    # Reading the file
    df = pd.read_table(file_path)

    # Converting 'date' to datetime
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

    # Group by month and year to calculate monthly averages
    df['month_year'] = df['date'].dt.to_period('M')
    monthly_averages = df.groupby('month_year')['value'].mean().reset_index()

    # Convert 'month_year' to 'MM/YYYY' string format
    monthly_averages['month_year'] = monthly_averages['month_year'].dt.strftime('%m/%Y')

    # Constructing the new file path with '_r4pe_mon' appended and ensuring the extension is .csv
    base_file_path = os.path.splitext(file_path)[0]
    new_file_path = f"{base_file_path}_mon.csv"

    # Save the result to the new file as CSV
    monthly_averages.to_csv(new_file_path, index=False)
    print(f"File saved: {new_file_path}")



#%% 3.2. Create monthly ts for daily precipitation for brdwgd datasets

import pandas as pd
import os

# List of file paths to process
file_paths = [
    '../data/brdwgd/lapagrandecave_brdwgd.txt',
    '../data/brdwgd/paraisocave_brdwgd.txt',
    '../data/brdwgd/tamborilcave_brdwgd.txt',
    '../data/brdwgd/tocadaboavistacave_brdwgd.txt',
    '../data/brdwgd/curupiracave_brdwgd.txt' 
]


for file_path in file_paths:
    # Reading the file
    df = pd.read_table(file_path)

    # Converting 'date' to datetime
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

    # Group by month and year to calculate monthly averages
    df['month_year'] = df['date'].dt.to_period('M')
    monthly_averages = df.groupby('month_year')['value'].mean().reset_index()

    # Convert 'month_year' to 'MM/YYYY' string format
    monthly_averages['month_year'] = monthly_averages['month_year'].dt.strftime('%m/%Y')

    # Constructing the new file path with '_r4pe_mon' appended and ensuring the extension is .csv
    base_file_path = os.path.splitext(file_path)[0]
    new_file_path = f"{base_file_path}_mon.csv"

    # Save the result to the new file as CSV
    monthly_averages.to_csv(new_file_path, index=False)
    print(f"File saved: {new_file_path}")



#%% 3.3. Import the monthly .csv generated _r4pe_mon.csv files and compare

import pandas as pd
import os
import pyleoclim as pyleo

# List of file names to process
file_names = [
    'dinocave_r4pe_mon.csv',
    'tayuntscave_r4pe_mon.csv',
    'shatucacave_r4pe_mon.csv',
    'porvenircave_r4pe_mon.csv',
    'tigrecave_r4pe_mon.csv',
    'tayuntscave_r4pe_mon.csv',  
]

# Directory where the files are located
data_dir = '../data/r4pe/'

def format_label(file_name):
    """Format file name into a proper label."""
    # Remove the suffix and split by "cave"
    name_parts = file_name.split('_')[0].split("cave")
    # Capitalize the first part and reassemble the label
    label = name_parts[0].capitalize() + " cave"
    return label

# Loop through each file name
for file_name in file_names:
    # Construct the full file path
    file_path = data_dir + file_name
    
    # Read the data file
    df = pd.read_csv(file_path)
    
    # Convert date to 'DD/MM/YYYY' format recognizable in Pyleoclim
    df['month_year'] = pd.to_datetime(df['month_year'], format='%m/%Y')
    
    # Convert to "Year CE" as floating-point years correctly
    df['year_ce'] = df['month_year'].dt.year + (df['month_year'].dt.dayofyear - 1) / 365.25

    # Format the label using the helper function
    label = format_label(file_name)

    # Create a Pyleoclim Series object
    ts = pyleo.Series(
        time=df["year_ce"],
        value=df["value"],
        time_name="Date",
        time_unit="days",
        value_name="Rainfall",
        value_unit="mm",
        label=f"Monthly Rainfall {label} 1981-2015 (mm)"
    )
    
    # Plot the series
    ts.plot()



#%% 3.4. Import the monthly .csv generated _brdwgd_mon.csv files and compare

import pandas as pd
import os
import pyleoclim as pyleo

# List of file names to process
file_names = [
    "lapagrandecave_brdwgd_mon.csv",
    "paraisocave_brdwgd_mon.csv",
    "tamborilcave_brdwgd_mon.csv",
    "tocadaboavistacave_brdwgd_mon.csv",
    "curupiracave_brdwgd_mon.csv"
]

# Directory where the files are located
data_dir = '../data/brdwgd/'

def format_label(file_name):
    """Format file name into a proper label."""
    # Remove the suffix and split by "cave"
    name_parts = file_name.split('_')[0].split("cave")
    # Capitalize the first part and reassemble the label
    label = name_parts[0].capitalize() + " cave"
    return label

# Loop through each file name
for file_name in file_names:
    # Construct the full file path
    file_path = data_dir + file_name
    
    # Read the data file
    df = pd.read_csv(file_path)
    
    # Convert date to 'DD/MM/YYYY' format recognizable in Pyleoclim
    df['month_year'] = pd.to_datetime(df['month_year'], format='%m/%Y')
    
    # Convert to "Year CE" as floating-point years correctly
    df['year_ce'] = df['month_year'].dt.year + (df['month_year'].dt.dayofyear - 1) / 365.25

    # Format the label using the helper function
    label = format_label(file_name)

    # Create a Pyleoclim Series object
    ts = pyleo.Series(
        time=df["year_ce"],
        value=df["value"],
        time_name="Date",
        time_unit="days",
        value_name="Rainfall",
        value_unit="mm",
        label=f"Monthly Rainfall {label} 1981-2000 (mm)"
    )
    
    # Plot the series
    ts.plot()







#%% 4. Spectral analysis of the time-series
'''
Section 3. only produces the plot of the individual series, but they are to stored. Here in this section, we clearly create them to be used in the spectral-wavelet analysis 
'''
## 4.1 Individually create the ts daily data for R4PE

def format_label(file_path):
    """Extract and format label from file path."""
    # Extract the file name without extension
    file_name = file_path.split('/')[-1].split('.')[0]
    # Split by '_', take the first part, then split by 'cave'
    parts = file_name.split('_')[0].split("cave")
    # Capitalize and reassemble the name with ' Cave'
    label = parts[0].capitalize() + " cave"
    return f"Daily Rainfall {label} 1981-2015 (mm)"

def read_and_process_file(file_path):
    """Read a data file, process it, and return a pyleo.Series object."""
    df = pd.read_table(file_path)
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
    df['year_ce'] = df['date'].dt.year + (df['date'].dt.dayofyear - 1) / 365.25
    label = format_label(file_path)
    return pyleo.Series(
        time=df["year_ce"],
        value=df["value"],
        time_name="Date",
        time_unit="days",
        value_name="Rainfall",
        value_unit="mm",
        label=label
    )

# File paths for the data files
file_paths = [
    '../data/r4pe/dinocave_r4pe.txt',
    '../data/r4pe/tayuntscave_r4pe.txt',
    '../data/r4pe/shatucacave_r4pe.txt',
    '../data/r4pe/porvenircave_r4pe.txt',
    '../data/r4pe/tigrecave_r4pe.txt',
]

# Manually create a variable for each series
ts_dinocave = read_and_process_file('../data/r4pe/dinocave_r4pe.txt')
ts_tayuntscave = read_and_process_file('../data/r4pe/tayuntscave_r4pe.txt')
ts_shatucacave = read_and_process_file('../data/r4pe/shatucacave_r4pe.txt')
ts_porvenircave = read_and_process_file('../data/r4pe/porvenircave_r4pe.txt')
ts_tigrecave = read_and_process_file('../data/r4pe/tigrecave_r4pe.txt')




## 4.2 Individually create the ts monthly data for R4PE
def format_label(file_path):
    """Extract and format label from file path."""
    # Extract the file name without extension
    file_name = file_path.split('/')[-1].split('.')[0]
    # Split by '_', take the first part, then split by 'cave'
    parts = file_name.split('_')[0].split("cave")
    # Capitalize and reassemble the name with ' Cave'
    label = parts[0].capitalize() + " cave"
    return f"Monthly Rainfall {label} 1981-2015 (mm)"

def read_and_process_file(file_path):
    """Read a data file, process it, and return a pyleo.Series object."""
    df = pd.read_csv(file_path)
    df['month_year'] = pd.to_datetime(df['month_year'], format='%m/%Y')
    df['year_ce'] = df['month_year'].dt.year + (df['month_year'].dt.dayofyear - 1) / 365.25
    label = format_label(file_path)
    return pyleo.Series(
        time=df["year_ce"],
        value=df["value"],
        time_name="Date",
        time_unit="days",
        value_name="Rainfall",
        value_unit="mm",
        label=label
    )

# File paths for the data files
file_paths = [
    '../data/r4pe/dinocave_r4pe_mon.csv',
    '../data/r4pe/tayuntscave_r4pe_mon.csv',
    '../data/r4pe/shatucacave_r4pe_mon.csv',
    '../data/r4pe/porvenircave_r4pe_mon.csv',
    '../data/r4pe/tigrecave_r4pe_mon.csv',
]

# Manually create a variable for each series
tsm_dinocave = read_and_process_file('../data/r4pe/dinocave_r4pe_mon.csv')
tsm_tayuntscave = read_and_process_file('../data/r4pe/tayuntscave_r4pe_mon.csv')
tsm_shatucacave = read_and_process_file('../data/r4pe/shatucacave_r4pe_mon.csv')
tsm_porvenircave = read_and_process_file('../data/r4pe/porvenircave_r4pe_mon.csv')
tsm_tigrecave = read_and_process_file('../data/r4pe/tigrecave_r4pe_mon.csv')




ms = pyleo.MultipleSeries([tsm_tayuntscave,tsm_shatucacave])
ms.standardize().plot()

ms = pyleo.MultipleSeries([tsm_dinocave,tsm_shatucacave])
ms.standardize().plot()




#%%
# Example of using the variables
# ts_dinocave.plot()
# ts_tayuntscave.plot()
# Add plotting or further processing for each variable as needed

ms = pyleo.MultipleSeries([ts_tayuntscave,ts_shatucacave])
ms.standardize().plot()


ms = pyleo.MultipleSeries([ts_dinocave,ts_shatucacave, ts_porvenircave])
ms.standardize().plot()



## 3.2 Create monthly averages

dinobar = pd.read_table('../data/r4pe/dinocave_r4pe.txt')
dinobar.head()

# Step 1: Convert 'date' to datetime
dinobar['date'] = pd.to_datetime(dinobar['date'], format='%d/%m/%Y')

# Step 2: Convert to "Year CE" as floating-point years
dinobar['year_ce'] = dinobar['date'].dt.year + (dinobar['date'].dt.dayofyear - 1) / 365.25
dinobar.head()


ts_dinobar = pyleo.Series(
    time =  dinobar["year_ce"] , 
    value = dinobar["value"],
    time_name = 'Age',
    time_unit = 'Years BP',
    value_name = 'd18O',
    value_unit = 'VPDB',
    label = 'GGD Cave, Ecuador d18Ocalc-5mm res', verbose=False)

ts_dinobar.plot()


ts_dinobar.hist()

ms.stackplot()

ts_dinobar.std()


fig, ax = ts_dinobar.histplot()


fig, ax = cnbts.histplot()
fig, ax = cnbts.stripes(show_xaxis=True)




#%%

'''
2024.04.09

Finished reading SSA052_Khider et al.2022 pyleoclim package. This section I attempt to repdroduce the
paper figures and play with data

'''

df = pd.read_table('..\data\GDD1_d18O_CopraSpline_2mm.txt')
df.head()

ts_gdd = pyleo.Series(time =  df.iloc[:, 0] , value = df.iloc[:, 1], label = 'Dino1 speleothem',
                  time_name = 'Age', value_name = 'd18O',
                  time_unit = 'Years BP',   value_unit = 'VPDB', verbose=False) 


ts_gdd.standardize().detrend().plot()

ts_gdd.wavelet(method='wwz').plot()



wavelet_result = ts_gdd.wavelet(method='wwz')
wavelet_result.plot()


























#%%

# Multiple plots for preliminary visualization
ms = pyleo.MultipleSeries([ts_din2,ts_tang])
ms = pyleo.MultipleSeries([ts_din2,ts_sant])
ms = pyleo.MultipleSeries([ts_din2,ts_tig])
ms = pyleo.MultipleSeries([ts_din2,ts_tigmh])

ms.standardize().plot()
fig, ax = ms.stackplot(linewidth=0.5, fill_between_alpha=0)

coh = ts_tig.wavelet_coherence(ts_din2,method='wwz')
fig, ax = coh.plot()

# Performs significance test
coh_sig = coh.signif_test(number=5)
fig, ax = coh_sig.plot()

# Visualizing the WTC and XWT 
coh_sig.dashboard()

plt.savefig(r'..\results\din_tang_sig5_XWT.png', format='png', dpi=300)
plt.close()








