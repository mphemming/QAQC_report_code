##################################

####################################################################


# Script: QCreport_PlotDepthDistribution.py
# Created: 13 Dec 2022 by Michael Hemming (NSW-IMOS)

# using Python version 3.9, Spyder (managed using Anaconda)

######################################################################################################################

##################################

# %% -----------------------------------------------------------
# Importing packages

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import requests
import re
import matplotlib as mpl
import os

# %% -----------------------------------------------------------------------------------------------
# Determine which computer this script is on

if 'mphem' in os.getcwd():
    account = 'mphem'
else:
    account = 'z3526971'
    
# %% -----------------------------------------------------------
# function to scrape file names for thredds folder

# Make a request to https://codedamn-classrooms.github.io/webscraper-python-codedamn-classroom-website/
# Store the result in 'res' variable
# site = 'CH100'
# data_type = 'aggregated_timeseries'

def get_thredds_filenames(site,data_type):
    # scrape thredds server
    res = requests.get(
        'https://thredds.aodn.org.au/thredds/catalog/IMOS/ANMN/NSW/' + site + '/' + data_type + '/catalog.html')
    txt = res.text
    # identify file names
    start_file = []
    end_file = []
    files = []
    # get start and end locations of file names in text
    for m in re.finditer('IMOS_ANMN-NSW', txt):
        start_file.append(m.start())
    for m in re.finditer('.nc', txt):
        end_file.append(m.end())  
    # get file names
    for n_file in range(len(start_file)):
        files.append(txt[start_file[n_file]:end_file[n_file]])
    # Only use unique file names
    files = np.unique(files)
    locs = []
    for n in range(len(files)):
            locs.append('https://thredds.aodn.org.au/thredds/dodsC/IMOS/ANMN/NSW/' + site + '/' +
                        data_type + '/' + files[n])
        
    return files,locs
    

def get_LTSPs(site):
    _,locs = get_thredds_filenames(site,'aggregated_timeseries')
    site_LTSPs = []
    for nf in locs:
        try:
            site_LTSPs.append(xr.open_dataset(nf))
        except:
            print(nf + ' -----> cannot be read and written (null)')
    return site_LTSPs


def add_box(n0,bins,color_txt):
    
    if np.sum(np.diff(bins) > 20) < 1:
        # add box if no major vertical gaps
        plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*bins[0],color_txt,linewidth=3)
        plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*bins[-1],color_txt,linewidth=3)
        plt.plot(np.ones(np.size(bins))*n0,bins,color_txt,linewidth=3)
        plt.plot(np.ones(np.size(bins))*n0+1,bins,color_txt,linewidth=3) 
    else:
        # add boxes if major vertical gaps
        f = np.int32(np.squeeze(np.where(np.diff(bins) > 20)))
        # first box
        plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*bins[0],color_txt,linewidth=3)
        plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*bins[f],color_txt,linewidth=3)
        plt.plot(np.ones(np.size(bins[0:f]))*n0,bins[0:f],color_txt,linewidth=3)
        plt.plot(np.ones(np.size(bins[0:f]))*n0+1,bins[0:f],color_txt,linewidth=3) 
        # second box
        plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*bins[f+1],color_txt,linewidth=3)
        plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*bins[-1],color_txt,linewidth=3)
        plt.plot(np.ones(np.size(bins[f+1::]))*n0,bins[f+1::],color_txt,linewidth=3)
        plt.plot(np.ones(np.size(bins[f+1::]))*n0+1,bins[f+1::],color_txt,linewidth=3) 


# %% -----------------------------------------------------------
# load in LTSPs for each site

# CH
CH050 = get_LTSPs('CH050')
CH070 = get_LTSPs('CH070')
CH100 = get_LTSPs('CH100')

# SYD
SYD100 = get_LTSPs('SYD100')
SYD140 = get_LTSPs('SYD140')
PH100 = get_LTSPs('PH100')
# ORS
ORS065_TEMP = xr.open_dataset('C:\\Users\\' + account + '\\OneDrive - UNSW\\Work\\MooringsData_2023\\' +
                         'MooringsData_2023\\Data\\Raw_data\\IMOS_ANMN-NSW_TZ_20060502_' +
                         'ORS065_FV01_TEMP-aggregated-timeseries_END-20220110_C-20220718.nc')
