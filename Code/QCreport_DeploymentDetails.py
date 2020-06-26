# -*- coding: utf-8 -*-

# Created on Fri Jun  5 10:03:39 2020
# Contributers:  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# contact email: m.hemming@unsw.edu.au

# Section: Deployment Details


# %% -----------------------------------------------------------------------------------------------
# Import packages
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# Python Packages
import numpy as np
from datetime import datetime
# QC report modules
import QCreport_paths as paths
import QCreport_format as form
import QCreport_netCDF as nc


#------------------------------------------------------------
# Information 
#-------------

# These are the Python and QC report modules required to run 
# this script. The python modules should be installed using 
# 'pip/condo install', the QCreport modules need to be in 
# the same folder as this script.

#------------------------------------------------------------

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# %% -----------------------------------------------------------------------------------------------
# get netCDF attributes for section
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# get attributes for temperature, biogeochemistry and velocity files
attributes_TEMP = nc.get_netCDF(paths.netCDF_TEMP_dir)
attributes_SBE37 = nc.get_netCDF(paths.netCDF_SBE37_dir)
attributes_CTD = nc.get_netCDF(paths.netCDF_CTD_dir)
attributes_CURR = nc.get_netCDF(paths.netCDF_CURR_dir)
attributes_BGC = nc.get_netCDF(paths.netCDF_BGC_dir)
# combine all attributes
# get list of attributes
class_fields = dir(attributes_TEMP)
class_fields = class_fields[-27:-1]; # index determined after looking at class_fields
# execute string combinations as python code, substituting in each attribute name 
# the result: variables for each attribute and file ('atts_{attribute name>')
for n_atts in range(len(class_fields)):
    # create empty dictionary
    exec('atts_' + str(class_fields[n_atts]) + ' = {}')
    # combine all attributes from each sensor file
    if isinstance(attributes_TEMP,str) == 0:
        for n_keys in range(len(attributes_TEMP.abstract)):
            exec('atts_' + str(class_fields[n_atts]) + '[n_keys] = [attributes_TEMP.' + str(class_fields[n_atts]) + '[n_keys]]')  
    if isinstance(attributes_SBE37,str) == 0:
        for n_keys in range(len(attributes_SBE37.abstract)):
            exec('atts_' + str(class_fields[n_atts]) + '[n_keys] = [attributes_SBE37.' + str(class_fields[n_atts]) + '[n_keys]]')     
    if isinstance(attributes_CURR,str) == 0:    
        for n_keys in range(len(attributes_CURR.abstract)):
            n_keys_n = n_keys+len(attributes_TEMP.abstract)
            exec('atts_' + str(class_fields[n_atts]) + '[n_keys_n] = [attributes_CURR.' + str(class_fields[n_atts]) + '[n_keys]]')          
    if isinstance(attributes_BGC,str) == 0:    
        for n_keys in range(len(attributes_BGC.abstract)):
            n_keys_n = n_keys+len(attributes_TEMP.abstract)+len(attributes_CURR.abstract)
            exec('atts_' + str(class_fields[n_atts]) + '[n_keys_n] = [attributes_BGC.' + str(class_fields[n_atts]) + '[n_keys]]')  
    if isinstance(attributes_CTD,str) == 0:    
        for n_keys in range(len(attributes_CTD.abstract)):
            n_keys_n = n_keys+len(attributes_CTD.abstract)+len(attributes_CTD.abstract)
            exec('atts_' + str(class_fields[n_atts]) + '[n_keys_n] = [attributes_CTD.' + str(class_fields[n_atts]) + '[n_keys]]')  
# remove full file directory from 'atts_toolbox_input_file'
atts_toolbox_input_file_name = [] 
for n_atts in range(len(atts_toolbox_input_file)):
    
    a = str(atts_toolbox_input_file[n_atts])
    for n_char in range(len(a)-1):
        a_n = a[n_char:n_char+1]
        if a_n.find("\\") > -1:
            last_char = n_char       
    atts_toolbox_input_file_name.append(a[last_char+1:-1])
    
            
#------------------------------------------------------------
# Information 
#-------------

