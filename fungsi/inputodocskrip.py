import pandas as pd
import numpy as np
import random
import copy
import math
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

class stage_1:
    def __init__(self, S, K, J, I, u, s, D, w, d, v1, v2, v3, t, c):
        self.S = S
        self.K = K
        self.D = D
        self.J = J
        self.I = I
        self.s = s
        self.t = t
        self.u = u 
        self.v1 =v1
        self.v2 = v2
        self.v3 = v3
        self.d = d
        self.w = w
        self.c = c
    def decode(self):
        b = np.array([[0]*len(self.S)]*len(self.K))
        stg_2 = stage_2(self.K, self.J, self.I, self.D, self.w, self.d, self.c, self.v2,  self.v3).decode()
        D_aksen = stg_2[1]
        f = stg_2[0]
        q = stg_2[2]
        p = stg_2[3]
        z = stg_2[4]
        capacityD = copy.deepcopy(self.D)
        for k in range(len(self.K)):
            capacityD[k] = self.u*D_aksen[k]
        chromosom1=copy.deepcopy(self.v1)
        if len(self.v1) > len(self.S)+len(self.K):
            chromosom1.pop()
        b = decoding(self.S, self.K, capacityD, self.s, self.t, chromosom1)[0]
        return b,f,q,p,z

class stage_2:
    def __init__(self, K, J, I,De, w, d, a, v2, v3):
        self.K = list(K)
        self.J = list(J)
        self.a = a
        self.v2 = v2
        self.I = list(I)
        self.De = list(De)
        self.v3 = v3
        self.d = list(d)
        self.w = list(w)
        
    def decode(self):
        D_aksen = [0]*len(self.K)
        D = [0]*len(self.K)
        temp_w = [0]*len(self.w)
        for i in range(len(self.w)):
            temp_w[i] = self.w[i]
        stg_3= stage_3(self.J, self.I, temp_w, self.d, self.v3).decode()
        q=stg_3[1]
        z=stg_3[3]
        tot_dem = 0
        Pd = [0]*len(self.K)
        for j in range(len(self.J)):
            tot_dem = tot_dem + sum(q[j])
        tot_cap = 0
        p = [0]*len(self.K)
        for k in range(len(self.K)):
            tot_cap = tot_cap+ self.De[k]*p[k]
            Pd[k] = self.v2[k]
        Op = []
        Cp = [None]*len(self.K)
        for k in range(len(self.K)):
            Cp[k] = self.K[k]
            D[k] = self.De[k]
        Np = len(Op)
        P = 2
        while tot_cap < tot_dem and Np < P:
            hp_k = 0
            temp = 0
            for k in range(len(self.K)):
                if temp == 0 :
                    temp = Pd[k]
                    hp_k = k
                elif Pd[k] > temp:
                    temp = Pd[k]
                    hp_k = k
            p[hp_k] = 1
            tot_cap = tot_cap + D[hp_k]*p[hp_k]
            Op.append(self.K[hp_k])
            Np = Np + 1
            Pd[hp_k] = 0
        Cp = list(set(self.K)-set(Op))  
        chromosom2 = copy.deepcopy(self.v2)
        if len(Cp) != 0:
            for e in range(len(Cp)):
                chromosom2[self.K.index(Cp[e])] = 0
        while len(Op) > P or tot_cap < tot_dem: 
            index_op =[]
            for i in range(len(Op)):
                index_op.append(self.K.index(Op[i]))
            dok =[]
            for x in range(len(index_op)):
                dok.append(D[index_op[x]])
            dck = list(set(D) -set(dok))
            dop = len(dok)
            dp = P
            d_tot_cap = tot_cap
            d_tot_dem = tot_dem
            dok = repair_alg(dok, dck, dp, dop, d_tot_cap, d_tot_dem)
            Op  = []
            p = [0]*len(self.K)
            tot_cap = sum(dok)
            temp_dok = np.array(dok)
            temp_De = np.array(self.De)
            for k in range(len(dok)):
                Op.append(self.K[self.De.index(dok[k])])
                if len(np.where(temp_dok == temp_De)[0]) > 1:
                    for x in range(len(np.where(temp_dok == temp_De)[0])):
                        p[np.where(temp_dok == temp_De)[0][x]] = 1        
                else:
                    p[self.De.index(dok[k])] = 1
        if len(self.v2) > len(self.K)+len(self.J):
            chromosom2.pop()
        temp_d=[0]*len(self.K)
        temp_we=[0]*len(self.w)
        for k in range(len(self.K)):
            temp_d[k] = D[k]*p[k]
        for j in range(len(self.w)):
            temp_we[j] = self.w[j]*z[j]
        temp_q=[0]*len(self.w)
        for j in range(len(self.w)):
            temp_q[j] = sum(q[j])
        pros_1 = decoding(self.K, self.J, temp_q, temp_d, self.a ,chromosom2)
        f = pros_1[0]
        D_aksen = pros_1[1]
        return  f, D_aksen, q, p,z

