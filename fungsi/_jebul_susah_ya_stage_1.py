#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 17:21:15 2019

@author: rudi


"""

import numpy as np
import random
#from repair import repair_alg
class create:
    def __init__(self, supplier, plant, dc, customer,S,K,J,I, maks_plant, maks_dc):
        ### sebagai himpunan ###
        self.supplier = supplier
        self.plant = plant
        self.dc = dc
        self.customer = customer
#        self.Od = Od
#        self.Cd = Cd
#        self.Op = Op
#        self.Cp = Cp
        ### sebagai value
        self.S = S
        self.K = K
        self.J = J
        self.I = I
        self.maks_plant = maks_plant
        self.maks_dc = maks_dc
    def supplier_to_plant(self):
        b = np.array([[1000]*len(self.K)]*len(self.S))
        p = [1]*len(self.K)
        Op = [None]*len(self.K)
        temp_K = [None]*len(self.K)
        temp_plant = [None]*len(self.K)
        Cp = []
        for k in range(len(self.K)):
            Op[k] = self.plant[k]
            temp_K[k] = self.K[k]
            temp_plant[k] = self.plant[k]
        while len(Op) > self.maks_plant:
            rd = random.randint(0, len(Op)-1)
            Cp.append(Op[rd])
            p[self.plant.index(Op[rd])] = 0
            Op.remove(Op[rd])            
        for s in range(len(self.S)):
            while sum(b[s]) > self.S[s]:
                for k in range(len(self.K)):
                    if p[k] != 0:
                        b[s][k] = random.randint(0, self.S[s])
                    else:
                        b[s][k] = 0
        temp = [0]*len(self.S)
        for s in range(len(self.S)):
            if self.S[s] - sum(b[s])!=0:
                temp[s] = self.S[s] - sum(b[s])
        if sum(temp) != 0:
            temp_plant.append("dummy")
            temp_K.append(sum(temp))
            b = np.append(b, np.array([temp]).T,1)
        print("nilai b     ", b)
        return b, p, temp_plant, temp_K
    
    
supplier = ["s1","s2","s3"]
plant = ["p1","p2","p3"]
dc = ["dc1","dc2","dc3","dc4"]
customer =["cust1","cust2", "cust3","cust4"]

sups =[250,200,250]
D = [200,150,200] 
W = [150, 100, 200, 100]
d = [50, 100, 50, 100]

# supplier, plant, dc, customer,S,K,J,I, maks_plant, maks_dc

stage_satu = create(supplier, plant, dc, customer, sups, D, W, d, 2, 3)
#print(stage_satu.supplier_to_plant())
print(stage_satu.supplier_to_plant()) 