#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Thu Jan 12 11:57:03 2023
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
import matplotlib.dates as mdates
import glob
import re
import requests
import datetime
# QCreport modules
import QCreport_paths as paths
import QCreport_DeploymentDetails as DepDet
import QCreport_setup as setup
from scipy.signal import savgol_filter
import datetime
import seaborn as sns
import pandas as pd

# %% -----------------------------------------------------------------------------------------------
# Function to get LTSP filename
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

def getLTSPfilenames(node,site,folder):
     res = requests.get(
         'https://thredds.aodn.org.au/thredds/catalog/IMOS/ANMN/' + node + '/' + site + '/' + str(folder) + '/catalog.html')
     txt = res.text
     # identify file names
     start_file = []
     end_file = []
     files = []
     # get start and end locations of file names in text
     for m in re.finditer('IMOS_ANMN-NSW', txt):
         start_file.append(m.start())
     for m in re.finditer(r'\b.nc\b', txt): # r'\b .. \b is used for exact phrase
         end_file.append(m.end())  
     # get file names
     for n_file in range(len(start_file)):
         files.append(txt[start_file[n_file]:end_file[n_file]])       

     # Only use unique file names
     files = np.unique(files)
     locs = []
     for n in range(len(files)):
             locs.append('https://thredds.aodn.org.au/thredds/dodsC/IMOS/ANMN/NSW/' + site + '/' +
                         str(folder) + '/' + files[n])
     
     return files,locs
 
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# %% -----------------------------------------------------------------------------------------------
# Function to get daily climatology
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# SMoothing function for climatology   

def smooth(x,window_len,window='flat'):
    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
    
    see also: 
    
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y



def calc_clim_daily(YEARDAY,VAR):
    
    clim = []
    for n_dy in np.arange(1,366,1):
        check = YEARDAY == n_dy
        clim.append(np.nanmean(VAR[check]))
    
    return clim

def getDailyClim(doy,VAR,DEPTH,depths,day_smooth):

    if 'all depths' not in depths:
        # make space
        clim = np.ones((365,len(depths)),dtype=float)*np.nan
        P10 = np.ones((365,len(depths)),dtype=float)*np.nan
        P50 = np.ones((365,len(depths)),dtype=float)*np.nan
        P90 = np.ones((365,len(depths)),dtype=float)*np.nan
        std = np.ones((365,len(depths)),dtype=float)*np.nan  
        for D in range(len(depths)):
            # only get data in depth bin
            cD = np.logical_and(DEPTH >= depths[D]-3,
                                DEPTH <= depths[D]+3)
            V = VAR[cD]
            dy = doy[cD]
            #day grid for clim
            day_grid = list(range(1,60,1)) + list(range(61,367,1))
            if '[]' not in str(V):
                # calculate climatology
                for day in range(len(day_grid)):
                    d1 = day_grid[day]-6
                    d2 = day_grid[day]+6
                    if d1 > 0 and d2 < 366:
                        c = (dy > d1) & (dy < d2)            
                    if d1 < 0:
                        d1 = d1+366
                        c =  (dy > d1) | (dy < d2)
                    if d2 > 366:
                        d2 = d2-366
                        c = (dy > d1) | (dy < d2) 
                    clim[day,D] = np.nanmean(V[c])
                    P90[day,D] = np.percentile(V[c][np.isfinite(V[c])],90)
                    P50[day,D] = np.percentile(V[c][np.isfinite(V[c])],50)
                    P10[day,D] = np.percentile(V[c][np.isfinite(V[c])],10)
                    std[day,D] = np.nanstd(V[c])
            else:
                clim[day,D] = np.nan
                P90[day,D] = np.nan
                P50[day,D] = np.nan
                P10[day,D] = np.nan
                std[day,D] = np.nan
            sm_array = np.concatenate([clim[:,D],clim[:,D],clim[:,D]])
            sm_array = smooth(sm_array,day_smooth,window='hanning')
            clim[:,D] = sm_array[366+round(day_smooth/2)-1:366+365+round(day_smooth/2)-1]
            sm_array = np.concatenate([P90[:,D],P90[:,D],P90[:,D]])
            sm_array = smooth(sm_array,day_smooth,window='hanning')
            P90[:,D] = sm_array[366+round(day_smooth/2)-1:366+365+round(day_smooth/2)-1]
            sm_array = np.concatenate([P50[:,D],P50[:,D],P50[:,D]])
            sm_array = smooth(sm_array,day_smooth,window='hanning')
            P50[:,D] = sm_array[366+round(day_smooth/2)-1:366+365+round(day_smooth/2)-1]
            sm_array = np.concatenate([P10[:,D],P10[:,D],P10[:,D]])
            sm_array = smooth(sm_array,day_smooth,window='hanning')
            P10[:,D] = sm_array[366+round(day_smooth/2)-1:366+365+round(day_smooth/2)-1]
            sm_array = np.concatenate([std[:,D],std[:,D],std[:,D]])
            sm_array = smooth(sm_array,day_smooth,window='hanning')
            std[:,D] = sm_array[366+round(day_smooth/2)-1:366+365+round(day_smooth/2)-1]
    return clim, P90, P50, P10, std

