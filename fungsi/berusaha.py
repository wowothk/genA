#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 13:47:41 2019

@author: rudi
"""
from genetic_algorithm import parentMutation
from genetic_algorithm import swapMutation
from genetic_algorithm import integerMutation
import random
from genetic_algorithm import check_integer_enc
import numpy as np
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
#a=[[[1,3],[4,2]],[[4,1],[3,5]]]
#b=np.array(a.copy())
#c=[0]*len(a)
#print(len(a))
#for x in range(len(a)):
#    c[x] = a[x]
#for x in range(2):
#    b[x][0] = 10+x
#print(a)
#print(b)
#print(c)
mu=[[[5, 7, 2, 4, 3, 1, 6], [6, 4, 2, 3, 1, 7, 5, 8], [3, 3, 3, 4]],
 [[5, 7, 2, 1, 3, 4, 6], [3, 6, 4, 5, 1, 7, 2, 8], [3, 3, 1, 1, 3]],
 [[7, 2, 5, 6, 1, 3, 4], [4, 3, 7, 1, 6, 5, 2, 8], [3, 3, 3, 2]],
 [[5, 7, 2, 1, 3, 6, 4], [1, 4, 6, 5, 3, 7, 2, 8], [1, 3, 1, 3, 1]],
 [[7, 5, 2, 1, 3, 6, 4], [1, 6, 4, 5, 2, 7, 3, 8], [1, 3, 3, 1, 3]],
 [[5, 7, 2, 6, 3, 1, 4], [4, 7, 3, 5, 1, 6, 2, 8], [3, 1, 3, 3, 1]],
 [[5, 7, 2, 1, 3, 4, 6], [1, 4, 7, 5, 3, 6, 2, 8], [3, 1, 3, 3, 1]],
 [[7, 5, 2, 6, 1, 3, 4], [4, 1, 6, 5, 2, 7, 3, 8], [3, 1, 3, 3, 1]],
 [[7, 5, 2, 1, 3, 6, 4], [2, 7, 4, 1, 3, 6, 5, 8], [3, 4, 3, 3]],
 [[2, 5, 7, 3, 1, 6, 4], [4, 3, 7, 2, 6, 5, 1, 8], [2, 3, 2, 3]]]
lambdas=copy.deepcopy(mu)
random_mutation = [0]*len(lambdas)
for i in range(len(random_mutation)):
    random_mutation[i] = random.random()
    
index_parent = parentMutation(random_mutation, 0.2)
print('parent  ',index_parent)
print('mu ',mu[index_parent[0]])
random_individu = random.randint(0,2)
for x in range(len(index_parent)):
    if random_individu % 2 == 0:
        print('condisi 1')
        lambdas[index_parent[x]][0] = swapMutation(lambdas[index_parent[x]][0])
        temp = copy.deepcopy(lambdas[index_parent[x]][2])
        lambdas[index_parent[x]][2] = integerMutation(lambdas[index_parent[x]][2], len(dc))
        check= check_integer_enc(lambdas[index_parent[x]][2],W, d)
        while (check == False):
            lambdas[index_parent[x]][2] = np.array(integerMutation(temp, len(dc)))
            check= check_integer_enc(lambdas[index_parent[x]][2], W, d)
    else:
        print('condisi 2')
        lambdas[index_parent[x]][1] = swapMutation(lambdas[index_parent[x]][1])
    print('cek ini')
    print('lambda', lambdas[index_parent[x]])
    print('mu    ',mu[index_parent[x]])
