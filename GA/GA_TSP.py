from TSP_Graph import TSP_Graph
import numpy as np
from Tour import Tour
from collections import defaultdict
import sys
import random
from numpy.core.fromnumeric import nonzero

class GA_TSP:
    
    #object to hold graph
    graph = TSP_Graph("",0)
    
    #size of the population
    npop = 0
    
    #max number of generation
    max_g = 100;
    
    #current population
    pop = []
    
    #mating pool
    mating_pool = []
    
    #store the average cost of each generation
    average_cost = []
    
    #min cost of each generation
    min_cost = []
    
    modified_pop_cost = 0
    
    best_tour = Tour()
       
    def __init__(self, filename):
        self.graph = TSP_Graph(filename, 15)
        self.graph._read_data()
        self.npop = self.graph.vcount * 2
        
        
    def _create_init_pop(self):
        var = []
        for i in range(0,self.npop):
            temp_tour = Tour()
            temp = np.random.permutation(self.graph.vcount)
            temp_tour.tour = temp
            temp_tour.tour_cost = self.graph._get_tour_cost(temp_tour.tour)
            var.append(temp_tour)
        self.pop =var;
        self._modify_costs()
        self._sort_tours(self.pop)
       
    def _sort_tours(self, pop):
        self.pop = sorted(pop, key=lambda x: x.tour_cost)
    
    def _modify_costs(self):
        sum_cost = 0;
        min_cost = sys.maxint
        self.modified_pop_cost = 0
        for i in range(0,self.npop):
            sum_cost = sum_cost + self.pop[i].tour_cost
            if(min_cost > self.pop[i].tour_cost):
                min_cost = self.pop[i].tour_cost
                self.best_tour = self.pop[i]
                
        for i in range(0,self.npop):
            self.pop[i].tour_cost = sum_cost - self.pop[i].tour_cost
            self.modified_pop_cost = self.modified_pop_cost + self.pop[i].tour_cost
        
        self.average_cost.append(sum_cost/self.npop)
        self.min_cost.append(min_cost)
        
        
    def _create_mating_pool(self):
        
        for i in range(self.npop):
            rand = np.random.randint(0, self.modified_pop_cost + 1)
            for t in self.pop :
                rand = rand - t.tour_cost
                if(rand <= 0):
                    self.mating_pool.append(t)
                    break
        #print("printing pop")        
        #self._print_pool(self.pop)
        #print("print mate pop")
        #self._print_pool(self.mating_pool)        
            
    def _get_next_gen(self):
        
        self._create_mating_pool()
        new_pop = []
        temp = self.npop/2
        for i in range(0,temp):
            a,b = np.random.randint(0, self.npop, 2)
            #print(i,a,b)
            child1 = self._get_child(self.mating_pool[a], self.mating_pool[b] )
            child2 = self._get_child(self.mating_pool[b], self.mating_pool[a] )
            new_pop.append(child1)
            new_pop.append(child2)
        self.pop = new_pop
        self._modify_costs()
        self._sort_tours(self.pop)
        self.mating_pool = []
    
    def _get_child(self, p1,p2):
        child = self._mate_parents(p1,p2)
        return child
    
    def _mate_parents(self,p1,p2):
        size = self.graph.vcount
        
        child_tour = np.zeros(self.graph.vcount) + p2.tour
        while(1) :
            a = np.random.randint(0, size, 2)
            if(a[0]!=a[1]):
                temp = min(a[0],a[1])
                a[1] = a[0]+a[1] - temp
                a[0] = temp
                break;
        index_list = []
        for i in range(a[0],a[1] + 1):
            temp = nonzero(p2.tour == p1.tour[i] )
            index_list.append(temp[0][0])
            
        index_list.sort()
        for i in range(index_list.__len__()):
            temp = a[0] + i
            child_tour[index_list[i]] = p1.tour[temp]
        
        child = Tour()
        child.tour = child_tour
        child.tour_cost = self.graph._get_tour_cost(child_tour)    
        return child    
    
    
    def _run(self):
        self._create_init_pop();
        for i in range(0,self.max_g):
            #print(self.npop,self.pop.__len__(),self.mating_pool.__len__())
            
            self._get_next_gen()
            print("generation " , i )
            
        return self.best_tour    
            
    def _print_pool(self, pool):
        for t in pool:
            print(t.tour.tolist(), t.tour_cost)        
np.random.seed(1)            
g = GA_TSP("15-cities")
ans = g._run()
print("ans-")
print(ans.tour)

print("avg")
print(g.average_cost)

print("min_cost")
print(g.min_cost)