#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 22:24:41 2021

@author: carolineskalla
"""

"""
Iterating through list: I think when Python iterates through a list, it is tracking the index, so it will look at 
index 0, 1, 2.... When you delete elements, the indexes adjust to fit the new size of the list, so the iteration will
delete an element at index 0, but then the element that was at index 1 will now be at 0, but the iteration process will
not know to go back and look at the element that is now at index 0 which hasn't been considered yet. So this is only
a problem when elements are going to be deleted.'
"""

#problem
list = [1,2,3,4,5]

for agent in list:
    print(agent)
    list.remove(agent)
    print(list)
    
    
print("/n")
#fix
list2 = [1,2,3,4,5]

index = 0

print("list2: ", list2)
#0-length list2 - 1
for i in range(len(list2)):
    agent = list2.pop()
    print(agent)
    if(i % 2 == 0):
        list2.insert(0, agent)
print(list2)

print("/n")
#fix
list3 = [1,2,3,4,5]

index = 0

print("list3: ", list3)
#0-length list2 - 1
for i in range(len(list3)):
    agent = list3[index]
    print(agent)
    if(i % 2 == 0):
        #remove this agent
        list3.pop(index)
    else:
        index += 1
print(list3)