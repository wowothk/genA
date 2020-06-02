#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 15:32:21 2019

@author: rudi
"""
import sys
sys.path.insert(0, '/home/rudi/Documents/skripsi')
from encode import priority_based_enc
from encode import integer_encoding
from dummy import add_dummy
import numpy as np
import random
import copy
from evaluation_funtion import evaluation
from eval2 import evaluation2
#from decoding_stage_3 import stage_3
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
        func1 = evaluation(mu[x][0],mu[x][1],mu[x][2], sups, D, W, d, t,a,c,g,v,mu[x][3], mu[x][4], r1, r2).func1()
        func2 = evaluation(mu[x][0],mu[x][1],mu[x][2], sups, D, W, d, t,a,c,g,v,mu[x][3], mu[x][4], r1, r2).func2()
        func3 = evaluation(mu[x][0],mu[x][1],mu[x][2], sups, D, W, d, t,a,c,g,v,mu[x][3], mu[x][4], r1, r2).func3()
        evalMu[x] = weight1*func1+weight2*func2+weight3*func3
    evalPlusLambda = [0]*len(plusLambda)
    for y in range(len(plusLambda)):#b,f,q, sups, D, W, d, t, a, c,g,v,p,z, r1, r2
        func1 = evaluation(plusLambda[x][0],plusLambda[x][1],plusLambda[x][2], sups, D, W, d, t,a,c,g,v,plusLambda[x][3], plusLambda[x][4], r1, r2).func1()
        func2 = evaluation(plusLambda[x][0],plusLambda[x][1],plusLambda[x][2], sups, D, W, d, t,a,c,g,v,plusLambda[x][3], plusLambda[x][4], r1, r2).func2()
        func3 = evaluation(plusLambda[x][0],plusLambda[x][1],plusLambda[x][2], sups, D, W, d, t,a,c,g,v,plusLambda[x][3], plusLambda[x][4], r1, r2).func3()
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
def evaluate(population, sups, D, W, d, t, a, c, g ,v,r1, r2, weight1, weight2, weight3, h, tau):
    evalPopulation = [0]*len(population)
    evalf1 = [0]*len(population)
    evalf2 =[0]*len(population)
    evalf3 =[0]*len(population)
    for x in range(len(population)):
        func1 = evaluation(population[x][0],population[x][1],population[x][2], sups, D, W, d, t,a,c,g,v,population[x][3], population[x][4], r1, r2, h, tau).func1_alternative()
        func2 = evaluation(population[x][0],population[x][1],population[x][2], sups, D, W, d, t,a,c,g,v,population[x][3], population[x][4], r1, r2, h, tau).func2()
        func3 = evaluation(population[x][0],population[x][1],population[x][2], sups, D, W, d, t,a,c,g,v,population[x][3], population[x][4], r1, r2, h, tau).func3()
        evalf1[x] = func1
        evalf2[x] = func2
        evalf3[x] = func3
        
    print(evalf1,evalf2,evalf3)
    f1 = normalize(evalf1)
    f2 = normalize(evalf2)
    f3 = normalize(evalf3)
    
    for x in range(len(population)):
        evalPopulation[x] = weight1*f1[x]-weight2*f2[x]+weight3*f3[x]
#    evalPopulation[x] = weight1*func1-weight2*func2+weight3*func3
    return evalPopulation, evalf1, evalf2, evalf3

def evaluate_alternative(population, sups, D, W, d, t, a, c, g ,v,r1, r2, weight1, weight2, weight3, h, tau):
    evalPopulation = [0]*len(population)
    evalAsf = [0]*len(population)
    evalf1 = [0]*len(population)
    evalf2 =[0]*len(population)
    evalf3 =[0]*len(population)
    for x in range(len(population)):
        func1 = evaluation(population[x][0],population[x][1],population[x][2], sups, D, W, d, t,a,c,g,v,population[x][3], population[x][4], r1, r2, h, tau).func1_alternative()
        func2 = evaluation(population[x][0],population[x][1],population[x][2], sups, D, W, d, t,a,c,g,v,population[x][3], population[x][4], r1, r2, h, tau).func2()
        func3 = evaluation(population[x][0],population[x][1],population[x][2], sups, D, W, d, t,a,c,g,v,population[x][3], population[x][4], r1, r2, h, tau).func3()
        evalf1[x] = func1
        evalf2[x] = func2
        evalf3[x] = func3
        evalAsf[x] = [func1, func2, func3]
#    print(evalf1,evalf2,evalf3)
    f1 = normalize(evalf1)
    f2 = normalize(evalf2)
    f3 = normalize(evalf3)
    
    for x in range(len(population)):
        evalPopulation[x] = weight1*f1[x]-weight2*f2[x]+weight3*f3[x]
#    evalPopulation[x] = weight1*func1-weight2*func2+weight3*func3
    return evalPopulation, evalf1, evalf2, evalf3, evalAsf, f1,f2,f3

def evaluate_problem1(population, sups, D, W, d, t, a, c, g ,v,r1, r2, weight1, weight2, h, tau):
    evalPopulation = [0]*len(population)
    evalAsf = [0]*len(population)
    evalf1 = [0]*len(population)
    evalf2 =[0]*len(population)
#    evalf3 =[0]*len(population)
    for x in range(len(population)):
        func1 = evaluation(population[x][0],population[x][1],population[x][2], sups, D, W, d, t,a,c,g,v,population[x][3], population[x][4], r1, r2, h, tau).func1_alternative()
        func2 = evaluation(population[x][0],population[x][1],population[x][2], sups, D, W, d, t,a,c,g,v,population[x][3], population[x][4], r1, r2, h, tau).func2()
#        func3 = evaluation(population[x][0],population[x][1],population[x][2], sups, D, W, d, t,a,c,g,v,population[x][3], population[x][4], r1, r2, h, tau).func3()
        evalf1[x] = func1
        evalf2[x] = func2
#        evalf3[x] = func3
        evalAsf[x] = [func1, func2]
#    print(evalf1,evalf2,evalf3)
    f1 = normalize(evalf1)
    f2 = normalize(evalf2)
#    f3 = normalize(evalf3)
    
    for x in range(len(population)):
        evalPopulation[x] = weight1*f1[x]-weight2*f2[x]
#    evalPopulation[x] = weight1*func1-weight2*func2+weight3*func3
    return evalPopulation, evalf1, evalf2, evalAsf, f1,f2

def evaluate_problem2(population, sups, D, W, d, t, a, c, g ,v,r1, r2, weight1, weight3):
    evalPopulation = [0]*len(population)
    evalAsf = [0]*len(population)
    evalf1 = [0]*len(population)
    evalf3 =[0]*len(population)
    for x in range(len(population)):
        func1 = evaluation2(population[x][0],population[x][1],population[x][2], sups, D, W, d, t,a,c,g,v,population[x][3], population[x][4], r1, r2).func1_alternative()
        func3 = evaluation2(population[x][0],population[x][1],population[x][2], sups, D, W, d, t,a,c,g,v,population[x][3], population[x][4], r1, r2).func3()
        evalf1[x] = func1
        evalf3[x] = func3
        evalAsf[x] = [func1, func3]
    f1 = normalize(evalf1)
    f3 = normalize(evalf3)
    
    for x in range(len(population)):
        evalPopulation[x] = weight1*f1[x]+weight3*f3[x]
    return evalPopulation, evalf1, evalf3, evalAsf, f1,f3

def normalize(f):
    temp_f = copy.deepcopy(f)
    if (max(f)-min(f))==0:
        for i in range(len(f)):
            temp_f[i] = 0
    else:    
        for i in range(len(f)):
            temp_f[i] = (f[i] - min(f))/(max(f)-min(f))
    return temp_f

def randomPopulation(len_of_sups, len_of_plant,len_of_dc, len_of_customer, the_number_of_individu):
    stage1=[]
    for x in range(len_of_sups+len_of_plant):
        stage1.append(x+1)
    stage2=[]
    for x in range(len_of_dc+len_of_plant):
        stage2.append(x+1)
    stage3=[None]*len_of_customer
    for x in range(len_of_customer):
        stage3[x]=random.randint(1,len_of_dc)
    population=np.array([[None]*3]*the_number_of_individu)
    for x in range(the_number_of_individu):
        for y in range(3):
            if y==0:
                population[x][y]=random.sample(stage1, len(stage1))
            elif y==1:
                population[x][y]=random.sample(stage2, len(stage2))
            else:
                for z in range(len_of_customer):
                    stage3[z]=random.randint(1,len_of_dc)
                population[x][y]=copy.deepcopy(stage3)
    return population.tolist()

def rouletteWheel(evalPopulation, population):
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
            newPopulation[k] = population[0]
        else:
            s=1
            while s<len(population):
                if rand <= cumulativeProbability[s] and rand > cumulativeProbability[s-1]:
                    newPopulation[k] = population[s]
                    break
                s = s+1
            
    return newPopulation

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
def enc_pop(population, supplier, plant, dc, customer, sups, D, W, d, t, a, c):
    encoding_population=[None]*len(population)
    for i in range(len(population)):
        p = population[i][3].copy()
        z = population[i][4].copy()
        for j in range(3):
            if j == 0:
                capacity = copy.deepcopy(sups)
                demand = copy.deepcopy(D)
                for m in range(len(plant)):
                    demand[m] = sum(population[i][j+1][m])*p[m]#salah di sini begitupun pada yang bawah mengingat demand itu ditentukan oleh permintaan customer
                plant_with_dummy=add_dummy(supplier, plant, capacity, demand, t, population[i][j])
                shipment_with_dummy  = plant_with_dummy[0]
                cost_with_dummy = plant_with_dummy[1]
                depot_with_dummy =plant_with_dummy[2]
                demand_with_dummy = plant_with_dummy[3]
                v1 = priority_based_enc(supplier,depot_with_dummy, capacity, demand_with_dummy, cost_with_dummy, shipment_with_dummy).encoding()
            elif j == 1:
                capacity = copy.deepcopy(D)
                for k in range(len(plant)):
                    capacity[k] = capacity[k]*p[k]
                demand = copy.deepcopy(W)
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
                capacity = copy.deepcopy(W)
                temp_cost = copy.deepcopy(c)
                for m in range(len(dc)):
                    capacity[m] = capacity[m]*z[m]
                demand = copy.deepcopy(d)
                temp = [0]*len(W)
                population_aksen = copy.deepcopy(population[i][j])
                for x in range(len(W)):
                    if (capacity[x] - sum(population[i][j][x])) > 0:
                        temp[x] = capacity[x] - sum(population[i][j][x])
                if sum(temp) != 0:
                    temp_customer.append("dummy")
                    demand.append(sum(temp))
                    temp_cost = np.append(temp_cost, np.array([[0]*len(W)]).T,1)
                    population_aksen = np.append(population_aksen, np.array([temp]).T,1)
                v3 = integer_encoding(dc, temp_customer, capacity, d,temp_cost,population_aksen).encode()
        
        encoding_population[i] = [v1,v2,v3]
    return encoding_population
def check_integer_enc(integerSet, capacity_value, demand_value):
    check = True
    capacity=copy.deepcopy(capacity_value)
    capacityDemand = [0]*len(capacity)
    for i in range(len(capacity_value)):
        capacity[integerSet[i]-1] = capacity[integerSet[i]-1] - demand_value[i]
        capacityDemand[integerSet[i]-1] = capacityDemand[integerSet[i]-1] + demand_value[i]
    for i in range(len(capacity)):
        if capacity_value[i] < capacityDemand[i]:
            check = False
            break
    return check

def isDominated(z, Z):
    temp_Z = np.unique(np.array(Z),axis=0)
    pop = [list(x) for x in temp_Z]
    for x in pop:
        if z[0] < x[0] and z[1] >= x[1] and z[2] <= x[2]:
            status = "nondominated"
        elif z[0] <= x[0] and z[1] > x[1] and z[2] <= x[2]:
            status = "nondominated"
        elif z[0] <= x[0] and z[1] >= x[1] and z[2] < x[2]:
            status = "nondominated"
        else:
            status = "dominated"
            break
    return status

def sumOfNonDominated(Z):
    status = ['a']*len(Z)
    for i in range(len(status)):
        status[i] = isDominated(Z[i], Z)
    summation = len(np.where(np.array(status) == 'nondominated'))
    return summation, status


def toBmatrix(matrices):
    string_matrices = ''
    for i in matrices:
        if isinstance(i, np.ndarray):
            matrix = '\\begin{bmatrix}\n'
            for k in i:
                for l in range(len(k)):
                    matrix = matrix+str(int(k[l]))+'&' if l != len(k)-1 else matrix+str(int(k[l]))+'\\\\'
            matrix = matrix+'\n'+ '\\end{bmatrix}\n'
        else:
            matrix = [str(k) for k in i]
            matrix = ''.join(matrix)+'\n'
        string_matrices = string_matrices+matrix+'\n\n'
    return string_matrices

def get_key(val): 
    for key, value in my_dict.items(): 
         if val == value: 
             return key 
  
    return "key doesn't exist"

def ordered(x):
    # x harus genap jumlahnya
    temp = list()
    val = list()
    for i in range(len(x)):                
        if (i+1)%2!=0:
            temp.append(x[i])
        else:
            temp.append(x[i])
            val.append(temp)
            temp = list()
    return val

# semen tonasa andi burhanuddin
#def evaluation_semen(population, a, f, x, y, b, w,c):
#    evalPopulation = [0]*len(population)
#    for x in range(len(population)):
#        func1 = evaluation(population[x][0],population[x][1],population[x][2], sups, D, W, d, t,a,c,g,v,population[x][3], population[x][4], r1, r2, h, tau).func1_alternative()
#    
#    return evalPopulation


#print(integerMutation([1,3,4,5,2], 5))
#s=randomPopulation(4,3,4,5,2)
#print(s)    
#s=list(randomPopulation(4,3,4,5,2))
#print(s[0)
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
#check= check_integer_enc([3, 3, 3, 3,4], W, d)
#print(check)