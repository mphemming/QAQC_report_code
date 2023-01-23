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
os.chdir('C:\\Users\\mphem\\OneDrive - UNSW\\Work\\LTSP\\Code\\python-aodntools-master\\' +
          'python-aodntools-master\\')
# Velocity LTSPs
import aodntools.timeseries_products.velocity_aggregated_timeseries as vat
import aodntools.timeseries_products.velocity_hourly_timeseries as vatrly
import aodntools.timeseries_products.velocity_gridded_timeseries_Michael as vatm
# Temp/other LTSPs
import aodntools.timeseries_products.aggregated_timeseries as agg
import aodntools.timeseries_products.hourly_timeseries as hrly
import aodntools.timeseries_products.gridded_timeseries as grid
# get file list
# import geoserverCatalog as gc # not needed today as we are using files stored on the server
# other useful packages
import numpy as np
# import xarray as xr
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
import numpy.matlib

# %% Define sites and variables required for LTSPs (must mirror folder names in data folder)
#----------------------------------------------------------------------------

# sites = ['BMP070','BMP090','BMP120','CH050','CH070','CH100','ORS065','PH100','SYD100','SYD140'];

sites = ['CH100']

# variables = ['TEMP','CURR','PSAL','DOX2','CPHL']
variables = ['TEMP']

user = 'z3526971'

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
        
# %% function to create all LTSPs
#----------------------------------------------------------------------------        
        
def getLTSPs(file_list,variable,site_code,input_dir,output_dir):  
    
    #####################################################################################
    # aggregated product
    # agg.main_aggregator(file_list, variable, site_code, input_dir, 
    #             output_dir, download_url_prefix=None, opendap_url_prefix=None)
    #####################################################################################
    # hourly product
    # qcflags = [1,2] # good data, probably good data
    # hrly_filename,_,_ = hrly.hourly_aggregator(file_list, site_code, qcflags, input_dir, output_dir,
    #                   download_url_prefix=None, opendap_url_prefix=None);
    #####################################################################################
    # gridded product
    hrly_filename = ('Z:\\home\\z3526971\\sci-maths-ocean\\IMOS\\DATA\\MOORINGS\\' +
                     'PROCESSED_2_5\\CH100\LTSPs\\' + 
                    'IMOS_ANMN-NSW_TZ_20090815_CH100_FV02_hourly-timeseries_END-20120110_C-20220818.nc')
    resolution = 1
    separation = 16
    grid.grid_variable(hrly_filename, variable, depth_bins=None, max_separation=separation, depth_bins_increment=resolution,
              input_dir=input_dir, output_dir=output_dir, download_url_prefix=None, opendap_url_prefix=None)
    
        
def getLTSPs_Vel(file_list,site_code,input_dir,output_dir): 
    
    #####################################################################################
    # velocity aggregated product
    input_file,_ = vat.velocity_aggregated(file_list, site_code, input_dir, output_dir,
                    download_url_prefix=None, opendap_url_prefix=None)
    #####################################################################################
    # velocity hourly product
    vatrly.velocity_hourly_aggregated(file_list, site_code, input_dir, output_dir,
                           download_url_prefix=None, opendap_url_prefix=None)
    #####################################################################################
    # velocity gridded product
    input_dir = input_dir[0:-8] + 'LTSPs\\'
    depth_bins = list(range(0,150))
    max_separation=16
    depth_bins_increment=1
    vatm.grid_variable(input_file, ['VCUR','UCUR'], depth_bins, max_separation, 
                       depth_bins_increment,input_dir, output_dir, 
                       download_url_prefix=None, opendap_url_prefix=None)
        
# %% if products don't exist / or aren't up to date, create/update LTSPs
#----------------------------------------------------------------------------

# for site_name in sites:
#     print(site_name)
#     # check if files exist in LTSP folder
#     files = os.listdir(mooring_dir + '\\' + site_name + '\\LTSPs\\')
#     # if there are files, is it the latest file (based on date of latest file)
#     if len(files) != 0:
#         # for each variable
#         for v in variables:
#             # and for each file in folder
#             for f in files:
#                 if v in f:
#                     # get end date of the LTSP
#                     end_ind_1 = f.find('END')+4
#                     end_ind_2 = end_ind_1+8
#                     end_date = f[end_ind_1:end_ind_2]
#                     end_date = np.datetime64((end_date[0:4] + '-' + 
#                                            end_date[4:6] + '-' +
#                                            end_date[6:8]))
#                     # does this match the latest file date?
#                     max_file_date = np.nanmax(filenames[site_name + '_' + v + '_end_dates'])
#                     if max_file_date != end_date:
#                         # combine all files for site
#                         # file_list = []
#                         # for fn in fn_keys:
#                         #     if np.logical_and(site_name in fn,
#                         #                       'files' in fn):
#                         #         file_list.append(filenames[fn])
#                         # file_list = np.concatenate(file_list)
#                         # create LTSPs
#                         # -----------------------------
#                         if 'TEMP' in v:
#                             # TEMPERATURE
#                             file_list = filenames[site_name +'_' + v + '_files'];
#                             input_dir = filenames[site_name +'_' + v + '_path'][0];
#                             output_dir = ('Z:\\home\\' + user + '\\sci-maths-ocean\\IMOS\\' +
#                                             'DATA\\MOORINGS\\PROCESSED_2_5\\' + site_name + 
#                                             '\\LTSPs\\')
#                             getLTSPs(file_list,v,site_name,input_dir,output_dir)
                            
