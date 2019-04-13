#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 16:27:42 2019

@author: zackkingbackup
"""
import boto3

from extract import extract
from transform import transform
from load import load


def lambda_handler(event, context):
    
    ''' Event is passed with --payload from AWS CLI or test from console. '''
    query_date = event['query_date']
    
    ''' set up an S3 resource to use for file download/upload to S3 bucket '''
    s3_resource = boto3.resource('s3')
    
    ''' execute the ETL functions '''
    extract(query_date,s3_resource)
    transform(query_date,s3_resource)
    load(query_date,s3_resource)
    
    print ("SampleProject completed with input: "+str(query_date))
    return