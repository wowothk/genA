#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 23:33:35 2019

@author: rudi

decoding stage 2

"""
import numpy as np
import random
from decoding_stage_3 import stage_3
from repair import repair_alg
from prosedur1 import decoding

class stage_2:
    def __init__(self, K, J, I, p, c, v2, d, w, v3):
        self.K = K
        self.J = J
        self.p = p
        self.c = c
        self.v2 = v2
        self.I = I
        self.v3 = v3
        self.d = d
        self.w = w
        
    def decode(self):
#        f = np.array([[0]*self.J]*self.K)
        D_aksen = [0]*len(self.K)
        D = [0]*len(self.K)
        stg_3= stage_3(self.J, self.I, self.w, self.d, self.v3).decode()
        q=stg_3[1]
#        Cd = stg_3[2]
        tot_dem = 0
        Pd = [0]*len(self.K)
        for k in range(len(self.K)):
            tot_dem = tot_dem + sum(q[k])
            Pd[k] = self.v2[k]
        tot_cap = 0
        for k in range(len(self.K)):
            tot_cap = tot_cap+ self.D[k]*self.p[k]
        Op = []
        Cp = [None]*len(self.K)
        for k in range(len(self.K)):
            Cp[k] = self.K[k]
            D[k] = self.K[k]
        Np = len(Op)
        P = 2
        while tot_cap < tot_dem and Np < P:
            hp_k = 0
            temp = 0
            for k in range(len(self.K)):
                if temp == 0 :
                    temp = Pd[k]
                    hp_k = k
                elif Pd[k] < temp:
                    temp = Pd[k]
                    hp_k = k
            self.p[hp_k] = 1
            tot_cap = tot_cap + D[hp_k]
            Op.append(self.K[hp_k])
            Cp.remove(self.K[hp_k])
            Np = Np + 1
            Pd[hp_k] = 0
        for s in range(len(self.v2)):
          for e in range(len(Cp)):
              if Cp[e] == self.v2[s]:
                  self.v2[s] = 0
        while Op > P or tot_cap < tot_dem: # disini kemungkinan ada kres antara Op (value atau stringnya)
            dok = Op
            dck = Cp
            dop = Np
            dp = P
            d_tot_cap =tot_cap
            d_tot_dem = tot_dem 
            Op = repair_alg(dok, dck, dp, dop, d_tot_cap, d_tot_dem)
       #panggil prosedur 1
        f = decoding(self.K, self.J, D, self.w, self.c ,self.v2)
        return f   
    
            
            
            
            
                  
