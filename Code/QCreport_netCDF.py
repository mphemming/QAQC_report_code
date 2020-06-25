#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Fri Jun  5 10:20:49 2020
# Contributers:  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
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
# QC report modules
import QCreport_paths as paths

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
    date_id = '-' + paths.deployment_file_date_identifier + '-'
    # Get list of netCDF files in folder
    nc_files = glob.glob(path + "*" + paths.site_name + "*" + date_id + "*.nc")
    len_files = len(nc_files)

    if len_files > 0:

        # Get netCDF attributes for each file
        for file in range(len_files):
            f_info = nc.Dataset(nc_files[file])
    
            if hasattr(f_info,'abstract'):
                abstract[file] = f_info.abstract
            else:
                abstract[file] = 'No data'
        
            if hasattr(f_info,'author'):
                author[file] = f_info.author
            else:
                author[file] = 'No data'
                
            if hasattr(f_info,'author_email'):
                author_email[file] = f_info.author_email
            else:
                author_email[file] = 'No data'            
                
            if hasattr(f_info,'comment'):
                comment[file] = f_info.comment
            else:
                comment[file] = 'No data'
                
            if hasattr(f_info,'history'):
                history[file] = f_info.history
            else:
                history[file] = 'No data'            
                
            if hasattr(f_info,'instrument'):
                instrument[file] = f_info.instrument
            else:
                instrument[file] = 'No data'           
    
            if hasattr(f_info,'instrument_nominal_depth'):
                instrument_nominal_depth[file] = f_info.instrument_nominal_depth
            else:
                instrument_nominal_depth[file] = 'No data'
                
            if hasattr(f_info,'instrument_sample_interval'):
                instrument_sample_interval[file] = f_info.instrument_sample_interval
            else:
                instrument_sample_interval[file] = 'No data'
                
            if hasattr(f_info,'instrument_serial_number'):
                instrument_serial_number[file] = f_info.instrument_serial_number
            else:
                instrument_serial_number[file] = 'No data'
    
            if hasattr(f_info,'local_time_zone'):
                local_time_zone[file] = f_info.local_time_zone
            else:
                local_time_zone[file] = 'No data'
    
            if hasattr(f_info,'platform_code'):
                platform_code[file] = f_info.platform_code
            else:
                platform_code[file] = 'No data'            
    
            if hasattr(f_info,'principal_investigator'):
                principal_investigator[file] = f_info.principal_investigator
            else:
                principal_investigator[file] = 'No data'
    
            if hasattr(f_info,'quality_control_log'):
                quality_control_log[file] = f_info.quality_control_log
            else:
                quality_control_log[file] = 'No data'
                
            if hasattr(f_info,'time_coverage_start'):
                time_coverage_start[file] = f_info.time_coverage_start
            else:
                time_coverage_start[file] = 'No data'
                
            if hasattr(f_info,'time_coverage_end'):
                time_coverage_end[file] = f_info.time_coverage_end
            else:
                time_coverage_end[file] = 'No data'
    
            if hasattr(f_info,'toolbox_input_file'):
                toolbox_input_file[file] = f_info.toolbox_input_file
            else:
                toolbox_input_file[file] = 'No data'            
    
            if hasattr(f_info,'toolbox_version'):
                toolbox_version[file] = f_info.toolbox_version
            else:
                toolbox_version[file] = 'No data'
                
            if hasattr(f_info,'geospatial_lat_min'):
                geospatial_lat_min[file] = f_info.geospatial_lat_min
            else:
                geospatial_lat_min[file] = 'No data'
    
            if hasattr(f_info,'geospatial_lat_max'):
                geospatial_lat_max[file] = f_info.geospatial_lat_max
            else:
                geospatial_lat_max[file] = 'No data'
    
            if hasattr(f_info,'geospatial_lon_min'):
                geospatial_lon_min[file] = f_info.geospatial_lon_min
            else:
                geospatial_lon_min[file] = 'No data'
    
            if hasattr(f_info,'geospatial_lon_max'):
                geospatial_lon_max[file] = f_info.geospatial_lon_max
            else:
                geospatial_lon_max[file] = 'No data'            
    
            if hasattr(f_info,'variables'):
                variables[file] = f_info.variables
                var_names[file] = f_info.variables.keys()
            else:
                variables[file] = 'No data'
                var_names[file] = 'No data'    
            
            # get TIME and DEPTH attributes
            if 'TIME' in var_names[0]:
                tatt = f_info.variables['TIME']
                time_units[file] = tatt.units
                time_comment[file] = tatt.comment
            if 'DEPTH' in var_names[0]:
              Datt = f_info.variables['DEPTH']      
              depth_comment[file] = Datt.comment
              
            # get times in/out water
            if hasattr(f_info,'quality_control_log'):
                if 'imosInOutWaterQC' in f_info.quality_control_log:
                    f_string = str(f_info.quality_control_log)
                    pos = f_string.find('imosInOutWaterQC')
                    in_water[file] = f_info.quality_control_log[pos+20:pos+37]
                    out_water[file] = f_info.quality_control_log[pos+43:pos+60]
            
           
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
    
    
    else:
        
        nc_attributes = 'Does not exist'
        
    return nc_attributes         
    
            
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

    











