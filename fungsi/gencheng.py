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
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
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
# from genetic_algorithm import evaluate_problem2
from genetic_algorithm import rouletteWheel
from genetic_algorithm import randomPopulation
from genetic_algorithm import sumOfNonDominated
from genetic_algorithm import evaluate_problem1
from genetic_algorithm import evaluate_problem2
#from genetic_algorithm import roulettewheelSelection
from genetic_algorithm import enc_pop
from genetic_algorithm import toBmatrix
from genetic_algorithm import ordered
#from genetic_algorithm import check_integer_enc
from decoding_stage_1 import stage_1
import copy
import re

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

h= np.array([[7,5,3,1],[2,4,6,5],[3,7,8,4],[9,3,2,1]])
tau=6
g=[40,50,60]
v=[30,70,50,60]

weight=np.array([[0.36459012, 0.31979052, 0.31561936]])
r=[0.36026144, 0.63973856]
the_number_of_generation=1000
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

# population=np.array([[None]*3]*5)
# for x in range(5):
#     for y in range(3):
#         if y==0:
#             population[x][y]=random.sample(stage1, len(stage1))
#         elif y==1:
#             population[x][y]=random.sample(stage2, len(stage2))
#         else:
#             for z in range(len(d)):
#                 stage3[z]=random.randint(1,len(dc))
#             population[x][y]=copy.deepcopy(stage3)
# population = [list(x) for x in population]   

######### documentation text
file1 = open("0109gencheng.txt", "w+")
file1.write("##################################\n")
file1.write("Inisialisasi\n")
population = [[[2, 1, 4, 3, 5, 6], [7, 3, 2, 1, 6, 4, 5], [1, 1, 1, 3]], [[4, 1, 2, 3, 6, 5],[5, 3, 6, 4, 7, 1, 2],[4, 3, 2, 3]],[[3, 2, 1,6, 5, 4],[1, 5, 3, 4, 6, 7, 2],[2, 1, 1,1]],[[1,2,6, 5, 3, 4],[1, 5, 7, 6, 3, 2, 4],[2, 2, 4, 1]], [[4, 3, 1, 2, 5, 6],[1, 7, 5, 2, 6, 4, 3],[4, 1, 4, 1]]]
for x in range(len(population)):
    file1.writelines("Individu "+str(x+1)+" & ")
    for y in population[x]:
        str_population = [str(z)+" " for z in y]
        file1.writelines(str_population)
    file1.write("\\\\"+"\n")
