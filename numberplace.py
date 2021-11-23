#!/usr/bin/env python3
import os
import copy
import numpy as np


class Numberplace:
    N = 0
    status = 0
    ntry = 0
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
            self.val = 0
            self.valflag = 0
            self.idx = idx
            self.idxb = []
            self.blk = []
            self.cand = list(np.arange(N*N)+1)
            self.candflag = np.ones(N*N)


    def __init__(self, N=3, rseed=None, reset_rng=True, debug=False):
        self.N = N
        self.ndim = N*N
        self.debug=debug
        self.cells = []
        self._init_cells()
        self.status = None
        self.ntry = None
        self.reset_rng = reset_rng

        if rseed is None:
            self.rseed = np.random.randint(2**32-1)
        else:
            self.rseed = rseed

        if reset_rng:
            np.random.seed(self.rseed)
            
        try:
            os.mkdir ('result')
        except:
            pass
        try:
            os.mkdir ('npl')
        except:
            pass

    def _init_cells(self):
        self.cells = []
        for i in range(self.ndim):
            cells_row = []
            for j in range(self.ndim):
                idx = (i, j)
                celltmp = self.Cell(idx, self.N)
                celltmp.idxb = self.idx2idxb(idx)
                celltmp.blk = (celltmp.idxb[0], celltmp.idxb[1])
                cells_row.append(celltmp)
            self.cells.append(cells_row)
        self.cells = np.array(self.cells) 

    def reset(self):
        self.__init__(N=self.N, rseed=self.rseed, reset_rng=self.reset_rng, debug=self.debug)
        

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


    def print(self, arr=None, hlidx=None, returnmsg=False):
        try:
            hi, hj = hlidx
        except:
            hi, hj = (None, None)

        N = self.N
        if arr is None:
            arr = self.get_npl_arr()

        hline = "-"*(N*N*4 + self.N + 1) 

        msg = ""

        msg += hline + "\n"
        
        for i, npli in enumerate(arr):
            msg += "|"
            for j, nplj in enumerate(npli):
                try:
                    msgseg = f" {nplj:2d} "
                except ValueError:
                    msgseg = f" {nplj:2.2f} "
                if nplj < 1:
                    msgseg = '\033[91m' + msgseg + '\033[0m'

                if i==hi and j==hj:
                    msgseg = '\033[95m' + msgseg + '\033[0m'

                msg += msgseg 
                msg += "|" if j%N == N-1 else "" 

            if i%N == N-1:
                msg += "\n"
                msg += hline

            msg += "\n"

        msg += "\n"

        if returnmsg:
            return msg
        else:
            print (msg)

        return 


    def place_number(self, idx, num, test=True, null=False):
        if self.debug:
            print (f"Placing {num} at {idx}.")

        if null:
            test=False

        i, j = idx
        if test:
            if self.cells[i, j].val > 0:
                if self.debug:
                    print (f"A number {self.cells[i,j].val} is already placed at {idx}.")
                return 0

            res = self.test_null_cell(idx, num)
            if res < 0:
                if self.debug:
                    print (f"Cannot place {num} at {idx}, cuz it makes null cell.")
                return -1
                
            res = self.test_row_unique(idx)
            if res > 0:
                if num != res:
                    if self.debug:
                        print (f"From row unique test: Placing {res} instead of {num} at {idx}.")
                    num = res

            res = self.test_col_unique(idx)
            if res > 0:
                if num != res:
                    if self.debug:
                        print (f"From col unique test: Placing {res} instead of {num} at {idx}.")
                    num = res

            res = self.test_blk_unique(idx)
            if res > 0:
                if num != res:
                    if self.debug:
                        print (f"From blk unique test: Placing {res} instead of {num} at {idx}.")
                    num = res

        cell = self.cells[i,j]

        cell.val = num

        if null:
            cell.valflag = 1
            cell.cand = []
            cell.candflag[:] = 0
        else:
            self.change_flags(idx, num)

        if test:
            self.test_all_unique()

        return 0


    def place_rand_number(self, idx):
        row, col = idx
        cell = self.cells[row, col]
        try:
            num = cell.cand[np.random.randint(len(cell.cand))] 
            res = self.place_number(idx, num)
        except ValueError as e:
            if self.debug:
                print (f"ValueError: {e}, num = -1")
            res = self.place_number(idx, -1, null=True) 

        if res < 0:
            return -1 

        return 0


    def change_flags(self, idx, num, cells=None):
        if cells is None:
            cells = self.cells
        else:
            cells = cells

        row, col = idx
        cell = cells[row, col]
        cells_row = list(cells[row,:])
        cells_col = list(cells[:,col])
        blki, blkj = cell.blk
        cells_blk = list((cells[self.N*blki: self.N*(blki + 1), self.N*blkj:self.N*(blkj + 1)]).flatten())

        cells_list = cells_row + cells_col + cells_blk
        cell.valflag = 1
        cell.cand = []
        cell.candflag[:] = 0

        for c in cells_list:
            try:
                c.candflag[num-1] = 0
                c.cand.remove(num)
            except ValueError as e:
                if self.debug:
                    pass #print (e) 

        return 


    def get_cells_blk(self, blk):
        blki, blkj = blk 
        return self.cells[self.N*blki: self.N*(blki + 1), self.N*blkj:self.N*(blkj + 1)]


    def get_npl_arr(self):
        arr = []
        for i in range(self.ndim):
            arr_row = []
            for j in range(self.ndim):
                arr_row.append(self.cells[i,j].val)
            arr.append(arr_row)

        return arr

    def get_valflag_arr(self, cells=None):
        if cells is None:
            cells = self.cells
        ndim = self.ndim
        arr = np.zeros((ndim, ndim), dtype=int)
        for i in range(ndim):
            for j in range(ndim):
                arr[i,j] = cells[i,j].valflag

        return arr

    def get_ncandflag_arr(self, cells=None):  
        if cells is None:
            cells = self.cells

        ndim = self.ndim
        arr = np.zeros((ndim, ndim), dtype=int)

        for i in range(ndim):
            for j in range(ndim):
                arr[i,j] = sum(cells[i,j].candflag)

        return arr

    def get_entropy(self, idx):
        ncand_arr = self.get_ncandflag_arr()
        rncand_arr = self.ndim - np.array(ncand_arr)
        
        i, j = idx
        blki, blkj, _, _ = self.idx2idxb(idx)
        entropy = np.sum(rncand_arr[i,:])
        entropy += np.sum(rncand_arr[:,i])
        entropy += np.sum(rncand_arr[self.N*blki:self.N*(blki+1), self.N*blkj:self.N*(blkj+1)])
        entropy += rncand_arr[i-1, j] if i-1 > -1 else 0
        entropy += rncand_arr[i+1, j] if i+1 < self.ndim else 0
        entropy += rncand_arr[i, j-1] if j-1 > -1 else 0
        entropy += rncand_arr[i, j+1] if j+1 < self.ndim else 0
        entropy += self.cells[i,j].valflag*1000
        
        return entropy
        
    def get_entropy_arr(self, cells=None):
        if cells is None:
            cells = self.cells

        ndim = self.ndim
        arr = np.zeros((ndim, ndim))

        for i in range(ndim):
            for j in range(ndim):
                arr[i,j] = self.get_entropy((i,j))

        return arr
        

    def test_null_cell(self, idx, num):
        cells = copy.deepcopy(self.cells)
        self.change_flags(idx, num, cells=cells)
        ncandflag = self.get_ncandflag_arr(cells=cells)
        valflag = self.get_valflag_arr(cells=cells)
        zeroflag = ncandflag + valflag

        if 0 in zeroflag:
            if self.debug:
                print (zeroflag)
            return -1

        return 0 

    def test_all_unique(self):
        cells = self.cells
        for ci in cells:
            for cell in ci:
                if len(cell.cand) == 1:
                    num = cell.cand[0]
                    if self.debug:
                        print ("From all unique test: ", end="")
                    self.place_number(cell.idx, num)


    def test_row_unique(self, idx):
        row, col = idx
        cells_row = self.cells[row,:] 

        for num in self.cells[row, col].cand:
            rowflags = []
            for cell in cells_row: 
                rowflags.append(cell.candflag[num-1])

            if sum(rowflags) == 1:
                return num

        return 0

    def test_col_unique(self, idx):
        row, col = idx
        cells_col = self.cells[:,col] 

        for num in self.cells[row, col].cand:
            colflags = []
            for cell in cells_col: 
                colflags.append(cell.candflag[num-1])

            if sum(colflags) == 1:
                return num

        return 0

    def test_blk_unique(self, idx):
        row, col = idx
        blki, blkj = self.cells[row, col].blk
        cells_blk = (self.cells[self.N*blki: self.N*(blki + 1), self.N*blkj:self.N*(blkj + 1)]).flatten()

        for num in self.cells[row, col].cand:
            blkflags = []
            for cell in cells_blk: 
                blkflags.append(cell.candflag[num-1])

            if sum(blkflags) == 1:
                return num

        return 0

    def validation(self, silent=False):
        npl = np.array(self.get_npl_arr())
        N = self.N
        ndim = self.ndim

        if not silent:
            print ("="*50)
            print (f"Seed: {self.rseed}")
            print (f"Ntry: {self.ntry}")
            print (f"Result:")
            self.print()

        num, cnt = np.unique(npl, return_counts=True)
        try:
            nerrorcell = dict(zip(num, cnt))[-1]
        except:
            nerrorcell = 0
        isok = "OK" if cnt.all() == 9  else "Error"

        if self.debug:
            print (f"total: {dict(zip(num, cnt))} ({isok})") 

        if not silent:
            print (f"Number of error cells: {nerrorcell}")

        errorcnt = nerrorcell
        correct = np.sum(np.arange(ndim)+1)

        if self.debug: print ("Row test")
        for i in range(ndim):
            num, cnt = np.unique(npl[i, :], return_counts=True)
            dic = dict(zip(num, cnt))
            if -1 in num:
                del dic[-1]
            if (len(cnt)==ndim and sum(cnt)==ndim and sum(num)==correct):
                isok = "OK" 
            else:
                isok = "Error"
                errorcnt += 1

            if self.debug:
                print (f"\trow #{i}: {dic}, sum= {sum(num)} ({isok})") 

        if self.debug: print ("Column test")
        for i in range(ndim):
            num, cnt = np.unique(npl[:, i], return_counts=True)
            dic = dict(zip(num, cnt))
            if -1 in num:
                del dic[-1]
            if (len(cnt)==ndim and sum(cnt)==ndim and sum(num)==correct):
                isok = "OK" 
            else:
                isok = "Error"
                errorcnt += 1

            if self.debug:
                print (f"\tcol #{i}: {dic}, sum= {sum(num)} ({isok})") 

        if self.debug: print ("Block test")
        for i in range(N):
            for j in range(N):
                num, cnt = np.unique(npl[N*i:N*(i+1),N*j:N*(j+1)], return_counts=True)
                dic = dict(zip(num, cnt))
                if -1 in num:
                    del dic[-1]
                if (len(cnt)==ndim and sum(cnt)==ndim and sum(num)==correct):
                    isok = "OK" 
                else:
                    isok = "Error"
                    errorcnt += 1

                if self.debug:
                    print (f"\tblock #{i},{j}: {dic}, sum= {sum(num)} ({isok})") 

        if errorcnt == 0:
            self.status = "SUCCESS"
            if not silent:
                print (self.status)
            return 1
        else:
            self.status = "FAIL"
            if not silent:
                print (self.status)
            return -1

        return 0
    
    def write_result(self):
        fname = f"./result/result_N{self.N}_seed{self.rseed}_ntry{self.ntry}_{self.status}.txt"
        with open(fname, 'a') as f:
            f.write(f"Seed: {self.rseed}\n")
            f.write(f"Ntry: {self.ntry}\n")
            f.write(f"Result: \n\n")
            f.write(f"{self.print(returnmsg=True)}")

        return
    
    def write_npl(self):
        fname = f"./npl/npl_N{self.N}_seed{self.rseed}_ntry{self.ntry}_{self.status}.txt"
        np.savetxt(fname, self.get_npl_arr())

        return


def test():
    npl = Numberplace(N=3)
    npl.print()
    npl.print(npl.get_ncandflag_arr())
    npl.print(npl.get_entropy_arr())
    npl.place_number((3,3), 3)
    npl.print()
    npl.print(npl.get_ncandflag_arr())
    npl.print(npl.get_entropy_arr())

if __name__=="__main__":
    test()

