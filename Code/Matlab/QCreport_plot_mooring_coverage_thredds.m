node = 'NSW';
saving = 1;

plot_coverage(node, saving)

function plot_coverage(node, saving)
%
% Originally written by Moninya Roughan
% Updates by Brad Morris, Amandine Schaeffer, Michael Hemming
% New version incorporating previous contributions written by Michael
% Hemming on 03/03/2020, NSW-IMOS, Sydney, m.hemming@unsw.edu.au
% Last updated 11/11/2020 by MPH
%
% plot_mooring_coverage_thredds.m
%
% Input:
% ~~~~~~
% 
% node    | Which IMOS node you would like to plot. 
%             Examples: 'NSW', 'QLD', 'SA', 'WA', 'NRS'
% saving   | 1/0 = yes/no to saving the plot locally
%
% NOTE: This plot shows deployment time period using the start and end time included in the file name.
% It does not take into account any QC. Hence, there are no gaps where QC is bad. 
%

%% Add general path

addpath(genpath('C:\Users\mphem\OneDrive - UNSW\Work\Plot_series_functions'))

%% Extract web files from website

%лллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллл
% get list of sites
api = 'http://thredds.aodn.org.au/thredds/catalog/IMOS/ANMN/';
url = [api, node,'/','catalog.html'];
sites_html = webread(url);
k_start = strfind(sites_html,'href=');
k_start([1:2,end-3:end]) = [];
k_end = strfind(sites_html,'/catalog.html''><tt>');
for n_site = 1:numel(k_end)
    thredds(n_site).sites = sites_html(k_start(n_site)+6:k_end(n_site)-1);
end

%лллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллл
% get list of files for TEMP, PSAL, VEL, CHL, O2, CTD profiles at each site (if available)
clear k_start k_end
% find out what data types are available at each site
for n_site = 1:numel(thredds)
    % find out what variables are available    
    url = [api, node,'/', thredds(n_site).sites,'/','catalog.html'];
    vars_list = webread(url);
    k_start = strfind(vars_list,'href=');
    k_start([1:2,end-3:end]) = [];
    k_end = strfind(vars_list,'/catalog.html''><tt>');
    for n_var = 1:numel(k_end)
        thredds(n_site).folders(n_var).names = vars_list(k_start(n_var)+6:k_end(n_var)-1);    
    end
end
    
%лллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллллл
for n_site = 1:numel(thredds)
    folders = [thredds(n_site).folders(:)];
    clear find*
    for n_folder = 1:numel(folders)
        find_TEMP(n_folder) = ~isempty(strfind(folders(n_folder).names,'Temperature'));
        find_CTDT(n_folder) = ~isempty(strfind(folders(n_folder).names,'CTD_timeseries'));
        find_VEL(n_folder) = ~isempty(strfind(folders(n_folder).names,'Velocity'));
        find_BGC(n_folder) = ~isempty(strfind(folders(n_folder).names,'Biogeochem_timeseries'));
        find_BGC_profs(n_folder) = ~isempty(strfind(folders(n_folder).names,'Biogeochem_profiles'));
    end
    
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
% TEMP  
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     
 if sum(find_TEMP) == 1
    var = 'Temperature/';
    url = [api, node,'/', thredds(n_site).sites,'/',var,'catalog.html'];
    var_html = webread(url);
    k_start = strfind(var_html,'dataset');
    k_end = strfind(var_html,'.nc');
    k_end(2:2:end) = [];
    for n_files = 1:numel(k_end)
        thredds(n_site).TEMP(n_files).names = var_html(k_start(n_files+1)+41:k_end(n_files)+2);
        thredds(n_site).TEMP(n_files).vars_included = NaN;   
        thredds(n_site).TEMP(n_files).TEMP_index = NaN;  
        thredds(n_site).TEMP(n_files).PSAL_index = NaN;  
        thredds(n_site).TEMP(n_files).DOX_index = NaN;
        thredds(n_site).TEMP(n_files).CHL_index = NaN;  
    end
 else
     thredds(n_site).TEMP(1).names = NaN;  
     thredds(n_site).TEMP(1).vars_included = NaN;   
     thredds(n_site).TEMP(1).TEMP_index = NaN;  
     thredds(n_site).TEMP(1).PSAL_index = NaN;  
     thredds(n_site).TEMP(1).DOX_index = NaN;
     thredds(n_site).TEMP(1).CHL_index = NaN;  
 end
 

%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
% CTD timeseries
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     
if sum(find_CTDT) == 1
    var = 'CTD_timeseries/';
    url = [api, node,'/', thredds(n_site).sites,'/',var,'catalog.html'];
    var_html = webread(url);
    k_start = strfind(var_html,'dataset');
    k_end = strfind(var_html,'.nc');
    k_end(2:2:end) = [];
    for n_files = 1:numel(k_end)
        thredds(n_site).CTD_timeseries(n_files).names = var_html(k_start(n_files+1)+41:k_end(n_files)+2);
        underscores = strfind(thredds(n_site).CTD_timeseries(n_files).names,'_');
        thredds(n_site).CTD_timeseries(n_files).vars_included = thredds(n_site).CTD_timeseries(n_files).names(underscores(2)+1:underscores(3)-1);
        % Temperature
        if ~isempty(strfind(thredds(n_site).CTD_timeseries(n_files).vars_included,'T'))
            thredds(n_site).CTD_timeseries(n_files).TEMP_index = 1;
        else
            thredds(n_site).CTD_timeseries(n_files).TEMP_index = 0;
        end     
        % Salinity
        if ~isempty(strfind(thredds(n_site).CTD_timeseries(n_files).vars_included,'S'))
            thredds(n_site).CTD_timeseries(n_files).PSAL_index = 1;
        else
            thredds(n_site).CTD_timeseries(n_files).PSAL_index = 0;
        end       
        % Oxygen
        if ~isempty(strfind(thredds(n_site).CTD_timeseries(n_files).vars_included,'O'))
            thredds(n_site).CTD_timeseries(n_files).DOX_index = 1;
        else
            thredds(n_site).CTD_timeseries(n_files).DOX_index = 0;
        end   
        % Fluorescence
        if ~isempty(strfind(thredds(n_site).CTD_timeseries(n_files).vars_included,'B'))
            thredds(n_site).CTD_timeseries(n_files).CHL_index = 1;
        else
            thredds(n_site).CTD_timeseries(n_files).CHL_index = 0;
        end           
    end
else
    thredds(n_site).CTD_timeseries(1).names = NaN;  
     thredds(n_site).CTD_timeseries(1).vars_included = NaN;   
     thredds(n_site).CTD_timeseries(1).TEMP_index = NaN;  
     thredds(n_site).CTD_timeseries(1).PSAL_index = NaN;  
     thredds(n_site).CTD_timeseries(1).DOX_index = NaN;
     thredds(n_site).CTD_timeseries(1).CHL_index = NaN;      
