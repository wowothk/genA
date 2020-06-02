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
from genetic_algorithm import evaluate_problem2
from genetic_algorithm import ordered
#from genetic_algorithm import roulettewheelSelection
from genetic_algorithm import enc_pop
#from genetic_algorithm import check_integer_enc
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


file1 = open("semenfix0109.txt", "w+")
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

# population=np.array([[None]*3]*1000)
# for x in range(1000):
#     for y in range(3):
#         if y==0:
#             population[x][y]=random.sample(stage1, len(stage1))
#         elif y==1:
#             population[x][y]=random.sample(stage2, len(stage2))
#         else:
#             for z in range(len(distri)):
#                 stage3[z]=random.randint(1,len(up))
#             population[x][y]=copy.deepcopy(stage3)

# population = [list(x) for x in population]

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

mu = copy.deepcopy(population)
lambdas =copy.deepcopy(population)
generation = 0
the_number_of_generation=2000
while generation < the_number_of_generation:    
    print(generation)
    ### crossover
    random_crossover=[0]*len(mu)
    temp=[]
    for i in range(len(lambdas)):
        random_crossover[i] = random.random()
        if random_crossover[i]<0.9:
            temp.append(random_crossover[i])

    if len(temp)%2!=0:
        temp.remove(temp[random.randint(0,len(temp)-1)])

    parent = ordered(temp)
    index_parent = [[ np.where(np.array(random_crossover)==j)[0][0] for j in i ]for i in parent]

    for x in range(len(index_parent)):
        children = crossover(lambdas[index_parent[x][0]], lambdas[index_parent[x][1]], sups, up, plant, distri)
        lambdas[index_parent[x][0]]=children[0]
        lambdas[index_parent[x][1]]=children[1]
    #    ### mutation
    random_mutation = [0]*len(lambdas)
    for i in range(len(random_mutation)):
        random_mutation[i] = random.random()
    index_parent = parentMutation(random_mutation, 0.1)
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

    # print("evalmupluslambda", evaluate)

    # df2 = pd.DataFrame({
    #                         "generasi":generation+1,
    #                         "f1":evaluate[1],
    #                         "f2":evaluate[2],
    #                         "Optimal":evaluate[0]})
            
    # df = df.append(df2, ignore_index=True)


    newPopulation=[]

    #dict.fromkeys() digunakan untuk membuat list tidak 
    best_selection = sorted(list(dict.fromkeys(eval_mupluslambda)))

    if len(mu) == len(best_selection):
        for i in best_selection:
            newPopulation.append(mupluslambda[eval_mupluslambda.index(i)])

    else:
        newPopulation = [mupluslambda[eval_mupluslambda.index(i)] for i in best_selection[0:2]]
        pop = randomPopulation(len(sups),len(plant),len(pengantongan),len(distributor), len(mu)-len(newPopulation))        
        for i in pop:
            newPopulation.append(i)


    # afterSelectBest = copy.deepcopy(mupluslambda)
    # for i in best_selection:
    #     newPopulation.append(mupluslambda[eval_mupluslambda.index(i)])
    #     afterSelectBest = list(filter(lambda x: x != mupluslambda[eval_mupluslambda.index(i])], afterSelectBest))
    #     # afterSelectBest.remove(mupluslambda[eval_mupluslambda.index(best_selection[i])])    


    # # decode_afterSelectBest =[0]*len(afterSelectBest)
    # decode_afterSelectBest=dict()

    # for x in afterSelectBest:
    #     decode_afterSelectBest[str(x)]=stage_1(pemasok, pabrik, pengantongan, distributor,1, sups, plant, up, distri,x[0],x[1],x[2],t,a).decode()

    # eval_afterSelectBest = evaluate_problem2(list(decode_afterSelectBest.values),sups, plant, up,distri,t,a,c,g,v,r[0],r[1],0.5,0.5)[0] 
    
    # print('#####################')
    # print(eval_afterSelectBest)
    # print('#####################')

    '''
    part berikut merupakan algoritma untuk memastikan bahwasanya apabila terdapat sejumlah individu berbeda yang dapat membentuk populasi baru maka dibentuk populasi baru dengan individu tersebut

    namun apabila tidak maka akan diacak sejumlah individu untuk melengkapi terbentuknya populasi baru. 
    '''

    # bestOf = list(dict.fromkeys(eval_afterSelectBest))
    # if len(bestOf) == len(mu)-len(newPopulation):
    #     for i in bestOf:
    #         newPopulation.append(mupluslambda[eval_mupluslambda.index(i)])
    # else:
    #     pop = randomPopulation(len(sups),len(plant),len(pengantongan),len(distributor), len(mu)-len(newPopulation))        
    #     for i in range(len(pop)):
    #         newPopulation.append(pop[i])
    
    decode_population =[0]*len(population)
    for x in range(len(population)):
        decode_population[x]=stage_1(pemasok, pabrik, pengantongan, distributor, 1, sups,plant, up, distri,newPopulation[x][0],newPopulation[x][1],newPopulation[x][2],t,a).decode()    
    greatPopulation200 = evaluate_problem2(decode_population,sups, plant, up,distri,t,a,c,g,v,r[0],r[1],0.5,0.5)
    
    if (generation+1)%100==0:  
    # print("greatPopulation ", greatPopulation200)
        df200 = pd.DataFrame({
                                "generasi":generation+1,
                                "f1":[greatPopulation200[1][greatPopulation200[0].index(min(greatPopulation200[0]))]],
                                "f2":[greatPopulation200[2][greatPopulation200[0].index(min(greatPopulation200[0]))]],
                                "Optimal":[greatPopulation200[0][greatPopulation200[0].index(min(greatPopulation200[0]))]]})
            
        df = df.append(df200, ignore_index=True)

    mu = copy.deepcopy(newPopulation)
    lambdas = copy.deepcopy(mu)   
    generation = generation + 1
    
