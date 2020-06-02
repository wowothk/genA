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
from genetic_algorithm import evaluate_alternative
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
data_Path = '/home/rudi/Documents/import_excel/datacustomer.xlsx'

dataNama = pd.read_excel(data_Path,sheet_name='naming')
supplier = np.array(dataNama['supplier'].dropna(how='any'))
plant = np.array(dataNama['plant'].dropna(how='any'))
dc = np.array(dataNama['dc'].dropna(how='any'))
customer =np.array(dataNama['customer'].dropna(how='any'))

dataCapacity = pd.read_excel(data_Path, sheet_name="kapasitas")
supsinton =np.array(dataCapacity['supplier (ton)'].dropna(how='any'))
D = np.array(dataCapacity['plant(pac)'].dropna(how='any'))
W = np.array(dataCapacity['dc(pac)'].dropna(how='any'))
sups = [None]*len(supsinton)
for x in range(len(supsinton)):
    sups[x] = supsinton[x]/0.02458
    
dataDemand = pd.read_excel(data_Path, sheet_name = 'permintaan customer')
d = np.array(dataDemand['demand'])

t = np.array(pd.read_excel(data_Path, sheet_name='supplier ke plant').iloc[:,1:4])
a = np.array(pd.read_excel(data_Path, sheet_name='plant ke dc').iloc[:,1:7])
c = np.array(pd.read_excel(data_Path, sheet_name='dc ke customer').iloc[:,1:64])

h= np.array(pd.read_excel(data_Path, sheet_name='Pembentukan h').iloc[:,1:64])
#print(t)
tau=12




g=np.array(dataCapacity['fixed cost plant'].dropna(how='any'))
v=np.array(dataCapacity['fixed cost dc'].dropna(how='any'))

##weight =np.random.dirichlet(np.ones(3), size=1)
weight=np.array([[0.36459012, 0.31979052, 0.31561936]])
r=[0.36026144, 0.63973856]
the_number_of_generation=500
# initialization
stage1=[]
for x in range(len(sups)+len(plant)):
    stage1.append(x+1)
stage2=[]
for x in range(len(dc)+len(plant)):
    stage2.append(x+1)
stage3=[None]*len(d)
for x in range(len(d)):
    stage3[x]=random.randint(1,len(dc))

population=np.array([[None]*3]*400)
for x in range(400):
    for y in range(3):
        if y==0:
            population[x][y]=random.sample(stage1, len(stage1))
        elif y==1:
            population[x][y]=random.sample(stage2, len(stage2))
        else:
            for z in range(len(d)):
                stage3[z]=random.randint(1,len(dc))
            population[x][y]=copy.deepcopy(stage3)
