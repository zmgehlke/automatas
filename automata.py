import numpy as np



class Automata(object):
    @staticmethod
    def GAME_OF_LIFE(patch):
        # TODO: This can't be efficient, lol.
        #       Deal with memory ordering and actual stride patterns.
        neighbors = patch[0,0] + patch[0,1] + patch[0,2] + \
                    patch[1,0] + patch[1,2] + \
                    patch[2,0] + patch[2,1] + patch[2,2]
                    
        if patch[1,1]:
            if neighbors < 2:
                return 0
            if neighbors > 3:
                return 0
            else:
                return 1
        else:
            if 3 == neighbors:
                return 1
        return 0


    # TODO: Look into dtypes that have a smaller memory footprint.
    #       Alternatively, look into using uints as bit vectors.
    def __init__(self, shape):
        self.shape = tuple(list(shape))
        self._data = np.zeros(shape=self.shape, dtype=int)
        
        self._update = Automata.GAME_OF_LIFE    
        return
        
    def boundary(self):
        return self._data[0]
    
    # TODO: This is like the poster child of parallel processing, right?    
    def run(self):
        # Subtract 1 to not try to update the future from the last time step.
        for i in range(self.shape[0] -1):
            # Never update the edge so 1 to -1.
            # Hacky -- solves edge conditions by creating them, lulz.
            for x1 in range(1, self.shape[1] -1):
                for x2 in range(1, self.shape[2] -1):
                    # The +2 is because you need to specify a range of 4 to get 3 elements. Yay Python!
                    patch = self._data[i, (x1-1):(x1+2), (x2-1):(x2+2)]
                    self._data[i+1, x1, x2] = self._update(patch)
        return
