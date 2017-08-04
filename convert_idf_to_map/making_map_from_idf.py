#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import glob

import pcraster as pcr

import raster_func

# input directory containing idf file
inp_folder = "/scratch-shared/edwinhs/tristan_data/Colombia/head/l1/"
inp_folder = "/scratch-shared/edwinhs/tristan_data/Colombia/head/l2/"
inp_folder = "/scratch-shared/edwinhs/tristan_data/Colombia/head/l3/"

# list of idf files
idf_files  = glob.glob(inp_folder + "/*")

# output directory
out_folder = "/scratch-shared/edwinhs/colombia_model_results/head/l1_top/"
out_folder = "/scratch-shared/edwinhs/colombia_model_results/head/l2_mid/"
out_folder = "/scratch-shared/edwinhs/colombia_model_results/head/l3_bot/"

# making output directory
try:
    os.makedirs(out_folder)
except:
    os.system('rm -r ' + str(out_folder))
    pass

# convert idf file to map file
for idf_file in idf_files:
    print idf_file
    # read idf file
    map_array = raster_func.raster2arr(idf_file)
    # save it to pcraster file
    pcraster_file_name = out_folder + "/" + os.path.basename(idf_file) + ".map"
    print pcraster_file_name
    map_array .write(pcraster_file_name)
