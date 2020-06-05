#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Fri Jun  5 10:20:49 2020
# Contributers:  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# contact email: m.hemming@unsw.edu.au

# What does this script do?

# o   Get attribute information from netCDF files for selected deployment

# -----------------------------------------------------------------------------------------------
# Import packages

import QCreport_paths as paths
import netCDF4 as nc
import glob


# -----------------------------------------------------------------------------------------------
# Get attributes

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

def get_netCDF(path):
    # Get list of netCDF files in folder
    nc_files = glob.glob(path + "*.nc")
    
    # Get netCDF attributes for each file
    for file in range(len(nc_files)):
        f_info = nc.Dataset(nc_files[file])
        abstract[file] = f_info.abstract
        author[file] = f_info.author
        author_email[file] = f_info.author_email
        comment[file] = f_info.comment
        history[file] = f_info.history
        instrument[file] = f_info.instrument
        instrument_nominal_depth[file] = f_info.instrument_nominal_depth
        instrument_sample_interval[file] = f_info.instrument_sample_interval
        instrument_serial_number[file] = f_info.instrument_serial_number
        local_time_zone[file] = f_info.local_time_zone
        platform_code[file] = f_info.platform_code
        principal_investigator[file] = f_info.principal_investigator
        quality_control_log[file] = f_info.quality_control_log
        time_coverage_start[file] = f_info.time_coverage_start
        time_coverage_end[file] = f_info.time_coverage_end
        toolbox_input_file[file] = f_info.toolbox_input_file
        toolbox_version[file] = f_info.toolbox_version
        geospatial_lat_min[file] = f_info.geospatial_lat_min
        geospatial_lat_max[file] = f_info.geospatial_lat_max       
        geospatial_lon_min[file] = f_info.geospatial_lon_min    
        geospatial_lon_max[file] = f_info.geospatial_lon_max
        variables[file] = f_info.variables
        var_names[file] = f_info.variables.keys()
        
        # get TIME and DEPTH attributes
        if 'TIME' in var_names[0]:
            tatt = f_info.variables['TIME']
            time_units[file] = tatt.units
            time_comment[file] = tatt.comment
        if 'DEPTH' in var_names[0]:
          Datt = f_info.variables['DEPTH']      
          depth_comment[file] = Datt.comment
       
    # Save information as a class    
    class nc_attributes:
        abstract = abstract  
        author = author
        author_email = author_email
        comment = comment
        history = history
        instrument = instrument
        instrument_nominal_depth = instrument_nominal_depth
        instrument_serial_number = instrument_serial_number
        local_time_zone = local_time_zone
        platform_code = platform_code
        principal_investigator = principal_investigator
        quality_control_log = quality_control_log
        time_coverage_start = time_coverage_start
        time_coverage_end = time_coverage_end
        toolbox_input_file = toolbox_input_file
        toolbox_version = toolbox_version
        geospatial_lat_min = geospatial_lat_min
        geospatial_lat_max = geospatial_lat_max 
        geospatial_lon_min = geospatial_lon_min  
        geospatial_lon_max = geospatial_lon_max       
        variables = variables
        var_names = var_names
        time_units = time_units
        time_comment = time_comment
        depth_comment = depth_comment
        
    return nc_attributes
        

# -----------------------------------------------------------------------------------------------
# get percentage of data flagged

# TBC later...











