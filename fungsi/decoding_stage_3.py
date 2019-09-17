#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 21:27:15 2019

@author: rudi

Decoding stage 3

"""
import numpy as np
import random
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
        Od = []
        Cd = [None]*len(self.J)
        for j in range(len(self.J)):
            Cd[j] = self.J[j]
        q = np.array([[0]*len(self.J)]*len(self.I))
        w_aksen = [0]*len(self.J) # total banyaknya demand untuk product J
#        print("Cd   ", Cd)
#        print("J   ", self.J)
        temp = []
        for i in range(len(self.I)):
#            print(i)
#            print("Od   ",Od)
#            print("Cd    ", Cd)
            z[self.v[i]] = 1
            y[self.v[i]][i] = 1
#            print("Self.J[v[i]]  ", self.J[self.v[i]])        
            Od.append(self.J[self.v[i]])
#            Cd.remove(self.J[self.v[i]])
        Cd = list(set(self.J)-set(Od))
        tot_cap =0
        for j in range(len(self.J)):
            tot_cap = tot_cap+ self.w[j]*z[j]
        tot_dem = 0
        for i in range(len(self.I)):
            tot_dem = tot_dem + self.d[i]
        if len(Od) <= len(self.w) and tot_cap >= tot_dem:
            for i in range(len(self.I)):
                q[self.v[i]][i] = self.d[i]
                self.w[self.v[i]] = self.w[self.v[i]] - q[self.v[i]][i]
                w_aksen[self.v[i]] = w_aksen[self.v[i]] + q[self.v[i]][i]
                self.d[i] = 0
            temp = []
            for j in range(len(self.J)):
                if self.w[j] < 0:
                    for i in range(len(self.I)):
                        if y[j][i] != 0:
                            temp.append(i)
                    k = random.randint(0, len(temp)-1)
                    y[j][temp[k]] = 0 
                    self.w[j] = self.w[j] + q[j][temp[k]]
                    w_aksen[j] = w_aksen[j] - q[j][temp[k]]
                    for je in range(len(self.J)):
                        if je != j :
                            self.w[je] = self.w[je] - q[je][temp[k]]
                            if self.w[j] >= 0:
                                y[j][temp[k]] = 1
    #                            self.w[j] = self.w[j] - q[j][k]
                                w_aksen[j] = w_aksen[j] + q[j][temp[k]]
                                self.v[temp[k]] = je
                                q[je][temp[k]] = self.d[temp[k]]
                            else:
                                self.w[je] = self.w[je] + q[je][temp[k]]
#            print("Nilai W,  ", self.w)
#            print("Nilai z   ", z)
#            print("Nilai y   ", y)
#            print("Nilai q   ", q)
#            print("================")
            return w_aksen, q, Cd, z
        else:
            temp_j = np.array(self.J)
            temp_od = np.array(Od)
            index_od = np.where(temp_j == temp_od)
#            print("index  ", index_od)
            dok =[]
            for x in range(len(index_od[0])):
                dok.append(self.w[index_od[0][x]])
#            print('dok    ', dok)
            dck = list(set(self.w) -set(dok))
#            print('dck    ', dck)
#            dok = Od
#            print('dok     ', dok)
            dop = len(dok)
            dp = 3
            d_tot_cap = tot_cap
            d_tot_dem = tot_dem
            
#            print('tot_cap   ', tot_cap)
#            print('tot_dem   ', tot_dem)
            dok = repair_alg(dok, dck, dp, dop, d_tot_cap, d_tot_dem)
            k = list(set(self.w) - set(dok))
            for j in range(len(Od)):
                for p in range(len(k)):
                    if Od[j] == k[p]:
                        for i in range(len(self.I)):
                            y[j][i] =0
                            r = random.randint(0, len(Od)-1)
                            index = np.where(temp_od[r] == temp_j)[0]
                            rand = random.randint(0, len(index)-1)
                            self.v[i] = self.w[index[rand]]
                            
#            print(type(self.v[0]))
            stage_3(self.J, self.I, self.w, self.d, self.v).decode()
            
    
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
#c = np.array([[3,5,2,4,0],[6,2,5,1,0],[4,3,6,5,0],[2,4,3,2,0]])
#
#v3 = [0,0,2,2,2]
#stg_3 = stage_3(dc, customer, W, d, v3).decode()
#print(stg_3)
