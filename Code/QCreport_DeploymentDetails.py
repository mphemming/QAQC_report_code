# -*- coding: utf-8 -*-

# Created on Fri Jun  5 10:03:39 2020
# Contributers (code):  Michael Hemming (NSW-IMOS), Neil Malan (NSW-IMOS)
# Contributers (review): Moninya Roughan (NSW-IMS), Tim Austin (NSW-IMOS), Stuart Milburn (NSW-IMOS) 
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
import QCreport_setup as setup


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
    param_list_WCUR = []
    param_list_CSPD = []
    param_list_CDIR = []
    param_list_ECUR = []
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
        # WCUR available?
        if vn_file.find('WCUR') > -1 :
            n = 1
            param_list_WCUR.append(n)
        else:
            n = 0
            param_list_WCUR.append(n)             
        # CSPD available?
        if vn_file.find('CSPD') > -1 :
            n = 1
            param_list_CSPD.append(n)
        else:
            n = 0
            param_list_CSPD.append(n)
        # CDIR available?
        if vn_file.find('CDIR') > -1 :
            n = 1
            param_list_CDIR.append(n)
        else:
            n = 0
            param_list_CDIR.append(n) 
        # ECUR available?
        if vn_file.find('ECUR') > -1 :
            n = 1
            param_list_ECUR.append(n)
        else:
            n = 0
            param_list_ECUR.append(n)             
             
            
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
        WCUR = param_list_WCUR  
        CSPD = param_list_CSPD  
        CDIR = param_list_CDIR
        ECUR = param_list_ECUR          
        
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
lat = str(np.absolute(atts_geospatial_lat_min[0])) # assuming min/max is the same, and same for each file
lon = remove_characters(lon[0:6])
lat = remove_characters(lat[0:6])
# Toolbox version
tb_vers = remove_characters(str(get_unique(atts_toolbox_version)))
# local time zone
try:
    ltz = remove_characters(str(round(int(get_unique(rm_nodata(atts_local_time_zone))))))
except:
    ltz = 'not specified'
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


def intro_table(doc):

    with doc.create(form.Tabular('|l|l|')) as table:
        table.add_hline()
        table.add_row(('Site', setup.site_name))
        table.add_hline()
        table.add_row(('Deployment',setup.deployment))
        table.add_hline()
        table.add_row(('Start Date',start_date))
        table.add_hline()
        table.add_row(('End Date',end_date))
        table.add_hline()
        table.add_row(('Longitude',lon + form.degree_symbol + ' E'))
        table.add_hline()
        table.add_row(('Latitude',lat + form.degree_symbol + ' S'))
        table.add_hline()
        table.add_row(('Principle Investigator', PO))
        table.add_hline()
        table.add_row(('Field Team', FT))
        table.add_hline()
    
#------------------------------------------------------------
# Information 
#-------------
        
# This function creates the introduction table on the first
# page showing things like Site name, Principle Investigator, 
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
    
def instrument_table(doc):
    
    with doc.create(form.Subsection('Instrument Serial Numbers and Nominal Depths')):
        doc.append('') 
    
    with doc.create(form.Tabular('|l|l|l|')) as table:
        table.add_hline()
        table.add_row(('Instrument','Serial Number','Nominal Depth'))
        table.add_hline()
        # add rows using loop
        for row_n in range(len(atts_instrument)):
        
            inst = remove_characters(str(atts_instrument[row_n]))
            sn = remove_characters(str(atts_instrument_serial_number[row_n]))
            nd = remove_characters(str(atts_instrument_nominal_depth[row_n]))
            if '.0' in nd:
                nd = str(int(float(nd)))
            
            table.add_row((inst,sn,nd + ' m'))
            table.add_hline()

#------------------------------------------------------------
# Information 
#-------------
        
# This function creates the instrument table including serial
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
        
