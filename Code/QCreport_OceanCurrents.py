
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Tue Jul 14 08:56:18 2020
# Contributers (code):  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# Contributers (review): Moninya Roughan (NSW-IMS), Tim Austin (NSW-IMOS), Stuart Milburn (NSW-IMOS) 
# contact email: m.hemming@unsw.edu.au

# %% -----------------------------------------------------------------------------------------------
# Import modules

from urllib import request
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
def get_OCimages(url):
    
    # get image name
    find_gif = url.find('gif')
    if 'pctiles' in url or 'SST' in url:
        image_name = url[find_gif-9:]
    else:
        image_name = url[find_gif-11:]        
        
    # setup saving
    # get current path
    current_path = os.getcwd()
    
    if 'pctiles' in url:
        dir = 'C:\\Users\\mphem\\Documents\\Work\\UNSW\\QC_reports\\' + \
                                                'Example_data_BMP070_29\\OceanCurrents\\Percentiles'
    if 'SST' in url:
        dir = 'C:\\Users\\mphem\\Documents\\Work\\UNSW\\QC_reports\\' + \
                                                'Example_data_BMP070_29\\OceanCurrents\\SST'   
    if 'chl' in url:
        dir = 'C:\\Users\\mphem\\Documents\\Work\\UNSW\QC_reports\\' + \
                                                'Example_data_BMP070_29\\OceanCurrents\\Chl'                                                    
        
    # Go to ocean currents plot directory for saving
    if dir in os.getcwd():
        dir = dir
        dir = dir + '/'
    else:
        dir = dir + '/'
        os.chdir(dir) 
    # download image and save
    f = open(image_name, 'wb')
    f.write(request.urlopen(url).read())
    f.close()
    os.chdir(current_path)



#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# %% -----------------------------------------------------------------------------------------------
# get images

min_time = DepDet.start_date   
max_time = DepDet.end_date   
OCdates_str = get_dates(min_time,max_time)
 
numb_images = len(OCdates_str) 

for n_images in range(numb_images):
    
    # SST images
    try:    
        url = 'http://oceancurrent.imos.org.au/DR_SST_daily/SST/SNSW/' + OCdates_str[n_images] + '.gif'  
        get_OCimages(url)
    except:
        pass        
    # percentiles images
    try:    
        url = 'http://oceancurrent.imos.org.au/DR_SST_daily/pctiles/SNSW/' + OCdates_str[n_images] + '.gif'   
        get_OCimages(url)    
    except:
        pass        
    # Ocean color images
    try:
        url = 'http://oceancurrent.imos.org.au/SNSW_chl/' + OCdates_str[n_images] + '04.gif'
        get_OCimages(url)  
    except:
        pass
    
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   
# %% -----------------------------------------------------------------------------------------------
# Produce plots for report

#-------------------------------------------------------------   
# Percentiles plot 
#--------------
# Check if plots already exist before running below code
OC_plots_in_dir = glob.glob('C:\\Users\\mphem\\Documents\\Work\\UNSW\\QC_reports\\' + \
                            'Example_data_BMP070_29\\OceanCurrents\\*percentiles*.png')    

if len(OC_plots_in_dir) == 0:
 
    # Create figure
    fig = plt.figure(figsize=[5,10],dpi = 400) 
    fig.tight_layout()   
    # add Ocean Current images
    for n_images in range(numb_images):
        # get image
        date_n = OCdates_str[n_images]
        img=mpimg.imread('C:\\Users\\mphem\\Documents\\Work\\UNSW\\QC_reports\\' + \
                          'Example_data_BMP070_29\\OceanCurrents\\Percentiles\\' + date_n + '.gif')
        # used for subplots
        n = n_images+1
        # setup subplots depending on number of images available
        if numb_images < 24:
            subplot(6,4,n)
        else:
            subplot(8,4,n)        
        # plot image                
        plt.imshow(img)  
        # add title
        title(date_n[-2:] + '/' + date_n[-4:-2] + '/' + date_n[0:4],fontsize=8)
        # remove axis ticks
        ax = plt.gca()
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        # remove whitespace in figure
        plt.subplots_adjust(top = 1.2, bottom = 0, right = 1, left = 0, 
                hspace = 0, wspace = 0)
        plt.margins(0,0)
    #--------------    
    # save figure
    fig.savefig('C:\\Users\\mphem\\Documents\\Work\\UNSW\\QC_reports\\Example_data_BMP070_29\\OceanCurrents\\' + \
                setup.site_name + '_' + setup.deployment + '_' + 'percentiles_OC.png', dpi=400)    
    #-------------------------------------------------------------     

