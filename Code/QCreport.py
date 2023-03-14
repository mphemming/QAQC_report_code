
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Thu Jun  4 13:42:02 2020
# Contributers (code):  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# Contributers (review): Moninya Roughan (NSW-IMS), Tim Austin (NSW-IMOS), Stuart Milburn (NSW-IMOS), Neil Malan (NSW-IMOS) 
# contact email: m.hemming@unsw.edu.au

# What does this script do?

# o   Create a QC report for a selected site and deployment
# o   Uses the Python FPDF module to create a PDF report
# o   Incorporates paths, variables, and functions from all 'QCreport_< name>.py' scripts

# Instructions:

# o   Modify script 'QCreport_format.py' to setup QC report paths
# o   Run this script

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
# Import modules

# set path of QC code
import glob
import warnings
import importlib
os.chdir('C:\\Users\\' + account + '\\OneDrive - UNSW\\Work\\QC_reports\\Code')
import runpy

# %% -----------------------------------------------------------------------------------------------
# import remaining modules

# QCreport modules
import QCreport_setup as setup
import QCreport_format as form
import QCreport_paths as paths
import QCreport_DeploymentDetails as DepDet
import QCreport_QualityControl as QCR
import QCreport_DeploymentPhotographs as DepPhoto
import QCreport_ToolboxPlots as tbp
import QCreport_cover as cover

# needed for creating multiple reports in a loop
importlib.reload(setup)
if hasattr(setup, 'CreationMode'):
    importlib.reload(DepDet)
    importlib.reload(QCR)
    importlib.reload(DepPhoto)
    importlib.reload(tbp)

#------------------------------------------------------------
# Information 
#-------------

# These are the QC report modules required to run 
# this script. The QCreport modules need to be in 
# the same folder as this script.

#------------------------------------------------------------

print('Modules loaded')

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
# Check if LTSPs already in TEMPORARY_dir are for this site, if not remove and copy over correct LTSPs

files_in_TEMP = glob.glob(paths.TEMPORARY_dir + '*.nc')
for f in files_in_TEMP:
    if setup.site_name not in f:
        print(f)
        os.remove(f)

# %% -----------------------------------------------------------------------------------------------
# Run code to transfer LTSPs to temporary folder, and update if necessary
runpy.run_path('QCreport_checkLTSPs.py')

# NOTE: This script has to be run before importing some modules, as they require LTSPs to be present
#       (e.g. QCreport_AdditionalPlots)

# import remaining package that required LTSPs updated/organised first
import QCreport_AdditionalPlots as Addp
# needed for creating multiple reports in a loop
if hasattr(setup, 'CreationMode'):
    importlib.reload(Addp) 

# %% -----------------------------------------------------------------------------------------------
# Determine Paths

# obtain paths 
toolbox_dir = paths.tb_dir
saving_dir = paths.savedir()
mooring_dir = paths.md_dir
depphoto_dir = paths.dpp_dir

#------------------------------------------------------------
# Information 
#-------------

# These are the paths required to run this script, obtained
# from module QCreport_paths.py. These must be altered to 
# the correct paths before running the script. Refer to 
# script QCreport_paths.py to do this.

#------------------------------------------------------------

print('Paths loaded')

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
# Create document and set Format

# call function to format PDF document
geometry_options = {"tmargin": "2cm", "lmargin": "2cm"}
doc = form.Document(geometry_options=geometry_options,
                    font_size='large')
doc.append(form.Command('fontsize', arguments = ['18', '16']))
# set TOC depth to 4
doc.preamble.append(form.Command('setcounter', arguments=['tocdepth', '4']))

# Latex packages
doc.packages.append(form.Package('rotating')) # for rotating toolbox plots
doc.packages.append(form.Package('lmodern')) # change font to 'palatino'
doc.packages.append(form.Package('sectsty'))
doc.packages.append(form.Package('titlesec','compact, big'))
doc.packages.append(form.Package('placeins','section')) # ensures plots stay in correct section, and don't float around
doc.packages.append(form.Package('graphicx')) # for front cover images
doc.packages.append(form.Package('hyperref')) # for opendap links
doc.packages.append(form.Package('morefloats')) # To allow for more floats (graphics/plots) in the report
# doc.packages.append(form.Package('hyperref','[colorlinks=false]')) # for opendap links
# doc.packages.append(form.NoEscape(r'\usepackage[bgcolor=transparent]{minted}'))# to remove colored boxes
# doc.packages.append(form.NoEscape(r'\usepackage[colorlinks=false]{hyperref}'))
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
# Sections


# %% -----------------------------------------------------------------------------------------------
# --------------------------------------------
# Front Cover
# --------------------------------------------

# Add content
cover.create_cover(doc)

print('Front Cover Created')

# %% -----------------------------------------------------------------------------------------------
# Create Table of Contents

# doc.append(form.Command('newpage'))
doc.append(form.Command('tableofcontents'))


print('Table of Contents added')

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
# --------------------------------------------
# Section: Deployment Details
# --------------------------------------------

doc.append(form.Command('newpage'))

