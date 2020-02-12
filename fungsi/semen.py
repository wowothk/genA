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
from genetic_algorithm import evaluate_problem2
#from genetic_algorithm import roulettewheelSelection
from genetic_algorithm import enc_pop
#from genetic_algorithm import check_integer_enc
from decoding_stage_1 import stage_1
import copy
data_Path = '/home/rudi/Documents/import_excel/ringkasan semen.xlsx'

dataName = pd.read_excel(data_Path,sheet_name='Naming')
pemasok = np.array(dataName['Pemasok'].dropna(how='any'))
pabrik = np.array(dataName['pabrik'].dropna(how='any'))
pengantongan = np.array(dataName['pengantongan'].dropna(how='any'))
distributor =np.array(dataName['Distributor'].dropna(how='any'))

dataKapasitasPemasok = pd.read_excel(data_Path, sheet_name="kapasitas pemasok")
sups = np.array(dataKapasitasPemasok['kapasitas'])
dataKapasitasPabrik = pd.read_excel(data_Path, sheet_name="Kapasitas Pabrik")
plant = np.array(dataKapasitasPabrik['Kapasitas'])
dataKapasitasPengantongan = pd.read_excel(data_Path, sheet_name="Kapasitas Unit Pengantongan")
up = np.array(dataKapasitasPengantongan['Kapasitas'])
dataBanyakPermintaan = pd.read_excel(data_Path, sheet_name="Banyak Permintaan")
distri = np.array(dataBanyakPermintaan['Permintaan'][0:24])
dataBiayaKirim1= pd.read_excel(data_Path, sheet_name="Biaya Kirim dari Pemasok")
t=np.array(dataBiayaKirim1.iloc[:,1:5])

dataBiayaKirim2= pd.read_excel(data_Path, sheet_name="Biaya Kirim dari Pabrik")
a=np.array(dataBiayaKirim2.iloc[:,1:3])
dataBiayaKirim3= pd.read_excel(data_Path, sheet_name="Biaya Kirim dari Pengantongan").transpose().loc['biaya per ton dari Beringkassi':'Biaya perton dari makasar',:]
c=np.array(dataBiayaKirim3.iloc[:,0:25])

dataBiayaTahunan= pd.read_excel(data_Path, sheet_name="annual cost")
g = np.array(dataBiayaTahunan['pabrik'].dropna(how='any'))
v = np.array(dataBiayaTahunan['pengantongan'].dropna(how='any'))


h= np.array(pd.read_excel(data_Path, sheet_name='waktu distribusi').transpose().loc['Up Biringkasi':'Up Makassar',:].iloc[:,0:25])
tau=12

###weight =np.random.dirichlet(np.ones(3), size=1)
weight=np.array([[0.36459012, 0.31979052, 0.31561936]])
r=[0.36026144, 0.63973856]


# initialization
#stage1=[]
#for x in range(len(sups)+len(plant)):
#    stage1.append(x+1)
#stage2=[]
#for x in range(len(up)+len(plant)):
#    stage2.append(x+1)
#stage3=[None]*len(distri)
#for x in range(len(distri)):
#    stage3[x]=random.randint(1,len(up))
#
#population=np.array([[None]*3]*10)
#for x in range(10):
#    for y in range(3):
#        if y==0:
#            population[x][y]=random.sample(stage1, len(stage1))
#        elif y==1:
#            population[x][y]=random.sample(stage2, len(stage2))
#        else:
#            for z in range(len(distri)):
#                stage3[z]=random.randint(1,len(up))
#            population[x][y]=copy.deepcopy(stage3)
#
#population = [list(x) for x in population]
population=[[[3, 4, 2, 1, 5],
      [1, 5, 6, 3, 2, 4],
      [1, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 2, 1, 2, 2, 2, 2, 1, 2, 1, 1, 2]],
     [[1, 5, 4, 2, 3],
      [5, 6, 3, 1, 2, 4],
      [1, 1, 1, 1, 2, 2, 2, 2, 1, 2, 1, 1, 1, 2, 1, 2, 2, 1, 2, 1, 1, 1, 2, 2]],
     [[3, 4, 1, 2, 5],
      [1, 2, 3, 6, 4, 5],
      [1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1]],
     [[4, 5, 1, 2, 3],
      [4, 1, 5, 6, 3, 2],
      [2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 1, 2, 2, 1, 2, 2, 2, 1, 2, 1]],
     [[5, 2, 1, 3, 4],
      [5, 1, 2, 4, 3, 6],
      [2, 2, 1, 2, 2, 2, 1, 1, 2, 1, 2, 2, 2, 1, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2]],
     [[2, 4, 1, 5, 3],
      [5, 6, 4, 2, 3, 1],
      [2, 1, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 1, 2, 2, 1, 2, 1]],
     [[1, 2, 3, 5, 4],
      [3, 5, 4, 6, 1, 2],
      [2, 2, 1, 2, 2, 1, 1, 1, 2, 2, 2, 2, 1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1]],
     [[3, 5, 1, 4, 2],
      [4, 1, 3, 6, 5, 2],
      [2, 2, 2, 1, 2, 1, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1, 2, 2, 1, 1, 2, 1, 2]],
     [[4, 2, 5, 1, 3],
      [4, 1, 6, 2, 3, 5],
      [2, 1, 1, 2, 1, 2, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2]],
     [[2, 5, 1, 3, 4],
      [2, 6, 5, 3, 4, 1],
      [2, 2, 2, 2, 1, 2, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 2, 1]]]
     
