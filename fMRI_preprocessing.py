#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 12:43:44 2023

@author: victor
"""

import os
from os.path import join
import fnmatch

maindir = os.path.dirname(os.path.split(os.getcwd())[0])
datadir = join(maindir,'Data/fMRI/VHMC/resting-task_state/')
patient_list = sorted([x for x in fnmatch.filter(os.listdir(datadir),'sub-*')])

for patient in patient_list:
    task_images = sorted([x for x in fnmatch.filter(os.listdir(join(datadir, patient, 'func')),'*nii') if 'run-' in x])
    
    for number, i in enumerate(task_images):
         os.system(str('fslroi %s %s 3 120' 
                      % (join(datadir, patient, 'func', i),
                         join(datadir, patient, 'func', i))))
        
        os.system(str('rm %s' % (join(datadir, patient, 'func', i))))        
        os.system(str('gunzip %s' % (join(datadir, patient, 'func', i + '.gz'))))
        os.system(str('3dDespike -NEW25 -overwrite -prefix %s %s' 
                      % (join(datadir, patient, 'func', i),
                         join(datadir, patient, 'func', i))))
        
    rest_image = sorted([x for x in fnmatch.filter(os.listdir(join(datadir, patient, 'func')),'*nii') if '-rest' in x])
    os.system(str('3dDespike -NEW25 -overwrite -prefix %s %s' 
                  % (join(datadir, patient, 'func', str(rest_image)[2:-2]),
                     join(datadir, patient, 'func', str(rest_image)[2:-2]))))
    del task_images, rest_image
    