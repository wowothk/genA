import random
import numpy as np
import copy

class priority_based_enc:
    def __init__(self, sources, depot, a, b, c, g):
        self.sources = sources
        self.depot = depot
        self.a = a
        self.b = b
        self.c = c
        self.g = g
#        self.P = P
    """
    dengan 
    sources: himpunan sumber; depot: himpunan tujuan;
    a: kapasitas sumber; b: kapasitas tujuan;
    c: matrik biaya; g: banyaknya yang dikirim dari sources k ke depot j
    P: maksimum tujuan
    """
    
    def encoding(self):
        temp_sources = [None]*len(self.sources)
        temp_depot= [None]*len(self.depot)
        temp_a = [None]*len(self.sources)
        temp_b = [None]*len(self.depot)
        temp_g = np.array([[None]*len(self.depot)]*len(self.sources))
        temp_c = np.array([[None]*len(self.depot)]*len(self.sources))
        for k in range(len(self.sources)):
            temp_sources[k] = self.sources[k]
            temp_a[k] = self.a[k]
            
        for j in range(len(self.depot)):
            temp_depot[j]=self.depot[j]
            temp_b[j] = self.b[j]
                
        for k in range(len(self.sources)):
            for j in range(len(self.depot)):
                temp_g[k][j] = self.g[k][j]
                temp_c[k][j] = self.c[k][j]
#        print('temp_sources  ', temp_sources)
#        print('temp_depot   ', temp_depot )
#        print('permintaan  ',temp_b)
#        print('persediaan  ', temp_a)
#        print('yang dikirim  ', temp_g)
#        print('biaya   ', temp_c)
#        DCK = [] # set of closed depot
#        P = self.P # the number of depot that can open
#        
#        if P!=0:
#            for k in range(len(self.depot)-P):
#                if DCK ==[]:
#                    i = random.randint(0,len(temp_depot)-1) # index of temp_depot
#                else:
#                    x = 0
#                    while i == temp_depot.index(DCK[x]):
#                            i = random.randint(0, len(temp_depot)-1)
#                            if x == len(temp_depot):
#                                x = 0
#                       
#                DCK.append(temp_depot[i])
#                temp_b[i] = 0
#                for j in range(len(self.sources)):
#                    temp_g[j][i] = 0
#        print("##### setup g")
#        print(temp_g)
#        if len(DCK)!=0:
#            temp_depot.append("dummy")
#            dummy_column =np.array([[0]*len(self.sources)]).T
#            for i in range(len(DCK)):
#                col = np.array([self.g[:,self.depot.index(DCK[i])]])
#                dummy_column = dummy_column + col.T
#            temp_b.append(int(sum(dummy_column)))
#            temp_g = np.append(temp_g, dummy_column, 1)
#            dummy_cost =np.array([[0]*len(self.sources)]).T
#            temp_c = np.append(temp_c, dummy_cost, 1)
#        
        v = [None]*(len(temp_depot)+len(temp_sources))
        p = len(temp_depot)+len(temp_sources)
        i=0
#        print("+++++++++++++++++++++++++++++++")
#        print(temp_sources)
#        print(temp_depot)
#        print(temp_g)
#        print(temp_b)
#        print(temp_a)
#        print(temp_c)
#        print(temp_g)
        index=[0,0]
        temp_index = copy.deepcopy(index)
#        checking_none=[]  or checking_none != v
#        while temp_b[index[1]] != 0 or temp_a[index[0]] != 0:
        while sum(temp_b) != 0 or sum(temp_a)!=0: 
        #while sum(temp_b) != 0 or sum(temp_a)!=0: pakai ini untuk cara yang satunya atau dkl yg mendefinisikan dummy secara detail
            #ini yang kuganti barusan 
            #jadi ketika jumlahannya nol itu memastikan bahwa setiap depot atau source sama dengan nol
            # kemudian untuk depot yang closed dia akan digenerate dengan iterasi for setelah while
            # kemudian juga diperhatikan bahwasanya sebelum memasuki proses ini harus ada pembentukan dummy
            i=i+1
#            print(i)
#            print(index)
            temp_cost = 0 
            was_passed = False
            for k in range(len(temp_sources)):
#                temp_cost = 0
                for j in range(len(temp_depot)):
                    
                    if temp_g[k][j] != 0 and (temp_b[j] == temp_g[k][j] or temp_a[k]==temp_g[k][j]):
                        if temp_cost == 0 and was_passed == False:
                            temp_cost=temp_c[k][j]
                            index[0] = k
                            index[1] = j
                            was_passed = True
                        elif temp_c[k][j] < temp_cost:
                            temp_cost = temp_c[k][j]
                            index[0] = k
                            index[1] = j
                    
#            print("temp_cost", temp_cost)
            
            if i !=0 and index == temp_index:
                for k in range(len(temp_sources)):
#                temp_cost = 0
                    for j in range(len(temp_depot)):
                        if temp_g[k][j] != 0:
                            if temp_cost == 0 and was_passed == False:
                                temp_cost=temp_c[k][j]
                                index[0] = k
                                index[1] = j
                                was_passed = True
                            elif temp_c[k][j] < temp_cost:
                                temp_cost = temp_c[k][j]
                                index[0] = k
                                index[1] = j
                            
            temp_index= copy.deepcopy(index)
            temp_b[index[1]] = temp_b[index[1]]-temp_g[index[0]][index[1]]
            temp_a[index[0]] = temp_a[index[0]]-temp_g[index[0]][index[1]] 
