#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Fri Jun  5 10:20:49 2020
# Contributers (code):  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# Contributers (review): Moninya Roughan (NSW-IMS), Tim Austin (NSW-IMOS), Stuart Milburn (NSW-IMOS) 
# contact email: m.hemming@unsw.edu.au

# What does this script do?

# o   Get attribute information from netCDF files for selected deployment

# %% -----------------------------------------------------------------------------------------------
# Import packages
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# Python Packages
import xarray as xr
import glob
import numpy as np
# QC report modules
import QCreport_paths as paths
import QCreport_setup as setup
import importlib
importlib.reload(setup) # needed for creating multiple reports in a loop

#------------------------------------------------------------
# Information 
#-------------

# These are the Python and QC report modules required to run 
# this script. The python modules should be installed using 
# 'pip/condo install', the QCreport modules need to be in 
# the same folder as this script.

#------------------------------------------------------------

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# %% -----------------------------------------------------------------------------------------------
# Function to select mutiple dictionary keys
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

def select_keys(dict,key_n):
    if key_n > 0:
        selected_keys = (range(0,key_n))
        subdict = {x: dict[x] for x in selected_keys if x in dict}
    else:
        subdict = dict[key_n]
    return subdict

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
    
# %% -----------------------------------------------------------------------------------------------
# Get attributes
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
    
abstract = {}
author = {}
author_email = {}
comment = {}
history = {}
instrument = {}
instrument_nominal_depth = {}
instrument_sample_interval = {}
instrument_serial_number = {}
local_time_zone = {}
platform_code = {}
principal_investigator = {}
quality_control_log = {}
time_coverage_start = {}
time_coverage_end = {}
toolbox_input_file = {}
toolbox_version = {}
geospatial_lat_max = {}
geospatial_lat_min = {}
geospatial_lon_max = {}
geospatial_lon_min = {}
variables = {}
var_names = {}
time_units = {}
time_comment = {}
depth_comment = {}
in_water = {}
out_water = {}

