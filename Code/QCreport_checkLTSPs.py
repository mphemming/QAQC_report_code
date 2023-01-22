#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created Thu Jan 19 10:52:33 2023
# Contributers (code):  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# Contributers (review): Moninya Roughan (NSW-IMS), Tim Austin (NSW-IMOS), Stuart Milburn (NSW-IMOS) 
# contact email: m.hemming@unsw.edu.au

# %% -----------------------------------------------------------------------------------------------
# Import packages
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

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

import xarray as xr
import numpy as np
import matplotlib
matplotlib.use('qt5Agg')
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import glob
import re
import os
import requests
import shutil
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

os.chdir('C:\\Users\\mphem\\OneDrive - UNSW\\Work\\QC_reports\\Code\\LTSPs\\')
import LTSP_Functions as LTSPFs
os.chdir('C:\\Users\\mphem\\OneDrive - UNSW\\Work\\QC_reports\\Code\\')

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# %% -----------------------------------------------------------------------------------------------
# Functions

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________


def get_latest_deployment_date(node, site_code,variable):
    if 'TEMP' in variable or 'hourly' in variable:
        if 'hourly' in variable:
            variable = 'TEMP'
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
            start_dates_thredds = []
            end_dates_thredds = []
            for f in files:
                underscore_index = [nn for nn in range(len(f)) if f.find('_', nn) == nn]
                start_dates_thredds.append(f[underscore_index[2]+1:underscore_index[2]+9])
                end_dates_thredds.append(f[underscore_index[6]+5:underscore_index[6]+13])
            end_dates_thredds = np.sort(end_dates_thredds)
            latest_date_thredds = end_dates_thredds[-1] 
    if 'velocity' in variable:
        # get all file names
        folders = LTSPFs.get_thredds_folders(node, site_code, 'CURR')
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

