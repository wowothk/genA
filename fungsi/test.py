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

newPopulation = [[[3, 6, 2, 4, 1, 5], [2, 1, 6, 5, 3, 7, 4], [3, 3, 3, 2]], 
[[3, 1, 5, 6, 4, 2], [4, 1, 3, 6, 2, 5, 7], [3, 3, 3, 2]],
[[3, 1, 6, 4, 2, 5], [6, 5, 3, 2, 7, 4, 1], [4, 4, 3, 3]], 
[[4, 1, 6, 2, 3, 5], [3, 4, 5, 6, 7, 2, 1], [4, 4, 3, 2]], 
[[3, 1, 4, 5, 2, 6], [4, 3, 5, 6, 1, 2, 7], [2, 1, 3, 4]]] 

    
decode_population =[0]*len(newPopulation)
for x in range(len(newPopulation)):
    decode_population[x]=stage_1(supplier, plant, dc, customer, 1, sups, D, W, d,newPopulation[x][0],newPopulation[x][1],newPopulation[x][2],t,a).decode()    


greatPopulation = evaluate_problem2(decode_population,sups, D, W,d,t,a,c,g,v,r[0],r[1],0.5,0.5)

print(greatPopulation)
print(greatPopulation[0])
print(min(greatPopulation[0]))
print("setelah operasi genetik ", min(greatPopulation[0]))


