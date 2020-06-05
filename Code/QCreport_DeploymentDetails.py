# -*- coding: utf-8 -*-

# Created on Fri Jun  5 10:03:39 2020
# Contributers:  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# contact email: m.hemming@unsw.edu.au

# Section: Deployment Details


# -----------------------------------------------------------------------------------------------
# Import packages

from fpdf import FPDF
import QCreport_paths as paths
import QCreport_format as form
import QCreport_netCDF as nc
import numpy as np

# -----------------------------------------------------------------------------------------------
# get netCDF attributes for section

attributes = nc.get_netCDF(paths.ncdir())

# -----------------------------------------------------------------------------------------------
# Useful functions

# Function to get unique strings in attributes (i.e. from n number of netCDF files)
def get_unique(dict):
    list_dict = list(dict.values())
    unique_dicts = np.unique(list_dict)
    return unique_dicts

# -----------------------------------------------------------------------------------------------
# Determine date range of deployment
    
# Possible future issues:
# o deployments where data were collected/retrieved on different days (comparing instrument files)
# o Improvement may be to use min/max dates in those circumstances

# Start date
# -------------------
start_date = get_unique(attributes.time_coverage_start)
# if multiple start dates, get unique dates
if len(start_date) > 1:
    sd = []
    for n_sd in range(len(start_date)-1):
        dt = str(start_date[n_sd])
        dt = dt[0:10]
        sd.append(dt)
    un_sd = np.unique(sd)
    un_sd = str(un_sd.tolist())
    start_date = un_sd
# convert from array to string    
start_date = str(start_date)
# if string is too long, it include hours, mins, etc. 
# remove unuseful string characters and select date only
if len(start_date) > 10:
    start_date = start_date.replace('[','')
    start_date = start_date.replace(']','')
    start_date = start_date.replace("'","")
    start_date = start_date[0:10]
    
# end date
# -------------------
end_date = get_unique(attributes.time_coverage_end)
# if multiple end dates, get unique dates
if len(end_date) > 1:
    ed = []
    for n_ed in range(len(end_date)-1):
        dt = str(end_date[n_ed])
        dt = dt[0:10]
        ed.append(dt)
    un_ed = np.unique(ed)
    un_ed = str(un_ed.tolist())
    un_ed = un_ed.replace('[','')
    un_ed = un_ed.replace(']','')
    un_ed = un_ed.replace("'","")
    end_date = un_ed
# convert from array to string       
end_date = str(end_date)
# if string is too long, it include hours, mins, etc. 
# remove unuseful string characters and select date only
if len(end_date) > 10:
    end_date = end_date.replace('[','')
    end_date = end_date.replace(']','')
    end_date = end_date.replace("'","")
    end_date = end_date[0:10]

# -----------------------------------------------------------------------------------------------
# Other information for table
    
    
PO = str(attributes.principal_investigator[0])  
FT = str(attributes.author[0])  
lon = str(attributes.geospatial_lon_min[0]) # assuming min/max is the same, and same for each file
lat = str(attributes.geospatial_lat_min[0]) # assuming min/max is the same, and same for each file
lon = lon[0:6]
lat = lat[0:6]


# -----------------------------------------------------------------------------------------------
# Create intro table of details    

def intro_table(report):
    
    report.set_font_size(12)
    report.set_fill_color(224,224,224)
    form.add_space()
    #---------------------------------
    # row 1
    report.set_font('Helvetica',style='B')
    report.cell(60,8,"Site",1,0,'L'); 
    report.set_font('Helvetica',style='')
    report.cell(80,8,"BMP070",1,0,'C');
    report.ln()
    #---------------------------------
    # row 2    
    report.set_font('Helvetica',style='B')
    report.cell(60,8,"Deployment",1,0,'L'); 
    report.set_font('Helvetica',style='')
    report.cell(80,8,paths.deployment,1,0,'C');
    report.ln()    
    #---------------------------------
    # row 3    
    report.set_font('Helvetica',style='B')
    report.cell(60,8,"Dates",1,0,'L'); 
    report.set_font('Helvetica',style='')
    report.cell(80,8,start_date + '  |  ' + end_date,1,0,'C');
    report.ln()        
    #---------------------------------
    # row 4    
    report.set_font('Helvetica',style='B')
    report.cell(60,8,"Longitude",1,0,'L'); 
    report.set_font('Helvetica',style='')
    report.cell(80,8,lon,1,0,'C');
    report.ln()      
    #---------------------------------
    # row 5    
    report.set_font('Helvetica',style='B')
    report.cell(60,8,"Latitude",1,0,'L'); 
    report.set_font('Helvetica',style='')
    report.cell(80,8,lat,1,0,'C');
    report.ln()      
    #---------------------------------
    # row 6    
    report.set_font('Helvetica',style='B')
    report.cell(60,8,"Principal Investigator",1,0,'L'); 
    report.set_font('Helvetica',style='')
    report.cell(80,8,PO,1,0,'C');
    report.ln()     
    #---------------------------------
    # row 7    
    report.set_font('Helvetica',style='B')
    report.cell(60,8,"Field Team",1,0,'L'); 
    report.set_font('Helvetica',style='')
    report.cell(80,8,FT,1,0,'C');
    report.ln()
       
    
    
# -----------------------------------------------------------------------------------------------
# Create instrument table
    
def instrument_table(report):
    
    report.set_font_size(12)    
    form.add_space()  
    form.add_space()
    form.add_space()
    #---------------------------------
    # Header
    report.set_font('Helvetica',style='B')
    report.cell(60,8,"Instrument",1,0,'C');     
    report.cell(35,8,"Serial Number",1,0,'C');         
    report.cell(40,8,"Nominal Depth",1,0,'C'); 
    report.cell(30,8,"Time in",1,0,'C');             
    report.cell(30,8,"Time Out",1,0,'C');
    report.ln() 
    #---------------------------------
    # add rows using loop
    report.set_font('Helvetica',style='')
    for row_n in range(len(attributes.instrument)):
    
        inst = str(attributes.instrument[row_n])
        sn = str(attributes.instrument_serial_number[row_n])
        nd = str(attributes.instrument_nominal_depth[row_n])
        ti = 'INSERT'
        to = 'INSERT'      
        
        report.cell(60,8,inst,1,0,'C');     
        report.cell(35,8,sn,1,0,'C');         
        report.cell(40,8,nd,1,0,'C'); 
        report.cell(30,8,ti,1,0,'C');             
        report.cell(30,8,to,1,0,'C');
        report.ln() 

# IDEA FOR LATER, COLOR THE CELLS WHEE THERE IS A PT SENSOR
        
# -----------------------------------------------------------------------------------------------
# Create instrument file table
    
# attributes.toolbox_input_file
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




    
    






    
    
    
    