ORS065_Vel = xr.open_dataset('C:\\Users\\' + account + '\\OneDrive - UNSW\\Work\\MooringsData_2023\\' +
                         'MooringsData_2023\\Data\\Raw_data\\IMOS_ANMN-NSW_' + 
                         'VZ_20060502_ORS065_FV01_velocity-aggregated-timeseries_END-20211109_C-20221219.nc')

# BMP
BMP070 = get_LTSPs('BMP070')
BMP090 = get_LTSPs('BMP090')
BMP120 = get_LTSPs('BMP120')


# load PH100, and ORS065 buoy temperature data

# MAI (not focused on this site)
# direct = 'C:\\Users\\mphem\\OneDrive - UNSW\\Work\\Climatology\\Data\\Raw_data\\MAI_surface\\'
# files = os.listdir(direct);
# dfiles = []
# MAI_S_D = []
# for nf in range(len(files)):
#     dfiles.append(xr.open_dataset(direct + files[nf]).SSTI);
#     D = np.array(dfiles[nf]); D[D > 25] = np.nan; D[D < 5] = np.nan;
#     D[np.isfinite(D)] = 0.6;
#     MAI_S_D.append(D)
# MAI_S_D = np.concatenate(MAI_S_D)
#
direct = ('C:\\Users\\' + account + '\\OneDrive - UNSW\\Work\\Climatology\\Data\\Raw_data\\PH100_Surface_Temp\\')
files = os.listdir(direct); files = files[5:11]
dfiles = []
PH100_S_D = []
for nf in range(len(files)):
    dfiles.append(xr.open_dataset(direct + files[nf]).TEMP);
    QC = np.array(xr.open_dataset(direct + files[nf]).TEMP_quality_control);
    D = np.array(dfiles[nf]); D[QC > 2] = np.nan;
    D[np.isfinite(D)] = 0.6;
    PH100_S_D.append(D)
PH100_S_D = np.concatenate(PH100_S_D)

# ORS
direct = 'C:\\Users\\mphem\\OneDrive - UNSW\\Work\\Climatology\\Data\\Raw_data\\ORS_Buoy_TEMP\\'
files = os.listdir(direct); files = files[12::]
dfiles = []
ORS_S_D = []
for nf in range(len(files)):
    dfiles.append(xr.open_dataset(direct + files[nf]).TEMP);
    D = np.array(dfiles[nf]);
    # D[np.isfinite(D)] = 0.6;
    ORS_S_D.append(D)
ORS_S_D = np.concatenate(ORS_S_D)
ORS_S_D[ORS_S_D > 27] = np.nan
ORS_S_D[ORS_S_D < 15.3] = np.nan
ORS_S_D[206000:208500] = np.nan
ORS_S_D[np.isfinite(ORS_S_D)] = 0.6;

# %% -----------------------------------------------------------
# Average bottom depth for each site

# Did this manually using histograms 

# %% -----------------------------------------------------------
# get histograms of data sets (using depth)

# temperature

# CH050
ds = CH050[0]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.TEMP_quality_control > 2] = np.nan
hist = np.histogram(D[np.isfinite(D)],bins=range(0,70,1))
c=[hist[0] > 0]
bins = hist[1][0:-1]+0.5

class CH050_b:
    T_bins = bins[c]
    T = hist[0][c]

del ds, D, hist, c, bins

# CH070
# temperature
ds = CH070[0]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.TEMP_quality_control > 2] = np.nan
T_hist = np.histogram(D[np.isfinite(D)],bins=range(0,100,1))
cT=[T_hist[0] > 0]
bins = T_hist[1][0:-1]+0.5
# vel
ds = CH070[1]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.VCUR_quality_control > 2] = np.nan
V_hist = np.histogram(D[np.isfinite(D)],bins=range(0,100,1))
cV=[V_hist[0] > 0]
bins = V_hist[1][0:-1]+0.5