class stage_3:
    def __init__(self, J, I, w, d, v):
        self.J = list(J)
        self.I = list(I)
        self.w = list(w)
        self.d = list(d)
        self.v = v
    
    def decode(self):
        z = [0]*len(self.J)
        y = np.array([[0]*len(self.I)]*len(self.J))
        customerDemand = copy.deepcopy(self.d)
        Od = []
        Cd = [None]*len(self.J)
        for j in range(len(self.J)):
            Cd[j] = self.J[j]
        q = np.array([[0]*len(self.I)]*len(self.J))
        w_aksen = [0]*len(self.J)
        temp = []
        chromosom=copy.deepcopy(self.v)
        temp_chromosom=copy.deepcopy(self.v)
        capacityW=copy.deepcopy(self.w)
        for k in range(len(self.v)):
            chromosom[k] = chromosom[k]-1
        if len(self.v)>len(self.d):
            chromosom.pop()
            temp_chromosom.pop()            
        for i in range(len(self.I)):
            z[chromosom[i]] = 1
            y[chromosom[i]][i] = 1  
            Od.append(self.J[chromosom[i]])
        Od =list(set(Od))
        Cd = list(set(self.J)-set(Od))
        tot_cap =0
        for j in range(len(self.J)):
            tot_cap = tot_cap+ capacityW[j]*z[j]
        tot_dem = 0
        for i in range(len(self.I)):
            tot_dem = tot_dem + self.d[i]
        if len(Od) <= len(capacityW) and tot_cap >= tot_dem:
            for i in range(len(self.I)):
                q[chromosom[i]][i] = self.d[i]
                capacityW[chromosom[i]] = capacityW[chromosom[i]] - q[chromosom[i]][i]
                w_aksen[chromosom[i]] = w_aksen[chromosom[i]] + q[chromosom[i]][i]
                customerDemand[i] = 0
            temp = []
            for j in range(len(self.J)):
                if self.w[j] < 0:
                    for i in range(len(self.I)):
                        if y[j][i] != 0:
                            temp.append(i)
                    k = random.randint(0, len(temp)-1)
                    y[j][temp[k]] = 0 
                    capacityW[j] = capacityW[j] + q[j][temp[k]]
                    w_aksen[j] = w_aksen[j] - q[j][temp[k]]
                    for je in range(len(self.J)):
                        if je != j :
                            capacityW[je] = capacityW[je] - q[je][temp[k]]
                            if capacityW[j] >= 0:
                                y[j][temp[k]] = 1
                                w_aksen[j] = w_aksen[j] + q[j][temp[k]]
                                capacityW[temp[k]] = je
                                q[je][temp[k]] = self.d[temp[k]]
                            else:
                                capacityW[je] = capacityW[je] + q[je][temp[k]]
            return w_aksen, q, Cd, z
        else:
            temp_j = np.array(self.J)
            temp_od = np.array(Od)
            index_od = np.where(np.in1d(temp_j, temp_od))
            dok =[]
            for x in range(len(index_od[0])):
                dok.append(capacityW[index_od[0][x]])
            dck = list(set(capacityW) -set(dok))
            dop = len(dok)
            dp = 4
            d_tot_cap = tot_cap
            d_tot_dem = tot_dem
            dok = repair_alg(dok, dck, dp, dop, d_tot_cap, d_tot_dem)
            Od = []
            for x in dok:
                Od.append(self.J[self.w.index(x)])
            Cd = list(set(self.J)-set(Od))
            temp_capacity=copy.deepcopy(capacityW)   
            for i in range(len(temp_capacity)):
                for x in Cd:
                    if i == self.J.index(x):
                        temp_capacity[i] = 0
            for i in range(len(chromosom)):
                for j in range(len(temp_capacity)):
                    if temp_capacity[j] >= self.d[i]:
                        temp_chromosom[i] = j+1
                        temp_capacity[j] = temp_capacity[j] - self.d[i]  
                        break
            return stage_3(self.J, self.I, capacityW, self.d, temp_chromosom).decode()


