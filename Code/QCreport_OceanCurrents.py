
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Tue Jul 14 08:56:18 2020
# Contributers (code):  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# Contributers (review): Moninya Roughan (NSW-IMS), Tim Austin (NSW-IMOS), Stuart Milburn (NSW-IMOS) 
# contact email: m.hemming@unsw.edu.au

# %% -----------------------------------------------------------------------------------------------
# Import modules

from urllib import request
import requests
import re
import os.path
import numpy as np
import datetime as dt
from datetime import datetime as dtdt
import matplotlib as mat
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from pylab import *
import glob as glob

# QCreport modules
import QCreport_paths as paths
import QCreport_format as form
import QCreport_DeploymentDetails as DepDet
import QCreport_QualityControl as QCR
import QCreport_DeploymentPhotographs as DepPhoto
import QCreport_ToolboxPlots as tbp
import QCreport_setup as setup
import QCreport_cover as cover

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
# Define functions

def get_dates(min_time,max_time):
    # calculate dates
    start_dobj = dtdt.strptime(min_time, "%Y-%m-%d")
    end_dobj = dtdt.strptime(max_time, "%Y-%m-%d")
    OCdates = [start_dobj + dt.timedelta(days=x) for x in range(0,(end_dobj-start_dobj).days,7)]
    # convert datetime back into strings
    OCdates_str = []
    for n_dates in range(len(OCdates)):
        OCdates_str.append(OCdates[n_dates].strftime('%Y%m%d'))
        
    return OCdates_str

# Function to download images from ocean currents website
def get_OCimages(url,path,data_type):
    
    # get image name
    find_gif = url.find('gif')
    if 'pctiles' in url or 'SST' in url:
        image_name = url[find_gif-9:]
    else:
        image_name = url[find_gif-11:]        
        
    # setup saving
    # get current path
    current_path = os.getcwd()
    
    if 'percentiles' in data_type:
        dirr = path + 'percentiles\\'
    if 'SST' in data_type:
        dirr = path + 'SST\\' 
    if 'chl' in data_type:
        dirr = path + 'CPHL\\'                                                    
        
    # Go to ocean currents plot directory for saving
    if dirr in os.getcwd():
        dirr = dirr
        dirr = dirr + '/'
    else:
        dirr = dirr + '/'
        os.chdir(dirr) 
    # download image and save
    f = open(image_name, 'wb')
    f.write(request.urlopen(url).read())
    f.close()
    os.chdir(current_path)


def getFiles(link,data_type):
    res = requests.get(link)
    txt = res.text
    files = []
    file_dates = []
    
    if 'SST' in data_type or 'chl' in data_type:
        for m in re.finditer('href=', txt):
            ftxt = txt[m.start()+5:m.start()+16] + 'gif'
            if '20' in ftxt and '/>' not in ftxt and 'SNSW' not in ftxt:
                files.append(link + ftxt)
                try:
                    file_dates.append(np.datetime64(ftxt[0:4] + '-' + ftxt[4:6] + '-' + ftxt[6:8]))
                except:
                    pass  
    if 'percentiles' in data_type:
        for m in re.finditer('.gif</a>', txt):
            ftxt = txt[m.start()-8:m.start()+4]
            files.append(link + ftxt)
            try:
                file_dates.append(np.datetime64(ftxt[0:4] + '-' + ftxt[4:6] + '-' + ftxt[6:8]))
            except:
                pass  
            
    return files, file_dates

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
# get images (updated version)