def calc_clim_monthly(YEARDAY,VAR,DEPTH,depths):
    
    # get months from yeardays
    # Convert yearday to a datetime64 array
    date = []
    month = []
    for n in range(len(YEARDAY)):
        date.append(datetime.datetime(2023, 1, 1) + datetime.timedelta(int(YEARDAY[n]) - 1))
        month.append(date[n].month)
    MNsOut = []
    STDsOut = []
    MAXsOut = []
    MINsOut = []
    # get climatology
    if 'depth-averaged' not in str(depths):
        for n in range(len(depths)):   
            MNs = []
            STDs = []
            maxs = []
            mins = []
            for n_mon in np.arange(1,13,1):
                cm = month == n_mon
                cd = np.logical_and(DEPTH >= depths[n]-3,
                                    DEPTH < depths[n]+3)
                check = np.logical_and(cm,cd)
                if check.sum() != 0:
                    MNs.append(np.nanmean(VAR[check]))
                    STDs.append(np.nanstd(VAR[check]))
                    maxs.append(np.nanmax(VAR[check]))
                    mins.append(np.nanmin(VAR[check]))
                else:
                    MNs.append(np.nan)
                    STDs.append(np.nan)
                    maxs.append(np.nan)
                    mins.append(np.nan)                
            MNsOut.append(MNs)
            STDsOut.append(STDs)
            MAXsOut.append(maxs)
            MINsOut.append(mins)
    else:
        MNs = []
        STDs = []
        maxs = []
        mins = []
        for n_mon in np.arange(1,13,1):
            check = month == n_mon
            if check.sum() != 0:
                MNs.append(np.nanmean(VAR[check]))
                STDs.append(np.nanstd(VAR[check]))
                maxs.append(np.nanmax(VAR[check]))
                mins.append(np.nanmin(VAR[check]))
            else:
                MNs.append(np.nan)
                STDs.append(np.nan)
                maxs.append(np.nan)
                mins.append(np.nan)                
        MNsOut.append(MNs)
        STDsOut.append(STDs)
        MAXsOut.append(maxs)
        MINsOut.append(mins)
    return MNsOut, STDsOut, MAXsOut, MINsOut

def CreateBoxPlot(YEARDAY,VAR,DEPTH,depths,site_name,var_name,save_path):
    # A boxplot is a way to visualize the distribution of a dataset. 
    # It shows the median of the data as a horizontal line inside a rectangle, 
    # which represents the middle 50% of the data (the interquartile range, or IQR). 
    # The upper and lower "whiskers" represent the most extreme data points that are 
    # still within 1.5 times the IQR from the median. Any points outside this range are plotted
    # as individual points, and are considered outliers. Boxplots can be used to compare the 
    # distributions of multiple datasets at once.
    # get monthly climatology
    MNsOut, STDsOut, MAXsOut, MINsOut = calc_clim_monthly(YEARDAY,VAR,DEPTH,depths)
    # get months from yeardays
    # Convert yearday to a datetime64 array
    date = []
    month = []
    for n in range(len(YEARDAY)):
        date.append(datetime.datetime(2023, 1, 1) + datetime.timedelta(int(YEARDAY[n]) - 1))
        month.append(date[n].month)
    if 'depth-averaged' not in str(depths):
        for n in range(len(depths)):   
            plt.figure(figsize=(10,5))
            ax = plt.gca()
            for n_mon in np.arange(1,13,1):
                cm = np.array(month) == n_mon
                cd = np.logical_and(DEPTH >= depths[n]-3,
                                    DEPTH < depths[n]+3)
                check = np.logical_and(cm,cd)
                data = np.array(VAR)[check]
                # plt.scatter(np.ones(check.sum())*n_mon,np.array(VAR)[check],1,c='k')
                ax.boxplot(data[np.isfinite(data)], positions=[n_mon],showfliers=False,showmeans=True)
            plt.show()
        if np.isfinite(data).sum() != 0:
            plt.plot(range(1,13),MNsOut[n],label='Mean Climatology')
            plt.plot(range(1,13),np.array(MNsOut[n])+np.array(STDsOut[n]),
                     c='r',label='Standard Deviation Climatology')   
            plt.plot(range(1,13),np.array(MNsOut[n])-np.array(STDsOut[n]),c='r')   
            plt.plot(range(1,13),MAXsOut[n],label='Maximum')
            plt.plot(range(1,13),MINsOut[n],label='Minimum')
            plt.title(site_name + ' ' + var_name + ' ' + str(int(depths[n])) + 'm depth')
            plt.grid()
            ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
            if np.sum(data < 0) != 0:
                plt.ylabel('Velocity [m S$^{-1}$]')
            else:
                plt.ylabel('Speed [m S$^{-1}$]')
            plt.legend(loc='lower left', ncol=4, frameon=False)
            plt.ylim(np.nanmin(MINsOut[n])-0.5,
                     np.nanmax(MAXsOut[n])+0.5)
        filename = (save_path + 'Climatology\\' + var_name + '_climatology_' + site_name + '_D' + 
                        str(int(depths[n])) + '.png')
        # save figures
        plt.savefig(filename)
        plt.close()
    else:
        plt.figure(figsize=(10,5))
        ax = plt.gca()
        for n_mon in np.arange(1,13,1):
            cm = np.array(month) == n_mon
            data = np.array(VAR)[cm]
            # plt.scatter(np.ones(check.sum())*n_mon,np.array(VAR)[check],1,c='k')
            ax.boxplot(data[np.isfinite(data)], positions=[n_mon],showfliers=False,showmeans=True)
        plt.show() 
        if np.isfinite(data).sum() != 0:
            plt.plot(range(1,13),MNsOut[0],label='Mean Climatology')
            plt.plot(range(1,13),np.array(MNsOut[0])+np.array(STDsOut[0]),
                     c='r',label='Standard Deviation Climatology')   
            plt.plot(range(1,13),np.array(MNsOut[0])-np.array(STDsOut[0]),c='r')   
            plt.plot(range(1,13),MAXsOut[0],label='Maximum')
            plt.plot(range(1,13),MINsOut[0],label='Minimum')
            plt.title(site_name + ' ' + var_name + ' depth-averaged')
            plt.grid()
            ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
            if np.sum(data < 0) != 0:
                plt.ylabel('Velocity [m S$^{-1}$]')
            else:
                plt.ylabel('Speed [m S$^{-1}$]')
            plt.legend(loc='lower left', ncol=4, frameon=False)
            plt.ylim(np.nanmin(MINsOut[0])-0.5,
                     np.nanmax(MAXsOut[0])+0.5)
        filename = (save_path + 'Climatology\\' + var_name + '_climatology_' + site_name + '_depth-averaged.png')
        # save figures
        plt.savefig(filename)
        plt.close()
    plt.close()
        
       
        
