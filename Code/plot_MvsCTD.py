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
    # save CTD times for deployment
    CTD_time = []
    for n in range(len(CTD_f)):  
        if CTD_check[n] == 1:            
            CTD_time.append(CTD_times[n])    
    CTD_time, unique_index = np.unique(CTD_time, return_index=True)            
    CTD_files = np.asarray(CTD_files) 
    CTD_files = list(CTD_files[unique_index])       
    # return list of unique useful CTD files
    return CTD_files, CTD_time

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
    
def close_data(mooring,CTD,CTD_times,time_diff):
    
    time_range = {}
    TIME_C = {}
    TEMP = {}
    TEMP_QC = {}
    DEPTH = {}
    DEPTH_QC = {}    
    NOM_DEPTH = []
    for n_time in range(len(CTD_times)):
        time_range[0] = CTD_times[n_time] - time_diff
        time_range[1] = CTD_times[n_time] + time_diff
        for n_depth in range(len(mooring)):
            # get data
            data = mooring[n_depth]
            NOM_DEPTH.append(np.int(np.asarray(data.NOMINAL_DEPTH)))
            # convert time to python datetime
            TIME = list(np.asarray(data.TIME))
            TIME_dt = []
            for n in range(len(TIME)):
                TIME_dt.append(dt.datetime.utcfromtimestamp(TIME[n].tolist()/1e9))
            TIME_dt = np.asarray(TIME_dt)
            # get close data
            close_TIME = []
            close_TEMP = []
            close_TEMP_QC = []
            close_DEPTH = []
            close_DEPTH_QC = []             
            for n in range(len(TIME_dt)):
                # for each variable get close data
                if np.any(TIME_dt[n] >= time_range[0] and TIME_dt[n] < time_range[1]):
                    close_TIME.append(TIME_dt[n])
                    close_TEMP.append(data.TEMP[n])
                    close_DEPTH.append(data.DEPTH[n])
                    close_TEMP_QC.append(data.TEMP_quality_control[n])
                    close_DEPTH_QC.append(data.DEPTH_quality_control[n])                    
            # concatenate per time and depth
            TEMP[n_time,n_depth] = xr.concat(close_TEMP,dim='TIME')    
            TEMP_QC[n_time,n_depth] = xr.concat(close_TEMP_QC,dim='TIME')  
            DEPTH[n_time,n_depth] = xr.concat(close_DEPTH,dim='TIME')    
            DEPTH_QC[n_time,n_depth] = xr.concat(close_DEPTH_QC,dim='TIME')
            TIME_C[n_time,n_depth] = list(close_TIME)
    # return variables
    NOM_DEPTH = np.unique(NOM_DEPTH)
    return TIME_C, TEMP, TEMP_QC, DEPTH, DEPTH_QC, NOM_DEPTH

#--------------------------------------------------------------------------------

def bin_data(VAR,DEPTH,NOM_DEPTH):
    
    VAR_m = {}
    DEPTH_m = {}
    TIME_m = {}
    n_t = int(len(VAR)/len(NOM_DEPTH))
    for n_time in range(n_t):
        for n_depth in range(len(NOM_DEPTH)):
            VAR_m[n_time,n_depth] = np.nanmedian(VAR[n_time,n_depth])
            DEPTH_m[n_time,n_depth] = np.nanmedian(DEPTH[n_time,n_depth])
    class binned:
        VAR = VAR_m
        DEPTH = DEPTH_m
    return binned
    
#--------------------------------------------------------------------------------

def make_plot(TEMP,TEMP_QC,DEPTH,DEPTH_QC,CTD,NOM_DEPTH,binned):

    # setup figure
    fig= plt.figure(figsize=(6,8))
    axes= fig.add_axes([0.1,0.1,0.8,0.8])
    # plot data
    # mooring data
    for n_time in range(len(CTD)):
        for n_depth in range(len(NOM_DEPTH)):
            plt.scatter(x=TEMP[n_time,n_depth],y=DEPTH[n_time,n_depth],color='red')
    # CTD data
    for n_prof in range(len(CTD)):                
        plt.plot(CTD[n_prof].TEMP,CTD[n_prof].DEPTH,color='blue')    
    # binned mooring data    
    for n_time in range(len(CTD)):
        for n_depth in range(len(NOM_DEPTH)):
            plt.scatter(x=binned.VAR[n_time,n_depth],y=binned.DEPTH[n_time,n_depth],color='green')        
        
    plt.gca().invert_yaxis() 
    plt.title('Mooring / CTD comparison')
    plt.ylabel('Depth [m]')
    plt.xlabel('Temperature [˚C]')


# %% -----------------------------------------------------------------------------------------------
# Create plot

# define mooring files (TEMP files only)    
IMOS_f = DepDet.atts_files_list
IMOS_files = {}
for n in range(len(IMOS_f)):
    IMOS_f_string = str(IMOS_f[n])
    if IMOS_f_string.find('TEMPERATURE') > 0:
        IMOS_files[n] = IMOS_f[n]
# define time difference between mooring and CTD data 
time_diff = dt.datetime(2019, 4, 13,3,0,0)-dt.datetime(2019, 4, 13,0,0,0); # 3 hours between one another
# get CTD filenames and timings
CTD_files, CTD_times = get_CTD_files(DepDet.start_date,DepDet.end_date,setup.site_name)
# extract mooring and CTD data from files on server
mooring, CTD = get_data(IMOS_files,CTD_files)
# select mooring data close in time to CTD profiles
TIME, TEMP, TEMP_QC, DEPTH, DEPTH_QC, NOM_DEPTH = close_data(mooring,CTD,CTD_times,time_diff)
# bin mooring temperature data 
binned = bin_data(VAR,DEPTH,NOM_DEPTH)
# create figure
make_plot(TEMP,TEMP_QC,DEPTH,DEPTH_QC,CTD,NOM_DEPTH,binned)