with doc.create(form.Section('Deployment Details')):

    DepDet.intro_table(doc)
    QCR.intro_comments(doc)
    DepDet.instrument_table(doc)
    DepDet.parameter_table(doc)
    DepDet.timeinout_table(doc)
    DepDet.file_tables(doc)
    DepDet.toolbox_bullet(doc)

print('Section added: ''Deployment Details''')

# %% -----------------------------------------------------------------------------------------------
# --------------------------------------------
# Section: Plots
# --------------------------------------------
# 

with doc.create(form.Section('Plots')):
    
    Addp.addMap(doc,setup.site_name)
    doc.append(form.Command('newpage'))
    Addp.addTDplot(doc,setup.site_name,setup.deployment_file_date_identifier)
    doc.append(form.Command('newpage'))
    Addp.addPlotDeployment(doc,setup.site_name,setup.deployment_file_date_identifier)
    doc.append(form.Command('newpage'))
    Addp.addDepCoverage(doc)
    doc.append(form.Command('newpage'))
    Addp.addVertCoverage(doc)
    doc.append(form.Command('newpage'))
    Addp.addTimeSeriesplots(doc)
    doc.append(form.Command('newpage'))
    Addp.addClimplots(doc)
    doc.append(form.Command('newpage'))
    Addp.addVelEllipse(doc)
    doc.append(form.Command('newpage'))
    Addp.addVelBoxplots_VCUR(doc)
    doc.append(form.Command('newpage'))
    Addp.addVelBoxplots_UCUR(doc)
    doc.append(form.Command('newpage'))
    Addp.addCTDMooringplot(doc,setup.site_name,setup.deployment_file_date_identifier)


print('Section added: ''Plots''')


# %% -----------------------------------------------------------------------------------------------
# --------------------------------------------
# Section: Quality Control
# --------------------------------------------

doc.append(form.Command('newpage'))
with doc.create(form.Section('Quality Control')):

    QCR.QC_comments(doc)   
    
print('Section added: ''Quality Control''')

# %% -----------------------------------------------------------------------------------------------
# --------------------------------------------
# Section: Toolbox Plots
# --------------------------------------------

with doc.create(form.Section('Toolbox Plots')):
    tbp.toolbox_plots(toolbox_dir,doc)

print('Section added: ''Toolbox Plots''')

# %% -----------------------------------------------------------------------------------------------
# --------------------------------------------
# Section: Mooring Diagram
# --------------------------------------------

with doc.create(form.Section('Mooring Diagram')):
    
    with doc.create(form.Figure(position='h!')) as pic:
        pic.add_image((mooring_dir), 
                          width=form.NoEscape(r'0.8\linewidth'))
        pic.add_caption('Mooring Diagram')   
        
print('Section added: ''Mooring Diagrams''')


#------------------------------------------------------------
# Information 
#-------------

# This part creates the main bulk of the PDF document.  
# Each section has a corresponding python script/module that 
# creates the section and adds content.

# If there is an error related to the PDF content, it likely
# originates from one of the above functions - see 
# corresponding python scripts/modules.  

#------------------------------------------------------------

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
# --------------------------------------------
# Section: Appendix
# --------------------------------------------

with doc.create(form.Appendix()):
    with doc.create(form.Section('Appendix: Ocean Current Images')):
        Addp.addOCplots(doc)    
    with doc.create(form.Section('Appendix: Deployment Photographs')):
        DepPhoto.include_photos(depphoto_dir,doc)
        
print('Section added: ''Appendix''')

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
# Save report

print('Saving report in: ' + saving_dir)

filename = (saving_dir + setup.site_name + '_' + setup.deployment_file_date_identifier + 
            '_QC_report')
# First time to create the TOC file
try:
    # try/except bypasses the non-terminal CalledProcessError
    doc.generate_pdf(filename,compiler='pdflatex')
except:
    # check file was created, if not create warning
    check = os.path.exists(filename + '.pdf')
    if check == False:
        warnings.warn('Warning!! file: ' + filename + '.pdf was not created. Investigation required.')
    pass
# second time to include the TOCs
try:
    # try/except bypasses the non-terminal CalledProcessError
    doc.generate_pdf(filename,compiler='pdflatex')
except:
    pass
doc.generate_tex(filename)
print('Report saved.')

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# %% -----------------------------------------------------------------------------------------------
# tidy-up (remove unnecessary files in directory)

os.chdir(saving_dir)
aux_files = glob.glob(saving_dir + '*.aux')
toc_files = glob.glob(saving_dir + '*.toc')
out_files = glob.glob(saving_dir + '*.out')
log_files = glob.glob(saving_dir + '*.log')
tex_files = glob.glob(saving_dir + '*.tex')

# remove all but PDFs
for n in range(len(aux_files)):
    os.remove(aux_files[n])
for n in range(len(toc_files)):
    os.remove(toc_files[n])    
for n in range(len(out_files)):
    os.remove(out_files[n])      
for n in range(len(log_files)):
    os.remove(log_files[n])      
for n in range(len(tex_files)):
    os.remove(tex_files[n])      

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