# This part loads attributes from netCDF files available in 
# data folder, for different kinds of sensors, and combines
# them into one variable per attribute (starting 'atts_')
        
# This part needs improving as the 'exec' function is 
# lazy programming .. 
        
# WARNING: as 'exec' uses strings as input, be very careful 
# what strings you use if editing! 

#------------------------------------------------------------        
        
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________         

# %% -----------------------------------------------------------------------------------------------
# Useful functions
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________


#------------------------------------------------------------   
# Function to get unique strings in attributes (i.e. from n number of netCDF files)     
def get_unique(dict):
    list_dict = list(dict.values())
    unique_dicts = np.unique(list_dict)
    return unique_dicts
#------------------------------------------------------------   
# Function to remove indices where no data exists 
# if is a string 'No data'
def rm_nodata(array):
    n_save = 0
    new_array = {}
    for n_elements in range(len(array)-1):
        a = array[n_elements]
        if ('No data' in a) == False:
            new_array[n_save] = a
        n_save = n_save +1          
    return new_array
#------------------------------------------------------------   
# Function to remove unnecessary characters
def remove_characters(string):
    string = string.replace('[','')
    string = string.replace(']','')
    string = string.replace("'",'')
    string = string.replace('odict_keys(','')
    string = string.replace(')','')
    string = string.replace('\n','')
    return string
#------------------------------------------------------------   
# Function to remove unnecessary characters
# For use with QC information
def remove_characters_QC(string):
    string = string.replace('[','')
    string = string.replace(']','')
    string = string.replace("'",'')
    string = string.replace('odict_keys(','')
    string = string.replace('\n','')
    return string
#------------------------------------------------------------   
# Function to determine which parameters are available
# in netCDF files
def param_avail(string):
    # Create list objects
    param_list_TIME = []
    param_list_TEMP = []
    param_list_PRES = []
    param_list_DEPTH = []
    param_list_PSAL = []
    param_list_DOX = []
    param_list_TURB = []
    param_list_CPHL = []
    param_list_DENS = []
    param_list_CNDC = []
    param_list_FLU = []
    param_list_VCUR = []
    param_list_UCUR = []
    # produce index indicating whether parameters available or not
    for n_files in range(len(atts_instrument)):
        vn_file = remove_characters(str(atts_var_names[n_files]))
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
        # DOX available?
        if vn_file.find('DOX') > -1 :
            n = 1
            param_list_DOX.append(n)
        else:
            n = 0
            param_list_DOX.append(n)  
        # CPHL available?
        if vn_file.find('CPHL') > -1 :
            n = 1
            param_list_CPHL.append(n)
        else:
            n = 0
            param_list_CPHL.append(n)     
        # TURB available?
        if vn_file.find('TURB') > -1 :
            n = 1
            param_list_TURB.append(n)
        else:
            n = 0
            param_list_TURB.append(n)  
        # DENS available?
        if vn_file.find('DENS') > -1 :
            n = 1
            param_list_DENS.append(n)
        else:
            n = 0
            param_list_DENS.append(n) 
        # CNDC available?
        if vn_file.find('CNDC') > -1 :
            n = 1
            param_list_CNDC.append(n)
        else:
            n = 0
            param_list_CNDC.append(n)                     
        # FLU available?
        if vn_file.find('FLU') > -1 :
            n = 1
            param_list_FLU.append(n)
        else:
            n = 0
            param_list_FLU.append(n)   
        # VCUR available?
        if vn_file.find('VCUR') > -1 :
            n = 1
            param_list_VCUR.append(n)
        else:
            n = 0
            param_list_VCUR.append(n)  
        # UCUR available?
        if vn_file.find('UCUR') > -1 :
            n = 1
            param_list_UCUR.append(n)
        else:
            n = 0
            param_list_UCUR.append(n)                      
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
    # save parameter indices in class called 'param_list'         
    class param_list:
        TIME = param_list_TIME
        TEMP = param_list_TEMP
        PRES = param_list_PRES
        DEPTH = param_list_DEPTH
        PSAL = param_list_PSAL
        DOX = param_list_DOX
        TURB = param_list_TURB
        CPHL = param_list_CPHL
        DENS = param_list_DENS
        CNDC = param_list_CNDC
        FLU = param_list_FLU
        VCUR = param_list_VCUR
        UCUR = param_list_UCUR   
    return param_list

