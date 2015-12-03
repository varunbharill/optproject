import numpy as np

class TSP_Graph:
    vcount = 0;
    graph_matrix = np.matrix([])
    fname = ""
    
    def __init__(self, fname, vcount):
        self.fname = fname
        self.vcount = vcount
        
    def _read_data(self):
        self.graph_matrix = np.matrix(np.loadtxt(self.fname, int))
            
    
    def _get_tour_cost(self, t):
        cost = 0;
        for c in range(0, t.size - 1):
            cost = cost + self.graph_matrix[t[c],t[c+1]]
#             print(t[c],t[c+1],self.graph_matrix[t[c],t[c+1]])
        cost  = cost + self.graph_matrix[t[0],t[t.size - 1]]
#         print(t[t.size - 1],t[0],self.graph_matrix[t[t.size - 1],t[0]])
        return cost;
            
        
            