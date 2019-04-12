#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 19:33:06 2019

This is the Extract Module for my ETL code.
It must satisfy the following contract:
    1. Accept a QUERY DATE, S3 resource instance, boolean
       telling function whether its being run locally or by
       an AWS Lambda, local temp space, and a bucket name as inputs
    2. read sample-extract-output.csv from the top
       level folder in my S3 Bucket (mybucket1219)
    3. write the unmodified file to
       s3://$BUCKET/sample-project/extract/$QUERY_DATE/${QUERY_DATE}-extract-output.csv
       such that $BUCKET == mybucket1219

@author: zackkingbackup
"""

def extract_function(QUERY_DATE,s3_resource,LOCAL=False,
                     BUCKET='mybucket1219',
                     local_temp='data/'):
    '''
        extract_function(QUERY_DATE,s3_resource,LOCAL=False,
                     BUCKET='mybucket1219',
                     local_temp='data/'
            download sample-extract-output.csv from s3 and then upload
            it as sample-project/extract/$QUERY_DATE/${QUERY_DATE}-extract-output.csv
            
            Public API function
            
            Parameters
            ----------
            QUERY_DATE : str
                A date in the form YYYY-MM-DD
            s3_resource : boto3.resources.factory.s3.ServiceResource
                The s3 resource used for file upload/download from s3 bucket
            LOCAL : boolean, default=False
                Run ETL job from local machine (True) or from AWS Lambda (False)
            BUCKET : str, default='mybucket1219'
                Name of s3 bucket to read/write from
            local_temp : str, default='data/'
                Directory for storing temporary files created as part
                of the ETL job
            
            Returns
            -------
            none
    '''

    csvfile = 'sample-extract-output.csv' 
    download_loc = ''
    
    if LOCAL:
        download_loc = str(local_temp)+str(csvfile)
        s3_resource.Object(BUCKET, csvfile).download_file(
            download_loc)
    else:
        download_loc = '/tmp/'+str(csvfile)
        s3_resource.Object(BUCKET, csvfile).download_file(
            download_loc)
                
    s3_resource.Bucket(BUCKET).upload_file(
        Filename=download_loc, Key='sample-project/extract/'+str(QUERY_DATE)+'/'\
    +str(QUERY_DATE)+'-extract-output.csv')
    
    return