file1.write("##################################\n")
#########
 
         
#print(population)            
#population = [[[5, 7, 8, 2, 6, 3, 1, 4], [3, 5, 8, 7, 1, 6, 9, 4, 2], [5, 1, 1, 3, 3, 3, 6, 5, 2, 6, 6, 1, 6, 2, 6, 3, 6, 2, 1, 3, 5, 4, 1, 6, 6, 2, 1, 4, 2, 3, 1, 6, 5, 2, 1, 1, 3, 6, 2, 1, 5, 5, 5, 3, 1, 6, 5, 6, 6, 5, 5, 4, 6, 6, 1, 6, 1, 2, 1, 2, 3, 6, 5]], [[3, 8, 7, 6, 5, 4, 2, 1], [4, 2, 3, 1, 9, 8, 7, 6, 5], [6, 1, 2, 3, 4, 1, 4, 4, 2, 1, 2, 2, 1, 2, 1, 4, 4, 6, 5, 3, 4, 1, 2, 5, 4, 3, 5, 4, 2, 5, 1, 1, 2, 6, 4, 1, 6, 1, 2, 1, 1, 6, 6, 5, 4, 2, 6, 2, 4, 5, 2, 6, 6, 2, 1, 1, 5, 1, 2, 1, 6, 4, 4]], [[7, 5, 8, 1, 4, 6, 2, 3], [8, 3, 1, 5, 7, 4, 2, 9, 6], [1, 1, 6, 5, 1, 1, 4, 1, 6, 6, 6, 5, 1, 1, 3, 3, 3, 4, 3, 3, 3, 2, 5, 1, 6, 5, 3, 4, 4, 5, 2, 5, 6, 4, 3, 6, 4, 1, 2, 2, 2, 2, 3, 5, 4, 1, 6, 6, 5, 5, 4, 2, 2, 5, 4, 1, 1, 1, 5, 5, 2, 3, 6]], [[2, 3, 6, 1, 4, 5, 8, 7], [6, 1, 3, 2, 4, 7, 5, 8, 9], [5, 2, 2, 6, 5, 5, 1, 5, 3, 5, 3, 2, 5, 4, 1, 6, 4, 5, 4, 4, 1, 2, 4, 3, 4, 6, 6, 6, 5, 4, 3, 6, 6, 6, 1, 6, 4, 3, 2, 2, 4, 2, 1, 1, 1, 6, 4, 3, 3, 3, 2, 5, 3, 2, 2, 1, 1, 5, 2, 5, 6, 5, 5]], [[7, 4, 3, 2, 5, 1, 6, 8], [7, 2, 4, 3, 9, 1, 8, 6, 5], [3, 3, 2, 5, 6, 2, 5, 3, 2, 2, 1, 1, 5, 1, 6, 1, 3, 3, 5, 5, 1, 1, 6, 6, 3, 6, 3, 3, 1, 2, 5, 6, 2, 4, 6, 2, 4, 2, 2, 4, 4, 4, 4, 3, 5, 1, 6, 1, 3, 1, 4, 1, 2, 5, 2, 2, 3, 1, 4, 6, 2, 2, 2]], [[3, 4, 7, 8, 5, 2, 1, 6], [4, 9, 2, 3, 8, 5, 6, 1, 7], [5, 4, 1, 2, 1, 4, 3, 1, 1, 6, 2, 2, 3, 1, 3, 3, 4, 3, 5, 2, 3, 2, 1, 4, 2, 3, 4, 1, 1, 3, 4, 2, 2, 3, 3, 6, 1, 4, 4, 2, 4, 3, 2, 4, 1, 1, 6, 3, 2, 6, 5, 1, 2, 4, 2, 4, 6, 6, 4, 6, 2, 6, 4]], [[7, 1, 6, 2, 8, 4, 3, 5], [1, 5, 3, 2, 4, 8, 6, 9, 7], [2, 3, 3, 3, 1, 3, 2, 4, 2, 2, 6, 6, 3, 6, 6, 3, 4, 3, 4, 6, 4, 5, 5, 4, 2, 2, 1, 5, 3, 2, 5, 6, 2, 5, 1, 5, 1, 2, 2, 4, 1, 2, 2, 6, 6, 5, 3, 5, 1, 6, 3, 2, 2, 3, 4, 5, 4, 2, 4, 3, 2, 1, 2]], [[8, 3, 7, 2, 6, 1, 4, 5], [5, 1, 2, 7, 9, 6, 4, 8, 3], [6, 6, 2, 2, 3, 2, 2, 3, 3, 3, 2, 1, 2, 5, 6, 6, 4, 5, 2, 1, 2, 3, 5, 5, 2, 2, 2, 3, 4, 6, 3, 6, 4, 4, 3, 4, 5, 4, 3, 2, 1, 3, 5, 2, 3, 5, 6, 5, 1, 4, 2, 3, 5, 2, 4, 4, 6, 3, 1, 5, 5, 1, 5]], [[3, 5, 6, 7, 8, 1, 2, 4], [7, 5, 2, 9, 4, 3, 1, 6, 8], [6, 1, 5, 3, 4, 5, 6, 2, 6, 5, 6, 4, 6, 1, 3, 5, 3, 6, 4, 3, 1, 5, 6, 3, 5, 3, 1, 1, 2, 6, 6, 3, 1, 3, 3, 2, 6, 5, 1, 2, 1, 1, 3, 4, 3, 3, 6, 1, 5, 3, 4, 4, 5, 6, 6, 4, 2, 2, 4, 4, 4, 1, 1]], [[3, 1, 2, 8, 5, 7, 6, 4], [1, 9, 8, 3, 6, 4, 2, 5, 7], [1, 3, 3, 5, 6, 3, 1, 5, 3, 6, 6, 5, 5, 5, 1, 2, 6, 2, 5, 4, 6, 1, 5, 6, 1, 1, 5, 5, 3, 6, 1, 2, 1, 4, 5, 5, 1, 5, 4, 2, 1, 3, 4, 1, 4, 4, 1, 5, 3, 6, 3, 4, 3, 1, 2, 6, 5, 4, 3, 1, 4, 6, 2]]]
#
decode_population_pembanding =[0]*len(population)
for x in range(len(population)):
    decode_population_pembanding[x]=stage_1(supplier, plant, dc, customer, 1, sups, D, W, d,population[x][0],population[x][1],population[x][2],t,a).decode()    

greatPopulation2 = evaluate_problem2(decode_population_pembanding,sups, D, W,d,t,a,c,g,v,r[0],r[1],0.5,0.5)

