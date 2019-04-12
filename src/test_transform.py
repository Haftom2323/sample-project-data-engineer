#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 00:08:32 2019

@author: zackkingbackup
"""
import Transform as T

def test_name():
    input_name = "Arnoldo Ross"
    assert T.transform_name(input_name) == "ROSS Arnoldo"
    
def test_addr():
    input_addr = "878 Stone, Marquette, Utah, GP 29244"
    assert (T.transform_address(input_addr) == 
            "878 Stone  Marquette  Utah  GP 29244")