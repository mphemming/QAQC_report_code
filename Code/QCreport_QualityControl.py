#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Fri Jun 12 09:29:41 2020
# Contributers (code):  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# Contributers (review): Moninya Roughan (NSW-IMS), Tim Austin (NSW-IMOS), Stuart Milburn (NSW-IMOS) 
# contact email: m.hemming@unsw.edu.au

# Section: Quality Control

# %% -----------------------------------------------------------------------------------------------
# Import packages
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# QCreport modules
import QCreport_format as form
import QCreport_DeploymentDetails as DepDet
import QCreport_netCDF as nc
import QCreport_setup as setup

#------------------------------------------------------------
# Information 
#-------------

# These are the QC report modules required to run 
# this script. The QCreport modules need to be in 
# the same folder as this script to work. 

#------------------------------------------------------------

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# %% -----------------------------------------------------------------------------------------------
# Useful functions
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# create empty lists
date = {}
test = {}
comment = {}

###################################################################
#__________________________________________________________________
# Reason: obtain date, QC test name, and corresponding comment strings
# Usage: this script only

def separate_hist(his):
    
    # convert input to string
    string = str(his)
    # split string using newline html code
    split_string = string.rsplit('\\n')
    # for each split string, determine date, QC test, and corresponding comments
    for n_s in range(len(split_string)):
        # obtain string for this iteration
        ss =split_string[n_s]
        # find locations of letter 'Z' (related to time)
        fz = ss.find('Z')
        # use split string text after 'Z'
        ss_aftert = ss[fz:]
        # find location of hyphen
        fh = ss_aftert.find('-') + fz
        # find location of colon
        fc = ss_aftert.find(':') + fz
        # use locations of characters to extract string information
        dt = ss[0:fz]
        tt = ss[fh+2:fc]
        comm = ss[fc+1:]
        # save string information, removing unecessary characters if applicable
        date[n_s] = DepDet.remove_characters(dt)
        test[n_s] = DepDet.remove_characters(tt)
        comment[n_s] = DepDet.remove_characters(comm)
    # save string information as a class    
    class hist_c:
        date = nc.select_keys(date,len(split_string))
        test = nc.select_keys(test,len(split_string))
        comment = nc.select_keys(comment,len(split_string))
    # ensure class hist_c is accessed from function    
    return hist_c

###################################################################

###################################################################
#__________________________________________________________________
# Reason: split quality control log information into strings for 
#         each QC test performed
# Usage: this script only
    

def separate_log(QClog):
    
    # convert input to string    
    string = str(QClog)
    # split string using newline html code
    split_string = string.rsplit('\\n')
    # ensure split string is accessed from function
    return split_string

###################################################################

#------------------------------------------------------------
# Information 
#-------------

# These functions are used to split the strings containing
# attributes 'history' and 'quality_control_log' into smaller
# strings: e.g. date, test name, comment strings

#------------------------------------------------------------
    
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________  


# %% -----------------------------------------------------------------------------------------------
# Create intro table of details    
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________    

###################################################################
#__________________________________________________________________
# Reason: add content to section 'Quality Control' - history and quality_control_log information
# Usage: QCreport.py


def QC_comments(report):
    # set font size
    report.set_font_size(14)
    # add vertical space
    form.add_space()
    # For each deployment file, add quality control log and history information  
    for inst_n in range(len(DepDet.atts_instrument)):
        
        # get instrument and nominal depth strings 
        inst = DepDet.remove_characters_QC(str(DepDet.atts_instrument[inst_n]))
        nd = DepDet.remove_characters_QC(str(DepDet.atts_instrument_nominal_depth[inst_n]))
        if '.0' in nd:
            nd = str(int(float(nd)))   
        
        #---------------------------------
        # add instrument sub headings        
        form.sub_header(inst + ' ' + nd + ' m')
        # draw horizontal line
        form.add_line()
        # add vertical space
        form.add_space()
        #---------------------------------
        
        #---------------------------------
        # add QC log for each instrument         
        form.add_space()
        # add subheading
        report.set_font('Helvetica',style='B',size=16)
        report.cell(80,6,'Quality Control Log',0,0,'L');
        # add vertical space
        form.add_space()
        form.add_space()  
        # obtain string information from attribute 'quality_control_log'
        QClog = separate_log(DepDet.atts_quality_control_log[inst_n])
        # for each quality control log account, create bullet point
        for log_n in range(len(QClog)):    
            # set font
            report.set_font('Helvetica',style='B',size=12)
            # create bullet point for quality control log account
            form.bullet_point_multi(DepDet.remove_characters_QC(QClog[log_n]),12)     
            # go to next line
            report.ln() 
        #---------------------------------    
   
        #---------------------------------
        # add QC history for each instrument
        # add vertical space        
        form.add_space()
        # set font
        report.set_font('Helvetica',style='B',size=16)
        # add subheading
        report.cell(80,6,'History',0,0,'L');
        # add vertical space
        form.add_space()
        form.add_space()
        # add vertical space
        report.ln(2)   
        # obtain string information from attribute 'history'
        history = separate_hist(DepDet.atts_history[inst_n])
        # display information for each QC test
        for hist_n in range(len(history.date)):
            # set font
            report.set_font('Helvetica',style='B',size=12)
            # add bullet point subheading
            report.multi_cell(180,6,history.date[hist_n] + '  --->  ' + history.test[hist_n],0,0,'L');
            # add vertical space
            report.ln(2)
            # set font
            report.set_font('Helvetica',style='',size=12)
            # add vertical space            
            report.ln(2)
            # add vertical space 
            form.add_space()   
            # add bullet point
            form.bullet_point_multi(history.comment[hist_n],12)
            # go to next line
            report.ln()    
        #---------------------------------    
            
