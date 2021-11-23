#!/usr/bin/env python3
import numpy as np


class Numberplace(object):
    N = 0
    _cands = []
    _npl = []

    def __init__(self, N=3, rseed=np.random.randint(2**32-1)):
        self.N = N
        self.ndim = N*N
        self._cands = self._define_cands()
        self._npl = self._empty_npl()
        self._idxgrp = self._define_idxgrp()
        self._rseed = rseed 
        np.random.seed(rseed)

    def _empty_npl(self):
        npl = []
        for i in range(self.ndim):
            npltmp = []
            for j in range(self.ndim):
                npltmp.append(0)
            npl.append(npltmp)

        return npl

    def _define_cands(self):
        candlist = list(range(1, self.ndim+1))
        cands = []
        for i in range(self.ndim):
            candstmp = []
            for j in range(self.ndim):
                candstmp.append(candlist.copy())
            cands.append(candstmp)

        return cands

    def _define_idxgrp(self):
        idxgrp = []

        for i in range(self.N):
            idxgrpj = []
            for j in range(self.N):
                idxgrpk = []
                for k in range(self.N):
                    idxgrpl = []
                    for l in range(self.N):
                        idxgrpl.append((i*self.N+k, j*self.N+l))

                    idxgrpk.append(idxgrpl)

                idxgrpj.append(idxgrpk)

            idxgrp.append(idxgrpj)

        return idxgrp

    def idx2idxg(self, idx):
        idxg = []
        idxg.append(idx[0]//self.N)
        idxg.append(idx[1]//self.N)
        idxg.append(idx[0]%self.N)
        idxg.append(idx[1]%self.N)

        return idxg

    def idxg2idx(self, idxg):
        idx = []
        idx.append(idxg[0]*self.N+idxg[2])
        idx.append(idxg[1]*self.N+idxg[3])

        return idx

    def show(self):
        N = self.N
        npl = self._npl

        hline = "-"*(N*N*4+self.N+1)
        print (hline)
        
        for i, npli in enumerate(npl):
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

    def place_rand_number(self, idx):
        cand = self._cands[idx[0]][idx[1]]
        if len(cand):
            num = cand[np.random.randint(len(cand))]
        else:
            print (f"No more candidates in the cell {idx}. ")
            #raise
            return 

        self._npl[idx[0]][idx[1]] = num
        self.remove_cand(idx, num)
        return 


    def remove_cand(self, idx, num):
        idxs  = [(i, idx[1]) for i in range(self.ndim)]
        idxs += [(idx[0], j) for j in range(self.ndim)]

        ii = idx[0] // self.N
        jj = idx[1] // self.N

        for ik in self._idxgrp[ii][jj]:
            idxs += ik
                
        for iidx in idxs:
            try:
                self._cands[iidx[0]][iidx[1]].remove(num)
            except:
                pass