class CH070_b:
    T_bins = bins[cT]
    V_bins = bins[cV]
    T = T_hist[0][cT]
    V = V_hist[0][cV]

del ds, D, T_hist, V_hist, cV, cT, bins


# CH100
# temperature
ds = CH100[1]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.TEMP_quality_control > 2] = np.nan
T_hist = np.histogram(D[np.isfinite(D)],bins=range(0,120,1))
cT=[T_hist[0] > 0]
T_bins = T_hist[1][0:-1]+0.5
# PSAL
ds = CH100[0]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.PSAL_quality_control > 2] = np.nan
S_hist = np.histogram(D[np.isfinite(D)],bins=range(0,120,1))
cS=[S_hist[0] > 0]
S_bins = S_hist[1][0:-1]+0.5
# vel
ds = CH100[2]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.VCUR_quality_control > 2] = np.nan
V_hist = np.histogram(D[np.isfinite(D)],bins=range(0,120,1))
cV=[V_hist[0] > 0]
V_bins = V_hist[1][0:-1]+0.5


class CH100_b:
    T_bins = T_bins[cT]
    S_bins = S_bins[cS]
    V_bins = V_bins[cV]
    T = T_hist[0][cT]
    S = S_hist[0][cS]
    V = V_hist[0][cV]

del ds, D, T_hist, S_hist, V_hist, cV, cS, cT, T_bins, S_bins, V_bins

# ORS065
# temperature
ds = ORS065_TEMP; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.TEMP_quality_control > 2] = np.nan
D = np.concatenate((D,ORS_S_D))
T_hist = np.histogram(D[np.isfinite(D)],bins=range(0,160,1))
cT=[T_hist[0] > 0]
T_bins = T_hist[1][0:-1]+0.5
# vel 
ds = ORS065_Vel; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
V_hist = np.histogram(D[np.isfinite(D)],bins=range(0,120,1))
cV=[V_hist[0] > 0]
V_bins = V_hist[1][0:-1]+0.5

class ORS065_b:
    T_bins = T_bins[cT]
    V_bins = V_bins[cV]
    T = T_hist[0][cT]
    V = V_hist[0][cV]

del ds, D, T_hist, cT, T_bins

# SYD100
# temperature
ds = SYD100[7]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.TEMP_quality_control > 2] = np.nan
T_hist = np.histogram(D[np.isfinite(D)],bins=range(0,160,1))
cT=[T_hist[0] > 0]
T_bins = T_hist[1][0:-1]+0.5
# PSAL
ds = SYD100[6]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.PSAL_quality_control > 2] = np.nan
S_hist = np.histogram(D[np.isfinite(D)],bins=range(0,160,1))
cS=[S_hist[0] > 0]
S_bins = S_hist[1][0:-1]+0.5
# vel
ds = SYD100[9]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.VCUR_quality_control > 2] = np.nan
V_hist = np.histogram(D[np.isfinite(D)],bins=range(0,160,1))
cV=[V_hist[0] > 0]
V_bins = V_hist[1][0:-1]+0.5
# Oxygen ([3,4,5] have same results)
ds = SYD100[5]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.DOX2_quality_control > 2] = np.nan
O2_hist = np.histogram(D[np.isfinite(D)],bins=range(0,160,1))
cO2=[O2_hist[0] > 0]
O2_bins = O2_hist[1][0:-1]+0.5
# CPHL
ds = SYD100[1]; D1 = np.array(ds.DEPTH);
D1[ds.DEPTH_quality_control > 2] = np.nan
D1[ds.CHLU_quality_control > 2] = np.nan
ds = SYD100[2]; D2 = np.array(ds.DEPTH);
D2[ds.DEPTH_quality_control > 2] = np.nan
D2[ds.CPHL_quality_control > 2] = np.nan
D = np.concatenate([D1,D2])
CPHL_hist = np.histogram(D[np.isfinite(D)],bins=range(0,160,1))
cCPHL=[CPHL_hist[0] > 0]
CPHL_bins = CPHL_hist[1][0:-1]+0.5

