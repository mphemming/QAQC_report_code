# Created on Wed Jan 25 09:39:46 2023
# Contributers (code):  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# Contributers (review): Moninya Roughan (NSW-IMS), Tim Austin (NSW-IMOS), Stuart Milburn (NSW-IMOS) 
# contact email: m.hemming@unsw.edu.au


# %% -----------------------------------------------------------------------------------------------
# Determine which computer this script is on

import os
if 'mphem' in os.getcwd():
    account = 'mphem'
else:
    account = 'z3526971'
    
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
import time
import os
import scipy.stats as stats
import cmocean as cm
# QCreport modules
import QCreport_paths as paths
import QCreport_netCDF as nc
import QCreport_setup as setup
os.chdir('C:\\Users\\' + account + '\\OneDrive - UNSW\\Work\\QC_reports\\Code\\Utilities\\python-holteandtalley-master\\')
import holteandtalley as ht
os.chdir('C:\\Users\\' + account + '\\OneDrive - UNSW\\Work\\QC_reports\\Code\\')

# plan
# (1) create new gridded product that is every 1m depth for vel and temp (in other script)
# (2) rotate velocity, depending on site
# (3) Temp and vel plot over time for deployment


# %% -----------------------------------------------------------------------------------------------
# Load in data

# TEMPERATURE
griddedfilesintemp_TEMP = glob.glob(paths.TEMPORARY_dir + '*' + setup.site_name + '*TEMP-gridded*.nc')
datestamps = []
for f in griddedfilesintemp_TEMP:
    datestamps.append(time.ctime(os.stat(f).st_ctime))
fTEMP = np.argmax(datestamps)
TEMP_data = xr.open_dataset(griddedfilesintemp_TEMP[fTEMP])

# VELOCITY
griddedfilesintemp_VEL = glob.glob(paths.TEMPORARY_dir + '*' + setup.site_name + '*velocity-gridded*.nc')
datestamps = []
for f in griddedfilesintemp_VEL:
    datestamps.append(time.ctime(os.stat(f).st_ctime))
fVEL = np.argmax(datestamps)
VEL_data = xr.open_dataset(griddedfilesintemp_VEL[fVEL])

# %% -----------------------------------------------------------------------------------------------
# Required functions


# select this deployment only
def getDeployment(ds,nc):
    # get range
    start_time = np.datetime64(nc.time_coverage_start[0])
    end_time = np.datetime64(nc.time_coverage_end[0])
    # select data
    ds = ds.sel(TIME=slice(start_time, end_time))
    
    return ds

# get MLD for plot
def getMLDs(ds,ax):
    
    T = ds.TEMP.values
    t = ds.TIME.values
    MLDs = []
    for n in range(len(t)):
        Tint = np.interp(ds.DEPTH.values,ds.DEPTH.values[np.isfinite(T[n,:])],T[n,:][np.isfinite(T[n,:])])
        h = ht.HolteAndTalley(ds.DEPTH.values,Tint)
        ml = h.temp.calculateTTMLD()
        shallowest_D = np.nanmin(ds.DEPTH.values[np.isfinite(T[n,:])])
        if ml > shallowest_D:
            MLDs.append(ml) # 0.2 degrees threshold method
        else:
            MLDs.append(np.nan)
    # bin data
    bins = np.arange(min(t), max(t), np.timedelta64(1, 'h'))
    binned_data,bin_edges,_ = stats.binned_statistic(t.astype('int64'), MLDs, statistic='mean', bins=bins)
    ax.plot(bins[0:-1],binned_data,linewidth=0.3,c='k')    
    
    return MLDs


# get 14 degrees isotherm for plot

def plot_14deg(t,D,T,ax):

    c = np.logical_and((T.TEMP.values >= 13.9),(T.TEMP.values <= 14.1))
    
    t14 = t.transpose()[c]
    D14 = D.transpose()[c]
    # bin data
    bins = np.arange(min(t14), max(t14), np.timedelta64(1, 'h'))
    binned_data,bin_edges,_ = stats.binned_statistic(t14.astype('int64'), D14, statistic='mean', bins=bins)
    ax.plot(bins[0:-1],binned_data,linewidth=0.3,c='w')
    
    

# add nominal depths to plot

def plot_nomDepth(t,nc,ax):
    ND = [v for k, v in nc.instrument_nominal_depth.items()]
    ts = np.repeat(np.nanmin(t),len(ND))
    ax.scatter(ts,ND,marker='>',c='r')

