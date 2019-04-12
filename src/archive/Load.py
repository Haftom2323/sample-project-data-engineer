#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 20:53:16 2019

This is the Load Module for my ETL code.
It must satisfy the following contract:
    1. Accept a QUERY DATE, S3 resource instance, boolean
       telling function whether its being run locally or by
       an AWS Lambda, local temp space, and a bucket name as inputs
    2. read  s3://sample-project/transform/$QUERY_DATE/${QUERY_DATE}-transform-output.csv 
    3. write the unmodified file to
       s3://sample-project/load/$QUERY_DATE/${QUERY_DATE}.EMP.REC.LRF.csv
       such that $BUCKET == mybucket1219

@author: zackkingbackup
"""

def load_function(QUERY_DATE,s3_resource,LOCAL=False,
                     BUCKET='mybucket1219',
                     local_temp='/Users/zackkingbackup/Documents/Job Search/CapitalOne/'\
                     +'sample-project-data-engineer/data/'):

    download_loc = ''
    s3path = 'sample-project/transform/'+str(QUERY_DATE)+'/'+str(QUERY_DATE)
    csvfile = 'transform_output.csv'
        
    if LOCAL:
        ''' 
            TODO: change this long ugly path to something local to
            the run directory. Perhaps use the end-to-end script to
            make that local directory if it doesn't exist and clean it
            out if it does...
        '''
        s3_resource.Object(BUCKET, s3path+'-'+csvfile).download_file(
            f'/Users/zackkingbackup/Documents/Job Search/CapitalOne/'\
            +'sample-project-data-engineer/data/'+str(csvfile))
        download_loc = '/Users/zackkingbackup/Documents/Job Search/CapitalOne/'\
        +'sample-project-data-engineer/data/'+str(csvfile)
    else:
        s3_resource.Object(BUCKET, s3path+'-'+csvfile).download_file(
            f'/tmp/'+str(csvfile))
        download_loc = '/tmp/'+str(csvfile)
        
    ''' 
        Filename is the file you want to upload
        Key is the name of the file as it'll appear in your bucket
    '''
    s3_resource.Bucket(BUCKET).upload_file(
        Filename=download_loc, Key='sample-project/load/'+str(QUERY_DATE)+'/'\
    +str(QUERY_DATE)+'.EMP.REC.LRF.csv')
    
    return