def getFilesInRange(site, start_date, end_date, data_type):
    
    if 'SST' in data_type:
        # if start and end date years are the same
        if start_date.astype(datetime.datetime).year == end_date.astype(datetime.datetime).year:
            if 'CH' not in site:
                link = ('http://oceancurrent.imos.org.au/SNSW/' + 
                        str(start_date.astype(datetime.datetime).year) + '/')
            else:
               link = ('http://oceancurrent.imos.org.au/Coffs/' + 
                       str(start_date.astype(datetime.datetime).year) + '/') 
            files, file_dates = getFiles(link,data_type)
        else:
            # if start and end date years are not the same
            # get first list of files
            if 'CH' not in site:
                link = ('http://oceancurrent.imos.org.au/SNSW/' + 
                        str(start_date.astype(datetime.datetime).year) + '/')
            else:
                link = ('http://oceancurrent.imos.org.au/Coffs/' + 
                        str(start_date.astype(datetime.datetime).year) + '/')
            files_1, file_dates_1 = getFiles(link,data_type)
            # get second list of files
            if 'CH' not in site:
                link = ('http://oceancurrent.imos.org.au/SNSW/' + 
                        str(end_date.astype(datetime.datetime).year) + '/')
            else:
                link = ('http://oceancurrent.imos.org.au/Coffs/' + 
                        str(end_date.astype(datetime.datetime).year) + '/')
            files_2, file_dates_2 = getFiles(link,data_type)
            # combine
            files = np.concatenate([files_1,files_2])
            file_dates = np.concatenate([file_dates_1,file_dates_2])
            
    if 'percentiles' in data_type:
        if 'CH' not in site:
            link = ('http://oceancurrent.imos.org.au/DR_SST_daily/pctiles/SNSW/')
        else:
            link = ('http://oceancurrent.imos.org.au/DR_SST_daily/pctiles/Coffs/')
        files, file_dates = getFiles(link,data_type)
  
    if 'chl' in data_type:
        # if start and end date years are the same
        if start_date.astype(datetime.datetime).year == end_date.astype(datetime.datetime).year:
            if 'CH' not in site:
                link = ('http://oceancurrent.imos.org.au/SNSW_chl/' + 
                        str(start_date.astype(datetime.datetime).year) + '/')
            else:
               link = ('http://oceancurrent.imos.org.au/Coffs_chl/' + 
                       str(start_date.astype(datetime.datetime).year) + '/') 
            files, file_dates = getFiles(link,data_type)
        else:
            # if start and end date years are not the same
            # get first list of files
            if 'CH' not in site:
                link = ('http://oceancurrent.imos.org.au/SNSW_chl/' + 
                        str(start_date.astype(datetime.datetime).year) + '/')
            else:
                link = ('http://oceancurrent.imos.org.au/Coffs_chl/' + 
                        str(start_date.astype(datetime.datetime).year) + '/')
            files_1, file_dates_1 = getFiles(link,data_type)
            # get second list of files
            if 'CH' not in site:
                link = ('http://oceancurrent.imos.org.au/SNSW_chl/' + 
                        str(end_date.astype(datetime.datetime).year) + '/')
            else:
                link = ('http://oceancurrent.imos.org.au/Coffs_chl/' + 
                        str(end_date.astype(datetime.datetime).year) + '/')
            files_2, file_dates_2 = getFiles(link,data_type)
            # combine
            files = np.concatenate([files_1,files_2])
            file_dates = np.concatenate([file_dates_1,file_dates_2])
    
    # select files in range 
    f = np.logical_and(np.array(file_dates) >= start_date,
                       np.array(file_dates) <= end_date)
    files = np.array(files)[f]
    # select a smaller sample for figure, equaly spread out over time period
    splitter = np.round(len(files)/20)
    selector = np.int32(np.arange(0,len(files),splitter))
    files = np.array(files)[selector]
            
    # http://oceancurrent.imos.org.au/SNSW/2008/
    # http://oceancurrent.imos.org.au/SNSW_chl/2004/
    # percentiles one above is correct - use that!            
            
    return files
    

start_date = np.datetime64(DepDet.start_date)
end_date = np.datetime64(DepDet.end_date)        

# get images file names
chl_files = getFilesInRange(setup.site_name, start_date, end_date, 'chl')
SST_files = getFilesInRange(setup.site_name, start_date, end_date, 'SST')
percentiles_files = getFilesInRange(setup.site_name, start_date, end_date, 'percentiles')
# download images
for chl_f in chl_files:
    get_OCimages(chl_f,paths.plots_dir + 'OceanCurrent_Plots\\','chl')
for SST_f in SST_files:
    get_OCimages(SST_f,paths.plots_dir + 'OceanCurrent_Plots\\','SST')
for perc_f in percentiles_files:
    get_OCimages(perc_f,paths.plots_dir + 'OceanCurrent_Plots\\','percentiles')
    
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 
  
# %% -----------------------------------------------------------------------------------------------
# Produce plots for report

#-------------------------------------------------------------   
# Percentiles plot 
#-------------- 

OC_plots_in_dir = glob.glob(paths.plots_dir + 'OceanCurrent_Plots\\Percentiles\\*.gif')
sizes_percentiles = [os.path.getsize(f) for f in OC_plots_in_dir]

if len(OC_plots_in_dir) != 0 and sum(sizes_percentiles) !=0:
 
    # Create figure
    fig = plt.figure(figsize=[5,10],dpi = 400) 
    fig.tight_layout()   
    # add Ocean Current images
    for n_images in range(len(OC_plots_in_dir)):
        # get image
        date_n = OC_plots_in_dir[n_images][-12:-4]
        try:
            img=mpimg.imread(OC_plots_in_dir[n_images])
            # used for subplots
            n = n_images+1
            # setup subplots depending on number of images available
            subplot(6,5,n)      
            # plot image                
            plt.imshow(img)  
            # add title
            title(date_n[-2:] + '/' + date_n[-4:-2] + '/' + date_n[0:4],fontsize=8)
            # remove axis ticks
            ax = plt.gca()
            ax.axes.xaxis.set_visible(False)
            ax.axes.yaxis.set_visible(False)
        except:
            pass
            # remove whitespace in figure
            # plt.subplots_adjust(top = 1.2, bottom = 1, right = 1, left = 0, 
            #         hspace = 0, wspace = 0)
            # plt.margins(0,0)    
            plt.tight_layout()
    #--------------    
    # save figure
    fig.savefig((paths.plots_dir + 'OceanCurrent_Plots\\percentiles\\' + 
                setup.site_name + '_' + setup.deployment_file_date_identifier + 
                '_' + 'percentiles_OC.png'), dpi=800, bbox_inches="tight")    
    plt.close()
    #-------------------------------------------------------------     