class evaluation2:
    def __init__(self, b,f,q, sups, D, W, d, t, a, c,g,v,p,z, r1, r2):
        self.b = b
        self.f = f
        self.q = q
        self.sups = sups
        self.D = D
        self.W = W
        self.d = d
        self.t = t
        self.a = a
        self.c = c
        self.g = g
        self.v = v
        self.p = p
        self.z = z
        self.r1 = r1
        self.r2 = r2

    
    def func1(self):
        costPlant = [0]*len(self.p)
        for k in range(len(self.p)):
            costPlant[k] = self.g[k]*self.p[k]
        
        costDc = [0]*len(self.z)
        for j in range(len(self.z)):
            costDc[j] = self.v[j]*self.z[j]
        
        costOfb = np.array([[0]*len(self.D)]*len(self.sups))
        sumcostOfb = [0]*len(self.sups)
        for s in range(len(self.sups)):
            for k in range(len(self.D)):
                costOfb[s][k] = self.b[s][k]*self.t[s][k]
            sumcostOfb[s] = sum(costOfb[s])
        
        costOff = np.array([[0]*len(self.W)]*len(self.D))
        sumcostOff = [0]*len(self.D)
        for k in range(len(self.D)):
            for j in range(len(self.W)):
                costOff[k][j] = self.f[k][j]*self.a[k][j]
            sumcostOff[k] = sum(costOff[k])    
            
        costOfq = np.array([[0]*len(self.d)]*len(self.W))
        sumcostOfq = [0]*len(self.W)
        for j in range(len(self.W)):
            for i in range(len(self.d)):
                costOfq[j][i] = self.q[j][i]*self.c[j][i]
            sumcostOfq[j] = sum(costOfq[j])
        return sum(costPlant)+sum(costDc)+sum(sumcostOfb)+sum(sumcostOff)+sum(sumcostOfq)

    def func1_alternative(self):
        costPlant = [0]*len(self.p)
        for k in range(len(self.p)):
            costPlant[k] = self.g[k]*self.p[k]
        
        costDc = [0]*len(self.z)
        for j in range(len(self.z)):
            costDc[j] = self.v[j]*self.z[j]
        
        costOfb = np.array([[0]*len(self.D)]*len(self.sups))
        sumcostOfb = [0]*len(self.sups)
        for s in range(len(self.sups)):
            for k in range(len(self.D)):
                costOfb[s][k] = self.b[s][k]*0.02458*self.t[s][k]
            sumcostOfb[s] = sum(costOfb[s])
        
        costOff = np.array([[0]*len(self.W)]*len(self.D))
        sumcostOff = [0]*len(self.D)
        for k in range(len(self.D)):
            for j in range(len(self.W)):
                costOff[k][j] = self.f[k][j]*self.a[k][j]
            sumcostOff[k] = sum(costOff[k])    
            
        costOfq = np.array([[0]*len(self.d)]*len(self.W))
        sumcostOfq = [0]*len(self.W)
        for j in range(len(self.W)):
            for i in range(len(self.d)):
                costOfq[j][i] = self.q[j][i]*self.c[j][i]
            sumcostOfq[j] = sum(costOfq[j])
        return sum(costPlant)+sum(costDc)+sum(sumcostOfb)+sum(sumcostOff)+sum(sumcostOfq)    
    def func3(self):
        openPlant = list(np.multiply(self.D, self.p))
        openDc = list(np.multiply(self.W, self.z))
        equation1 = [0]*len(openPlant)
        equation2 = [0]*len(openDc)
        for k in range(len(self.D)):
            if self.p[k] != 0:
                equation1[k]=(sum(self.f[k])/self.D[k]-(np.sum(self.f)/sum(openPlant)))**2
        for j in range(len(self.W)):
            if self.z[j] != 0:
                equation2[j]=(sum(self.q[j])/self.W[j]-(np.sum(self.q)/sum(openDc)))**2        
        return self.r1*math.sqrt(sum(equation1)/sum(self.p))+self.r2*math.sqrt(sum(equation2)/sum(self.z))