population = [list(x) for x in population]            
#print(population)            
#population = [[[5, 7, 8, 2, 6, 3, 1, 4], [3, 5, 8, 7, 1, 6, 9, 4, 2], [5, 1, 1, 3, 3, 3, 6, 5, 2, 6, 6, 1, 6, 2, 6, 3, 6, 2, 1, 3, 5, 4, 1, 6, 6, 2, 1, 4, 2, 3, 1, 6, 5, 2, 1, 1, 3, 6, 2, 1, 5, 5, 5, 3, 1, 6, 5, 6, 6, 5, 5, 4, 6, 6, 1, 6, 1, 2, 1, 2, 3, 6, 5]], [[3, 8, 7, 6, 5, 4, 2, 1], [4, 2, 3, 1, 9, 8, 7, 6, 5], [6, 1, 2, 3, 4, 1, 4, 4, 2, 1, 2, 2, 1, 2, 1, 4, 4, 6, 5, 3, 4, 1, 2, 5, 4, 3, 5, 4, 2, 5, 1, 1, 2, 6, 4, 1, 6, 1, 2, 1, 1, 6, 6, 5, 4, 2, 6, 2, 4, 5, 2, 6, 6, 2, 1, 1, 5, 1, 2, 1, 6, 4, 4]], [[7, 5, 8, 1, 4, 6, 2, 3], [8, 3, 1, 5, 7, 4, 2, 9, 6], [1, 1, 6, 5, 1, 1, 4, 1, 6, 6, 6, 5, 1, 1, 3, 3, 3, 4, 3, 3, 3, 2, 5, 1, 6, 5, 3, 4, 4, 5, 2, 5, 6, 4, 3, 6, 4, 1, 2, 2, 2, 2, 3, 5, 4, 1, 6, 6, 5, 5, 4, 2, 2, 5, 4, 1, 1, 1, 5, 5, 2, 3, 6]], [[2, 3, 6, 1, 4, 5, 8, 7], [6, 1, 3, 2, 4, 7, 5, 8, 9], [5, 2, 2, 6, 5, 5, 1, 5, 3, 5, 3, 2, 5, 4, 1, 6, 4, 5, 4, 4, 1, 2, 4, 3, 4, 6, 6, 6, 5, 4, 3, 6, 6, 6, 1, 6, 4, 3, 2, 2, 4, 2, 1, 1, 1, 6, 4, 3, 3, 3, 2, 5, 3, 2, 2, 1, 1, 5, 2, 5, 6, 5, 5]], [[7, 4, 3, 2, 5, 1, 6, 8], [7, 2, 4, 3, 9, 1, 8, 6, 5], [3, 3, 2, 5, 6, 2, 5, 3, 2, 2, 1, 1, 5, 1, 6, 1, 3, 3, 5, 5, 1, 1, 6, 6, 3, 6, 3, 3, 1, 2, 5, 6, 2, 4, 6, 2, 4, 2, 2, 4, 4, 4, 4, 3, 5, 1, 6, 1, 3, 1, 4, 1, 2, 5, 2, 2, 3, 1, 4, 6, 2, 2, 2]], [[3, 4, 7, 8, 5, 2, 1, 6], [4, 9, 2, 3, 8, 5, 6, 1, 7], [5, 4, 1, 2, 1, 4, 3, 1, 1, 6, 2, 2, 3, 1, 3, 3, 4, 3, 5, 2, 3, 2, 1, 4, 2, 3, 4, 1, 1, 3, 4, 2, 2, 3, 3, 6, 1, 4, 4, 2, 4, 3, 2, 4, 1, 1, 6, 3, 2, 6, 5, 1, 2, 4, 2, 4, 6, 6, 4, 6, 2, 6, 4]], [[7, 1, 6, 2, 8, 4, 3, 5], [1, 5, 3, 2, 4, 8, 6, 9, 7], [2, 3, 3, 3, 1, 3, 2, 4, 2, 2, 6, 6, 3, 6, 6, 3, 4, 3, 4, 6, 4, 5, 5, 4, 2, 2, 1, 5, 3, 2, 5, 6, 2, 5, 1, 5, 1, 2, 2, 4, 1, 2, 2, 6, 6, 5, 3, 5, 1, 6, 3, 2, 2, 3, 4, 5, 4, 2, 4, 3, 2, 1, 2]], [[8, 3, 7, 2, 6, 1, 4, 5], [5, 1, 2, 7, 9, 6, 4, 8, 3], [6, 6, 2, 2, 3, 2, 2, 3, 3, 3, 2, 1, 2, 5, 6, 6, 4, 5, 2, 1, 2, 3, 5, 5, 2, 2, 2, 3, 4, 6, 3, 6, 4, 4, 3, 4, 5, 4, 3, 2, 1, 3, 5, 2, 3, 5, 6, 5, 1, 4, 2, 3, 5, 2, 4, 4, 6, 3, 1, 5, 5, 1, 5]], [[3, 5, 6, 7, 8, 1, 2, 4], [7, 5, 2, 9, 4, 3, 1, 6, 8], [6, 1, 5, 3, 4, 5, 6, 2, 6, 5, 6, 4, 6, 1, 3, 5, 3, 6, 4, 3, 1, 5, 6, 3, 5, 3, 1, 1, 2, 6, 6, 3, 1, 3, 3, 2, 6, 5, 1, 2, 1, 1, 3, 4, 3, 3, 6, 1, 5, 3, 4, 4, 5, 6, 6, 4, 2, 2, 4, 4, 4, 1, 1]], [[3, 1, 2, 8, 5, 7, 6, 4], [1, 9, 8, 3, 6, 4, 2, 5, 7], [1, 3, 3, 5, 6, 3, 1, 5, 3, 6, 6, 5, 5, 5, 1, 2, 6, 2, 5, 4, 6, 1, 5, 6, 1, 1, 5, 5, 3, 6, 1, 2, 1, 4, 5, 5, 1, 5, 4, 2, 1, 3, 4, 1, 4, 4, 1, 5, 3, 6, 3, 4, 3, 1, 2, 6, 5, 4, 3, 1, 4, 6, 2]]]
#
decode_population_pembanding =[0]*len(population)
for x in range(len(population)):
    decode_population_pembanding[x]=stage_1(supplier, plant, dc, customer, 0.98, sups, D, W, d,population[x][0],population[x][1],population[x][2],t,a).decode()    
