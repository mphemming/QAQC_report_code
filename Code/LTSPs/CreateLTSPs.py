# CreateLTSPs.py
#
# Created on 04/01/2023
# Written by  Michael Hemming (NSW-IMOS)
# contact email: m.hemming@unsw.edu.au
#
# %% ------------------------------------------------------------------------------------
# Import Packages

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
import psutil
os.chdir('C:\\Users\\mphem\\OneDrive - UNSW\\Work\\QC_reports\\Code\\LTSPs\\')
import LTSP_Functions as LTSPFs


# %% ------------------------------------------------------------------------------------
# function to get LTSPs

def getLTSPs(file_list,variable,site_code,input_dir,output_dir):  
    
    #####################################################################################
    # first determine which files already exist
    ExistingFiles = os.listdir(output_dir)
    file_type = []
    for EF in ExistingFiles:
        underscore_index = [nn for nn in range(len(EF)) if EF.find('_', nn) == nn]
        if sum(underscore_index) > 0:
            file_type.append(EF[underscore_index[5]+1:underscore_index[6]])
    
    #####################################################################################
    # aggregated product
    if 'CURR' not in variable: 
        if 'aggregated' not in str(file_type):
            print('Creating aggregated product')
            agg.main_aggregator(file_list, variable, site_code, input_dir, 
                        output_dir, download_url_prefix=None, opendap_url_prefix=None)
    else:
        # velocity aggregated product
        if 'velocity-aggregated' not in str(file_type):
            print('Creating velocity aggregated product')
            input_file,_ = vat.velocity_aggregated(file_list, site_code, input_dir, output_dir,
                            download_url_prefix=None, opendap_url_prefix=None)
    #####################################################################################
    # hourly and gridded products
    if 'CURR' not in variable:
        # hourly
        if 'hourly' not in str(file_type):
            print('Creating hourly product')
            qcflags = [1,2] # good data, probably good data
            hrly_filename,_ = hrly.hourly_aggregator(file_list, site_code, qcflags, input_dir, output_dir,
                              download_url_prefix=None, opendap_url_prefix=None);
            # gridded
            resolution = 1
            separation = 16
            grid.grid_variable(hrly_filename, variable, depth_bins=None, max_separation=separation, 
                               depth_bins_increment=resolution,input_dir=input_dir, 
                               output_dir=output_dir, download_url_prefix=None, opendap_url_prefix=None)
    else:
        if 'velocity-hourly' not in str(file_type):
            print('Creating velocity hourly product')
            # velocity hourly product
            hrly_filename,_ = vatrly.velocity_hourly_aggregated(file_list, site_code, input_dir, output_dir,
                                   download_url_prefix=None, opendap_url_prefix=None) 
            # velocity gridded product
            # !!!!! To add gridded velocity product soon
            # depth_bins = list(range(0,150))
            # max_separation=16
            # depth_bins_increment=1
            # vatm.grid_variable(hrly_filename, site_code, depth_bins, max_separation, 
            #                     depth_bins_increment,input_dir, output_dir, 
            #                     download_url_prefix=None, opendap_url_prefix=None)
                                   

# %% ------------------------------------------------------------------------------------
# get LTSPs

# get file names for each site and variable
sites = ['BMP070','BMP090','BMP120','SYD140','SYD100','PH100','ORS065','CH050','CH070','CH100']
node = 'NSW'
variables = ['TEMP','PSAL','BGC','CURR']

# for testing
site = 'PH100'
variable = 'CURR'
time_range = [np.datetime64('2021-01-01'), np.datetime64('2022-01-01')]
output_dir = 'C:\\Users\\mphem\\Desktop\\'
folders = LTSPFs.get_thredds_folders(node,site,'CURR')
files, locs = LTSPFs.get_thredds_files(node,folders, site, time_range)
getLTSPs(locs,'CURR',site,'',output_dir)

for nn in range(len(sites)):
    output_dir = ('Z:\\home\\z3526971\\sci-maths-ocean\\IMOS\\DATA\\MOORINGS\PROCESSED_2_5\\' + sites[nn] + 
                  '\\LTSPs\\')
    for v in variables:
        print(sites[nn] + ' | ' + v)
        folders = LTSPFs.get_thredds_folders(node,sites[nn],v)
        if len(folders) > 0:
            files, locs = LTSPFs.get_thredds_files(node,folders, sites[nn], '')
            print(output_dir)
            getLTSPs(locs,v,sites[nn],'',output_dir)

# %% ------------------------------------------------------------------------------------
# remove all temporay netCDF files

filesAtOutput =os.listdir(output_dir)
remove_index = []
for nf in filesAtOutput:
    if 'tmp' in nf and '.nc' in nf:
        os.remove(output_dir + nf)
    else:
        continue

open_files = psutil.Process().open_files()
for nf in open_files:
    if 'tmp' in str(nf) and '.nc' in str(nf):
        file_to_close = nf
    else:
        continue


    file_to_close.kill(file_to_close)


# %% ------------------------------------------------------------------------------------
# testing parallel computing

# import multiprocessing as mp
# print("Number of processors: ", mp.cpu_count())

# np.random.RandomState(100)
# arr = np.random.randint(0, 10, size=[200000, 5])
# data = arr.tolist()

# def howmany_within_range(row, minimum, maximum):
#     """Returns how many numbers lie within `maximum` and `minimum` in a given `row`"""
#     count = 0
#     for n in row:
#         if minimum <= n <= maximum:
#             count = count + 1
#     return count

# # Step 1: Init multiprocessing.Pool()
# pool = mp.Pool(mp.cpu_count())

# # Step 2: `pool.apply` the `howmany_within_range()`
# results = [pool.apply(howmany_within_range, args=(row, 4, 8)) for row in data]

# # Step 3: Don't forget to close
# pool.close()  

# %% ------------------------------------------------------------------------------------