df = pd.DataFrame({
        "generation":0,
        "f1":[greatPopulation2[1][greatPopulation2[0].index(min(greatPopulation2[0]))]],
        "f2":[greatPopulation2[2][greatPopulation2[0].index(min(greatPopulation2[0]))]],
#        "f3":[greatPopulation2[3][greatPopulation2[0].index(min(greatPopulation2[0]))]],
        "Optimal":[greatPopulation2[0][greatPopulation2[0].index(min(greatPopulation2[0]))]]})

################
file1.write("##################################\n")
file1.write("Inisialisasi decoding\n")

for x in decode_population_pembanding:
    file1.write(toBmatrix(x))

file1.write("##################################\n")
################
print(population)
mu = copy.deepcopy(population)
lambdas =copy.deepcopy(population)

generation = 0
#for generation in range(the_number_of_generation):
while generation < the_number_of_generation:
    print('iterasi   ', generation)
    ### crossover
    ############
    file1.write("##################################\n")
    file1.write("crossover dengan pc= 0.9\n")
    
    file1.write("1. random nilai\n")
    random_crossover=[0]*len(mu)
    temp=list()
    for i in range(len(lambdas)):
        random_crossover[i] = random.random()
        #
        file1.write('Individu '+str(i+1)+'&'+str(random_crossover[i])+"\\\\"+"\n")
        #
        if random_crossover[i]<0.9:
            temp.append(random_crossover[i])
    
    if len(temp)%2!=0:
        temp.remove(temp[random.randint(0,len(temp)-1)])
    #
    file1.write("2. parents \n")
    file1.write(str(temp)+"\n")
    
    parent = ordered(temp)
    index_parent = [[ np.where(np.array(random_crossover)==j)[0][0] for j in i ]for i in parent]

    for x in range(len(index_parent)):
        children = crossover(lambdas[index_parent[x][0]], lambdas[index_parent[x][1]], sups, W, D, d)
        lambdas[index_parent[x][0]]=children[0]
        lambdas[index_parent[x][1]]=children[1]

    ##output crossover
    file1.write("3. new population \n")
    
    for x in range(len(lambdas)):
        file1.writelines("Individu "+ str(x+1) +"& ")
        for y in lambdas[x]:
            str_population = [str(z)+" " for z in y]
            file1.writelines(str_population)
        file1.write("\\\\"+"\n")
    file1.write("##################################\n")
    ############
    
#    ### mutation
    file1.write("##################################\n")
    file1.write("mutasi dengan Pm = 0.1\n")
    file1.write("1. random nilai \n")
    random_mutation = [0]*len(lambdas)
    for i in range(len(random_mutation)):
        random_mutation[i] = random.random()
        
        file1.write('Individu '+str(i+1)+'&'+str(random_mutation[i])+"\\\\"+"\n")
        
    index_parent = parentMutation(random_mutation, 0.1)
    file1.write("2. parents \n")
    file1.write(str([i+1 for i in index_parent])+"\n")
    file1.write("3. pemilihan stage \n")
    random_individu = random.randint(0,2)
    for x in range(len(index_parent)):
        if random_individu % 2 == 0:
            file1.write("\n parent"+str(x)+"stage1 dan stage 3 \n")
            lambdas[index_parent[x]][0] = swapMutation(lambdas[index_parent[x]][0])
            file1.write("->stage1\n")
            file1.write(str(lambdas[index_parent[x]][0])+"\n")
            temp = copy.deepcopy(lambdas[index_parent[x]][2])
            lambdas[index_parent[x]][2] = integerMutation(lambdas[index_parent[x]][2], len(dc))
            file1.write("->stage3\n")
            file1.write(str(lambdas[index_parent[x]][2])+"\n")
        else:
            file1.write("parent"+str(x)+"stage 2 \n")
            lambdas[index_parent[x]][1] = swapMutation(lambdas[index_parent[x]][1])
            file1.write(str(lambdas[index_parent[x]][1])+"\n")

    ############
    file1.write("####populasi setelah dimutasi \n")
    for x in range(len(lambdas)):
        file1.writelines("Individu "+str(x+1)+" & ")
        for y in lambdas[x]:
            str_population = [str(z)+" " for z in y]
            file1.writelines(str_population)
        file1.write("\\\\"+"\n")
    file1.write("##################################\n")
    ############

    
    mupluslambda = mu + lambdas
    decode_mupluslambda=copy.deepcopy(mupluslambda)
    
    file1.write("####populasi mupluslmabda \n")
    for x in range(len(mupluslambda)):
        file1.writelines("Individu "+str(x+1)+" & ")
        for y in mupluslambda[x]:
            str_population = [str(z)+" " for z in y]
            file1.writelines(str_population)
        file1.write("\\\\"+"\n")
    file1.write("##################################\n")
