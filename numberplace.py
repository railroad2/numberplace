#!/usr/bin/env python3
import numpy as np


class Numberplace(object):
    N = 0
    _cands = []
    _npl = []
    _cflags = []
    _nflags = []

    def __init__(self, N=3, rseed=np.random.randint(2**32-1), debug=False):
        self.N = N
        self.ndim = N*N
        self._rseed = rseed 
        self._init_arrays()
        self.debug=debug
        np.random.seed(rseed)


    def _init_arrays(self):
        self._npl = np.zeros((self.ndim, self.ndim), dtype=int)
        self._nflags = np.array(self._npl.copy() * 0, dtype=int)
        self._cands = np.arange(self.ndim, dtype=int) + 1
        self._cflags = np.ones((self.ndim, self.ndim, self.ndim), dtype=int)


    def idx2idxb(self, idx):
        idxb = []
        idxb.append(idx[0]//self.N)
        idxb.append(idx[1]//self.N)
        idxb.append(idx[0]%self.N)
        idxb.append(idx[1]%self.N)

        return idxb


    def idxb2idx(self, idxb):
        idx = []
        idx.append(idxb[0]*self.N+idxb[2])
        idx.append(idxb[1]*self.N+idxb[3])

        return idx


    def print(self, arr=None):
        N = self.N
        if arr is None:
            arr = self._npl

        hline = "-"*(N*N*4 + self.N + 1)
        print (hline)
        
        for i, npli in enumerate(arr):
            print ("|", end="")
            for j, nplj in enumerate(npli):
                if j%N == N-1:
                    end = "|"
                else:
                    end = ""
                if nplj == 0:
                    print (f"    ", end=end)
                else:
                    print (f" {nplj:2d} ", end=end)
            if i%N == N-1:
                print ("")
                print (hline)
            else:
                print ("")

        print ("\n")

        return

    def place_number(self, idx, num):
        if self._nflags[idx[0], idx[1]]:
            print (f"The cell {idx} is already filled.")
            if (self.debug):
                raise

        cflag = self._cflags[idx[0], idx[1]]
        if cflag[num-1] == 0:
            print (f"{num} does not fit to {idx}.") 
            if (self.debug):
                raise

        if (self.debug):
            print (f"idx : {idx} \nnum : {num}");
        
        self._npl[idx[0], idx[1]] = num
        self._nflags[idx[0], idx[1]] = 1

        self.down_flags(idx, num)


    def place_rand_number(self, idx):
        if self._nflags[idx[0], idx[1]] == 1:
            print (f"The cell {idx} is already filled.")
            if (self.debug):
                return
            else:
                raise

        cflag = self._cflags[idx[0], idx[1]]
        cand = self._cands[cflag==1]
        if len(cand):
            nidx = np.random.randint(len(cand))
            num = cand[nidx]
        else:
            print (f"No more candidates in the cell {idx}. ")
            if (self.debug):
                return 
            else:
                raise

        self.place_number(idx, num)

        return 


    def down_flags(self, idx, num):
        self._cflags[idx[0], idx[1]] = 0
        self._cflags[idx[0], :, num-1] = 0
        self._cflags[:, idx[1], num-1] = 0

        blki, blkj = np.array(idx) // self.N 
        self._cflags[blki*self.N:blki*self.N+3, blkj*self.N:blkj*self.N+3, num-1] = 0


