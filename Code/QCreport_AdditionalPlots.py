
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
import QCreport_setup as setup
# This package runs python scripts within a script
import runpy
import os
import glob
import numpy as np
import subprocess
import time
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
# Determine which computer this script is on

import os
if 'mphem' in os.getcwd():
    account = 'mphem'
else:
    account = 'z3526971'

# %% -----------------------------------------------------------------------------------------------
# Run MATLAB code to update the Mooring coverage plot

script_path = r'C:\\Users\\' + account + '\\OneDrive - UNSW\\Work\\QC_reports\\Code\\Matlab\\UpdateMooringCoverage.bat'
subprocess.call([script_path])

# pause the script by 30 seconds to wait for the deployment coverage plot to be updated
time.sleep(20)

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
# Run code to create time-depth plot

# ensure at correct path first
os.chdir(paths.working_dir + '\\Code')
runpy.run_path('QCreport_TimeDepthView.py')

# %% -----------------------------------------------------------------------------------------------
# Run code to create deployment T,V,U plot

# ensure at correct path first
os.chdir(paths.working_dir + '\\Code')
runpy.run_path('QCreport_PlotDeployment.py')

# %% -----------------------------------------------------------------------------------------------
# Run code to create CTD comparison

# ensure at correct path first
os.chdir(paths.working_dir + '\\Code')
runpy.run_path('QCreport_CTDcomparison.py')

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
                SST_pic.add_image(p, width=form.NoEscape(r'0.75\linewidth'))
                SST_pic.add_caption('SST snapshots from Ocean Currents')  
    # Add Percentile plot   
    for p in perc_plots:    
        doc.append(form.Command('newpage'))
        with doc.create(form.Figure(position='h!')) as perc_pic:
                perc_pic.add_image(p, width=form.NoEscape(r'0.75\linewidth'))
                perc_pic.add_caption('Percentile snapshots from Ocean Currents')   
    # Add Ocean Color plot     
    for p in chl_plots:
        doc.append(form.Command('newpage'))
        with doc.create(form.Figure(position='h!')) as oc_pic:
            oc_pic.add_image(p, width=form.NoEscape(r'0.75\linewidth'))
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
            
# Velocity climatology plots
boxp_plots_VCUR = DepDet.nc.glob.glob(paths.plots_dir + 'Climatology\\' + 'VCUR_climatology_' + 
                            setup.site_name + '_*.png')
boxp_plots_UCUR = DepDet.nc.glob.glob(paths.plots_dir + 'Climatology\\' + 'UCUR_climatology_' + 
                            setup.site_name + '_*.png')

def addVelBoxplots_VCUR(doc):
    # Add climatology plots
    for n in range(len(boxp_plots_VCUR)):
        with doc.create(form.Figure()) as boxp_pics:
            boxp_pics.add_image(boxp_plots_VCUR[n], 
                              width=form.NoEscape(r'0.75\linewidth'))
            f1 = boxp_plots_VCUR[n].find('_D'); f2 = boxp_plots_VCUR[n].find('.png')
            depth = boxp_plots_VCUR[n][f1+2:f2]
            boxp_pics.add_caption('VCUR climatology at a nominal depth of ' 
                                  + depth + ' m.') 

def addVelBoxplots_UCUR(doc):
    # Add climatology plots
    for n in range(len(boxp_plots_UCUR)):
        print(boxp_plots_UCUR[n])
        with doc.create(form.Figure()) as boxp_pics:
            boxp_pics.add_image(boxp_plots_UCUR[n], 
                              width=form.NoEscape(r'0.75\linewidth'))
            f1 = boxp_plots_UCUR[n].find('_D'); f2 = boxp_plots_UCUR[n].find('.png')
            depth = boxp_plots_UCUR[n][f1+2:f2]
            boxp_pics.add_caption('UCUR climatology at a nominal depth of ' 
                                  + depth + ' m.') 
                
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
                              width=form.NoEscape(r'1\linewidth'))
            TD_pics.add_caption('Time-depth plot of historical mooring temperatures' + 
                                  ', alongside the selected deployment.')                
            
# %% -----------------------------------------------------------------------------------------------
# Add T,V,U deployment plot to the document

def addPlotDeployment(doc,site_name,deployment_file_date_identifier):
    file = (paths.plots_dir + 'DeploymentPeriod\\T_UVrotated_' + site_name + '_Deployment' + 
            deployment_file_date_identifier + '.png')
    if os.path.exists(file):
        with doc.create(form.Figure(position='h!')) as PD_pic:
            PD_pic.add_image(file, 
                              width=form.NoEscape(r'1\linewidth'))
            PD_pic.add_caption('Temperature and rotated velocities over time and depth' + 
                               ' during the deployment. The white line indicates the 14 deg. celsius isotherm,' + 
                               ' while the black line is the MLD (only shown if deeper than the shallowest'+
                               ' temperature measurement.')   

# %% -----------------------------------------------------------------------------------------------
# Add deployment coverage plot created using MATLAB

def addDepCoverage(doc):
    file = ('C:\\Users\\' + account + '\\OneDrive - UNSW\\Work\\QC_reports\\Code\\Matlab\\NSW_mooring_coverage.png')
    if os.path.exists(file):
        with doc.create(form.Figure(position='h!')) as DC_pic:
            DC_pic.add_image(file, 
                              width=form.NoEscape(r'1\linewidth'))
            DC_pic.add_caption('Data coverage at all NSW-IMOS sites. Note that coverage here is defined' +
                               ' as being when an instrument is in the water measuring a particular variable,' + 
                               ' not necessarily when "good" data is present.' + 
                               ' This plot has been updated for this report.')   
             
            
# %% -----------------------------------------------------------------------------------------------
# Add Depth-coverage plot (created for another project)

def addVertCoverage(doc):
    file = ('C:\\Users\\' + account + '\\OneDrive - UNSW\\Work\\QC_reports\\plots\\Other' + 
            '\\Figure_MooringDataDepths.png')
    if os.path.exists(file):
        with doc.create(form.Figure(position='h!')) as DC_pic:
            DC_pic.add_image(file, 
                              width=form.NoEscape(r'1\linewidth'))
            DC_pic.add_caption('Data Availability at the NSW-IMOS mooring sites off Coffs Harbour' +
                               ' (CH100,CH070, CH050), Sydney (ORS065, SYD100, SYD140, PH100),' + 
                               ' and Narooma (BMP070, BMP090, BMP120). Depths with low to high coverage' + 
                               ' are shaded from grey to black, respectively, and are surrounded by colored' + 
                               ' boxes indicating the vertical range and type of measurements: temperature' +
                               ' (blue), salinity (orange), velocity (brown), dissolved oxygen (light blue),' +
                               ' and chlorophyll-a flourescence (green). Data availability is approximate' +
                               ' as we do not accountfor any differences in temporal resolution.')   
                         
# %% -----------------------------------------------------------------------------------------------
# Add deployment coverage plot created using MATLAB

def addVelEllipse(doc):
    file =  (paths.plots_dir + 'VelEllipses\\VEl_Ellipse_' + setup.site_name + '_' + 
             setup.deployment_file_date_identifier + '_DepthAveraged.png')
    if os.path.exists(file):
        with doc.create(form.Figure(position='h!')) as Ell_pic:
            Ell_pic.add_image(file, 
                              width=form.NoEscape(r'1\linewidth'))
            Ell_pic.add_caption('Comparing velocity ellipses for all historical data collected over the same ' + 
                                'time of the year as the deployment, and deployment data. The ellipses use ' +
                                'data over the whole water column.')             


            
            