
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
import QCreport_AdditionalPlots as Addp

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
geometry_options = {"tmargin": "2cm", "lmargin": "2cm"}
doc = form.Document(geometry_options=geometry_options,
                    font_size='large')
doc.append(form.Command('fontsize', arguments = ['18', '16']))

# Latex packages
doc.packages.append(form.Package('rotating')) # for rotating toolbox plots
doc.packages.append(form.Package('lmodern')) # change font to 'palatino'
doc.packages.append(form.Package('sectsty'))
doc.packages.append(form.Package('titlesec','compact, big'))
doc.packages.append(form.Package('placeins','section')) # ensures plots stay in correct section, and don't float around
doc.packages.append(form.Package('graphicx')) # for front cover images

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

doc.append(form.Command('newpage'))
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
    
    Addp.addOCplots(doc)

print('Section added: ''Plots''')

# %% -----------------------------------------------------------------------------------------------
# --------------------------------------------
# Section: Deployment Photographs
# --------------------------------------------

with doc.create(form.Section('Deployment Photographs')):
    
    DepPhoto.include_photos(depphoto_dir,doc)

print('Section added: ''Deployment Photographs''')

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
# Save report

print('Saving report in: ' + saving_dir)

filename = (saving_dir + setup.site_name + '_' + setup.deployment + 
            '_QC_report')
doc.generate_pdf(filename,compiler='pdflatex')
doc.generate_tex(filename)
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