#------------------------------------------------------------
# Information 
#-------------
        
# The above are functions that are useful to sort and prepare
# attribute information from the netCDF files for use in the
# PDF report. 

#------------------------------------------------------------

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________

# %% -----------------------------------------------------------------------------------------------
# Determine date range of deployment    
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________    

#------------------------------------------------------------
# Start date
#------------------------------------------------------------
start_date = get_unique(atts_time_coverage_start)
# if multiple start dates (if not all files same), get unique dates
if len(start_date) > 1:
    sd = []
    for n_sd in range(len(start_date)-1):
        dt = str(start_date[n_sd])
        dt = dt[0:10]
        sd.append(dt)
    un_sd = np.unique(sd)
    un_sd_ts = []
    for n in range(len(un_sd)):
        conversion = datetime.fromisoformat(un_sd[n]).timestamp()
        un_sd_ts.append(conversion) 
    
    un_sd = str(datetime.fromtimestamp(np.min(np.array(un_sd_ts))))
    start_date = un_sd
# convert from array to string    
start_date = remove_characters(str(start_date))
# if string is too long, it include hours, mins, etc. 
# remove unuseful string characters and select date only
if len(start_date) > 10:
    start_date = start_date[0:10]
 #------------------------------------------------------------   
# end date
#------------------------------------------------------------
end_date = get_unique(atts_time_coverage_end)
# if multiple start dates (if not all files same), get unique dates
if len(end_date) > 1:
    ed = []
    for n_ed in range(len(end_date)-1):
        dt = str(end_date[n_ed])
        dt = dt[0:10]
        ed.append(dt)
    un_ed = np.unique(ed)
    un_ed_ts = []
    for n in range(len(un_ed)):
        conversion = datetime.fromisoformat(un_ed[n]).timestamp()
        un_ed_ts.append(conversion) 
    
    un_ed = str(datetime.fromtimestamp(np.max(np.array(un_ed_ts))))
    end_date = un_ed
# convert from array to string       
end_date = remove_characters(str(end_date))
# if string is too long, it include hours, mins, etc. 
# remove unuseful string characters and select date only
if len(end_date) > 10:
    end_date = end_date[0:10]
    
#------------------------------------------------------------
# Information 
#-------------
        
# This section determines the start and end date of the 
# deployment for use in the intro table on page 1 of the report.

# If more than one date is available for the start and end dates, 
# the start and end date used is the minimum and maximum time
# number, respectively.

#------------------------------------------------------------    
    
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________    

# %% -----------------------------------------------------------------------------------------------
# Other information for section
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________    
    
# Principle Investigator
PO = remove_characters(str(atts_principal_investigator[0]))  
# Author
FT = remove_characters(str(atts_author[0]))
# Location
lon = str(atts_geospatial_lon_min[0]) # assuming min/max is the same, and same for each file
lat = str(atts_geospatial_lat_min[0]) # assuming min/max is the same, and same for each file
lon = remove_characters(lon[0:6])
lat = remove_characters(lat[0:6])
# Toolbox version
tb_vers = remove_characters(str(get_unique(atts_toolbox_version)))
# local time zone
ltz = remove_characters(str(round(int(get_unique(rm_nodata(atts_local_time_zone))))))
# time units
tu = remove_characters(str(get_unique(atts_time_units)))
# variable names
vn = remove_characters(str(get_unique(atts_var_names)))

#------------------------------------------------------------
# Information 
#-------------
        
# Information extraction: things like Principle investigator, 
# location, variable names, for use in QC report.

#------------------------------------------------------------  

# %% -----------------------------------------------------------------------------------------------
# Create intro table of details
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________    

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
    
    
#------------------------------------------------------------
# Information 
#-------------
        
# This function creates the introduction table on the first
# page showing things like Site ID, Principle Investigator, 
# date range etc..

#------------------------------------------------------------      
       
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________    
    
