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
import numpy as np
#from dummy import add_dummy
#from population import create_population
#from evaluation_funtion import evaluation
from genetic_algorithm import crossover
import random
from genetic_algorithm import parentMutation
from genetic_algorithm import swapMutation
from genetic_algorithm import integerMutation
from genetic_algorithm import evaluate
from genetic_algorithm import rouletteWheel
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

#population = create_population(10,supplier,plant, dc, customer, sups, D, W,d,2,2)
population = [(np.array([[ 50,   0,   0],
         [  0,   0,   0],
         [150, 100,   0]]), np.array([[  0,   0, 200,   0],
         [  0,   0,   0, 100],
         [  0,   0,   0,   0]]), np.array([[  0,   0,   0,   0],
         [  0,   0,   0,   0],
         [ 50, 100,  50,   0],
         [  0,   0,   0, 100]]), [1, 1, 0], np.array([0, 0, 1, 1])), 
(np.array([[  0,   0,  50],
         [  0,   0,   0],
         [  0, 150, 100]]), np.array([[  0,   0,   0,   0],
         [  0,   0, 150,   0],
         [150,   0,   0,   0]]), np.array([[  0,   0,  50, 100],
         [  0,   0,   0,   0],
         [ 50, 100,   0,   0],
         [  0,   0,   0,   0]]), [0, 1, 1], np.array([1, 0, 1, 0])), (np.array([[  0,   0,   0],
         [  0,   0, 100],
         [200,   0,   0]]), np.array([[  0, 100, 100,   0],
         [  0,   0,   0,   0],
         [  0,   0, 100,   0]]), np.array([[  0,   0,   0,   0],
         [  0,   0,   0, 100],
         [ 50, 100,  50,   0],
         [  0,   0,   0,   0]]), [1, 0, 1], np.array([0, 1, 1, 0])), (np.array([[  0,   0, 200],
         [  0,   0,   0],
         [  0, 100,   0]]), np.array([[  0,   0,   0,   0],
         [100,   0,   0,   0],
         [  0,   0, 200,   0]]), np.array([[ 50,   0,  50,   0],
         [  0,   0,   0,   0],
         [  0, 100,   0, 100],
         [  0,   0,   0,   0]]), [0, 1, 1], np.array([1, 0, 1, 0])), (np.array([[  0,   0,   0],
         [  0,   0, 150],
         [  0, 150,   0]]), np.array([[  0,   0,   0,   0],
         [  0,   0, 150,   0],
         [150,   0,   0,   0]]), np.array([[ 50,   0,   0, 100],
         [  0,   0,   0,   0],
         [  0, 100,  50,   0],
         [  0,   0,   0,   0]]), [0, 1, 1], np.array([1, 0, 1, 0])), (np.array([[200,   0,   0],
         [  0,   0,   0],
         [  0, 100,   0]]), np.array([[100,   0, 100,   0],
         [  0,   0, 100,   0],
         [  0,   0,   0,   0]]), np.array([[  0, 100,   0,   0],
         [  0,   0,   0,   0],
         [ 50,   0,  50, 100],
         [  0,   0,   0,   0]]), [1, 1, 0], np.array([1, 0, 1, 0])), (np.array([[  0,  50,   0],
         [  0,   0,   0],
         [  0, 100, 150]]), np.array([[  0,   0,   0,   0],
         [100,   0,  50,   0],
         [  0,   0, 150,   0]]), np.array([[  0, 100,   0,   0],
         [  0,   0,   0,   0],
         [ 50,   0,  50, 100],
         [  0,   0,   0,   0]]), [0, 1, 1], np.array([1, 0, 1, 0])), (np.array([[  0,   0,   0],
         [100,   0,   0],
         [  0,   0, 200]]), np.array([[100,   0,   0,   0],
         [  0,   0,   0,   0],
         [  0,   0, 200,   0]]), np.array([[  0, 100,   0,   0],
         [  0,   0,   0,   0],
         [ 50,   0,  50, 100],
         [  0,   0,   0,   0]]), [1, 0, 1], np.array([1, 0, 1, 0])), (np.array([[  0,   0,   0],
         [  0,   0, 150],
         [  0, 150,   0]]), np.array([[  0,   0,   0,   0],
         [  0,   0, 150,   0],
         [  0,   0,  50, 100]]), np.array([[  0,   0,   0,   0],
         [  0,   0,   0,   0],
         [ 50,   0,  50, 100],
         [  0, 100,   0,   0]]), [0, 1, 1], np.array([0, 0, 1, 1])), (np.array([[200,   0,   0],
         [  0,   0, 100],
         [  0,   0,   0]]), np.array([[  0, 100, 100,   0],
         [  0,   0,   0,   0],
         [  0,   0, 100,   0]]), np.array([[  0,   0,   0,   0],
         [ 50,   0,  50,   0],
         [  0, 100,   0, 100],
         [  0,   0,   0,   0]]), [1, 0, 1], np.array([0, 1, 1, 0]))]
g=[4,5,6]
v=[3,7,5,6]
#weight =np.random.dirichlet(np.ones(3), size=1)
weight=np.array([[0.36459012, 0.31979052, 0.31561936]])
the_number_of_generation=100
# initialization
encoding_population = enc_pop(population, supplier, plant, dc, customer, sups, D, W, d, t, a, c)
mu = copy.deepcopy(encoding_population)
lambdas =copy.deepcopy(encoding_population)