# %% -----------------------------------------------------------------------------------------------
#-------------------------------------------------------------   
# SST plot 
#--------------
# Check if plots already exist before running below code    
OC_plots_in_dir = glob.glob('C:\\Users\\mphem\\Documents\\Work\\UNSW\\QC_reports\\' + \
                            'Example_data_BMP070_29\\OceanCurrents\\*SST*.png')        
if len(OC_plots_in_dir) == 0:
    # Create figure
    fig = plt.figure(figsize=[5,10],dpi = 400) 
    fig.tight_layout()   
    # add Ocean Current images
    for n_images in range(numb_images):
        # get image
        date_n = OCdates_str[n_images]
        img=mpimg.imread('C:\\Users\\mphem\\Documents\\Work\\UNSW\\QC_reports\\' + \
                          'Example_data_BMP070_29\\OceanCurrents\\SST\\' + date_n + '.gif')
        # used for subplots
        n = n_images+1
        # setup subplots depending on number of images available
        if numb_images < 24:
            subplot(6,4,n)
        else:
            subplot(8,4,n)        
        # plot image                
        plt.imshow(img)  
        # add title
        title(date_n[-2:] + '/' + date_n[-4:-2] + '/' + date_n[0:4],fontsize=8)
        # remove axis ticks
        ax = plt.gca()
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        # remove whitespace in figure
        plt.subplots_adjust(top = 1.2, bottom = 0, right = 1, left = 0, 
                hspace = 0, wspace = 0)
        plt.margins(0,0)    
    #--------------    
    # save figure
    fig.savefig('C:\\Users\\mphem\\Documents\\Work\\UNSW\\QC_reports\\Example_data_BMP070_29\\OceanCurrents\\' + \
                setup.site_name + '_' + setup.deployment + '_' + 'SSTs_OC.png', dpi=400)    
    #-------------------------------------------------------------       

   # %% ----------------------------------------------------------------------------------------------- 
#-------------------------------------------------------------   
# Ocean color plot 
#--------------
# Check if plots already exist before running below code    
OC_plots_in_dir = glob.glob('C:\\Users\\mphem\\Documents\\Work\\UNSW\\QC_reports\\' + \
                            'Example_data_BMP070_29\\OceanCurrents\\*Chl*.png')        
if len(OC_plots_in_dir) == 0:
    # Create figure
    fig = plt.figure(figsize=[5,10],dpi = 400) 
    fig.tight_layout()   
    # add Ocean Current images
    for n_images in range(numb_images):
        # get image
        date_n = OCdates_str[n_images]
        try:
            img=mpimg.imread('C:\\Users\\mphem\\Documents\\Work\\UNSW\\QC_reports\\' + \
                              'Example_data_BMP070_29\\OceanCurrents\\Chl\\' + date_n + '04.gif')
            # used for subplots
            n = n_images+1
            # setup subplots depending on number of images available
            if numb_images < 24:
                subplot(6,4,n)
            else:
                subplot(8,4,n)        
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
        plt.subplots_adjust(top = 1.2, bottom = 0, right = 1, left = 0, 
                hspace = 0, wspace = 0)
        plt.margins(0,0)    
    #--------------    
    # save figure
    fig.savefig('C:\\Users\\mphem\\Documents\\Work\\UNSW\\QC_reports\\Example_data_BMP070_29\\OceanCurrents\\' + \
                setup.site_name + '_' + setup.deployment + '_' + 'Chl_OC.png', dpi=400)    
    #-------------------------------------------------------------           
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    