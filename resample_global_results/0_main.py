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

# file name of the clone map defining the scope of output
cloneMapFileName = "/home/edwinhs/github/edwinkost/groundwater_model_comparison/making_clone_map_from_idf/clone_map_colombia_model.map"

# netcdf input file name
netcdf_input = {}
netcdf_input['file_name']     =  
netcdf_input['variable_name'] = varDict.netcdf_short_name[efas_variable_name] 

# location where outpuut pcraster files will be stored
pcraster_files = {}
pcraster_files['directory'] = "/scratch/edwin/input/forcing/hyperhydro_wg1/EFAS/source/pcraster/"
pcraster_files['file_name'] = efas_variable_name # "pr"

# prepare the output directory
try:
    os.makedirs(output['folder'])
except:
    os.system('rm -r ')
    pass

startDate     = "1990-01-01" # YYYY-MM-DD
endDate       = None

# projection/coordinate sy
inputEPSG  = "EPSG:3035" 
outputEPSG = "EPSG:4326"
resample_method = "near"

###########################################################################################################

def main():
    
    # prepare logger and its directory
    log_file_location = output['folder']+"/log/"
    try:
        os.makedirs(log_file_location)
    except:
        pass
    vos.initialize_logging(log_file_location)
    
    # time object
    modelTime = ModelTime() # timeStep info: year, month, day, doy, hour, etc
    modelTime.getStartEndTimeSteps(startDate,endDate,nrOfTimeSteps)
    
    calculationModel = CalcFramework(cloneMapFileName,\
                                     pcraster_files, \
                                     modelTime, \
                                     output, inputEPSG, outputEPSG, resample_method)

    dynamic_framework = DynamicFramework(calculationModel,modelTime.nrOfTimeSteps)
    dynamic_framework.setQuiet(True)
    dynamic_framework.run()

if __name__ == '__main__':
    sys.exit(main())