end      
    
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
% VEL 
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     
 if sum(find_VEL == 1)
        var = 'Velocity/';
        url = [api, node,'/', thredds(n_site).sites,'/',var,'catalog.html'];
        var_html = webread(url);
        k_start = strfind(var_html,'dataset');
        k_end = strfind(var_html,'.nc');
        k_end(2:2:end) = [];
        for n_files = 1:numel(k_end)
            thredds(n_site).VEL(n_files).names = var_html(k_start(n_files+1)+38:k_end(n_files)+2);
        end
 else
     thredds(n_site).VEL(1).names = NaN;  
 end   
    
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
% BGC - determining included variables    
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    % determine what variables are included in BGC timeseries (if available)
    % create index for PSAL, Chl, O2, 
    if sum(find_BGC == 1)
        var = 'Biogeochem_timeseries/';
        url = [api, node,'/', thredds(n_site).sites,'/',var,'catalog.html'];
        var_html = webread(url);
        k_start = strfind(var_html,'dataset');
        k_end = strfind(var_html,'.nc');
        k_end(2:2:end) = [];
        for n_files = 1:numel(k_end)
            thredds(n_site).BGC(n_files).names = var_html(k_start(n_files+1)+50:k_end(n_files)+2);
        end
        
        for n_files = 1:numel(thredds(n_site).BGC)
            underscores = strfind(thredds(n_site).BGC(n_files).names,'_');
            thredds(n_site).BGC(n_files).vars_included = thredds(n_site).BGC(n_files).names(underscores(2)+1:underscores(3)-1);
            % Temperature
            if ~isempty(strfind(thredds(n_site).BGC(n_files).vars_included,'T'))
                thredds(n_site).BGC(n_files).TEMP_index = 1;
            else
                thredds(n_site).BGC(n_files).TEMP_index = 0;
            end         
            % Salinity
            if ~isempty(strfind(thredds(n_site).BGC(n_files).vars_included,'S'))
                thredds(n_site).BGC(n_files).PSAL_index = 1;
            else
                thredds(n_site).BGC(n_files).PSAL_index = 0;
            end             
            % Oxygen Concentration
            if ~isempty(strfind(thredds(n_site).BGC(n_files).vars_included,'O'))
                
                thredds(n_site).BGC(n_files).DOX_index = 1;
            else
                thredds(n_site).BGC(n_files).DOX_index = 0;
            end
            % Fluorescence
            if ~isempty(strfind(thredds(n_site).BGC(n_files).vars_included,'B'))
                thredds(n_site).BGC(n_files).CHL_index = 1;
            else
                thredds(n_site).BGC(n_files).CHL_index = 0;
            end                        
        end
    else
     thredds(n_site).BGC(1).names = NaN; 
     thredds(n_site).BGC(1).vars_included = NaN;   
     thredds(n_site).BGC(1).TEMP_index = NaN;  
     thredds(n_site).BGC(1).PSAL_index = NaN;  
     thredds(n_site).BGC(1).DOX_index = NaN;
     thredds(n_site).BGC(1).CHL_index = NaN;  
    end
    
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
% CTD profiles 
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     
 if sum(find_BGC_profs == 1)
        var = 'Biogeochem_profiles/';
        url = [api, node,'/', thredds(n_site).sites,'/',var,'catalog.html'];
        var_html = webread(url);
        k_start = strfind(var_html,'dataset');
        k_end = strfind(var_html,'.nc');
        k_end(2:2:end) = [];
        for n_files = 1:numel(k_end)
            thredds(n_site).BGC_profiles(n_files).names = var_html(k_start(n_files+1)+49:k_end(n_files)+2);
        end    
 else
     thredds(n_site).BGC_profiles(n_files).names = NaN;
 end
end
           
clearvars -except thredds node saving

%% extract site information
% process: for each file (per variable), determine location of underscore
% in file name, use this to get site info per file, then get unique site info per variable (not repeated strings),
% finally assign unique number per site (e.g. 'CH070' = 1, 'PH100' = 2).
% Unique site number is not the same for each variable, as not all sites
% have BGC for example, so the order is different (at this stage).  
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% TEMP
for n_site = 1:numel(thredds)
    T_1 = string(repmat(thredds(n_site).sites,[numel(thredds(n_site).TEMP) 1]));
    sites_struct(n_site).TEMP = vertcat(T_1);
    if sum(~isnan([thredds(n_site).CTD_timeseries.names])) ~= 0
        CTD_timeseries_files = nansum([thredds(n_site).CTD_timeseries.TEMP_index]);
        T_2 = string(repmat(thredds(n_site).sites,[CTD_timeseries_files 1]));
        sites_struct(n_site).TEMP = vertcat(sites_struct(n_site).TEMP,T_2); 
    end
    if sum(~isnan([thredds(n_site).BGC.names])) ~= 0
        BGC_files = nansum([thredds(n_site).BGC.TEMP_index]);
        T_3 = string(repmat(thredds(n_site).sites,[BGC_files 1]));
        sites_struct(n_site).TEMP = vertcat(sites_struct(n_site).TEMP,T_3);
    end    
end
unique_sites = unique(vertcat(sites_struct.TEMP));
unique_sites_number = 1:numel(unique_sites);
% assign unique_sites_number to each site string in loop
for n_site = 1:numel(thredds)
        string_match = strcmp([sites_struct(n_site).TEMP],unique_sites(n_site));
        sites_struct(n_site).TEMP_index(string_match) = unique_sites_number(n_site);  
        sites_struct(n_site).TEMP_index_string = repmat(unique_sites(n_site), size(sites_struct(n_site).TEMP_index));              
end
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% VEL
for n_site = 1:numel(thredds)
    sites_struct(n_site).VEL = string(repmat(thredds(n_site).sites,[numel(thredds(n_site).VEL) 1]));
end
unique_sites = unique(vertcat(sites_struct.VEL));
unique_sites_number = 1:numel(unique_sites);
% assign unique_sites_number to each site string in loop
for n_site = 1:numel(thredds)
    string_match = strcmp([sites_struct(n_site).VEL],unique_sites(n_site));
    sites_struct(n_site).VEL_index(string_match) = unique_sites_number(n_site); 
    sites_struct(n_site).VEL_index_string = repmat(unique_sites(n_site), size(sites_struct(n_site).VEL_index));      
end
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% PSAL
for n_site = 1:numel(thredds)
    if isfield(thredds(n_site).BGC,'PSAL_index')
        total_PSAL_1 = sum([thredds(n_site).BGC.PSAL_index] == 1);
    end
    sites_struct(n_site).PSAL(1:total_PSAL_1) = string(thredds(n_site).sites);
    if isfield(thredds(n_site).CTD_timeseries,'PSAL_index')
        total_PSAL_2 = sum([thredds(n_site).CTD_timeseries.PSAL_index] == 1);
    end
     sites_struct(n_site).PSAL(total_PSAL_1+1:total_PSAL_1+total_PSAL_2) = string(thredds(n_site).sites);   
     if isempty(sites_struct(n_site).PSAL)
         sites_struct(n_site).PSAL = string(thredds(n_site).sites);
     end  
end

unique_sites = unique(vertcat(sites_struct.VEL)); % use velocity as should be same for BGC, get complicated with BGC
unique_sites_number = 1:numel(unique_sites);
% assign unique_sites_number to each site string in loop
for n_site = 1:numel(thredds)
    if numel([sites_struct(n_site).PSAL]) > 1
        string_match = find(strcmp([sites_struct(n_site).PSAL],unique_sites(n_site)));
        string_missing = find(strcmp([sites_struct(n_site).PSAL],unique_sites(n_site)) == 0); 
        sites_struct(n_site).PSAL_index(string_match) = unique_sites_number(n_site);  
        sites_struct(n_site).PSAL_index(string_missing) = NaN;
        sites_struct(n_site).PSAL_index_string = repmat(unique_sites(n_site), size(sites_struct(n_site).PSAL_index));  
