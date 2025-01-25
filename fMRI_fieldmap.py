#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 15:04:30 2023

@author: victor
"""

import os
from os.path import join
import fnmatch
from nipype.interfaces import afni
import json


maindir = os.path.dirname(os.path.split(os.getcwd())[0])

datadir = join(maindir,'Data/fMRI/VHMC/resting-task_state')

patient_list = sorted([x for x in fnmatch.filter(os.listdir(datadir),'sub-*')])

for patient in patient_list:
    
    magnitude_file = sorted(fnmatch.filter(os.listdir(join(datadir,patient,'fmap')),'*_magnitude1.nii'))
    
    phase_file = sorted(fnmatch.filter(os.listdir(join(datadir,patient,'fmap')),'*_phasediff.nii'))
    
    fmri_path = sorted(fnmatch.filter(os.listdir(join(datadir, patient, 'func')),'*run-*_bold.nii'))
    
    json_path = sorted(fnmatch.filter(os.listdir(join(datadir, patient, 'func')),'*run-*_bold.json'))
    
    os.system(str('bet %s %s -f .6 -R -m'
              % (join(datadir,patient,'fmap',str(magnitude_file)[2:-6]),
                 join(datadir,patient,'fmap',str(magnitude_file)[2:-6] + '_brain.nii.gz'))))
    
    os.system(str('fsl_prepare_fieldmap SIEMENS %s %s %s 2.46'
              % (join(datadir,patient,'fmap',str(phase_file)[2:-6]),
                 join(datadir,patient,'fmap',str(magnitude_file)[2:-6] + '_brain.nii.gz'),
                 join(datadir,patient,'fmap','fmap_rads.nii.gz'))))
    
    for run, path in enumerate(fmri_path):
        
        f = open(join(datadir,patient,'func',str(json_path[run])))
        
        data = json.load(f)
        
        tshift = afni.TShift()
        
        tshift.inputs.in_file = join(datadir,patient,'func',str(fmri_path[run]))
                        
        tshift.inputs.slice_timing = data['SliceTiming']
                        
        tshift.cmdline
        
        os.system(str('3dTshift -overwrite -quintic -TR 2 -tpattern @slice_timing.1D -prefix %s %s'
                  % (join(datadir,patient,'func',str(fmri_path[run])[0:-4] + '_shift.nii.gz'),
                     join(datadir,patient,'func',str(fmri_path[run])))))
        
        os.system(str('fslroi %s %s 0 1'
                  % (join(datadir,patient,'func',str(fmri_path[run])[0:-4] + '_shift.nii.gz'),
                     join(datadir,patient,'func',str(fmri_path[run])[0:-4] + '_01.nii.gz'))))
        
        os.system(str('flirt -in %s -ref %s -out %s -omat %s'
                  % (join(datadir,patient,'fmap',str(magnitude_file)[2:-6] + '_brain.nii.gz'),
                     join(datadir,patient,'func',str(fmri_path[run])[0:-4] + '_01.nii.gz'),
                     join(datadir,patient,'fmap',str(magnitude_file)[2:-6] + '_run_' + str(run + 1) + '.nii'),
                     join(datadir,patient,'fmap','matrix_fm_run_' + str(run + 1)))))
        
        os.system(str('flirt -in %s -ref %s -applyxfm -init %s -out %s'
                  % (join(datadir,patient,'fmap','fmap_rads.nii.gz'),
                     join(datadir,patient,'func',str(fmri_path[run])[0:-4] + '_01.nii.gz'),
                     join(datadir,patient,'fmap','matrix_fm_run_' + str(run + 1)),
                     join(datadir,patient,'fmap','fmap_rads_run_' + str(run + 1) + '.nii'))))
        
        os.system(str('rm -r %s' %join(datadir,patient,'func',str(fmri_path[run])[0:-4] + '_01.nii.gz')))
        
        os.system(str('fugue -i %s -s 4 --unwarpdir=y- --loadfmap=%s --dwell=0.00033 -u %s'
                  % (join(datadir,patient,'func',str(fmri_path[run])[0:-4] + '_shift.nii'),
                     join(datadir,patient,'fmap','fmap_rads_run_' + str(run + 1) + '.nii.gz'),
                     join(datadir,patient,'func',str(fmri_path[run])[0:-4] + '_fm.nii.gz'))))
        
        os.system(str('rm -r %s %s'
                  % (join(datadir,patient,'func',str(fmri_path[run])),
                     join(datadir,patient,'func',str(fmri_path[run])[0:-4] + '_shift.nii.gz'))))
        
        os.system(str('gunzip %s'
                  % (join(datadir,patient,'func',str(fmri_path[run])[0:-4] + '_fm.nii.gz'))))

        os.system(str('mv %s %s' 
                  % (join(datadir,patient,'func',str(fmri_path[run])[0:-4] + '_fm.nii'),
                     join(datadir,patient,'func',str(fmri_path[run])))))
        
        del f, data, tshift