decode_population_pembanding =[0]*len(population)
for x in range(len(population)):
    decode_population_pembanding[x]=stage_1(pemasok, pabrik, pengantongan, distributor, 0.98, sups,plant, up, distri,population[x][0],population[x][1],population[x][2],t,a).decode()    

greatPopulation2 = evaluate_problem2(decode_population_pembanding,sups, plant, up,distri,t,a,c,g,v,r[0],r[1],0.5,0.5, h, tau)

df = pd.DataFrame({
        "f1":[greatPopulation2[1][greatPopulation2[0].index(min(greatPopulation2[0]))]],
#        "f2":[greatPopulation2[2][greatPopulation2[0].index(min(greatPopulation2[0]))]],
        "f2":[greatPopulation2[2][greatPopulation2[0].index(min(greatPopulation2[0]))]],
        "Optimal":[greatPopulation2[0][greatPopulation2[0].index(min(greatPopulation2[0]))]]})


#    print(the_number_of_generation)
    #encoding_population = enc_pop(population, supplier, plant, dc, customer, sups, D, W, d, t, a, c)
mu = copy.deepcopy(population)
lambdas =copy.deepcopy(population)
the_number_of_generation=2000
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
        children = crossover(lambdas[index_parent[x][0]], lambdas[index_parent[x][1]], sups, up, plant, distri)
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
            lambdas[index_parent[x]][2] = integerMutation(lambdas[index_parent[x]][2], len(up))
        else:
            lambdas[index_parent[x]][1] = swapMutation(lambdas[index_parent[x]][1])
    mupluslambda = mu + lambdas
    decode_mupluslambda=copy.deepcopy(mupluslambda)
    
#### selection
    
    for x in range(len(mupluslambda)):
        decode_mupluslambda[x]=stage_1(pemasok, pabrik, pengantongan, distributor, 0.98, sups, plant, up, distri,mupluslambda[x][0],mupluslambda[x][1],mupluslambda[x][2],t,a).decode()
    eval_mupluslambda=evaluate_alternative(decode_mupluslambda,sups, plant, up,distri,t,a,c,g,v,r[0],r[1],weight[0][0],weight[0][1],weight[0][2], h, tau)[0]
    newPopulation=[]
    
    #dict.fromkeys() digunakan untuk membuat list tidak terdapat duplikat
#    print('tipe data eval_mu', type(eval_mupluslambda))
    best_selection = sorted(list(dict.fromkeys(eval_mupluslambda)))[0:2]
    afterSelectBest = copy.deepcopy(mupluslambda)
    for i in range(len(best_selection)):
        newPopulation.append(mupluslambda[eval_mupluslambda.index(best_selection[i])])
        afterSelectBest.remove(mupluslambda[eval_mupluslambda.index(best_selection[i])])    
        
    decode_afterSelectBest =[0]*len(afterSelectBest)
    for x in range(len(afterSelectBest)):
        decode_afterSelectBest[x]=stage_1(pemasok, pabrik, pengantongan, distributor, 0.98, sups, plant, up, distri,afterSelectBest[x][0],afterSelectBest[x][1],afterSelectBest[x][2],t,a).decode()
