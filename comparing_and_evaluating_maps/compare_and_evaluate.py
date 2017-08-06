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

# output folder location
output_folder = "/scratch-shared/edwinhs/tristan_output/evaluation/"
try:
    os.makedirs(output_folder)
except:
    pass
    
# calculate the average value/map of the local model
msg = "Calculate the average value/map of the local model!"
print(msg)
# - Using the top layer of the local model
local_model_folder  = "/scratch-shared/edwinhs/colombia_model_results/head/l1_top/" 
i_month = 0
cum_map = pcr.scalar(0.0)
for year in range(str_year, end_year + 1, 1):
    for month in range(1, 12 + 1, 1):
        # file name, e.g. "/scratch-shared/edwinhs/colombia_model_results/head/l1_top/head_20000201_l1.idf.map"
        file_name = "head_%04d%02d" %(year, month)
        file_name = local_model_folder + "/" + file_name + "01_l1.idf.map"   
        print(file_name)
        # cummulative values
        cum_map   = cum_map + pcr.readmap(file_name)
        i_month   = i_month + 1
# calculating average and saving it to a pcraster map
average_local = cum_map / i_month
pcr.aguila(average_local)
output_filename = output_folder + "/average_local.map"
pcr.report(average_local, output_filename)

# calculate the average value/map of the global model
msg = "Calculate the average value/map of the global model!"
print(msg)
# - Using the top layer of the global model
global_model_folder  = "/scratch-shared/edwinhs/modflow_results_in_pcraster/upper_layer/regional/" 
i_month = 0
cum_map = pcr.scalar(0.0)
for year in range(str_year, end_year + 1, 1):
    for month in range(1, 12 + 1, 1):
        # file name, e.g. /scratch-shared/edwinhs/modflow_results_in_pcraster/upper_layer/regional/htop_2000_01.map
        file_name = "htop_%04d_%02d" %(year, month)
        file_name = global_model_folder + "/" + file_name + ".map"   
        print(file_name)
        # cummulative values
        cum_map   = cum_map + pcr.readmap(file_name)
        i_month   = i_month + 1
# calculating average and saving it to a pcraster map
average_global = cum_map / i_month
# use only the values where local model exists:
average_global = pcr.ifthen(pcr.defined(average_local), average_global)
pcr.aguila(average_global)
pcr.report(average_global, output_folder + "/average_global.map")

# evaluating/comparing two maps 
difference = average_local - average_global
pcr.aguila(difference)
pcr.report(difference, output_folder + "/bias.map")

