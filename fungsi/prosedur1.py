## decoding prosedur 1 ###

import numpy as np
def decoding(sources, depot, b, a, c ,v):

    temp_a = [None]*len(a)
    temp_d = [0]*len(a)
    temp_b= [None]*len(b)
    for k in range(len(sources)):
        temp_a[k] = a[k]
#    print("===============prosedur 1============")
#    print(len(depot))
#    print(len(b))
    for j in range(len(depot)):
        temp_b[j]= b[j]

    g = np.array([[0]*len(depot)]*len(sources))
    k=0
    j=0
    index=[0,0]
    i=0 
    while sum(v[len(sources):]) !=0:  #dari prosedur yang diberikan didapat bahwasanya syaratnya bukan perihal semua v sama dengna 0
#        i=i+1
#        print('iterasi  ',i)
        temp_c =0
        for x in range(len(v)):
            if v[x] == max(v) and x < len(sources):
                k = x
                for jl in range(len(depot)):
#                    print('iterasine j  ', jl)
                    if v[len(sources)+jl] != 0:
                        if temp_c == 0:
                            temp_c = c[k][jl]
                            index[0]=k
                            index[1]=jl
                        elif c[k][jl] < temp_c:
#                            print('hai')
                            temp_c = c[k][jl]
                            index[0]=k
                            index[1]=jl
                j = index[1]
            elif v[x] == max(v) and x >= len(sources):
                j = x - len(sources)
                for kl in range(len(sources)):
                    if v[kl] != 0 :
                        if temp_c == 0:
                            temp_c = c[kl][j]
                            index[0]=kl
                            index[1]=j
                        elif c[kl][j]<temp_c:
                            temp_c = c[kl][j]
                            index[0]=kl
                            index[1]=j
                k=index[0]
#        print('maksimum v   ', max(v))
#        print('kj  ', k, j)                
#        print('paling murah  ', temp_c)
        g[k][j] = min(temp_a[k], temp_b[j])
        temp_a[k] = temp_a[k]-g[k][j]
        temp_d[k] = temp_d[k]+g[k][j]
#        print("temp_a   ", temp_a)
#        print("temp_d     ", temp_d)
        temp_b[j] = temp_b[j]-g[k][j]
        if temp_a[k] == 0:
            v[k] = 0
        if temp_b[j] == 0:
            v[len(sources)+j]= 0
#        if i == 50:
#            break
    return g, temp_d


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
#permintaan_plant=[0,150,150,400]
#persediaan_sups=[250, 0, 50]
#plant_dummy = ["p1","p2","p3", "dummy"]
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
#t = np.array([[4,3,1,0],[3,5,2,0],[1,6,4,0]])
#a = np.array([[5,2,4,3],[4,6,3,5],[3,5,1,6]])
#c = np.array([[3,5,2,4],[6,2,5,1],[4,3,6,5],[2,4,3,2]])
##
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
#print(decoding(supplier, plant_dummy, permintaan_plant, sups, t, [4, 7, 2, 1, 5, 3, 6]))

















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