class SYD100_b:
    T_bins = T_bins[cT]
    S_bins = S_bins[cS]
    V_bins = V_bins[cV]
    O2_bins = O2_bins[cO2]
    CPHL_bins = CPHL_bins[cCPHL]
    T = T_hist[0][cT]
    S = S_hist[0][cS]
    V = V_hist[0][cV]
    O2 = O2_hist[0][cO2]
    CPHL = CPHL_hist[0][cCPHL]

del ds, D, T_hist, S_hist, V_hist, O2_hist, CPHL_hist, cV, cS, cT, cO2, cCPHL, T_bins, S_bins, V_bins, O2_bins, CPHL_bins

# SYD140
# temperature
ds = SYD140[1]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.TEMP_quality_control > 2] = np.nan
T_hist = np.histogram(D[np.isfinite(D)],bins=range(0,160,1))
cT=[T_hist[0] > 0]
T_bins = T_hist[1][0:-1]+0.5
# PSAL
ds = SYD140[0]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.PSAL_quality_control > 2] = np.nan
S_hist = np.histogram(D[np.isfinite(D)],bins=range(0,160,1))
cS=[S_hist[0] > 0]
S_bins = S_hist[1][0:-1]+0.5
# vel
ds = SYD140[2]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.VCUR_quality_control > 2] = np.nan
V_hist = np.histogram(D[np.isfinite(D)],bins=range(0,160,1))
cV=[V_hist[0] > 0]
V_bins = V_hist[1][0:-1]+0.5

class SYD140_b:
    T_bins = T_bins[cT]
    S_bins = S_bins[cS]
    V_bins = V_bins[cV]
    T = T_hist[0][cT]
    S = S_hist[0][cS]
    V = V_hist[0][cV]

del ds, D, T_hist, S_hist, V_hist, cV, cS, cT, T_bins, S_bins, V_bins

# PH100
# temperature
ds = PH100[9]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.TEMP_quality_control > 2] = np.nan
D = np.concatenate((D,PH100_S_D))
T_hist = np.histogram(D[np.isfinite(D)],bins=range(0,160,1))
cT=[T_hist[0] > 0]
T_bins = T_hist[1][0:-1]+0.5
# PSAL
ds = PH100[8]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.PSAL_quality_control > 2] = np.nan
S_hist = np.histogram(D[np.isfinite(D)],bins=range(0,160,1))
cS=[S_hist[0] > 0]
S_bins = S_hist[1][0:-1]+0.5
# vel
ds = PH100[11]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.VCUR_quality_control > 2] = np.nan
V_hist = np.histogram(D[np.isfinite(D)],bins=range(0,160,1))
cV=[V_hist[0] > 0]
V_bins = V_hist[1][0:-1]+0.5
# Oxygen ([3,4,5] have same results)
ds = PH100[5]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.DOX2_quality_control > 2] = np.nan
O2_hist = np.histogram(D[np.isfinite(D)],bins=range(0,160,1))
cO2=[O2_hist[0] > 0]
O2_bins = O2_hist[1][0:-1]+0.5
# CPHL
ds = PH100[0]; D1 = np.array(ds.DEPTH);
D1[ds.DEPTH_quality_control > 2] = np.nan
D1[ds.CPHL_quality_control > 2] = np.nan
ds = PH100[1]; D2 = np.array(ds.DEPTH);
D2[ds.DEPTH_quality_control > 2] = np.nan
D2[ds.CHLF_quality_control > 2] = np.nan
ds = PH100[2]; D3 = np.array(ds.DEPTH);
D3[ds.DEPTH_quality_control > 2] = np.nan
D3[ds.CHLU_quality_control > 2] = np.nan
D = np.concatenate([D1,D2,D3])
CPHL_hist = np.histogram(D[np.isfinite(D)],bins=range(0,160,1))
cCPHL=[CPHL_hist[0] > 0]
CPHL_bins = CPHL_hist[1][0:-1]+0.5

class PH100_b:
    T_bins = T_bins[cT]
    S_bins = S_bins[cS]
    V_bins = V_bins[cV]
    O2_bins = O2_bins[cO2]
    CPHL_bins = CPHL_bins[cCPHL]
    T = T_hist[0][cT]
    S = S_hist[0][cS]
    V = V_hist[0][cV]
    O2 = O2_hist[0][cO2]
    CPHL = CPHL_hist[0][cCPHL]