# %% -----------------------------------------------------------------------------------------------
# Create instrument table
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
    
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
    report.ln() 
    #---------------------------------
    # add rows using loop
    report.set_font('Helvetica',style='')
    for row_n in range(len(atts_instrument)):
    
        inst = remove_characters(str(atts_instrument[row_n]))
        sn = remove_characters(str(atts_instrument_serial_number[row_n]))
        nd = remove_characters(str(atts_instrument_nominal_depth[row_n]))
        nd = str(int(float(nd)))
        
        report.cell(60,8,inst,1,0,'C');     
        report.cell(35,8,sn,1,0,'C');         
        report.cell(40,8,nd,1,0,'C'); 
        report.ln() 

#------------------------------------------------------------
# Information 
#-------------
        
# This function creates the inctrument table including serial
# numbers and nominal depths.

#------------------------------------------------------------ 

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
        
# %% -----------------------------------------------------------------------------------------------
# Create parameters table  
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________        
        
def parameter_table(report):
    
    param_list = param_avail(atts_var_names)
    
    form.sub_header('Available Parameters')
    report.set_font_size(12)    
    form.add_space()  
    #---------------------------------    
    #---------------------------------
    # Header
    report.set_font('Helvetica',style='B')
    report.cell(30,6,'Parameter',1,0,'C');  
    for n_inst in range(len(atts_instrument)):
        report.cell(15,6,'# ' + str(n_inst+1),1,0,'C');     
    report.ln()     
    #---------------------------------
    # add rows using loop
    report.set_font('Helvetica',style='')
    #---------------------------------
    # TEMP   
    report.cell(30,6,'TEMP',1,0,'C');    
    for n_inst in range(len(atts_instrument)): 
        if param_list.TEMP[n_inst] == 1:
            report.cell(15,6,'X',1,0,'C');   
        else:
            report.cell(15,6,' ',1,0,'C'); 
    report.ln()            
    #---------------------------------
    # PSAL   
    report.cell(30,6,'PSAL',1,0,'C');    
    for n_inst in range(len(atts_instrument)): 
        if param_list.PSAL[n_inst] == 1:
            report.cell(15,6,'X',1,0,'C');   
        else:
            report.cell(15,6,' ',1,0,'C');              
    report.ln() 
    #---------------------------------
    # VCUR   
    report.cell(30,6,'VCUR',1,0,'C');    
    for n_inst in range(len(atts_instrument)): 
        if param_list.VCUR[n_inst] == 1:
            report.cell(15,6,'X',1,0,'C');   
        else:
            report.cell(15,6,' ',1,0,'C');              
    report.ln() 
    #---------------------------------
    # UCUR  
    report.cell(30,6,'UCUR',1,0,'C');    
    for n_inst in range(len(atts_instrument)): 
        if param_list.UCUR[n_inst] == 1:
            report.cell(15,6,'X',1,0,'C');   
        else:
            report.cell(15,6,' ',1,0,'C');              
    report.ln()     
    #---------------------------------
    # CPHL   
    report.cell(30,6,'CPHL',1,0,'C');    
    for n_inst in range(len(atts_instrument)): 
        if param_list.CPHL[n_inst] == 1:
            report.cell(15,6,'X',1,0,'C');   
        else:
            report.cell(15,6,' ',1,0,'C');              
    report.ln()  
    #---------------------------------
    # DOX  
    report.cell(30,6,'DOX',1,0,'C');    
    for n_inst in range(len(atts_instrument)): 
        if param_list.DOX[n_inst] == 1:
            report.cell(15,6,'X',1,0,'C');   
        else:
            report.cell(15,6,' ',1,0,'C');              
    report.ln()     
    #---------------------------------
    # TURB 
    report.cell(30,6,'TURB',1,0,'C');    
    for n_inst in range(len(atts_instrument)): 
        if param_list.TURB[n_inst] == 1:
            report.cell(15,6,'X',1,0,'C');   
        else:
            report.cell(15,6,' ',1,0,'C');              
    report.ln()   
    #---------------------------------
    # PRES 
    report.cell(30,6,'PRES',1,0,'C');    
    for n_inst in range(len(atts_instrument)): 
        if param_list.PRES[n_inst] == 1:
            report.cell(15,6,'X',1,0,'C');   
        else:
            report.cell(15,6,' ',1,0,'C');              
    report.ln()   
    #---------------------------------
    # DEPTH  
    report.cell(30,6,'DEPTH',1,0,'C');    
    for n_inst in range(len(atts_instrument)): 
        if param_list.DEPTH[n_inst] == 1:
            report.cell(15,6,'X',1,0,'C');   
        else:
            report.cell(15,6,' ',1,0,'C');              
    report.ln()   
    #---------------------------------
    # TIME  
    report.cell(30,6,'TIME',1,0,'C');    
    for n_inst in range(len(atts_instrument)): 
        if param_list.TIME[n_inst] == 1:
            report.cell(15,6,'X',1,0,'C');   
        else:
            report.cell(15,6,' ',1,0,'C');              
    report.ln()
    #---------------------------------
    # Add legend below table
    report.set_font_size(10)       
    form.add_space()     
    for n_inst in range(len(atts_instrument)): 
        inst = remove_characters(str(atts_instrument[n_inst]))
        sn = remove_characters(str(atts_instrument_serial_number[n_inst]))
        nd = remove_characters(str(atts_instrument_nominal_depth[n_inst]))
        nd = str(int(float(nd)))
        report.cell(50,4,'# ' + str(n_inst+1) + '  =  ' + inst + ' ' + sn + ' ' + nd + ' m',0,0,'L');    
        report.ln()
        
