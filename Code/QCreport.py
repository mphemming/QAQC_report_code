#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Thu Jun  4 13:42:02 2020
# Contributers (code):  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# Contributers (review): Moninya Roughan (NSW-IMS), Tim Austin (NSW-IMOS), Stuart Milburn (NSW-IMOS) 
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
report = form.format_doc(setup.name_of_reportmaker)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
# Sections


# --------------------------------------------
# Front Cover
# --------------------------------------------

# Add content
cover.create_cover(report)

print('Front Cover Created')

# --------------------------------------------
# Section: Deployment Details
# --------------------------------------------

# Deployment Details heading
report.add_page(orientation='p')
form.section_header('Deployment Details')
# setup table of contents link
DD = report.add_link()
report.set_link(DD)
# Add content
DepDet.intro_table(report)
QCR.intro_comments(report)
DepDet.instrument_table(report)
DepDet.parameter_table(report)
DepDet.timeinout_table(report)
DepDet.file_tables(report)
DepDet.toolbox_bullet(report)

print('Section added: ''Deployment Details''')

# --------------------------------------------
# Section: Deployment Photographs
# --------------------------------------------

# Deployment Photos heading
report.add_page(orientation='p')
form.section_header('Deployment Photographs')
# setup table of contents link
DPP = report.add_link()
report.set_link(DPP)
# Add content
DepPhoto.include_photos(depphoto_dir,report)

print('Section added: ''Deployment Photographs''')

# --------------------------------------------
# Section: Quality Control
# --------------------------------------------

# Quality Control heading
report.add_page(orientation='p')
form.section_header('Quality Control')
# setup table of contents link
QC = report.add_link()
report.set_link(QC)
# Add content
QCR.QC_comments(report)

print('Section added: ''Quality Control''')

# --------------------------------------------
# Section: Toolbox Plots
# --------------------------------------------

# Toolbox Plots heading
report.add_page(orientation='l')
form.section_header('Toolbox Plots')
# setup table of contents link
TBP = report.add_link()
report.set_link(TBP)
# Add content
tbp.toolbox_plots(toolbox_dir,report)

print('Section added: ''Toolbox Plots''')

# --------------------------------------------
# Section: Mooring Diagram
# --------------------------------------------

# Mooring diagram heading
report.add_page(orientation='p')
form.section_header('Mooring Diagram')
# setup table of contents link
MD = report.add_link()
report.set_link(MD)
# Add image
report.image(mooring_dir)

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
# Header and Table of Contents

report.add_page(orientation='p')

# Main Header
report.set_font_size(28)
report.cell(200, 10, form.title_1, 0, 2, 'C') 
report.set_font_size(22)
report.cell(200, 10, form.title_2, 0, 2, 'C') 

# line break
report.ln(30)

# interactive table of contents

# Add section header
form.section_header('Report Contents')

form.TOC('Deployment Details',DD)
form.TOC('Mooring Diagram',MD)
form.TOC('Quality Control',QC)
form.TOC('Deployment Photographs',DPP)
form.TOC('Toolbox Plots',TBP)

print('Table of Contents added')

#------------------------------------------------------------
# Information 
#-------------

# This part creates an interactive table of contents. This
# is not fully working as hoped yet as the table of contents
# needs to be at the start of the document, rather than at
# the end. I haven't yet figured out how to include it at 
# the start without the links ceasing to work. 

#------------------------------------------------------------

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
# Save report

print('Saving report in: ' + saving_dir)
report.output(saving_dir + setup.site_name + '_' + setup.deployment + '_QC_report.pdf', 'F')
print('Report saved.')

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# %% -----------------------------------------------------------------------------------------------
# Reorganise PDF report so that title and table of contents is at the beginning of the document

# THIS METHOD DOES NOT WORK. THE TOC LINKS NO LONGER WORK... LOOK FOR ANOTHER METHOD

#PDF_report = PdfFileReader(saving_dir + setup.site_name + '_' + setup.deployment + '_QC_report.pdf')
#pdf_bulk_writer = PdfFileWriter()
#output_filename_bulk = "bulk.pdf"
#pdf_TOC_writer = PdfFileWriter()
#output_filename_TOC = "TOC.pdf"
#
#for page in range(PDF_report.getNumPages()):
#    current_page = PDF_report.getPage(page)
#    if page == PDF_report.getNumPages()-1:
#        pdf_TOC_writer.addPage(current_page)
#    if page <= PDF_report.getNumPages()-2:
#        pdf_bulk_writer.addPage(current_page)
#        
## Write the data to disk
#with open(output_filename_TOC, "wb") as out:
#     pdf_TOC_writer.write(out)
#     print("created", output_filename_TOC)       
#
## Write the data to disk
#with open(output_filename_bulk, "wb") as out:
#     pdf_bulk_writer.write(out)
#     print("created", output_filename_bulk)   
#
#pdfs = ['TOC.pdf', 'bulk.pdf']
#
#merger = PdfFileMerger()
#
#for pdf in pdfs:
#    merger.append(pdf)
#    
#merger.write("result.pdf")
#merger.close()

# NOTES: USE PyPDF to REORGANISE THE DOCUMENT AFTERWARDS
# https://pythonhosted.org/PyPDF2/PageObject.html
# https://pythonhosted.org/PyPDF2/PdfFileReader.html
# https://www.blog.pythonlibrary.org/2018/06/07/an-intro-to-pypdf2/
# http://fpdf.org/en/doc/

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>