%         if numel(sites_struct(n_site).PSAL_index) ~= numel(thredds(n_site).BGC)
%             if numel(thredds(n_site).CTD_timeseries) > 1
%                 if numel(sites_struct(n_site).PSAL_index) ~= (numel(thredds(n_site).BGC) + numel(thredds(n_site).CTD_timeseries))
%                     sites_struct(n_site).PSAL_index = ones(size(thredds(n_site).BGC))*unique(sites_struct(n_site).PSAL_index);
%                     sites_struct(n_site).PSAL_index_string = repmat(sites_struct(n_site).PSAL_index_string,size(thredds(n_site).BGC));
%                 end
%             end
%         end
    else
        sites_struct(n_site).PSAL_index =  unique_sites_number(n_site);
        sites_struct(n_site).PSAL_index_string = unique_sites(n_site);
    end
end
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% Oxygen
for n_site = 1:numel(thredds)
    if isfield(thredds(n_site).BGC,'DOX_index')
        total_DOX_1 = sum([thredds(n_site).BGC.DOX_index] == 1);
    end
    sites_struct(n_site).DOX(1:total_DOX_1) = string(thredds(n_site).sites);
    if isfield(thredds(n_site).CTD_timeseries,'DOX_index')
        total_DOX_2 = sum([thredds(n_site).CTD_timeseries.DOX_index] == 1);
    end
     sites_struct(n_site).DOX(total_DOX_1+1:total_DOX_1+total_DOX_2) = string(thredds(n_site).sites);   
     if isempty(sites_struct(n_site).DOX)
         sites_struct(n_site).DOX = string(thredds(n_site).sites);
     end     
end

unique_sites = unique(vertcat(sites_struct.VEL)); % use velocity as should be same for BGC, get complicated with BGC
unique_sites_number = 1:numel(unique_sites);
% assign unique_sites_number to each site string in loop
for n_site = 1:numel(thredds)
    if numel([sites_struct(n_site).DOX]) > 1
        string_match = find(strcmp([sites_struct(n_site).DOX],unique_sites(n_site)));
        string_missing = find(strcmp([sites_struct(n_site).DOX],unique_sites(n_site)) == 0); 
        sites_struct(n_site).DOX_index(string_match) = unique_sites_number(n_site);  
        sites_struct(n_site).DOX_index(string_missing) = NaN;
        sites_struct(n_site).DOX_index_string = repmat(unique_sites(n_site), size(sites_struct(n_site).DOX_index));  
        if numel(sites_struct(n_site).DOX_index) ~= numel(thredds(n_site).BGC)
            if numel(thredds(n_site).CTD_timeseries) > 1
                if numel(sites_struct(n_site).DOX_index) ~= (numel(thredds(n_site).BGC) + numel(thredds(n_site).CTD_timeseries))
                    sites_struct(n_site).DOX_index = ones(1,sum([thredds(n_site).BGC.DOX_index]) + ...
                        sum([thredds(n_site).CTD_timeseries.DOX_index])) * unique(sites_struct(n_site).DOX_index);
                    sites_struct(n_site).DOX_index_string = repmat(unique_sites(n_site), size(sites_struct(n_site).DOX_index));
                end
            end
        end
    else
        sites_struct(n_site).DOX_index = unique_sites_number(n_site);
        sites_struct(n_site).DOX_index_string = unique_sites(n_site);
    end
end

%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% Chl

for n_site = 1:numel(thredds)
    if isfield(thredds(n_site).BGC,'CHL_index')
        total_CHL_1 = sum([thredds(n_site).BGC.CHL_index] == 1);
    end
    sites_struct(n_site).CHL(1:total_CHL_1) = string(thredds(n_site).sites);
    if isfield(thredds(n_site).CTD_timeseries,'CHL_index')
        total_CHL_2 = sum([thredds(n_site).CTD_timeseries.CHL_index] == 1);
    end
     sites_struct(n_site).CHL(total_CHL_1+1:total_CHL_1+total_CHL_2) = string(thredds(n_site).sites);   
     if isempty(sites_struct(n_site).CHL)
         sites_struct(n_site).CHL = string(thredds(n_site).sites);
     end     
end

unique_sites = unique(vertcat(sites_struct.VEL)); % use velocity as should be same for BGC, get complicated with BGC
unique_sites_number = 1:numel(unique_sites);
% assign unique_sites_number to each site string in loop
for n_site = 1:numel(thredds)
    if numel([sites_struct(n_site).CHL]) > 1
        string_match = find(strcmp([sites_struct(n_site).CHL],unique_sites(n_site)));
        string_missing = find(strcmp([sites_struct(n_site).CHL],unique_sites(n_site)) == 0); 
        sites_struct(n_site).CHL_index(string_match) = unique_sites_number(n_site);  
        sites_struct(n_site).CHL_index(string_missing) = NaN;
        sites_struct(n_site).CHL_index_string = repmat(unique_sites(n_site), size(sites_struct(n_site).CHL_index));  
        if numel(sites_struct(n_site).CHL_index) ~= numel(thredds(n_site).BGC)
            if numel(thredds(n_site).CTD_timeseries) > 1
                if numel(sites_struct(n_site).CHL_index) ~= (numel(thredds(n_site).BGC) + numel(thredds(n_site).CTD_timeseries))
                    sites_struct(n_site).CHL_index = ones(1,sum([thredds(n_site).BGC.CHL_index]) + ...
                        sum([thredds(n_site).CTD_timeseries.CHL_index])) * unique(sites_struct(n_site).CHL_index);
                    sites_struct(n_site).CHL_index_string = repmat(unique_sites(n_site), size(sites_struct(n_site).CHL_index));
                end
            end
        end
    else
        sites_struct(n_site).CHL_index = unique_sites_number(n_site);
        sites_struct(n_site).CHL_index_string = unique_sites(n_site);
    end
end

%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% clear unnecessary variables
clearvars -except thredds node sites_struct saving

%% concatenate useful variables

%~~~~~~~~~~~~~~~~~~~~~~~~~   
% TEMP ~~~~~~~~~~~~~~~~~~~~
%~~~~~~~~~~~~~~~~~~~~~~~~~

for n_site = 1:numel(sites_struct)
    T_1 = thredds(n_site).TEMP;
    T_2 = thredds(n_site).CTD_timeseries;
    T_3 = thredds(n_site).BGC;
    % remove those files that don't include TEMP
    if sum(([thredds(n_site).CTD_timeseries.TEMP_index])) ~= numel(T_2)
        if numel(([thredds(n_site).CTD_timeseries.TEMP_index])) ~= numel(T_2)
            f_0 = find([thredds(n_site).CTD_timeseries.TEMP_index] == 0);
            T_2(f_0) = [];
        end
    end
    if sum(([thredds(n_site).BGC.TEMP_index])) ~= numel(T_3)
        if numel(([thredds(n_site).BGC.TEMP_index])) ~= numel(T_3)
            f_0 = find([thredds(n_site).BGC.TEMP_index] == 0);
            T_3(f_0) = [];
        end
    end    
    Files_TEMP(n_site).TEMP = [T_1,T_2,T_3];
    n = 0;
    clear nan_index
    for n_files = 1:numel(Files_TEMP(n_site).TEMP)
        if sum(isnan(Files_TEMP(n_site).TEMP(n_files).names)) == 1
            n = n+1;
            nan_index(n) = n_files;
        end
    end
    if exist('nan_index','var')
        nan_index(nan_index == 1) = [];
        Files_TEMP(n_site).TEMP(nan_index) = [];
    end
