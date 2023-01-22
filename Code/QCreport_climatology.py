#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Thu Jan 12 11:57:03 2023
# Contributers (code):  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# Contributers (review): Moninya Roughan (NSW-IMS), Tim Austin (NSW-IMOS), Stuart Milburn (NSW-IMOS) 
# contact email: m.hemming@unsw.edu.au

# %% -----------------------------------------------------------------------------------------------
# Import packages
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

import xarray as xr
import numpy as np
import matplotlib
matplotlib.use('qt5Agg')
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import glob
import re
import requests
import datetime
# QCreport modules
import QCreport_paths as paths
import QCreport_format as form
import QCreport_DeploymentDetails as DepDet
import QCreport_QualityControl as QCR
import QCreport_DeploymentPhotographs as DepPhoto
import QCreport_ToolboxPlots as tbp
import QCreport_setup as setup
import QCreport_cover as cover
import QCreport_AdditionalPlots as Addp

# %% -----------------------------------------------------------------------------------------------
# Function to get LTSP filename
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

def getLTSPfilenames(node,site,folder):
     res = requests.get(
         'https://thredds.aodn.org.au/thredds/catalog/IMOS/ANMN/' + node + '/' + site + '/' + str(folder) + '/catalog.html')
     txt = res.text
     # identify file names
     start_file = []
     end_file = []
     files = []
     # get start and end locations of file names in text
     for m in re.finditer('IMOS_ANMN-NSW', txt):
         start_file.append(m.start())
     for m in re.finditer(r'\b.nc\b', txt): # r'\b .. \b is used for exact phrase
         end_file.append(m.end())  
     # get file names
     for n_file in range(len(start_file)):
         files.append(txt[start_file[n_file]:end_file[n_file]])       

     # Only use unique file names
     files = np.unique(files)
     locs = []
     for n in range(len(files)):
             locs.append('https://thredds.aodn.org.au/thredds/dodsC/IMOS/ANMN/NSW/' + site + '/' +
                         str(folder) + '/' + files[n])
     
     return files,locs
 
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________


# %% -----------------------------------------------------------------------------------------------
# Load LTSP for the site, determine depths to compare
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# get temperature LTSP filename
files = glob.glob(paths.TEMPORARY_dir + '*.nc');
for f in files:
    if 'TEMP-aggregated-timeseries' in f:
        file2use = f


# Load the gridded LTSP available on thredds
# _,file_loc = getLTSPfilenames('NSW',setup.site_name,'gridded_timeseries')
agg_TEMP = xr.open_dataset(file2use,cache=False).load()
agg_T = agg_TEMP.TEMP.values; 
agg_T_QC = agg_TEMP.TEMP_quality_control.values; 
agg_D = agg_TEMP.DEPTH.values;
agg_D_QC = agg_TEMP.DEPTH_quality_control.values; 
agg_t = agg_TEMP.TIME.values;
# use 'good' data only
c = np.logical_and(agg_T_QC != 1,
                   agg_D_QC != 1)
agg_T[c] = np.nan
agg_D[c] = np.nan

# agg_D = np.tile(agg_TEMP.DEPTH.values,[len(agg_TEMP.TIME),1]).flatten(); 
# agg_t = np.tile(agg_TEMP.TIME.values,[len(agg_TEMP.DEPTH),1]).transpose().flatten(); 

# get nominal depths, time, temp and depth of deployment files
IMOS_files = DepDet.attributes_TEMP.files_list
NDs = []
Ds = []
Ts = []
ts = []

for f in IMOS_files:
    NDs.append(xr.open_dataset(f).instrument_nominal_depth)
    D = xr.open_dataset(f).DEPTH.values;
    D_QC = xr.open_dataset(f).DEPTH_quality_control.values;
    D[D_QC != 1] = np.nan
    t = xr.open_dataset(f).TIME.values;
    T = xr.open_dataset(f).TEMP.values;
    T_QC = xr.open_dataset(f).TEMP_quality_control.values;
    T[T_QC != 1] = np.nan
    Ds.append(D)
    Ts.append(T)
    ts.append(t)
    
# get actual depth range for these deployment files
D_range = []
for n in range(len(NDs)):
    D_range.append(np.round([np.percentile(Ds[n][np.isfinite(Ds[n])],5), 
              np.percentile(Ds[n][np.isfinite(Ds[n])],95)],2))
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________



# %% -----------------------------------------------------------------------------------------------
# Create timeseries figure
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

