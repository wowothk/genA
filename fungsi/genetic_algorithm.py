#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 15:32:21 2019

@author: rudi
"""

import numpy as np
pop1 = [3,7,4,2,8,5,1,4,5,6,8,3,2,7,1,1,3,3,3]
pop2 = [1,4,5,6,7,3,2,8,1,3,5,7,6,4,2,1,3,2,2]

supplier = ["s1","s2","s3"]
plant = ["p1","p2","p3"]
dc = ["dc1","dc2","dc3","dc4"]
customer =["cust1","cust2", "cust3","cust4"]

sups =[250,200,250]
D = [200,150,200] 
W = [150, 100, 200, 100]
d = [50, 100, 50, 100]

c = np.array([[3,5,2,4],[6,2,5,1],[4,3,6,5],[2,4,3,2]])
a = np.array([[5,2,4,3],[4,6,3,5],[3,5,1,6]])
t = np.array([[4,3,1],[3,5,2],[1,6,4]])

z = [1, 0, 1, 0]
p = [1, 1, 0]
temp_w = [0]*len(z)
temp_d =[0]*len(p)
for i in range(len(D)):
    temp_d[i] = D[i]*p[i]
for j in range(len(W)):
    temp_w[j] = W[i]*z[i]
    
def spare(chromosom, sups, W, D, d):
    if sum(sups) - sum(D) > 0:
        len_v1=len(sups)+len(D)+1
    else:
        len_v1=len(sups)+len(D)
    v1=[0]*len_v1
    if sum(D) - sum(W)>0:
        len_v2=len(W)+len(D)+1
    else:
        len_v2=len(W)+len(D)
    v2=[0]*len_v2
    
    if sum(W) - sum(d)>0:
        len_v3=len(d)+1
    else:
        len_v3=len(d)
#    print('total ', len(d))
#    print(sum(temp_w))
#    print(sum(d))
#    print(len_v3)
    v3 = [0]*len_v3
        
    for x in range(len(chromosom)):
        if x < len_v1:
            v1[x]=chromosom[x]        
        elif len_v1 <= x and x < len_v1+len_v2:
            v2[x%len_v1] = chromosom[x]
        else:
            v3[x%(len_v1+len_v2)] = chromosom[x]
    return v1, v2, v3

def crossover(chromosom1, chromosom2, sups, W, D, d):
    parent1 = list(spare(chromosom1, sups, W, D, d))
    parent2 = list(spare(chromosom2, sups, W, D, d))
    temp=0
    for i in range(len(parent1)):
        if i%2 != 0:
            temp = parent1[i]
            parent1[i] = parent2[i]
            parent2[i] = temp
    return parent1, parent2

spr = spare(pop1, sups, W, D, d)
v1=spr[0]
v2=spr[1]
v3=spr[2]
print(len(spr))
print(v1)
print(v2)
print(v3)

silang=crossover(pop1, pop2, sups, W, D, d)
print('parent 1  :',silang[0])
print('parent 2  :',silang[1])
#print('v1: ', v1, 'v2: ', v2, 'v3: ', v3)