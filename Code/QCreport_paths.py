#!\\usr\\bin\\env python3
# -*- coding: utf-8 -*-

# Created on Thu Jun  4 13:42:02 2020
# Contributers (code):  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# Contributers (review): Moninya Roughan (NSW-IMS), Tim Austin (NSW-IMOS), Stuart Milburn (NSW-IMOS) 
# contact email: m.hemming@unsw.edu.au

# What does this script do?

# o   Ability to select site, deployment number, and save other info
# o   Defines the directory paths for files\\plots used in QCreport
# o   Path strings are called from QCreport.py using functions stored here (e.g. def <name_of_function>)
# o   'return' is required in the functions for the result of the function (i.e. file path strings) to be called in 'QCreport.py'

# Instructions:

# o   Modify the site and deployment number
# o   Modify the paths for your use
# o   PLEASE ENSURE TO INCLUDE FINAL '\\' IN YOUR PATHS

# %% -----------------------------------------------------------------------------------------------
# Import modules

import os
import QCreport_setup as setup

#------------------------------------------------------------
# Information 
#-------------

# These are modules required to get current path information

#------------------------------------------------------------

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
# Determine main paths
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# get current directory
pwd_info = os.getcwd()
# depending on where working, create path
if ('home' in pwd_info) == 0:
    # working from Windows using mounted sci-maths-ocean
    starting_path = 'Z:\\home\\z3526971\\'
else:
    # Working from campus \\ ssh login
    z = pwd_info.find('z')
    zuser = pwd_info[z:z+8]
    starting_path = '\\home\\' + zuser
# remaining part of path
ending_path = 'sci-maths-ocean\\IMOS\\Moorings_Report\\Automatic_reporting\\'
ending_path_data = 'sci-maths-ocean\\IMOS\\DATA\\MOORINGS\\PROCESSED_2_5\\'
# check if missing '\\' at end of strings
if ('\\' in starting_path[-1]) == 0:
    starting_path = starting_path + '\\'
if ('\\' in ending_path[-1]) == 0:
    ending_path = ending_path + '\\'    
# complete path
main_path = starting_path + ending_path
main_path_data = starting_path + ending_path_data


# working directory

# account = 'z3526971'
account = 'mphem'

working_dir = ('C:\\Users\\' + account + '\\OneDrive - UNSW\\Work\\QC_reports\\')

# temporary directory

TEMPORARY_dir = 'C:\\Users\\' + account + '\\OneDrive - UNSW\\Work\\QC_reports\\TEMPORARY\\'

#------------------------------------------------------------
# Information 
#-------------
        
# Determine where script is being run from (MAC or server). 
# Does not work for windows for the time being. Gets
# the main path for folder containing code etc. and data

#------------------------------------------------------------

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# %% -----------------------------------------------------------------------------------------------
# netCDF files
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# Functions to choose correct paths to netCDF files
#------------------------------------------------------------
def ncdir_TEMP(site_name):
    switcher = {
            'BMP070': main_path_data + 'BMP070\\TEMPERATURE\\',
            'BMP120': main_path_data + 'BMP120\\TEMPERATURE\\',
            'CH050': main_path_data + 'CH050\\TEMPERATURE\\',
            'CH070': main_path_data + 'CH070\\TEMPERATURE\\',
            'CH100': main_path_data + 'CH100\\TEMPERATURE\\',
            'PH100': main_path_data + 'PH100\\TEMPERATURE\\',
            'SYD100': main_path_data + 'SYD100\\TEMPERATURE\\',
            'SYD140': main_path_data + 'SYD140\\TEMPERATURE\\',
            'ORS065': main_path_data + 'ORS065\\TEMPERATURE\\',
            }

    netCDF_TEMP_dir = switcher.get(site_name)
    return netCDF_TEMP_dir
# Functions to choose correct paths to netCDF files
#------------------------------------------------------------
def ncdir_SBE37(site_name):
    switcher = {
            'BMP070': main_path_data + 'BMP070\\SBE37\\',
            'BMP120': main_path_data + 'BMP120\\SBE37\\',
            'CH050': main_path_data + 'CH050\\SBE37\\',
            'CH070': main_path_data + 'CH070\\SBE37\\',
            'CH100': main_path_data + 'CH100\\SBE37\\',
            'PH100': main_path_data + 'PH100\\SBE37\\',
            'SYD100': main_path_data + 'SYD100\\SBE37\\',
            'SYD140': main_path_data + 'SYD140\\SBE37\\',
            'ORS065': main_path_data + 'ORS065\\SBE37\\',
            }

    netCDF_SBE37_dir = switcher.get(site_name)
    return netCDF_SBE37_dir
