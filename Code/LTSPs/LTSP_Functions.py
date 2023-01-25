# LTSP_Functions.py
#
# Created on 05/01/2023
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

# %% ------------------------------------------------------------------------------------
# Functions


def get_thredds_folders(node,site,variable):
    res = requests.get(
        'https://thredds.aodn.org.au/thredds/catalog/IMOS/ANMN/' + node + '/' + site + '/catalog.html')
    txt = res.text
    # identify folder names
    end_txt = []
    folder_names = []
    for m in re.finditer('/</tt></a>', txt):
        end_txt.append(m.start())
    for m in range(len(end_txt)):
        first_attempt = txt[end_txt[m]-30:end_txt[m]]
        # remove stray html code
        f = first_attempt.find('<tt>')
        folder = first_attempt[f+4::]
        # only save variable folder names
        if 'TEMP' in variable:
            if ('Biogeochem_timeseries' in folder) or ('CTD_timeseries' in folder) or ('Temperature' in folder):
                folder_names.append(folder)
        if 'PSAL' in variable:
            if ('Biogeochem_timeseries' in folder) or ('CTD_timeseries' in folder):
                folder_names.append(folder)
        if ('BGC' in variable) or ('CTD_timeseries' in folder):
            if ('Biogeochem_timeseries' in folder):
                folder_names.append(folder)
        if 'CURR' in variable:
            if ('Velocity' in folder):
                folder_names.append(folder)
    
    return folder_names
    

def get_thredds_filenames(node,site,folder):
    # scrape thredds server
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
                        str(folder) + '/' + files[n])
        
    return files,locs


def get_thredds_files(node,folder,site,time_range):
    files = []; locs = [];
    if np.size(folder) == 1:
        files,locs = get_thredds_filenames(node,site,np.squeeze(folder))
    else:    
        for flds in folder:
            f,l = get_thredds_filenames(node,site,flds)
            files.append(f); locs.append(l);
        files = np.concatenate(files); locs = np.concatenate(locs)
        
    files = np.array(files); locs = np.array(locs)
    
    # select time_range if required
    if len(time_range) == 2:
        # get start and end dates of files
        start_dates = []; end_dates = [];
        for nf in range(len(files)):
            # Identify all underscores in filename to get dates
            f = files[nf]
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
                
        c = np.logical_and(start_dates >= time_range[0],
                           start_dates <= time_range[1])
        files = files[c]; locs = locs[c]
        
        # print warning if empty
        if len(files) == 0:
            print('No files within the time range selected')
    
    return files, locs