#    decode_mupluslambda[x]=stage_1(supplier, plant, dc, customer, 0.98, sups, D, W, d,mupluslambda[x][0],mupluslambda[x][1],mupluslambda[x][2],t,a).decode()



greatPopulation2 = evaluate_alternative(decode_population_pembanding,sups, D, W,d,t,a,c,g,v,r[0],r[1],weight[0][0],weight[0][1],weight[0][2], h, tau)

df = pd.DataFrame({
        "f1":[greatPopulation2[1][greatPopulation2[0].index(min(greatPopulation2[0]))]],
        "f2":[greatPopulation2[2][greatPopulation2[0].index(min(greatPopulation2[0]))]],
        "f3":[greatPopulation2[3][greatPopulation2[0].index(min(greatPopulation2[0]))]],
        "Optimal":[greatPopulation2[0][greatPopulation2[0].index(min(greatPopulation2[0]))]]})
    
#######Problem 1
greatProblem1 = evaluate_problem1(decode_population_pembanding,sups, D, W,d,t,a,c,g,v,r[0],r[1],0.5,0.5, h, tau)
dfProblem1 = pd.DataFrame({
        "f1":[greatProblem1[1][greatProblem1[0].index(min(greatProblem1[0]))]],
        "f2":[greatProblem1[2][greatProblem1[0].index(min(greatProblem1[0]))]],
        "Optimal":[greatProblem1[0][greatProblem1[0].index(min(greatProblem1[0]))]]})

######## Problem 2
greatProblem2 = evaluate_problem2(decode_population_pembanding,sups, D, W,d,t,a,c,g,v,r[0],r[1],0.5,0.5, h, tau)
dfProblem2 = pd.DataFrame({
        "f1":[greatProblem2[1][greatProblem2[0].index(min(greatProblem2[0]))]],
        "f3":[greatProblem2[2][greatProblem2[0].index(min(greatProblem2[0]))]],
        "Optimal":[greatProblem2[0][greatProblem2[0].index(min(greatProblem2[0]))]]})
    
    
#encoding_population = enc_pop(population, supplier, plant, dc, customer, sups, D, W, d, t, a, c)
mu = copy.deepcopy(population)
lambdas =copy.deepcopy(population)

generation = 0
#for generation in range(the_number_of_generation):
while generation < the_number_of_generation:
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
    index_parent = parentMutation(random_mutation, 0.7)
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
    
#### selection
    
    for x in range(len(mupluslambda)):
        decode_mupluslambda[x]=stage_1(supplier, plant, dc, customer, 0.98, sups, D, W, d,mupluslambda[x][0],mupluslambda[x][1],mupluslambda[x][2],t,a).decode()
    eval_mupluslambda=evaluate_alternative(decode_mupluslambda,sups, D, W,d,t,a,c,g,v,r[0],r[1],weight[0][0],weight[0][1],weight[0][2], h, tau)[0]
    newPopulation=[]
    
    #dict.fromkeys() digunakan untuk membuat list tidak terdapat duplikat
#    print('tipe data eval_mu', type(eval_mupluslambda))
#     best_selection = sorted(list(dict.fromkeys(eval_mupluslambda)))[0:2]
#     afterSelectBest = copy.deepcopy(mupluslambda)
#     for i in range(len(best_selection)):
#         newPopulation.append(mupluslambda[eval_mupluslambda.index(best_selection[i])])
#         afterSelectBest.remove(mupluslambda[eval_mupluslambda.index(best_selection[i])])    
        
#     decode_afterSelectBest =[0]*len(afterSelectBest)
#     for x in range(len(afterSelectBest)):
#         decode_afterSelectBest[x]=stage_1(supplier, plant, dc, customer, 0.98, sups, D, W, d,afterSelectBest[x][0],afterSelectBest[x][1],afterSelectBest[x][2],t,a).decode()
# #    print('rolet')
#     eval_afterSelectBest = evaluate_alternative(decode_afterSelectBest,sups, D, W,d,t,a,c,g,v,r[0],r[1],weight[0][0],weight[0][1], weight[0][2], h, tau)[0] 
    
