from TSP_Graph import TSP_Graph
import numpy as np
from Tour import Tour
import sys
import random
import matplotlib as plt

class GA_TSP:
    
    #object to hold graph
    graph = TSP_Graph("",0)
    
    #size of the population
    npop = 0
    
    #max number of generation
    max_g = 200;
    
    #current population
    pop = []
    
    #store the average cost of each generation
    average_cost = []
    
    #min cost of each generation
    min_cost = []
    
    modified_pop_cost = 0
    
    best_tour = Tour()
    
    tournament_size = 6
    
    elitist = 1
       
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
        self._analyse_costs()
        self._sort_tours(self.pop)
#         self._print_pool(self.pop)
       
    def _sort_tours(self, pop):
        self.pop = sorted(pop, key=lambda x: x.tour_cost)
    
    def _analyse_costs(self):
        sum_cost = 0;
        min_cost = sys.maxint
        for i in range(0,self.npop):
            sum_cost = sum_cost + self.pop[i].tour_cost
            if(min_cost > self.pop[i].tour_cost):
                min_cost = self.pop[i].tour_cost
                self.best_tour = self.pop[i]
                 
        self.average_cost.append(sum_cost/self.npop)
        self.min_cost.append(min_cost)
         
        
#     def _create_mating_pool(self):
#          
#         for i in range(self.npop):
#             rand = np.random.randint(0, self.modified_pop_cost + 1)
#             for t in self.pop :
#                 rand = rand - t.tour_cost
#                 if(rand <= 0):
#                     self.mating_pool.append(t)
#                     break
        #print("printing pop")        
        #self._print_pool(self.pop)
        #print("print mate pop")
        #self._print_pool(self.mating_pool)        
            
    def _get_next_gen(self):
        
        new_pop = []
        for i in range(0,self.npop - self.elitist):
            p1 = self._get_parent()
            p2 = self._get_parent()
            child = self._get_child(p1, p2)
            child.tour_cost = self.graph._get_tour_cost(child.tour)
            child = self._mutate(child)
            new_pop.append(child)
            
        if(self.elitist):
            new_pop.append(self.pop[0])
        
        self.pop = new_pop
        self._analyse_costs()
        self._sort_tours(self.pop)
#         self._print_pool(self.pop)
        
    def _get_parent(self):
        players = np.random.randint(0,self.graph.vcount - 1, self.tournament_size)
        best_tour = -1
        for i in players:
            if(best_tour == -1):
                best_tour = self.pop[i]
            else:
                if(best_tour.tour_cost > self.pop[i].tour_cost):
                    best_tour = self.pop[i]
        return best_tour
                    
            
    
    def _get_child(self, p1,p2):
        child = self._mate_parents(p1,p2)
        return child
    
    def _mate_parents(self,p1,p2):
        size = self.graph.vcount
        
        child_tour = -1 * np.ones(self.graph.vcount)
        while(1) :
            a = np.random.randint(0, size, 2)
            if(a[0]!=a[1]):
                temp = min(a[0],a[1])
                a[1] = a[0]+a[1] - temp
                a[0] = temp
                break;
        for i in range(a[0],a[1] + 1):
            child_tour[i] = p1.tour[i]
        
        p2_pos = 0
        for i in range(0,self.graph.vcount):
            if(child_tour[i] == -1):
                while(p2.tour[p2_pos] in child_tour):
                    p2_pos += 1
                child_tour[i] = p2.tour[p2_pos]    
        
        
        child = Tour()
        child.tour = child_tour
        child.tour_cost = self.graph._get_tour_cost(child_tour)    
        return child
    
    def _mutate(self,t):
        a = np.random.randint(0, self.graph.vcount, 2)
        temp = t.tour[a[0]]
        t.tour[a[0]] = t.tour[a[1]]
        t.tour[a[1]] = temp
        return t   
    
    
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

true_opt = np.asarray([1,13, 2,15, 9, 5, 7, 3,12,14,10, 8, 6, 4,11]) - 1
true_cost = g.graph._get_tour_cost(true_opt)
print(true_cost,true_opt)