def PlotPDFs(YEARDAY,VAR,DEPTH,depths,site_name,var_name,save_path): 
        

    MNsOut, STDsOut, MAXsOut, MINsOut = calc_clim_monthly(YEARDAY,VAR,DEPTH,depths)
    # get months from yeardays
    # Convert yearday to a datetime64 array
    date = []
    month = []
    for n in range(len(YEARDAY)):
        date.append(datetime.datetime(2023, 1, 1) + datetime.timedelta(int(YEARDAY[n]) - 1))
        month.append(date[n].month)
    for n in range(len(depths)):   
        ax = plt.gca()
        df = pd.DataFrame()
        data = []
        months = []
        for n_mon in np.arange(1,13,1):
            cm = np.array(month) == n_mon
            cd = np.logical_and(DEPTH >= depths[n]-3,
                                DEPTH < depths[n]+3)
            check = np.logical_and(cm,cd)
            data.append(np.array(VAR)[check])
            months.append(np.ones(np.size(data[n_mon-1]))*n_mon)
        if np.isfinite(data[0]).sum() != 0:
            # Create data frame
            df = pd.DataFrame({(site_name + ' ' + str(int(depths[n])) + 'm Month'): np.concatenate(months), (var_name + ' [m s$^{-1}$]'): np.concatenate(data)})
        
            # create the plot
            sns.displot(data=df, x=(var_name + ' [m s$^{-1}$]'), 
                            col=(site_name + ' ' + str(int(depths[n])) + 'm Month'), 
                            col_wrap=4, kde=True)
            # save figures
            filename = (save_path + 'Climatology\\' + var_name + '_PDFs_' + site_name + '_D' + 
                            str(int(depths[n])) + '.png')
            plt.savefig(filename)
            plt.close()
        plt.close()
        

# %% -----------------------------------------------------------------------------------------------
# Load LTSP for the site, determine depths to compare
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# %% 
# get temperature and vel LTSP filename
files = glob.glob(paths.TEMPORARY_dir + '*.nc');
for f in files:
    if 'TEMP-aggregated-timeseries' in f:
        file2use = f
    if 'velocity-gridded' in f:
        file2useVelGridded = f


# Load the Temp data product
# _,file_loc = getLTSPfilenames('NSW',setup.site_name,'gridded_timeseries')
agg_TEMP = xr.open_dataset(file2use,cache=False).load()
agg_T = agg_TEMP.TEMP.values; 
agg_T_QC = agg_TEMP.TEMP_quality_control.values; 
agg_D = agg_TEMP.DEPTH.values;
agg_D_QC = agg_TEMP.DEPTH_quality_control.values; 
agg_t = agg_TEMP.TIME.values;
# use 'good' data only
c = np.logical_or(agg_T_QC != 1,
                   agg_D_QC != 1)
agg_T[c] = np.nan
agg_D[c] = np.nan

# get nominal depths, time, temp and depth of deployment files
IMOS_files = DepDet.attributes_TEMP.files_list
NDs = []
Ds = []
Ts = []
ts = []

for f in IMOS_files:
    NDs.append(xr.open_dataset(f).instrument_nominal_depth)
    D = xr.open_dataset(f).DEPTH.values;
    D_QC = xr.open_dataset(f).DEPTH_quality_control.values;
    D[D_QC != 1] = np.nan
    t = xr.open_dataset(f).TIME.values;
    T = xr.open_dataset(f).TEMP.values;
    T_QC = xr.open_dataset(f).TEMP_quality_control.values;
    T[T_QC != 1] = np.nan
    Ds.append(D)
    Ts.append(T)
    ts.append(t)
    
