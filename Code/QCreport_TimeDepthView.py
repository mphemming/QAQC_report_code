#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created Mon Jan 16 14:40:23 2023
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
import re
import requests
# QCreport modules
import QCreport_paths as paths
import QCreport_DeploymentDetails as DepDet
import QCreport_setup as setup
import importlib
importlib.reload(setup) # needed for creating multiple reports in a loop
import glob
import QCreport_netCDF as nc

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
# Get LTSP and mooring data at the site
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________


# files,locs = getLTSPfilenames('NSW',setup.site_name,'aggregated_timeseries')
# for l in locs:
#     if 'TEMP' in l:
#         t = xr.open_dataset(l).TIME.values
#         D = xr.open_dataset(l).DEPTH.values
#         D_QC = xr.open_dataset(l).DEPTH_quality_control.values

# get temperature and vel LTSP filename
files = glob.glob(paths.TEMPORARY_dir + '*.nc');
for f in files:
    if 'TEMP-aggregated-timeseries' in f:
        file2use = f
t = xr.open_dataset(file2use).TIME.values
D = xr.open_dataset(file2use).DEPTH.values
D_QC = xr.open_dataset(file2use).DEPTH_quality_control.values
T_QC = xr.open_dataset(file2use).TEMP_quality_control.values
D[D_QC != 1] = np.nan
D[T_QC != 1] = np.nan

# get depths during deployment
c = np.logical_and(t > np.datetime64(DepDet.attributes_TEMP().time_coverage_start[0])+np.timedelta64(3,'D'),
                   t < np.datetime64(DepDet.attributes_TEMP().time_coverage_end[0])-np.timedelta64(3,'D'))


# # define mooring files (TEMP files only)    
# IMOS_f = DepDet.atts_files_list
# IMOS_files = {}
# for n in range(len(IMOS_f)):
#     IMOS_f_string = str(IMOS_f[n])
#     if IMOS_f_string.find('TEMPERATURE') > 0:
#         IMOS_files[n] = IMOS_f[n]
        
# # get time and depth from selected deployment
# Mt = []; Md = []; Md_QC = []
# for n in range(len(IMOS_files)):
#       Mt.append(xr.open_dataset(IMOS_files[n][0]).TIME) 
#       Md.append(xr.open_dataset(IMOS_files[n][0]).DEPTH)   
#       Md_QC.append(xr.open_dataset(IMOS_files[n][0]).DEPTH_quality_control)  
      
# Mt = np.concatenate(Mt)        
# Md = np.concatenate(Md)         
# Md_QC = np.concatenate(Md_QC)

# Md[Md_QC != 1] = np.nan    

Mt=t[c]; Md = D[c]

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
        
# %% -----------------------------------------------------------------------------------------------
# Create figure
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

plt.figure(figsize=(12,8))

plt.scatter(t[0::10],D[0::10],1,label='Historical')
plt.scatter(Mt[0::10],Md[0::10],1,label='Deployment')

# appearance
plt.legend(loc='lower left',fontsize=14,ncol=2)
plt.show()
plt.grid()
ax = plt.gca(); ax.invert_yaxis()
plt.ylabel('Depth [m]',fontsize=16)
plt.title('Deployment ' + setup.deployment_file_date_identifier +
          ' historical Depth comparison',fontsize=16)
# Set the font size for the tick labels
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

 
# save figures
filename = (paths.plots_dir + 'TimeSeries\\TEMP_DEPTH_' + setup.site_name + '_' + 
            setup.deployment_file_date_identifier + '.png')
plt.savefig(filename)
plt.close()

 
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