end
Files_TEMP = [Files_TEMP.TEMP];
Files_TEMP_site_index = horzcat(sites_struct.TEMP_index);
Files_TEMP_site_index_string = horzcat(sites_struct.TEMP_index_string);    

%~~~~~~~~~~~~~~~~~~~~~~~~~   
% VEL ~~~~~~~~~~~~~~~~~~~~
%~~~~~~~~~~~~~~~~~~~~~~~~~
Files_VEL = horzcat(thredds.VEL);
Files_VEL_site_index = horzcat(sites_struct.VEL_index);
Files_VEL_site_index_string = horzcat(sites_struct.VEL_index_string);
%~~~~~~~~~~~~~~~~~~~~~~~~~   
% PSAL ~~~~~~~~~~~~~~~~~~~~
%~~~~~~~~~~~~~~~~~~~~~~~~~
for n_site = 1:numel(sites_struct)
    S_1 = thredds(n_site).CTD_timeseries;
    S_2 = thredds(n_site).BGC;
    % remove those files that don't include TEMP
    if sum(([thredds(n_site).CTD_timeseries.PSAL_index])) ~= numel(S_1)
        if numel(([thredds(n_site).CTD_timeseries.PSAL_index])) ~= numel(S_1)
            f_0 = find([thredds(n_site).CTD_timeseries.PSAL_index] == 0);
            S_1(f_0) = [];
        end
    end
    if sum(([thredds(n_site).BGC.PSAL_index])) ~= numel(S_2)
        if numel(([thredds(n_site).BGC.PSAL_index])) ~= numel(S_2)
            f_0 = find([thredds(n_site).BGC.PSAL_index] == 0);
            S_2(f_0) = [];
        end
    end    
    Files_PSAL(n_site).PSAL = [S_1,S_2];
    n = 0;
    clear nan_index
    for n_files = 1:numel(Files_PSAL(n_site).PSAL)
        if sum(isnan(Files_PSAL(n_site).PSAL(n_files).names)) == 1
            n = n+1;
            nan_index(n) = n_files;
        end
    end
    if exist('nan_index','var')
        nan_index(nan_index == 1) = [];
        Files_PSAL(n_site).PSAL(nan_index) = [];
    end
end
Files_PSAL = [Files_PSAL.PSAL];
F1 = horzcat(sites_struct.PSAL_index);
F2 = horzcat(sites_struct.PSAL_index_string);   
% Remove NaNs and when file doesn't contain PSAL
PSAL_OK = vertcat(Files_PSAL.PSAL_index);
PSAL_OK = find(isfinite(PSAL_OK) & PSAL_OK == 1); 
Files_PSAL = Files_PSAL(PSAL_OK);
% only include those sites with data
% only keep those indices that repeat (= some data)
unNum   = unique(F1);
[n,bin] = histc(F1,unNum);
f_repeated = find(n > 1);
for n_loop = 1:numel(f_repeated)
    check = find(F1 == f_repeated(n_loop));
    Files_PSAL_site_index(check) = f_repeated(n_loop);
    Files_PSAL_site_index_string(check) = F2(check);
end
Files_PSAL_site_index(Files_PSAL_site_index == 0) = [];
Files_PSAL_site_index_string(ismissing(Files_PSAL_site_index_string)) = [];

%~~~~~~~~~~~~~~~~~~~~~~~~~   
% DOX ~~~~~~~~~~~~~~~~~~~~
%~~~~~~~~~~~~~~~~~~~~~~~~~
for n_site = 1:numel(sites_struct)
    D_1 = thredds(n_site).CTD_timeseries;
    D_2 = thredds(n_site).BGC;
    % remove those files that don't include TEMP
    if sum(([thredds(n_site).CTD_timeseries.DOX_index])) ~= numel(D_1)
        if numel(([thredds(n_site).CTD_timeseries.DOX_index])) ~= numel(D_1)
            f_0 = find([thredds(n_site).CTD_timeseries.DOX_index] == 0);
            D_1(f_0) = [];
        end
    end
    if sum(([thredds(n_site).BGC.DOX_index])) ~= numel(D_2)
        if numel(([thredds(n_site).BGC.DOX_index])) ~= numel(D_1)
            f_0 = find([thredds(n_site).BGC.DOX_index] == 0);
            D_2(f_0) = [];
        end
    end    
    Files_DOX(n_site).DOX = [D_1,D_2];
    n = 0;
    clear nan_index
    for n_files = 1:numel(Files_DOX(n_site).DOX)
        if sum(isnan(Files_DOX(n_site).DOX(n_files).names)) == 1
            n = n+1;
            nan_index(n) = n_files;
        end
    end
    if exist('nan_index','var')
        nan_index(nan_index == 1) = [];
        Files_DOX(n_site).DOX(nan_index) = [];
    end
end
Files_DOX = [Files_DOX.DOX];
F1 = horzcat(sites_struct.DOX_index);
F2 = horzcat(sites_struct.DOX_index_string);   
% Remove NaNs and when file doesn't contain DOX
DOX_OK = vertcat(Files_DOX.DOX_index);
DOX_OK = find(isfinite(DOX_OK) & DOX_OK == 1); 
Files_DOX = Files_DOX(DOX_OK);
% only include those sites with data
% only keep those indices that repeat (= some data)
unNum   = unique(F1);
[n,bin] = histc(F1,unNum);
f_repeated = find(n > 1);
for n_loop = 1:numel(f_repeated)
    check = find(F1 == f_repeated(n_loop));
    Files_DOX_site_index(check) = f_repeated(n_loop);
    Files_DOX_site_index_string(check) = F2(check);
end
Files_DOX_site_index(Files_DOX_site_index == 0) = [];
Files_DOX_site_index_string(ismissing(Files_DOX_site_index_string)) = [];

%~~~~~~~~~~~~~~~~~~~~~~~~~   
% CHL ~~~~~~~~~~~~~~~~~~~~
%~~~~~~~~~~~~~~~~~~~~~~~~~
for n_site = 1:numel(sites_struct)
    C_1 = thredds(n_site).CTD_timeseries;
    C_2 = thredds(n_site).BGC;
    % remove those files that don't include TEMP
    if sum(([thredds(n_site).CTD_timeseries.CHL_index])) ~= numel(C_1)
        if numel(([thredds(n_site).CTD_timeseries.CHL_index])) ~= numel(C_1)
            f_0 = find([thredds(n_site).CTD_timeseries.CHL_index] == 0);
            C_1(f_0) = [];
        end
    end
    if sum(([thredds(n_site).BGC.CHL_index])) ~= numel(C_2)
        if numel(([thredds(n_site).BGC.CHL_index])) ~= numel(D_1)
            f_0 = find([thredds(n_site).BGC.CHL_index] == 0);
            C_2(f_0) = [];
        end
    end    
    Files_CHL(n_site).CHL = [C_1,C_2];
    n = 0;
    clear nan_index
    for n_files = 1:numel(Files_CHL(n_site).CHL)
        if sum(isnan(Files_CHL(n_site).CHL(n_files).names)) == 1
            n = n+1;
            nan_index(n) = n_files;
        end
    end
    if exist('nan_index','var')
        nan_index(nan_index == 1) = [];
        Files_CHL(n_site).CHL(nan_index) = [];
    end
