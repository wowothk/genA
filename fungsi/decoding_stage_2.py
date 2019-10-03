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
    def __init__(self, K, J, I,De, a, v2, d, w, v3):
        self.K = K
        self.J = J
#        self.p = p
        self.a = a
        self.v2 = v2
        self.I = I
        self.De = De
        self.v3 = v3
        self.d = d
        self.w = w
        
    def decode(self):
#        f = np.array([[0]*self.J]*self.K)
        D_aksen = [0]*len(self.K)
        D = [0]*len(self.K)
        temp_w = [0]*len(self.w)
#        print("Iki w yalllll hehe", self.w)
        for i in range(len(self.w)):
            temp_w[i] = self.w[i]
        stg_3= stage_3(self.J, self.I, temp_w, self.d, self.v3).decode()
#        print("Iki w yalllll", temp_w)
#        print(self.J)
#        print("Iki w yalllll hehe", self.w)
        w_aksen=stg_3[0]
        q=stg_3[1]
        z=stg_3[3]
#        Cd = stg_3[2]
        tot_dem = 0
        Pd = [0]*len(self.K)
        for k in range(len(self.K)):
            tot_dem = tot_dem + sum(q[k])
            Pd[k] = self.v2[k]
        tot_cap = 0
        p = [0]*len(self.K)
        for k in range(len(self.K)):
            tot_cap = tot_cap+ self.De[k]*p[k]
        Op = []
        Cp = [None]*len(self.K)
        for k in range(len(self.K)):
            Cp[k] = self.K[k]
            D[k] = self.De[k]
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
            p[hp_k] = 1
            tot_cap = tot_cap + D[hp_k]*p[hp_k]
            Op.append(self.K[hp_k])
#            Cp.remove(self.K[hp_k])
            Np = Np + 1
            Pd[hp_k] = 0
        Cp = list(set(self.K)-set(Op))
        if len(Cp) != 0:
            for e in range(len(Cp)):
                self.v2[self.K.index(Cp[e])] = 0
#        
#        for s in range(len(self.K)):
#          for e in range(len(Cp)):
#              if Cp[e] == self.v2[s]: #dalam hal ini s harus kurang dari len(self.K)
#                  self.v2[s] = 0
#        print('D    ',D)
        while len(Op) > P or tot_cap < tot_dem: # disini kemungkinan ada kres antara Op (value atau stringnya)
#            dok = Op
#            dck = Cp
#            dop = Np
#            dp = P
#            d_tot_cap =tot_cap
#            d_tot_dem = tot_dem 
#            Op = repair_alg(dok, dck, dp, dop, d_tot_cap, d_tot_dem)
            
            
            temp_k = np.array(self.K)
            temp_op = np.array(Op)
            index_op = np.where(temp_k == temp_op)
#            print("index  ", index_od)
            dok =[]
            for x in range(len(index_op[0])):
                dok.append(D[index_op[0][x]])
#            print('dok    ', dok)
            dck = list(set(D) -set(dok))
#            print('dck    ', dck)
#            dok = Od
#            print('dok     ', dok)
            dop = len(dok)
            dp = P
            d_tot_cap = tot_cap
            d_tot_dem = tot_dem
            
#            print('tot_cap   ', tot_cap)
#            print('tot_dem   ', tot_dem)
            dok = repair_alg(dok, dck, dp, dop, d_tot_cap, d_tot_dem)
            # dalam hal ini dok adalah yang terbuka
#            Op = dok
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
            
#            k = list(set(Op) - set(dok))
       #panggil prosedur 1
#        temp_j = [0]*len(self.J)
#        for  j in range(len(self.J)):
#            temp_j[j] = self.J[j]
#        dummy = 0
        if len(self.v2) > len(self.K)+len(self.J):
            self.v2.pop()
#            temp_j.append('dummy')
#            temp_c= np.append(self.a,np.array([[0]*len(self.K)]).T, 1)
#        print('k   ', self.K)
#        print('j    ', self.J)
#        print('w    ', self.w)
        print('z    ', z)
#        print('tot_cap   ', tot_cap)
#        print('tot_dem   ', tot_dem)
        
        temp_d=[0]*len(self.K)
        temp_we=[0]*len(self.w)
        for k in range(len(self.K)):
            temp_d[k] = D[k]*p[k]
        for j in range(len(self.w)):
            temp_we[j] = self.w[j]*z[j]
        temp_q=[0]*len(self.w)
        for j in range(len(self.w)):
            temp_q[j] = sum(q[j])
#        if tot_cap > tot_dem:
#            dummy = tot_cap-tot_dem
#            temp_we.append(dummy)
#        print('k   ', self.K)
        print('p    ', p)
#        print('temp we   ', temp_we)
#        print('temp_d    ', temp_d)#temporary for D as capacity of plant
#        print('temp_q    ', temp_q)
#        print('Op     ', Op)
        pros_1 = decoding(self.K, self.J, temp_q, temp_d, self.a ,self.v2)
        f = pros_1[0]
        D_aksen = pros_1[1]
#        print("f ", f)
#        print("D aksen   ", D_aksen)
        return f, D_aksen   
        ## masalah terakhir adalah total kapasitas kurang dari total permintaan
        # dan plant yang dapat berfungsi ketika kapasitasnya memiliki kapasitas yang sama

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

v2 =[4,5,6,8,3,2,7,1]
v3 = [0,0,2,2,2]
#stg_3 = stage_3(dc, customer, W, d, v3).decode()
#print(stg_3)
stg_2 = stage_2(plant,dc,customer, D, a,v2, d, W,v3).decode()
print(stg_2)
            
            
                  
