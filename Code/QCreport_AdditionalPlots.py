
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

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
# Add Ocean currents plots

def addOCplots(report):
    
   # Add SST plot 
   report.image(paths.OC_dir + \
            setup.site_name + '_' + setup.deployment + '_' + 'SSTs_OC.png',h=260,w=160,x=20,y=30)    
   # Add Percentile plot 
   report.add_page()
   report.image(paths.OC_dir + \
            setup.site_name + '_' + setup.deployment + '_' + 'percentiles_OC.png',h=260,w=160,x=20,y=30)    
   # Add ocean color plot 
   report.add_page()
   report.image(paths.OC_dir + \
            setup.site_name + '_' + setup.deployment + '_' + 'Chl_OC.png',h=260,w=160,x=20,y=30) 

