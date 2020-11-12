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
import netCDF4 as nc
import glob
import numpy as np
# QC report modules
import QCreport_paths as paths
import QCreport_setup as setup

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
            nd.append(ncf[find_nd-2:find_nd])
        nd_sorted = np.sort(nd)
        # shift file order around
        nc_files_sorted = []
        for n_sort in range(len_files): 
            for n_file in range(len_files): 
                if '-' + nd_sorted[n_sort] + '_' in nc_files[n_file]:
                    nc_files_sorted.append(nc_files[n_file])
        nc_files = nc_files_sorted
        len_files = len(nc_files)

    if len_files > 0:

        # Get netCDF attributes for each file
        for n_file in range(len_files):
            f_info = nc.Dataset(nc_files[n_file])
    
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
                time_units[n_file] = tatt.units
                time_comment[n_file] = tatt.comment
            if 'DEPTH' in var_names[0]:
              Datt = f_info.variables['DEPTH']      
              depth_comment[n_file] = Datt.comment
              
            # get times in/out water
            if hasattr(f_info,'quality_control_log'):
                if 'imosInOutWaterQC' in f_info.quality_control_log:
                    f_string = str(f_info.quality_control_log)
                    pos = f_string.find('imosInOutWaterQC')
                    in_water[n_file] = f_info.quality_control_log[pos+20:pos+37]
                    out_water[n_file] = f_info.quality_control_log[pos+43:pos+60]
            
           
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
    
            
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# %% -----------------------------------------------------------------------------------------------
# Create Thredds OPeNDAP links for report table
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________   
files = {}
# get netCDF filenames from server
files[0] = get_netCDF(paths.netCDF_TEMP_dir)
files[1] = get_netCDF(paths.netCDF_SBE37_dir)
files[2] = get_netCDF(paths.netCDF_CTD_dir)
files[3] = get_netCDF(paths.netCDF_CURR_dir)
files[4] = get_netCDF(paths.netCDF_BGC_dir)
# check whether files exist
# Select files available
files_avail = []
for n_check in range(len(files)):
    if type(files[n_check]) != str:
        f = list(files[n_check].files_list)
        for n_items in range(len(f)):
            files_avail.append(f[n_items])
# Create Thredds OPeNDAP links
first_part = 'http://thredds.aodn.org.au/thredds/dodsC/IMOS/ANMN/NSW/'
# combine string parts to create thredds links
OPeNDAP_links = []
for n_files in range(len(files_avail)):
    fname = files_avail[n_files]
    # find point in string where 'PROCESSED_2_5/'
    find_start = fname.find('2_5/')
    OPeNDAP_string = first_part + fname[find_start+67:]
    OPeNDAP_string = OPeNDAP_string.replace('\\', '/')
    OPeNDAP_links.append(OPeNDAP_string)
            















