#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import glob

import pcraster as pcr

import raster_func

# set the clone map to the regional/local model
clone_map_filename = "/scratch-shared/edwinhs/colombia_model_results/head/l1_top/head_20000101_l1.idf.map" 
pcr.setclone(clone_map_filename)

# start and end years
str_year = 2000
end_year = 2012

# calculate the average value/map of the local model
msg = "Calculate the average value/map of the local model!"
print(msg)
# - Using the top layer of the local model
local_model_folder  = "/scratch-shared/edwinhs/colombia_model_results/head/l1_top/" 
i_month = 0
cum_map = pcr.scalar(0.0)
for year in range(str_year, end_year + 1, 1):
    for month in range(1, 12+1, 1):
        i_month   = i_month + 1
        file_name = "head_%04d%02d" %(year, month)
        file_name = local_model_folder + "/" + file_name + "01_l1.idf.map"   
        print(file_name)
        cum_map   = cum_map + pcr.readmap(file_name)
average_local = cum_map / i_month
pcr.aguila(average_local)

#~ # calculate the average value/map of the global model
#~ # - Using the upper layer of the global model
#~ global_model_folder = "/scratch-shared/edwinhs/modflow_results_in_pcraster/upper_layer/regional/" 
#~ i_month = 0
#~ for year in (str_year, end_year + 1, 1):
    #~ for month in (1, 12 + 1, 1):
#~ average_global = 
#~ 
#~ # calculate the anomaly value of the local model
#~ anomaly_local  = {}
#~ 
#~ 
#~ # calculate the anomaly value of the global model
#~ anomaly_global = {}
#~ 
#~ 
#~ # calculate the climatology values of the local  model's anomaly value
#~ climatology_anomaly_local = 
#~ for month in (1, 12 + 1, 1):
#~ 
#~ 
#~ # calculate the climatology values of the global model's anomaly value
#~ climatology_anomaly_global = 
#~ for month in (1, 12 + 1, 1):
#~ 
#~ 
#~ # evaluating climatology maps (e.g. calculate the differences in climatology maps) 
#~ difference = map_1 - map_2
#~ for month in (1, 12 + 1, 1):
#~ 