for n in range(len(NDs)):
    
    plt.figure(figsize=(10,5))
    
    # plot the historical record for this depth range
    c = np.logical_and(agg_D >= D_range[n][0],
                       agg_D < D_range[n][1])
    plt.scatter(agg_t[c],agg_T[c],2,label='Historical')
    # plot the deployment
    plt.scatter(ts[n],Ts[n],2,label='This Deployment')
    # appearance
    plt.legend(loc='lower left',fontsize=14,ncol=2)
    plt.show()
    plt.grid()
    plt.ylabel('Temperature [$^\circ$C]',fontsize=16)
    plt.title('Deployment: ' + setup.deployment_file_date_identifier + ', Nominal Depth: ' +
              str(NDs[n]) +' m, depth range: ' + str(D_range[n][0]) + ' - ' + str(D_range[n][1]) + 
              ' m',fontsize=16)
    # Set the font size for the tick labels
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    if np.nanmax(ts[n]) > np.nanmax(agg_t):
        plt.xlim(np.nanmin(agg_t)-np.timedelta64(365,'D'),np.nanmax(ts[n])+np.timedelta64(365,'D'))
    else:
        plt.xlim(np.nanmin(agg_t)-np.timedelta64(365,'D'),np.nanmax(agg_t)+np.timedelta64(365,'D'))
        
    # save figures
    filename = (paths.plots_dir + 'TimeSeries\\TEMP_' + setup.site_name + '_' + setup.deployment_file_date_identifier + '_D' + 
                    str(NDs[n]) + '.png')
    plt.savefig(filename)
    plt.close()
    
    

# %% -----------------------------------------------------------------------------------------------
# Create climatology figures
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# use data subsets as aggregated data set too large
agg_t = agg_t[0::10]
agg_T = agg_T[0::10]
agg_D = agg_D[0::10]

# get gridded date elements and year day 
date_string = np.datetime_as_string(agg_t,unit='s') # convert datetime64 to string format
date_elements = []
yearday = []
for nt in range(len(date_string)):
    date_elements.append(datetime.datetime.strptime(date_string[nt], "%Y-%m-%dT%H:%M:%S"))
    y = date_elements[nt].year
    m = date_elements[nt].month
    d = date_elements[nt].day
    yearday.append(datetime.datetime(y,m,d).timetuple().tm_yday)
# get deployment date elements and year day 

date_string = np.datetime_as_string(agg_t,unit='s') # convert datetime64 to string format
date_elements = []
yearday = []
for nt in range(len(date_string)):
    date_elements.append(datetime.datetime.strptime(date_string[nt], "%Y-%m-%dT%H:%M:%S"))
    y = date_elements[nt].year
    m = date_elements[nt].month
    d = date_elements[nt].day
    yearday.append(datetime.datetime(y,m,d).timetuple().tm_yday)
    
for n in range(len(NDs)):
    
    plt.figure(figsize=(10,5))

    
    # plot the historical record for this depth range
    c = np.logical_and(agg_D >= D_range[n][0],
                       agg_D < D_range[n][1])
    plt.scatter(np.array(yearday)[c],agg_T[c],2,label='Historical')
    # plot the deployment
    # get yearday per depth level
    date_elements_dep = []
    yearday_dep = []
    for nt in range(len(ts[n])):
        date_elements_dep.append(datetime.datetime.strptime(np.datetime_as_string(ts[n][nt],unit='s'), "%Y-%m-%dT%H:%M:%S"))
        y = date_elements_dep[nt].year
        m = date_elements_dep[nt].month
        d = date_elements_dep[nt].day
        yearday_dep.append(datetime.datetime(y,m,d).timetuple().tm_yday)
    
    plt.scatter(yearday_dep,Ts[n],2,label='This Deployment')
    # appearance
    plt.legend(loc='lower left',fontsize=14,ncol=2)
    plt.show()
    plt.grid()
    plt.ylabel('Temperature [$^\circ$C]',fontsize=16)
    plt.title('Deployment: ' + setup.deployment_file_date_identifier + ', Nominal Depth: ' +
              str(NDs[n]) +' m, depth range: ' + str(D_range[n][0]) + ' - ' + str(D_range[n][1]) + 
              ' m',fontsize=16)
    # Set the font size for the tick labels
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    # format x ticks to show the months instead of yearday
    month_fmt = mdates.DateFormatter('%b')
    ax = plt.gca()
    ax.xaxis.set_major_formatter(month_fmt)
    # save figures
    filename = (paths.plots_dir + 'Climatology\\TEMP_climatology_' + setup.site_name + '_' + setup.deployment_file_date_identifier + '_D' + 
                    str(NDs[n]) + '.png')
    plt.savefig(filename)
    plt.close()
    
    
    
    
    
    
