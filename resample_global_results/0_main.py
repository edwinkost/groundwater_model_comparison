#!/usr/bin/python
# -*- coding: utf-8 -*-

# EHS (02 August 2017): This is the main script for converting 
#                       a netcdf fileset of pcraster time series maps  
#                          into a single netcdf time series file. 
#
# EHS (27 November 2014): I use this script for converting EFAS-Meteo pcraster files to netcdf format

import os
import sys

# pcraster dynamic framework is used.
from pcraster.framework import DynamicFramework

# The calculation script (engine) is imported from the following module.
from dynamic_calc_framework import CalcFramework

# time object
from currTimeStep import ModelTime

# utility module:
import virtualOS as vos

# variable dictionaries:
import efas_variable_list_final as varDict

import logging
logger = logging.getLogger(__name__)


###########################################################################################################

# file name of the global clone map defining the scope of input (global extent, 5 arcmin resolution) 
globeCloneMapFileName = "/home/edwinhs/github/edwinkost/groundwater_model_comparison/global_maps/lddsound_05min.map"

# file name of the clone map defining the scope of output (from the local/regional model) 
localCloneMapFileName = "/home/edwinhs/github/edwinkost/groundwater_model_comparison/making_clone_map_from_idf/clone_map_colombia_model.map"

# netcdf input file name
netcdf_input = {}
# - for the bottom layer
netcdf_input['file_name']        = "/projects/0/aqueduct/users/edwinhs/pcrglobwb_modflow_version_2015_06_XX/merged_1958_to_2015/global/netcdf/groundwaterHeadLayer1_monthEnd_output_1958-01-31_to_2015-12-31_compressed.nc" 
netcdf_input['variable_name']    = "groundwater_head_for_layer_1" 
#~ # - for the top layer
#~ netcdf_input['file_name']     = "/projects/0/aqueduct/users/edwinhs/pcrglobwb_modflow_version_2015_06_XX/merged_1958_to_2015/global/netcdf/groundwaterHeadLayer2_monthEnd_output_1958-01-31_to_2015-12-31.nc" 
#~ netcdf_input['variable_name'] = "groundwater_head_for_layer_2" 

# location where output pcraster files will be stored
pcraster_output = {}
pcraster_output['output_folder']  = "/scratch-shared/edwinhs/modflow_results_in_pcraster/"

# file names:          
# - for the bottom layer         
pcraster_output['file_name']      = "hbot"
#~ # - for the top layer         
#~ pcraster_output['file_name']   = "htop"

# starting and end dates     # YYYY-MM-DD
startDate     = "2000-01-01"
endDate       = "2012-12-01"

# resampling method
resample_method = "near"

# projection/coordinate system 
# - the input is in the lat/lon coordinate system (WGS 84)
inputEPSG  = "EPSG:4326"
# - the output will be in EPSG:3115, MAGNA-SIRGAS / Colombia West Zone
outputEPSG = "EPSG:3115"
# Info from Sandra: The coordinates for Valle del Cauca (ESCACES): I checked 2 things. 
# * A website I found http://www.cali.gov.co/planeacion/publicaciones/105289/proyecciones_transformaciones_cartograficas_idesc/ where it says for Cali the coordinate system is Sistema de Coordenadas Cartesiano de Cali. (en ArcGIS: MAGNA_Cali_Valle_del_Cauca_2009).
# * I then open one of the files I have in for ESCACES 2 and check the coordinate system (attached image). The CRS is EPSG:3115, MAGNA-SIRGAS / Colombia West Zone.


###########################################################################################################

def main():
    
    # prepare the output directory
    try:
        os.makedirs(pcraster_output['output_folder'])
    except:
        os.system('rm -r ' + str(pcraster_output['output_folder']))
        pass
    # - making the directory for storing global extent output files
    os.makedirs(pcraster_output['output_folder'] + "/global/")
    # - making the directory for storing regional extent output files
    os.makedirs(pcraster_output['output_folder'] + "/regional/")
    
    # prepare logger and its directory
    log_file_location = pcraster_output['output_folder'] + "/log/"
    try:
        os.makedirs(log_file_location)
    except:
        pass
    vos.initialize_logging(log_file_location)

    # prepare a temporary folder
    tmp_file_location = pcraster_output['output_folder'] + "/tmp/"
    try:
        os.makedirs(tmp_file_location)
    except:
        pass

    # time object
    modelTime = ModelTime() # timeStep info: year, month, day, doy, hour, etc
    modelTime.getStartEndTimeSteps(startDate, endDate)
    
    calculationModel = CalcFramework(globeCloneMapFileName, localCloneMapFileName, \
                                     netcdf_input, \
                                     pcraster_output, \
                                     modelTime, \
                                     inputEPSG, outputEPSG, resample_method)

    dynamic_framework = DynamicFramework(calculationModel,modelTime.nrOfTimeSteps)
    dynamic_framework.setQuiet(True)
    dynamic_framework.run()

if __name__ == '__main__':
    sys.exit(main())