#--------------------------------------------------------------
def crossover(chromosom1, chromosom2, sups, W, D, d):
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

def integerMutation(chromosom, length_source):
    gen = int(random.random()*len(chromosom))
    changeWith = random.randint(1, length_source)
    while changeWith == chromosom[gen]:
        changeWith = random.randint(1, length_source)
    chromosom[gen] = changeWith
    return chromosom

def parentMutation(random_value, mutationRatio):
    parent=[]
    for i in range(len(random_value)):
        if random_value[i] < mutationRatio:
            parent.append(i)
    return parent

def swapMutation(chromosom):
    gen1 = int(random.random()*len(chromosom))
    gen2 = int(random.random()*len(chromosom))
    while gen2==gen1:
        gen2 = int(random.random()*len(chromosom))
    temp =chromosom[gen1]
    chromosom[gen1] =chromosom[gen2]
    chromosom[gen2] = temp
    return chromosom

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

def repair_alg(DOK, DCK, DP, DOP, d_tot_cap, d_tot_dem):
    temp_dok = [0]*len(DOK)
    temp_dck = [0]*len(DCK)
    for x in range(len(DOK)):
        temp_dok[x]=DOK[x]
    for y in range(len(DCK)):
        temp_dck[y]=DCK[y]
    i=0        
    while DOP > DP or d_tot_cap < d_tot_dem:
        i=i+1
        if DOP > DP and d_tot_cap >= d_tot_dem:
            while DOP > DP:
                if len(temp_dok) != 0:
                    index = random.randint(0,len(temp_dok)-1)
                    temp = temp_dok[index]
                    del temp_dok[index]
                    temp_dck.append(temp)
                    DOP = len(temp_dok)
            d_tot_cap = sum(temp_dok)
        elif (DOP<DP or DOP >= DP) and d_tot_cap< d_tot_dem:
            while d_tot_cap < d_tot_dem:
                if len(temp_dck) != 0:
                    index = random.randint(0, len(temp_dck)-1)
                    temp = temp_dck[index]
                    del temp_dck[index]
                    temp_dok.append(temp)
                d_tot_cap = sum(temp_dok)
            DOP = len(temp_dok)
    return temp_dok

def decoding(sources, depot, b, a, c ,v):
    temp_a = copy.deepcopy(a)
    temp_d = [0]*len(a)
    temp_b= copy.deepcopy(b)
    g = np.array([[0]*len(depot)]*len(sources)).astype(float)
    k=0
    j=0
    index=[0,0]
    for i in range(len(temp_a)):
        if a[i] == 0:
            v[i] = 0
    for i in range(len(temp_b)):
        if b[i] == 0:
            v[len(sources)+i]=0
    i=0
    while sum(v[len(sources):]) !=0: 
        temp_c =0
        was_passed = False
        i=i+1
        for x in range(len(v)):
            if v[x] == max(v) and x < len(sources):
                k = x
                for jl in range(len(depot)):
                    if v[len(sources)+jl] != 0:
                        if temp_c == 0 and was_passed == False:
                            temp_c = c[k][jl]
                            index[0]=k
                            index[1]=jl
                            was_passed = True
                        elif c[k][jl] < temp_c:
                            temp_c = c[k][jl]
                            index[0]=k
                            index[1]=jl
                j = index[1]
            elif v[x] == max(v) and x >= len(sources):
                j = x - len(sources)
                for kl in range(len(sources)):
                    if v[kl] != 0 :
                        if temp_c == 0 and was_passed == False:
                            temp_c = c[kl][j]
                            index[0]=kl
                            index[1]=j
                            was_passed=True
                        elif c[kl][j]<temp_c:
                            temp_c = c[kl][j]
                            index[0]=kl
                            index[1]=j
                k=index[0]
        g[k][j] = min(temp_a[k], temp_b[j])
        temp_a[k] = temp_a[k]-g[k][j]
        temp_d[k] = temp_d[k]+g[k][j]
        temp_b[j] = temp_b[j]-g[k][j]
        if temp_a[k] == 0:
            v[k] = 0
        if temp_b[j] == 0:
            v[len(sources)+j]= 0
    return g, temp_d
