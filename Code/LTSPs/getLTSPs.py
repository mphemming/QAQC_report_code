#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Thu July  28 10:21 2022
# Contributers (code):  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# Contributers (review): Moninya Roughan (NSW-IMS), Tim Austin (NSW-IMOS), Stuart Milburn (NSW-IMOS), Neil Malan (NSW-IMOS) 
# contact email: m.hemming@unsw.edu.au

# What does this script do?

# o   gets Long Time-Series Products (LTSPs), aggregated, hourly and gridded, TEMP and VEL, 
#     for each site as per data available in 'sci-maths-ocean\IMOS\DATA\MOORINGS\PROCESSED_2_5\'

# Instructions:

# o   TBC

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% Import Packages
#----------------------------------------------------------------------------
# change directory to aodntools where scripts are stored
import os
os.chdir('C:\\Users\\mphem\\OneDrive - UNSW\\Work\\QC_reports\\Code\\' + 
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

# %% Define sites and variables required for LTSPs (must mirror folder names in data folder)
#----------------------------------------------------------------------------

# sites = ['BMP070','BMP090','BMP120','CH050','CH070','CH100','ORS065','PH100','SYD100','SYD140'];

sites = ['ORS065_Original']

# variables = ['TEMP','CURR','PSAL','DOX2','CPHL']
variables = ['CURR']

user = 'z3526971'

time_range = [np.datetime64('2020-01-01'),np.datetime64('2023-01-01')]
# time_range = [] # if want all data

# %% get file names for each site
#----------------------------------------------------------------------------

#############################################################################
#############################################################################
#############################################################################

# Function to get file names

def get_files(mooring_dir,site_code,var,time_start,time_end):
    #######################################################################################
    # time_start   Use np.datetime64 or '' if no start limit
    # time_end   Use np.datetime64 or '' if no end limit
    #######################################################################################
    # Includes the files that has data within this range, but does not slice the file.
    # So aggregated product will not exactly have the input time range
    #######################################################################################
    path = mooring_dir + '\\' + site_code + '\\' + var + '\\' # need double '\'
    files = os.listdir(path)
    #######################################################################################
    # remove non-netCDF formats
    for n in range(len(files)):
        if '.nc' not in files[n]:
            files[n] = []
    # remove all empty slots
    files = [ele for ele in files if ele != []]
    #######################################################################################
    start_dates = []
    end_dates = []
    # remove files outside of time range
    if 'datetime64' in str(type(time_start)):
        for n in range(len(files)):
            ###############################################
            # get start and end date of file
            f = files[n]
            # Identify all underscores in filename to get dates
            underscore_index = [nn for nn in range(len(f)) if f.find('_', nn) == nn]
            start_date = f[underscore_index[2]+1:underscore_index[3]-1]
            end_date = f[underscore_index[6]+5:underscore_index[7]-1]
            # convert to numpy datetime64
            start_date = np.datetime64(start_date[0:4] + '-' + start_date[4:6] 
                                       + '-' + start_date[6:8])
            end_date = np.datetime64(end_date[0:4] + '-' + end_date[4:6] 
                                       + '-' + end_date[6:8])
            start_dates.append(start_date)
            end_dates.append(end_date)
            ###############################################
            # if no input for time_start and time_end, get earliest date
            if '-' not in str(time_start):
                time_start = np.datetime64('2008-01-01')
            if '-' not in str(time_end):
                time_end = np.datetime64('2030-01-01')
            ###############################################
            # remove file if outside of the time range
            if start_date < time_start or end_date > time_end:
                files[n] = []
                start_dates = []
                end_dates = []
    # again, remove files outside of time range
    files = [ele for ele in files if ele != []]
    start_dates = [ele for ele in start_dates if ele != []]
    end_dates = [ele for ele in end_dates if ele != []]
    
    # repeat path to conform with other variable lengths
    P1s = []
    for n in range(len(files)):      
        P1s.append(path)
    path = P1s
    
    return files, path, start_dates, end_dates

#############################################################################
#############################################################################
#############################################################################

# create dictionary to store filenames

filenames = {}
filenames['sites'] = sites;

mooring_dir = 'Z:\\home\\' + user + '\\sci-maths-ocean\\IMOS\\DATA\\MOORINGS\\PROCESSED_2_5'

time_start = np.datetime64('2005-01-01'); # date much earlier than mooring record
time_end = '' # if left as '' no end date limit

# get filenames
for site_name in sites:
    print(site_name)
    # TEMPERATURE
    filenames[site_name + '_TEMP_files'], \
    filenames[site_name + '_TEMP_path'],\
    filenames[site_name + '_TEMP_start_dates'], \
    filenames[site_name + '_TEMP_end_dates'] = get_files(
                            mooring_dir,site_name,'TEMPERATURE',time_start,time_end)
    # CURRENT
    if os.path.exists(mooring_dir + '\\' + site_name + '\\CURRENT'): 
        filenames[site_name + '_CURR_files'], \
        filenames[site_name + '_CURR_path'],\
        filenames[site_name + '_CURR_start_dates'], \
        filenames[site_name + '_CURR_end_dates'] = get_files(
                                mooring_dir,site_name,'CURRENT',time_start,time_end)
    # SBE37 (TEMP, PSAL and others)
    if os.path.exists(mooring_dir + '\\' + site_name + '\\SBE37'):
        filenames[site_name + '_SBE_files'], \
        filenames[site_name + '_SBE_path'],\
        filenames[site_name + '_SBE_start_dates'], \
        filenames[site_name + '_SBE_end_dates'] = get_files(
                                mooring_dir,site_name,'SBE37',time_start,time_end)
    if os.path.exists(mooring_dir + '\\' + site_name + '\\SBE37_CTD'):
        filenames[site_name + '_SBE_files'], \
        filenames[site_name + '_SBE_path'],\
        filenames[site_name + '_SBE_start_dates'], \
        filenames[site_name + '_SBE_end_dates'] = get_files(
                                mooring_dir,site_name,'SBE37_CTD',time_start,time_end)        
    # ORS/PH100 buoy TEMP (TEMP, PSAL and others)
    if os.path.exists(mooring_dir + '\\' + site_name + '\\Buoy_TEMP'): 
        filenames[site_name + '_Buoy_TEMP_files'], \
        filenames[site_name + '_Buoy_TEMP_path'],\
        filenames[site_name + '_Buoy_TEMP_start_dates'], \
        filenames[site_name + '_Buoy_TEMP_end_dates'] = get_files(
                                mooring_dir,site_name,'Buoy_TEMP',time_start,time_end)    
    # BGC (TEMP, PSAL and others)
    if os.path.exists(mooring_dir + '\\' + site_name + '\\BGC'): 
        filenames[site_name + '_BGC_files'], \
        filenames[site_name + '_BGC_path'],\
        filenames[site_name + '_BGC_start_dates'], \
        filenames[site_name + '_BGC_end_dates'] = get_files(
                                mooring_dir,site_name,'BGC',time_start,time_end)                  
      
fn_keys = filenames.keys()

if 'TEMP' in variables:
    
    # if more than one instrument available for temperature, combine
    file_type_check = [] 
    file_type_start = []
    for key in fn_keys:
        if 'files' in key and 'CURR' not in key:
            file_type_check.append(key)
        if 'start' in key and 'CURR' not in key:
            file_type_start.append(key)   
        
    combined_files = []
    combined_start = []
    
    for key in file_type_check:     
        combined_files.append(filenames[key])
    for key in file_type_start:     
        combined_start.append(filenames[key])
        
    combined_files = np.concatenate(combined_files)
    combined_start = np.concatenate(combined_start)

if 'PSAL' in variables:
    
    # if more than one instrument available for temperature, combine
    file_type_check = [] 
    file_type_start = []
    for key in fn_keys:
        if 'files' in key and 'CURR' not in key and 'TEMP' not in key:
            file_type_check.append(key)
        if 'start' in key and 'CURR' not in key and 'TEMP' not in key:
            file_type_start.append(key)   
        
    combined_files = []
    combined_start = []
    
    for key in file_type_check:     
        combined_files.append(filenames[key])
    for key in file_type_start:     
        combined_start.append(filenames[key])
        
    combined_files = np.concatenate(combined_files)
    combined_start = np.concatenate(combined_start)
    
if 'CURR' in variables:
    
    # if more than one instrument available for temperature, combine
    file_type_check = [] 
    file_type_start = []
    for key in fn_keys:
        if 'files' in key and 'CURR' in key:
            file_type_check.append(key)
        if 'start' in key and 'CURR' in key:
            file_type_start.append(key)   
        
    combined_files = []
    combined_start = []
    
    for key in file_type_check:     
        combined_files.append(filenames[key])
    for key in file_type_start:     
        combined_start.append(filenames[key])
        
    combined_files = np.concatenate(combined_files)
    combined_start = np.concatenate(combined_start)    
    
    
def get_thredds_filenames(node,site,data_type):
    # scrape thredds server
    res = requests.get(
        'https://thredds.aodn.org.au/thredds/catalog/IMOS/ANMN/' + node + '/' + site + '/' + data_type + '/catalog.html')
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
    

# %% if time range required
#----------------------------------------------------------------------------

if len(time_range) == 2:
    c = np.logical_and(combined_start >= time_range[0],
                       combined_start <= time_range[1])
    combined_files = np.array(combined_files)[c]

# %% Directories
#----------------------------------------------------------------------------

output_dir = ('C:\\Users\\mphem\\Desktop')


# input_dir = filenames[site_name +'_' + 'BGC' + '_path'][0];

input_dir = 'http://thredds.aodn.org.au/'

# NEED TO ADAPT THE CODE TO CREATE TEMP DATA PRODUCTS FIRST, FOLLOWED BY OTHER FOLDERS
# PAIN IN THE ASS THAT THERE IS A FOLDER FOR 'TEMPERATURE', 'SBE37','BUOY' ETC.
# HOW BEST TO DO THIS?

# add correct OpenDAP link to filenames
combined_files_dir = []
for n in combined_files:
    if 'SBE' in n:
        combined_files_dir.append('thredds/dodsC/IMOS/ANMN/NSW/PH100/CTD_timeseries/' + n)
    else:
        combined_files_dir.append('thredds/dodsC/IMOS/ANMN/NSW/PH100/Biogeochem_timeseries/' + n)


# %% TEMP aggregated
#----------------------------------------------------------------------------

# files_to_agg = combined_files_dir
# var_to_agg = 'PSAL'
# site_code = site_name
# download_url_prefix=None
# opendap_url_prefix=None

agg.main_aggregator(combined_files_dir, 'PSAL', site_name, input_dir, 
             output_dir, download_url_prefix=None, opendap_url_prefix=None)

# for file_name in combined_files:
#     ds = xr.open_dataset(input_dir + file_name)
#     # if 'deployment_start' in list(ds.attrs):
#     #     print(file_name)
#     if 'float64' in str(ds.TIME.dtype):
#         print(file_name)
        
# concatenation for Neil's paper
# import xarray as xr
# new_data = xr.open_dataset(output_dir + '\\IMOS_ANMN-NSW_SZ_20220318_PH100_FV01_PSAL-aggregated-timeseries_END-20220616_C-20220902.nc')
# LTSP = xr.open_dataset('http://thredds.aodn.org.au/thredds/dodsC/IMOS/ANMN/NSW/PH100/aggregated_timeseries/IMOS_ANMN-NSW_SZ_20100504_PH100_FV01_PSAL-aggregated-timeseries_END-20220317_C-20220622.nc')
 
# # create new xarray to get around INSTRUMENT error
# nd = xr.Dataset()
# var_list = list(new_data.variables)
# var_list = var_list[0:8]
# for v in var_list:
#     nd[v] = new_data[v]
# nd.attrs = new_data.attrs
# # same for LTSP
# ltsp = xr.Dataset()
# for v in var_list:
#     ltsp[v] = LTSP[v]
# ltsp.attrs = LTSP.attrs

# conc_data = xr.concat([ltsp,nd],dim='OBSERVATION')
# conc_data.to_netcdf(output_dir + '\\IMOS_ANMN-NSW_SZ_20100504_PH100_FV01_PSAL-aggregated-timeseries_END-20220616_C-20220902.nc')


# %% TEMP hourly
#----------------------------------------------------------------------------

# %% TEMP gridded
#----------------------------------------------------------------------------

# %% VEL aggregated
#----------------------------------------------------------------------------

# start here, this code needs cleaning. Use OpenDAP instead. 
# can't use for ORS065 yet as Tim is still working on the files.. 

node = 'NSW'
site = 'ORS065'
data_type = 'Velocity'

files,locs = get_thredds_filenames(node,site,data_type)
indir = 'Z:\\home\\z3526971\\sci-maths-ocean\\IMOS\\DATA\\MOORINGS\\PROCESSED_2_5\\ORS065_Original\\CURRENT\\'
# so let's use the server option
vat.velocity_aggregated(list(combined_files), 'ORS065', input_dir=indir, output_dir='C:\\Users\\mphem\\Desktop',
                        download_url_prefix=None, opendap_url_prefix=None)


# %% VEL hourly
#----------------------------------------------------------------------------

# %% VEL gridded
#----------------------------------------------------------------------------


