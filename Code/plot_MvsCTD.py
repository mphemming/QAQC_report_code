#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Mon Jul 27 09:52:29 2020
# Contributers (code):  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# Contributers (review): Moninya Roughan (NSW-IMS), Tim Austin (NSW-IMOS), Stuart Milburn (NSW-IMOS) 
# contact email: m.hemming@unsw.edu.au

# %% -----------------------------------------------------------------------------------------------
# Import packages
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

import xarray as xr
import numpy as np
from matplotlib import pyplot as plt
import datetime as dt
import glob
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


# %% -----------------------------------------------------------------------------------------------
# Required functions

def get_CTD_files(start_date,end_date,site_name):
    
    # first convert to IMOS datetime
    start_date = dt.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end_date, '%Y-%m-%d')
    # get list of available CTD profiles
    CTD_path = paths.main_path_data + site_name + '/CTD/'
    CTD_f = np.sort(glob.glob(CTD_path + "*" + site_name + "*.nc"))
    # get times of CTD profiles
    CTD_times = []
    CTD_check = []
    CTD_files = []
    for n in range(len(CTD_f)):
        c = CTD_f[n]
        CTD_times.append(dt.datetime.strptime(c[93:101],'%Y%m%d'))
        if dt.datetime.strptime(c[93:101],'%Y%m%d') >= start_date and dt.datetime.strptime(c[93:101],'%Y%m%d') < end_date:
            CTD_files.append(c)
            CTD_check.append(1)
        else:
            CTD_check.append(0) 
    # return list of useful CTD files
    return CTD_files

#--------------------------------------------------------------------------------

def get_data(IMOS_files,CTD_files):
    
    # convert to list
    IMOS_file_list = []
    for n in range(len(IMOS_files)):
        IMOS_file_list.append(IMOS_files[n])
    
    # load in Mooring data
    mooring = []
    for n in range(len(IMOS_files)):
        mooring.append(xr.open_mfdataset(IMOS_file_list[n]))
    # load in CTD data
    CTD = []
    for n in range(len(CTD_files)):
        CTD.append(xr.open_mfdataset(CTD_files[n]))
    # Return data
    return mooring, CTD  

#--------------------------------------------------------------------------------
    
def compare(mooring,CTD,time_diff):
    
    # This is a function to determine mooring data close in space and time to CTD data
    
    

#--------------------------------------------------------------------------------

def make_plot(mooring,CTD):
    
    # This is a function that creates the plot
    
    



# %% -----------------------------------------------------------------------------------------------
# Create plot

start_date = dt.datetime.strptime(start_date, '%Y-%m-%d')
end_date = dt.datetime.strptime(end_date, '%Y-%m-%d')
site_name = setup.site_name
IMOS_files = DepDet.atts_files_list






