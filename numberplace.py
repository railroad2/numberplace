#!/usr/bin/env python3
import numpy as np


class Numberplace:
    N = 0
    npl = []
    ncandflag = []
    valflag = []

    cells = []

    class Cell:
        N = 3
        ndim = 9
        val = 0 
        valflag = 0
        cand = [] 
        candflag = []
        idx = []
        idxb = [] 
        blk = []

        def __init__(self, idx, N=3):
            self.N = N
            self.ndim = N*N
            self.idx = idx
            self.cand = list(range(N*N)) 
            self.candflag = np.ones(N*N)

    def __init__(self, N=3, rseed=np.random.randint(2**32-1), debug=False):
        self.N = N
        self.ndim = N*N
        self._rseed = rseed 
        self.debug=debug
        np.random.seed(rseed)
        self._init_cells()

    def _init_cells(self):
        for i in range(self.ndim):
            cells_row = []
            for j in range(self.ndim):
                idx = (i, j)
                celltmp = self.Cell(idx, self.N)
                celltmp.idxb = self.idx2idxb(idx)
                celltmp.blk = (celltmp.idxb[0], celltmp.idxb[1])
                cells_row.append(celltmp)
            self.cells.append(cells_row)
         

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
            arr = self.get_npl()

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
        i = idx[0]
        j = idx[1]
        cell = self.cells[i][j]

        cell.val = num
        cell.valflag = 1
        self.down_flags(idx, num)

    def place_rand_number(self, idx):
        pass


    def down_flags(self, idx, num):
        pass


    def get_npl(self):
        arr = []
        for i in range(self.ndim):
            arr_row = []
            for j in range(self.ndim):
                arr_row.append(self.cells[i][j].val)
            arr.append(arr_row)

        return arr

    def get_ncandflags(self):  
        ndim = self.ndim
        arr = np.zeros((ndim, ndim), dtype=int)
        for i in range(ndim):
            for j in range(ndim):
                arr[i,j] = sum(self.cells[i][j].candflag)

        return arr


def test():
    npl = Numberplace(N=3)
    npl.print()
    npl.print(npl.get_ncandflags())
    npl.place_number((3,3), 3)
    npl.print()
    npl.print(npl.get_ncandflags())
    

if __name__=="__main__":
    test()