# get actual depth range for these deployment files
D_range = []
for n in range(len(NDs)):
    D_range.append(np.round([np.percentile(Ds[n][np.isfinite(Ds[n])],5), 
              np.percentile(Ds[n][np.isfinite(Ds[n])],95)],2))

# %% Velocity

# Load the Vel gridded data product
grid_VEL = xr.open_dataset(file2useVelGridded,cache=False).load()

# function to rotate velocity
def rotateVel(U,V,site_name):
    
    # CH070: Calc using mean of all deployments as of Sept 2016, 7 years / 20 in book chapter
    # CH100: Calc using mean of all deployments as of Sept 2016, ~7 years / 20 in book chapter
    # ORS065: Calc using mean of all deployments as of Sept 2016, ~8.5 years / 16 in book chapter
    # SYD100 and SYD140: Calc using mean of all deployments as of Sept 2016, 8 years
    # PH100: Calc using mean of all deployments as of Sept 2016, 5 years / 33 in book chapter
    # BMP070: 358 Calc using mean of all deployments as of Sept 2016, 425 days
    # BMP090: 348 Calc using mean of all deployments as of Sept 2016, 134 days / 15 in book chapter
    # BMP120: Calc using mean of all deployments as of Sept 2016, 587 days / 15 in book chapter
    
    angles = {'CH070': -18,
              'CH0100': -18,
              'ORS065': -15,
              'SYD100': -19,
              'SYD140': -24,
              'PH100': -36,
              'BMP070': +2,
              'BMP090': +12,
              'BMP120': -1,
              'testing': 90}
    
    # get current direction
    direction = np.arctan2(U.values, V.values) * 180 / np.pi
    ang = angles[site_name]
    new_direction = direction + ang
    new_direction[new_direction < 0] = 360-np.abs(new_direction[new_direction < 0])
    # get current speed
    CSPD = np.sqrt((U.values**2) + (V.values**2))
    # get rotated U and V
    Urotated = CSPD*np.sin(np.deg2rad(new_direction));
    Vrotated = CSPD*np.cos(np.deg2rad(new_direction));

    return Urotated,Vrotated,CSPD,new_direction,ang




Urotated,Vrotated,CSPD,new_direction,ang = rotateVel(grid_VEL.UCUR,
                                                     grid_VEL.VCUR,
                                                     setup.site_name)

grid_VCUR = Vrotated.flatten(); 
grid_UCUR = Urotated.flatten(); 
grid_D = np.tile(grid_VEL.DEPTH.values,[len(grid_VEL.TIME.values),1]).flatten()
grid_t = np.tile(grid_VEL.TIME.values,[len(grid_VEL.DEPTH.values),1]).transpose().flatten()

########################################################################
# testing that the rotation works
########################################################################
# U = grid_VEL.UCUR; U.values = np.ones([np.size(U.values,0),np.size(U.values,1)])*0;
# V = grid_VEL.VCUR; V.values = np.ones([np.size(V.values,0),np.size(V.values,1)])*-1;
# Urotated,Vrotated,CSPD,new_direction,ang = rotateVel(U,V,
#                                                      'testing')
# Testing confirms that rotation works! :)
########################################################################
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# %% -----------------------------------------------------------------------------------------------
# Create timeseries figure
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

for n in range(len(NDs)):
    
    plt.figure(figsize=(10,5))
    
    # plot the historical record for this depth range
    c = np.logical_and(agg_D >= D_range[n][0],
                       agg_D < D_range[n][1])
    plt.scatter(agg_t[c],agg_T[c],2,label='Historical')
    # plot the deployment
    plt.scatter(ts[n],Ts[n],2,label='This Deployment')
    # appearance
    plt.legend(loc='lower left',fontsize=14,ncol=2)
    plt.show()
    plt.grid()
    plt.ylabel('Temperature [$^\circ$C]',fontsize=16)
    plt.title('Deployment: ' + setup.deployment_file_date_identifier + ', Nominal Depth: ' +
              str(NDs[n]) +' m, depth range: ' + str(D_range[n][0]) + ' - ' + 
              str(D_range[n][1]) + ' m',fontsize=16)
    # Set the font size for the tick labels
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    if np.nanmax(ts[n]) > np.nanmax(agg_t):
        plt.xlim(np.nanmin(agg_t)-np.timedelta64(365,'D'),np.nanmax(ts[n])+np.timedelta64(365,'D'))
    else:
        plt.xlim(np.nanmin(agg_t)-np.timedelta64(365,'D'),np.nanmax(agg_t)+np.timedelta64(365,'D'))
        
    # save figures
    filename = (paths.plots_dir + 'TimeSeries\\TEMP_' + setup.site_name + '_' + setup.deployment_file_date_identifier + '_D' + 
                    str(NDs[n]) + '.png')
    plt.savefig(filename)
    plt.close()
    
    

# %% -----------------------------------------------------------------------------------------------
# Create climatology figures
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# %% Temperature

# use data subsets as aggregated data set too large
agg_t = agg_t[0::10]
agg_T = agg_T[0::10]
agg_D = agg_D[0::10]