#------------------------------------------------------------
def ncdir_CURR(site_name):
    switcher = {
            'BMP070': main_path_data + 'BMP070\\CURRENT\\',
            'BMP120': main_path_data + 'BMP120\\CURRENT\\',
            'CH050': main_path_data + 'CH050\\CURRENT\\',
            'CH070': main_path_data + 'CH070\\CURRENT\\',
            'CH100': main_path_data + 'CH100\\CURRENT\\',
            'PH100': main_path_data + 'PH100\\CURRENT\\',
            'SYD100': main_path_data + 'SYD100\\CURRENT\\',
            'SYD140': main_path_data + 'SYD140\\CURRENT\\',
            'ORS065': main_path_data + 'ORS065\\CURRENT\\',
            }

    netCDF_CURR_dir = switcher.get(site_name)
    return netCDF_CURR_dir
#------------------------------------------------------------
def ncdir_BGC(site_name):
    switcher = {
            'BMP070': main_path_data + 'BMP070\\BGC\\',
            'BMP120': main_path_data + 'BMP120\\BGC\\',
            'CH050': main_path_data + 'CH050\\BGC\\',
            'CH070': main_path_data + 'CH070\\BGC\\',
            'CH100': main_path_data + 'CH100\\BGC\\',
            'PH100': main_path_data + 'PH100\\BGC\\',
            'SYD100': main_path_data + 'SYD100\\BGC\\',
            'SYD140': main_path_data + 'SYD140\\BGC\\',
            'ORS065': main_path_data + 'ORS065\\BGC\\',
            }

    netCDF_BGC_dir = switcher.get(site_name)
    return netCDF_BGC_dir
#------------------------------------------------------------
def ncdir_CTD(site_name):
    switcher = {
            'BMP070': main_path_data + 'BMP070\\CTD\\',
            'BMP120': main_path_data + 'BMP120\\CTD\\',
            'CH050': main_path_data + 'CH050\\CTD\\',
            'CH070': main_path_data + 'CH070\\CTD\\',
            'CH100': main_path_data + 'CH100\\CTD\\',
            'PH100': main_path_data + 'PH100\\CTD\\',
            'SYD100': main_path_data + 'SYD100\\CTD\\',
            'SYD140': main_path_data + 'SYD140\\CTD\\',
            'ORS065': main_path_data + 'ORS065\\CTD\\',
            }

    netCDF_CTD_dir = switcher.get(site_name)
    return netCDF_CTD_dir
#------------------------------------------------------------
# get netCDF paths
netCDF_TEMP_dir = ncdir_TEMP(setup.site_name) 
netCDF_SBE37_dir = ncdir_SBE37(setup.site_name) 
netCDF_CURR_dir = ncdir_CURR(setup.site_name) 
netCDF_BGC_dir = ncdir_BGC(setup.site_name) 
netCDF_CTD_dir = ncdir_CTD(setup.site_name) 

#------------------------------------------------------------
# Information 
#-------------
        
# Select paths for site selected

#------------------------------------------------------------

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# %% -----------------------------------------------------------------------------------------------
# Mooring diagram location
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# Function to choose correct path to mooring diagram
#------------------------------------------------------------
def mddir(site_name):
    switcher = {
            'BMP070': main_path + 'Mooring_Diagrams\\BMP070\\BMP070_120_mooring_diagram.png',
            'BMP120': main_path + 'Mooring_Diagrams\\BMP120\\BMP070_120_mooring_diagram.png',
            'CH050': main_path + 'Mooring_Diagrams\\CH050\\',
            'CH070': main_path + 'Mooring_Diagrams\\CH070\\',
            'CH100': main_path + 'Mooring_Diagrams\\CH100\\',
            'PH100': main_path + 'Mooring_Diagrams\\PH100\\',
            'SYD100': main_path + 'Mooring_Diagrams\\SYD100\\',
            'SYD140': main_path + 'Mooring_Diagrams\\SYD140\\',
            'ORS065': main_path + 'Mooring_Diagrams\\ORS065\\',
            }

    md_dir = switcher.get(site_name)
    return md_dir

