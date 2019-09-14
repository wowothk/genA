#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 01:44:43 2019

@author: rudi
"""

### Encoding stage 1 #####
#S : set of suppliers
#K : set of plants
#D : total customer demand
#t : unit transportation cost
#a : the amount of raw material
#b : the amount of raw material that have to shipment
import random
import numpy as np

class prosedur2:
    def __init__(self, S, K, a, b, c, g):
        self.S = S
        self.K = K
        self.a = a
        self.b = b
        self.c = c
        self.g = g
    def encode(self):
        temp_sources = [None]*len(self.S)
        temp_depot= [None]*len(self.K)
        for s in range(len(self.S)):
            temp_sources[s] = self.a[s]
    
        for k in range(len(self.K)):
            temp_depot[k]=self.b[k]
    
        v = [None]*(len(self.K)+len(self.S))
        prio = len(self.S)+len(self.K)
        i=0
        index=[0,0]
        while temp_depot[index[1]] != 0 or temp_sources[index[0]] != 0:
            i=i+1
            if i > len(self.K)+len(self.S):
                break
            print(i)
            temp_c = 0 
            for s in range(len(self.S)):
                for k in range(len(self.K)):
                    if self.g[s][k] != 0 and (temp_depot[k] == self.g[s][k] or temp_sources[s]==self.g[s][k]):
                        if temp_c == 0:
                            temp_c=self.c[s][k]
                            index[0] = s
                            index[1] = k
                        elif self.c[s][k] < temp_c:
                            temp_c = self.c[s][k]
                            index[0] = s
                            index[1] = k
            temp_depot[index[1]] = temp_depot[index[1]]-self.g[index[0]][index[1]]
            temp_sources[index[0]] = temp_sources[index[0]]-self.g[index[0]][index[1]]                
            if temp_depot[index[1]] == 0 :
                v[len(self.S)+index[1]] = prio
                prio = prio-1
                self.g[index[0]][index[1]] = 0
            if  temp_sources[index[0]] == 0 :
                v[index[0]] = prio
                prio = prio-1
                self.g[index[0]][index[1]] = 0
        for l in range(prio):
            t = random.randint(0, len(temp_depot)+len(temp_sources)-1)
            while v[t] != None:
                t = random.randint(0, len(temp_depot)+len(temp_sources)-1)
            v[t] = l+1
        return v
        
class enc_stage_1:
    def __init__(self, S, K, a, b, c, g, P):
        self.S = S
        self.K = K
        self.a = a
        self.b = b
        self.c = c
        self.g = g
        self.P = P
    
    def encoding(self):
        Op = [0]*len(self.K)
        for k in range(len(self.K)):
            Op[k] = self.K[k]
        Cp = []
        p = [1]*len(self.K)
        while len(Op) > self.P:
            r = random.randint(0,len(Op)-1)
            p[r] = 0
            Cp.append(Op[r])
            Op.remove(Op[r])
        temp = [0]*len(self.S)
        for s in range(len(self.S)):
            for k in range(len(self.K)):
                if p[k]==0:
                    temp[s] = temp[s] + self.g[s][k]
                    self.g[s][k] = 0
        self.K.append("dummy")
        self.g = np.append(self.g, np.array([temp]).T,1)
        self.c = np.append(self.c, np.array([[0]*len(self.S)]).T,1)
        self.b.append(sum(temp))
        
        v = prosedur2(self.S, self.K, self.a, self.b, self.c, self.g).encode()
        return v, Op, Cp, p, self.P    

class enc_stage_2:
    def __init__(self, K, J, Op, Cp, p, a, b, c, g, P):
        self.K = K
        self.J = J
        self.Op = Op
        self.Cp = Cp
        self.p = p
        self.a = a
        self.b = b
        self.c = c
        self.g = g
        self.P = P
    def encoding(self):
        z=[1]*len(self.J)
        Od= [0]*len(self.J)
        Cd=[]
        if len(self.K) > len(self.p):
            self.K.remove("dummy")
            del self.a[-1]
#        print("+++++")
#        print(self.K)
#        print(self.a)
        for j in range(len(self.J)):
            Od[j] = self.J[j]
        for k in range(len(self.K)): 
            self.a[k] = self.a[k]*self.p[k]
#        tot_cap = sum(self.a)
#        r = random.randint(0, len(self.J)-1) # maks yang dibuka
        while len(Od) >self.P:
            rand = random.randint(0, len(self.J)-1)
            Cd.append(Od[rand])
            Od.remove(Od[rand])
            z[rand]=0
        temp = [0]*len(self.K)
        for k in range(len(self.K)):
            for j in range(len(self.J)):
                if z[j] == 0:
                    temp[k] = temp[k] + self.g[k][j]
                    self.g[k][j] = 0
#                elif z[j] == 1 &&  self.g[k][j] ==0:
                    
        self.g = np.append(self.g, np.array([temp]).T,1)
        self.c = np.append(self.c, np.array([[0]*len(self.K)]).T,1)
        for k in range(len(self.K)):
            if self.p[k] == 0:
                self.g[k][j] = 0
        for j in range(len(self.J)):#hati-hati di sini
            self.b[j] = self.b[j]*z[j]
        self.b.append(sum(temp))
        self.J.append("dummy")
        
        print(self.b, self.a, self.c, self.g)
        v = prosedur2(self.K, self.J, self.a, self.b,self.c, self.g).encode()
        return v, Od, Cd, z, self.P
    
supplier = ["s1","s2","s3"]
plant = ["p1","p2","p3"]
dc = ["dc1","dc2","dc3","dc4"]
customer =["cust1","cust2", "cust3","cust4"]

sups =[250,200,250]
D = [200,150,200] 
W = [150, 100, 200, 100]
d = [50, 100, 50, 100]

b = np.array([[0,150,100],[200,0,0],[0,0,50]]) 
f = np.array([[0,0,0,0],[0,0,150,0],[150,50,0,0]])
q = np.array([[50,100,0,0],[0,0,0,0],[0,0,50,100],[0,0,0,0]])

t = np.array([[4,3,1],[3,5,2],[1,6,4]])
a = np.array([[5,2,4,3],[4,6,3,5],[3,5,1,6]])
c = np.array([[3,5,2,4],[6,2,5,1],[4,3,6,5],[2,4,3,2]])

stage1 = enc_stage_1(supplier, plant, sups, D, t, b, 2)
v1 = stage1.encoding()
Op = v1[1]
Cp = v1[2]
p  = v1[3]

stage2 = enc_stage_2(plant, dc, Op,Cp, p, D, W, a, f, 3)
v2 = stage2.encoding()
            
        