###################################################################            
   
###################################################################
#__________________________________________________________________
# Reason: add further comments to section 'Quality Control' 
# Usage: QCreport.py
     
        
def intro_comments(report):
    
    #---------------------------------
    # add sub heading        
    form.sub_header('Deployment Assessment')
    # add vertical space
    form.add_space()
    #------------------------------------------
    # Add QC assessment details as table
    #------------------------------------------
    report.set_font_size(12)
    report.set_fill_color(224,224,224)
    form.add_space()
    #---------------------------------
    # row 1
    report.set_font('Helvetica',style='B')
    report.cell(60,8,"QC undertaken",1,0,'L'); 
    report.set_font('Helvetica',style='')
    report.cell(70,8,setup.QCcomment,1,0,'L');
    report.ln()
    #---------------------------------
    # row 2    
    report.set_font('Helvetica',style='B')
    report.cell(60,8,"QC type",1,0,'L'); 
    report.set_font('Helvetica',style='')
    report.cell(70,8,setup.QCmethod,1,0,'L');
    report.ln()    
    #---------------------------------
    # row 3    
    report.set_font('Helvetica',style='B')
    report.cell(60,8,"Fieldwork issues",1,0,'L'); 
    report.set_font('Helvetica',style='')
    report.cell(70,8,setup.Fieldwork_issues,1,0,'L');
    report.ln()        
    #---------------------------------
    # row 4    
    report.set_font('Helvetica',style='B')
    report.cell(60,8,"Sensor Damage",1,0,'L'); 
    report.set_font('Helvetica',style='')
    report.cell(70,8,setup.Sensor_damage,1,0,'L');
    report.ln()       
    #---------------------------------
    # row 5    
    report.set_font('Helvetica',style='B')
    report.cell(60,8,"Lost Equipment",1,0,'L'); 
    report.set_font('Helvetica',style='')
    report.cell(70,8,setup.Lost_equipment,1,0,'L');
    report.ln()       
    #---------------------------------
    # row 6    
    report.set_font('Helvetica',style='B')
    report.cell(60,8,"Biofouling",1,0,'L'); 
    report.set_font('Helvetica',style='')
    report.cell(70,8,setup.Biofouling,1,0,'L');
    report.ln()      
    #---------------------------------
    # row 7    
    report.set_font('Helvetica',style='B')
    report.cell(60,8,"Other issues",1,0,'L'); 
    report.set_font('Helvetica',style='')
    report.cell(70,8,setup.Other_issues,1,0,'L');
    report.ln()       
    #---------------------------------
    # row 8    
    report.set_font('Helvetica',style='B')
    report.cell(60,8,"Additional QC",1,0,'L'); 
    report.set_font('Helvetica',style='')
    report.cell(70,8,setup.Additional_QC,1,0,'L');
    report.ln()       
    #---------------------------------
    # term explainer after table
    report.ln() 
    report.set_font('Helvetica',style='',size=10) 
    report.cell(70,4,'Options: ''None'', ''Some'', ''Moderate'', ''Substantial''',0,0,'L');    
    report.ln()      
    report.cell(70,4,'QC type options: ''Automatic'', ''Manual'', ''Automatic and manual''',0,0,'L');    
    report.ln()      
    #---------------------------------
    # comments
    # add sub heading        
    form.sub_header('Comments')
    # add vertical space
    form.add_space()    
    # set font
    report.set_font('Helvetica',style='',size=12) 
    # add vertical space           
    report.ln(2)
    # add vertical space
    form.add_space()            
    # add comments to PDF 
    report.multi_cell(180,6,setup.comments,0,0,'L')
    # go to next line
    report.ln()      
    
    
    
    
###################################################################    
    
#------------------------------------------------------------
# Information 
#-------------

# These functions are used to add content to the report in
# section 'Quality Control'. File history and quality_control_log
# attributes are loaded from netCDF file and content displayed.
# Introductory comments included - section will be blank if comments
# string is not filled in QCreport module 'QCreport_IntroComments.py'. 
    
    
#------------------------------------------------------------    
    
            
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________        
        
        
        
        


