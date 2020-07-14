# -*- coding: utf-8 -*-

# Created on Mon Jun 29 16:11:18 2020
# Contributers (code):  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# Contributers (review): Moninya Roughan (NSW-IMS), Tim Austin (NSW-IMOS), Stuart Milburn (NSW-IMOS) 
# contact email: m.hemming@unsw.edu.au


# %% -----------------------------------------------------------------------------------------------
# Import packages

# Python Packages
import datetime

# %% -----------------------------------------------------------------------------------------------
# Choose site, deployment, add name of report maker 
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

site_name = 'BMP070'
deployment = '29'
deployment_file_date_identifier = '1904'
name_of_reportmaker = 'Michael Hemming'

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________


# %% -----------------------------------------------------------------------------------------------
# Add Comments to Report 
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

QCcomment = 'Some'
# options: 'None', 'Some', 'Moderate', 'Substantial'
QCmethod = 'Automatic and manual'
# options: 'Automatic', 'Manual', 'Automatic and manual'
Fieldwork_issues = 'None'
# default: 'None', if issues add text here
Sensor_damage = 'None'
# default: 'None', if damage add text here
Lost_equipment = 'None'
# default: 'None', if lost equipment add text here
Biofouling = 'Moderate, see attached images'
# options: 'None', 'Some', 'Moderate', 'Substantial'
Other_issues = 'None'
# default: 'None', if other issues add text here
Additional_QC = 'Yes, see comments'
# options: 'yes' or 'no'

# Keep information above short (no more than 4 words). If there
# is a neeed to add more information, add this in the 'comments' string below  

comments = 'Some pressure sensor drift. See end of report for details.'
# default: 'None', if comments add text here   
# tips: copy & paste might not work - only use characters in 'latin-q' codec
# e.g. commas copied over from somewhere else may be different to commas in latin-1
# use '' instead       

#------------------------------------------------------------
# Information 
#-------------
        
# Information added here will be included in the introduction 
# comments at the start of the deployment report

#------------------------------------------------------------               
            
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# %% -----------------------------------------------------------------------------------------------
# get date of document creation for cover

now = datetime.date.today().strftime("%B %d, %Y")
now_year = datetime.date.today().strftime("%Y")

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________


# %% -----------------------------------------------------------------------------------------------
# citation

# split name of reportmaker into first and second name
findspace = name_of_reportmaker.find(' ')
firstname = name_of_reportmaker[0:findspace]
surname = name_of_reportmaker[findspace+1:]

if 'Austin' in surname:
    citation = 'Austin, T, Roughan, M, and Milburn, S. ' + \
    'Report on the Quality Control of the NSW-IMOS Australian National Moorings Network site: ' + \
    site_name + ' - Deployment ' + deployment + ', (' + now_year + ').' + \
    ' Integrated Marine Observing System, Australia.'
if 'Roughan' in surname:
    citation = 'Roughan, M, Austin, T, and Milburn, S. ' + \
    'Report on the Quality Control of the NSW-IMOS Australian National Moorings Network site: ' + \
    site_name + ' - Deployment ' + deployment + ', (' + now_year + ').' + \
    ' Integrated Marine Observing System, Australia.'
if 'Milburn' in surname:
    citation = 'Milburn, S, Roughan, M, and Austin, T. ' + \
    'Report on the Quality Control of the NSW-IMOS Australian National Moorings Network site: ' + \
    site_name + ' - Deployment ' + deployment + ', (' + now_year + ').' + \
    ' Integrated Marine Observing System, Australia.'
if 'Hemming' in surname:
    citation = 'Hemming, M, Roughan, M, and Austin, T, Milburn, S, Malan, N. ' + \
    'Report on the Quality Control of the NSW-IMOS Australian National Moorings Network site: ' + \
    site_name + ' - Deployment ' + deployment + ', (' + now_year + ').' + \
    ' Integrated Marine Observing System, Australia.'    
if 'Malan' in surname:
    citation = 'Malan, N, Roughan, M, and Austin, T, Milburn, S, Hemming, M. ' + \
    'Report on the Quality Control of the NSW-IMOS Australian National Moorings Network site: ' + \
    site_name + ' - Deployment ' + deployment + ', (' + now_year + ').' + \
    ' Integrated Marine Observing System, Australia.'    
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________





