#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 22:43:52 2019

@author: rudi
"""

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
tau=12

g=np.array(dataCapacity['fixed cost plant'].dropna(how='any'))
v=np.array(dataCapacity['fixed cost dc'].dropna(how='any'))

##weight =np.random.dirichlet(np.ones(3), size=1)
weight=np.array([[0.36459012, 0.31979052, 0.31561936]])
r=[0.36026144, 0.63973856]
the_number_of_generation=20

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

population=np.array([[None]*3]*10)
for x in range(10):
    for y in range(3):
        if y==0:
            population[x][y]=random.sample(stage1, len(stage1))
        elif y==1:
            population[x][y]=random.sample(stage2, len(stage2))
        else:
            for z in range(len(d)):
                stage3[z]=random.randint(1,len(dc))
            population[x][y]=copy.deepcopy(stage3)
            
print(population.tolist())