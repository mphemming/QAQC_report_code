#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Mon Jul 13 14:31:31 2020
# Contributers (code):  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# Contributers (review): Moninya Roughan (NSW-IMS), Tim Austin (NSW-IMOS), Stuart Milburn (NSW-IMOS) 
# contact email: m.hemming@unsw.edu.au


# %% -----------------------------------------------------------------------------------------------
# Import packages

# Python Packages
from fpdf import FPDF
import fpdf
# QC report modules
import QCreport_paths as paths
import QCreport_setup as setup
import QCreport_format as form

# %% -----------------------------------------------------------------------------------------------
# Create front cover

def create_cover(report):
    
    #-----------------------------------------------
    # Front Cover
    #-----------------------------------------------
    # Add IMOS wave image
    report.add_page()   
    report.image(paths.cover_dir + 'Cover_1.png',h=200,w=250,x=-10,y=30)
    report.image(paths.cover_dir + 'CMSI_logo.png',h=35,w=60,x=15,y=250)
    report.image(paths.cover_dir + 'UNSW-Sydney-logo.png',h=35,w=60,x=75,y=250)    
    report.image(paths.cover_dir + 'sims_logo.png',h=35,w=60,x=135,y=250)       
    # Add Document title and names
    report.ln(30)
    report.set_text_color(r=255,g=255,b=255)
    form.title_header('Report on the Quality Control of the NSW-IMOS Australian National Moorings Network site:')
    report.ln(3)
    report.set_font('Helvetica', size=18, style ='B')
    report.cell(200, 10, setup.site_name + '  |  Deployment ' + setup.deployment, 0, 2, 'l')       
    report.ln(3)    
    report.cell(200, 10, setup.name_of_reportmaker, 0, 2, 'l') 
    report.ln(3)    
    report.cell(200, 10, setup.now, 0, 2, 'l') 
    report.ln(3)  
    report.set_text_color(r=0,g=0,b=0)    
    #-----------------------------------------------
    # Second page
    #-----------------------------------------------
    report.add_page()    
    report.image(paths.cover_dir + 'legal_stuff.png',h=120,w=160,x=20,y=20)    
    report.ln(135)
    report.set_font('Helvetica', size=10, style ='')
    report.set_left_margin(20)
    report.multi_cell(140, 4, setup.citation, 0, 2, 'l')  
    report.set_left_margin(10)
    report.image(paths.cover_dir + 'NCRIS.png',h=20,w=160,x=20,y=165)  

     
    
    
    