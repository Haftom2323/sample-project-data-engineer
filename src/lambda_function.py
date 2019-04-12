#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 16:27:42 2019

@author: zackkingbackup
"""

from Extract import extract_function
from Transform import transform_function
from Load import load_function
import boto3

def lambda_handler(event, context):
    
    ''' event is passed in with --payload from AWS CLI or test from console '''
    QUERY_DATE = event['QUERY_DATE']
    
    ''' set up an S3 resource to use for file download/upload to S3 bucket '''
    s3_resource = boto3.resource('s3')
    
    ''' execute the ETL functions '''
    extract_function(QUERY_DATE,s3_resource)
    transform_function(QUERY_DATE,s3_resource)
    load_function(QUERY_DATE,s3_resource)
    
    print ("SampleProject completed with input: "+str(QUERY_DATE))
    return