#------------------------------------------------------------
# get Mooring diagram path
md_dir = mddir(setup.site_name) 

#------------------------------------------------------------
# Information 
#-------------
        
# Select paths for site mooring diagram file

#------------------------------------------------------------

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# %% -----------------------------------------------------------------------------------------------
# Deployment Photographs location
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# Function to choose correct path to Deployment photographs
#------------------------------------------------------------
def dppdir(site_name):
    switcher = {
            'BMP070': main_path + 'Deployment_Photographs\\BMP070\\Deployment_' + setup.deployment + '\\',
            'BMP120': main_path + 'Deployment_Photographs\\BMP120\\Deployment_' + setup.deployment +'\\',
            'CH050': main_path + 'Deployment_Photographs\\CH050\\Deployment_' + setup.deployment +'\\',
            'CH070': main_path + 'Deployment_Photographs\\CH070\\Deployment_' + setup.deployment +'\\',
            'CH100': main_path + 'Deployment_Photographs\\CH100\\Deployment_' + setup.deployment +'\\',
            'PH100': main_path + 'Deployment_Photographs\\PH100\\Deployment_' + setup.deployment +'\\',
            'SYD100': main_path + 'Deployment_Photographs\\SYD100\\Deployment_' + setup.deployment +'\\',
            'SYD140': main_path + 'Deployment_Photographs\\SYD140\\Deployment_' + setup.deployment +'\\',
            'ORS065': main_path + 'Deployment_Photographs\\ORS065\\Deployment_' + setup.deployment +'\\',
            }

    dpp_dir = switcher.get(site_name)
    return dpp_dir

#------------------------------------------------------------
# get Mooring diagram path
dpp_dir = dppdir(setup.site_name) 
    
#------------------------------------------------------------
# Information 
#-------------
        
# Select paths for deployment photographs

#------------------------------------------------------------    

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# %% -----------------------------------------------------------------------------------------------
# Toolbox plots
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
  
# Function to choose correct path to Deployment photographs
#------------------------------------------------------------
def tbdir(site_name):
    switcher = {
            'BMP070': main_path_data + 'BMP070\\PLOTS_TOOLBOX\\',
            'BMP120': main_path_data + 'BMP120\\PLOTS_TOOLBOX\\',
            'ORS065': main_path_data + 'ORS065\\PLOTS_TOOLBOX\\',
            'CH050': main_path_data + 'CH050\\PLOTS_TOOLBOX\\',
            'CH070': main_path_data + 'CH070\\PLOTS_TOOLBOX\\',
            'CH100': main_path_data + 'CH100\\PLOTS_TOOLBOX\\',
            'PH100': main_path_data + 'PH100\\PLOTS_TOOLBOX\\',
            'SYD100': main_path_data + 'SYD100\\PLOTS_TOOLBOX\\',
            'SYD140': main_path_data + 'SYD140\\PLOTS_TOOLBOX\\',
            }

    tb_dir = switcher.get(site_name)
    return tb_dir

tb_dir = tbdir(setup.site_name) 

#------------------------------------------------------------
# Information 
#-------------
        
# Select paths for stored Toolbox plots
# Need to update this section when working from the server

#------------------------------------------------------------   

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# %% -----------------------------------------------------------------------------------------------
# get front cover images path
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

cover_dir = main_path + 'Cover_images\\'


# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# %% -----------------------------------------------------------------------------------------------
# plots paths
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# <<<<<<< Updated upstream
# OC_dir = 'C:\\Users\\mphem\\Documents\\Work\\UNSW\QC_reports\\Example_data_BMP070_29\\OceanCurrents\\'
# =======
plots_dir = ('C:\\Users\\' + account + '\\OneDrive - UNSW\\Work\\QC_reports\\plots\\')
# >>>>>>> Stashed changes

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________


# %% -----------------------------------------------------------------------------------------------
# Report saving location
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

def savedir():
#    save_dir = main_path + 'Reports\\'
    save_dir = 'C:\\Users\\mphem\\OneDrive - UNSW\\Work\\QC_reports\\Reports\\'; # for testing
    return save_dir

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# %% -----------------------------------------------------------------------------------------------
# Double-check if paths include '\\' at end (unless a single file)