#     bestOf = list(dict.fromkeys(eval_afterSelectBest))
#     if len(bestOf) == len(mu)-len(newPopulation):
#         for i in range(len(bestOf)):
#             newPopulation.append(mupluslambda[eval_mupluslambda.index(best_selection[i])])
#     else:
#         pop = randomPopulation(len(sups),len(plant),len(dc),len(customer), len(mu)-len(newPopulation))        
#         for i in range(len(pop)):
#             newPopulation.append(pop[i])
    best_selection = sorted(list(dict.fromkeys(eval_mupluslambda)))

    if len(mu) == len(best_selection):
        for i in best_selection:
            newPopulation.append(mupluslambda[eval_mupluslambda.index(i)])

    else:
        newPopulation = [mupluslambda[eval_mupluslambda.index(i)] for i in best_selection[0:2]]
        pop = randomPopulation(len(sups),len(plant),len(pengantongan),len(distributor), len(mu)-len(newPopulation))        
        for i in pop:
            newPopulation.append(i)
    
    
    
    if generation > 20 and generation%(2)==0:
#        print("GENERASI  ", generation)
        decode_population_cek =[0]*len(population)
        for x in range(len(population)):
            decode_population_cek[x]=stage_1(supplier, plant, dc, customer, 0.98,  sups, D, W, d,newPopulation[x][0],newPopulation[x][1],newPopulation[x][2],t,a).decode()    
        
        greatPopulation200 = evaluate_alternative(decode_population_cek,sups, D, W,d,t,a,c,g,v,r[0],r[1],weight[0][0],weight[0][1],weight[0][2], h, tau)
        
        df200 = pd.DataFrame({
                "f1":[greatPopulation200[1][greatPopulation200[0].index(min(greatPopulation200[0]))]],
                "f2":[greatPopulation200[2][greatPopulation200[0].index(min(greatPopulation200[0]))]],
                "f3":[greatPopulation200[3][greatPopulation200[0].index(min(greatPopulation200[0]))]],
                "Optimal":[greatPopulation200[0][greatPopulation200[0].index(min(greatPopulation200[0]))]]})
        
        df = df.append(df200, ignore_index=True)
        
        ### problem 1
        greatPopulation200_problem1 = evaluate_problem1(decode_population_cek,sups, D, W,d,t,a,c,g,v,r[0],r[1],0.5,0.5, h, tau)
        
        df200_problem1 = pd.DataFrame({
                "f1":[greatPopulation200_problem1[1][greatPopulation200_problem1[0].index(min(greatPopulation200_problem1[0]))]],
                "f2":[greatPopulation200_problem1[2][greatPopulation200_problem1[0].index(min(greatPopulation200_problem1[0]))]],
                "Optimal":[greatPopulation200_problem1[0][greatPopulation200_problem1[0].index(min(greatPopulation200_problem1[0]))]]})
        
        dfProblem1 = dfProblem1.append(df200_problem1, ignore_index=True)
        ### problem 2
        greatPopulation200_problem2 = evaluate_problem2(decode_population_cek,sups, D, W,d,t,a,c,g,v,r[0],r[1],0.5,0.5, h, tau)
        
        df200_problem2 = pd.DataFrame({
                "f1":[greatPopulation200_problem2[1][greatPopulation200_problem2[0].index(min(greatPopulation200_problem2[0]))]],
                "f3":[greatPopulation200_problem2[2][greatPopulation200_problem2[0].index(min(greatPopulation200_problem2[0]))]],
                "Optimal":[greatPopulation200_problem2[0][greatPopulation200_problem2[0].index(min(greatPopulation200_problem2[0]))]]})
        
        dfProblem2 = dfProblem2.append(df200_problem2, ignore_index=True)
    # diversification strategy
