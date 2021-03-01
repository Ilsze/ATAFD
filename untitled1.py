#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 17:14:58 2021

@author: carolineskalla
"""
DEBUG = False

def log(s):
    if DEBUG:
        print(s)

def main():
    log("the number "+ str(2))
    
main()