#----------------------------------------------
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


weight=np.array([[0.36459012, 0.31979052, 0.31561936]])
r=[0.36026144, 0.63973856]


file1 = open("semen66.txt", "w+")
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

population=np.array([[None]*3]*10)
for x in range(10):
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

mu = copy.deepcopy(population)
lambdas =copy.deepcopy(population)
generation = 0
the_number_of_generation=100
while generation < the_number_of_generation:    
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
    eval_mupluslambda=evaluate_problem2(decode_mupluslambda,sups, plant, up,distri,t,a,c,g,v,r[0],r[1],0.5,0.5)[0]
    newPopulation=[]
    
    #dict.fromkeys() digunakan untuk membuat list tidak 
    best_selection = sorted(list(dict.fromkeys(eval_mupluslambda)))[0:2]
    afterSelectBest = copy.deepcopy(mupluslambda)
    for i in range(len(best_selection)):
        newPopulation.append(mupluslambda[eval_mupluslambda.index(best_selection[i])])
        afterSelectBest.remove(mupluslambda[eval_mupluslambda.index(best_selection[i])])    
    decode_afterSelectBest =[0]*len(afterSelectBest)
    for x in range(len(afterSelectBest)):
        decode_afterSelectBest[x]=stage_1(pemasok, pabrik, pengantongan, distributor,1, sups, plant, up, distri,afterSelectBest[x][0],afterSelectBest[x][1],afterSelectBest[x][2],t,a).decode()
    eval_afterSelectBest = evaluate_problem2(decode_afterSelectBest,sups, plant, up,distri,t,a,c,g,v,r[0],r[1],0.5,0.5)[0] 
    
    bestOf = list(dict.fromkeys(eval_afterSelectBest))
    if len(bestOf) == len(mu)-len(newPopulation):
        for i in range(len(bestOf)):
            newPopulation.append(mupluslambda[eval_mupluslambda.index(bestOf[i])])
    else:
        pop = randomPopulation(len(sups),len(plant),len(pengantongan),len(distributor), len(mu)-len(newPopulation))        
        for i in range(len(pop)):
            newPopulation.append(pop[i])
    
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
    
        
decode_population =[0]*len(newPopulation)
for x in range(len(newPopulation)):
    decode_population[x]=stage_1(pemasok, pabrik, pengantongan, distributor, 1, sups,plant, up, distri,newPopulation[x][0],newPopulation[x][1],newPopulation[x][2],t,a).decode()    
greatPopulation = evaluate_problem2(decode_population,sups, plant, up,distri,t,a,c,g,v,r[0],r[1],0.5,0.5)

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
        str_population = [str(z)+"\n" for z in y]
        file1.writelines(str_population)
        file1.write("\n\n")
    file1.write("##################################\n")

df2 = pd.DataFrame({
        "generasi":generation+1,
        "f1":[greatPopulation[1][greatPopulation[0].index(min(greatPopulation[0]))]],
        "f2":[greatPopulation[2][greatPopulation[0].index(min(greatPopulation[0]))]],
        "Optimal":[greatPopulation[0][greatPopulation[0].index(min(greatPopulation[0]))]]})
df = df.append(df2, ignore_index=True)
    
export_excel = df.to_excel (r'/home/rudi/Documents/skripsi/selangseratus606.xlsx', index = None, header=True)
export_excel2 = hubdistpeng.to_excel (r'/home/rudi/Documents/skripsi/hubdistpeng808.xlsx', header=True)

plt.scatter(df['f1'],df['f2'], label="solusi optimal", color='r', s=15, marker="o")

plt.xlabel('f1')
plt.ylabel('f2')
plt.title('Grafik Optimal Pareto')
plt.legend()
plt.savefig('optimalparetosementonasa.png')
plt.show()

