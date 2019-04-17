#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 19:33:06 2019

This is the Extract Module for my ETL code.
It must satisfy the following contract:
    1. Accept a query_date, S3 resource instance, a local temp space, 
       and a bucket name as inputs
    2. read sample-extract-output.csv from the top
       level folder in my S3 Bucket (mybucket1219)
    3. write the unmodified file to
       s3://$BUCKET/sample-project/extract/$QUERY_DATE/${QUERY_DATE}-extract-output.csv
       such that $BUCKET == mybucket1219

@author: zackkingbackup
"""
import os

def extract(query_date,s3_resource,
            bucket='mybucket1219',
            local_temp='/tmp/'):
    '''
        extract(query_date,s3_resource,
                bucket='mybucket1219',
                local_temp='/tmp/'
            Download sample-extract-output.csv from s3 and then upload
            it as sample-project/extract/$QUERY_DATE/${QUERY_DATE}-extract-output.csv
            
            Public API function
            
            Parameters
            ----------
            query_date : str
                A date in the form YYYY-MM-DD
            s3_resource : boto3.resources.factory.s3.ServiceResource
                The s3 resource used for file upload/download from s3 bucket
            bucket : str, default='mybucket1219'
                Name of s3 bucket to read/write from
            local_temp : str, default='/tmp/'
                Directory for storing temporary files created as part
                of the ETL job
            
            Returns
            -------
            None
    '''

    csvfile = 'sample-extract-output.csv' 
    
    download_loc = os.path.join(local_temp,csvfile)
    s3_resource.Object(bucket, csvfile).download_file(
            download_loc)
    
    vars = {'QUERY_DATE' : query_date}            
    s3_resource.Bucket(bucket).upload_file(
        Filename=download_loc, 
        Key=os.path.join('sample-project',
                         'extract',
                         str(query_date),
                         '{QUERY_DATE}-extract-output.csv'.format_map(vars)))
    
    return