end
Files_CHL = [Files_CHL.CHL];
F1 = horzcat(sites_struct.CHL_index);
F2 = horzcat(sites_struct.CHL_index_string);   
% Remove NaNs and when file doesn't contain CHL
CHL_OK = vertcat(Files_CHL.CHL_index);
CHL_OK = find(isfinite(CHL_OK) & CHL_OK == 1); 
Files_CHL = Files_CHL(CHL_OK);
% only include those sites with data
% only keep those indices that repeat (= some data)
unNum   = unique(F1);
[n,bin] = histc(F1,unNum);
f_repeated = find(n > 1);
for n_loop = 1:numel(f_repeated)
    check = find(F1 == f_repeated(n_loop));
    Files_CHL_site_index(check) = f_repeated(n_loop);
    Files_CHL_site_index_string(check) = F2(check);
end
Files_CHL_site_index(Files_CHL_site_index == 0) = [];
Files_CHL_site_index_string(ismissing(Files_CHL_site_index_string)) = [];

clearvars -except Files* thredds node sites_struct saving

%% extract time coverage
% just deployment time periods (no indication of data quality or vertical coverage)
% process: for each file (per variable), determine location of underscores
% in file name, extract start and end date, create MATLAB datenum for range
% between start and end date
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% TEMP
for n_files = 1:numel(Files_TEMP)
    if sum(~isnan(Files_TEMP(n_files).names)) == numel(Files_TEMP(n_files).names)
        underscores = strfind(Files_TEMP(n_files).names,'_');
        if ~isempty(underscores)
            Files_TEMP_start_time(n_files) = string(Files_TEMP(n_files).names(underscores(3)+1:underscores(4)-1));
            Files_TEMP_end_time(n_files) = string(Files_TEMP(n_files).names(underscores(7)+5:underscores(8)-1));
            char_st = char(Files_TEMP_start_time(n_files));
            char_et = char(Files_TEMP_end_time(n_files));
            coverage(n_files).TEMP = ...
                datenum(str2double(char_st(1:4)),str2double(char_st(5:6)),str2double(char_st(7:8))) : 1 : ...
                datenum(str2double(char_et(1:4)),str2double(char_et(5:6)),str2double(char_et(7:8)));
            coverage(n_files).TEMP_site = repmat(Files_TEMP_site_index(n_files),[1 numel(coverage(n_files).TEMP)]);
        	coverage(n_files).TEMP_site_string = repmat(Files_TEMP_site_index_string(n_files),[1 numel(coverage(n_files).TEMP)]);
        else
            coverage(n_files).TEMP = NaN;
            coverage(n_files).TEMP_site = NaN;
            coverage(n_files).TEMP_site_string = NaN;
        end
    end
end

TEMP_coverage = [coverage.TEMP];
TEMP_coverage_site = [coverage.TEMP_site];
TEMP_coverage_site_string = [coverage.TEMP_site_string];
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% VEL
for n_files = 1:numel(Files_VEL)
    if sum(~isnan(Files_VEL(n_files).names)) == numel(Files_VEL(n_files).names)
        underscores = strfind(Files_VEL(n_files).names,'_');
        Files_VEL_start_time(n_files) = string(Files_VEL(n_files).names(underscores(3)+1:underscores(4)-1));
        Files_VEL_end_time(n_files) = string(Files_VEL(n_files).names(underscores(7)+5:underscores(8)-1));
        char_st = char(Files_VEL_start_time(n_files));
        char_et = char(Files_VEL_end_time(n_files));
        coverage(n_files).VEL = ...
            datenum(str2double(char_st(1:4)),str2double(char_st(5:6)),str2double(char_st(7:8))) : 1 : ...
            datenum(str2double(char_et(1:4)),str2double(char_et(5:6)),str2double(char_et(7:8)));
        coverage(n_files).VEL_site = repmat(Files_VEL_site_index(n_files),[1 numel(coverage(n_files).VEL)]);
        coverage(n_files).VEL_site_string = repmat(Files_VEL_site_index_string(n_files),[1 numel(coverage(n_files).VEL)]);
    end
end
if isfield(coverage,'VEL')
VEL_coverage = [coverage.VEL];
VEL_coverage_site = [coverage.VEL_site];
VEL_coverage_site_string = [coverage.VEL_site_string];
end

%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% PSAL

for n_files = 1:numel(Files_PSAL)
    if sum(~isnan(Files_PSAL(n_files).names)) == numel(Files_PSAL(n_files).names)
        underscores = strfind(Files_PSAL(n_files).names,'_');
        if ~isempty(underscores)
            Files_PSAL_start_time(n_files) = string(Files_PSAL(n_files).names(underscores(3)+1:underscores(4)-1));
            Files_PSAL_end_time(n_files) = string(Files_PSAL(n_files).names(underscores(7)+5:underscores(8)-1));
            char_st = char(Files_PSAL_start_time(n_files));
            char_et = char(Files_PSAL_end_time(n_files));
            coverage(n_files).PSAL = ...
                datenum(str2double(char_st(1:4)),str2double(char_st(5:6)),str2double(char_st(7:8))) : 1 : ...
                datenum(str2double(char_et(1:4)),str2double(char_et(5:6)),str2double(char_et(7:8)));
            coverage(n_files).PSAL_site = repmat(Files_PSAL_site_index(n_files),[1 numel(coverage(n_files).PSAL)]);
        	coverage(n_files).PSAL_site_string = repmat(Files_PSAL_site_index_string(n_files),[1 numel(coverage(n_files).PSAL)]);
        else
            coverage(n_files).PSAL = NaN;
            coverage(n_files).PSAL_site = NaN;
            coverage(n_files).PSAL_site_string = NaN;
        end
    end
end
if isfield(coverage,'PSAL')
    PSAL_coverage = [coverage.PSAL];
    PSAL_coverage_site = [coverage.PSAL_site];
    PSAL_coverage_site_string = [coverage.PSAL_site_string];
end

%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% DOX
for n_files = 1:numel(Files_DOX)
    if sum(~isnan(Files_DOX(n_files).names)) == numel(Files_DOX(n_files).names)
        underscores = strfind(Files_DOX(n_files).names,'_');
        Files_DOX_start_time(n_files) = string(Files_DOX(n_files).names(underscores(3)+1:underscores(4)-1));
        Files_DOX_end_time(n_files) = string(Files_DOX(n_files).names(underscores(7)+5:underscores(8)-1));
        char_st = char(Files_DOX_start_time(n_files));
        char_et = char(Files_DOX_end_time(n_files));
        coverage(n_files).DOX = ...
            datenum(str2double(char_st(1:4)),str2double(char_st(5:6)),str2double(char_st(7:8))) : 1 : ...
            datenum(str2double(char_et(1:4)),str2double(char_et(5:6)),str2double(char_et(7:8)));
        coverage(n_files).DOX_site = repmat(Files_DOX_site_index(n_files),[1 numel(coverage(n_files).DOX)]);
        coverage(n_files).DOX_site_string = repmat(Files_DOX_site_index_string(n_files),[1 numel(coverage(n_files).DOX)]);
    end
end

