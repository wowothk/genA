#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 01:00:10 2019

@author: rudi

decoding stage 1

"""
import numpy as np
from prosedur1 import decoding
from decoding_stage_2 import stage_2
import copy
class stage_1:
    def __init__(self, S, K, J, I, u, s, D, w, d, v1, v2, v3, t, c):
        self.S = S
        self.K = K
        self.D = D
        self.J = J
        self.I = I
        self.s = s
        self.t = t
        self.u = u 
#        self.a = a
        self.v1 =v1
        self.v2 = v2
        self.v3 = v3
        self.d = d
        self.w = w
        self.c = c
    def decode(self):
        b = np.array([[0]*len(self.S)]*len(self.K))
#        self, K, J, I,De, a, v2, d, w, v3
        stg_2 = stage_2(self.K, self.J, self.I, self.D, self.w, self.d, self.c, self.v2,  self.v3).decode()
        D_aksen = stg_2[1]
        f = stg_2[0]
        q = stg_2[2]
        p = stg_2[3]
        z = stg_2[4]
        capacityD = copy.deepcopy(self.D)
        for k in range(len(self.K)):
            capacityD[k] = self.u*D_aksen[k]
#        pros_1 = decoding(self.K, self.J, temp_q, temp_d, self.a ,self.v2)
        chromosom1=copy.deepcopy(self.v1)
        if len(self.v1) > len(self.S)+len(self.K):
            chromosom1.pop()
#        print("D   ", self.D)
        b = decoding(self.S, self.K, capacityD, self.s, self.t, chromosom1)[0]
        return b,f,q,p,z
    
#supplier = ["s1","s2","s3"]
#plant = ["p1","p2","p3"]
#dc = ["dc1","dc2","dc3","dc4"]
#customer =["cust1","cust2", "cust3","cust4"]
#
#sups =[250,200,250]
#D = [200,150,200] 
#W = [150, 100, 200, 100]
#d = [50, 100, 50, 100]
#
#c = np.array([[3,5,2,4],[6,2,5,1],[4,3,6,5],[2,4,3,2]])
#a = np.array([[5,2,4,3],[4,6,3,5],[3,5,1,6]])
#t = np.array([[4,3,1],[3,5,2],[1,6,4]])
#
#v2 =[4,5,6,8,3,2,7,1]
#v3 = [1,1,3,3,3]
#v1 =[3,7,4,2,6,5,1]
##stg_3 = stage_3(dc, customer, W, d, v3).decode()
##print(stg_3)
##(self, S, K, I, u, s, D, w, d, v1, v2, v3, t, c):
#p,qi,r=[2, 5, 7, 6, 1, 3, 4], [4, 8, 3, 2, 6, 5, 1, 7], [3, 3, 3, 4]
#
#stg_1 = stage_1(supplier,plant,dc,customer, 1, sups,D, W, d,[5, 7, 2, 1, 3, 4, 6], [3, 6, 4, 5, 1, 7, 2, 8], [3, 3, 1, 1, 3],t,a).decode()
#print(stg_1)

