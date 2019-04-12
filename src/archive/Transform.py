#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 21:21:29 2019

This is the Transform Module for my ETL code.
It must satisfy the following contract:
    1. Accept a QUERY DATE, S3 resource instance, boolean
       telling function whether its being run locally or by
       an AWS Lambda, local temp space, and a bucket name as inputs
    2. read  s3://sample-project/extract/$QUERY_DATE/${QUERY_DATE}-extract-output.csv 
    3. write the transformed file to
       s3://sample-project/transform/$QUERY_DATE/${QUERY_DATE}-transform-output.csv
       such that $BUCKET == mybucket1219

@author: zackkingbackup
"""

import pandas as pd

def transform_name(name):
    '''
        TODO: document
    '''
    name = name.split()
    first_name = name[0]
    last_name = name[1].upper()
    
    return last_name+" "+first_name

'''
    I could do without this helper function and just use this in transform:
    df['home_address'] = df.apply(lambda x: x['address'].replace(',',' '), axis=1)
    
    but that wouldn't be very testable so I'll create transform_address
    to do the same thing.
'''
def transform_address(addr):
    '''
        TODO: document
    '''
    return addr.replace(',',' ')

def transform_function(QUERY_DATE,s3_resource,LOCAL=False,
                     BUCKET='mybucket1219',
                     local_temp='/Users/zackkingbackup/Documents/Job Search/CapitalOne/'\
                     +'sample-project-data-engineer/data/'):
    '''
        TODO: document
    '''
    
    download_loc = ''
    csvfile = 'extract-output.csv'
    s3path = 'sample-project/extract/'+str(QUERY_DATE)+'/'+str(QUERY_DATE)
    
    if LOCAL:
        s3_resource.Object(BUCKET, s3path+'-'+csvfile).download_file(
            f'/Users/zackkingbackup/Documents/Job Search/CapitalOne/'\
        +'sample-project-data-engineer/data/'+str(csvfile))
        download_loc = '/Users/zackkingbackup/Documents/Job Search/CapitalOne/'\
        +'sample-project-data-engineer/data/'+str(csvfile)
    else:
        s3_resource.Object(BUCKET, s3path+'-'+csvfile).download_file(
            f'/tmp/'+str(csvfile))
        download_loc = '/tmp/'+str(csvfile)
    
    ''' read the extract output into a pandas.DataFrame '''
    df = pd.read_csv(download_loc)
    
    ''' transform full_name to employee name via helper function '''
    df['employee_name'] = df.apply(lambda x: transform_name(x['full_name']), 
                                   axis=1)
    
    ''' email is a direct map to email_address, no helper needed '''
    df['email_address'] = df['email']
    
    ''' 
        replace all the commas with spaces to transform address
        into home_address via helper function
    '''
    df['home_address'] = df.apply(lambda x: transform_address(x['address']), 
                                  axis=1)
    
    ''' 
        df contains all columns pre and post transformations;
        use the transformed only columns to create a DataFrame
        that pandas.to_csv can write out for upload to the S3 bucket
    '''
    output_df = df[['employee_name','email_address','home_address']]
    
    output_loc = ''
    if LOCAL:
        output_df.to_csv(local_temp+"transformed.csv",index=False)
        output_loc = local_temp+"transformed.csv"
    else:
        output_df.to_csv('/tmp/transformed.csv')
        output_loc = '/tmp/transformed.csv'
    
    s3_resource.Bucket(BUCKET).upload_file(
        Filename=output_loc, 
        Key='sample-project/transform/'+QUERY_DATE+'/'+QUERY_DATE+'-transform_output.csv')

    return