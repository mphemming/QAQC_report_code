# -*- coding: utf-8 -*-

# Created on Fri Jun  5 10:03:39 2020
# Contributers:  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# contact email: m.hemming@unsw.edu.au

# Section: Deployment Details


# %% -----------------------------------------------------------------------------------------------
# Import packages

from fpdf import FPDF
import QCreport_paths as paths
import QCreport_format as form
import QCreport_netCDF as nc
import numpy as np

# %% -----------------------------------------------------------------------------------------------
# get netCDF attributes for section

attributes_TEMP = nc.get_netCDF(paths.ncdir_TEMP())
attributes_CURR = nc.get_netCDF(paths.ncdir_CURR())
attributes_BGC = nc.get_netCDF(paths.ncdir_BGC())
# combine all attributes
class_fields = dir(attributes_TEMP)
class_fields = class_fields[-25:-1]

for n_atts in range(len(class_fields)-1):
    
    exec('att_' + str(class_fields[n_atts]) + ' = [attributes_TEMP.' + str(class_fields[n_atts]) 
        + ', attributes_CURR.' + str(class_fields[n_atts]) + ', attributes_BGC.' + str(class_fields[n_atts]) + ']')


# %% -----------------------------------------------------------------------------------------------
# Useful functions

# Function to get unique strings in attributes (i.e. from n number of netCDF files)
def get_unique(dict):
    list_dict = list(dict.values())
    unique_dicts = np.unique(list_dict)
    return unique_dicts

def remove_characters(string):
    
    string = string.replace('[','')
    string = string.replace(']','')
    string = string.replace("'",'')
    string = string.replace('odict_keys(','')
    string = string.replace(')','')
    string = string.replace('\n','')
    return string

def param_avail(string):
    
    param_list_TIME = []
    param_list_TEMP = []
    param_list_PRES = []
    param_list_DEPTH = []
    param_list_PSAL = []
    
    for n_files in range(len(attributes.instrument)-1):
        vn_file = remove_characters(str(attributes.var_names[n_files]))
        # TIME available?
        if vn_file.find('TIME') > -1 :
            n = 1
            param_list_TIME.append(n)
        else:
            n = 0
            param_list_TIME.append(n)                
        # TEMP available?
        if vn_file.find('TEMP') > -1 :
            n = 1
            param_list_TEMP.append(n)
        else:
            n = 0
            param_list_TEMP.append(n)
        # PSAL available?
        if vn_file.find('PSAL') > -1 :
            n = 1
            param_list_PSAL.append(n)
        else:
            n = 0
            param_list_PSAL.append(n)               
        # PRES available?
        if vn_file.find('PRES') > -1 or vn_file.find('PRES_REL') > -1:
            n = 1
            param_list_PRES.append(n)
        else:
            n = 0
            param_list_PRES.append(n) 
        # DEPTH available?
        if vn_file.find('DEPTH') > -1 :
            n = 1
            param_list_DEPTH.append(n)
        else:
            n = 0
            param_list_DEPTH.append(n)             
            

# %% -----------------------------------------------------------------------------------------------
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
start_date = remove_characters(str(start_date))
# if string is too long, it include hours, mins, etc. 
# remove unuseful string characters and select date only
if len(start_date) > 10:
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
    end_date = un_ed
    
# convert from array to string       
end_date = remove_characters(str(end_date))
# if string is too long, it include hours, mins, etc. 
# remove unuseful string characters and select date only
if len(end_date) > 10:
    end_date = end_date[0:10]

# %% -----------------------------------------------------------------------------------------------
# Other information for section
    
    
PO = str(attributes.principal_investigator[0])  
FT = str(attributes.author[0])  
lon = str(attributes.geospatial_lon_min[0]) # assuming min/max is the same, and same for each file
lat = str(attributes.geospatial_lat_min[0]) # assuming min/max is the same, and same for each file
lon = lon[0:6]
lat = lat[0:6]
tb_vers = remove_characters(str(get_unique(attributes.toolbox_version)))
ltz = remove_characters(str(round(int(get_unique(attributes.local_time_zone)))))
tu = remove_characters(str(get_unique(attributes.time_units)))
vn = remove_characters(str(get_unique(attributes.var_names)))

# %% -----------------------------------------------------------------------------------------------
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
       
    
    
# %% -----------------------------------------------------------------------------------------------
# Create instrument table
    
def instrument_table(report):

    form.sub_header('Instrument Serial Numbers and Nominal Depths')    
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
        nd = str(int(attributes.instrument_nominal_depth[row_n]))
        ti = 'INSERT'
        to = 'INSERT'      
        
        report.cell(60,8,inst,1,0,'C');     
        report.cell(35,8,sn,1,0,'C');         
        report.cell(40,8,nd,1,0,'C'); 
        report.cell(30,8,ti,1,0,'C');             
        report.cell(30,8,to,1,0,'C');
        report.ln() 

# IDEA FOR LATER, COLOR THE CELLS WHEE THERE IS A PT SENSOR
        
# %% -----------------------------------------------------------------------------------------------
# Create parameters table  
        
#def parameter_table(report):
      
    
    
    


# %% -----------------------------------------------------------------------------------------------
# Create instrument Time in / Time out table
     
def timeinout_table(report):  
     
    form.sub_header('Instruments times in / out')
    report.set_font_size(12)    
     
# %% -----------------------------------------------------------------------------------------------
# Create instrument file table and details bullet list
    
def files_table(report):
     
    report.add_page()
    form.sub_header('File Locations')
    report.set_font_size(12)    
    form.add_space()  
    form.add_space()
    form.add_space()
    #---------------------------------
    # Header
    report.set_font('Helvetica',style='B')
    report.cell(80,8,"Instrument & nom. depth",1,0,'C');     
    report.cell(100,8,"File Location",1,0,'C');  
    report.ln()    
    #---------------------------------
    # add rows using loop      
    for row_n in range(len(attributes.instrument)): 
        
        inst = str(attributes.instrument[row_n])
        nd = str(int(round(attributes.instrument_nominal_depth[row_n])))        
        file = str(attributes.toolbox_input_file[row_n])
        report.set_font('Helvetica',style='B')
        report.cell(80,18,inst + '  ' + nd + ' m',1,0,'L');
        report.set_font('Helvetica',style='')
        report.multi_cell(100,6,file,1,0,'C'); 
        
def instrument_bullets(report):
    
    form.add_space()     
    form.add_space() 
    report.set_font_size(12)         
    form.bullet_point('Toolbox version: ' + tb_vers)
    
    
    
    
    
    
    
    
    
    




    
    






    
    
    
    