print("Populasi Baru")        
for i in newPopulation:
    print(i)

decode_population =[0]*len(newPopulation)
for x in range(len(newPopulation)):
    decode_population[x]=stage_1(pemasok, pabrik, pengantongan, distributor, 1, sups,plant, up, distri,newPopulation[x][0],newPopulation[x][1],newPopulation[x][2],t,a).decode()    
greatPopulation = evaluate_problem2(decode_population,sups, plant, up,distri,t,a,c,g,v,r[0],r[1],0.7,0.3)

print("Output Program \n")
print("Nilai minimum hasil evaluasi : ", min(greatPopulation[0]))
print("dengan nilai dari masing-masing fungsi obyek sebagai berikut: \n")
ind=greatPopulation[0].index(min(greatPopulation[0]))
print("f1 = ",greatPopulation[1][ind], "/ dalam bentuk normalisasi ",greatPopulation[4][ind])
print("f2 = ",greatPopulation[2][ind], "/ dalam bentuk normalisasi ",greatPopulation[5][ind])

print("\n Setelah didekodekan diperoleh bahwa")

for i in range(len(decode_population[ind])):
    if i == 0:
        for k in range(len(decode_population[ind][i])):
            for j in range(len(decode_population[ind][i][k])):
                if decode_population[ind][i][k][j] != 0:
                    print("Banyak bahan yang dikirim dari pemasok ", pemasok[k], " ke pabrik ",pabrik[j], " sebanyak ", decode_population[ind][i][k][j])
        print("\n")
    elif i ==1:
        for k in range(len(decode_population[ind][i])):
            for j in range(len(decode_population[ind][i][k])):
                if decode_population[ind][i][k][j] != 0:
                    print("Banyak bahan yang dikirim dari pabrik ", pabrik[k], " ke gudang ",pengantongan[j], " sebanyak ", decode_population[ind][i][k][j])
        print("\n")
    elif i ==2:
        hubdistpeng = {'Distributor': distributor}

        for k in range(len(decode_population[ind][i])):
            hubdistpeng[str(pengantongan[k])]=decode_population[ind][i][k]
            for j in range(len(decode_population[ind][i][k])):
                if decode_population[ind][i][k][j] != 0:
                    print("Banyak bahan yang dikirim dari pengantongan ", pengantongan[k], " ke distributor ",distributor[j], " sebanyak ", decode_population[ind][i][k][j])
        print("\n")
        hubdistpeng = pd.DataFrame(hubdistpeng)
    elif i == 3:
        print('Dalam hal ini pabrik yang beroperasi adalah ')
        for k in range(len(decode_population[ind][i])):
            if decode_population[ind][i][k] != 0:
                print("pabrik  ", pabrik[k])
        print("\n")
    elif i == 4:
        print('Dalam hal ini pengantongan yang beroperasi adalah ')
        for k in range(len(decode_population[ind][i])):
            if decode_population[ind][i][k] != 0:
                print("pengantongan  ", pengantongan[k])

print("Dengan kata lain individu optimal adalah intividu ke-",ind,"yaitu \n")
print(newPopulation[ind])

file1.write("decode final population #################\n")
for x in decode_population:
    for y in x:
        str_population = [re.sub("\s+","&", str(z)) +"\\" for z in y]
        file1.writelines(str_population)
        file1.write("\n\n")
    file1.write("##################################\n")

# df2 = pd.DataFrame({
#         "generasi":generation+1,
#         "f1":[greatPopulation[1][greatPopulation[0].index(min(greatPopulation[0]))]],
#         "f2":[greatPopulation[2][greatPopulation[0].index(min(greatPopulation[0]))]],
#         "Optimal":[greatPopulation[0][greatPopulation[0].index(min(greatPopulation[0]))]]})
# df = df.append(df2, ignore_index=True)
    
export_excel = df.to_excel (r'/home/rudi/Documents/skripsi/selangseratus0109.xlsx', index = None, header=True)
export_excel2 = hubdistpeng.to_excel (r'/home/rudi/Documents/skripsi/hubdistpengfix.xlsx', header=True)

plt.scatter(df['f1'],df['f2'], label="solusi optimal", color='r', s=15, marker="o")

plt.xlabel('f1')
plt.ylabel('f2')
plt.title('Grafik Optimal Pareto')
plt.legend()
plt.savefig('optimalparetosementonasafix.png')
plt.show()

