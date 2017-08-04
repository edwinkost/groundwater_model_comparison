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

    def initial(self): 
        pass

    def dynamic(self):
        
        # re-calculate current model time using current pcraster timestep value
        self.modelTime.update(self.currentTimeStep())

        # perform the operation only at the last day of the month (as the input netcdf file has a monthly resolution with the last date of the month as its time stamp)
        if self.modelTime.isLastDayOfMonth():
        
            # reading a netcdf file (global extent, 5 arcmin resolution): 
            pcr.setclone(self.globeCloneMapFileName)
            global_pcraster_map = vos.netcdf2PCRobjClone(ncFile    = self.netcdf_input['file_name'], \
                                                         varName   = self.netcdf_input['variable_name'], \
                                                         dateInput = self.modelTime.fulldate)
            # save it to pcraster maps (still at a global extent and 5 arcmin resolution); 
            # there will be two files as follows:
            # - Format 1: example file names: htop0000.001 (for the 1st time step), htop0000.002, htop0000.003, etc. ...
            pcraster_file_name = pcraster_output['output_folder'] + "/global/" + pcraster_output['file_name']
            pcraster_map_file_name = pcr.framework.frameworkBase.generateNameT(pcraster_file_name,\
                                                                               self.modelTime.timeStepPCR)
            pcr.report(global_pcraster_map, pcraster_file_name)
            # - Format 2: example file names: htop_2000_01.map, htop_2000_02.map, etc.
            pcraster_file_name = pcraster_output['output_folder'] + "/global/" + pcraster_output['file_name'] + "_" + self.modelTime.fulldate[0:7].replace("-", "_") + "*.map"
            pcr.report(global_pcraster_map, pcraster_file_name)
            
            # reproject and resample it to a local coordinate system
            pcr.setclone(self.localCloneMapFileName)
            local_pcraster_map = vos.readPCRmapClone(v = pcraster_file_name, \
                                                     cloneMapFileName = self.localCloneMapFileName, \
                                                     tmpDir = self.output['folder'] + "/tmp/", \
                                                     absolutePath = None,\
                                                     isLddMap = False, \
                                                     cover = None, \
                                                     isNomMap = False, \
                                                     inputEPSG  = self.inputEPSG, 
                                                     outputEPSG = self.outputEPSG,
                                                     method = "near")
            # save it to pcraster maps (now already at the extent, the resolution and the coordinate system of the local model) 
            # there will be two file sas follows:
            # - Format 1: example file names: htop0000.001 (for the 1st time step), htop0000.002, htop0000.003, etc. ...
            pcraster_file_name = pcraster_output['output_folder'] + "/regional/" + pcraster_output['file_name']
            pcraster_map_file_name = pcr.framework.frameworkBase.generateNameT(pcraster_file_name,\
                                                                               self.modelTime.timeStepPCR)
            pcr.report(local_pcraster_map, pcraster_file_name)
            # - Format 2: example file names: htop_2000_01.map, htop_2000_02.map, etc.
            pcraster_file_name = pcraster_output['output_folder'] + "/regional/" + pcraster_output['file_name'] + "_" + self.modelTime.fulldate[0:7].replace("-", "_") + "*.map"
            pcr.report(local_pcraster_map, pcraster_file_name)