#                             # SBE37
#                             if np.logical_or(site_name + '_' + 'SBE37' + '_files' in filenames,
#                                           site_name + '_' + 'SBE37_CTD' + '_files' in filenames):
                                
#                                 file_list = filenames[site_name +'_' + 'SBE' + '_files'];
#                                 input_dir = filenames[site_name +'_' + 'SBE' + '_path'][0];
#                                 output_dir = ('Z:\\home\\' + user + 
#                                               '\\sci-maths-ocean\\IMOS\\' +
#                                               'DATA\\MOORINGS\\PROCESSED_2_5\\' 
#                                               + site_name + '\\LTSPs\\')
#                                 getLTSPs(file_list,v,site_name,input_dir,output_dir)
                                
#                             # BGC
#                             file_list = filenames[site_name +'_' + 'BGC' + '_files'];
#                             input_dir = filenames[site_name +'_' + 'BGC' + '_path'][0];
#                             output_dir = ('Z:\\home\\' + user + '\\sci-maths-ocean\\IMOS\\' +
#                                             'DATA\\MOORINGS\\PROCESSED_2_5\\' + site_name + 
#                                             '\\LTSPs\\')
#                             getLTSPs(file_list,v,site_name,input_dir,output_dir)
                            
#                             # Bouy TEMP
#                             file_list = filenames[site_name +'_' + 'Bouy_TEMP' + '_files'];
#                             input_dir = filenames[site_name +'_' + 'Bouy_TEMP' + '_path'][0];
#                             output_dir = ('Z:\\home\\' + user + '\\sci-maths-ocean\\IMOS\\' +
#                                             'DATA\\MOORINGS\\PROCESSED_2_5\\' + site_name + 
#                                             '\\LTSPs\\')
#                             getLTSPs(file_list,v,site_name,input_dir,output_dir)
                            
#                             if 'CURR' in v:
#                                 file_list = filenames[site_name +'_' + v + '_files'];
#                                 input_dir = filenames[site_name +'_' + v + '_path'][0];
#                                 output_dir = ('Z:\\home\\' + user + '\\sci-maths-ocean\\IMOS\\' +
#                                                 'DATA\\MOORINGS\\PROCESSED_2_5\\' + site_name + 
#                                                 '\\LTSPs\\')
#                                 getLTSPs(file_list,v,site_name,input_dir,output_dir)
                            
                            
                            
#         else:
             
# %% ------------------------------------------
# quicker version for PUG

# for site_name in sites:
#     print(site_name)
#     # for each variable
#     for v in variables:
#         file_list = filenames[site_name +'_' + v + '_files'];
#         input_dir = filenames[site_name +'_' + v + '_path'][0];
#         output_dir = ('Z:\\home\\' + user + '\\sci-maths-ocean\\IMOS\\' +
#                         'DATA\\MOORINGS\\PROCESSED_2_5\\' + site_name + 
#                         '\\LTSPs\\')
#         getLTSPs_Vel(file_list,site_name,input_dir,output_dir)        
                    
                    
# %% ------------------------------------------
# create LTSPs (testing CH100 deployments)

# sort out files
v = 'TEMP'
start_dates = filenames[site_name +'_' + v + '_start_dates'];
file_list = filenames[site_name +'_' + v + '_files'];
v = 'SBE'
start_dates_SBE = [filenames[site_name +'_' + v + '_start_dates']];
file_list_SBE = [filenames[site_name +'_' + v + '_files']];
# select files wanted
c = start_dates <= np.datetime64('2012-01-01')
file_list = np.array(file_list)[c]
c = start_dates_SBE <= np.datetime64('2012-01-01')
file_list_SBE = np.array(file_list_SBE)[c]

# Temperature
# paths
v = 'TEMP'
output_dir = ('Z:\\home\\' + user + '\\sci-maths-ocean\\IMOS\\' +
                'DATA\\MOORINGS\\PROCESSED_2_5\\' + site_name + 
                '\\LTSPs\\')
input_dir = filenames[site_name +'_' + v + '_path'][0];

getLTSPs(file_list,'TEMP','CH100',input_dir,output_dir)
# SBE
v = 'SBE'
output_dir = ('Z:\\home\\' + user + '\\sci-maths-ocean\\IMOS\\' +
                'DATA\\MOORINGS\\PROCESSED_2_5\\' + site_name + 
                '\\LTSPs\\')
input_dir = filenames[site_name +'_' + v + '_path'][0];

getLTSPs(file_list_SBE,'TEMP','CH100',input_dir,output_dir)




