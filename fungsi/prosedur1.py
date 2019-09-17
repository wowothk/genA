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
    while sum(v[len(sources):]) !=0: #dari prosedur yang diberikan didapat bahwasanya syaratnya bukan perihal semua v sama dengna 0
#        i=i+1
#        print(i)
        temp_c =0
        for x in range(len(v)): 
            if v[x] == max(v) and x < len(sources):
                k = x
                for jl in range(len(depot)):
                    if v[len(sources)+jl] != 0:
                        if temp_c == 0:
                            temp_c = c[k][jl]
                            index[0]=k
                            index[1]=jl
                        elif c[k][j] < temp_c:
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

#C = np.array([[11,19,17,18],[16,14,18,15],[15,16,19,13]])
#j = ['d1','d2','d3','d4']
#k=['p1','p2','p3']
#depot = [300, 350, 300, 350]
#sources = [550,400,450]
#
#v=[3,5,1,7,4,2,6]

#print(decoding(k, j, depot, sources, C,v)[1])
