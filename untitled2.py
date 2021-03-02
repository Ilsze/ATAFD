#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 20:58:41 2021

@author: carolineskalla
"""

a = [1,2,3,4,5]
print(a)

for agent in list(a):
    print(agent)
    if agent == 3 or agent == 1:
        a.remove(agent)
        
print(a)

