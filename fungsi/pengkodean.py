#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 11:57:16 2020

@author: rudi

decoding file
"""

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
from genetic_algorithm import evaluate_problem2
#from genetic_algorithm import roulettewheelSelection
from genetic_algorithm import enc_pop
#from genetic_algorithm import check_integer_enc
from decoding_stage_1 import stage_1
import copy
data_Path = '/home/rudi/Documents/skripsi/sementonasa.xlsx'

data_kapasitas_pabrik = pd.read_excel(data_Path,sheet_name='kapasitas pabrik')
dataKapasitasPengantongan = pd.read_excel(data_Path, sheet_name="kapasitas pengantongan")
dataBanyakPermintaan = pd.read_excel(data_Path, sheet_name="permintaan")
pemasok = ['pemasok1']
pabrik = np.array(data_kapasitas_pabrik['Nama Pabrik'].dropna(how='any'))
pengantongan = np.array(dataKapasitasPengantongan['Nama UP'].dropna(how='any'))
distributor =np.array(dataBanyakPermintaan['nama distributor'].dropna(how='any'))
sups = [5980000]
plant = np.array(data_kapasitas_pabrik['Kapasitas'])
up = np.array(dataKapasitasPengantongan['Kapasitas'])
distri = np.array(dataBanyakPermintaan['banyak permintaan'])

t = np.array([[30247.84864, 30247.84864, 30247.84864, 30247.84864]])

dataBiayaKirim2= pd.read_excel(data_Path, sheet_name="pabrik ke pengantongan 2")
a=np.array(dataBiayaKirim2.iloc[:,1:3])

#dataBiayaKirim3= pd.read_excel(data_Path, sheet_name="Biaya Kirim dari Pengantongan").transpose().loc['biaya per ton dari Beringkassi':'Biaya perton dari makasar',:]
dataBiayaKirim3 = pd.read_excel(data_Path, sheet_name="pengantongan ke distributor")
c=np.array(dataBiayaKirim3.iloc[:,1:29])
#dataBiayaTahunan= pd.read_excel(data_Path, sheet_name="annual cost")
g = [0]*len(plant)
v = [0]*len(up)


#h= np.array(dataBiayaKirim3.iloc[:,1:28])
tau=12

###weight =np.random.dirichlet(np.ones(3), size=1)
weight=np.array([[0.36459012, 0.31979052, 0.31561936]])
r=[0.36026144, 0.63973856]

population=[[[5, 2, 3, 1, 4], [5, 4, 6, 1, 2, 3], [2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2]]]
decode_population_pembanding =[0]*len(population)
for x in range(len(population)):
    decode_population_pembanding[x]=stage_1(pemasok, pabrik, pengantongan, distributor, 1, sups,plant, up, distri,population[x][0],population[x][1],population[x][2],t,a).decode()    

greatPopulation2 = evaluate_problem2(decode_population_pembanding, sups, plant, up, distri, t,a,c, g,v, r[0],r[1],0.5,0.5)

print(decode_population_pembanding)

         0     31800\\39800         0\\0     28900\\29870         0\\0     29100\\22000         0\\30500         0\\29400         0\\41002         0\\0     39800\\19780         0\\0     21000\\0     44000\\0     24000\\0     27890\\20200         0\\0     30160\\0     44000\\0     15900\\47800         0\\0     16900\\0     30800\\0     33100\\37200         0\\0     38200\\0     34800\\0     35000\\0      7000