#### selection
    
    for x in range(len(mupluslambda)):
        decode_mupluslambda[x]=stage_1(supplier, plant, dc, customer, 1, sups, D, W, d,mupluslambda[x][0],mupluslambda[x][1],mupluslambda[x][2],t,a).decode()
    
    evaluate = evaluate_problem2(decode_mupluslambda,sups, D, W,d,t,a,c,g,v,r[0],r[1],0.5,0.5)

    
    eval_mupluslambda= evaluate[0]
    newPopulation=[]
    
    ############
    file1.write("##################################\n")
    file1.write("decode muplus lambda\n")
    
    for x in decode_mupluslambda:
        file1.write(toBmatrix(x))
    file1.write("##################################\n")
    ############

    file1.write("& $f_{1}$ sebelum normal & $f_{2}$ sebelum normal \\\\\n")
    for x in range(len(evaluate[5])):        
        file1.write("Individu "+ str(x+1)+" & " +str(evaluate[1][x])+" & "+str(evaluate[2][x])+"\\\\\n")

    file1.write("##################################\n")

    file1.write("& $f_{1}$ setelah normal & $f_{2}$ setelah normal \\\\\n")
    for x in range(len(evaluate[5])):
        file1.write("Individu "+ str(x+1)+" & " +str(evaluate[4][x])+" & "+str(evaluate[5][x])+"\\\\\n")


    file1.write("##################################\n")
    
    file1.write("eval muplus lambda\n")
    
    for x in range(len(eval_mupluslambda)):
        file1.write("Individu "+str(x+1)+" & "+str(eval_mupluslambda[x])+"\\\\"+"\n")
    file1.write("##################################\n")
    
    #dict.fromkeys() digunakan untuk membuat list tidak terdapat duplikat
#    print('tipe data eval_mu', type(eval_mupluslambda))
    # best_selection = sorted(list(dict.fromkeys(eval_mupluslambda)))[0:2]
    # afterSelectBest = copy.deepcopy(mupluslambda)
    # for i in range(len(best_selection)):
    #     newPopulation.append(mupluslambda[eval_mupluslambda.index(best_selection[i])])
    #     afterSelectBest.remove(mupluslambda[eval_mupluslambda.index(best_selection[i])])    
        
    # decode_afterSelectBest =[0]*len(afterSelectBest)
    # for x in range(len(afterSelectBest)):
    #     decode_afterSelectBest[x]=stage_1(supplier, plant, dc, customer, 1, sups, D, W, d,afterSelectBest[x][0],afterSelectBest[x][1],afterSelectBest[x][2],t,a).decode()
    # eval_afterSelectBest = evaluate_problem2(decode_afterSelectBest,sups, D, W,d,t,a,c,g,v,r[0],r[1],0.5,0.5)[0] 
    
    # bestOf = list(dict.fromkeys(eval_afterSelectBest))
    # if len(bestOf) == len(mu)-len(newPopulation):
    #     for i in range(len(bestOf)):
    #         newPopulation.append(mupluslambda[eval_mupluslambda.index(best_selection[i])])
    # else:
    #     pop = randomPopulation(len(sups),len(plant),len(dc),len(customer), len(mu)-len(newPopulation))        
    #     for i in range(len(pop)):
    #         newPopulation.append(pop[i])
    best_selection = sorted(list(dict.fromkeys(eval_mupluslambda)))

    if len(mu) == len(best_selection):
        for i in best_selection:
            newPopulation.append(mupluslambda[eval_mupluslambda.index(i)])

    else:
        newPopulation = [mupluslambda[eval_mupluslambda.index(i)] for i in best_selection[0:2]]
        pop = randomPopulation(len(sups),len(plant),len(dc),len(customer), len(mu)-len(newPopulation))        
        for i in pop:
            newPopulation.append(i)
    
    ############
    file1.write("##################################\n")
    file1.write("populasi baru \n")

    for x in range(len(newPopulation)):
        file1.write("Individu "+str(x+1)+" & ")
        for y in newPopulation[x]:
            str_population = [str(z)+" " for z in y]
            file1.writelines(str_population)
        file1.write("\\\\"+"\n")
    file1.write("##################################\n")
    ############
    
    decode_population_cek =[0]*len(population)
    for x in range(len(population)):
        decode_population_cek[x]=stage_1(supplier, plant, dc, customer, 1,  sups, D, W, d,newPopulation[x][0],newPopulation[x][1],newPopulation[x][2],t,a).decode()    
        
    greatPopulation200 = evaluate_problem2(decode_population_cek,sups, D, W,d,t,a,c,g,v,r[0],r[1],0.5,0.5)
    
