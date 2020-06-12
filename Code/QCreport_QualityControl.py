#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Fri Jun 12 09:29:41 2020
# Contributers:  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# contact email: m.hemming@unsw.edu.au

# Section: Toolbox Plots

# %% -----------------------------------------------------------------------------------------------
# Import packages

import QCreport_paths as paths
import glob
from fpdf import FPDF
import QCreport_format as form
import QCreport_DeploymentDetails as DepDet
import QCreport_netCDF as nc

# %% -----------------------------------------------------------------------------------------------
# Useful functions

date = {}
test = {}
comment = {}

def separate_hist(his):
    
    string = str(his)
    split_string = string.rsplit('\\n')
    
    for n_s in range(len(split_string)):
        
        ss =split_string[n_s]
        fz = ss.find('Z')
        ss_aftert = ss[fz:]
        fh = ss_aftert.find('-') + fz
        fc = ss_aftert.find(':') + fz
        dt = ss[0:fz]
        tt = ss[fh+2:fc]
        comm = ss[fc+1:]
        
        date[n_s] = DepDet.remove_characters(dt)
        test[n_s] = DepDet.remove_characters(tt)
        comment[n_s] = DepDet.remove_characters(comm)
        
#    date = date[0:len(split_string)] 
#    test = test[0:len(split_string)] 
#    comment = comment[0:len(split_string)] 
        
    class hist_c:
        date = nc.select_keys(date,len(split_string))
        test = nc.select_keys(test,len(split_string))
        comment = nc.select_keys(comment,len(split_string))
        
    return hist_c
    
    


# %% -----------------------------------------------------------------------------------------------
# Create intro table of details    

def QC_comments(report):
    
    report.set_font_size(14)
    form.add_space()
    
    for inst_n in range(len(DepDet.atts_instrument)):
        
        inst = DepDet.remove_characters(str(DepDet.atts_instrument[inst_n]))
        nd = DepDet.remove_characters(str(DepDet.atts_instrument_nominal_depth[inst_n]))
        nd = str(int(float(nd)))   
        
        #---------------------------------
        # Add QC log for each instrument         
            
        
        
        
            
        #---------------------------------
        # Add QC history for each instrument        
        
        form.sub_header(inst + ' ' + nd + ' m')
        form.add_space()
        report.set_font('Helvetica',style='B',size=16)
        report.cell(80,6,'History',0,0,'L');
        form.add_space()
        form.add_space()
        report.ln(2)      
        history = separate_hist(DepDet.atts_history[inst_n])
        
        for hist_n in range(len(history.date)):
            
            report.set_font('Helvetica',style='B',size=12)
            report.multi_cell(180,6,history.date[hist_n] + '  --->  ' + history.test[hist_n],0,0,'L');
            report.ln(2)
            report.set_font('Helvetica',style='',size=12)            
            report.ln(2)
            form.add_space()            
            form.bullet_point_multi(history.comment[hist_n],12)
            report.ln()    
        
        
        
        
        
        
        
        