# get gridded date elements and year day 
date_string = np.datetime_as_string(agg_t,unit='s') # convert datetime64 to string format
date_elements = []
yearday = []
for nt in range(len(date_string)):
    date_elements.append(datetime.datetime.strptime(date_string[nt], "%Y-%m-%dT%H:%M:%S"))
    y = date_elements[nt].year
    m = date_elements[nt].month
    d = date_elements[nt].day
    yearday.append(datetime.datetime(y,m,d).timetuple().tm_yday)
# get deployment date elements and year day 

# # sort out depths
NDord = np.argsort(NDs)
NDsorted = np.array(NDs)[NDord]

# Get daily climatology
T_MN_31, T_P90_31, T_P50_31, T_P10_31, VCUR_std_31 = getDailyClim(np.array(yearday),agg_T,
                                            agg_D,np.array(NDs),31)

for n in range(len(NDs)):
    
    plt.figure(figsize=(10,5))
    # plot the historical record for this depth range
    c = np.logical_and(agg_D >= D_range[n][0],
                       agg_D < D_range[n][1])
    plt.scatter(np.array(yearday)[c],agg_T[c],2,label='Historical',color='gray')
    # plot the deployment
    # get yearday per depth level
    date_elements_dep = []
    yearday_dep = []
    for nt in range(len(ts[n])):
        date_elements_dep.append(datetime.datetime.strptime(np.datetime_as_string(ts[n][nt],unit='s'), "%Y-%m-%dT%H:%M:%S"))
        y = date_elements_dep[nt].year
        m = date_elements_dep[nt].month
        d = date_elements_dep[nt].day
        yearday_dep.append(datetime.datetime(y,m,d).timetuple().tm_yday)
    
    plt.scatter(yearday_dep,Ts[n],2,label='This Deployment',color='g')
    plt.plot(T_MN_31[:,n],'k',label='Mean')
    plt.plot(T_P90_31[:,n],'r',label='90th Percentile')
    plt.plot(T_P10_31[:,n],'b',label='10th Percentile')
    
    # appearance
    plt.legend(loc='lower left',fontsize=14,ncol=3)
    plt.show()
    plt.grid()
    plt.ylabel('Temperature [$^\circ$C]',fontsize=16)
    plt.title('Deployment: ' + setup.deployment_file_date_identifier + ', Nominal Depth: ' +
              str(NDs[n]) +' m, depth range: ' + str(D_range[n][0]) + ' - ' + str(D_range[n][1]) + 
              ' m',fontsize=16)
    plt.ylim([np.nanmin(agg_T[c])-2,np.nanmax(agg_T[c])+1])
    # Set the font size for the tick labels
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    # format x ticks to show the months instead of yearday
    month_fmt = mdates.DateFormatter('%b')
    ax = plt.gca()
    ax.xaxis.set_major_formatter(month_fmt)
    # save figures
    filename = (paths.plots_dir + 'Climatology\\TEMP_climatology_' + setup.site_name + '_' + setup.deployment_file_date_identifier + '_D' + 
                    str(NDs[n]) + '.png')
    plt.savefig(filename)
    plt.close()
    
# %% Velocity

# %% VCUR

# # get gridded date elements and year day 
# date_string = np.datetime_as_string(grid_t,unit='s') # convert datetime64 to string format
# date_elements = []
# yearday = []
# for nt in range(len(date_string)):
#     date_elements.append(datetime.datetime.strptime(date_string[nt], "%Y-%m-%dT%H:%M:%S"))
#     y = date_elements[nt].year
#     m = date_elements[nt].month
#     d = date_elements[nt].day
#     yearday.append(datetime.datetime(y,m,d).timetuple().tm_yday)

# # sort out depths
# NDord = np.argsort(NDs)
# NDsorted = np.array(NDs)[NDord]

# # get climatology
# VCUR_MN_31, VCUR_P90_31, VCUR_P50_31, VCUR_P10_31, VCUR_std_31 = getDailyClim(np.array(yearday),np.array(grid_VCUR),
#                                             np.array(grid_D),np.array(NDsorted),31)

# for D in range(len(NDsorted)):
    
#     plt.figure(figsize=(10,5))

#     # plot the historical record for this depth range
#     c = np.logical_and(grid_D >= D_range[D][0],
#                         grid_D < D_range[D][1])
#     if np.sum(c) != 0:
#         plt.scatter(np.array(yearday)[c],grid_VCUR[c],2,label='Historical')
        
#         # plot climatology
#         plt.plot(VCUR_MN_31[:,D],'k',label='Climatology mean (31-day smoothed)')
#         plt.plot(VCUR_MN_31[:,D]+VCUR_std_31[:,D],'r',label='Climatology std. dev. (31-day smoothed)')
#         plt.plot(VCUR_MN_31[:,D]-VCUR_std_31[:,D],'r')
        
#         # plot the deployment
#         # get yearday per depth level
#         ct = np.logical_and(grid_t >= np.datetime64(DepDet.start_date),
#                             grid_t < np.datetime64(DepDet.end_date))
#         cc = np.logical_and(c,ct)
        