#------------------------------------------------------------
# Information 
#-------------
        
# This function creates the 'Available Parameters' table.
# Not all parameters are currently shown.

#------------------------------------------------------------         

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________    
    
# %% -----------------------------------------------------------------------------------------------
# Create instrument Time in / Time out table
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
        
def timeinout_table(report): 

    report.add_page()    
    form.sub_header('Instrument times in / out')
    report.set_font_size(12)    
    form.add_space()  
    form.add_space()
    form.add_space()
    #---------------------------------
    # Header
    report.set_font('Helvetica',style='B')
    report.cell(80,8,"Instrument & nom. depth",1,0,'C');     
    report.cell(40,8,"Time in",1,0,'C');  
    report.cell(40,8,"Time out",1,0,'C');  
    report.ln()    
    #---------------------------------
    # add rows using loop
    report.set_font('Helvetica',style='')
    for row_n in range(len(atts_instrument)):
    
        inst = remove_characters(str(atts_instrument[row_n]))
        nd = remove_characters(str(atts_instrument_nominal_depth[row_n]))
        nd = str(int(float(nd)))
        ti = remove_characters(str(atts_in_water[row_n]))
        to = remove_characters(str(atts_out_water[row_n]))
        
        report.cell(80,8,inst + '  ' + nd + ' m',1,0,'L');    
        report.cell(40,8,ti,1,0,'C');         
        report.cell(40,8,to,1,0,'C'); 
        report.ln()     
        
#------------------------------------------------------------
# Information 
#-------------
        
# This function creates the 'Instrument times in / out table.

#------------------------------------------------------------         

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________   
     
# %% -----------------------------------------------------------------------------------------------
# Create instrument file table and details bullet list
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
        
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
    for row_n in range(len(atts_instrument)): 
        
        inst = remove_characters(str(atts_instrument[row_n]))
        nd = remove_characters(str(atts_instrument_nominal_depth[row_n]))
        nd = str(int(float(nd)))       
        file = remove_characters(str(atts_toolbox_input_file_name[row_n]))

        report.set_font('Helvetica',style='B')
        report.cell(80,18,inst + '  ' + nd + ' m',1,0,'L');
        report.set_font('Helvetica',style='')
        report.multi_cell(100,6,'Raw:' + file + '   ' + 'Processed:' + 'thredds_link_here',1,0,'C');            
        
def instrument_bullets(report):
    
    form.add_space()     
    form.add_space() 
    report.set_font_size(12)         
    form.bullet_point('Toolbox version: ' + tb_vers)
    
    
#------------------------------------------------------------
# Information 
#-------------
        
# This function creates the File location table.

#------------------------------------------------------------ 

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________    
    
    
    
    
    
    
    
    
    




    
    






    
    
    
    