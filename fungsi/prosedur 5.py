## decoding stage 1###
# input
# S : set of suppliers
# K : set of plants
# D' : total customer demand for product on plant k
# t_sk : unit transportation and purchasing cost of raw material from
# suppliers s to plant k
# u : utilization rate of raw material per unit of product
# a_k : the amount of raw material to produce the product on plant K
# v(s+k) : chromosom, for all s in S, for all k in k
#output 
# b_sk : the amount of raw material shipped from supplier s to plant k
import numpy as np
def decode_pb_1(S, K, D, t, u,  v):
    b=np.array([[0]*len(S)]*len(K))
    a=[0]*len(K)
    for k in range(len(K)):
        a[k]=D[k]*u
    
    from prosedur1 import decoding
    decoding(S, K, D, a, u ,v)

    