#         plt.scatter(np.array(yearday)[cc],grid_VCUR[cc],2,label='This Deployment')
#         # appearance
#         plt.legend(loc='lower left',fontsize=14,ncol=2)
#         plt.show()
#         plt.grid()
#         plt.ylabel('VCUR [m s$^{-1}$]',fontsize=16)
#         plt.title('Deployment: ' + setup.deployment_file_date_identifier + ', Nominal Depth: ' +
#                   str(NDsorted[D]) +' m, depth range: ' + str(D_range[D][0]) + ' - ' + str(D_range[D][1]) + 
#                   ' m',fontsize=16)
#         # Set the font size for the tick labels
#         plt.xticks(fontsize=16)
#         plt.yticks(fontsize=16)
#         # format x ticks to show the months instead of yearday
#         month_fmt = mdates.DateFormatter('%b')
#         ax = plt.gca()
#         ax.xaxis.set_major_formatter(month_fmt)
#         # save figures
#         filename = (paths.plots_dir + 'Climatology\\VCUR_climatology_' + setup.site_name + '_' + setup.deployment_file_date_identifier + '_D' + 
#                         str(NDsorted[D]) + '.png')
#         plt.savefig(filename)
#         plt.close()
#     plt.close()
        
    
# %% UCUR

# # get gridded date elements and year day 
# date_string = np.datetime_as_string(grid_t,unit='s') # convert datetime64 to string format
# date_elements = []
# yearday = []
# for nt in range(len(date_string)):
#     date_elements.append(datetime.datetime.strptime(date_string[nt], "%Y-%m-%dT%H:%M:%S"))
#     y = date_elements[nt].year
#     m = date_elements[nt].month
#     d = date_elements[nt].day
#     yearday.append(datetime.datetime(y,m,d).timetuple().tm_yday)

# # sort out depths
# NDord = np.argsort(NDs)
# NDsorted = np.array(NDs)[NDord]

# # get climatology
# UCUR_MN_31, UCUR_P90_31, UCUR_P50_31, UCUR_P10_31, UCUR_std_31 = getDailyClim(np.array(yearday),np.array(grid_UCUR),
#                                            np.array(grid_D),np.array(NDsorted),31)

# for D in range(len(NDsorted)):
    
#     plt.figure(figsize=(10,5))

#     # plot the historical record for this depth range
#     c = np.logical_and(grid_D >= D_range[D][0],
#                        grid_D < D_range[D][1])
#     if np.sum(c) != 0:
#         plt.scatter(np.array(yearday)[c],grid_UCUR[c],2,label='Historical')
        
#         # plot climatology
#         plt.plot(UCUR_MN_31[:,D],'k',label='Climatology mean (31-day smoothed)')
#         plt.plot(UCUR_MN_31[:,D]+UCUR_std_31[:,D],'r',label='Climatology std. dev. (31-day smoothed)')
#         plt.plot(UCUR_MN_31[:,D]-UCUR_std_31[:,D],'r')
        
#         # plot the deployment
#         # get yearday per depth level
#         ct = np.logical_and(grid_t >= np.datetime64(DepDet.start_date),
#                             grid_t < np.datetime64(DepDet.end_date))
#         cc = np.logical_and(c,ct)
        
#         plt.scatter(np.array(yearday)[cc],grid_UCUR[cc],2,label='This Deployment')
#         # appearance
#         plt.legend(loc='lower left',fontsize=14,ncol=2)
#         plt.show()
#         plt.grid()
#         plt.ylabel('UCUR [m s$^{-1}$]',fontsize=16)
#         plt.title('Deployment: ' + setup.deployment_file_date_identifier + ', Nominal Depth: ' +
#                   str(NDsorted[D]) +' m, depth range: ' + str(D_range[D][0]) + ' - ' + str(D_range[D][1]) + 
#                   ' m',fontsize=16)
#         # Set the font size for the tick labels
#         plt.xticks(fontsize=16)
#         plt.yticks(fontsize=16)
#         # format x ticks to show the months instead of yearday
#         month_fmt = mdates.DateFormatter('%b')
#         ax = plt.gca()
#         ax.xaxis.set_major_formatter(month_fmt)
#         # save figures
#         filename = (paths.plots_dir + 'Climatology\\UCUR_climatology_' + setup.site_name + '_' + setup.deployment_file_date_identifier + '_D' + 
#                         str(NDsorted[D]) + '.png')
#         plt.savefig(filename)
#         plt.close()
#     plt.close()
         
    
# %% VCUR, UCUR, CSPD monthly climatology box plots and PDFs

# get gridded date elements and year day 
date_string = np.datetime_as_string(grid_t,unit='s') # convert datetime64 to string format
date_elements = []
yearday = []
for nt in range(len(date_string)):
    date_elements.append(datetime.datetime.strptime(date_string[nt], "%Y-%m-%dT%H:%M:%S"))
    y = date_elements[nt].year
    m = date_elements[nt].month
    d = date_elements[nt].day
    yearday.append(datetime.datetime(y,m,d).timetuple().tm_yday)

# sort out depths
NDord = np.argsort(NDs)
NDsorted = np.array(NDs)[NDord]

# VCUR
CreateBoxPlot(np.array(yearday),np.array(grid_VCUR),
              np.array(grid_D),np.array(NDsorted),
              grid_VEL.site_code,'VCUR',paths.plots_dir)
CreateBoxPlot(np.array(yearday),np.array(grid_VCUR),
              np.array(grid_D),'depth-averaged',
              grid_VEL.site_code,'VCUR',paths.plots_dir)
