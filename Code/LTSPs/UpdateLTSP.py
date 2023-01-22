# UpdateLTSP.py
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
import shutil
import glob

# %% ------------------------------------------------------------------------------------
# check which files need updating

def get_latest_deployment_date(node, site_code,variable):
    if 'TEMP' in variable:
        # get all file names
        folders = LTSPFs.get_thredds_folders(node, site_code, variable)
        files, locs = LTSPFs.get_thredds_files(node,folders, site_code, '')
        # get start dates for files on thredds
        start_dates_thredds = []
        end_dates_thredds = []
        for f in files:
            underscore_index = [nn for nn in range(len(f)) if f.find('_', nn) == nn]
            start_dates_thredds.append(f[underscore_index[2]+1:underscore_index[2]+9])
            end_dates_thredds.append(f[underscore_index[6]+5:underscore_index[6]+13])
        end_dates_thredds = np.sort(end_dates_thredds)
        latest_date_thredds = end_dates_thredds[-1]
    if 'PSAL' in variable:
        # get all file names
        folders = LTSPFs.get_thredds_folders(node, site_code, variable)
        if '[]' not in str(folders):
            files, locs = LTSPFs.get_thredds_files(node,folders, site_code, '')
            # get start dates for files on thredds
            end_dates_thredds = []
            for f in files:
                underscore_index = [nn for nn in range(len(f)) if f.find('_', nn) == nn]
                start_dates_thredds.append(f[underscore_index[2]+1:underscore_index[2]+9])
                end_dates_thredds.append(f[underscore_index[6]+5:underscore_index[6]+13])
            end_dates_thredds = np.sort(end_dates_thredds)
            latest_date_thredds = end_dates_thredds[-1] 
    if 'CURR' in variable:
        # get all file names
        folders = LTSPFs.get_thredds_folders(node, site_code, variable)
        if '[]' not in str(folders):
            files, locs = LTSPFs.get_thredds_files(node,folders, site_code, '')
            # get start dates for files on thredds
            start_dates_thredds = []
            end_dates_thredds = []
            for f in files:
                underscore_index = [nn for nn in range(len(f)) if f.find('_', nn) == nn]
                start_dates_thredds.append(f[underscore_index[2]+1:underscore_index[2]+9])
                end_dates_thredds.append(f[underscore_index[6]+5:underscore_index[6]+13])
            end_dates_thredds = np.sort(end_dates_thredds)
            latest_date_thredds = end_dates_thredds[-1]  
            
    # convert latest_date_thredds to correct format
    latest_date_thredds =   np.datetime64((latest_date_thredds[0:4] + '-' + latest_date_thredds[4:6] + 
                             '-' + latest_date_thredds[6:8]))    
    
    return latest_date_thredds
 
