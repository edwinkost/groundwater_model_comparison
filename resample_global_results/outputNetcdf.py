#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import time
import re
import subprocess
import netCDF4 as nc
import numpy as np
import pcraster as pcr
import virtualOS as vos

class OutputNetcdf():
    
    def __init__(self,cloneMapFileName,netcdf_attribute_description):
        		
        # cloneMap
        cloneMap = pcr.boolean(pcr.readmap(cloneMapFileName))
        cloneMap = pcr.boolean(pcr.scalar(1.0))
        
        # properties of the clone maps
        # - numbers of rows and colums
        rows = pcr.clone().nrRows() 
        cols = pcr.clone().nrCols()
        # - cell size in arc minutes rounded to one value behind the decimal
        cellSizeInArcMin = round(pcr.clone().cellSize() * 60.0, 1) 
        # - cell sizes in ar degrees for longitude and langitude direction 
        deltaLon = cellSizeInArcMin / 60.
        deltaLat = deltaLon
        # - coordinates of the upper left corner - rounded to two values behind the decimal in order to avoid rounding errors during (future) resampling process
        x_min = round(pcr.clone().west(), 2)
        y_max = round(pcr.clone().north(), 2)
        # - coordinates of the lower right corner - rounded to two values behind the decimal in order to avoid rounding errors during (future) resampling process
        x_max = round(x_min + cols*deltaLon, 2) 
        y_min = round(y_max - rows*deltaLat, 2) 
        
        # cell centres coordinates
        self.longitudes = np.arange(x_min + deltaLon/2., x_max, deltaLon)
        self.latitudes  = np.arange(y_max - deltaLat/2., y_min,-deltaLat)

        #~ # cell centres coordinates
        #~ self.longitudes = np.linspace(x_min + deltaLon/2., x_max - deltaLon/2., cols)
        #~ self.latitudes  = np.linspace(y_max - deltaLat/2., y_min + deltaLat/2., rows)
        
        #~ # cell centres coordinates (latitudes and longitudes, directly from the clone maps)
        #~ self.latitudes  = np.unique(pcr.pcr2numpy(pcr.ycoordinate(cloneMap), vos.MV))[::-1]
        #~ self.longitudes = np.unique(pcr.pcr2numpy(pcr.xcoordinate(cloneMap), vos.MV))
        
        # netCDF format and attributes:
        important_information = "The dataset was resampled to "+str(cellSizeInArcMin)+" arc minute resolution. "
        self.format = 'NETCDF3_CLASSIC'
        self.attributeDictionary = {}
        self.attributeDictionary['institution']  = "European Commission - JRC and Department of Physical Geography, Utrecht University"
        self.attributeDictionary['title'      ]  = "EFAS-Meteo 5km for Rhine-Meuse - resampled to "+str(cellSizeInArcMin)+" arc minute resolution. "
        self.attributeDictionary['source'     ]  = "5km Gridded Meteo Database (C) European Commission - JRDC, 2014"
        self.attributeDictionary['history'    ]  = "The data were provided by Ad de Roo (ad.de-roo@jrc.ec.europa.eu) on 19 November 2014 and then converted by Edwin H. Sutanudjaja (E.H.Sutanudjaja@uu.nl) to netcdf. "
        self.attributeDictionary['history'    ] += important_information 
        self.attributeDictionary['references' ]  = "Ntegeka et al., 2013. EFAS-Meteo: A European daily high-resolution gridded meteorological data set. JRC Technical Reports. doi: 10.2788/51262"
        self.attributeDictionary['comment'    ]  = "Please use this dataset only for Hyper-Hydro test bed experiments. " 
        self.attributeDictionary['comment'    ] += "For using it and publishing it, please acknowledge its source: 5km Gridded Meteo Database (C) European Commission - JRDC, 2014 and its reference: Ntegeka et al., 2013 (doi: 10.2788/51262). "
        self.attributeDictionary['comment'    ] += "The original data provided by JRC are in European ETRS projection, 5km grid; http://en.wikipedia.org/wiki/European_grid. "
        self.attributeDictionary['comment'    ] += important_information 

        self.attributeDictionary['description']  = netcdf_attribute_description

        
    def createNetCDF(self,ncFileName,varName,varUnits,varLongName):

        rootgrp= nc.Dataset(ncFileName,'w',format= self.format)

        #-create dimensions - time is unlimited, others are fixed
        rootgrp.createDimension('time',None)
        rootgrp.createDimension('lat',len(self.latitudes))
        rootgrp.createDimension('lon',len(self.longitudes))

        date_time= rootgrp.createVariable('time','f4',('time',))
        date_time.standard_name= 'time'
        date_time.long_name= 'Days since 1901-01-01'

        date_time.units= 'Days since 1901-01-01' 
        date_time.calendar= 'standard'

        lat= rootgrp.createVariable('lat','f4',('lat',))
        lat.long_name= 'latitude'
        lat.units= 'degrees_north'
        lat.standard_name = 'latitude'

        lon= rootgrp.createVariable('lon','f4',('lon',))
        lon.standard_name= 'longitude'
        lon.long_name= 'longitude'
        lon.units= 'degrees_east'

        lat[:]= self.latitudes
        lon[:]= self.longitudes

        shortVarName = varName

        var= rootgrp.createVariable(shortVarName,'f4',('time','lat','lon',) ,fill_value=vos.MV,zlib=True)
        var.standard_name= varName
        var.long_name= varLongName
        var.units= varUnits

        attributeDictionary = self.attributeDictionary
        for k, v in attributeDictionary.items():
          setattr(rootgrp,k,v)

        rootgrp.sync()
        rootgrp.close()

    def data2NetCDF(self,ncFile,varName,varField,timeStamp=None,posCnt=None):

        #-write data to netCDF
        rootgrp= nc.Dataset(ncFile,'a')    

        if isinstance(varName,list) == False: varName = [varName] 
        if isinstance(varField,list) == False: varField = [varField]

        # index for time
        if timeStamp != None:
            date_time = rootgrp.variables['time']
            if posCnt == None: posCnt = len(date_time)
            date_time[posCnt] = nc.date2num(timeStamp,date_time.units,date_time.calendar)	                                                                                                                                                  

        for i in range(0, len(varName)):
            shortVarName = varName[i]
            if timeStamp != None:                                                                                                                                                  
                rootgrp.variables[shortVarName][posCnt,:,:] = varField[i]                                                                      
            else:                                                                                                                                                                      
                rootgrp.variables[shortVarName][:,:]        = varField[i]

        rootgrp.sync()
        rootgrp.close()
