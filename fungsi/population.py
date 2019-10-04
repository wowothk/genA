#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 13:31:08 2019

@author: rudi
create population

"""
from susahnya_stage2 import create
def  create_population(the_number_of_population, supplier, plant, dc, customer,S,K,J,I, maks_plant, maks_dc):
    population = [None]*the_number_of_population
    for i in range(the_number_of_population):
        create_population = create(supplier, plant, dc, customer,S,K,J,I, maks_plant, maks_dc).supplier_to_plant()
        population[i]= create_population[0:3]
        
    return population

supplier = ["s1","s2","s3"]
plant = ["p1","p2","p3"]
dc = ["dc1","dc2","dc3","dc4"]
customer =["cust1","cust2", "cust3","cust4"]

sups =[250,200,250]
D = [200,150,200] 
W = [150, 100, 200, 100]
d = [50, 100, 50, 100]

print(create_population(5,supplier,plant, dc, customer, sups, D, W,d,2,2))