def updateAggregatedLTSP(node, site_code, ServerFile,latest_deployment_thredds,variable,output_dir):
    ServerFile_endDate = np.datetime64(xr.open_dataset(ServerFile).time_coverage_end[0:10])
    if ServerFile_endDate < latest_deployment_thredds:
        print('Updating LTSP: ......... ' + ServerFile)
        # define time range needed to create aggregated LTSP
        time_range = [ServerFile_endDate, latest_deployment_thredds]
        # get files needed
        folders = LTSPFs.get_thredds_folders(node,site_code,variable)
        files, locs = LTSPFs.get_thredds_files(node,folders, site_code, time_range)
        if '[]' not in str(files): # if there are new files, continue
            # create aggregated LTSP
            if 'velocity' not in ServerFile:
                ncout_path,_ = agg.main_aggregator(locs, variable, site_code, '', 
                            output_dir, download_url_prefix=None, opendap_url_prefix=None)
            else:
                ncout_path,_ = vat.velocity_aggregated(file_list, site_code, input_dir, output_dir,
                                download_url_prefix=None, opendap_url_prefix=None)    
            # load existing LTSP
            existing = xr.open_dataset(ServerFile)
            latest = xr.open_dataset(ncout_path)
            # separate datasets into dims INSTRUMENT and OBSERVATION for merging
            vs = list(existing.variables)
            existing_obs = dict(); existing_ins = dict()
            for v in vs:
                if 'OBSERVATION' in existing[v].dims:
                    existing_obs[v] = existing[v];
                else:
                    existing_ins[v] = existing[v];
            latest_obs = dict(); latest_ins = dict()
            for v in vs:
                if 'OBSERVATION' in latest[v].dims:
                    latest_obs[v] = latest[v];
                else:
                    latest_ins[v] = latest[v];
            # convert to dataset
            existing_obs = xr.Dataset(existing_obs)
            existing_ins = xr.Dataset(existing_ins)
            latest_obs = xr.Dataset(latest_obs)
            latest_ins = xr.Dataset(latest_ins)
            # concatenate
            combined_obs = xr.concat([existing_obs,latest_obs],dim='OBSERVATION')
            combined_ins = xr.concat([existing_ins,latest_ins],dim='INSTRUMENT')
            # create one combined LTSP file
            combined = xr.merge([combined_obs,combined_ins])
            # add attributes
            combined.attrs = existing.attrs
            combined.attrs['time_coverage_end'] = latest.time_coverage_end
            combined.attrs['title'] = existing.title.replace(combined.time_coverage_end.to_dict()['data'],
                                                       latest.time_coverage_end)
            combined.attrs['history'] = latest.history
            # create updated filename
            old_time = "".join([existing.time_coverage_end[0:4],
                                 existing.time_coverage_end[5:7],
                                 existing.time_coverage_end[8:10]])
            new_time = "".join([latest.time_coverage_end[0:4],
                                 latest.time_coverage_end[5:7],
                                 latest.time_coverage_end[8:10]])
            old_creation = ServerFile[-11:-3];
            new_filename = ServerFile.replace(old_time, new_time)
            new_filename = new_filename.replace(old_creation,datetime.datetime.now().strftime('%Y%m%d'))
            # save new dataset
            combined.to_netcdf(new_filename)
            # remove latest file as not needed anymore
            latest.close()
            os.remove(ncout_path)
            # remove any temporary files
            # !!! doesn't work, but perhaps I'll create another script to remove temporary files later..
            # temp_files = glob.glob(output_dir + 'tmp*.nc')
            # for tf in temp_files:
            #     os.remove(tf)
        
def updateHourlyLTSP(node, site_code, ServerFile,latest_deployment_thredds,variable,output_dir):
    ServerFile_endDate = np.datetime64(xr.open_dataset(ServerFile).time_coverage_end[0:10])
    if ServerFile_endDate < latest_deployment_thredds:
        print('Updating LTSP: ......... ' + ServerFile)
        # define time range needed to create aggregated LTSP
        time_range = [ServerFile_endDate, latest_deployment_thredds]
        # get files needed
        folders = LTSPFs.get_thredds_folders(node,site_code,variable)
        files, locs = LTSPFs.get_thredds_files(node,folders, site_code, time_range)
        # create aggregated LTSP
        ncout_path,_ = agg.main_aggregator(locs, variable, site_code, '', 
                    output_dir, download_url_prefix=None, opendap_url_prefix=None)
        # load existing LTSP
        existing = xr.open_dataset(ServerFile)
        latest = xr.open_dataset(ncout_path)
        # separate datasets into dims INSTRUMENT and OBSERVATION for merging
        vs = list(existing.variables)
        existing_obs = dict(); existing_ins = dict()
        for v in vs:
            if 'OBSERVATION' in existing[v].dims:
                existing_obs[v] = existing[v];
            else:
                existing_ins[v] = existing[v];
        latest_obs = dict(); latest_ins = dict()
        for v in vs:
            if 'OBSERVATION' in latest[v].dims:
                latest_obs[v] = latest[v];
            else:
                latest_ins[v] = latest[v];
        # convert to dataset
        existing_obs = xr.Dataset(existing_obs)
        existing_ins = xr.Dataset(existing_ins)
        latest_obs = xr.Dataset(latest_obs)
        latest_ins = xr.Dataset(latest_ins)
        # concatenate
        combined_obs = xr.concat([existing_obs,latest_obs],dim='OBSERVATION')
        combined_ins = xr.concat([existing_ins,latest_ins],dim='INSTRUMENT')
        # create one combined LTSP file
        combined = xr.merge([combined_obs,combined_ins])
        # add attributes
        combined.attrs = existing.attrs
        combined.attrs['time_coverage_end'] = latest.time_coverage_end
        combined.attrs['title'] = existing.title.replace(combined.time_coverage_end.to_dict()['data'],
                                                   latest.time_coverage_end)
        combined.attrs['history'] = latest.history
        # create updated filename
        old_time = "".join([existing.time_coverage_end[0:4],
                             existing.time_coverage_end[5:7],
                             existing.time_coverage_end[8:10]])
        new_time = "".join([latest.time_coverage_end[0:4],
                             latest.time_coverage_end[5:7],
                             latest.time_coverage_end[8:10]])
        old_creation = ServerFile[-11:-3];
        new_filename = ServerFile.replace(old_time, new_time)
        new_filename = new_filename.replace(old_creation,datetime.datetime.now().strftime('%Y%m%d'))
        # save new dataset
        combined.to_netcdf(new_filename)
        # remove latest file as not needed anymore
        latest.close()
        os.remove(ncout_path)
        # remove any temporary files
        # !!! doesn't work, but perhaps I'll create another script to remove temporary files later..
        # temp_files = glob.glob(output_dir + 'tmp*.nc')
        # for tf in temp_files:
        #     os.remove(tf)

