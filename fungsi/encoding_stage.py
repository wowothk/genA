#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 12:09:18 2019

@author: rudi
encoding susahnya stage 2
"""
import random
import numpy as np
import sys
sys.path.insert(0, '/home/rudi/Documents/skripsi')
from susahnya_stage2 import create
from encode import priority_based_enc
from prosedur1 import decoding

supplier = ["s1","s2","s3"]
plant = ["p1","p2","p3"]
dc = ["dc1","dc2","dc3","dc4"]
customer =["cust1","cust2", "cust3","cust4"]

sups =[250,200,250]
D = [200,150,200] 
W = [150, 100, 200, 100]
d = [50, 100, 50, 100]

t = np.array([[4,3,1,100],[3,5,2,100],[1,6,4,100]])
stage_satu = create(supplier, plant, dc, customer, sups, D, W, d, 2, 2).supplier_to_plant()
b=stage_satu[0]
print(b)
b_aksen=np.array([[None]*len(plant)]*len(supplier))
f_aksen = stage_satu[1]
temp_plant = stage_satu[4]
temp_k =[0]*len(plant)
temp_k_aksen =[0]*len(plant)
print(f_aksen)
for k in range(len(plant)):
    temp_k[k] = sum(f_aksen[k])
    temp_k_aksen[k] = sum(f_aksen[k])    
for s in range(len(supplier)):
    for k in range(len(plant)):
        b_aksen[s][k]=b[s][k]
temp = [0]*len(supplier)
for s in range(len(supplier)):
    if sups[s] - sum(b[s]) > 0:
        temp[s] = sups[s] - sum(b[s])
if sum(temp) != 0:
#        temp_plant.append("dummy")
    temp_k.append(sum(temp))
    b_aksen = np.append(b_aksen, np.array([temp]).T,1)
#    print('nilai p  ', p)
print(b_aksen)


print("====")


#temp_k = stage_satu[5]

t_aksen = np.array([[4,3,1],[3,5,2],[1,6,4]])
#print(b_aksen)
#print(temp_plant)
print(temp_k)
#def __init__(self, sources, depot, a, b, c, g,P):
v=priority_based_enc(supplier, temp_plant, sups, temp_k, t,b_aksen,2).encoding()
print(v)

print(decoding(supplier, temp_plant, temp_k, sups, t ,v))