#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 21:21:29 2019

This is the Transform Module for my ETL code.
It must satisfy the following contract:
    1. Accept a query_date, S3 resource instance, 
       local temp space, and a bucket name as inputs
    2. Read  s3://sample-project/extract/$QUERY_DATE/${QUERY_DATE}-extract-output.csv 
    3. Write the transformed file to
       s3://sample-project/transform/$QUERY_DATE/${QUERY_DATE}-transform-output.csv
       such that $BUCKET == mybucket1219

@author: zackkingbackup
"""

import pandas as pd
import os

def transform_name(name):
    '''
        transform_name(name)
            Transform a name from "First Last" to "LAST First"
            
            Private helper function
            
            Parameters
            ----------
            name : str
                The string contains the name in "First Last" format
                
            Returns
            -------
            result : str
                result contains the name in "LAST First" format
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
        transform_address(addr)
            Transform an address by replacing commas with spaces
            
            Private helper function
            
            Parameters
            ----------
            addr : str
                The string contains the address with commas
                
            Returns
            -------
            result : str
                result contains the address with spaces instead of commas
    '''
    return addr.replace(',',' ')

def transform(query_date, s3_resource,
              bucket='mybucket1219',
              local_temp='/tmp/'):
    '''
        transform(query_date, s3_resource,
                  bucket='mybucket1219',
                  local_temp='/tmp/')
            Transform all fields of the Extract Module's output csv
            according to the transform spec. Upload the transformed
            csv to sample-project/extract/$QUERY_DATE/${QUERY_DATE}-transform-output.csv
            
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
    
    download_loc = ''
    csvfile = 'extract-output.csv'
    vars = {'QUERY_DATE': query_date}
    download_from = os.path.join('sample-project',
                                 'extract',
                                 str(query_date),
                                 '{QUERY_DATE}-extract-output.csv'.format_map(vars))

    download_loc = os.path.join(local_temp, csvfile)
    s3_resource.Object(bucket, download_from).download_file(
        download_loc)

    
    ''' Read the extract output into a pandas.DataFrame '''
    df = pd.read_csv(download_loc)
    
    ''' Transform full_name to employee name via helper function. '''
    df['employee_name'] = df.apply(lambda x: transform_name(x['full_name']), 
                                   axis=1)
    
    ''' Email is a direct map to email_address, no helper needed. '''
    df['email_address'] = df['email']
    
    ''' 
        Replace all the commas with spaces to transform address
        into home_address via helper function.
    '''
    df['home_address'] = df.apply(lambda x: transform_address(x['address']), 
                                  axis=1)
    
    ''' 
        df contains all columns pre and post transformations;
        use the transformed only columns to create a DataFrame
        that pandas.to_csv can write out for upload to the S3 bucket.
    '''
    output_df = df[['employee_name','email_address','home_address']]
        
    output_loc = os.path.join(local_temp, "transformed.csv")
    output_df.to_csv(output_loc,index=False)
    
    vars = {'QUERY_DATE' : query_date}
    s3_resource.Bucket(bucket).upload_file(
        Filename=output_loc, 
        Key=os.path.join('sample-project',
                         'transform',
                         str(query_date),
                         '{QUERY_DATE}-transform-output.csv'.format_map(vars)))
        
    return