# %% ------------------------------------------------------------------------------------
# testing
    
# !!! Notes
# Need to test velocity aggregated product above
#
# Issue with BMP070 velocity aggregated product, doesn't load ...
# same for hourly products too (various sites).. But works when using file downlaoded from internet ..
#
# SYD140
# IMOS_ANMN-NSW_STZ_20080625_SYD140_FV02_hourly-timeseries_END-20220920_C-20221213.nc: something went wrong .. 
# SYD100
# IMOS_ANMN-NSW_VZ_20080625_SYD100_FV01_velocity-aggregated-timeseries_END-20221017_C-20221213.nc: something went wrong .. 



site_code = 'BMP120'
node = 'NSW'
output_dir = ('Z:\\home\\z3526971\\sci-maths-ocean\\IMOS\\DATA\\MOORINGS\PROCESSED_2_5\\' + site_code + 
              '\\LTSPs\\hourly_timeseries\\')
variable = 'TEMP'

ExistingLTSPs = os.listdir(output_dir)
ServerFile = output_dir + ExistingLTSPs[1]
if 'TEMP' in ServerFile or 'PSAL' in ServerFile:
    latest_deployment_thredds = get_latest_deployment_date(node, site_code,'TEMP')
else:
    latest_deployment_thredds = get_latest_deployment_date(node, site_code,'CURR')
# testing 
latest_deployment_thredds = np.datetime64('2022-01-01')

    
# %% ------------------------------------------------------------------------------------
# 

LTSP_filename = (output_dir + 'IMOS_ANMN-NSW_TZ_20141118_BMP070_FV02_hourly-timeseries' + 
                 '_END-20220913_C-20230104.nc')
LTSP_end_date = np.datetime64(end_dates[0])
variable = 'TEMP'

def updateLTSP(LTSP_filename,LTSP_end_date,variable):
    # Need to first move LTSP file to local directory
    dst = ('C:\\Users\\mphem\\OneDrive - UNSW\\Work\\QC_reports\\Code\\LTSPs\\' + 
           'IMOS_ANMN-NSW_TZ_20141118_BMP070_FV02_hourly-timeseries_END-20220913_C-20230104.nc')
    shutil.copy(LTSP_filename, dst)shutil.copy(LTSP_filename, dst)
    # open file (STILL NOT WORKING. WHY?)
    data = xr.open_dataset(LTSP_filename)



# get list of files in directory
ExistingLTSPs = os.listdir(output_dir)
# get file information
start_dates = []
end_dates = []
product = []
for E in ExistingLTSPs:
    underscore_index = [nn for nn in range(len(E)) if E.find('_', nn) == nn]
    start_dates.append(np.datetime64(E[underscore_index[2]+1:underscore_index[3]]))
    product.append(E[underscore_index[5]+1:underscore_index[6]])
    end_dates.append(E[underscore_index[7]-8:underscore_index[7]])
# determine which products need updating
updating_index = []
for nfile in range(len(ExistingLTSPs)):
    if 'TEMP' in product[nfile]:
        latest_TEMP = get_latest_deployment_date(node, site_code, 'TEMP')
        if np.datetime64(end_dates[nfile]) < latest_TEMP:
            print('hello')
    if 'PSAL' in product[nfile]:
        latest_PSAL = get_latest_deployment_date(node, site_code, 'PSAL')
        if np.datetime64(end_dates[nfile]) < latest_PSAL:
            print('hello')
    if 'velocity' in product[nfile]:
        latest_CURR = get_latest_deployment_date(node, site_code, 'CURR')
        if np.datetime64(end_dates[nfile]) < latest_CURR:
            print('hello')
            
        
# %% ------------------------------------------------------------------------------------
# 

# %% ------------------------------------------------------------------------------------
# 

# %% ------------------------------------------------------------------------------------
# 