# %% -----------------------------------------------------------------------------------------------
#-------------------------------------------------------------   
# SST plot 
#--------------
   
OC_plots_in_dir = glob.glob(paths.plots_dir + 'OceanCurrent_Plots\\SST\\*.gif')
sizes_SST = [os.path.getsize(f) for f in OC_plots_in_dir]

if len(OC_plots_in_dir) != 0 and sum(sizes_SST) !=0:
    # Create figure
    fig = plt.figure(figsize=[5,10],dpi = 400) 
    fig.tight_layout()   
    # add Ocean Current images
    for n_images in range(len(OC_plots_in_dir)):
        # get image
        date_n = OC_plots_in_dir[n_images][-14:-4]
        try:
            img=mpimg.imread(OC_plots_in_dir[n_images])
            # used for subplots
            n = n_images+1
            # setup subplots depending on number of images available
            subplot(6,5,n)
            # plot image                
            plt.imshow(img)  
            # add title
            title(date_n[-4:-2] + '/' + date_n[-6:-4] + '/' + date_n[0:4],fontsize=8)
            # remove axis ticks
            ax = plt.gca()
            ax.axes.xaxis.set_visible(False)
            ax.axes.yaxis.set_visible(False)
        except:
            pass
            # remove whitespace in figure
            # plt.subplots_adjust(top = 1.2, bottom = 1, right = 1, left = 0, 
            #         hspace = 0, wspace = 0)
            # plt.margins(0,0)    
            plt.tight_layout()
    #--------------    
    # save figure
    fig.savefig((paths.plots_dir + 'OceanCurrent_Plots\\SST\\' + setup.site_name + '_' + setup.deployment_file_date_identifier + 
                '_' + 'SSTs_OC.png'), dpi=800, bbox_inches="tight")    
    plt.close()
    #-------------------------------------------------------------       

# %% ----------------------------------------------------------------------------------------------- 
#-------------------------------------------------------------   
# Ocean color plot 
#--------------
# Check if plots already exist before running below code    
OC_plots_in_dir = glob.glob(paths.plots_dir + 'OceanCurrent_Plots\\CPHL\\*.gif')
sizes_OColor = [os.path.getsize(f) for f in OC_plots_in_dir]
    
if len(OC_plots_in_dir) != 0 and sum(sizes_OColor) !=0:
    # Create figure
    fig = plt.figure(figsize=[5,10],dpi = 400)   
    # add Ocean Current images
    for n_images in range(len(OC_plots_in_dir)):
        # get image
        date_n = OC_plots_in_dir[n_images][-14:-6]
        try:
            img=mpimg.imread(OC_plots_in_dir[n_images])
            # used for subplots
            n = n_images+1
            # setup subplots depending on number of images available
            subplot(6,5,n)     
            # plot image                
            plt.imshow(img)  
            # add title
            title(date_n[-2:] + '/' + date_n[-4:-2] + '/' + date_n[0:4],fontsize=8)
            # remove axis ticks
            ax = plt.gca()
            ax.axes.xaxis.set_visible(False)
            ax.axes.yaxis.set_visible(False)
        except:
            pass
        # remove whitespace in figure
        # plt.subplots_adjust(top = 1.2, bottom = 1, right = 1, left = 0, 
        #         hspace = 0, wspace = 0)
        # plt.margins(0,0)    
    fig.tight_layout()
    # fig.tight_layout(rect=[0, 1, 1, 0.95])
    #--------------    
    # save figure
    fig.savefig((paths.plots_dir + 'OceanCurrent_Plots\\CPHL\\' + 
                setup.site_name + '_' + setup.deployment_file_date_identifier + 
                '_' + 'Chl_OC.png'), dpi=800, bbox_inches="tight")    
    plt.close()
    #-------------------------------------------------------------           
    
# %% ----------------------------------------------------------------------------------------------- 
# Delete all gif files from folder as no longer required
 
# SST
files2remove = glob.glob(paths.plots_dir + 'OceanCurrent_Plots\\SST\\*.gif')
for f in files2remove:
    os.remove(f)  
# percentiles
files2remove = glob.glob(paths.plots_dir + 'OceanCurrent_Plots\\percentiles\\*.gif')
for f in files2remove:
    os.remove(f)  
# CPHL
files2remove = glob.glob(paths.plots_dir + 'OceanCurrent_Plots\\CPHL\\*.gif')
for f in files2remove:
    os.remove(f)  
    
# %% ----------------------------------------------------------------------------------------------- 
# Delete all gif files from folder as no longer required    
plt.close('all')   
    
    
    
    
    
    
    
    
    
    
    
    
    
    