#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 15:11:51 2019

@author: rudi
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 16:53:00 2019

@author: rudi
evaluation

f1(g,p,v,z,t,b,a,f,c,q)
f2(q, d)
f3(f,D,Op, q, W, Od)

D: the capacity of the plant that available
Op: the number of opened plant
Od: the number of opened Dc
W: the capacity of the dc that available
b: the amount of shipment from supplier to plant
q: the amount of shipment from dc to customer
f: the amount of shipment from plant to dc
g: the annual cost for the operation of plant
v: the annual cost for the operation of DC
t: the cost of shipment from supplier to plant
a: the cost of shipment from plant to dc
c: the cost of shipment from dc to customer

"""
import numpy as np, numpy.random
import math
from check_time import check_time
from check_time import summation_by_time

class evaluation2:
    def __init__(self, b,f,q, sups, D, W, d, t, a, c,g,v,p,z, r1, r2):
        self.b = b
        self.f = f
        self.q = q
        self.sups = sups
        self.D = D
        self.W = W
        self.d = d
        self.t = t
        self.a = a
        self.c = c
        self.g = g
        self.v = v
        self.p = p
        self.z = z
#        self.Op = Op
#        self.Od = Od
        self.r1 = r1
        self.r2 = r2

    
    def func1(self):
        costPlant = [0]*len(self.p)
        for k in range(len(self.p)):
            costPlant[k] = self.g[k]*self.p[k]
        
        costDc = [0]*len(self.z)
        for j in range(len(self.z)):
            costDc[j] = self.v[j]*self.z[j]
        
        costOfb = np.array([[0]*len(self.D)]*len(self.sups))
        sumcostOfb = [0]*len(self.sups)
        for s in range(len(self.sups)):
            for k in range(len(self.D)):
                costOfb[s][k] = self.b[s][k]*self.t[s][k]
            sumcostOfb[s] = sum(costOfb[s])
        
        costOff = np.array([[0]*len(self.W)]*len(self.D))
        sumcostOff = [0]*len(self.D)
        for k in range(len(self.D)):
            for j in range(len(self.W)):
                costOff[k][j] = self.f[k][j]*self.a[k][j]
            sumcostOff[k] = sum(costOff[k])    
            
        costOfq = np.array([[0]*len(self.d)]*len(self.W))
        sumcostOfq = [0]*len(self.W)
        for j in range(len(self.W)):
            for i in range(len(self.d)):
                costOfq[j][i] = self.q[j][i]*self.c[j][i]
            sumcostOfq[j] = sum(costOfq[j])
        return sum(costPlant)+sum(costDc)+sum(sumcostOfb)+sum(sumcostOff)+sum(sumcostOfq)

    def func1_alternative(self):
        costPlant = [0]*len(self.p)
        for k in range(len(self.p)):
            costPlant[k] = self.g[k]*self.p[k]
        
        costDc = [0]*len(self.z)
        for j in range(len(self.z)):
            costDc[j] = self.v[j]*self.z[j]
        
        costOfb = np.array([[0]*len(self.D)]*len(self.sups))
        sumcostOfb = [0]*len(self.sups)
        for s in range(len(self.sups)):
            for k in range(len(self.D)):
                costOfb[s][k] = self.b[s][k]*0.02458*self.t[s][k]
            sumcostOfb[s] = sum(costOfb[s])
        
        costOff = np.array([[0]*len(self.W)]*len(self.D))
        sumcostOff = [0]*len(self.D)
        for k in range(len(self.D)):
            for j in range(len(self.W)):
                costOff[k][j] = self.f[k][j]*self.a[k][j]
            sumcostOff[k] = sum(costOff[k])    
            
        costOfq = np.array([[0]*len(self.d)]*len(self.W))
        sumcostOfq = [0]*len(self.W)
        for j in range(len(self.W)):
            for i in range(len(self.d)):
                costOfq[j][i] = self.q[j][i]*self.c[j][i]
            sumcostOfq[j] = sum(costOfq[j])
        return sum(costPlant)+sum(costDc)+sum(sumcostOfb)+sum(sumcostOff)+sum(sumcostOfq)
        
#    def func2(self):
#        C=check_time(self.h, self.tau, len(self.W), len(self.d))
#        summation = summation_by_time(self.q, C)
##        sumOfq = [0]*len(self.W)
##        for j in range(len(self.W)):
##            sumOfq[j] = sum(self.q[j])
#        
#        return summation/sum(self.d)
    
    def func3(self):
        openPlant = list(np.multiply(self.D, self.p))
        openDc = list(np.multiply(self.W, self.z))
        equation1 = [0]*len(openPlant)
        equation2 = [0]*len(openDc)
        for k in range(len(self.D)):
            if self.p[k] != 0:
                equation1[k]=(sum(self.f[k])/self.D[k]-(np.sum(self.f)/sum(openPlant)))**2
        for j in range(len(self.W)):
            if self.z[j] != 0:
                equation2[j]=(sum(self.q[j])/self.W[j]-(np.sum(self.q)/sum(openDc)))**2        
        return self.r1*math.sqrt(sum(equation1)/sum(self.p))+self.r2*math.sqrt(sum(equation2)/sum(self.z))
   
    
    
    
    
    """
    for find weight for the weight sum approach
    
    import numpy as np, numpy.random
    
    np.random.dirichlet(np.ones(x), size=1) , dengan x merupakan banyaknya weight yang ingin dibuat
    
    """