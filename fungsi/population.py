#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 13:31:08 2019

@author: rudi
create population

"""
from susahnya_stage2 import create
import sys
sys.path.insert(0, '/home/rudi/Documents/skripsi')
from encode import priority_based_enc
from encode import integer_encoding
import numpy as np
from dummy import add_dummy
def  create_population(the_number_of_population, supplier, plant, dc, customer,S,K,J,I, maks_plant, maks_dc):
    population = [None]*the_number_of_population
    for i in range(the_number_of_population):
        create_population = create(supplier, plant, dc, customer,S,K,J,I, maks_plant, maks_dc).supplier_to_plant()
        population[i]= create_population[0:5]
        
    return population

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

population = create_population(5,supplier,plant, dc, customer, sups, D, W,d,2,2)
#print(population[1][4])
#### coba encoding 3 stage ####
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
    
    encoding_population[i] = v1+v2+v3
###########

for i in range(len(population)):
    print('populasi ke-',i)
    print(population[i])
    print(encoding_population[i])