#    if (generation+1) %100 == 0:
    df200 = pd.DataFrame({
                    "generation": generation+1,
                    "f1":[greatPopulation200[1][greatPopulation200[0].index(min(greatPopulation200[0]))]],
                    "f2":[greatPopulation200[2][greatPopulation200[0].index(min(greatPopulation200[0]))]],
                    "Optimal":[greatPopulation200[0][greatPopulation200[0].index(min(greatPopulation200[0]))]]})
            
    df = df.append(df200, ignore_index=True)
  
    mu = copy.deepcopy(newPopulation)
    lambdas = copy.deepcopy(mu)
    generation = generation + 1
    
    
decode_population =[0]*len(newPopulation)
for x in range(len(newPopulation)):
    decode_population[x]=stage_1(supplier, plant, dc, customer, 1, sups, D, W, d,newPopulation[x][0],newPopulation[x][1],newPopulation[x][2],t,a).decode()    

greatPopulation = evaluate_problem2(decode_population,sups, D, W,d,t,a,c,g,v,r[0],r[1],0.5,0.5)

print("Output Program \n")
print("Nilai minimum hasil evaluasi : ", min(greatPopulation[0]))
print("dengan nilai dari masing-masing fungsi obyek sebagai berikut: \n")
ind=greatPopulation[0].index(min(greatPopulation[0]))
print("f1 = ",greatPopulation[1][ind], "/ dalam bentuk normalisasi ",greatPopulation[4][ind])
print("f2 = ",greatPopulation[2][ind], "/ dalam bentuk normalisasi ",greatPopulation[5][ind])

print("\n Setelah didekodekan diperoleh bahwa")

# b,f,q,p,z

for i in range(len(decode_population[ind])):
    if i == 0:
        for k in range(len(decode_population[ind][i])):
            for j in range(len(decode_population[ind][i][k])):
                if decode_population[ind][i][k][j] != 0:
                    print("Banyak bahan yang dikirim dari pemasok ", supplier[k], " ke pabrik ",plant[j], " sebanyak ", decode_population[ind][i][k][j])
        print("\n")
    elif i ==1:
        for k in range(len(decode_population[ind][i])):
            for j in range(len(decode_population[ind][i][k])):
                if decode_population[ind][i][k][j] != 0:
                    print("Banyak bahan yang dikirim dari pabrik ", plant[k], " ke gudang ",dc[j], " sebanyak ", decode_population[ind][i][k][j])
        print("\n")
    elif i ==2:
        for k in range(len(decode_population[ind][i])):
            for j in range(len(decode_population[ind][i][k])):
                if decode_population[ind][i][k][j] != 0:
                    print("Banyak bahan yang dikirim dari gudang ", dc[k], " ke pelanggan ",customer[j], " sebanyak ", decode_population[ind][i][k][j])
        print("\n")
    elif i == 3:
        print('Dalam hal ini pabrik yang beroperasi adalah ')
        for k in range(len(decode_population[ind][i])):
            if decode_population[ind][i][k] != 0:
                print("pabrik  ", plant[k])
        print("\n")
    elif i == 4:
        print('Dalam hal ini gudang yang beroperasi adalah ')
        for k in range(len(decode_population[ind][i])):
            if decode_population[ind][i][k] != 0:
                print("gudang  ", dc[k])

print("Dengan kata lain individu optimal adalah intividu ke-",ind,"yaitu \n")
print(newPopulation[ind])
optchr = ''.join(''.join([str(j) for j in i]) for i in newPopulation[ind])
print(optchr)
file1.write("decode final population #################\n")
for x in decode_population:
    file1.write(toBmatrix(x))
    file1.write("##################################\n")

export_excel = df.to_excel (r'/home/rudi/Documents/skripsi/0109gencheng.xlsx', index = None, header=True)
file1.close()

plt.scatter(df['f1'],df['f2'], label="solusi optimal", color='r', s=15, marker="o")

plt.xlabel('f1')
plt.ylabel('f2')
plt.title('Grafik Optimal Pareto')
plt.legend()
plt.show()