#    if generation == the_number_of_generation/5 - 1 and newPopulation == population:
#        newPopulation = randomPopulation(len(sups),len(plant),len(dc),len(customer), len(newPopulation))
#        generation = -1
#    decode_newPopulation=copy.deepcopy(newPopulation)
#    for x in range(len(newPopulation)):
#        decode_newPopulation[x]=stage_1(supplier, plant, dc, customer, 0.98, sups, D, W, d,newPopulation[x][0],newPopulation[x][1],newPopulation[x][2],t,a).decode()
#    eval_newPopulation=evaluate_alternative(decode_newPopulation,sups, D, W,d,t,a,c,g,v,r[0],r[1],weight[0][0],weight[0][1],weight[0][2], h, tau)[4]
#    temp_newPopulation = []
#    nondominanceCheck = sumOfNonDominated(eval_newPopulation)
#    k = list(np.where(nondominanceCheck[1]=='nondominated')[0])
#    if nondominanceCheck[0] > 0.1*len(population):
#        for i in range(len(k)):
#            temp_newPopulation.append(newPopulation[k[i]])
#        restPopulation = randomPopulation(len(sups),len(plant),len(dc),len(customer), len(newPopulation)-len(k))
#        for i in range(len(restPopulation)):
#            temp_newPopulation.append(restPopulation[i])
#    elif nondominanceCheck[0] <= 0.1*len(population):
#        for i in range(len(k)):
#            temp_newPopulation.append(newPopulation[k[i]])
#        restPopulation = randomPopulation(len(sups),len(plant),len(dc),len(customer), len(newPopulation)-len(k))
#        for i in range(len(restPopulation)):
#            temp_newPopulation.append(restPopulation[i])
#    newPopulation = copy.deepcopy(temp_newPopulation)
#    afterRouletteSelection=rouletteWheel(eval_afterSelectBest, afterSelectBest)
##    print(afterRouletteSelection)
#    decode_afterRouletteSelection =[0]*len(afterRouletteSelection)
#    for x in range(len(afterRouletteSelection)):
#        decode_afterRouletteSelection[x]=stage_1(supplier, plant, dc, customer, 0.98, sups, D, W, d,afterRouletteSelection[x][0],afterRouletteSelection[x][1],afterRouletteSelection[x][2],t,a).decode()
#    
#    eval_afterRouletteSelection=evaluate_alternative(decode_afterRouletteSelection,sups, D, W, d, t, a, c, g ,v,r[0], r[1], weight[0][0], weight[0][1], weight[0][2], h, tau)[0]    
#    best_select = sorted(eval_afterRouletteSelection)[0:len(mu)-len(newPopulation)]
#    for i in range(len(best_select)):
#        newPopulation.append(afterSelectBest[eval_afterRouletteSelection.index(best_select[i])])
    mu = copy.deepcopy(newPopulation)
    lambdas = copy.deepcopy(mu)
    generation = generation + 1
    
    
#decode_population =[0]*len(newPopulation)
#for x in range(len(newPopulation)):
#    decode_population[x]=stage_1(supplier, plant, dc, customer, 0.98, sups, D, W, d,newPopulation[x][0],newPopulation[x][1],newPopulation[x][2],t,a).decode()    
#decode_population2 =[0]*len(population)
#for x in range(len(population)):
#    decode_population2[x]=stage_1(supplier, plant, dc, customer, 0.98, sups, D, W, d,population[x][0],population[x][1],population[x][2],t,a).decode()    
#
#greatPopulation = evaluate_alternative(decode_population,sups, D, W,d,t,a,c,g,v,r[0],r[1],weight[0][0],weight[0][1],weight[0][2], h, tau)
#greatPopulation2 = evaluate_alternative(decode_population2,sups, D, W,d,t,a,c,g,v,r[0],r[1],weight[0][0],weight[0][1],weight[0][2], h, tau)
##print("minimum fungsi satu", greatPopulation[1])
##print("maximum fungsi dua", greatPopulation[2])
##print("minimum fungsi satu", greatPopulation[3])
#print(greatPopulation[0])
#print(min(greatPopulation2[0]))
#print("setelah operasi genetik ", min(greatPopulation[0]))

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['f1'],df['f2'],df['f3'])

fig2 = plt.figure()
ax2 = fig2.add_axes([0,0,1,1])
ax2.scatter(dfProblem1['f1'],dfProblem1['f2'])
plt.show();

fig3 = plt.figure()
ax3 = fig3.add_axes([0,0,1,1])
ax3.scatter(dfProblem2['f1'],dfProblem2['f3'])
plt.show();
#ax3 = fig.add_subplot(111, projection='2d')
#




export_excel = df.to_excel (r'/home/rudi/Documents/import_excel/gen.xlsx', index = None, header=True)
export_excel_problem1 = dfProblem1.to_excel (r'/home/rudi/Documents/import_excel/problem1.xlsx', index = None, header=True)
export_excel_problem2 = dfProblem2.to_excel (r'/home/rudi/Documents/import_excel/problem2.xlsx', index = None, header=True)