PlotPDFs(np.array(yearday),np.array(grid_VCUR),
              np.array(grid_D),np.array(NDsorted),
              grid_VEL.site_code,'VCUR',paths.plots_dir)

# UCUR
CreateBoxPlot(np.array(yearday),np.array(grid_UCUR),
              np.array(grid_D),np.array(NDsorted),
              grid_VEL.site_code,'UCUR',paths.plots_dir)
CreateBoxPlot(np.array(yearday),np.array(grid_VCUR),
              np.array(grid_D),'depth-averaged',
              grid_VEL.site_code,'UCUR',paths.plots_dir)
PlotPDFs(np.array(yearday),np.array(grid_UCUR),
              np.array(grid_D),np.array(NDsorted),
              grid_VEL.site_code,'UCUR',paths.plots_dir)

# CSPD = np.sqrt( (np.array(grid_UCUR))**2 + (np.array(grid_VCUR))**2)
# CreateBoxPlot(np.array(yearday),CSPD,
#               np.array(grid_D),np.array(NDsorted),
#               grid_VEL.site_code,'Current Speed',paths.plots_dir)
# CreateBoxPlot(np.array(yearday),CSPD,
#               np.array(grid_D),'depth-averaged',
#               grid_VEL.site_code,'Current Speed',paths.plots_dir)
# PlotPDFs(np.array(yearday),CSPD,
#               np.array(grid_D),np.array(NDsorted),
#               grid_VEL.site_code,'Current Speed',paths.plots_dir)
    
# FOR TESTING FUNCTIONS 
# CreateBoxPlot(YEARDAY,VAR,DEPTH,depths,site_name,var_name,save_path)
# YEARDAY = np.array(yearday)
# VAR = np.array(grid_VCUR)
# DEPTH = np.array(grid_D)
# depths = np.array(NDsorted)
# site_name = grid_VEL.site_code
# var_name = 'VCUR'
# save_path = paths.plots_dir

# %% Save climatologies as data set NetCDFs

#####################################################
# TEMP




#####################################################
# VEL 181 day smoothed
# define data with variable attributes

# data_vars = {'VCUR_MEAN':(['DEPTH','TIME'], VCUR_MN_181[0:-2,:].transpose(), 
#              {'units': 'm/s', 
#               'long_name':'Northward velocity',
#               'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'VCUR_STD':(['DEPTH','TIME'], VCUR_std_181[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity standard deviation',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'VCUR_PER90':(['DEPTH','TIME'], VCUR_P90_181[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity ninetieth percentile',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'VCUR_PER50':(['DEPTH','TIME'], VCUR_P50_181[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity median',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'VCUR_PER10':(['DEPTH','TIME'], VCUR_P10_181[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity tent percentile',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'UCUR_MEAN':(['DEPTH','TIME'], UCUR_MN_181[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity mean',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'UCUR_STD':(['DEPTH','TIME'], UCUR_std_181[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity standard deviation',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'UCUR_PER90':(['DEPTH','TIME'], UCUR_P90_181[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity ninetieth percentile',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'UCUR_PER50':(['DEPTH','TIME'], UCUR_P50_181[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity median',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'UCUR_PER10':(['DEPTH','TIME'], UCUR_P10_181[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity tent percentile',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')})             
#              }



# # define coordinates
# start_date = np.datetime64('2009-01-01')
# yd = np.array(list(range(1,60,1)) + list(range(61,365,1)))
# datetime_array = start_date + np.timedelta64(1, 'D') * yd

# coords = {'TIME': (['TIME'], datetime_array),
#           'DEPTH':(['DEPTH'],NDsorted)}

# # define global attributes
# attrs = {'creation_date': datetime.datetime.now().strftime('%Y%m%d%H%M%S'), 
#          'Principal Investigator':'Moninya Roughan',
#          'NSW Mooring Team':'Tim Austin, Stuart Milburn',
#          'dataset author':'Michael Hemming', 
#          'dataset author email':'m.hemming@unsw.edu.au',
#          'comment':('This data set includes daily climatology statistics calculated' +
#                     ' using an 11-day moving window, and smoothed as final step using a' +
#                     ' window of 181 days.')}

# # create dataset
# ds = xr.Dataset(data_vars=data_vars, 
#                 coords=coords, 
#                 attrs=attrs)
# # save dataset
# mint = np.datetime_as_string(np.nanmin(grid_t))
# maxt = np.datetime_as_string(np.nanmax(grid_t))
# ds.to_netcdf(paths.TEMPORARY_dir + 'DataFiles\\' + 'CH100_Velocity_Climatology_Mooring_' + mint[0:4] +
#              '-' + maxt[0:4] + '_SM181Days_C' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') +
#              '.nc')

# #####################################################
# # VEL 91 day smoothed
# # define data with variable attributes

