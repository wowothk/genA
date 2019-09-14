import numpy as np 
from priority_based import encoding, decoding
# C as cost
# source = [1,2,3]
# depot =[1,2,3,4]
# C = np.array([[11,19,17,18],[16,14,18,15],[15,16,19,13]])
# b = [300, 350, 300, 350]
# a = [550,300,450]
# g = np.array([[300,0,250,0],[0,300,0,0],[0,50,50,350]])
# v=[3,5,1,7,4,2,6]

# sumber = [1,2,3,4,5]
# tujuan= [1,2,3,45,5]
# q=np.array([[50,100,0,0,0],[0,0,0,0,0],[0,0,50,100,50],[0,0,0,0,0],[0,0,0,0,0]])
# persediaan =[150,100,200,100,50]
# permintaan=[50,100,50,50,100,50]
#supplier = ["s1","s2","s3"]
#plant = ["p1","p2","p3"]
#dc = ["dc1","dc2","dc3","dc4"]
#customer =["cust1","cust2", "cust3","cust4"]
#
#import numpy as np
sups =[250,200,250]
D = [200,150,200] 
#W = [150, 100, 200, 100]
#d = [50, 100, 50, 100]
#
b = np.array([[0,150,100],[0,0,0],[0,0,50]]) 
#f = np.array([[0,0,0,0],[0,0,150,0],[150,0,0,0]])
#q = np.array([[50,100,0,0],[0,0,0,0],[0,0,50,100],[0,0,0,0]])
#
t = np.array([[4,3,1],[3,5,2],[1,6,4]])
#a = np.array([[5,2,4,3],[4,6,3,5],[3,5,1,6]])
#c = np.array([[3,5,2,4],[6,2,5,1],[4,3,6,5],[2,4,3,2]])
chromosom = encoding(t, sups,D, b)
print(chromosom)
g1 = decoding(C,sources,depot,chromosom)
print(g1)