if isfield(coverage,'DOX')
DOX_coverage = [coverage.DOX];
DOX_coverage_site = [coverage.DOX_site];
DOX_coverage_site_string = [coverage.DOX_site_string];
end
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% CHL
for n_files = 1:numel(Files_CHL)
    if sum(~isnan(Files_CHL(n_files).names)) == numel(Files_CHL(n_files).names)
        underscores = strfind(Files_CHL(n_files).names,'_');
        Files_CHL_start_time(n_files) = string(Files_CHL(n_files).names(underscores(3)+1:underscores(4)-1));
        Files_CHL_end_time(n_files) = string(Files_CHL(n_files).names(underscores(7)+5:underscores(8)-1));
        char_st = char(Files_CHL_start_time(n_files));
        char_et = char(Files_CHL_end_time(n_files));
        coverage(n_files).CHL = ...
            datenum(str2double(char_st(1:4)),str2double(char_st(5:6)),str2double(char_st(7:8))) : 1 : ...
            datenum(str2double(char_et(1:4)),str2double(char_et(5:6)),str2double(char_et(7:8)));
        coverage(n_files).CHL_site = repmat(Files_CHL_site_index(n_files),[1 numel(coverage(n_files).CHL)]);
        coverage(n_files).CHL_site_string = repmat(Files_CHL_site_index_string(n_files),[1 numel(coverage(n_files).CHL)]);
    end
end
if isfield(coverage,'CHL')
CHL_coverage = [coverage.CHL];
CHL_coverage_site = [coverage.CHL_site];
CHL_coverage_site_string = [coverage.CHL_site_string];
end
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% clear unnecessary variables
clearvars -except *coverage* coverage thredds sites_struct node saving
%% Some minor QC for time coverage
% for cases where the filename date is incorrect
% Too far in future (from now) 
% NOTE: might need to add some QC here if filename date is too far back 
% in the past.
TEMP_coverage(TEMP_coverage > now) = NaN;
if isfield(coverage,'VEL')
VEL_coverage(VEL_coverage > now) = NaN;
end
if isfield(coverage,'PSAL')
PSAL_coverage(PSAL_coverage > now) = NaN;
end
if isfield(coverage,'DOX')
DOX_coverage(DOX_coverage > now) = NaN;
end
if isfield(coverage,'CHL')
CHL_coverage(CHL_coverage > now) = NaN;
end
%% Assign new individual site numbers
% as order of site is not the same for each variable (as mentioned above)
% process: get unique site numbers considering all variables, define site
% number variables, for each unique site (all variables) use strcmp to find
% indices where same site string is present, replace previous numbers with
% unique site number. Now consistent site numbers for TEMP, VEL, BGC.

if isfield(coverage,'PSAL') & isfield(coverage,'DOX') & isfield(coverage,'CHL') & isfield(coverage,'VEL')
    unique_sites = unique([TEMP_coverage_site,VEL_coverage_site,PSAL_coverage_site,DOX_coverage_site,CHL_coverage_site]);
else
    unique_sites = unique([TEMP_coverage_site]);
end
if isfield(coverage,'VEL')
    unique_sites_VEL = unique(VEL_coverage_site);
    unique_sites = [unique_sites, unique_sites_VEL];
end
if isfield(coverage,'PSAL')
    unique_sites_PSAL = unique(PSAL_coverage_site);
    unique_sites = [unique_sites, unique_sites_PSAL];
end
if isfield(coverage,'DOX')
    unique_sites_DOX = unique(DOX_coverage_site);
    unique_sites = [unique_sites, unique_sites_DOX];    
end
if isfield(coverage,'CHL')
    unique_sites_CHL = unique(CHL_coverage_site);
    unique_sites = [unique_sites, unique_sites_CHL];    
end


TEMP_coverage_site_number = ones(size(TEMP_coverage_site));
if exist('VEL_coverage_site','var')
VEL_coverage_site_number = ones(size(VEL_coverage_site));
end
if exist('PSAL_coverage_site','var')
PSAL_coverage_site_number = ones(size(PSAL_coverage_site));
end
if exist('DOX_coverage_site','var')
DOX_coverage_site_number = ones(size(DOX_coverage_site));
end
if exist('CHL_coverage_site','var')
CHL_coverage_site_number = ones(size(CHL_coverage_site));
end

%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
for n_unique_sites = 1:numel(unique_sites)
    %~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    % TEMP
    f_TEMP = TEMP_coverage_site == unique_sites(n_unique_sites);
    TEMP_coverage_site_number(f_TEMP) = unique_sites(n_unique_sites);
    %~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    % VEL
    if exist('VEL_coverage_site','var')    
    f_VEL = VEL_coverage_site == unique_sites(n_unique_sites);
    VEL_coverage_site_number(f_VEL) = unique_sites(n_unique_sites);
    end
    %~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    % PSAL
    if exist('PSAL_coverage_site','var')
    f_PSAL = PSAL_coverage_site == unique_sites(n_unique_sites);
    PSAL_coverage_site_number(f_PSAL) = unique_sites(n_unique_sites);    
    end
    %~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    % DOX
    if exist('DOX_coverage_site','var')
    f_DOX = DOX_coverage_site == unique_sites(n_unique_sites);
    DOX_coverage_site_number(f_DOX) = unique_sites(n_unique_sites);   
    end
    %~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    % CHL
    if exist('CHL_coverage_site','var')
    f_CHL = CHL_coverage_site == unique_sites(n_unique_sites);
    CHL_coverage_site_number(f_CHL) = unique_sites(n_unique_sites);  
    end
end
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% clear unnecessary variables
clear f_* n_unique_sites unique_sites
%% convert individual site numbers to plot y coordinates
% Process: define new y locations for each variable, define yticks and
% labels for each variable, 
Tconv = 5:5:2002; Vconv = 4:5:2001; PSALconv = 3:5:2000; DOXconv = 2:5:199; CHLconv = 1:5:1989;
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% TEMP
TEMP_un = unique(TEMP_coverage_site_number);
% remove missing values
f_missing = ismissing(TEMP_coverage_site_string);
TEMP_coverage_site_string(f_missing) = [];
TEMP_coverage_site(f_missing) = [];
TEMP_coverage_site_number(f_missing) = [];
TEMP_coverage(f_missing) = [];
TEMP_un = unique(TEMP_coverage_site_number);
for n_site = 1:numel(TEMP_un)
    check = TEMP_coverage_site_number == TEMP_un(n_site);
    T_plot_coord(check) = Tconv(TEMP_un(n_site))* ones(size(1,sum(check)));
    T_plot_labels(check) = string(repmat([num2str(unique(TEMP_coverage_site_string(check)))],[sum(check) 1]));
end
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% VEL
if exist('VEL_coverage_site','var')
VEL_un = unique(VEL_coverage_site_number);
loop_it = 1:numel(TEMP_un);
for n_site = 1:numel(VEL_un)
    check = VEL_coverage_site_number == VEL_un(n_site);
    V_plot_coord(check) = Vconv(VEL_un(n_site))* ones(size(1,sum(check)));
    V_plot_labels(check) = string(repmat([num2str(unique(VEL_coverage_site_string(check)))],[sum(check) 1]));
