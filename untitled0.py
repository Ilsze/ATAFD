#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 00:29:34 2021

@author: carolineskalla
"""

class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
    self.list = [1,2,3]

p1 = Person("John", 36)
print(p1.list)
p1.list.append(4)
print(p1.list)

print(p1.name)
print(p1.age)

def addEl(person):
    person.list.append(5)
addEl(p1)
   
print(p1.list)
    