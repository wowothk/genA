#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 10:02:27 2019

@author: rudi
"""
from evaluation_funtion import evaluation
import numpy as np
supplier = ["s1","s2","s3"]
plant = ["p1","p2","p3"]
dc = ["dc1","dc2","dc3","dc4"]
customer =["cust1","cust2", "cust3","cust4"]

sups =[250,200,250]
D = [200,150,200] 
W = [150, 100, 200, 100]
d = [50, 100, 50, 100]

t = np.array([[4,3,1],[3,5,2],[1,6,4]])
a = np.array([[5,2,4,3],[4,6,3,5],[3,5,1,6]])
c = np.array([[3,5,2,4],[6,2,5,1],[4,3,6,5],[2,4,3,2]])

h= np.array([[7,5,3,1],[2,4,6,5],[3,7,8,4],[9,3,2,1]])
tau=6
r=[0.36026144, 0.63973856]
weight=[0.36459012, 0.31979052, 0.31561936]
g=[4,5,6]
v=[3,7,5,6]


#banyak generasi 10
#nilai minimum = 646.2420142712814

individu1 = (np.array([[ 50,   0, 200],
        [  0,   0,   0],
        [ 50,   0,   0]]), np.array([[  0, 100,   0,   0],
        [  0,   0,   0,   0],
        [  0,   0, 200,   0]]), np.array([[  0,   0,   0,   0],
        [  0,   0,   0, 100],
        [ 50, 100,  50,   0],
        [  0,   0,   0,   0]]), [1, 0, 1], [0, 1, 1, 0])
individu2 = (np.array([[ 50,   0, 200],
        [  0,   0,   0],
        [ 50,   0,   0]]), np.array([[  0, 100,   0,   0],
        [  0,   0,   0,   0],
        [  0,   0, 200,   0]]), np.array([[  0,   0,   0,   0],
        [  0,   0,   0, 100],
        [ 50, 100,  50,   0],
        [  0,   0,   0,   0]]), [1, 0, 1], [0, 1, 1, 0])
individu3=(np.array([[ 50,   0, 200],
        [  0,   0,   0],
        [ 50,   0,   0]]), np.array([[  0, 100,   0,   0],
        [  0,   0,   0,   0],
        [ 50,   0, 150,   0]]), np.array([[  0,   0,  50,   0],
        [  0,   0,   0, 100],
        [ 50, 100,   0,   0],
        [  0,   0,   0,   0]]), [1, 0, 1], [1, 1, 1, 0])
individu4=(np.array([[  0,   0, 200],
        [  0,   0,   0],
        [100,   0,   0]]), np.array([[  0, 100,   0,   0],
        [  0,   0,   0,   0],
        [  0,   0, 200,   0]]), np.array([[  0,   0,   0,   0],
        [  0,   0,   0, 100],
        [ 50, 100,  50,   0],
        [  0,   0,   0,   0]]), [1, 0, 1], [0, 1, 1, 0])
def cek(individu, sups, D, W, d, t, a,c,g,v, r1, r2, h, tau):
    func1 = evaluation(individu[0],individu[1],individu[2], sups, D, W, d, t,a,c,g,v,individu[3], individu[4], r1, r2, h, tau).func1()
    func2 = evaluation(individu[0],individu[1],individu[2], sups, D, W, d, t,a,c,g,v,individu[3], individu[4], r1, r2, h, tau).func2()
    func3 = evaluation(individu[0],individu[1],individu[2], sups, D, W, d, t,a,c,g,v,individu[3], individu[4], r1, r2, h, tau).func3()
    
    return func1, func2, func3

print(cek(individu4, sups, D, W, d, t, a,c,g,v, r[0], r[1], h, tau))