for generation in range(the_number_of_generation):
    print('iterasi   ', generation)
    ### crossover
    random_crossover=[0]*len(mu)
    temp=[]
    for i in range(len(lambdas)):
        random_crossover[i] = random.random()
        if random_crossover[i]<0.5:
            temp.append(random_crossover[i])
    
    if len(temp)%2!=0:
        temp.remove(temp[random.randint(0,len(temp)-1)])
    parent = [[0]*2]*int(len(temp)/2)
    index_parent =[[0]*2]*int(len(temp)/2)
    for x in range(len(parent)):
        for y in range(2):
            if x != 0:
                parent[x][y]=temp[x+y+1]
                index_parent[x][y]=np.where(np.array(random_crossover)==temp[x+y+1])[0][0]
            else:
                parent[x][y]=temp[x+y]
                index_parent[x][y]=np.where(np.array(random_crossover)==temp[x+y])[0][0]
    for x in range(len(index_parent)):
        children = crossover(lambdas[index_parent[x][0]], lambdas[index_parent[x][1]], sups, W, D, d)
        lambdas[index_parent[x][0]]=children[0]
        lambdas[index_parent[x][1]]=children[1]
#    ### mutation
    random_mutation = [0]*len(lambdas)
    for i in range(len(random_mutation)):
        random_mutation[i] = random.random()
    index_parent = parentMutation(random_mutation, 0.2)
    random_individu = random.randint(0,2)
    for x in range(len(index_parent)):
        if random_individu % 2 == 0:
            lambdas[index_parent[x]][0] = swapMutation(lambdas[index_parent[x]][0])
            temp = copy.deepcopy(lambdas[index_parent[x]][2])
            lambdas[index_parent[x]][2] = integerMutation(lambdas[index_parent[x]][2], len(dc))
        else:
            lambdas[index_parent[x]][1] = swapMutation(lambdas[index_parent[x]][1])
    mupluslambda = mu + lambdas
    decode_mupluslambda=copy.deepcopy(mupluslambda)
#    print('selection')
    for x in range(len(mupluslambda)):
        decode_mupluslambda[x]=stage_1(supplier, plant, dc, customer, 1, sups, D, W, d,mupluslambda[x][0],mupluslambda[x][1],mupluslambda[x][2],t,a).decode()
    eval_mupluslambda=evaluate(decode_mupluslambda,sups, D, W,d,t,a,c,g,v,0.8,0.8,weight[0][0],weight[0][1],weight[0][2])
    newPopulation=[]
    
    #dict.fromkeys() digunakan untuk membuat list tidak terdapat duplikat
    best_selection = sorted(list(dict.fromkeys(eval_mupluslambda)))[0:2]
    afterSelectBest = copy.deepcopy(mupluslambda)
    for i in range(len(best_selection)):
        newPopulation.append(mupluslambda[eval_mupluslambda.index(best_selection[i])])
        afterSelectBest.remove(mupluslambda[eval_mupluslambda.index(best_selection[i])])    
    
    decode_afterSelectBest =[0]*len(afterSelectBest)
    for x in range(len(afterSelectBest)):
        decode_afterSelectBest[x]=stage_1(supplier, plant, dc, customer, 1, sups, D, W, d,afterSelectBest[x][0],afterSelectBest[x][1],afterSelectBest[x][2],t,a).decode()
#    print('rolet')
    eval_afterSelectBest = evaluate(decode_afterSelectBest,sups, D, W,d,t,a,c,g,v,0.8,0.8,weight[0][0],weight[0][1], weight[0][2]) 
    afterRouletteSelection=rouletteWheel(eval_afterSelectBest, afterSelectBest)
    decode_afterRouletteSelection =[0]*len(afterRouletteSelection)
    for x in range(len(afterRouletteSelection)):
        decode_afterRouletteSelection[x]=stage_1(supplier, plant, dc, customer, 1, sups, D, W, d,afterRouletteSelection[x][0],afterRouletteSelection[x][1],afterRouletteSelection[x][2],t,a).decode()
    
    eval_afterRouletteSelection=evaluate(decode_afterRouletteSelection,sups, D, W, d, t, a, c, g ,v,0.8, 0.8, weight[0][0], weight[0][1], weight[0][2])    
    best_select = sorted(eval_afterRouletteSelection)[0:len(mu)-len(newPopulation)]
    for i in range(len(best_select)):
        newPopulation.append(afterSelectBest[eval_afterRouletteSelection.index(best_select[i])])
    mu = copy.deepcopy(newPopulation)
    lambdas = copy.deepcopy(mu)
    
    
decode_population =[0]*len(newPopulation)
for x in range(len(newPopulation)):
    decode_population[x]=stage_1(supplier, plant, dc, customer, 1, sups, D, W, d,newPopulation[x][0],newPopulation[x][1],newPopulation[x][2],t,a).decode()    


print(evaluate(decode_population,sups, D, W,d,t,a,c,g,v,0.8,0.8,weight[0][0],weight[0][1],weight[0][2]))
print("setelah operasi genetik ", min(evaluate(decode_population,sups, D, W,d,t,a,c,g,v,0.8,0.8,weight[0][0],weight[0][1],weight[0][2])))