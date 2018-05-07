import numpy as np

from numba import cuda

@cuda.jit
def GAME_OF_LIFE(current, next):

    x1, x2 = cuda.grid(2)
    
    x1 = x1 + 1
    x2 = x2 + 1
    
    n00 = current[x1-1, x2-1]
    n01 = current[x1-1, x2]
    n02 = current[x1-1, x2+1]
    n10 = current[x1, x2-1]
    n11 = current[x1, x2]
    n12 = current[x1, x2+1]
    n20 = current[x1+1, x2-1]
    n21 = current[x1+1, x2]
    n22 = current[x1+1, x2+1]
    

    n = n00 + n01 + n02 + n10 + n12 + n20 + n21 + n22
    a = n11
    
    # Uh... GPU magic. A.next := (N >= 2) AND (N <= 3) AND (N=3 OR A)
    #                            (N > 1) AND (4 > N) AND (N>2 OR A)
    c1 = min(1, max(0, n-1))
    c2 = min(1, max(0, 4-n))
    c3 = min(1, max(0, n-2) + a)      
    next[x1, x2] = min(1, c1 * c2 * c3)
    return

class Automata(object):
    def __init__(self, shape):
        self.shape = tuple(list(shape))
        self._data = np.zeros(shape=self.shape, dtype=np.uint8) 
        return
        
    def boundary(self):
        return self._data[0]
    
    def run(self):
        # Subtract 1 to not try to update the future from the last time step.
        for i in range(self.shape[0] -1):
            # Hacky -- solves edge conditions by creating them, lulz.
                                    #Buffer         # Zero
                                    #Adjustment     # Indexing
            width = self.shape[1]   - 2             - 1
            height = self.shape[2]  - 2             - 1
            
            threadsperblock = (8, 8)
            bheight = (height + threadsperblock[0]) // threadsperblock[0]
            bwidth = (width + threadsperblock[1]) // threadsperblock[1]
            blockspergrid   = (bheight, bwidth)

            GAME_OF_LIFE[blockspergrid, threadsperblock](self._data[i, :, :], self._data[i+1, :, :])
        return
