#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import glob

import pcraster as pcr

import raster_func

# set the clone map
pcr.setclone()

# input map(s)
map_1 = 
map_2 = 

# evaluating map (e.g. calculate the difference) 
difference = map_1 - map_2
# and save it to a pcraster file
pcr.report()
# save 
analysis_result = 

