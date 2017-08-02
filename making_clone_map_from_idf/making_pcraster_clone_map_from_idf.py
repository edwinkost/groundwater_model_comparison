#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

import pcraster as pcr

import raster_func

# reference/input idf file
idf_file_name       = "head_20000101_l1.idf"

# output file name for pcraster clone
clone_map_file_name = "clone_map_colombia_model.map"

# read idf file
map_array = raster_func.raster2arr(idf_file_name)

# convert the array to a pcraster file and make a pcraster clone map file based on this array
map_array.write(clone_map_file_name + ".tmp")
clone_map = pcr.defined(pcr.defined(clone_map_file_name + ".tmp"))
pcr.report(clone_map, clone_map_file_name)
