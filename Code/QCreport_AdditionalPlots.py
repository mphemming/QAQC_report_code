
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

def addOCplots(doc):
    # Add SST plot     
    with doc.create(form.Figure(position='h!')) as SST_pic:
        SST_pic.add_image((paths.OC_dir + \
                              setup.site_name + '_' + setup.deployment
                              + '_' + 'SSTs_OC.png'), 
                          width=form.NoEscape(r'0.7\linewidth'))
        SST_pic.add_caption('SST snapshots from Ocean Currents')          
    # Add Percentile plot     
    with doc.create(form.Figure(position='h!')) as perc_pic:
        perc_pic.add_image((paths.OC_dir + \
                              setup.site_name + '_' + setup.deployment
                              + '_' + 'percentiles_OC.png'),
                          width=form.NoEscape(r'0.7\linewidth'))
        perc_pic.add_caption('Percentile snapshots from Ocean Currents')          
    # Add Ocean Color plot     
    with doc.create(form.Figure(position='h!')) as oc_pic:
        oc_pic.add_image((paths.OC_dir + \
                              setup.site_name + '_' + setup.deployment
                              + '_' + 'Chl_OC.png'), 
                         width=form.NoEscape(r'0.7\linewidth'))
        oc_pic.add_caption('Ocean color snapshots from Ocean Currents')      
    
    
  