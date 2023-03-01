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
import matplotlib
matplotlib.use('qt5Agg')
from matplotlib import pyplot as plt
import datetime as dt
import glob
# QCreport modules
import QCreport_paths as paths
import QCreport_DeploymentDetails as DepDet
import QCreport_setup as setup

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
    for n in list(IMOS_files):
        IMOS_file_list.append(IMOS_files[n][0])
    
    # load in Mooring data
    mooring = []
    for n in range(len(IMOS_files)):
        ds = xr.open_dataset(IMOS_file_list[n], cache=False).load();
        print(ds.instrument_nominal_depth)
        mooring.append(ds)
        ds.close()
    # load in CTD data
    CTD = []
    for n in range(len(CTD_files)):
        CTD.append(xr.open_mfdataset(CTD_files[n]))
    # Return data
    return mooring, CTD  

#--------------------------------------------------------------------------------
    
def near_data(mooring,CTD,CTD_time,time_diff):
    
    time_range = {}
    TIME_C = {}
    TIME_diff_C = {}
    TEMP = {}
    TEMP_QC = {}
    DEPTH = {}
    DEPTH_QC = {}    
    NOM_DEPTH = []

    time_range[0] = CTD_time - time_diff
    time_range[1] = CTD_time + time_diff
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
        close_TIME_diff = []
        close_TEMP = []
        close_TEMP_QC = []
        close_DEPTH = []
        close_DEPTH_QC = []             
        for n in range(len(TIME_dt)):
            # for each variable get close data
            if np.any(TIME_dt[n] >= time_range[0] and TIME_dt[n] < time_range[1]):
                # use QC'd data
                T = data.TEMP.where(data.TEMP_quality_control == 1,np.nan)
                close_TIME.append(TIME_dt[n])
                t_diff = TIME_dt[n]-CTD_time
                t_diff = abs(int(t_diff.total_seconds() / 60))
                close_TIME_diff.append(t_diff)
                close_TEMP.append(T[n])
                close_DEPTH.append(data.DEPTH[n])
                close_TEMP_QC.append(data.TEMP_quality_control)
                close_DEPTH_QC.append(data.DEPTH_quality_control[n])                    
        # concatenate per time and depth
        TEMP[n_depth] = xr.concat(close_TEMP,dim='TIME')    
        TEMP_QC[n_depth] = xr.concat(close_TEMP_QC,dim='TIME')  
        DEPTH[n_depth] = xr.concat(close_DEPTH,dim='TIME')    
        DEPTH_QC[n_depth] = xr.concat(close_DEPTH_QC,dim='TIME')
        TIME_C[n_depth] = list(close_TIME)
        TIME_diff_C[n_depth] = list(close_TIME_diff)
    # return variables
    NOM_DEPTH = np.unique(NOM_DEPTH)
    return TIME_C, TIME_diff_C, TEMP, TEMP_QC, DEPTH, DEPTH_QC, NOM_DEPTH

#--------------------------------------------------------------------------------

def bin_data(VAR,DEPTH,NOM_DEPTH):
    
    VAR_m = {}
    DEPTH_m = {}
    TIME_m = {}

    for n_depth in range(len(NOM_DEPTH)):
        VAR_m[n_depth] = np.nanmedian(VAR[n_depth])
        DEPTH_m[n_depth] = np.nanmedian(DEPTH[n_depth])
    class binned:
        VAR = VAR_m
        DEPTH = DEPTH_m
    return binned
    
#--------------------------------------------------------------------------------

def make_plot(TIME_diff, TEMP,TEMP_QC,DEPTH,DEPTH_QC,CTD,NOM_DEPTH,binned):

    # setup figure
    fig= plt.figure(figsize=(8,8))
    axes= fig.add_axes([0.1,0.1,0.8,0.8])
    # plot data
    # mooring data
    for n_depth in range(len(NOM_DEPTH)):
        if n_depth == 0:
            sc = plt.scatter(x=TEMP[n_depth].values,y=DEPTH[n_depth],c=np.array(TIME_diff[n_depth]),label='Mooring')
        else:
            plt.scatter(x=TEMP[n_depth].values,y=DEPTH[n_depth],c=np.array(TIME_diff[n_depth]))
    # CTD data
    for n_prof in range(len(CTD)):                  
        ctd = plt.plot(CTD[n_prof].TEMP,CTD[n_prof].DEPTH,color='blue',label='CTD')      
    # binned mooring data    
    for n_depth in range(len(NOM_DEPTH)):
        if n_depth == 0:
            plt.scatter(x=binned.VAR[n_depth],y=binned.DEPTH[n_depth],
                        facecolor='white', edgecolor='black',label='Mooring median')  
        else:
            plt.scatter(x=binned.VAR[n_depth],y=binned.DEPTH[n_depth],
                        facecolor='white', edgecolor='black')     
    cb =  plt.colorbar(sc)    
    cb.set_label('Time difference between mooring and CTD [minutes]',fontsize=16)
    # Set the font size for the tick labels
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    
    plt.legend()
    
    axes.text(14, 80, (''), fontsize=14, backgroundcolor='gray')
        
    plt.gca().invert_yaxis() 
    plt.title('Mooring / CTD comparison',fontsize=16)
    plt.ylabel('Depth [m]',fontsize=16)
    plt.xlabel('Temperature [˚C]',fontsize=16)
    plt.grid()
    plt.tight_layout()
    
    # save figures
    filename = (paths.plots_dir + 'CTDcomparison\\TEMP_' + setup.site_name + '_' + 
                setup.deployment_file_date_identifier + '.png')
    plt.savefig(filename)
    plt.close()
    

# %% -----------------------------------------------------------------------------------------------
# Create plot

# define mooring files (TEMP files only)    
IMOS_f = DepDet.atts_files_list
IMOS_files = {}
for n in range(len(IMOS_f)):
    IMOS_f_string = str(IMOS_f[n])
    if IMOS_f_string.find('TEMPERATURE') > 0:
        IMOS_files[n] = IMOS_f[n]
        
# if available, get CTD profile        
CTD_folder = glob.glob(paths.netCDF_TEMP_dir.replace('TEMPERATURE\\','') + '*CTD*')
identifier = '20' + setup.deployment_file_date_identifier
CTD_file = glob.glob(CTD_folder[0] + '\\*' + identifier + '*FV01*.nc');        

# define time difference between mooring and CTD data 
mooring, CTD = get_data(IMOS_files,CTD_file)
CTD_time = np.datetime64(CTD[0].time_coverage_start).tolist()
time_diff = dt.datetime(2019, 4, 13,1,00,0)-dt.datetime(2019, 4, 13,0,0,0); # 1 hours between one another
TIME, TIME_diff, TEMP, TEMP_QC, DEPTH, DEPTH_QC, NOM_DEPTH = near_data(mooring,CTD,CTD_time,time_diff)
# bin mooring temperature data 
binned = bin_data(TEMP,DEPTH,NOM_DEPTH)
# create figure
make_plot(TIME_diff, TEMP,TEMP_QC,DEPTH,DEPTH_QC,CTD,NOM_DEPTH,binned)











