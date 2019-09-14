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
        Cd = [0]*len(self.J)
        for j in range(len(self.J)):
            Cd[j] = self.J[j]
        q = np.array([[0]*len(self.J)]*len(self.I))
        w_aksen = [0]*len(self.J) # total banyaknya demand untuk product J
        
        for i in range(len(self.I)):
            z[self.v[i]] = 1
            y[self.v[i]][i] = 1
            Od.append(self.J[self.v[i]])
            Cd.remove(self.J[self.v[i]])
        tot_cap = 0
        for j in range(len(self.J)):
            tot_cap = tot_cap+ self.w[j]*z[j]
        tot_dem = 0
        for i in range(len(self.I)):
            tot_dem = tot_dem + self.d[i]
        if len(Od) <= len(self.w) and tot_cap >= tot_dem:
            for i in range(len(self.I)):
                q[self.v[i]][i] = self.d[i]
                self.w[self.v[i]] = self.w[self.v[i]] - q[self.v[i]][i]
                w_aksen[self.v[i]] = self.w_aksen[self.v[i]] + q[self.v[i]][i]
                self.d[i] = 0
            temp = []
            for j in range(len(self.J)):
                if self.w[j] < 0:
                    for i in range(len(self.I)):
                        if y[j][i] != 0:
                            temp.append(i)
                k = random.randint(0, len(temp)-1)
                y[j][k] = 0 
                self.w[j] = self.w[j] + q[j][k]
                w_aksen[j] = self.w_aksen[j] - q[j][k]
                for je in range(len(self.J)):
                    if je != j :
                        self.w[je] = self.w[je] - q[je][k]
                        if self.w[j] >= 0:
                            y[j][k] = 1
#                            self.w[j] = self.w[j] - q[j][k]
                            w_aksen[j] = self.w_aksen[j] + q[j][k]
                            self.v[k] = je
                            q[je][k] = self.d[k]
                        else:
                            self.w[je] = self.w[je] + q[je][k]
                                                                     
                return w_aksen, q, Cd
        else:
            dok = Od
            dck = Cd
            dop = len(dok)
            dp = 3
            d_tot_cap = tot_cap
            d_tot_dem = tot_dem
            dok = repair_alg(dok, dck, dp, dop, d_tot_cap, d_tot_dem)
            k = list(set(Od) - set(dok))
            for j in range(len(Od)):
                for p in range(len(k)):
                    if Od[j] == k[p]:
                        for i in range(len(self.I)):
                            y[j][i] =0
                            r = random.randint(0, len(Od)-1)
                            self.v[i] = Od[r]
            stage_3(self.J, self.I, self.w, self.d, self.v)