def parameter_table(doc): 
    
    param_list = param_avail(atts_var_names)
    
    with doc.create(form.Subsection('Derived Parameters')):
        doc.append('') 
    # determine number of rows required
    n_depths = len(atts_instrument)    
    tab_str = 'l|'
    input_str = '|' + tab_str*(n_depths+1)
    #---------------------------------    
    #---------------------------------
    # Table   
    with doc.create(form.Tabular(input_str)) as table:
        table.add_hline() 
        #---------------------------------
        # Header
        header = ['Parameter']
        for n_inst in range(len(atts_instrument)): 
            nd = remove_characters(str(atts_instrument_nominal_depth[n_inst]))
            if '.0' in nd:
                nd = str(int(float(nd))) 
            header.append(nd + ' m')
        table.add_row((header))
        table.add_hline()             
        # #---------------------------------
        # # add rows using loop                
        # #---------------------------------
        # # TEMP 
        row_xs = ['TEMP [' + form.degree_symbol + 'C]']
        for n_inst in range(len(atts_instrument)): 
            if param_list.TEMP[n_inst] == 1:
                row_xs.append('x')
            else:
                row_xs.append(' ')                   
        table.add_row((row_xs))
        table.add_hline() 
        # # PSAL 
        row_xs = ['PSAL']
        for n_inst in range(len(atts_instrument)): 
            if param_list.PSAL[n_inst] == 1:
                row_xs.append('x')
            else:
                row_xs.append(' ')                   
        table.add_row((row_xs))
        table.add_hline()         
        # # VCUR 
        row_xs = ['VCUR [' + form.vel_units + ']']
        for n_inst in range(len(atts_instrument)): 
            if param_list.VCUR[n_inst] == 1:
                row_xs.append('x')
            else:
                row_xs.append(' ')                   
        table.add_row((row_xs))
        table.add_hline() 
        # # UCUR 
        row_xs = ['UCUR [' + form.vel_units + ']']
        for n_inst in range(len(atts_instrument)): 
            if param_list.UCUR[n_inst] == 1:
                row_xs.append('x')
            else:
                row_xs.append(' ')                   
        table.add_row((row_xs))
        table.add_hline() 
        # # WCUR 
        row_xs = ['WCUR [' + form.vel_units + ']']
        for n_inst in range(len(atts_instrument)): 
            if param_list.WCUR[n_inst] == 1:
                row_xs.append('x')
            else:
                row_xs.append(' ')                   
        table.add_row((row_xs))
        table.add_hline() 
        # # CSPD 
        row_xs = ['CSPD [' + form.vel_units + ']']
        for n_inst in range(len(atts_instrument)): 
            if param_list.CSPD[n_inst] == 1:
                row_xs.append('x')
            else:
                row_xs.append(' ')                   
        table.add_row((row_xs))
        table.add_hline() 
        # # CDIR
        row_xs = ['CDIR[' + form.degree_symbol + ']']
        for n_inst in range(len(atts_instrument)): 
            if param_list.CDIR[n_inst] == 1:
                row_xs.append('x')
            else:
                row_xs.append(' ')                   
        table.add_row((row_xs))
        table.add_hline()         
        # # ECUR 
        row_xs = ['ECUR [' + form.vel_units + ']']
        for n_inst in range(len(atts_instrument)): 
            if param_list.ECUR[n_inst] == 1:
                row_xs.append('x')
            else:
                row_xs.append(' ')                   
        table.add_row((row_xs))
        table.add_hline() 
        # # CPHL 
        row_xs = ['CPHL [' + form.chl_units + ']']
        for n_inst in range(len(atts_instrument)): 
            if param_list.CPHL[n_inst] == 1:
                row_xs.append('x')
            else:
                row_xs.append(' ')                   
        table.add_row((row_xs))
        table.add_hline() 
        # # DOX 
        row_xs = ['DOX [' + form.O2_units + ']']
        for n_inst in range(len(atts_instrument)): 
            if param_list.DOX[n_inst] == 1:
                row_xs.append('x')
            else:
                row_xs.append(' ')                   
        table.add_row((row_xs))
        table.add_hline() 
        # # TURB 
        row_xs = ['TURB [NTU]']
        for n_inst in range(len(atts_instrument)): 
            if param_list.TURB[n_inst] == 1:
                row_xs.append('x')
            else:
                row_xs.append(' ')                   
        table.add_row((row_xs))
        table.add_hline() 
        # # PRES 
        row_xs = ['PRES [dbar]']
        for n_inst in range(len(atts_instrument)): 
            if param_list.PRES[n_inst] == 1:
                row_xs.append('x')
            else:
                row_xs.append(' ')                   
        table.add_row((row_xs))
        table.add_hline() 
        # # DEPTH 
        row_xs = ['DEPTH [m]']
        for n_inst in range(len(atts_instrument)): 
            if param_list.DEPTH[n_inst] == 1:
                row_xs.append('x')
            else:
                row_xs.append(' ')                   
        table.add_row((row_xs))
        table.add_hline() 
        # # TIME 
        row_xs = ['TIME']
        for n_inst in range(len(atts_instrument)): 
            if param_list.TIME[n_inst] == 1:
                row_xs.append('x')
            else:
                row_xs.append(' ')                   
        table.add_row((row_xs))
        table.add_hline()      
        
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
        
