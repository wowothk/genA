## decoding prosedur 1 ###
import copy
import numpy as np
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
#    print('v   ', v)
#    print(temp_a, temp_b)
    i=0
    while sum(v[len(sources):]) !=0:  #dari prosedur yang diberikan didapat bahwasanya syaratnya bukan perihal semua v sama dengna 0
        temp_c =0
        was_passed = False
        i=i+1
#        print('#####iteration',i)
#        if i == 8:
#            break
#        print('max(v)   :', max(v))
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
#                print(k,j)
            elif v[x] == max(v) and x >= len(sources):
                j = x - len(sources)
                for kl in range(len(sources)):
                    if v[kl] != 0 :
                        if temp_c == 0 and was_passed == False:
                            temp_c = c[kl][j]
                            index[0]=kl#        print('#####iteration'#        print('#####iteration',i),i)
                            index[1]=j
#                            print('temp_c', temp_c)
#                            print('c[k][j]', c[kl][j])
#                            print('k  ',kl)
                            was_passed=True
                        elif c[kl][j]<temp_c:
                            temp_c = c[kl][j]
                            index[0]=kl
                            index[1]=j
                k=index[0]
#                print(k,j)
#        print(temp_a[k],temp_b[j])
        g[k][j] = min(temp_a[k], temp_b[j])
#        print(temp_a, temp_b)
#        print('============')
#        tempg=min(temp_a[k], temp_b[j])
#        print(tempg)
#        print('g[k][j]',g[k][j])
        temp_a[k] = temp_a[k]-g[k][j]
        temp_d[k] = temp_d[k]+g[k][j]
        temp_b[j] = temp_b[j]-g[k][j]
#        print(j)
        if temp_a[k] == 0:
            v[k] = 0
        if temp_b[j] == 0:
            v[len(sources)+j]= 0
#        print(v)
#        print('============')
    return g, temp_d


#import pandas as pd
#
#data_Path = '/home/rudi/Documents/import_excel/datacustomer.xlsx'
#
#dataNama = pd.read_excel(data_Path,sheet_name='naming')
#supplier = np.array(dataNama['supplier'].dropna(how='any'))
#plant = np.array(dataNama['plant'].dropna(how='any'))
#dc = np.array(dataNama['dc'].dropna(how='any'))
#customer =np.array(dataNama['customer'].dropna(how='any'))
#
#dataCapacity = pd.read_excel(data_Path, sheet_name="kapasitas")
#supsinton =np.array(dataCapacity['supplier (ton)'].dropna(how='any'))
#D = np.array(dataCapacity['plant(pac)'].dropna(how='any'))
#W = np.array(dataCapacity['dc(pac)'].dropna(how='any'))
#sups = [None]*len(supsinton)
#for x in range(len(supsinton)):
#    sups[x] = supsinton[x]/0.2458
#    
#dataDemand = pd.read_excel(data_Path, sheet_name = 'permintaan customer')
#d = np.array(dataDemand['demand'])
#
#t = np.array(pd.read_excel(data_Path, sheet_name='supplier ke plant').iloc[:,1:4])
#a = np.array(pd.read_excel(data_Path, sheet_name='plant ke dc').iloc[:,1:7])
#c = np.array(pd.read_excel(data_Path, sheet_name='dc ke customer').iloc[:,1:64])


#supplier = ["s1","s2","s3"]
#plant = ["p1","p2","p3"]
#dc = ["dc1","dc2","dc3","dc4"]
#customer =["cust1","cust2", "cust3","cust4"]
#
#sups =[250,200,250]
#D = [200,150,200] 
#W = [150, 100, 200, 100]
#d = [50, 100, 50, 100]
#
#permintaan_plant=[200,100,0,400]
#persediaan_sups=[250, 200, 250]
#plant_dummy = ["p1","p2","p3", "dummy"]
#dc_dummy = ["dc1","dc2","dc3","dc4",'dummy']
#perse= [200, 150, 0,0]
#permi= [0, 0, 200, 100,50]
#
#c1=[100,100,150]
#c2=[50,150,100,50]
#c3=np.array([[1,6,5,2],[6,2,4,5],[3,4,2,1]])
#c4=np.array([[50,0,50,0],[0,100,0,0],[0,50,50,50]])
#b1= np.array([[0,0,0],[150,0,0],[0,150,0]])
#
#b = np.array([[0,150,100],[0,0,0],[0,0,50]]) 
#f = np.array([[0,0,0,0],[0,0,150,0],[150,0,0,0]])
#q = np.array([[50,100,0,0],[0,0,0,0],[0,0,50,100],[0,0,0,0]])
#
#t = np.array([[4,3,1,100],[3,5,2,100],[1,6,4,100]])
#a = np.array([[5,2,4,3,0],[4,6,3,5,0],[3,5,1,6,0]])
#c = np.array([[3,5,2,4],[6,2,5,1],[4,3,6,5],[2,4,3,2]])
#
##stage1 = priority_based_enc(supplier, plant, persediaan_sups, permintaan_plant, t, b)
##v1 = stage1.encoding()
##print(v1)
#v1=[6,4,3,2,7,5,1]
#v2=[6,4,2,3,7,5,1]
#v3=[3,7,4,2,6,5,1]
#v1.pop()
#v2.pop()
#v3.pop()
#print(v1)
#
#print(decoding(supplier, plant, sups, D, t, [5, 8, 6, 7, 2, 1, 4, 3]))

















#C = np.array([[11,19,17,18],[16,14,18,15],[15,16,19,13]])
#C1 = np.array([[1,6,5,2],[6,2,4,5],[3,4,2,1]])
#j = ['d1','d2','d3','d4']
#k=['p1','p2','p3']
#depot = [300, 350, 300, 350]
#depot1=[50,150,100,50]
#sources = [550,300,450]
#source1=[100,100,150]
#
#c1=[100,100,150]
#c2=[50,150,100,50]
#c3=np.array([[1,6,5,2],[6,2,4,5],[3,4,2,1]])
#
#v=[3,5,1,7,4,2,6]
#v1=[3,7,4,2,6,1,5]
#v2= [1, 5, 3, 7, 4, 2, 6]
##
#print(decoding(k, j, c2, c1, c3,v2)[0])
