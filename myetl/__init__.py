#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 10:00:59 2019

@author: zackkingbackup
"""

import boto3
import argparse
import os
import json

#from extract import extract
#from transform import transform
#from load import load
from myetl import extract, transform, load


def lambda_handler(event, context):
    
    ''' Event is passed with --payload from AWS CLI or test from console. '''
    query_date = event['query_date']
    
    ''' set up an S3 resource to use for file download/upload to S3 bucket '''
    s3_resource = boto3.resource('s3')
    
    ''' execute the ETL functions '''
    extract.extract(query_date,s3_resource)
    transform.transform(query_date,s3_resource)
    load.load(query_date,s3_resource)
    
    print ("SampleProject completed with input: "+str(query_date))
    return

def cli_handler():
    
    ''' Use argparse.parser to pick off command line args. '''
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
    
    query_date = args.date
    local_temp = args.local_temp
    clean = args.clean
    clean = json.loads(clean.lower())
    
    if os.path.exists(os.path.join(os.getcwd(), local_temp)):
        ''' See if the local temp space already has files in it; delete them. '''
        for temp_file in os.listdir(local_temp):
            file_path = os.path.join(local_temp, temp_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
    else:
        ''' If the local temp space does not exist, create it. '''
        os.mkdir(os.path.join(os.getcwd(), local_temp))
            
    ''' Set up an S3 resource to use for file download/upload to S3 bucket. '''
    s3_resource = boto3.resource('s3')
    
    ''' Execute the ETL functions. '''
    extract.extract(query_date,s3_resource,
            local_temp=local_temp)
    transform.transform(query_date,s3_resource,
              local_temp=local_temp)
    load.load(query_date,s3_resource,
         local_temp=local_temp)
    
    ''' Clean up. '''
    if clean:
        import shutil
        shutil.rmtree(os.path.join(os.getcwd(), local_temp))
        
    return