def get_netCDF(path):   
 
    # add hyphens to deployment file date identifier
    date_id = '-' + setup.deployment_file_date_identifier + '-'
    # Get list of netCDF files in folder
    nc_files = glob.glob(path + "*" + setup.site_name + "*" + date_id + "*.nc")
    len_files = len(nc_files)
    # sort by nominal depth (shallowest to deepest)
    if len_files > 1:
        nd = []
        for n_file in range(len_files):
            ncf = nc_files[n_file]
            find_nd = ncf.find('_END')
            nomD_str = ncf[find_nd-5:find_nd]
            find_hyphen = nomD_str.find('-')
            # if containing non-useful strings
            nomD_str = nomD_str[find_hyphen+1::]
            nd.append(nomD_str)
            
        f = np.argsort(np.array(nd).astype(float))  
        nd_sorted = np.array(nd).astype(float).astype(str)[f]
        # convert to 'integral' str by removing decimal point and zero, if applicable
        for n in range(len_files):
            if '.5' not in nd_sorted[n]:
                nd_sorted[n] = str(round(float(nd_sorted[n])))
        # shift file order around
        nc_files_sorted = np.array(nc_files)[f]
        
        # nc_files_sorted = []
        # for n_sort in range(len_files): 
        #     for n_file in range(len_files): 
        #         if '-' + nd_sorted[n_sort] + '_' in nc_files[n_file]:
        #             nc_files_sorted.append(nc_files[n_file])
        # nc_files = nc_files_sorted
        
        len_files = len(nc_files)

    if len_files > 0:

        # Get netCDF attributes for each file
        for n_file in range(len_files):
            f_info = xr.open_dataset(nc_files[n_file]).load()
    
            if hasattr(f_info,'abstract'):
                abstract[n_file] = f_info.abstract
            else:
                abstract[n_file] = 'No data'
        
            if hasattr(f_info,'author'):
                author[n_file] = f_info.author
            else:
                author[n_file] = 'No data'
                
            if hasattr(f_info,'author_email'):
                author_email[n_file] = f_info.author_email
            else:
                author_email[n_file] = 'No data'            
                
            if hasattr(f_info,'comment'):
                comment[n_file] = f_info.comment
            else:
                comment[n_file] = 'No data'
                
            if hasattr(f_info,'history'):
                history[n_file] = f_info.history
            else:
                history[n_file] = 'No data'            
                
            if hasattr(f_info,'instrument'):
                instrument[n_file] = f_info.instrument
            else:
                instrument[n_file] = 'No data'           
    
            if hasattr(f_info,'instrument_nominal_depth'):
                instrument_nominal_depth[n_file] = f_info.instrument_nominal_depth
            else:
                instrument_nominal_depth[n_file] = 'No data'
                
            if hasattr(f_info,'instrument_sample_interval'):
                instrument_sample_interval[n_file] = f_info.instrument_sample_interval
            else:
                instrument_sample_interval[n_file] = 'No data'
                
            if hasattr(f_info,'instrument_serial_number'):
                instrument_serial_number[n_file] = f_info.instrument_serial_number
            else:
                instrument_serial_number[n_file] = 'No data'
    
            if hasattr(f_info,'local_time_zone'):
                local_time_zone[n_file] = f_info.local_time_zone
            else:
                local_time_zone[n_file] = 'No data'
    
            if hasattr(f_info,'platform_code'):
                platform_code[n_file] = f_info.platform_code
            else:
                platform_code[n_file] = 'No data'            
    
            if hasattr(f_info,'principal_investigator'):
                principal_investigator[n_file] = f_info.principal_investigator
            else:
                principal_investigator[n_file] = 'No data'
    
            if hasattr(f_info,'quality_control_log'):
                quality_control_log[n_file] = f_info.quality_control_log
            else:
                quality_control_log[n_file] = 'No data'
                
            if hasattr(f_info,'time_coverage_start'):
                time_coverage_start[n_file] = f_info.time_coverage_start
            else:
                time_coverage_start[n_file] = 'No data'
                
            if hasattr(f_info,'time_coverage_end'):
                time_coverage_end[n_file] = f_info.time_coverage_end
            else:
                time_coverage_end[n_file] = 'No data'
                
            # to deal with xarray bug
            if time_coverage_start[n_file] == time_coverage_end[n_file]:
                # get from filename
                # start
                f = nc_files[n_file].find('TZ_')
                time_coverage_start[n_file] = (nc_files[n_file][f+3:f+7] + '-' + 
                                             nc_files[n_file][f+7:f+9] + '-' +
                                             nc_files[n_file][f+9:f+11] + 'T' + 
                                             nc_files[n_file][f+12:f+14] + ':' + 
                                             nc_files[n_file][f+14:f+16] + ':00Z')
                # end
                f = nc_files[n_file].find('END-')
                time_coverage_end[n_file] = (nc_files[n_file][f+4:f+8] + '-' + 
                                             nc_files[n_file][f+8:f+10] + '-' +
                                             nc_files[n_file][f+10:f+12] + 'T' + 
                                             nc_files[n_file][f+13:f+15] + ':' + 
                                             nc_files[n_file][f+15:f+17] + ':00Z')
    
            if hasattr(f_info,'toolbox_input_file'):
                toolbox_input_file[n_file] = f_info.toolbox_input_file
            else:
                toolbox_input_file[n_file] = 'No data'            
    
            if hasattr(f_info,'toolbox_version'):
                toolbox_version[n_file] = f_info.toolbox_version
            else:
                toolbox_version[n_file] = 'No data'
                
            if hasattr(f_info,'geospatial_lat_min'):
                geospatial_lat_min[n_file] = f_info.geospatial_lat_min
            else:
                geospatial_lat_min[n_file] = 'No data'
    
            if hasattr(f_info,'geospatial_lat_max'):
                geospatial_lat_max[n_file] = f_info.geospatial_lat_max
            else:
                geospatial_lat_max[n_file] = 'No data'
    
            if hasattr(f_info,'geospatial_lon_min'):
                geospatial_lon_min[n_file] = f_info.geospatial_lon_min
            else:
                geospatial_lon_min[n_file] = 'No data'
    
            if hasattr(f_info,'geospatial_lon_max'):
                geospatial_lon_max[n_file] = f_info.geospatial_lon_max
            else:
                geospatial_lon_max[n_file] = 'No data'            
    
            if hasattr(f_info,'variables'):
                variables[n_file] = f_info.variables
                var_names[n_file] = f_info.variables.keys()
            else:
                variables[n_file] = 'No data'
                var_names[n_file] = 'No data'    
            
            # get TIME and DEPTH attributes
            if 'TIME' in var_names[0]:
                tatt = f_info.variables['TIME']
                try:
                    time_units[n_file] = tatt.units
                except: 
                    time_units[n_file] = 'no units defined'
                try:
                    time_comment[n_file] = tatt.comment
                except:
                    pass
            if 'DEPTH' in var_names[0]:
                Datt = f_info.variables['DEPTH']      
                try:
                    depth_comment[n_file] = Datt.comment
                except:
                    pass
            # get times in/out water
            if hasattr(f_info,'quality_control_log'):
                if 'imosInOutWaterQC' in f_info.quality_control_log:
                    f_string = str(f_info.quality_control_log)
                    pos = f_string.find('imosInOutWaterQC')
                    in_water[n_file] = f_info.quality_control_log[pos+20:pos+37]
                    out_water[n_file] = f_info.quality_control_log[pos+43:pos+60]
                    
            f_info.close()
            
           
        # Save information as a class    
        class nc_attributes:
            abstract = select_keys(abstract,len_files)
            author = select_keys(author,len_files)
            author_email = select_keys(author_email,len_files)
            comment = select_keys(comment,len_files)
            history = select_keys(history,len_files)
            instrument = select_keys(instrument,len_files)
            instrument_nominal_depth = select_keys(instrument_nominal_depth,len_files)
            instrument_serial_number = select_keys(instrument_serial_number,len_files)
            local_time_zone = select_keys(local_time_zone,len_files)
            platform_code = select_keys(platform_code,len_files)
            principal_investigator = select_keys(principal_investigator,len_files)
            quality_control_log = select_keys(quality_control_log,len_files)
            time_coverage_start = select_keys(time_coverage_start,len_files)
            time_coverage_end = select_keys(time_coverage_end,len_files)
            toolbox_input_file = select_keys(toolbox_input_file,len_files)
            toolbox_version = select_keys(toolbox_version,len_files)
            geospatial_lat_min = select_keys(geospatial_lat_min,len_files)
            geospatial_lat_max = select_keys(geospatial_lat_max,len_files)
            geospatial_lon_min = select_keys(geospatial_lon_min,len_files) 
            geospatial_lon_max = select_keys(geospatial_lon_max,len_files)      
            variables = select_keys(variables,len_files)
            var_names = select_keys(var_names,len_files)
            time_units = select_keys(time_units,len_files)
            time_comment = select_keys(time_comment,len_files)
            depth_comment = select_keys(depth_comment,len_files)
            in_water = select_keys(in_water,len_files)
            out_water = select_keys(out_water,len_files)
            files_list = nc_files
    
    
    else:
        
        nc_attributes = 'Does not exist'
        
    return nc_attributes         
    
            
            











