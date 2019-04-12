#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 22:45:43 2019

@author: zackkingbackup
"""

from Extract import extract_function
from Transform import transform_function
from Load import load_function
import argparse

parser = argparse.ArgumentParser(prog='runETL',
                                 description='Run Sample Project')

parser.add_argument('-d', dest='date',
                    default='1999-12-31',help='Date in YYYY-MM-DD format'+
                    '; default=1999-12-31',
                    metavar='YYYY-MM-DD')
parser.add_argument('-t', dest='local_temp',
                    default='temp_data',
                    help='directory to temporarily store files downloaded '+
                    'from the S3 bucket.\nOnly needed if running locally;\n'+
                    'default=temp_data',
                    metavar='dir')
parser.add_argument('-L', dest='local',
                    default='False',help='Boolean to determine if run in AWS'+
                    ' Lambda or Locally; default=False (AWS Lambda)',
                    metavar='True/False')

args = parser.parse_args()

QUERY_DATE = args.date
local_temp = args.local_temp
local = args.local
if local != 'False':
    LOCAL = True
    
    import os
    if os.direxists(os.path.join(os.getcwd(), local_temp)):
        ''' see if the local temp space already has files in it; delete them '''
        for temp_file in os.listdir(local_temp):
            file_path = os.path.join(local_temp, temp_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
    else:
        ''' if the local temp space does not exist, create it '''
        os.mkdir(os.path.join(os.getcwd(), local_temp))
else:
    LOCAL = False



