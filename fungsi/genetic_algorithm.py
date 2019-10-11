#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 15:32:21 2019

@author: rudi
"""

import numpy as np
import random
from evaluation_funtion import evaluation
pop1 = [3,7,4,2,8,5,1,4,5,6,8,3,2,7,1,1,3,3,3]
pop2 = [1,4,5,6,7,3,2,8,1,3,5,7,6,4,2,1,3,2,2]

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
t = np.array([[4,3,1],[3,5,2],[1,6,4]])

z = [1, 0, 1, 0]
p = [1, 1, 0]
temp_w = [0]*len(z)
temp_d =[0]*len(p)
for i in range(len(D)):
    temp_d[i] = D[i]*p[i]
for j in range(len(W)):
    temp_w[j] = W[i]*z[i]
    
def spare(chromosom, sups, W, D, d):
    if sum(sups) - sum(D) > 0:
        len_v1=len(sups)+len(D)+1
    else:
        len_v1=len(sups)+len(D)
    v1=[0]*len_v1
    if sum(D) - sum(W)>0:
        len_v2=len(W)+len(D)+1
    else:
        len_v2=len(W)+len(D)
    v2=[0]*len_v2
    
    if sum(W) - sum(d)>0:
        len_v3=len(d)+1
    else:
        len_v3=len(d)
#    print('total ', len(d))
#    print(sum(temp_w))
#    print(sum(d))
#    print(len_v3)
    v3 = [0]*len_v3
        
    for x in range(len(chromosom)):
        if x < len_v1:
            v1[x]=chromosom[x]        
        elif len_v1 <= x and x < len_v1+len_v2:
            v2[x%len_v1] = chromosom[x]
        else:
            v3[x%(len_v1+len_v2)] = chromosom[x]
    return v1, v2, v3

def crossover(chromosom1, chromosom2, sups, W, D, d):
#    parent1 = list(spare(chromosom1, sups, W, D, d))
#    parent2 = list(spare(chromosom2, sups, W, D, d))
    parent1 = list(chromosom1)
    parent2 = list(chromosom2)
    temp=0
    for i in range(len(parent1)):
        if i%2 != 0:
            temp = parent1[i]
            parent1[i] = parent2[i]
            parent2[i] = temp
    children1=parent1.copy()
    children2=parent2.copy()
    return children1, children2

# dengan cara ini dapat dilakukan swap mutasi, tapi dengan cara ini akan
# terdapat mutasi secara terus menurus yang mana dia akan bertukar/swap pada setiap iterasi        
#def swapMutation(chromosom, mutationRate):
#    for swapped in range(len(chromosom)):
#        if(random.random() < mutationRate):
#            swapWith = int(random.random() * len(chromosom))
#            
#            gen1 = chromosom[swapped]
#            gen2 = chromosom[swapWith]
#            
#            chromosom[swapped] = gen2
#            chromosom[swapWith] = gen1
#    return chromosom
### versi kak mei
def swapMutation(chromosom):
    gen1 = int(random.random()*len(chromosom))
    gen2 = int(random.random()*len(chromosom))
    while gen2==gen1:
        gen2 = int(random.random()*len(chromosom))
    temp =chromosom[gen1]
    chromosom[gen1] =chromosom[gen2]
    chromosom[gen2] = temp
    return chromosom

#def integerMutation(chromosom, mutationRate, length_source):
#    for swapped in range(len(chromosom)):
#        if (random.random() < mutationRate):
#            swapWith = random.randint(1,length_source)
#            while chromosom[swapped]==swapWith:
#                swapWith = random.randint(1,length_source)
#            chromosom[swapped] = swapWith
#    return chromosom
    
def integerMutation(chromosom, length_source):
    gen = int(random.random()*len(chromosom))
    changeWith = random.randint(1, length_source)
    while changeWith == chromosom[gen]:
        changeWith = random.randint(1, length_source)
    chromosom[gen] = changeWith
    return chromosom

def parentCrossover(nilai_random, crossoverRatio):
    find_pair = []
    pair=[]
    for i in range(len(nilai_random)):
        if nilai_random[i] < crossoverRatio:
            find_pair.append(i)
            if len(find_pair) == 2:
                pair.append(find_pair)
                find_pair =[]
    return pair

def parentMutation(random_value, mutationRatio):
    parent=[]
    for i in range(len(random_value)):
        if random_value[i] < mutationRatio:
            parent.append(i)
    return parent

def mulambdaSelection(mu,plusLambda, sups, D, W, d, t, a, c,g,v,r1, r2, weight1, weight2, weight3):
    evalMu = [0]*len(mu)
    for x in range(len(mu)):
        func1 = evaluation(mu[x][0],mu[x][1],mu[x][2], sups, D, W, d, t,a,c,g,v,mu[x][3], mu[x][4], mu[x][5],mu[x][6], r1, r2).func1()
        func2 = evaluation(mu[x][0],mu[x][1],mu[x][2], sups, D, W, d, t,a,c,g,v,mu[x][3], mu[x][4], mu[x][5],mu[x][6], r1, r2).func2()
        func3 = evaluation(mu[x][0],mu[x][1],mu[x][2], sups, D, W, d, t,a,c,g,v,mu[x][3], mu[x][4], mu[x][5],mu[x][6], r1, r2).func3()
        evalMu[x] = weight1*func1+weight2*func2+weight3*func3
    evalPlusLambda = [0]*len(plusLambda)
    for y in range(len(plusLambda)):
        func1 = evaluation(plusLambda[x][0],plusLambda[x][1],plusLambda[x][2], sups, D, W, d, t,a,c,g,v,plusLambda[x][3], plusLambda[x][4], plusLambda[x][5],plusLambda[x][6], r1, r2).func1()
        func2 = evaluation(plusLambda[x][0],plusLambda[x][1],plusLambda[x][2], sups, D, W, d, t,a,c,g,v,plusLambda[x][3], plusLambda[x][4], plusLambda[x][5],plusLambda[x][6], r1, r2).func2()
        func3 = evaluation(plusLambda[x][0],plusLambda[x][1],plusLambda[x][2], sups, D, W, d, t,a,c,g,v,plusLambda[x][3], plusLambda[x][4], plusLambda[x][5],plusLambda[x][6], r1, r2).func3()
        evalPlusLambda[x] = weight1*func1+weight2*func2+weight3*func3
    elite = [] # yang dimasukkan ke elite adalah parent atau lambda
    temporary = evalMu + evalPlusLambda
    while len(temporary) !=0:
        index_max_value = np.where(np.array(temporary)==max(temporary))[0][0]
        
        if index_max_value < len(evalMu):
            elite.append(mu[np.where(np.array(evalMu)==max(temporary))[0][0]])
        else:
            elite.append(mu[np.where(np.array(evalPlusLambda)==max(temporary))[0][0]])       
        temporary.remove(max(temporary))
    
    return elite
def roulettewheelSelection(population, sups, D, W, d, t, a, c, g ,v,r1, r2, weight1, weight2, weight3):
    evalPopulation = [0]*len(population)
    for x in range(len(population)):
        func1 = evaluation(population[x][0],population[x][1],population[x][2], sups, D, W, d, t,a,c,g,v,population[x][3], population[x][4], population[x][5],population[x][6], r1, r2).func1()
        func2 = evaluation(population[x][0],population[x][1],population[x][2], sups, D, W, d, t,a,c,g,v,population[x][3], population[x][4], population[x][5],population[x][6], r1, r2).func2()
        func3 = evaluation(population[x][0],population[x][1],population[x][2], sups, D, W, d, t,a,c,g,v,population[x][3], population[x][4], population[x][5],population[x][6], r1, r2).func3()
        evalPopulation[x] = weight1*func1+weight2*func2+weight3*func3
    total_fitness = sum(evalPopulation)
    probabilityChromosom = [0]*len(evalPopulation)
    for k in range(len(probabilityChromosom)):
        probabilityChromosom[k] = evalPopulation[k]/total_fitness
    cumulativeProbability = [0]*len(evalPopulation)
    for k in range(len(probabilityChromosom)):
        if k == 0:
            cumulativeProbability[k] = probabilityChromosom[k]
        else:
            cumulativeProbability[k] = probabilityChromosom[k]+cumulativeProbability[k-1]
    
    newPopulation = [None]*len(population)
    for k in range(len(newPopulation)):
        rand = random.random()
        if rand <= cumulativeProbability[0]:
            newPopulation[k] = population[k]
        else:
            s=1
            while s<len(population):
                if rand <= cumulativeProbability[s] and rand > cumulativeProbability[s-1]:
                    newPopulation[k] = cumulativeProbability[s]
                    break
                s = s+1
            
    return newPopulation
            
#print(integerMutation([1,3,4,5,2], 5))

#spr = spare(pop1, sups, W, D, d)
#v1=spr[0]
#v2=spr[1]
#v3=spr[2]
#print(len(spr))
#print(v1)
#print(v2)
#print(v3)
#
#silang=crossover(pop1, pop2, sups, W, D, d)
#print('parent 1  :',silang[0])
#print('parent 2  :',silang[1])
#print('v1: ', v1, 'v2: ', v2, 'v3: ', v3)