# data_vars = {'VCUR_MEAN':(['DEPTH','TIME'], VCUR_MN_91[0:-2,:].transpose(), 
#              {'units': 'm/s', 
#               'long_name':'Northward velocity',
#               'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'VCUR_STD':(['DEPTH','TIME'], VCUR_std_91[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity standard deviation',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'VCUR_PER90':(['DEPTH','TIME'], VCUR_P90_91[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity ninetieth percentile',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'VCUR_PER50':(['DEPTH','TIME'], VCUR_P50_91[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity median',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'VCUR_PER10':(['DEPTH','TIME'], VCUR_P10_91[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity tent percentile',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'UCUR_MEAN':(['DEPTH','TIME'], UCUR_MN_91[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity mean',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'UCUR_STD':(['DEPTH','TIME'], UCUR_std_91[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity standard deviation',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'UCUR_PER90':(['DEPTH','TIME'], UCUR_P90_91[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity ninetieth percentile',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'UCUR_PER50':(['DEPTH','TIME'], UCUR_P50_91[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity median',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'UCUR_PER10':(['DEPTH','TIME'], UCUR_P10_91[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity tent percentile',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')})             
#              }



# # define coordinates
# start_date = np.datetime64('2009-01-01')
# yd = np.array(list(range(1,60,1)) + list(range(61,365,1)))
# datetime_array = start_date + np.timedelta64(1, 'D') * yd

# coords = {'TIME': (['TIME'], datetime_array),
#           'DEPTH':(['DEPTH'],NDsorted)}

# # define global attributes
# attrs = {'creation_date': datetime.datetime.now().strftime('%Y%m%d%H%M%S'), 
#          'Principal Investigator':'Moninya Roughan',
#          'NSW Mooring Team':'Tim Austin, Stuart Milburn',
#          'dataset author':'Michael Hemming', 
#          'dataset author email':'m.hemming@unsw.edu.au',
#          'comment':('This data set includes daily climatology statistics calculated' +
#                     ' using an 11-day moving window, and smoothed as final step using a' +
#                     ' window of 91 days.')}

# # create dataset
# ds = xr.Dataset(data_vars=data_vars, 
#                 coords=coords, 
#                 attrs=attrs)
# # save dataset
# mint = np.datetime_as_string(np.nanmin(grid_t))
# maxt = np.datetime_as_string(np.nanmax(grid_t))
# ds.to_netcdf(paths.TEMPORARY_dir + 'DataFiles\\' + 'CH100_Velocity_Climatology_Mooring_' + mint[0:4] +
#              '-' + maxt[0:4] + '_SM91Days_C' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') +
#              '.nc')


# #####################################################
# # VEL 31 day smoothed
# # define data with variable attributes

# data_vars = {'VCUR_MEAN':(['DEPTH','TIME'], VCUR_MN_31[0:-2,:].transpose(), 
#              {'units': 'm/s', 
#               'long_name':'Northward velocity',
#               'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'VCUR_STD':(['DEPTH','TIME'], VCUR_std_31[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity standard deviation',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'VCUR_PER90':(['DEPTH','TIME'], VCUR_P90_31[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity ninetieth percentile',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'VCUR_PER50':(['DEPTH','TIME'], VCUR_P50_31[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity median',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'VCUR_PER10':(['DEPTH','TIME'], VCUR_P10_31[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity tent percentile',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'UCUR_MEAN':(['DEPTH','TIME'], UCUR_MN_31[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity mean',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'UCUR_STD':(['DEPTH','TIME'], UCUR_std_31[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity standard deviation',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'UCUR_PER90':(['DEPTH','TIME'], UCUR_P90_31[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity ninetieth percentile',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'UCUR_PER50':(['DEPTH','TIME'], UCUR_P50_31[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity median',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')}),
#              'UCUR_PER10':(['DEPTH','TIME'], UCUR_P10_31[0:-2,:].transpose(), 
#                           {'units': 'm/s', 
#                            'long_name':'Northward velocity tent percentile',
#                            'comment':('Velocity has been rotated' + str(ang) + ' degrees')})             
#              }



# # define coordinates
# start_date = np.datetime64('2009-01-01')
# yd = np.array(list(range(1,60,1)) + list(range(61,365,1)))
# datetime_array = start_date + np.timedelta64(1, 'D') * yd

# coords = {'TIME': (['TIME'], datetime_array),
#           'DEPTH':(['DEPTH'],NDsorted)}

# # define global attributes
# attrs = {'creation_date': datetime.datetime.now().strftime('%Y%m%d%H%M%S'), 
#          'Principal Investigator':'Moninya Roughan',
#          'NSW Mooring Team':'Tim Austin, Stuart Milburn',
#          'dataset author':'Michael Hemming', 
#          'dataset author email':'m.hemming@unsw.edu.au',
#          'comment':('This data set includes daily climatology statistics calculated' +
#                     ' using an 11-day moving window, and smoothed as final step using a' +
#                     ' window of 31 days.')}

# # create dataset
# ds = xr.Dataset(data_vars=data_vars, 
#                 coords=coords, 
#                 attrs=attrs)
# # save dataset
# mint = np.datetime_as_string(np.nanmin(grid_t))
# maxt = np.datetime_as_string(np.nanmax(grid_t))
# ds.to_netcdf(paths.TEMPORARY_dir + 'DataFiles\\' + 'CH100_Velocity_Climatology_Mooring_' + mint[0:4] +
#              '-' + maxt[0:4] + '_SM31Days_C' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') +
#              '.nc')


    
    
    
    
    