#    print('rolet')
    eval_afterSelectBest = evaluate_alternative(decode_afterSelectBest,sups, plant, up,distri,t,a,c,g,v,r[0],r[1],weight[0][0],weight[0][1], weight[0][2], h, tau)[0] 
    
    bestOf = list(dict.fromkeys(eval_afterSelectBest))
    if len(bestOf) == len(mu)-len(newPopulation):
        for i in range(len(bestOf)):
            newPopulation.append(mupluslambda[eval_mupluslambda.index(best_selection[i])])
    else:
        pop = randomPopulation(len(sups),len(pabrik),len(pengantongan),len(distributor), len(mu)-len(newPopulation))        
        for i in range(len(pop)):
            newPopulation.append(pop[i])
    
    if generation > 1000 and generation%(10)==0:
        print("GENERASI  ", generation)
        decode_population_cek =[0]*len(population)
        for x in range(len(population)):
            decode_population_cek[x]=stage_1(pemasok, pabrik, pengantongan, distributor, 0.98, sups,plant, up, distri,newPopulation[x][0],newPopulation[x][1],newPopulation[x][2],t,a).decode()    
        
        greatPopulation200 = evaluate_problem2(decode_population_cek,sups, plant, up,distri,t,a,c,g,v,r[0],r[1],0.5,0.5, h, tau)
        
        df200 = pd.DataFrame({
                "f1":[greatPopulation200[1][greatPopulation200[0].index(min(greatPopulation200[0]))]],
#                "f2":[greatPopulation200[2][greatPopulation200[0].index(min(greatPopulation200[0]))]],
                "f3":[greatPopulation200[2][greatPopulation200[0].index(min(greatPopulation200[0]))]],
                "Optimal":[greatPopulation200[0][greatPopulation200[0].index(min(greatPopulation200[0]))]]})
        
        df = df.append(df200, ignore_index=True)
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
#    decode_population3 =[0]*len(newPopulation)
#    for x in range(len(newPopulation)):
#        decode_population3[x]=stage_1(pemasok, pabrik, pengantongan, distributor, 0.98, sups, plant, up, distri,newPopulation[x][0],newPopulation[x][1],newPopulation[x][2],t,a).decode()
#    greatPopulation3 = evaluate_alternative(decode_population3,sups, plant, up,distri,t,a,c,g,v,r[0],r[1],weight[0][0],weight[0][1],weight[0][2], h, tau)
#    print(greatPopulation3[4])
##    dummyVariable =[0]*10
#    for i in range(10):
#        print(greatPopulation3[5][i], greatPopulation3[6][i], greatPopulation3[7][i])
#    
#        print("##### pareto as single", i)
#        print(greatPopulation3[5][i]-greatPopulation3[6][i]+greatPopulation3[7][i])
#    print("=============")
#    print(dummyVariable)
#    print(greatPopulation3[0], greatPopulation3[5], greatPopulation3[6], greatPopulation3[7])
    generation = generation + 1
    
    
decode_population =[0]*len(newPopulation)
for x in range(len(newPopulation)):
    decode_population[x]=stage_1(pemasok, pabrik, pengantongan, distributor, 0.98, sups, plant, up, distri,newPopulation[x][0],newPopulation[x][1],newPopulation[x][2],t,a).decode()    
decode_population2 =[0]*len(population)
for x in range(len(population)):
    decode_population2[x]=stage_1(pemasok, pabrik, pengantongan, distributor, 0.98, sups, plant, up, distri,population[x][0],population[x][1],population[x][2],t,a).decode()    

greatPopulation = evaluate_problem2(decode_population,sups, plant, up,distri,t,a,c,g,v,r[0],r[1],0.5,0.5, h, tau)
greatPopulation2 = evaluate_problem2(decode_population2,sups, plant, up,distri,t,a,c,g,v,r[0],r[1],0.5,0.5, h, tau)
#print("minimum fungsi satu", greatPopulation[1])
#print("maximum fungsi dua", greatPopulation[2])
#print("minimum fungsi satu", greatPopulation[3])
print(greatPopulation[0])
print(min(greatPopulation2[0]))
print("setelah operasi genetik ", min(greatPopulation[0]))
export_excel = df.to_excel (r'/home/rudi/Documents/import_excel/cobatenanan.xlsx', index = None, header=True)