end
end
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% PSAL
if exist('PSAL_coverage_site','var')
% remove missing values
f_missing = ismissing(PSAL_coverage_site_string);
PSAL_coverage_site_string(f_missing) = [];
PSAL_coverage_site(f_missing) = [];
PSAL_coverage_site_number(f_missing) = [];
PSAL_coverage(f_missing) = [];
PSAL_un = unique(PSAL_coverage_site_number);
for n_site = 1:numel(PSAL_un)
    check = PSAL_coverage_site_number == PSAL_un(n_site);
    PSAL_plot_coord(check) = PSALconv(PSAL_un(n_site))* ones(size(1,sum(check)));
    PSAL_plot_labels(check) = string(repmat([num2str(unique(PSAL_coverage_site_string(check)))],[sum(check) 1]));    
end
end
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% DOX
if exist('DOX_coverage_site','var')
DOX_un = unique(DOX_coverage_site_number);
for n_site = 1:numel(DOX_un)
    check = DOX_coverage_site_number == DOX_un(n_site);
    DOX_plot_coord(check) = DOXconv(DOX_un(n_site))* ones(size(1,sum(check)));
    DOX_plot_labels(check) = string(repmat([num2str(unique(DOX_coverage_site_string(check)))],[sum(check) 1]));    
end
end
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% CHL
if exist('CHL_coverage_site','var')
CHL_un = unique(CHL_coverage_site_number);
for n_site = 1:numel(CHL_un)
    check = CHL_coverage_site_number == CHL_un(n_site);
    CHL_plot_coord(check) = CHLconv(CHL_un(n_site))* ones(size(1,sum(check)));
    CHL_plot_labels(check) = string(repmat([num2str(unique(CHL_coverage_site_string(check)))],[sum(check) 1]));    
end
end
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% get ytick information
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% TEMP
T_unC = unique(T_plot_coord);
for n_unique = 1:numel(T_unC)
    labels.T_label(n_unique) = unique(T_plot_labels(T_plot_coord == T_unC(n_unique)));
    labels.T_tick(n_unique) = T_unC(n_unique);
end
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% VEL
if exist('VEL_coverage_site','var')
V_unC = unique(V_plot_coord);
for n_unique = 1:numel(V_unC)
    labels.V_label(n_unique) = unique(V_plot_labels(V_plot_coord == V_unC(n_unique)));
    labels.V_tick(n_unique) = V_unC(n_unique);
end
end
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% PSAL
if exist('PSAL_coverage_site','var')
PSAL_unC = unique(PSAL_plot_coord);
for n_unique = 1:numel(PSAL_unC)
    labels.PSAL_label(n_unique) = unique(PSAL_plot_labels(PSAL_plot_coord == PSAL_unC(n_unique)));
    labels.PSAL_tick(n_unique) = PSAL_unC(n_unique);
end
end
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% DOX
if exist('DOX_coverage_site','var')
DOX_unC = unique(DOX_plot_coord);
for n_unique = 1:numel(DOX_unC)
    labels.DOX_label(n_unique) = unique(DOX_plot_labels(DOX_plot_coord == DOX_unC(n_unique)));
    labels.DOX_tick(n_unique) = DOX_unC(n_unique);
end
end
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% CHL
if exist('CHL_coverage_site','var')
CHL_unC = unique(CHL_plot_coord);
for n_unique = 1:numel(CHL_unC)
    labels.CHL_label(n_unique) = unique(CHL_plot_labels(CHL_plot_coord == CHL_unC(n_unique)));
    labels.CHL_tick(n_unique) = CHL_unC(n_unique);
end
end
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
combined_labels = [labels.T_label];
combined_ticks = [labels.T_tick];
if exist('VEL_coverage_site','var')
    combined_labels = [combined_labels, labels.V_label];
    combined_ticks = [combined_ticks, labels.V_tick];
end
if exist('PSAL_coverage_site','var')
    combined_labels = [combined_labels, labels.PSAL_label];
    combined_ticks = [combined_ticks, labels.PSAL_tick];
end
if exist('DOX_coverage_site','var')
    combined_labels = [combined_labels, labels.DOX_label];
    combined_ticks = [combined_ticks, labels.DOX_tick];
end
if exist('CHL_coverage_site','var')
    combined_labels = [combined_labels, labels.CHL_label];
    combined_ticks = [combined_ticks, labels.CHL_tick];
end

%% Sort out yticks further, and define xticks
% yticks need to be increasing, and remove spaces between yticks for
% aesthetics 
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% sorting yticks
[~,idx] = sort(combined_ticks);
combined_ticks = combined_ticks(idx);
combined_labels = combined_labels(idx);
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% remove gaps in ytick coordinates to make plot look nicer
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% process: for each iteration, work out difference between each element of
% yticks, continue until there are no differences
new_combined_ticks = combined_ticks;
for n_ticks = 1:numel(new_combined_ticks)
    ct_diff = diff(new_combined_ticks);
    ct_diff(2:numel(ct_diff)+1) = ct_diff;ct_diff(1) = 0; 
    ct_diff(ct_diff == 1) = 0;
    ct_diff(ct_diff > 0) = ct_diff(ct_diff > 0)-1;
    if sum(ct_diff) > 0
        new_combined_ticks = new_combined_ticks - ct_diff;
    else
        continue
    end
end
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% Now convert the y plot coordinates to the new yticks so that the data
% coverage and yticks and yticklabels match
for n_diff = 1:numel(combined_ticks)
    T_plot_coord(T_plot_coord == combined_ticks(n_diff)) = new_combined_ticks(n_diff);
    if exist('VEL_coverage_site','var')    
        V_plot_coord(V_plot_coord == combined_ticks(n_diff)) = new_combined_ticks(n_diff);
    end
    if exist('PSAL_coverage_site','var')
        PSAL_plot_coord(PSAL_plot_coord == combined_ticks(n_diff)) = new_combined_ticks(n_diff);
    end
    if exist('DOX_coverage_site','var')
        DOX_plot_coord(DOX_plot_coord == combined_ticks(n_diff)) = new_combined_ticks(n_diff);
    end
    if exist('CHL_coverage_site','var')
        CHL_plot_coord(CHL_plot_coord == combined_ticks(n_diff)) = new_combined_ticks(n_diff);
    end
end
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% for xticks
% to show a vertical line for each year on record
[yrs,~,~,~,~,~] = datevec([TEMP_coverage]);
if exist('VEL_coverage_site','var')
    [yrs_VEL,~,~,~,~,~] = datevec([VEL_coverage]);
    yrs = [yrs,yrs_VEL];
end
if exist('PSAL_coverage_site','var')
    [yrs_PSAL,~,~,~,~,~] = datevec([PSAL_coverage]);
    yrs = [yrs,yrs_PSAL];
end
if exist('DOX_coverage_site','var')
    [yrs_DOX,~,~,~,~,~] = datevec([DOX_coverage]);
    yrs = [yrs,yrs_DOX];
end
if exist('CHL_coverage_site','var')
    [yrs_CHL,~,~,~,~,~] = datevec([CHL_coverage]);
    yrs = [yrs,yrs_CHL];
end
yrs_un = nanmin(yrs):nanmax(yrs);
xticks = datenum(yrs_un,01,01);
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% clear unnecessary variables
clear check BGC_un BGC_unC T_un T_unC V_un V_unC *conv idx n_site n_unique TEMP_un VEL_un yrs_un

%% Create Plot

figure('units','normalized','position',[0 1 1 1])
% scatter the data
hold on

scatter(TEMP_coverage,T_plot_coord,60,'filled','Marker','Sq',...
    'MarkerFaceColor','k','MarkerEdgeColor','k')
