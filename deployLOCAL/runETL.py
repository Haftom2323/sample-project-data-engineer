#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 22:45:43 2019

@author: zackkingbackup
"""
import sys
sys.path.append('/Users/zackkingbackup/Documents/Job Search/CapitalOne/sample-project-data-engineer/src/')
from Extract import extract_function
from Transform import transform_function
from Load import load_function
import argparse
import boto3
import os

''' use argparse.parser to pick off command line args '''
parser = argparse.ArgumentParser(prog='runETL',
                                 description='Run Sample Project')

parser.add_argument('-d', dest='date',
                    default='1999-12-31',help='Date in YYYY-MM-DD format'+
                    '; default=1999-12-31',
                    metavar='YYYY-MM-DD')
parser.add_argument('-t', dest='local_temp',
                    default='temp_data',
                    help='relative path for directory to temporarily store '+
                    'files downloaded '+
                    'from the S3 bucket.\nOnly needed if running locally;\n'+
                    'default=temp_data',
                    metavar='dir')
parser.add_argument('-C', dest='clean',
                    default='False',help='Boolean to determine if local temp '+
                    'space to store S3 downloads\nshould be deleted on script'+
                    ' completion;\ndefault=False (do not remove it)',
                    metavar='True/False')

args = parser.parse_args()

QUERY_DATE = args.date
local_temp = args.local_temp
clean = args.clean

''' the temp data space needs to end with a forward slash '''
if local_temp[-1] != '/':
    local_temp += '/'

LOCAL = True

if os.path.exists(os.path.join(os.getcwd(), local_temp)):
    ''' see if the local temp space already has files in it; delete them '''
    for temp_file in os.listdir(local_temp):
        file_path = os.path.join(local_temp, temp_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
else:
    ''' if the local temp space does not exist, create it '''
    os.mkdir(os.path.join(os.getcwd(), local_temp))
    
if clean != 'False':
    CLEAN = True
else:
    CLEAN = False
    
''' set up an S3 resource to use for file download/upload to S3 bucket '''
s3_resource = boto3.resource('s3')

''' execute the ETL functions '''
extract_function(QUERY_DATE,s3_resource,LOCAL=LOCAL,
                     local_temp=local_temp)
transform_function(QUERY_DATE,s3_resource,LOCAL=LOCAL,
                     local_temp=local_temp)
load_function(QUERY_DATE,s3_resource,LOCAL=LOCAL,
                     local_temp=local_temp)

''' clean up '''
if CLEAN:
    import shutil
    shutil.rmtree(os.path.join(os.getcwd(), local_temp))