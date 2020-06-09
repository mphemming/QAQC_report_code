#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Fri Jun  5 10:20:49 2020
# Contributers:  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# contact email: m.hemming@unsw.edu.au

# What does this script do?

# o   Get attribute information from netCDF files for selected deployment

# %% -----------------------------------------------------------------------------------------------
# Import packages

import QCreport_paths as paths
import netCDF4 as nc
import glob


# %% -----------------------------------------------------------------------------------------------
# Get attributes

def get_netCDF(path):
    # Get list of netCDF files in folder
    nc_files = glob.glob(path + "*" + paths.site_name + "*" + paths.deployment_file_date_identifier + "*.nc")
    
    # Get netCDF attributes for each file
    for file in range(len(nc_files)):
        f_info = nc.Dataset(nc_files[file])
        
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
        

# %% -----------------------------------------------------------------------------------------------
# get percentage of data flagged

# TBC later...