Tl = scatter(TEMP_coverage,T_plot_coord,'filled','Marker','Sq',...
    'MarkerFaceColor',[.2 .6 .8],'MarkerEdgeColor',[.2 .6 .8]);

if exist('VEL_coverage_site','var')
scatter(VEL_coverage,V_plot_coord,60,'filled','Marker','Sq',...
    'MarkerFaceColor','k','MarkerEdgeColor','k')
Vl = scatter(VEL_coverage,V_plot_coord,'filled','Marker','Sq',...
    'MarkerFaceColor',[.6 .4 .4],'MarkerEdgeColor',[.6 .4 .4]);
end

if exist('PSAL_coverage_site','var')
    scatter(PSAL_coverage,PSAL_plot_coord,60,'filled','Marker','Sq',...
        'MarkerFaceColor','k','MarkerEdgeColor','k')
    Sl = scatter(PSAL_coverage,PSAL_plot_coord,'filled','Marker','Sq',...
        'MarkerFaceColor',[1 .8 .4],'MarkerEdgeColor',[1 .8 .4]);
end

if exist('DOX_coverage_site','var')
    scatter(DOX_coverage,DOX_plot_coord,60,'filled','Marker','Sq',...
        'MarkerFaceColor','k','MarkerEdgeColor','k')
    Dl = scatter(DOX_coverage,DOX_plot_coord,'filled','Marker','Sq',...
        'MarkerFaceColor',[.6 .8 .8],'MarkerEdgeColor',[.6 .8 .8]);
end

if exist('CHL_coverage_site','var')
    scatter(CHL_coverage,CHL_plot_coord,60,'filled','Marker','Sq',...
        'MarkerFaceColor','k','MarkerEdgeColor','k')
    Cl = scatter(CHL_coverage,CHL_plot_coord,'filled','Marker','Sq',...
        'MarkerFaceColor',[.2 .6 .4],'MarkerEdgeColor',[.2 .6 .4]);
end

% convert x-axis from datenum to datestr
datetick('x','YYYY','KeepLimits');  
% set axes properties
xlimits = [min([TEMP_coverage])-60 ...
                max([TEMP_coverage])+60];
if exist('VEL_coverage_site','var')
    xlimits = [min([TEMP_coverage,VEL_coverage])-60 ...
                max([TEMP_coverage,VEL_coverage])+60];
end
if exist('PSAL_coverage_site','var')
    xlimits = [min([TEMP_coverage,VEL_coverage,PSAL_coverage])-60 ...
                max([TEMP_coverage,VEL_coverage,PSAL_coverage])+60];
end
if exist('PSAL_coverage_site','var') & exist('DOX_coverage_site','var')
    xlimits = [min([TEMP_coverage,VEL_coverage,PSAL_coverage,DOX_coverage])-60 ...
                max([TEMP_coverage,VEL_coverage,PSAL_coverage,DOX_coverage])+60];
end
if exist('PSAL_coverage_site','var') & exist('DOX_coverage_site','var') & exist('CHL_coverage_site','var')
    xlimits = [min([TEMP_coverage,VEL_coverage,PSAL_coverage,DOX_coverage,CHL_coverage])-60 ...
                max([TEMP_coverage,VEL_coverage,PSAL_coverage,DOX_coverage,CHL_coverage])+60];
end

% reduce clogging-up of labels
unique_n = unique([TEMP_coverage_site]);
unique_n_string = unique([TEMP_coverage_site_string]);
if exist('VEL_coverage_site','var')
   unique_n = unique([unique_n, VEL_coverage_site]);
   unique_n_string = unique([unique_n_string, VEL_coverage_site_string]);
end
if exist('PSAL_coverage_site','var')
   unique_n = unique([unique_n, PSAL_coverage_site]);
   unique_n_string = unique([unique_n_string, PSAL_coverage_site_string]);   
end
if exist('DOX_coverage_site','var')
   unique_n = unique([unique_n, DOX_coverage_site]);
   unique_n_string = unique([unique_n_string, DOX_coverage_site_string]);   
end
if exist('CHL_coverage_site','var')
   unique_n = unique([unique_n, CHL_coverage_site]);
   unique_n_string = unique([unique_n_string, CHL_coverage_site_string]);
end

for n_sites = 1:numel(unique_n_string)
    f_labels = strmatch(unique_n_string(n_sites),combined_labels);
    if ~isempty(f_labels)
        dont_keep = f_labels(f_labels < nanmax(f_labels));
        combined_labels(dont_keep) = '|';
    end
end

set(gca,'LineWidth',2,'FontSize',14,...
    'YLim',[min([new_combined_ticks])-1 ...
            max([new_combined_ticks])+1], ...
            'Box','On','XGrid','On', ...
            'XLim',xlimits, ...
            'YTick',new_combined_ticks, ...
            'YTickLabels',combined_labels, ...
            'XTick',xticks,'XTickLabels',datestr(xticks,'yyyy'));
% labels                      
xlabel('Year','FontSize',24);

if sum(node == 'NSW') == 3 | sum(node == 'WA') > 0 | sum(node == 'SA') > 0
    title([node,'-IMOS Mooring Deployment Coverage'],'FontSize',24);
end
if sum(node == 'QLD') > 0
    title(['Q-IMOS Mooring Deployment Coverage'],'FontSize',24);
end
if sum(node == 'NRS') == 3
    title(['NRS Mooring Deployment Coverage'],'FontSize',24);
end

% reformat axis
ax = gca;
ax.Position(1) = 0.18;
set(gca,'Position',ax.Position);
% add legend
leg = legend([Tl],'Temperature');
if exist('VEL_coverage_site','var')
leg = legend([Tl, Vl],'Temperature','Velocity');
end
if exist('PSAL_coverage_site','var')
leg = legend([Tl, Vl, Sl],'Temperature','Velocity','Salinity');
end
if exist('PSAL_coverage_site','var') & exist('DOX_coverage_site','var')
leg = legend([Tl, Vl, Sl, Dl],'Temperature','Velocity','Salinity','O_2');
end
if exist('PSAL_coverage_site','var') & exist('DOX_coverage_site','var') & exist('CHL_coverage_site','var')
leg = legend([Tl, Vl, Sl, Dl, Cl],'Temperature','Velocity','Salinity','O_2','Chl. Fluorescence');
end
leg.Position(1) = 0.005;
leg.Position(2) = 0.15;
set(leg,'Box','Off','FontSize',18,'Position',leg.Position);
% add IMOS logo
axes
logo = imread('IMOS_logo.png');
imagesc(logo)
set(gca,'Position',[0.005 0.8 0.11 0.11],'Visible','Off')
set(gcf,'Color','w');
% add plot credit
annotation(gcf,'textbox',...
    [0.00933333333333333 0.0117493472584856 0.5 0.0248041775456919],...
    'String','Plotting software developed by NSW-IMOS: Michael Hemming, Moninya Roughan, Amandine Schaeffer.','FitBoxToText','off',...
    'LineStyle','None','FontSize',12,'FitBoxToText','off');

% final say
disp('Plot Created. Save interactively, or if you require HD plots use the following:')

if saving == 1
    [yrs,mns,dys,~,~,~] = datevec(now);
    print(gcf,'-dpng','-r400',[node,'_mooring_coverage.png']);
    disp('Plot saved.')
    
%     savefig([node,'_mooring_coverage_',datestr(datenum(yrs,mns,dys)),'.fig']);
end

disp(' If you use this plot, please cite this software as: example')
end