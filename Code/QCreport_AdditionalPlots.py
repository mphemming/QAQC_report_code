
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Tue Jul 14 16:35:51 2020
# Contributers (code):  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# Contributers (review): Moninya Roughan (NSW-IMS), Tim Austin (NSW-IMOS), Stuart Milburn (NSW-IMOS) 
# contact email: m.hemming@unsw.edu.au

# %% -----------------------------------------------------------------------------------------------
# Import modules

# QCreport modules
import QCreport_paths as paths
import QCreport_format as form
import QCreport_DeploymentDetails as DepDet
import QCreport_QualityControl as QCR
import QCreport_DeploymentPhotographs as DepPhoto
import QCreport_ToolboxPlots as tbp
import QCreport_setup as setup
import QCreport_cover as cover
# This package runs python scripts within a script
import runpy
import os
import glob
import numpy as np
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
# Run code to create OceanCurrent plots

# ensure at correct path first
os.chdir(paths.working_dir + '\\Code')
runpy.run_path('QCreport_OceanCurrents.py')

# %% -----------------------------------------------------------------------------------------------
# Run code to create climatology plots

# ensure at correct path first
os.chdir(paths.working_dir + '\\Code')
runpy.run_path('QCreport_climatology.py')

# %% -----------------------------------------------------------------------------------------------
# Add Map figure

def addMap(doc,site_name):
    file = (paths.plots_dir + 'Maps\\Moorings_map.png')
    with doc.create(form.Figure(position='h!')) as map_pic:
        map_pic.add_image(file, 
                          width=form.NoEscape(r'0.85\linewidth'))
        if 'BMP' in site_name:
            map_pic.add_caption('Mooring locations along New South Wales. Site ' +
                                site_name + ' is close to Narooma shown in panel (d).')  
        if 'SYD' in site_name or 'PH' in site_name or 'ORS' in site_name:
            map_pic.add_caption('Mooring locations along New South Wales. Site ' +
                                site_name + ' is close to Sydney shown in panel (c).')     
        if 'CH' in site_name:
            map_pic.add_caption('Mooring locations along New South Wales. Site ' +
                                site_name + ' is close to Coffs Harbour shown in panel (b).') 

# %% -----------------------------------------------------------------------------------------------
# Add Ocean currents plots

def addOCplots(doc):
    # get list of plots to include
    SST_plots = glob.glob(paths.plots_dir + 'OceanCurrent_Plots\\SST\\' + setup.site_name + '_' + 
                       setup.deployment_file_date_identifier
                          + '_' + 'SST_OC*.png')
    perc_plots = glob.glob(paths.plots_dir + 'OceanCurrent_Plots\\percentiles\\' + setup.site_name + '_' + 
                       setup.deployment_file_date_identifier
                          + '_' + 'percentiles_OC*.png')
    chl_plots = glob.glob(paths.plots_dir + 'OceanCurrent_Plots\\CPHL\\' + setup.site_name + '_' + 
                       setup.deployment_file_date_identifier
                          + '_' + 'Chl_OC*.png')
    # Add SST plot     
    for p in SST_plots:
        doc.append(form.Command('newpage'))
        with doc.create(form.Figure(position='h!')) as SST_pic:
                SST_pic.add_image(p, width=form.NoEscape(r'0.85\linewidth'))
                SST_pic.add_caption('SST snapshots from Ocean Currents')  
    # Add Percentile plot   
    for p in perc_plots:    
        doc.append(form.Command('newpage'))
        with doc.create(form.Figure(position='h!')) as perc_pic:
                perc_pic.add_image(p, width=form.NoEscape(r'0.85\linewidth'))
                perc_pic.add_caption('Percentile snapshots from Ocean Currents')   
    # Add Ocean Color plot     
    for p in chl_plots:
        doc.append(form.Command('newpage'))
        with doc.create(form.Figure(position='h!')) as oc_pic:
            oc_pic.add_image(p, width=form.NoEscape(r'0.85\linewidth'))
            oc_pic.add_caption('Ocean color snapshots from Ocean Currents')  
    
# %% -----------------------------------------------------------------------------------------------
# Add time series plots

# get all climatology plots
timeseries_plots = DepDet.nc.glob.glob(paths.plots_dir + 'TimeSeries\\' + 'TEMP_' + 
                            setup.site_name + '_' + 
                            setup.deployment_file_date_identifier + '*.png')
NDs = []
for f in timeseries_plots:
    f1 = f.find(setup.deployment_file_date_identifier)
    f2 = f.find('.png')
    nd = f[f1+4:f2].replace('_','')
    nd = nd.replace('D','')
    NDs.append(nd)
    # NDs.append(f[-9:-6].replace('D',''))
f = np.argsort(np.round(np.array(NDs).astype(float)))
NDs = np.int32(np.round(np.array(NDs).astype(float)))[f]
timeseries_plots = np.array(timeseries_plots)[f]

def addTimeSeriesplots(doc):
    # Add climatology plots
    for n in range(len(timeseries_plots)):
        with doc.create(form.Figure(position='h!')) as timeseries_pics:
            timeseries_pics.add_image(timeseries_plots[n], 
                              width=form.NoEscape(r'0.85\linewidth'))
            timeseries_pics.add_caption('Time series comparison at a nominal depth of ' 
                                  + str(NDs[n]) + ' m.')       
    
    
# %% -----------------------------------------------------------------------------------------------
# Add climatology plots

# get all climatology plots
clim_plots = DepDet.nc.glob.glob(paths.plots_dir + 'Climatology\\' + 'TEMP_climatology_' + 
                            setup.site_name + '_' + 
                            setup.deployment_file_date_identifier + '*.png')
# NDs = []
# for f in clim_plots:
#     NDs.append(f[-9:-6].replace('D',''))
# f = np.argsort(np.int32(NDs))
# NDs = np.int32(NDs)[f]
clim_plots = np.array(clim_plots)[f]

def addClimplots(doc):
    # Add climatology plots
    for n in range(len(clim_plots)):
        with doc.create(form.Figure(position='h!')) as clim_pics:
            clim_pics.add_image(clim_plots[n], 
                              width=form.NoEscape(r'0.85\linewidth'))
            clim_pics.add_caption('Climatology comparison at a nominal depth of ' 
                                  + str(NDs[n]) + ' m.')          
   
# %% -----------------------------------------------------------------------------------------------
# Add CTD-mooring comparison

def addCTDMooringplot(doc,site_name,deployment_file_date_identifier):
    file = (paths.plots_dir + 'CTDcomparison\\TEMP_' + setup.site_name + '_' + 
                setup.deployment_file_date_identifier + '.png')
    if os.path.exists(file):
        with doc.create(form.Figure(position='h!')) as clim_pics:
            clim_pics.add_image(file, 
                              width=form.NoEscape(r'0.85\linewidth'))
            clim_pics.add_caption('A comparison between mooring measurements near in time and space' + 
                                  ' to the deployment CTD profile.')     
        
# %% -----------------------------------------------------------------------------------------------
# Add Time-Depth plot

def addTDplot(doc,site_name,deployment_file_date_identifier):
    file = (paths.plots_dir + 'TimeSeries\\TEMP_DEPTH_' + site_name + '_' + 
            deployment_file_date_identifier + '.png')
    if os.path.exists(file):
        with doc.create(form.Figure(position='h!')) as TD_pics:
            TD_pics.add_image(file, 
                              width=form.NoEscape(r'0.85\linewidth'))
            TD_pics.add_caption('Time-depth plot of historical mooring temperatures' + 
                                  ', alongside the selected deployment.')                
            
            