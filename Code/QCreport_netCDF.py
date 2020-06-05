#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Fri Jun  5 10:20:49 2020
# Contributers:  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# contact email: m.hemming@unsw.edu.au

# What does this script do?

# o   Get attribute information from netCDF file

# -----------------------------------------------------------------------------------------------
# Import packages

import QCreport_paths as paths
import netCDF4 as nc
import glob


# global attributes
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

# parameter attributes



def get_netCDF(path):
    # Get list of netCDF files in folder
    nc_files = glob.glob(path + "*.nc")
    
    # Get netCDF attributes for each file
    for file in range(len(nc_files)):
        f_info = nc.Dataset(nc_files[file])
        abstract[file] = f_info.abstract
        author[file] = f_info.author
        
       
    # Save information as a class    
    class nc_attributes:
        abstract = abstract  
        author = author
        
    return nc_attributes
        

TIME = f_info.variables['TIME']
