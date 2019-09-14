import numpy as np 
# C as cost
C = np.array([[11,19,17,18],[16,14,18,15],[15,16,19,13]])
depot = [300, 350, 300, 350]
sources = [550,300,450]
#g = np.array([[300,0,250,0],[0,300,0,0],[0,50,50,350]])
temp_sources = [None]*len(sources)
temp_depot= [None]*len(depot)
for k in range(len(sources)):
    temp_sources[k] = sources[k]

for j in range(len(depot)):
    temp_depot[j]=depot[j]
g =np.array([[0]*len(depot)]*len(sources))
v=[3,5,1,7,4,2,6]
k=0
j=0
index=[0,0]
i=0
while sum(v) !=0:
# for y in range(len(v)):
    # i=i+1
    # print("iterasi",i)
    temp_c =0
    for x in range(len(v)):
        if v[x] == max(v) and x < len(sources):
            k = x
            for jl in range(len(depot)):
                if v[len(sources)+jl] != 0:
                    if temp_c == 0:
                        temp_c = C[k][jl]
                        index[0]=k
                        index[1]=jl
                    elif C[k][j] < temp_c:
                        temp_c = C[k][jl]
                        index[0]=k
                        index[1]=jl
            j = index[1]
        elif v[x] == max(v) and x >= len(sources):
            j = x - len(sources)
            for kl in range(len(sources)):
                if v[kl] != 0 :
                    if temp_c == 0:
                        temp_c = C[kl][j]
                        index[0]=kl
                        index[1]=j
                    elif C[kl][j]<temp_c:
                        temp_c = C[kl][j]
                        index[0]=kl
                        index[1]=j
            k=index[0]
    # print(k, j)
    # print(sources[k])
    # print(depot[j])
    g[k][j] = min(temp_sources[k], temp_depot[j])
    # print(g[k][j])
    temp_sources[k] = temp_sources[k]-g[k][j]
    # print("update sources", sources[k])
    temp_depot[j] = temp_depot[j]-g[k][j]
    # print("update depot", depot[j])
    if temp_sources[k] == 0:
        v[k] = 0
    if temp_depot[j] == 0:
        v[len(sources)+j]= 0
print(g)
# print(sources)
# print(depot)
