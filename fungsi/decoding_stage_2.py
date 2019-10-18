#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 23:33:35 2019

@author: rudi

decoding stage 2

"""
import numpy as np
import random
import copy
from decoding_stage_3 import stage_3
from repair import repair_alg
from prosedur1 import decoding

class stage_2:
    def __init__(self, K, J, I,De, w, d, a, v2, v3):
        self.K = K
        self.J = J
        self.a = a
        self.v2 = v2
        self.I = I
        self.De = De
        self.v3 = v3
        self.d = d
        self.w = w
        
    def decode(self):
        D_aksen = [0]*len(self.K)
        D = [0]*len(self.K)
        temp_w = [0]*len(self.w)
        for i in range(len(self.w)):
            temp_w[i] = self.w[i]
#        print(self.J, self.I, temp_w, self.d, self.v3)
        stg_3= stage_3(self.J, self.I, temp_w, self.d, self.v3).decode()
#        print(stg_3)
#        w_aksen=stg_3[0]
        q=stg_3[1]
        z=stg_3[3]
#        Cd = stg_3[2]
        tot_dem = 0
        Pd = [0]*len(self.K)
        for j in range(len(self.J)):
            tot_dem = tot_dem + sum(q[j])
        tot_cap = 0
        p = [0]*len(self.K)
        for k in range(len(self.K)):
            tot_cap = tot_cap+ self.De[k]*p[k]
            Pd[k] = self.v2[k]
        Op = []
        Cp = [None]*len(self.K)
        for k in range(len(self.K)):
            Cp[k] = self.K[k]
            D[k] = self.De[k]
        Np = len(Op)
        P = 2
        
#        print('Pd   :',Pd ) #Kemungkinan Pdk ini salah 
#        print('q    :', q)
#        print("tot_cap  :", tot_cap)
#        print("tot_dem  :", tot_dem)
#        print("Cp   ", Cp)
#        print("D   ", D)
        while tot_cap < tot_dem and Np < P:
            hp_k = 0
            temp = 0
            for k in range(len(self.K)):
                if temp == 0 :
                    temp = Pd[k]
                    hp_k = k
                elif Pd[k] > temp:
                    temp = Pd[k]
                    hp_k = k
            p[hp_k] = 1
            tot_cap = tot_cap + D[hp_k]*p[hp_k]
            Op.append(self.K[hp_k])
#            Cp.remove(self.K[hp_k])
            Np = Np + 1
            Pd[hp_k] = 0
        Cp = list(set(self.K)-set(Op))
        
#        print("Op   ",Op)
#        print("tot_cap  :", tot_cap)
#        print("Cp    ", Cp)
        #kesalahan lain adalah pada permasalahn ini tot_cap tidak bisa unique
        
        
        
        chromosom2 = copy.deepcopy(self.v2)
        if len(Cp) != 0:
            for e in range(len(Cp)):
                chromosom2[self.K.index(Cp[e])] = 0
        
        while len(Op) > P or tot_cap < tot_dem: # disini kemungkinan ada kres antara Op (value atau stringnya)
#            temp_k = np.array(self.K)
#            temp_op = np.array(Op)
            index_op =[]
            for i in range(len(Op)):
                index_op.append(self.K.index(Op[i]))
            
            dok =[]
            for x in range(len(index_op)):
                dok.append(D[index_op[x]])
            dck = list(set(D) -set(dok))

            dop = len(dok)
            dp = P
            d_tot_cap = tot_cap
            d_tot_dem = tot_dem
            dok = repair_alg(dok, dck, dp, dop, d_tot_cap, d_tot_dem)
            # dalam hal ini dok adalah yang terbuka
            Op  = []
            p = [0]*len(self.K)
            tot_cap = sum(dok)
            temp_dok = np.array(dok)
            temp_De = np.array(self.De)
            for k in range(len(dok)):
                Op.append(self.K[self.De.index(dok[k])])
                if len(np.where(temp_dok == temp_De)[0]) > 1:
                    for x in range(len(np.where(temp_dok == temp_De)[0])):
                        p[np.where(temp_dok == temp_De)[0][x]] = 1        
                else:
                    p[self.De.index(dok[k])] = 1
        
        if len(self.v2) > len(self.K)+len(self.J):
            chromosom2.pop()
        temp_d=[0]*len(self.K)
        temp_we=[0]*len(self.w)
        for k in range(len(self.K)):
            temp_d[k] = D[k]*p[k]
        for j in range(len(self.w)):
            temp_we[j] = self.w[j]*z[j]
#        print(temp_d)
#        print(temp_we)
#        print(chromosom2)
        temp_q=[0]*len(self.w)
        for j in range(len(self.w)):
            temp_q[j] = sum(q[j])
        pros_1 = decoding(self.K, self.J, temp_q, temp_d, self.a ,chromosom2)
        f = pros_1[0]
        D_aksen = pros_1[1]
        return  f, D_aksen, q, p,z
        ## masalah terakhir adalah total kapasitas kurang dari total permintaan
        # dan plant yang dapat berfungsi ketika kapasitasnya memiliki kapasitas yang sama

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
#
#v2 =[4,5,6,8,3,2,7,1]
#v3 = [1,1,3,3,3]
##stg_3 = stage_3(dc, customer, W, d, v3).decode()
##print(stg_3)
#print(W)
#stg_2 = stage_2(plant,dc,customer, D, W, d,a,[2, 8, 1, 3, 7, 7, 5, 4], [3, 3, 3, 4]).decode()
#print(stg_2)

            
            
                  
