# Comparisons the number of populations


import sys
sys.path.insert(0, '/home/rudi/Documents/skripsi')
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
from genetic_algorithm import enc_pop
from decoding_stage_1 import stage_1
import copy
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import re

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

dataBiayaKirim3 = pd.read_excel(data_Path, sheet_name="pengantongan ke distributor")
c=np.array(dataBiayaKirim3.iloc[:,1:29])
g = [0]*len(plant)
v = [0]*len(up)
r=[0.36026144, 0.63973856]

file1 = open("semenfix.txt", "w+")
# initialization
stage1=[]
for x in range(len(sups)+len(plant)):
    stage1.append(x+1)
stage2=[]
for x in range(len(up)+len(plant)):
    stage2.append(x+1)
stage3=[None]*len(distri)
for x in range(len(distri)):
    stage3[x]=random.randint(1,len(up))

population=np.array([[None]*3]*1000)
for x in range(1000):
    for y in range(3):
        if y==0:
            population[x][y]=random.sample(stage1, len(stage1))
        elif y==1:
            population[x][y]=random.sample(stage2, len(stage2))
        else:
            for z in range(len(distri)):
                stage3[z]=random.randint(1,len(up))
            population[x][y]=copy.deepcopy(stage3)

population = [list(x) for x in population]

population =[[[2, 4, 5, 1, 3],
  [1, 4, 6, 5, 3, 2],
  [2,1,1,2,1,2,1,1,2,2,1,1,2,2,1,1,1,2,2,1,1,1,1,1,1,1,2,2]],
 [[3, 5, 4, 2, 1],
  [4, 1, 6, 3, 2, 5],
  [1,2,2,2,1,1,1,1,1,1,2,1,2,2,1,2,1,1,1,1,2,1,1,2,1,2,2,1]],
 [[5, 4, 2, 1, 3],
  [6, 3, 1, 2, 4, 5],
  [1,2,2,2,1,2,2,1,2,1,2,2,1,1,1,2,1,1,1,2,2,2,1,2,2,2,2,1]],
 [[3, 5, 1, 4, 2],
  [1, 5, 2, 4, 3, 6],
  [1,1,2,1,2,2,2,2,2,1,2,1,1,2,2,1,2,2,1,2,1,2,2,2,1,2,1,2]],
 [[1, 2, 5, 4, 3],
  [5, 1, 2, 6, 3, 4],
  [2,2,2,2,2,1,2,1,2,2,2,1,1,2,1,2,2,2,1,1,2,2,1,2,1,2,2,2]],
 [[4, 5, 3, 1, 2],
  [4, 3, 1, 6, 5, 2],
  [2,1,1,2,1,1,2,2,2,1,1,1,2,1,2,2,1,2,1,1,1,1,2,2,2,1,2,2]],
 [[2, 1, 3, 5, 4],
  [2, 6, 3, 5, 1, 4],
  [1,1,2,2,2,1,1,2,1,1,1,1,1,1,1,2,2,1,1,1,2,2,2,2,1,2,1,2]],
 [[4, 5, 2, 3, 1],
  [2, 3, 5, 4, 6, 1],
  [2,2,1,2,1,2,2,2,1,2,1,1,1,1,1,1,1,2,1,2,1,2,2,2,1,1,2,1]],
 [[5, 2, 3, 4, 1],
  [6, 3, 5, 4, 1, 2],
  [1,2,1,1,1,2,2,2,1,2,1,1,1,1,2,1,1,1,2,2,2,2,2,1,2,1,1,1]],
 [[5, 2, 1, 3, 4],
  [4, 5, 6, 2, 3, 1],
  [1,2,2,2,1,1,1,1,1,2,1,2,1,2,2,1,1,1,1,1,1,2,2,1,1,1,2,1]]]

decode_population_pembanding =[0]*len(population)
for x in range(len(population)):
    decode_population_pembanding[x]=stage_1(pemasok, pabrik, pengantongan, distributor, 1, sups,plant, up, distri,population[x][0],population[x][1],population[x][2],t,a).decode()    

greatPopulation2 = evaluate_problem2(decode_population_pembanding, sups, plant, up, distri, t,a,c, g,v, r[0],r[1],0.5,0.5)

df = pd.DataFrame({
        "generasi": 1,
        "f1":[greatPopulation2[1][greatPopulation2[0].index(min(greatPopulation2[0]))]],    
        "f2":[greatPopulation2[2][greatPopulation2[0].index(min(greatPopulation2[0]))]],
        "Optimal":[greatPopulation2[0][greatPopulation2[0].index(min(greatPopulation2[0]))]]})

generations = [(i+1)*100 for i in range(20)]

for gen in generations:
    print(gen)
    for iteration in range(10):
        mu = copy.deepcopy(population)
        lambdas =copy.deepcopy(population)
        generation = 0
        the_number_of_generation=gen
        while generation < the_number_of_generation:  
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
                    lambdas[index_parent[x]][2] = integerMutation(lambdas[index_parent[x]][2], len(pengantongan))
                else:
                    lambdas[index_parent[x]][1] = swapMutation(lambdas[index_parent[x]][1])
            mupluslambda = mu + lambdas
            
            decode_mupluslambda=copy.deepcopy(mupluslambda)
            #### selection
            for x in range(len(mupluslambda)):
                decode_mupluslambda[x]=stage_1(pemasok, pabrik, pengantongan, distributor, 1, sups, plant, up, distri,mupluslambda[x][0],mupluslambda[x][1],mupluslambda[x][2],t,a).decode()
            
            evaluate = evaluate_problem2(decode_mupluslambda,sups, plant, up,distri,t,a,c,g,v,r[0],r[1],0.5,0.5)
            eval_mupluslambda=evaluate[0]
            newPopulation=[]
            best_selection = sorted(list(dict.fromkeys(eval_mupluslambda)))

            if len(mu) == len(best_selection):
                for i in best_selection:
                    newPopulation.append(mupluslambda[eval_mupluslambda.index(i)])

            else:
                newPopulation = [mupluslambda[eval_mupluslambda.index(i)] for i in best_selection[0:2]]
                pop = randomPopulation(len(sups),len(plant),len(pengantongan),len(distributor), len(mu)-len(newPopulation))        
                for i in pop:
                    newPopulation.append(i)

            decode_population =[0]*len(population)
            for x in range(len(population)):
                decode_population[x]=stage_1(pemasok, pabrik, pengantongan, distributor, 1, sups,plant, up, distri,newPopulation[x][0],newPopulation[x][1],newPopulation[x][2],t,a).decode()    
            greatPopulation200 = evaluate_problem2(decode_population,sups, plant, up,distri,t,a,c,g,v,r[0],r[1],0.5,0.5)
            
            if (generation+1)%100==0:  
                df200 = pd.DataFrame({
                                        "generasi":generation+1,
                                        "f1":[greatPopulation200[1][greatPopulation200[0].index(min(greatPopulation200[0]))]],
                                        "f2":[greatPopulation200[2][greatPopulation200[0].index(min(greatPopulation200[0]))]],
                                        "Optimal":[greatPopulation200[0][greatPopulation200[0].index(min(greatPopulation200[0]))]]})
                    
                df = df.append(df200, ignore_index=True)

            mu = copy.deepcopy(newPopulation)
            lambdas = copy.deepcopy(mu)   
            generation = generation + 1


export_excel = df.to_excel (r'/home/rudi/Documents/skripsi/populasimore.xlsx', index = None, header=True)