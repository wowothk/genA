#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 20:02:29 2019

@author: rudi
"""

from genetic_algorithm import enc_pop
from decoding_stage_1 import stage_1
import numpy as np
import sys
sys.path.insert(0, '/home/rudi/Documents/skripsi')
from encode import priority_based_enc
from prosedur1 import decoding
supplier = ["s1","s2","s3"]
plant = ["p1","p2","p3"]
plant1 = ["p1","p2","p3","dummy"]
dc = ["dc1","dc2","dc3","dc4"]
customer =["cust1","cust2", "cust3","cust4"]

sups =[250,200,250]
D = [200,150,200] 
W = [150, 100, 200, 100]
d = [50, 100, 50, 100]

t = np.array([[4,3,1],[3,5,2],[1,6,4]])
cost=np.array([[1,6,5,2],[6,2,4,5],[3,4,2,1]])
t1 = np.array([[4,3,1,0],[3,5,2,0],[1,6,4,0]])
t2 = np.array([[4,3,1,100],[3,5,2,100],[1,6,4,100]])
a = np.array([[5,2,4,3],[4,6,3,5],[3,5,1,6]])
c = np.array([[3,5,2,4],[6,2,5,1],[4,3,6,5],[2,4,3,2]])
individu=[(np.array([[ 50,   0,   0],
         [  0,   0,   0],
         [150, 100,   0]]), np.array([[  0,   0, 200,   0],
         [  0,   0,   0, 100],
         [  0,   0,   0,   0]]), np.array([[  0,   0,   0,   0],
         [  0,   0,   0,   0],
         [ 50, 100,  50,   0],
         [  0,   0,   0, 100]]), [1, 1, 0], np.array([0, 0, 1, 1]))]

#chromosom = enc_pop(individu, supplier, plant, dc, customer, sups, D, W, d, t, a, c)
#print(chromosom)
#decode_chromosom = stage_1(supplier, plant, dc, customer, 1, sups, D, W, d, chromosom[0][0],chromosom[0][1],chromosom[0][2], t, a).decode()
#print(decode_chromosom)

temp=[[ 50,   0,   0],
         [  0,   0,   0],
         [150, 100,   0]]
temp1=[[ 50,   0,   0,200],
         [  150,   0,   0,50],
         [0, 100,   0,150]]
temp2=[[50,0,50,0],
       [0,100,0,0],
       [0,50,50,50]]
sumber =[100,100,150]
tujuan =[50,150,100,50]
print(temp2)
pengkodean =priority_based_enc(supplier, plant1, sumber,tujuan,cost,temp2).encoding()
print(pengkodean)
print(decoding(supplier, plant1, tujuan, sumber, cost ,pengkodean))

