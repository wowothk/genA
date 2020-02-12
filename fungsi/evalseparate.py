#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 14:58:19 2019

@author: rudi
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 12:17:21 2019

@author: rudi

main program
1. initialization
2. evaluation
3. genetic operator
4. selection

Sebagai catatan inisialisasi disini dimaksudkan untuk menginisialisasi populasi yang
telah diencode

masalah yang belum terselesaikan adalah 
pada masalah ini ada indikasi bahwasanya ketika inisialisasi populasi dengan dc yang
muncul akhirnya adalah 3 sementara yang dibolehkan buka adalah 2 maka ada kemungkinan dia 
juga menghasilkan optimisasi yang salah

2 untuk setiap generasi dilakukan encode

"""
#from susahnya_stage2 import create
import sys
sys.path.insert(0, '/home/rudi/Documents/skripsi')
#from encode import priority_based_enc
#from encode import integer_encoding
import pandas as pd
import numpy as np
from genetic_algorithm import crossover
import random
from genetic_algorithm import parentMutation
from genetic_algorithm import swapMutation
from genetic_algorithm import integerMutation
# from genetic_algorithm import evaluate_problem2
from genetic_algorithm import rouletteWheel
from genetic_algorithm import randomPopulation
from genetic_algorithm import sumOfNonDominated
from genetic_algorithm import evaluate_problem1
from genetic_algorithm import evaluate_problem2
#from genetic_algorithm import roulettewheelSelection
from genetic_algorithm import enc_pop
#from genetic_algorithm import check_integer_enc
from decoding_stage_1 import stage_1
import copy

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
g=[40,50,60]
v=[30,70,50,60]

weight=np.array([[0.36459012, 0.31979052, 0.31561936]])
r=[0.36026144, 0.63973856]


decode = [(np.array([[  0., 100.,   0.],
[0., 0., 0.],
[200.,   0.,   0.]]),

np.array([[100.,   0., 100.,   0.],
[100.,   0.,   0.,   0.],
[0., 0., 0., 0.]]),

np.array([[ 50, 100,  50,   0],
[0, 0, 0, 0],
[0, 0, 0, 100],
[0, 0, 0, 0]]),
[1,1,0],
[1,0,1,0]),


(np.array([[ 50.,   0., 200.],
[0., 0., 0.],
[50.,  0.,  0.]]),


np.array([[ 0., 50.,  0., 50.],
[0., 0., 0., 0.],
[  0.,   0., 200.,   0.]]),


np.array([[0, 0, 0, 0],
[0,  0, 50, 0],
[  0, 100,   0, 100],
[50,  0,  0,  0]]),

[1,0,1],[0,1,1,1]),


(np.array([[  0., 150., 100.],
[ 0.,  0., 50.],
[0., 0., 0.]]),


np.array([[0., 0., 0., 0.],
[150.,   0.,   0.,   0.],
[  0.,  50., 100.,   0.]]),


np.array([[ 50, 100,   0,   0],
[ 0,  0, 50,  0],
[ 0,  0,   0, 100],
[0, 0, 0, 0]]),


[0,1,1],[1,1,1,0]),


(np.array([[ 0., 50.,  0.],
[0., 0., 0.],
[  0.,  50., 200.]]),


np.array([[0., 0., 0., 0.],
[ 0., 50.,  0., 50.],
[100., 100.,   0.,   0.]]),


np.array([[  0,   0,   0, 100],
[ 50, 100,   0,   0],
[0, 0, 0, 0],
[ 0,  0, 50,  0]]),

[0,1,1],[1,1,0,1]),


(np.array([[  0., 100., 150.],
[ 0., 50.,  0.],
[0., 0., 0.]]),


np.array([[0., 0., 0., 0.],
[ 50.,   0., 100.,   0.],
[100.,  50.,   0.,   0.]]),


np.array([[ 50, 100,   0,   0],
[ 0,  0, 50,  0],
[  0,   0,   0, 100],
[0, 0, 0, 0]]),


[0,1,1],[1,1,1,0]),


(np.array([[  0., 100.,   0.],
[0., 0., 0.],
[200.,   0.,   0.]]),


np.array([[ 50.,  50., 100.,   0.],
[100.,   0.,   0.,   0.],
[0., 0., 0., 0.]]),


np.array([[ 50, 100,   0,   0],
[ 0,  0, 50,  0],
[  0,   0,   0, 100],
[0, 0, 0, 0]]),


[1,1,0],[1,1,1,0]),


(np.array([[  0., 100., 150.],
[ 0., 50.,  0.],
[0., 0., 0.]]),


np.array([[0., 0., 0., 0.],
[  0.,   0., 150.,   0.],
[  0.,   0., 100.,  50.]]),


np.array([[0, 0, 0, 0],
[0, 0, 0, 0],
[  0, 100,  50, 100],
[50,  0,  0,  0]]),


[0,1,1],[0,0,1,1]),


(np.array([[  0., 150., 100.],
[ 0.,  0., 50.],
[0., 0., 0.]]),


np.array([[0., 0., 0., 0.],
[150.,   0.,   0.,   0.],
[  0.,  50., 100.,   0.]]),


np.array([[ 50, 100,   0,   0],
[ 0,  0, 50,  0],
[  0,   0,   0, 100],
[0, 0, 0, 0]]),


[0,1,1],[1,1,1,0]),


(np.array([[ 0., 50.,  0.],
[0., 0., 0.],
[  0.,  50., 200.]]),


np.array([[0., 0., 0., 0.],
[  0.,   0.,   0., 100.],
[100., 100.,   0.,   0.]]),


np.array([[  0,   0,   0, 100],
[  0, 100,   0,   0],
[0, 0, 0, 0],
[50,  0, 50,  0]]),


[0,1,1],[1,1,0,1]),


(np.array([[ 50.,   0., 200.],
[50.,  0.,  0.],
[0., 0., 0.]]),


np.array([[50., 50.,  0.,  0.],
[0., 0., 0., 0.],
[100.,   0., 100.,   0.]]),


np.array([[ 50, 100,   0,   0],
[ 0,  0, 50,  0],
[  0,   0,   0, 100],
[0, 0, 0, 0]]),

[1,0,1],[1,1,1,0])]
#evalPopulation, evalf1, evalf3, evalAsf, f1,f3


greatPopulation2 = evaluate_problem2(decode,sups, D, W,d,t,a,c,g,v,r[0],r[1],0.5,0.5)
df = pd.DataFrame({
        "f1": greatPopulation2[1],
        "f2":greatPopulation2[2],
        "f1*":greatPopulation2[4],
         "f2*":greatPopulation2[5]   
        })

export_excel = df.to_excel (r'/home/rudi/Documents/skripsi/normalization.xlsx', index = None, header=True)