#            print("tem_b", temp_b)
#            print("temP_ a", temp_a)
#            print(temp_b[index[1]])   
#            print(temp_a[index[0]])
#            print(temp_g)
#            print("++++++++")
            if temp_b[index[1]] == 0 :
                v[len(temp_sources)+index[1]] = p 
                p = p-1
                temp_g[index[0]][index[1]] = 0
            if  temp_a[index[0]] == 0 :
                v[index[0]] = p 
                p = p-1
                temp_g[index[0]][index[1]] = 0
            
#            print(temp_b[index[1]])
#            print(temp_a[index[0]])
#            checking_none = list(filter(None, v))
#            print(checking_none)
#            print(v)
#            if i == len(temp_depot)+len(temp_sources):
#                break
            if i == 50:
                break
#        print(v)
        for l in range(p):
            t = random.randint(0, len(temp_depot)+len(temp_sources)-1)
            while v[t] != None:
                t = random.randint(0, len(temp_depot)+len(temp_sources)-1)
            v[t] = l+1
#        print(v)
        ##### tambahan #####
#        print(sum(temp_a))
        if sum(temp_b) == 0 and sum(temp_a) !=0:
            
#            temp_a = 0
            v.append(0)
#            print('temp_b  ', temp_b)
#            print('v  ', v)
            for x in range(len(v)):
                v[x]=v[x]+1
            
            ####################
        return v

class integer_encoding:
    def __init__(self, sources, depot, a, b, c, q):
        self.sources = sources
        self.depot = depot
        self.a = a
        self.b = b
        self.c = c
        self.q = q
    
    """
    dengan 
    sources: himpunan sumber; depot: himpunan tujuan;
    a: kapasitas sumber; b: kapasitas tujuan;
    c: matrik biaya; q: banyaknya yang dikirim dari sources k ke depot j
    """
    def encode(self):
        v = [0]*len(self.depot)
        for j in range(len(self.sources)):
            for i in range(len(self.depot)):
                if self.q[j][i] != 0:
                    v[i] = j+1
        
        return v
#
#"""
#dc: gudang
#plant : pabrik
#
#sups: kapasitas suplier
#D : kapasitas plant
#W : kapasitas cc
#d : banyaknya permintaan customer
#
#b : banyaknya barang yang dikirim dari suplier ke plant
#f : banyaknya barang yang dikirim dari plant ke dc
#q : banyaknya barang yang dikirim dari dc ke customer
#
#t : biaya pengiriman barang dari suplier ke pabrik
#a : biaya pengiriman barang dari pabrik ke dc
#c : biaya pengiriman barang dari dc ke customer
#
#"""
#supplier = ["s1","s2","s3"]
#plant = ["p1","p2","p3"]
#dc = ["dc1","dc2","dc3","dc4"]
#customer =["cust1","cust2", "cust3","cust4"]
#
#x=[np.array([[ 50,   0,   0],
#         [  0,   0,   0],
#         [150, 100,   0]]), np.array([[  0,   0, 200,   0,0],
#         [  0,   0,   0, 100,50],
#         [  0,   0,   0,   0,0]]), np.array([[  0,   0,   0,   0],
#         [  0,   0,   0,   0],
#         [ 50, 100,  50,   0],
#         [  0,   0,   0, 100]]), [1, 1, 0], np.array([0, 0, 1, 1])]
#
#sups =[250,200,250]
#D = [200,150,200] 
#W = [150, 100, 200, 100]
#d = [50, 100, 50, 100]
#
#permintaan_plant=[0,150,150,400]
#persediaan_sups=[250, 0, 50]
#plant_dummy = ["p1","p2","p3", "dummy"]
#dc_dummy = ["dc1","dc2","dc3","dc4",'dummy']
#c1=[100,100,150]
#c2=[50,150,100,50]
#c3=np.array([[1,6,5,2],[6,2,4,5],[3,4,2,1]])
#c4=np.array([[50,0,50,0],[0,100,0,0],[0,50,50,50]])
#b1= np.array([[0,0,0],[150,0,0],[0,150,0]])
#
#b = np.array([[0,150,100,0],[0,0,0,200],[0,0,50,200]]) 
#f = np.array([[0,0,0,0],[0,0,150,0],[150,0,0,0]])
#q = np.array([[50,100,0,0],[0,0,0,0],[0,0,50,100],[0,0,0,0]])
#
#t = np.array([[4,3,1,0],[3,5,2,0],[1,6,4,0]])
#a = np.array([[5,2,4,3],[4,6,3,5],[3,5,1,6]])
#t_a=np.array([[5,2,4,3,0],[4,6,3,5,0],[3,5,1,6,0]])
#c = np.array([[3,5,2,4],[6,2,5,1],[4,3,6,5],[2,4,3,2]])
##
#stage1 = priority_based_enc(plant, dc_dummy, [200, 150, 0], [0, 0, 200, 100,50], t_a, x[1])
#v1 = stage1.encoding()
#print(v1)
#stage2 = priority_based_enc(plant, dc, D, W, a, f, 3)
#v2 = stage2.encoding()
#stage3 = integer_encoding(dc, customer, W, d, c, q)
#v3 = stage3.encode()
#
#v=[0]*(len(v1)+len(v2)+len(v3))
#for i in range(len(v)):
#    if i < len(v1):
#        v[i] = v1[i]
#    elif i >= len(v1) and i < len(v2):
#        v[i] = v2[i-len(v1)]
#    else:
#        v[i] = v3[i-len(v2)]
#
#print(v)