del ds, D, T_hist, S_hist, V_hist, O2_hist, CPHL_hist, cV, cS, cT, cO2, cCPHL, T_bins, S_bins, V_bins, O2_bins, CPHL_bins

# BMP070
# temperature
ds = BMP070[0]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.TEMP_quality_control > 2] = np.nan
T_hist = np.histogram(D[np.isfinite(D)],bins=range(0,160,1))
cT=[T_hist[0] > 0]
T_bins = T_hist[1][0:-1]+0.5
# vel
ds = BMP070[1]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.VCUR_quality_control > 2] = np.nan
V_hist = np.histogram(D[np.isfinite(D)],bins=range(0,160,1))
cV=[V_hist[0] > 0]
V_bins = V_hist[1][0:-1]+0.5

class BMP070_b:
    T_bins = T_bins[cT]
    V_bins = V_bins[cV]
    T = T_hist[0][cT]
    V = V_hist[0][cV]

del ds, D, T_hist, V_hist, cV, cT, T_bins, V_bins

# BMP090
# temperature
ds = BMP090[0]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.TEMP_quality_control > 2] = np.nan
T_hist = np.histogram(D[np.isfinite(D)],bins=range(0,160,1))
cT=[T_hist[0] > 0]
T_bins = T_hist[1][0:-1]+0.5
# vel
ds = BMP090[1]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.VCUR_quality_control > 2] = np.nan
V_hist = np.histogram(D[np.isfinite(D)],bins=range(0,160,1))
cV=[V_hist[0] > 0]
V_bins = V_hist[1][0:-1]+0.5

class BMP090_b:
    T_bins = T_bins[cT]
    V_bins = V_bins[cV]
    T = T_hist[0][cT]
    V = V_hist[0][cV]

del ds, D, T_hist, V_hist, cV, cT, T_bins, V_bins


# BM120
# temperature
ds = BMP120[1]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.TEMP_quality_control > 2] = np.nan
T_hist = np.histogram(D[np.isfinite(D)],bins=range(0,160,1))
cT=[T_hist[0] > 0]
T_bins = T_hist[1][0:-1]+0.5
# PSAL
ds = BMP120[0]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.PSAL_quality_control > 2] = np.nan
S_hist = np.histogram(D[np.isfinite(D)],bins=range(0,160,1))
cS=[S_hist[0] > 0]
S_bins = S_hist[1][0:-1]+0.5
# vel
ds = BMP120[2]; D = np.array(ds.DEPTH);
D[ds.DEPTH_quality_control > 2] = np.nan
D[ds.VCUR_quality_control > 2] = np.nan
V_hist = np.histogram(D[np.isfinite(D)],bins=range(0,160,1))
cV=[V_hist[0] > 0]
V_bins = V_hist[1][0:-1]+0.5

class BMP120_b:
    T_bins = T_bins[cT]
    V_bins = V_bins[cV]
    S_bins = S_bins[cS]
    T = T_hist[0][cT]
    V = V_hist[0][cV]
    S = S_hist[0][cS]

del ds, D, T_hist, V_hist, S_hist, cV, cT, cS, T_bins, V_bins, S_bins

# %% -----------------------------------------------------------
# create figure

######################################
############################################################################
# THIS IS INCLUDING DATA WITH MULTIPLE SAMPLING RATES
############################################################################
######################################

# define colormap
cvO = mpl.colormaps['Greys']

# From north to south

