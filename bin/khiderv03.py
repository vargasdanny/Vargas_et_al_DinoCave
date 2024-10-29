# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 10:33:35 2024

Check https://linked.earth/paleoTS/ PaleoTS

"""

import pyleoclim as pyleo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
#os.chdir('C:/Users/danny/OneDrive/IKER Speleothems/Dino Spelo/bin')
os.chdir('C:/Users/danny/OneDrive - Universidad Politecnica Salesiana/Research/EGU2024/GDD_cave/bin')
print("Current Working Directory:", os.getcwd())


#%% 
'''
=============================================
1. Extract climatology from .nc files
=============================================

Daily value from RAIN4PE_daily_0.1d_1981_2015_v1.0.nc. using cdo are save as .txt. 
Then, monthly sum and climatology are saved as xxx_r4pe_mon.csv & xxx_r4pe_mon_climatology.xls

'''

import os
import subprocess
import pandas as pd

# Define the list of locations with names, latitudes, and longitudes
locations = [
    {"name": "ecsf", "lat": -3.971667, "lon": -79.079167},
    {"name": "laipuna", "lat": -4.2, "lon": -79.883},
    {"name": "huagapo", "lat": -4.2, "lon": -79.883},
    
    
    
]

# Define the directory paths and filenames
source_directory_path = '/mnt/c/Users/danny/"OneDrive - Universidad Politecnica Salesiana"/Research/RAIN4PE'
destination_directory_path = 'C:/Users/danny/OneDrive/IKER Speleothems/Dino Spelo/data/r4pe'
input_filename = "RAIN4PE_daily_0.1d_1981_2015_v1.0.nc"

# Ensure the destination directory exists
os.makedirs(destination_directory_path, exist_ok=True)

climatology_paths = []  # List to store paths of climatology files for later merging

for location in locations:
    name = location["name"]
    lon = location["lon"]
    lat = location["lat"]
    
    # Construct CDO commands and filenames
    output_nc_filename = f"{name}.nc"
    output_txt_filename = f"{name}.txt"
    cleaned_txt_filename = f"{name}_r4pe.txt"
    
    remap_command = f'cd {source_directory_path} && cdo remapnn,lon={lon}_lat={lat} {input_filename} {output_nc_filename}'
    export_command = f'cd {source_directory_path} && cdo outputtab,date,lon,lat,value {output_nc_filename} > {output_txt_filename}'
    
    # Execute CDO commands
    try:
        subprocess.run(["wsl", "bash", "-c", remap_command], check=True, capture_output=True, text=True)
        subprocess.run(["wsl", "bash", "-c", export_command], check=True, capture_output=True, text=True)
        print(f"CDO commands executed successfully for {name}.")
    except subprocess.CalledProcessError as e:
        print(f"Error running CDO command for {name}: {e.stderr}")
    
    # Process and save daily data
    original_file_path = os.path.join(source_directory_path.replace('/mnt/c', 'C:').replace('"', ''), output_txt_filename)
    new_file_path = os.path.join(destination_directory_path, cleaned_txt_filename)
    
    # Read and clean data
    with open(original_file_path, 'r') as file:
        lines = file.readlines()[:-1]
    with open(new_file_path, 'w') as new_file:
        for line in lines:
            new_file.write(line)
    
    # Format and save cleaned data
    df = pd.read_csv(new_file_path, delim_whitespace=True, header=None, skiprows=1, names=['date', 'lon', 'lat', 'value'])
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%d/%m/%Y')
    df.to_csv(new_file_path, sep='\t', index=False, header=True)
    print(f"Processed data and {cleaned_txt_filename} has been created in {destination_directory_path}.")

    # Create monthly time series for daily precipitation
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
    df['month_year'] = df['date'].dt.to_period('M')
    monthly_totals = df.groupby('month_year')['value'].sum().reset_index()
    monthly_totals['month_year'] = monthly_totals['month_year'].dt.strftime('%m/%Y')
    
    monthly_file_path = os.path.splitext(new_file_path)[0] + '_mon.csv'
    monthly_totals.to_csv(monthly_file_path, index=False)
    print(f"Monthly time series saved: {monthly_file_path}")

    # Calculate the total monthly precipitation for each month in each year
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    monthly_totals = df.groupby(['year', 'month'])['value'].sum().reset_index()

    # Calculate the climatology by averaging the total monthly precipitation across all years
    monthly_climatology = monthly_totals.groupby('month')['value'].mean().reset_index()
    monthly_climatology.columns = ['Month', 'Average Monthly Precipitation (mm/month)']

    # Save the climatology to CSV
    climatology_file_path = os.path.splitext(monthly_file_path)[0] + '_climatology.csv'
    monthly_climatology.to_csv(climatology_file_path, index=False)
    print(f"Climatology saved: {climatology_file_path}")
    
    climatology_paths.append(climatology_file_path)

# Merge all climatology data into one Excel file
all_climatology_data = {location['name']: pd.read_csv(path).set_index('Month') for location, path in zip(locations, climatology_paths)}
combined_climatology = pd.concat(all_climatology_data.values(), axis=1)
combined_climatology.columns = [location['name'] for location in locations]  # Set column headers as location names
combined_excel_path = os.path.join(destination_directory_path, 'combined_climatology.xlsx')
combined_climatology.to_excel(combined_excel_path)
print(f"All climatology data has been combined into one Excel file: {combined_excel_path}")


#%% 

'''
=============================================
2. Load the records
=============================================

'''
## Garganta del Dino cave, Ecuador
din2 = pd.read_table('..\data\GDD1_d18O_CopraSpline_2mm.txt')
ts_din2 = pyleo.Series(
    time =  din2.iloc[:, 0] , 
    value = din2.iloc[:, 1],
    time_name = 'Age',
    time_unit = 'Years BP',
    value_name = 'd18O',
    value_unit = 'VPDB',
    label = 'GDD Cave', verbose=False)

din5 = pd.read_table('..\data\GDD1_d18O_CopraSpline_5mm.txt')
ts_din5 = pyleo.Series(
    time =  din5.iloc[:, 0] , 
    value = din5.iloc[:, 1],
    time_name = 'Age',
    time_unit = 'Years BP',
    value_name = 'd18O',
    value_unit = 'VPDB',
    label = 'GGD Cave-5mm', verbose=False)

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
    label="Santiago Cave")

## Bond events: North Atlantic Holocene Drift Ice Proxy Data
bond = pd.read_table(r'..\data\bond2001b.txt', comment='#')
bond.head()
ts_bond = pyleo.Series(
    time=bond["age"],
    value=bond["HSG"],
    time_name="Age",
    time_unit="years BP",
    value_name="HSG",
    value_unit="%",
    label="VM29-191")

## Cariaco Basin, Venezuela
cariaco = pd.read_table(r'..\data\cariaco_ti.txt', comment='#')
cariaco.head()
ts_cariaco = pyleo.Series(
    time=cariaco["Age"],
    value=cariaco["Ti"],
    time_name="Age",
    time_unit="years BP",
    value_name="Ti",
    value_unit="%",
    label="Cariaco Basin")

## Alfredo-Jahn Cave, Venezuela
veaj = pd.read_csv(r'..\data\veaj.tab', delimiter="\t")
veaj.head()
ts_veaj = pyleo.Series(
    time=veaj.iloc[:, 5]*1000,
    value=veaj.iloc[:, 7],
    time_name="Age",
    time_unit="years BP",
    value_name="d18O",
    value_unit="permil",
    label="Alfredo Jahn Cave")

ts_veaj.plot(color="C1", invert_yaxis=True)

## Pallcacocha Lake, Ecuador
pall = pd.read_table(r'..\data\pallca_3.7-12.4ka.txt')
pall.head()
ts_pall = pyleo.Series(
    time=pall.iloc[:, 0],
    value=pall.iloc[:, 1],
    time_name="Age",
    time_unit="years BP",
    value_name="GrayScale",
    value_unit="%",
    label="Pallcacocha Lake")

## Shatuka cave, Peru
shatuca = pd.read_table(r'..\data\shatuka.txt', comment='#')
shatuca.head()
ts_shatuca = pyleo.Series(
    time=shatuca.iloc[:,0],
    value=shatuca.iloc[:,1],
    time_name="Age",
    time_unit="years BP",
    value_name="d18O",
    value_unit="permil",
    label="Shatuca cave")

ts_shatuca.plot()


## El Condor cave, Peru (Condor A+B)
condor = pd.read_table(r'..\data\condor_ab.txt', comment='#')
condor.head()
ts_condor = pyleo.Series(
    time=condor["age_calkaBP"]*1000,
    value=condor["d18OcarbVPDB"],
    time_name="Age",
    time_unit="years BP",
    value_name="d18O",
    value_unit="permil",
    label="Condor cave")

ts_condor.plot()


## Pacupahuain cave, Peru
pacupa = pd.read_csv(r'..\data\pacupahuain2012.csv')
pacupa.head()
ts_pacupa = pyleo.Series(
    time=pacupa["Age (BP 1950)"],
    value=pacupa["d18O (per mil)"],
    time_name="Age",
    time_unit="years BP",
    value_name="d18O",
    value_unit="permil",
    label="Pacupahuain cave")

ts_pacupa.plot()





## Huascaran Glacier, Peru
huas = read_table(r'..\data\huas.txt')
















## Other tropical records
## Tangga cave, Indonesia 2024.03.16
tang = pd.read_table(r'..\data\tangga2018d18o.txt', comment='#')
tang.head()

ts_tang = pyleo.Series(
    time=tang["age_calkaBP"]*1000,
    value=tang["d18O-raw"],
    time_name="Age",
    time_unit="years BP",
    value_name="d18O",
    value_unit="per mil",
    label="Tangga Cave")

ts_tang.plot(color="C1", invert_yaxis=False)
fig, ax = ts_tang.histplot()




## Heinrich events (H)



## Dansgaard/Oeschger (D/O)





### Brief comparison
ms = pyleo.MultipleSeries([ts_sant,ts_pacupa])
ms.standardize().plot()

coh = ts_pacupa.wavelet_coherence(ts_sant,method='wwz')
coh.plot()


# Performs significance test
coh_sig = coh.signif_test(number=5)
coh_sig.plot()

# Visualizing the WTC and XWT 
coh_sig.dashboard(title="Pacupahuain vs Santiago caves", overlap=False)

plt.savefig(r'..\results\pacu_sant_sig5.png', format='png', dpi=300)
plt.close()








#%%
'''
=============================================
3. Spectral analysis
=============================================

'''
## From Climatch https://comptools.climatematch.io/tutorials/W1D4_Paleoclimate/student/W1D4_Tutorial6.html# 
fig, ax = plt.subplots()
# basic periodogram
ts_sant.interp(step=0.5).standardize().spectral(method="periodogram").plot(
    ax=ax, xlim=[1000, 5], ylim=[0.001, 1000], label="Periodogram")
# Welch's periodogram
ts_sant.interp(step=0.5).standardize().spectral(method="welch").plot(
    ax=ax, xlim=[1000, 5], ylim=[0.001, 1000], label="Welch")
# Multi-taper Method
ts_sant.interp(step=0.5).standardize().spectral(method="mtm").plot(
    ax=ax, xlim=[1000, 5], ylim=[0.001, 1000], label="MTM")
# Lomb-Scargle periodogram
ts_sant.standardize().spectral(method="lomb_scargle").plot(
    ax=ax, xlim=[1000, 5], ylim=[0.001, 1000], label="Lomb Scargle")
# weighted wavelet Z-transform (WWZ)
ts_sant.standardize().spectral(method="wwz").plot(
    ax=ax, xlim=[1000, 5], ylim=[0.001, 1000], label="WWZ")

















import matplotlib.pyplot as plt

# Define your time series variable here
time_series = ts_sant  # Change ts_sant to any other time series as needed
#x_limits = [20000, 0]
y_limits = [0.01, 10000]

fig, ax = plt.subplots()
# Basic periodogram
time_series.interp(step=0.5).standardize().spectral(method="periodogram").plot(
    ax=ax, ylim=y_limits, label="Periodogram")
# Welch's periodogram
time_series.interp(step=0.5).standardize().spectral(method="welch").plot(
    ax=ax, ylim=y_limits, label="Welch")
# Multi-taper Method
time_series.interp(step=0.5).standardize().spectral(method="mtm").plot(
    ax=ax, ylim=y_limits, label="MTM")
# Lomb-Scargle periodogram
time_series.standardize().spectral(method="lomb_scargle").plot(
    ax=ax, ylim=y_limits, label="Lomb Scargle")
# Weighted wavelet Z-transform (WWZ)
time_series.standardize().spectral(method="wwz").plot(
    ax=ax, ylim=y_limits, label="WWZ")

# Display the legend and show the plot
ax.legend()
plt.show()





ts = pyleo.utils.load_dataset('SOI')

fig, ax = ts_sant.plot()
fig, ax = ts_sant.histplot()

ts_sant.plot()
ts_sant.histplot(bin_method='scott')



#----------------
## Histogram
#----------------
fig, ax = ts_din2.histplot()

## Histogram with Scott's rule
time_series = ts_sant 

# Extracting data and label from the time series object
data = time_series.value  # Assuming the time series data is stored in .value
label = time_series.label  # Assuming the time series label is stored in .label
# Convert data to a NumPy array and ensure type is float for numerical computations
data = np.array(data, dtype=float)
# Calculate bin width using Scott's Rule manually
std_dev = np.std(data)  # Standard deviation of the data
n = len(data)  # Number of observations
bin_width = 3.49 * std_dev * (n ** (-1/3))  # Scott's formula for bin width
# Determine the range of data and calculate the number of bins
data_range = np.max(data) - np.min(data)
bins = np.round(data_range / bin_width)
# Plotting the histogram
fig, ax = plt.subplots()
ax.hist(data, bins=int(bins), edgecolor='w')
ax.set_title(f'Histogram {label} Scott\'s Rule')
plt.show()


ts_sant.spectral(method='wwz').plot()




























ms = pyleo.MultipleSeries([ts_sant,ts_bond])
ms = pyleo.MultipleSeries([ts_din5,ts_bond])
ms = pyleo.MultipleSeries([ts_din2,ts_bond])
ms.standardize().plot()

coh = ts_bond.wavelet_coherence(ts_sant,method='wwz')
coh = ts_bond.wavelet_coherence(ts_din5,method='wwz')
coh = ts_bond.wavelet_coherence(ts_din2,method='wwz')
fig, ax = coh.plot()

# Performs significance test
coh_sig = coh.signif_test(number=100)
fig, ax = coh_sig.plot()

# Visualizing the WTC and XWT 
coh_sig.dashboard()

plt.savefig(r'..\results\bond_ggd_sig100_WT.png', format='png', dpi=300)
plt.close()

### EGU 2024
#Slice a time series
ts_condor_slice = ts_condor.slice([0,10000])
ts_sant_slice = ts_sant.slice([0,10000])
ts_tang_slice = ts_tang.slice([0,10000])
ts_bond_slice = ts_bond.slice([4000,7000])


ts_list = [ts_bond, ts_cariaco, ts_veaj, ts_pall, ts_din2, ts_shatuca, ts_condor_slice]
ms_sa = pyleo.MultipleSeries(ts_list, label="NSA Speleothems")
ms_sa.standardize().plot(xlim=[5000, 7000])
ms_sa.stackplot()

ms_sa.common_time(method="interp", step=0.5).standardize().stackplot()

plt.savefig(r'..\results\stack01.png', format='png', dpi=300)
plt.close()

#Now assign a common tim
#sa_ct = ms_sa.common_time(method="interp", step=0.5).standardize()
#sa_ct.stackplot()


mh01 = pyleo.MultipleSeries([ts_bond_slice, ts_din5, ts_din2])
mh01.standardize().stackplot()



#For inverting the bond time series yaxis in stackplot
fig, axs = mh01.stackplot()
if axs is not None:  # Check if the axes are accessible
    axs[0].invert_yaxis()  # Invert the y-axis of the first subplot
    plt.show()  # Show the plot with the modified axis
else:
    print("Axis objects are not accessible.")



ms.stackplot(xlim=[4000, 12000])




#stack02
ms = pyleo.MultipleSeries([ts_condor_slice, ts_shatuca, ts_sant_slice, ts_din5, ts_tang_slice]) #colors=["b", "g"]
ms.standardize().plot()

plt.savefig(r'..\results\stack02.png', format='png', dpi=300)
plt.close()

#Stackplot
ms.stackplot()
ms.stackplot(xlim=[4000, 12000])







##SPECTROGRAM
#ts_sant.standardize().spectral().signif_test(qs=[0.90,0.95,0.99]).plot()
ts_sant.standardize().spectral().signif_test(number=1000, qs=[0.90,0.95,0.99]).plot()
plt.savefig(r'..\results\ts_sant_spec01.png', format='png', dpi=300)
plt.close()

ts_sant.standardize().spectral(method='wwz').signif_test(number=10, qs=[0.90,0.95,0.99]).plot()


#Raw vs detrended
fig,ax = ts_sant.standardize().spectral().plot(label = 'No trend removal')
ts_sant.detrend().standardize().spectral().plot(ax=ax,label='detrended')

fig,ax = ts_din2.standardize().spectral().plot(label = 'No trend removal')
ts_din2.detrend().standardize().spectral().plot(ax=ax,label='detrended')



# Lomb-Scargle periodogram
fig,ax = ts_sant_ls_sd = ts_sant.standardize().spectral(method="lomb_scargle").plot(label = 'No trend removal LScargle')
ts_sant_ls_sd = ts_sant.detrend().standardize().spectral(method="lomb_scargle").plot(ax=ax,label = 'Detrended LScargle')

fig,ax = ts_din2.standardize().spectral(method="wwz").plot(label = 'No trend removal')
ts_din2.detrend().standardize().spectral(method="wwz").plot(ax=ax,label='detrended')




#Wavelet
scal = ts_sant.wavelet(method='wwz')
scal.plot()

scal_sig = scal.signif_test(method='ar1asym')
scal_sig.plot()


#%% Climamatch EXPERIMENTS

#Full wavelet https://comptools.climatematch.io/tutorials/W1D4_Paleoclimate/student/W1D4_Tutorial6.html

#01.Significance
ts_sant_ls_sd = ts_sant.standardize().spectral(method="lomb_scargle")
ts_sant_ls_sd.sig = ts_sant_ls_sd.signif_test()

#02.Scalogram
scal = ts_sant.standardize().wavelet(method="wwz")

#03.Wavelet & Amplitude
ts_sant.summary_plot(
    psd=ts_sant_ls_sd.sig, scalogram=scal, psd_label="Amplitude")


plt.savefig(r'..\results\sant_wavelet.png', format='png', dpi=300)
plt.close()

#%% Detrending santiago

#01.Significance
ts_sant_ls_sd = ts_sant.detrend().standardize().spectral(method="lomb_scargle")
ts_sant_ls_sd.sig = ts_sant_ls_sd.signif_test()

#02.Scalogram
scal = ts_sant.detrend().standardize().wavelet(method="wwz")

#03.Wavelet & Amplitude
ts_sant.summary_plot(
    psd=ts_sant_ls_sd.sig, scalogram=scal, psd_label="Amplitude")


plt.savefig(r'..\results\sant_detrend.wavelet.png', format='png', dpi=300)
plt.close()



#%% Wavelet coherence with Bond Santiago

coh = ts_sant.wavelet_coherence(ts_bond,method='wwz')
fig, ax = coh.plot()

coh_sig = coh.signif_test(number=5)

coh_sig.dashboard()
plt.savefig(r'..\results\sant_coh.png', format='png', dpi=300)
plt.close()

#%% Coherence Bond-Dino2

coh = ts_din2.wavelet_coherence(ts_bond,method='wwz')
fig, ax = coh.plot()

coh_sig = coh.signif_test(number=5)

coh_sig.dashboard()
plt.savefig(r'..\results\din2_coh.png', format='png', dpi=300)
plt.close()






#%%
coh = ts_din5.wavelet_coherence(ts_bond,method='wwz')
fig, ax = coh.plot()

coh_sig = coh.signif_test(number=5)

coh_sig.dashboard()
plt.savefig(r'..\results\din5_coh.png', format='png', dpi=300)
plt.close()


#%%

######################################################
To be revised
ts_tang.plot(color="C1", invert_yaxis=True)



#invert
# Assuming ts1 and ts2 are two Series objects
coh = ts1.wavelet_coherence(ts2).invert_yaxis (bool, optional)

# Plot coherence and get the figure and axes array
fig, ax = coh.plot()

# You might have multiple axes depending on the plot
# Here's how you might invert the y-axis on the first subplot
ax[0].invert_yaxis()  # Adjust index based on which subplot you need to alter

# Show the plot
plt.show()



ts_tig.plot(color="C1", invert_yaxis=False)





##♣
# List of time series pairs to work with
time_series_pairs = [
#    (ts_sant, ts_bond),
#    (ts_din5, ts_din2),
#    (ts_din2, ts_bond)
#    (ts_din2, ts_sant)
    (ts_bond, ts_din2)
]

# Function to create and plot MultipleSeries
def plot_multiple_series(ts_list):
    ms = pyleo.MultipleSeries(ts_list)
    ms.standardize().plot()

# Function to calculate and plot wavelet coherence
def plot_wavelet_coherence(ts1, ts2, method='wwz'):
    coh = ts1.wavelet_coherence(ts2, method=method)
    fig, ax = coh.plot()
    return fig, ax

# Loop through pairs and apply functions
for ts1, ts2 in time_series_pairs:
    plot_multiple_series([ts1, ts2])  # Plot each pair as a MultipleSeries
    plot_wavelet_coherence(ts2, ts1)  # Calculate and plot coherence


























#%% Wavelet analysis for Santiago and the orbital tunning (main frequencies as in SSA052_Khider et al.2022)

##♥copied

#From Climatch https://comptools.climatematch.io/tutorials/W1D4_Paleoclimate/student/W1D4_Tutorial6.html# 
fig, ax = plt.subplots()
# basic periodogram
ts_sant.interp(step=0.5).standardize().spectral(method="periodogram").plot(
    ax=ax, xlim=[1000, 5], ylim=[0.001, 1000], label="Periodogram")
# Welch's periodogram
ts_sant.interp(step=0.5).standardize().spectral(method="welch").plot(
    ax=ax, xlim=[1000, 5], ylim=[0.001, 1000], label="Welch")
# Multi-taper Method
ts_sant.interp(step=0.5).standardize().spectral(method="mtm").plot(
    ax=ax, xlim=[1000, 5], ylim=[0.001, 1000], label="MTM")
# Lomb-Scargle periodogram
ts_sant.standardize().spectral(method="lomb_scargle").plot(
    ax=ax, xlim=[1000, 5], ylim=[0.001, 1000], label="Lomb Scargle")
# weighted wavelet Z-transform (WWZ)
ts_sant.standardize().spectral(method="wwz").plot(
    ax=ax, xlim=[1000, 5], ylim=[0.001, 1000], label="WWZ")

##copied



#Estimate spectral density

# Lomb-Scargle periodogram
ts_sant_ls_sig = ts_sant.spectral(method="lomb_scargle").signif_test().plot(xlabel="Period [years]")                             #Raw data
ts_sant_std_ls_sig = ts_sant.standardize().spectral(method="lomb_scargle").signif_test().plot(xlabel="Period [years]")           #Standardize data


tsraw = ts_sant.spectral(method="lomb_scargle")
tsraw_sig = tsraw.signif_test()

fig, ax = plt.subplots()
ax.plot(tsraw_sig.frequency, tsraw_sig.amplitude)
#ax.set_xlim([0.000, 0.001])
#ax.set_ylim([0, 200])
ax.set_xlabel("Frequency [1/yr]")
ax.set_ylabel("Spectra Amplitude")



ts = ts_sant.standardize().spectral(method="lomb_scargle")
ts_sig = ts.signif_test()

fig, ax = plt.subplots()
ax.plot(ts_sig.frequency, ts_sig.amplitude)
#ax.set_xlim([0.000, 0.001])
#ax.set_ylim([0, 200])
ax.set_xlabel("Frequency [1/yr]")
ax.set_ylabel("Spectra Amplitude")









# create a scalogram
scal = ts_sant.standardize().wavelet(method='wwz')

# make plot
ts_sant.summary_plot(psd=tsraw_sig, scalogram=scal, psd_label="Amplitude")

ts_sant.summary_plot(psd=tsraw_sig, scalogram=scal, time_lim=[0, 60000], psd_label="Amplitude")










