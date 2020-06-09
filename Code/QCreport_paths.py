#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Thu Jun  4 13:42:02 2020
# Contributers:  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# contact email: m.hemming@unsw.edu.au

# What does this script do?

# o   Ability to select site, deployment number, and save other info
# o   Defines the directory paths for files/plots used in QCreport
# o   Path strings are called from QCreport.py using functions stored here (e.g. def <name_of_function>)
# o   'return' is required in the functions for the result of the function (i.e. file path strings) to be called in 'QCreport.py'

# Instructions:

# o   Modify the site and deployment number
# o   Modify the paths for your use
# o   PLEASE ENSURE TO INCLUDE FINAL '/' IN YOUR PATHS


# %% -----------------------------------------------------------------------------------------------
# Choose site, deployment, add name of report maker 

site_name = 'BMP070'
deployment = '29'
deployment_file_date_identifier = '1904'
name_of_reportmaker = 'Michael Hemming'

# %% -----------------------------------------------------------------------------------------------
# netCDF files

def ncdir_TEMP():
    netCDF_TEMP_dir = '/Users/Michael/Documents/Work/UNSW/Work/QC_reports/Example_data_BMP070_29/TEMPERATURE/'
    return netCDF_TEMP_dir

def ncdir_CURR():
    netCDF_CURR_dir = '/Users/Michael/Documents/Work/UNSW/Work/QC_reports/Example_data_BMP070_29/CURRENT/'
    return netCDF_CURR_dir

def ncdir_BGC():
    netCDF_BGC_dir = '/Users/Michael/Documents/Work/UNSW/Work/QC_reports/Example_data_BMP070_29/BGC/'
    return netCDF_BGC_dir

# %% -----------------------------------------------------------------------------------------------
# Mooring diagram location

def mddir():
    md_dir = '/Users/Michael/Documents/Work/UNSW/Work/QC_reports/Example_data_BMP070_29/Mooring_Diagram/BMP070_120_mooring_diagram.png'
    return md_dir


# %% -----------------------------------------------------------------------------------------------
# Toolbox plots

def tbdir():
    toolboxplots_dir = '/Users/Michael/Documents/Work/UNSW/Work/QC_reports/Toolbox_Plots/'
    return toolboxplots_dir

# %% -----------------------------------------------------------------------------------------------
# Report saving location

def savedir():
    save_dir = '/Users/Michael/Documents/Work/UNSW/Work/QC_reports/'
    return save_dir