#!/usr/bin/env python3
import numpy as np
from numberplace import Numberplace


def make_numberplace_A1(N=3, rseed=None):
    ## filling the npl in order of left to right, top to bottom
    npl = Numberplace(N, rseed)

    for i in range(N**2):
        for j in range(N**2):
            idx = (i,j)
            npl.place_rand_number(idx)
            npl.print()

    print ("Result:")
    npl.print()


def make_numberplace_A2(N=3, rseed=None):
    ## filling the npl 
    npl = Numberplace(N, rseed)

    for k in range(N):
        for l in range(N):
            for i in range(N):
                for j in range(N):
                    idx = npl.idxb2idx((i,j,k,l))
                    npl.place_rand_number(idx)
                    npl.print()

    print ("Result:")
    npl.print()


def make_numberplace_A3(N=3, rseed=None):
    ## filling the npl block by block
    npl = Numberplace(N, rseed)

    for i in range(N):
        for j in range(N):
            for k in range(N):
                for l in range(N):
                    idx = npl.idxb2idx((i,j,k,l))
                    npl.place_rand_number(idx)
                    npl.print()

    print ("Result:")
    npl.print()


def make_numberplace_A4(N=3, rseed=None):
    ## filling the npl uniformly distributing the candidate dropping
    npl = Numberplace(N, rseed)
    npl.debug = True

    for k in range(N):
        for l in range(N):
            for i in range(N):
                for j in range(N):
                    idx = npl.idxb2idx((i, j, (j+k)%N, (i+l)%N))
                    npl.place_rand_number(idx)
                    npl.print()

    print ("Result:")
    npl.print()


def make_numberplace_A5(N=3, rseed=None):
    ## filling the npl in order of number 1 to N*N
    npl = Numberplace(N, rseed)
    npl.debug = True

    for num in range(1, N*N+1):
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    for l in range(N):
                        idx = npl.idxb2idx((i, j, k, l))
                        if npl._cflags[idx[0], idx[1], num-1] == 1:
                            npl.place_number(idx, num)

    npl.print()

def flagtest(N=3, rseed=None):
    npl = Numberplace(N, rseed)
    npl.debug=True

    npl.place_rand_number((3,5))
    npl.print()
    npl.print(np.sum(npl._cflags, axis=-1))


if __name__=="__main__":
    make_numberplace_A5(3, 0)

    #flagtest(N=3, rseed=0)


