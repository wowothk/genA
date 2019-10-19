#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 21:27:15 2019

@author: rudi

Decoding stage 3

"""
import numpy as np
import random
import copy
from repair import repair_alg
class stage_3:
    def __init__(self, J, I, w, d, v):
        self.J = J
        self.I = I
        self.w = w
        self.d = d
        self.v = v
    
    def decode(self):
        z = [0]*len(self.J)
        y = np.array([[0]*len(self.J)]*len(self.I))
        customerDemand = copy.deepcopy(self.d)
        Od = []
        Cd = [None]*len(self.J)
        for j in range(len(self.J)):
            Cd[j] = self.J[j]
        q = np.array([[0]*len(self.J)]*len(self.I))
        w_aksen = [0]*len(self.J) # total banyaknya demand untuk product J
        temp = []
        chromosom=copy.deepcopy(self.v)
        capacityW=copy.deepcopy(self.w)
        for k in range(len(self.v)):
            chromosom[k] = chromosom[k]-1
        if len(self.v)>len(self.d):
            chromosom.pop()            
        for i in range(len(self.I)):
            z[chromosom[i]] = 1
            y[chromosom[i]][i] = 1  
            Od.append(self.J[chromosom[i]])
        Cd = list(set(self.J)-set(Od))
        tot_cap =0
        for j in range(len(self.J)):
            tot_cap = tot_cap+ capacityW[j]*z[j]
        tot_dem = 0
        for i in range(len(self.I)):
            tot_dem = tot_dem + self.d[i]
#        maks_od=2
#        print(Od)
        if len(Od) <= len(capacityW) and tot_cap >= tot_dem:
            for i in range(len(self.I)):
                q[chromosom[i]][i] = self.d[i]
                capacityW[chromosom[i]] = capacityW[chromosom[i]] - q[chromosom[i]][i]
                w_aksen[chromosom[i]] = w_aksen[chromosom[i]] + q[chromosom[i]][i]
                customerDemand[i] = 0
            temp = []
            for j in range(len(self.J)):
                if self.w[j] < 0:
                    for i in range(len(self.I)):
                        if y[j][i] != 0:
                            temp.append(i)
                    k = random.randint(0, len(temp)-1)
                    y[j][temp[k]] = 0 
                    capacityW[j] = capacityW[j] + q[j][temp[k]]
                    w_aksen[j] = w_aksen[j] - q[j][temp[k]]
                    for je in range(len(self.J)):
                        if je != j :
                            capacityW[je] = capacityW[je] - q[je][temp[k]]
                            if capacityW[j] >= 0:
                                y[j][temp[k]] = 1
                                w_aksen[j] = w_aksen[j] + q[j][temp[k]]
                                capacityW[temp[k]] = je
                                q[je][temp[k]] = self.d[temp[k]]
                            else:
                                capacityW[je] = capacityW[je] + q[je][temp[k]]
            return w_aksen, q, Cd, z
        else:
            temp_j = np.array(self.J)
            temp_od = np.array(Od)
            index_od = np.where(temp_j == temp_od)
            dok =[]
            for x in range(len(index_od[0])):
                dok.append(capacityW[index_od[0][x]])
            dck = list(set(capacityW) -set(dok))

            dop = len(dok)
            dp = 2
            d_tot_cap = tot_cap
            d_tot_dem = tot_dem
            dok = repair_alg(dok, dck, dp, dop, d_tot_cap, d_tot_dem)
            Od = []
            for x in dok:
                Od.append(self.J[self.w.index(x)])
            Cd = list(set(self.J)-set(Od))
#            print(k)
            temp_capacity=copy.deepcopy(capacityW)            
            for i in range(len(temp_capacity)):
                for x in Cd:
                    if i == self.J.index(x):
                        temp_capacity[i] = 0
            for i in range(len(chromosom)):
                for j in range(len(temp_capacity)):
                    if temp_capacity[j] >= self.d[i]:
                        chromosom[i] = j+1
                        temp_capacity[j] = temp_capacity[j] - self.d[i]                          
            return stage_3(self.J, self.I, capacityW, self.d, chromosom).decode()
            
#    
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
#
#v3 = [1,1,3,3,3]
##print(d)
#stg_3 = stage_3(dc, customer, W, d, [3, 3, 3,3]).decode()
#print(stg_3)
