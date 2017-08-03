#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import datetime

import pcraster as pcr
from pcraster.framework import DynamicModel

from outputNetcdf import OutputNetcdf
import virtualOS as vos

import logging
logger = logging.getLogger(__name__)

class CalcFramework(DynamicModel):

    def __init__(self, globeCloneMapFileName, localCloneMapFileName, \
                       netcdf_input, \
                       pcraster_output, \
                       modelTime, \
                       inputEPSG, outputEPSG, resample_method):
        DynamicModel.__init__(self)
        
        # clone map file names:
        self.globeCloneMapFileName = globeCloneMapFileName
        self.localCloneMapFileName = localCloneMapFileName
        
        # time variable/object
        self.modelTime = modelTime
        
        # netcdf input and pcraster output files
        self.netcdf_input    = netcdf_input
        self.pcraster_output = pcraster_output
        
        # input and output projection/coordinate systems 
        self.inputEPSG  =  inputEPSG
        self.outputEPSG = outputEPSG
        
        # resampling method
        self.resample_method = resample_method

        # prepare temporary directory
        self.tmpDir = output['folder']+"/tmp/"
        try:
            os.makedirs(self.tmpDir)
            os.system('rm -r '+tmpDir+"/*")
        except:
            pass
        
    def initial(self): 
        pass

    def dynamic(self):
        
        # re-calculate current model time using current pcraster timestep value
        self.modelTime.update(self.currentTimeStep())

        # perform the operation only at the last day of the month (as the input netcdf file has a monthly resolution with the last date of the month as its time stamp)
        if self.modelTime.isLastDayOfMonth():
        
            # reading a netcdf file (global extent, 5 arcmin resolution): 
            pcr.setclone(self.globeCloneMapFileName)
            UNTIL THIS PART
            global_pcraster_map = vos.netcdf2PCRobjClone(ncFile  = ,
                                                         varName = ,dateInput,\
                                                         useDoy = None,
                                                         cloneMapFileName  = None,\
                                                         LatitudeLongitude = True,\
                                                         specificFillValue = None)
            
            
            # - save it to a pcraster map (still at global extent and 5 arcmin resolution 
            
            # reproject and resample it to a local coordinate system
            
            # save it to a pcraster map with time stamp as its extension
            
            # save it to a pcraster map with default/common extension for pcraster file time series (e.g. using generateNameT)
            pcraster_map_file_name = pcr.framework.frameworkBase.generateNameT(self.pcraster_file_name,\
                                                                               self.modelTime.timeStepPCR)
        
