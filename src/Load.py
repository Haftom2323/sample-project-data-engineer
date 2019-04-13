#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 20:53:16 2019

This is the Load Module for my ETL code.
It must satisfy the following contract:
    1. Accept a QUERY DATE, S3 resource instance, boolean
       telling function whether its being run locally or by
       an AWS Lambda, local temp space, and a bucket name as inputs
    2. Read  s3://sample-project/transform/$QUERY_DATE/${QUERY_DATE}-transform-output.csv 
    3. Write the unmodified file to
       s3://sample-project/load/$QUERY_DATE/${QUERY_DATE}.EMP.REC.LRF.csv
       such that $BUCKET == mybucket1219

@author: zackkingbackup
"""
import os

def load(query_date,s3_resource,
         bucket='mybucket1219',
         local_temp='/tmp/'):
    '''
        load(query_date,s3_resource,LOCAL=False,
             bucket='mybucket1219', local_temp='/tmp/')
            Upload the Transform Module's output csv
            to sample-project/load/$QUERY_DATE/${QUERY_DATE}.EMP.REC.LRF.csv
            
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
    csvfile = 'transform-output.csv'
    vars = {'QUERY_DATE': query_date}
    download_from = os.path.join('sample-project',
                                 'transform',
                                 str(query_date),
                                 '{QUERY_DATE}-transform-output.csv'.format_map(vars))
       
    download_loc = os.path.join(local_temp,csvfile)
    s3_resource.Object(bucket, download_from).download_file(
        download_loc)
    
    vars = {'QUERY_DATE': query_date}
    s3_resource.Bucket(bucket).upload_file(
        Filename=download_loc, 
        Key=os.path.join('sample-project',
                         'load',
                         str(query_date),
                         '{QUERY_DATE}.EMP.REC.LRF.csv'.format_map(vars)))
    
    return