def timeinout_table(doc): 
    
    with doc.create(form.Subsection('Instrument times in / out')):
        doc.append('')     
    #---------------------------------
    # add table        
    with doc.create(form.Tabular('|l|l|l|')) as table:
        table.add_hline()     
        table.add_row('Instrument & nom. depth','Time in (UTC)','Time out (UTC)')
        table.add_hline()    
    #---------------------------------
    # add rows using loop
    for row_n in range(len(atts_instrument)): 
        inst = remove_characters(str(atts_instrument[row_n]))
        nd = remove_characters(str(atts_instrument_nominal_depth[row_n]))
        if '.0' in nd:
            nd = str(int(float(nd)))
        ti = remove_characters(str(atts_in_water[row_n]))
        to = remove_characters(str(atts_out_water[row_n]))  
        table.add_row(inst,ti,to)
        table.add_hline()         
        
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
    
def toolbox_bullet(doc):
    
    with doc.create(form.Subsection('Toolbox Version')):
        doc.append('Toolbox version: ' + tb_vers) 


def file_tables(doc):

    #---------------------------------
    # Raw file names
    #---------------------------------
    with doc.create(form.Subsection('Raw File Names')):
        doc.append('') 
    #---------------------------------
    # add table        
    with doc.create(form.Tabular('|l|l|')) as table:
        table.add_hline()     
        table.add_row('Instrument & nom. depth','Filename')
        table.add_hline()            
   #---------------------------------
   # add rows using loop      
    for row_n in range(len(atts_instrument)):     
        # get information for table
        inst = remove_characters(str(atts_instrument[row_n]))
        nd = remove_characters(str(atts_instrument_nominal_depth[row_n]))
        if '.0' in nd:
            nd = str(int(float(nd)))      
        file = remove_characters(str(atts_toolbox_input_file_name[row_n]))        
        table.add_row(inst + '  ' + nd + ' m',file)
        table.add_hline()          
    #---------------------------------
    # Thredds file names
    #---------------------------------       
    with doc.create(form.Subsection('Processed File Names')):
        doc.append('') 
    doc.append(form.Command('fontsize', arguments = ['8', '12']))
    doc.append(form.Command('selectfont'))
    #---------------------------------
    # add table        
    with doc.create(form.Tabular('|l|p{13cm}|')) as table:
        table.add_hline()     
        table.add_row('Instrument & nom. depth','Filename')
        table.add_hline() 
    #---------------------------------
    # add rows using loop      
    for row_n in range(len(atts_instrument)):     
        # get information for table
        inst = remove_characters(str(atts_instrument[row_n]))
        nd = remove_characters(str(atts_instrument_nominal_depth[row_n]))
        if '.0' in nd:
            nd = str(int(float(nd)))          
        OPenDAP = nc.OPeNDAP_links[row_n]
        # Need to split up string so that it fits into column
        OPenDAP = (OPenDAP[0:73] + ' ' + OPenDAP[41:107] + ' ' + OPenDAP[107::])
        table.add_row(inst + '  ' + nd + ' m',OPenDAP)
        table.add_hline()
    doc.append(form.Command('fontsize', arguments = ['15', '12']))
    doc.append(form.Command('selectfont'))     
    
#------------------------------------------------------------
# Information 
#-------------
  
# This function creates the File location table.

#------------------------------------------------------------ 

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________    
    
    
    
    
    
    
    
    
    




    
    






    
    
    
    