# LTSPsToServer.py
#
# Created on 05/01/2023
# Written by  Michael Hemming (NSW-IMOS)
# contact email: m.hemming@unsw.edu.au
#
# %% -----------------------------------------------------------------------------------------------
# Determine which computer this script is on

import os
if 'mphem' in os.getcwd():
    account = 'mphem'
else:
    account = 'z3526971'

# %% ------------------------------------------------------------------------------------
# Import Packages

import os
os.chdir('C:\\Users\\' + account + '\\OneDrive - UNSW\\Work\\QC_reports\\Code\\' + 
         'LTSPs\\python-aodntools-master\\')
# Velocity LTSPs
import aodntools.timeseries_products.velocity_aggregated_timeseries as vat
import aodntools.timeseries_products.velocity_hourly_timeseries as vatrly
import aodntools.timeseries_products.velocity_gridded_timeseries_Michael as vatm
# Temp/other LTSPs
import aodntools.timeseries_products.aggregated_timeseries as agg
import aodntools.timeseries_products.hourly_timeseries as hrly
import aodntools.timeseries_products.gridded_timeseries as grid
# other packages
import numpy as np
import numpy.matlib
import requests
import re
import xarray as xr
import psutil
os.chdir('C:\\Users\\' + account + '\\OneDrive - UNSW\\Work\\QC_reports\\Code\\LTSPs\\')
import LTSP_Functions as LTSPFs
import shutil
import netCDF4
import urllib.request as req
import glob

# %% ------------------------------------------------------------------------------------
# define sites

node = 'NSW'
sites = ['BMP070','BMP090','BMP120','SYD140','SYD100','PH100','ORS065','CH050','CH070','CH100']
# sites = ['ORS065','CH050','CH070','CH100']

# %% ------------------------------------------------------------------------------------
# If LTSP directories do not exist create them

def create_LTSP_directories(output_dir):
    Directory_stuff = os.listdir(output_dir)
    if 'aggregated_timeseries' not in str(Directory_stuff):
        os.mkdir(output_dir + 'aggregated_timeseries')
    if 'gridded_timeseries' not in str(Directory_stuff):
        os.mkdir(output_dir + 'gridded_timeseries')
    if 'hourly_timeseries' not in str(Directory_stuff):
        os.mkdir(output_dir + 'hourly_timeseries')

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
             locs.append('https://thredds.aodn.org.au/thredds/fileServer/IMOS/ANMN/NSW/' + site + '/' +
                         str(folder) + '/' + files[n])
     
     return files,locs


def transferLTSPs(node,site,output_dir):
    # aggregated timeseries
    files_agg,locs_agg = getLTSPfilenames(node,site,'aggregated_timeseries')
    print('Transferring aggregated products')
    for nf in range(len(locs_agg)):
        url = ('https://thredds.aodn.org.au/thredds/fileServer/IMOS/ANMN/' + node + '/' + site + 
               '/aggregated_timeseries/' + files_agg[nf])
        try:
            with req.urlopen(url) as d, open((output_dir + 'aggregated_timeseries\\' + files_agg[nf]), "wb") as opfile:
                data = d.read()
                opfile.write(data)
            # urllib.request.urlretrieve(url, (output_dir + 'aggregated_timeseries\\' + files_agg[nf]))
        except:
            print(files_agg[nf] + ': something went wrong .. ')
    # hourly timeseries
    print('Transferring hourly products')
    files_hrly,locs_hrly = getLTSPfilenames(node,site,'hourly_timeseries')
    for nf in range(len(locs_hrly)):
        url = (locs_hrly[nf])
        try:
            with req.urlopen(url) as d, open((output_dir + 'hourly_timeseries\\' + files_hrly[nf]), "wb") as opfile:
                data = d.read()
                opfile.write(data)
            # urllib.request.urlretrieve(url, (output_dir + 'hourly_timeseries\\' + files_hrly[nf]))
        except:
            print(files_hrly[nf] + ': something went wrong .. ')
    # gridded timeseries
    print('Transferring gridded products')
    files_grid,locs_grid = getLTSPfilenames(node,site,'gridded_timeseries')
    for nf in range(len(locs_grid)):
        url = ('https://thredds.aodn.org.au/thredds/fileServer/IMOS/ANMN/' + node + '/' + site + 
               '/gridded_timeseries/' + files_grid[nf])
        try:
            with req.urlopen(url) as d, open((output_dir + 'gridded_timeseries\\' + files_grid[nf]), "wb") as opfile:
                data = d.read()
                opfile.write(data)
            # urllib.request.urlretrieve(url, (output_dir + 'gridded_timeseries\\' + files_grid[nf]))
        except:
            print(files_grid[nf] + ': something went wrong .. ')       
            