# rotate velocity function

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
              'BMP120': -1}
    
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
    
    

# plotting function
def CreatePlot(T,U,V,nc):
    
   # setup figure
   fig, axs = plt.subplots(3, 1, figsize=[12, 8], tight_layout=True)
   #################################################################################
   #################################################################################
   # Temperature
   t,D = np.meshgrid(T.TEMP.TIME.values,T.TEMP.DEPTH.values)
   cf = axs[0].contourf(t,D,T.TEMP.transpose().values,levels=15)
   # beautify subplot
   axs[0].set_ylim([np.min(D)-5,np.max(D)+5])
   axs[0].set_xlim([np.min(t)-np.timedelta64(5, 'D'),np.max(t)+np.timedelta64(5, 'D')])
   axs[0].invert_yaxis()
   axs[0].set_ylabel('DEPTH [m]')
   axs[0].set_title('TEMP | ' + setup.site_name + ' | Dpl:' + setup.deployment_file_date_identifier)
   cbar = fig.colorbar(cf, ax=axs[0])
   axs[0].grid()
   # Set the x-axis time format
   xfmt = mdates.AutoDateFormatter(mdates.AutoDateLocator())
   axs[0].xaxis.set_major_formatter(xfmt)
   axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
   # add nominal depths
   plot_nomDepth(t,nc,axs[0])
   # add 14 deg isotherm
   plot_14deg(t,D,T,axs[0])
   # get MLDs
   MLDs = getMLDs(T,axs[0])
   #################################################################################
   #################################################################################
   # rotate velocities
   Urotated,Vrotated,CSPD,new_direction,ang = rotateVel(U,V,setup.site_name)
   #################################################################################
   #################################################################################
   # VCUR
   t,D = np.meshgrid(V.TIME.values,V.DEPTH.values)
   cf = axs[1].contourf(t,D,Vrotated.transpose(),cmap=cm.cm.balance,levels=15)
   # beautify subplot
   axs[1].set_ylim(axs[0].get_ylim())
   axs[1].set_xlim(axs[0].get_xlim())
   # axs[1].invert_yaxis()
   axs[1].set_ylabel('DEPTH [m]')
   axs[1].set_title('VCUR | ' + setup.site_name + ' | Dpl:' + setup.deployment_file_date_identifier 
                    + ' | Rotated ' + str(ang) + ' degrees')
   cbar = fig.colorbar(cf, ax=axs[1])
   axs[1].grid()
   # Set the x-axis time format
   xfmt = mdates.AutoDateFormatter(mdates.AutoDateLocator())
   axs[1].xaxis.set_major_formatter(xfmt)
   axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
   # add nominal depths
   plot_nomDepth(t,nc,axs[1])
   #################################################################################
   #################################################################################
   # UCUR
   t,D = np.meshgrid(U.TIME.values,U.DEPTH.values)
   cf = axs[2].contourf(t,D,Urotated.transpose(),cmap=cm.cm.balance,levels=15)
   # beautify subplot
   axs[2].set_ylim(axs[0].get_ylim())
   axs[2].set_xlim(axs[0].get_xlim())
   # axs[2].invert_yaxis()
   axs[2].set_ylabel('DEPTH [m]')
   axs[2].set_title('UCUR | ' + setup.site_name + ' | Dpl:' + setup.deployment_file_date_identifier 
                    + ' | Rotated ' + str(ang) + ' degrees')
   cbar = fig.colorbar(cf, ax=axs[2])
   axs[2].grid()
   # Set the x-axis time format
   xfmt = mdates.AutoDateFormatter(mdates.AutoDateLocator())
   axs[2].xaxis.set_major_formatter(xfmt)
   axs[2].xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
   # add nominal depths
   plot_nomDepth(t,nc,axs[2])   



# %% -----------------------------------------------------------------------------------------------
# Create plot

TEMP_data = getDeployment(TEMP_data,nc)
VEL_data = getDeployment(VEL_data,nc)

T = TEMP_data;
V = VEL_data.VCUR[0,:,:];
U = VEL_data.UCUR[0,:,:];

CreatePlot(T,U,V,nc)

# save figures
filename = (paths.plots_dir + 'DeploymentPeriod\\T_UVrotated_' + setup.site_name + '_Deployment' + 
            setup.deployment_file_date_identifier + '.png')
plt.savefig(filename)
plt.close()    

