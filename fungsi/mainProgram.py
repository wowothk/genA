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

"""
from susahnya_stage2 import create
import sys
sys.path.insert(0, '/home/rudi/Documents/skripsi')
from encode import priority_based_enc
from encode import integer_encoding
import numpy as np
from dummy import add_dummy
from population import create_population
from evaluation_funtion import evaluation
from genetic_algorithm import crossover
import random
from genetic_algorithm import parentMutation
from genetic_algorithm import swapMutation
from genetic_algorithm import integerMutation
from decoding_stage_1 import stage_1

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

# initialization
population = create_population(5,supplier,plant, dc, customer, sups, D, W,d,2,2)
encoding_population=[None]*len(population)
for i in range(len(population)):
    p = population[i][3].copy()
    z = population[i][4].copy()
    for j in range(3):
        if j == 0:
            capacity = sups.copy()
            demand = D.copy()
            for m in range(len(plant)):
                demand[m] = sum(population[i][j+1][m])*p[m]#salah di sini begitupun pada yang bawah mengingat demand itu ditentukan oleh permintaan customer
            plant_with_dummy=add_dummy(supplier, plant, capacity, demand, t, population[i][j])
            shipment_with_dummy  = plant_with_dummy[0]
            cost_with_dummy = plant_with_dummy[1]
            depot_with_dummy =plant_with_dummy[2]
            demand_with_dummy = plant_with_dummy[3]
#            print(plant_with_dummy)
            v1 = priority_based_enc(supplier,depot_with_dummy, capacity, demand_with_dummy, cost_with_dummy, shipment_with_dummy).encoding()
        elif j == 1:
            capacity = D.copy()
            for k in range(len(plant)):
                capacity[k] = capacity[k]*p[k]
            demand = W.copy()
            for m in range(len(dc)):
                demand[m] = sum(population[i][j+1][m])*z[m]
            dc_with_dummy=add_dummy(plant, dc, capacity, demand, a, population[i][j])
            shipment_with_dummy  = dc_with_dummy[0]
            cost_with_dummy = dc_with_dummy[1]
            depot_with_dummy =dc_with_dummy[2]
            demand_with_dummy = dc_with_dummy[3]
            v2 = priority_based_enc(plant, depot_with_dummy, capacity, demand_with_dummy, cost_with_dummy, shipment_with_dummy).encoding()
        else:
            temp_customer = customer.copy()
            capacity = W.copy()
            temp_cost = c.copy()
            for m in range(len(dc)):
                capacity[m] = capacity[m]*z[m]
            demand = d.copy()
            temp = [0]*len(W)
            population_aksen = population[i][j].copy()
            for x in range(len(W)):
                if (capacity[x] - sum(population[i][j][x])) > 0:
                    temp[x] = capacity[x] - sum(population[i][j][x])
            if sum(temp) != 0:
                temp_customer.append("dummy")
                demand.append(sum(temp))
                temp_cost = np.append(temp_cost, np.array([[0]*len(W)]).T,1)
                population_aksen = np.append(population_aksen, np.array([temp]).T,1)
#            print(population[i][j])
#            print(population_aksen)
            v3 = integer_encoding(dc, temp_customer, capacity, d,temp_cost,population_aksen).encode()
    
    encoding_population[i] = [v1,v2,v3]
###########b, f, q, p, z
# evaluation
g=[4,5,6]
v=[3,7,5,6]
eval_mu = [None]*len(population)
weight =np.random.dirichlet(np.ones(3), size=1)
for i in range(len(population)):
    function1 = evaluation(population[i][0],population[i][1],population[i][2], sups, D, W, d, t, a, c, g,v, population[i][3],population[i][4], 0.8, 0.8).func1()
    function2 = evaluation(population[i][0],population[i][1],population[i][2], sups, D, W, d, t, a, c, g,v, population[i][3],population[i][4], 0.8, 0.8).func2()
    function3 = evaluation(population[i][0],population[i][1],population[i][2], sups, D, W, d, t, a, c, g,v, population[i][3],population[i][4], 0.8, 0.8).func3()
    eval_mu[i] = weight[0][0]*function1-weight[0][1]*function2+weight[0][2]*function3

### crossover
mu = encoding_population.copy()
lambdas = encoding_population.copy()
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

### mutation
random_mutation = [0]*len(lambdas)
for i in range(len(random_mutation)):
    random_mutation[i] = random.random()
index_parent = parentMutation(random_mutation, 0.2)

random_individu = random.randint(0,2)
for x in range(len(index_parent)):
    if random_individu % 2 == 0:
        lambdas[x][0] = swapMutation(lambdas[x][0])
        lambdas[x][2] = integerMutation(lambdas[x][2], len(dc))
    else:
        lambdas[x][1] = swapMutation(lambdas[x][1])

### selection
## rubah lambda dan mu menjadi set
temp=[]
temp_lambdas=lambdas.copy()
for x in range(len(lambdas)):
    for y in range(len(mu)):
        if lambdas[x] == mu[y]:
            temp.append(x)
            break# make element unique
for l in range(len(temp)):
    lambdas.remove(temp_lambdas[temp[l]])    
print('parents :', mu)
print('childs  :', lambdas)
mupluslambda = mu + lambdas
for x in range(len(mupluslambda)):
    mupluslambda[x]=stage_1(supplier, plant, dc, customer, 1, sups, D, W, d,mupluslambda[x][0],mupluslambda[x][1],mupluslambda[x][2],t,a).decode()