plt.figure(figsize=(14,8))
########################################################################
# CH100
# TEMP
cv = cvO(np.linspace(0, 1, np.nanmax(CH100_b.T)))
n0 = 0
for n in range(len(CH100_b.T_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(CH100_b.T_bins[n]),
             c = cv[CH100_b.T[n]-1],linewidth=2)
add_box(n0,CH100_b.T_bins,'b')     
    
# PSAL
cv = cvO(np.linspace(0, 1, np.nanmax(CH100_b.S)))
n0 = 1.5
for n in range(len(CH100_b.S_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(CH100_b.S_bins[n]),
             c = cv[CH100_b.S[n]-1],linewidth=2)    
add_box(n0,CH100_b.S_bins,'orange') 
     
# Vel
cv = cvO(np.linspace(0, 1, np.nanmax(CH100_b.V)))
n0 = 3
for n in range(len(CH100_b.V_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(CH100_b.V_bins[n]),
             c = cv[CH100_b.V[n]-1],linewidth=2)
add_box(n0,CH100_b.V_bins,'brown')  


# vertical split line
plt.plot(np.ones(np.size(np.arange(0,150,1)))*4.5,np.arange(0,150,1),'k')

########################################################################
# CH070
# TEMP
cv = cvO(np.linspace(0, 1, np.nanmax(CH070_b.T)))
n0 = 5
for n in range(len(CH070_b.T_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(CH070_b.T_bins[n]),
             c = cv[CH070_b.T[n]-1],linewidth=2)
add_box(n0,CH070_b.T_bins,'b')    
    
# Vel
cv = cvO(np.linspace(0, 1, np.nanmax(CH070_b.V)))
n0 = 6.5
for n in range(len(CH070_b.V_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(CH070_b.V_bins[n]),
             c = cv[CH070_b.V[n]-1],linewidth=2)
add_box(n0,CH070_b.V_bins,'brown')

# vertical split line
plt.plot(np.ones(np.size(np.arange(0,150,1)))*8,np.arange(0,150,1),'k')

########################################################################
# CH050
cv = cvO(np.linspace(0, 1, np.nanmax(CH050_b.T)))
n0 = 8.5;
for n in range(len(CH050_b.T_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(CH050_b.T_bins[n]),
             c = cv[CH050_b.T[n]-1],linewidth=2)
add_box(n0,CH050_b.T_bins,'b')

# vertical split line
plt.plot(np.ones(np.size(np.arange(0,150,1)))*10,np.arange(0,150,1),'k') 

########################################################################
# ORS065
# TEMP
cv = cvO(np.linspace(0, 1, np.nanmax(ORS065_b.T)))
n0 = 10.5
for n in range(len(ORS065_b.T_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(ORS065_b.T_bins[n]),
             c = cv[ORS065_b.T[n]-1],linewidth=2)
add_box(n0,ORS065_b.T_bins,'b')     
#Vel
cv = cvO(np.linspace(0, 1, np.nanmax(ORS065_b.V)))
n0 = 12
for n in range(len(ORS065_b.V_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(ORS065_b.V_bins[n]),
              c = cv[ORS065_b.V[n]-1],linewidth=2)
add_box(n0,ORS065_b.V_bins,'brown')  


# vertical split line
plt.plot(np.ones(np.size(np.arange(0,150,1)))*13.5,np.arange(0,150,1),'k')

########################################################################
# SYD100
# TEMP
cv = cvO(np.linspace(0, 1, np.nanmax(SYD100_b.T)))
n0 = 14
for n in range(len(SYD100_b.T_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(SYD100_b.T_bins[n]),
             c = cv[SYD100_b.T[n]-1],linewidth=2)
add_box(n0,SYD100_b.T_bins,'b')     
    
# PSAL
cv = cvO(np.linspace(0, 1, np.nanmax(SYD100_b.S)))
n0 = 15.5
for n in range(len(SYD100_b.S_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(SYD100_b.S_bins[n]),
             c = cv[SYD100_b.S[n]-1],linewidth=2)    
add_box(n0,SYD100_b.S_bins,'orange') 
     
# Vel
cv = cvO(np.linspace(0, 1, np.nanmax(SYD100_b.V)))
n0 = 17
for n in range(len(SYD100_b.V_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(SYD100_b.V_bins[n]),
             c = cv[SYD100_b.V[n]-1],linewidth=2)
add_box(n0,SYD100_b.V_bins,'brown')  

# O2
cv = cvO(np.linspace(0, 1, np.nanmax(SYD100_b.O2)))
n0 = 18.5
for n in range(len(SYD100_b.O2_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(SYD100_b.O2_bins[n]),
             c = cv[SYD100_b.O2[n]-1],linewidth=2)
add_box(n0,SYD100_b.O2_bins,'lightblue')  

# CPHL
cv = cvO(np.linspace(0, 1, np.nanmax(SYD100_b.CPHL)))
n0 = 20
for n in range(len(SYD100_b.CPHL_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(SYD100_b.CPHL_bins[n]),
             c = cv[SYD100_b.CPHL[n]-1],linewidth=2)
add_box(n0,SYD100_b.CPHL_bins,'green')  

# vertical split line
plt.plot(np.ones(np.size(np.arange(0,150,1)))*22,np.arange(0,150,1),'k')

# add legend
plt.plot(np.arange(-1,-2,1),np.arange(-1,-2,1),'b',linewidth=2,label='Temperature')
plt.plot(np.arange(-1,-2,1),np.arange(-1,-2,1),'orange',linewidth=2,label='Salinity')
plt.plot(np.arange(-1,-2,1),np.arange(-1,-2,1),'brown',linewidth=2,label='Velocity')
plt.plot(np.arange(-1,-2,1),np.arange(-1,-2,1),'lightblue',linewidth=2,label='Dissolved Oxygen')
plt.plot(np.arange(-1,-2,1),np.arange(-1,-2,1),'green',linewidth=2,label='Chlorophyll-a Fluorescence')
plt.legend(loc='lower left')

########################################################################
# SYD140
# TEMP
cv = cvO(np.linspace(0, 1, np.nanmax(SYD140_b.T)))
n0 = 22.5
for n in range(len(SYD140_b.T_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(SYD140_b.T_bins[n]),
             c = cv[SYD140_b.T[n]-1],linewidth=2)
add_box(n0,SYD140_b.T_bins,'b')     
    
# PSAL
cv = cvO(np.linspace(0, 1, np.nanmax(SYD140_b.S)))
n0 = 24
for n in range(len(SYD140_b.S_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(SYD140_b.S_bins[n]),
             c = cv[SYD140_b.S[n]-1],linewidth=2)    
add_box(n0,SYD140_b.S_bins,'orange') 
     
# Vel
cv = cvO(np.linspace(0, 1, np.nanmax(SYD140_b.V)))
n0 = 25.5
for n in range(len(SYD140_b.V_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(SYD140_b.V_bins[n]),
             c = cv[SYD140_b.V[n]-1],linewidth=2)
add_box(n0,SYD140_b.V_bins,'brown')  

# vertical split line
plt.plot(np.ones(np.size(np.arange(0,150,1)))*27,np.arange(0,150,1),'k')

########################################################################
# PH100
# TEMP
cv = cvO(np.linspace(0, 1, np.nanmax(PH100_b.T)))
n0 = 27.5
for n in range(len(PH100_b.T_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(PH100_b.T_bins[n]),
             c = cv[PH100_b.T[n]-1],linewidth=2)
add_box(n0,PH100_b.T_bins,'b')     
    
# PSAL
cv = cvO(np.linspace(0, 1, np.nanmax(PH100_b.S)))
n0 = 29
for n in range(len(PH100_b.S_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(PH100_b.S_bins[n]),
             c = cv[PH100_b.S[n]-1],linewidth=2)    
add_box(n0,PH100_b.S_bins,'orange') 
     
# Vel
cv = cvO(np.linspace(0, 1, np.nanmax(PH100_b.V)))
n0 = 30.5
for n in range(len(PH100_b.V_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(PH100_b.V_bins[n]),
             c = cv[PH100_b.V[n]-1],linewidth=2)
add_box(n0,PH100_b.V_bins,'brown')  

# O2
cv = cvO(np.linspace(0, 1, np.nanmax(PH100_b.O2)))
n0 = 32
for n in range(len(PH100_b.O2_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(PH100_b.O2_bins[n]),
             c = cv[PH100_b.O2[n]-1],linewidth=2)
add_box(n0,PH100_b.O2_bins,'lightblue')  

# CPHL
cv = cvO(np.linspace(0, 1, np.nanmax(PH100_b.CPHL)))
n0 = 33.5
for n in range(len(PH100_b.CPHL_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(PH100_b.CPHL_bins[n]),
             c = cv[PH100_b.CPHL[n]-1],linewidth=2)
add_box(n0,PH100_b.CPHL_bins,'green')  

# vertical split line
plt.plot(np.ones(np.size(np.arange(0,150,1)))*35,np.arange(0,150,1),'k')

########################################################################
# BMP070
# TEMP
cv = cvO(np.linspace(0, 1, np.nanmax(BMP070_b.T)))
n0 = 35.5
for n in range(len(BMP070_b.T_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(BMP070_b.T_bins[n]),
             c = cv[BMP070_b.T[n]-1],linewidth=2)
add_box(n0,BMP070_b.T_bins,'b')     
     
# Vel
cv = cvO(np.linspace(0, 1, np.nanmax(BMP070_b.V)))
n0 = 37
for n in range(len(BMP070_b.V_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(BMP070_b.V_bins[n]),
             c = cv[BMP070_b.V[n]-1],linewidth=2)
add_box(n0,BMP070_b.V_bins,'brown')  

# vertical split line
plt.plot(np.ones(np.size(np.arange(0,150,1)))*38.5,np.arange(0,150,1),'k')

########################################################################
# BMP090
# TEMP
cv = cvO(np.linspace(0, 1, np.nanmax(BMP090_b.T)))
n0 = 39
for n in range(len(BMP090_b.T_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(BMP090_b.T_bins[n]),
             c = cv[BMP090_b.T[n]-1],linewidth=2)
add_box(n0,BMP090_b.T_bins,'b')     
     
# Vel
cv = cvO(np.linspace(0, 1, np.nanmax(BMP090_b.V)))
n0 = 40.5
for n in range(len(BMP090_b.V_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(BMP090_b.V_bins[n]),
             c = cv[BMP090_b.V[n]-1],linewidth=2)
add_box(n0,BMP090_b.V_bins,'brown')  

# vertical split line
plt.plot(np.ones(np.size(np.arange(0,150,1)))*42,np.arange(0,150,1),'k')

########################################################################
# BMP120
# TEMP
cv = cvO(np.linspace(0, 1, np.nanmax(BMP120_b.T)))
n0 = 42.5
for n in range(len(BMP120_b.T_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(BMP120_b.T_bins[n]),
             c = cv[BMP120_b.T[n]-1],linewidth=2)
add_box(n0,BMP120_b.T_bins,'b')     
    
# PSAL
cv = cvO(np.linspace(0, 1, np.nanmax(BMP120_b.S)))
n0 = 44
for n in range(len(BMP120_b.S_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(BMP120_b.S_bins[n]),
             c = cv[BMP120_b.S[n]-1],linewidth=2)    
add_box(n0,BMP120_b.S_bins,'orange') 
     
# Vel
cv = cvO(np.linspace(0, 1, np.nanmax(BMP120_b.V)))
n0 = 45.5
for n in range(len(BMP120_b.V_bins)):
    plt.plot(np.arange(n0,n0+1,0.1),np.ones(np.size(np.arange(n0,n0+1,0.1)))*np.float(BMP120_b.V_bins[n]),
             c = cv[BMP120_b.V[n]-1],linewidth=2)
add_box(n0,BMP120_b.V_bins,'brown')  



# other figure things
plt.rcParams.update({'font.size': 14})
plt.xlim([-1, 47]); plt.ylim([0,150])
# plt.grid('on')
ax = plt.gca()
ax.invert_yaxis()

x = [2,6.25,9,11.75,17.5,24.5,31,36.75,40.25,44.5]
labels = ['CH100','CH070','CH050','ORS065','SYD100','SYD140','PH100','BMP070','BMP090','BMP120']
plt.xticks(x, labels, rotation =45,fontsize=16)

plt.ylabel('Depth [m]',fontsize=20)

# %% save figure

plt.savefig('C:\\Users\\mphem\\OneDrive - UNSW\\Work\\MooringsData_2023\\MooringsData_2023\\Output\\Plots\\' + 
            'Figure_MooringDataDepths.png', dpi=300);  
plt.close()