def determUpdate(file_list,temporary_path):
    time_cov = []
    latest_deployment = []
    needs_updating = []
    files_2update = []
    for f in file_list:
        ff = f.find('IMOS_ANMN')
        filename = f[ff::]
        print(filename)
        if os.path.exists(temporary_path + filename) == False:
            shutil.copy(f,temporary_path)
        d = xr.open_dataset(temporary_path + filename);
        if 'PSAL' in f or 'TEMP' in f or 'velocity' in f or 'hourly' in f:
            time_cov.append([d.time_coverage_start,d.time_coverage_end])
            t = get_latest_deployment_date('NSW', setup.site_name, f)
            latest_deployment.append(t)
            files_2update.append(f)
            # if latest deployment after time_coverage_end
            if t > np.datetime64(d.time_coverage_end):
                needs_updating.append(1)
            else:
                needs_updating.append(0)
                
    return time_cov, latest_deployment, needs_updating, files_2update


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
                ncout_path,_ = vat.velocity_aggregated(locs, site_code, '', output_dir,
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
            combined.attrs['title'] = existing.title.replace(combined.time_coverage_end,
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
            new_filename = output_dir + ServerFile[ServerFile.find('IMOS_ANMN')::]
            new_filename = ServerFile.replace(old_time, new_time)
            new_filename = new_filename.replace(old_creation,datetime.datetime.now().strftime('%Y%m%d'))
            # save new dataset
            combined.to_netcdf(new_filename)
            # remove latest file as not needed anymore
            latest.close()
            os.remove(ncout_path)

# !!! Issues: hourly product contains all variables, not just main ones
# Do I update the product for all variables or just TEMP, PSAL and vel?
# Issue concatanting existing and latest file because different vars in each :-/

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
        if '[]' not in str(files): # if there are new files, continue
            # create aggregated LTSP
            if 'velocity' not in ServerFile:
                ncout_path,_ = hrly.hourly_aggregator(locs, site_code, [1,2],'',
                        output_dir, download_url_prefix=None, opendap_url_prefix=None)
            else:
                ncout_path,_ = vatrly.velocity_hourly_aggregated(locs, site_code,'',
                        output_dir, download_url_prefix=None, opendap_url_prefix=None)    

        # load existing LTSP
        existing = xr.open_dataset(ServerFile)
        latest = xr.open_dataset(ncout_path)
        # separate datasets into dims INSTRUMENT and OBSERVATION for merging
        vs_ex = list(existing.variables)
        vs_la = list(latest.variables)
        existing_obs = dict(); existing_ins = dict()
        for v in vs_ex:
            if 'OBSERVATION' in existing[v].dims:
                existing_obs[v] = existing[v];
            else:
                existing_ins[v] = existing[v];
        latest_obs = dict(); latest_ins = dict()
        for v in vs_la:
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
        combined_obs = xr.merge([existing_obs,latest_obs], compat='override', join='inner')
        combined_ins = xr.concat([existing_ins,latest_ins],dim='INSTRUMENT')
        # create one combined LTSP file
        aligned_ds1, aligned_ds2 = xr.align(existing_obs, latest_obs, join='outer')
        merged_ds = xr.merge([aligned_ds1, aligned_ds2])
        
        
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

# %% -----------------------------------------------------------------------------------------------
# get file names, time coverage, and latest deployment date on thredds

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# get directories
dirr = ('Z:\\home\\z3526971\\sci-maths-ocean\\IMOS\\DATA\\MOORINGS\PROCESSED_2_5\\' + setup.site_name + 
              '\\LTSPs\\')
dirr_agg = dirr + 'aggregated_timeseries\\'
dirr_hourly = dirr + 'hourly_timeseries\\'
dirr_gridded = dirr + 'gridded_timeseries\\'

# get files
files_agg = glob.glob(dirr_agg +'*.nc')
files_hourly = glob.glob(dirr_hourly +'*.nc')
files_gridded = glob.glob(dirr_gridded +'*.nc')

# get time coverage

# aggregated files
time_cov_agg, latest_deployment_agg, \
    needs_updating_agg, files_2update_agg = determUpdate(files_agg, paths.TEMPORARY_dir)    
# hourly files
time_cov_hourly, latest_deployment_hourly, \
    needs_updating_hourly, files_2update_hourly = determUpdate(files_hourly, 
                                                               paths.TEMPORARY_dir)   
# gridded files
time_cov_gridded, latest_deployment_gridded, \
    needs_updating_gridded, files_2update_gridded = determUpdate(files_gridded, 
                                                                 paths.TEMPORARY_dir)   
 
# check if gridded product/s are interpolated every 1m
for nf in range(len(files_2update_gridded)):
    if np.unique(np.diff(xr.open_dataset(files_2update_gridded[nf]).DEPTH.values)) != 1:
        needs_updating_gridded[nf] = 1
     
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# %% -----------------------------------------------------------------------------------------------
# Update the LTSPs if needed

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# aggregated
if np.sum(needs_updating_agg) > 0:
    for n in range(len(files_2update_agg)):
        if bool(needs_updating_agg[n]):
            f = files_2update_agg[n]
            if 'TEMP' in f:
                updateAggregatedLTSP('NSW', setup.site_name, f,latest_deployment_agg,
                                     'TEMP',paths.TEMPORARY_dir)
            if 'PSAL' in f:
                updateAggregatedLTSP('NSW', setup.site_name, f,latest_deployment_agg,
                                     'PSAL',paths.TEMPORARY_dir)
            if 'velocity' in f:
                updateAggregatedLTSP('NSW', setup.site_name, f,latest_deployment_agg,
                                     'velocity',paths.TEMPORARY_dir)

# hourly
# if np.sum(needs_updating_hourly) > 0:
    
    
    
#     for n in range(len(files_2update_hourly)):
#         if bool(needs_updating_hourly[n]) \
#         and 'including-non-QC' not in files_2update_hourly[n]:
#             if 'TEMP' in f or 'PSAL' in f or 'velocity' in f:
#                 updateHourlyLTSP('NSW', setup.site_name, f,latest_deployment_agg,
#                                      'TEMP',paths.TEMPORARY_dir)
# !!! check that file exists before creating new one
# !!! skipping for now, will look again next week (notes in above section)



# %% -----------------------------------------------------------------------------------------------
# Final message and tidy-up

print('LTSPs ready to use.')



