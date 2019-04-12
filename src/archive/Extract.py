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
                     local_temp='/Users/zackkingbackup/Documents/Job Search/CapitalOne/'\
                     +'sample-project-data-engineer/data/'):
    ''' 
        download sample-extract-output.csv
        and output it to:
            if running locally - 
                /Users/.../sample-project-data-engineer/data
            if running with AWS Lambda -
                /tmp/
                which should have 512 MB available for storage
                
        then upload to:
            s3://$BUCKET/sample-project/extract/$QUERY_DATE/${QUERY_DATE}-extract-output.csv
    '''

    csvfile = 'sample-extract-output.csv' 
    download_loc = ''
    
    if LOCAL:
        s3_resource.Object(BUCKET, csvfile).download_file(
            f'/Users/zackkingbackup/Documents/Job Search/CapitalOne/'\
            +'sample-project-data-engineer/data/'+str(csvfile))
        download_loc = '/Users/zackkingbackup/Documents/Job Search/CapitalOne/'\
        +'sample-project-data-engineer/data/'+str(csvfile)
    else:
        s3_resource.Object(BUCKET, csvfile).download_file(
            f'/tmp/'+str(csvfile))
        download_loc = '/tmp/'+str(csvfile)
        
    ''' 
        Filename is the file you want to upload
        Key is the name of the file as it'll appear in your bucket
    '''
    s3_resource.Bucket(BUCKET).upload_file(
        Filename=download_loc, Key='sample-project/extract/'+str(QUERY_DATE)+'/'\
    +str(QUERY_DATE)+'-extract-output.csv')
    
    return


