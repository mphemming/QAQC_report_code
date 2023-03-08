@echo off
set MATLAB_DIR=C:\Program Files\MATLAB\R2020a
set SCRIPT_DIR=C:\Users\mphem\OneDrive - UNSW\Work\QC_reports\Code\Matlab\
set SCRIPT_NAME=QCreport_plot_mooring_coverage_thredds.m

REM change directory to the script directory
cd /d %SCRIPT_DIR%

REM call MATLAB with the script
"%MATLAB_DIR%\bin\matlab.exe" -nodesktop -nosplash -r "run('%SCRIPT_NAME%'); exit;"
