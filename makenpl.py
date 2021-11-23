#!/usr/bin/env python3
import numpy as np
import time
from numberplace import Numberplace


def make_numberplace_A1(npl):
    ## filling the npl in order of left to right, top to bottom

    N = npl.N
    for i in range(N**2):
        for j in range(N**2):
            idx = (i,j)
            npl.place_rand_number(idx)
            npl.print(hlidx=idx)

    print ("Result:")
    npl.print()


def make_numberplace_A2(npl):
    ## filling the npl 
    N = npl.N

    for k in range(N):
        for l in range(N):
            for i in range(N):
                for j in range(N):
                    idx = npl.idxb2idx((i,j,k,l))
                    npl.place_rand_number(idx)
                    npl.print(hlidx=idx)

    print ("Result:")
    npl.print()


def make_numberplace_A3(npl):
    ## filling the npl block by block
    N = npl.N
    for i in range(N):
        for j in range(N):
            for k in range(N):
                for l in range(N):
                    idx = npl.idxb2idx((i,j,k,l))
                    npl.place_rand_number(idx)
                    npl.print(hlidx=idx)

    print ("Result:")
    npl.print()


def make_numberplace_A4(npl):
    ## filling the npl uniformly distributing the candidate dropping
    N = npl.N
    for k in range(N):
        for l in range(N):
            for i in range(N):
                for j in range(N):
                    idx = npl.idxb2idx((i, j, (j+k)%N, (i+l)%N))
                    npl.place_rand_number(idx)
                    npl.print(hlidx=idx)

    print ("Result:")
    npl.print()


def make_numberplace_A5(npl):
    ## filling the npl in order of number 1 to N*N
    N = npl.N

    for num in range(1, N*N+1):
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    for l in range(N):
                        idx = npl.idxb2idx((i, j, k, l))
                        if npl.cells[idx[0], idx[1]].candflag[num-1] == 1:
                            npl.place_number(idx, num)
                            npl.print(hlidx=idx)

    npl.print()


def make_numberplace_A6(npl):
    ## filling the npl based on entropy
    N = npl.N
    ndim = npl.ndim

    t0 = time.time()
    while (1):
        entropy = npl.get_entropy_arr()
        if npl.debug:
            print (entropy)
        
        idxs = np.where(entropy == np.min(entropy)) 
        idxs = list(zip(*idxs))

        idx = idxs[np.random.randint(len(idxs))]
        res = npl.place_rand_number(idx)
        while res < 0:
            try:
                idxs.remove(idx) 
            except ValueError:
                res = npl.place_number(idx, -1, null=True)

            res = npl.place_rand_number(idx)

        if npl.debug:
            npl.print()

        if np.sum(npl.get_valflag_arr()) == npl.ndim**2:
            break

    t1 = time.time()
    print (f"Elapsed time: {t1 - t0} s")
    res = npl.validation()

    if 1:#res == 1:
        npl.write_result()
    if res == 1:
        npl.write_npl()
    
    return res


def A6loop(seed0=None, ntrymax=1000):
    N = 3
    npl = Numberplace(N)
    npl.debug = False

    if seed0 is None:
        print ("Enter initial seed to start from")
        return

    seed = seed0
    while (1): # seed loop
        npl.set_rseed(seed)
        ntry = 0
        nsuccess = 0

        while (ntry <= ntrymax): #ntry loop
            npl.ntry = ntry
            res = make_numberplace_A6(npl)

            if res == 1:
                nsuccess += 1

            ntry += 1

        seed += 1

def flagtest(npl):
    npl.place_rand_number((3,5))
    npl.print()
    npl.print(np.sum(npl._cflags, axis=-1))


def doit():
    N = 3
    rseed = None
    npl = Numberplace(N)
    npl.debug = False

    make_numberplace_A6(npl)


def doit2():
    A6loop()


if __name__=="__main__":
    doit()