# %% ------------------------------------------------------------------------------------
# transfer all LTSPs from thredds to our server          

for nn in range(len(sites)):
    site = sites[nn]
    print(site)
    output_dir = ('Z:\\home\\z3526971\\sci-maths-ocean\\IMOS\\DATA\\MOORINGS\PROCESSED_2_5\\' + site + 
                  '\\LTSPs\\')
    create_LTSP_directories(output_dir)
    # transfer LTSPs from thredds to our server
    transferLTSPs(node,site,output_dir)
    
# %% ------------------------------------------------------------------------------------
# testing whether all files load

for nn in range(len(sites)):
    site = sites[nn]
    output_dir = ('Z:\\home\\z3526971\\sci-maths-ocean\\IMOS\\DATA\\MOORINGS\PROCESSED_2_5\\' + site + 
                  '\\LTSPs\\')
    # check aggregated files
    agg_files = glob.glob(output_dir + 'aggregated_timeseries\\IMOS*.nc')
    for f in agg_files:
        try:
            print(f)
            test = xr.open_dataset(f)
            test.close()
        except:
            print('!!!!!!!!!!!!!!!!!!!!!!!!! file did not open: ' + f + '!!!!!!!!!!!!!!!!!!!!!!!!!!')    
    # check aggregated files
    hrly_files = glob.glob(output_dir + 'hourly_timeseries\\IMOS*.nc')
    for f in hrly_files:
        try:
            print(f)
            test = xr.open_dataset(f)
            test.close()
        except:
            print('!!!!!!!!!!!!!!!!!!!!!!!!! file did not open: ' + f + '!!!!!!!!!!!!!!!!!!!!!!!!!!')    
    # check gridded files
    grid_files = glob.glob(output_dir + 'gridded_timeseries\\IMOS*.nc')
    for f in grid_files:
        try:
            print(f)
            test = xr.open_dataset(f)
            test.close()
        except:
            print('!!!!!!!!!!!!!!!!!!!!!!!!! file did not open: ' + f + '!!!!!!!!!!!!!!!!!!!!!!!!!!')         
            
            
            

# %% ------------------------------------------------------------------------------------
# 

 # output_dir = ('Z:\\home\\z3526971\\sci-maths-ocean\\IMOS\\DATA\\MOORINGS\PROCESSED_2_5\\' + sites[nn] + 
 #               '\\LTSPs\\')
 
 
 # url = ('https://thredds.aodn.org.au/thredds/fileServer/IMOS/ANMN/NSW/BMP070/aggregated_timeseries/IMOS_ANMN-NSW_TZ_20141118_BMP070_FV01_TEMP-aggregated-timeseries_END-20220913_C-20221213.nc')
 # dataset = netCDF4.Dataset(url)
 # dataset.
 
 
# Issue with BMP070 velocity aggregated product, doesn't load ...
# same for hourly products too (various sites).. But works when using file downlaoded from internet ..
#
# SYD140
# IMOS_ANMN-NSW_STZ_20080625_SYD140_FV02_hourly-timeseries_END-20220920_C-20221213.nc: something went wrong .. 
# SYD100
# IMOS_ANMN-NSW_VZ_20080625_SYD100_FV01_velocity-aggregated-timeseries_END-20221017_C-20221213.nc: something went wrong .. 



 
 
 
 
 
 
 
 