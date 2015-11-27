# uses a hbyrid of differential evolution to solve the graph coloring problem on a hard to color graph
from collections import defaultdict
import time
import random


graph = defaultdict(list)
for line in open("anna.txt"):
    # reads in graph as a dict where the nodes are keys and its edge connections are values (in a list)
    parts = line.split(" ")
    graph[int(parts[1])].append(int(parts[2]))


def getNumConflicts(solution):
    # return the number of unhappy edges for a given solution
    conflicts = 0
    for node in graph.keys():
        for connection in graph[node]:
            if solution.get(node) == solution.get(connection):
                conflicts += 1
    return conflicts


def mutate(child, colors):
    # mutate (i took the idea for this mutation from an online implementation of GA for graph coloring)
    conflicts = 0
    for node in graph.keys():
        for connection in graph[node]:
            if child[node] == child[connection]:
                child[node] = random.randint(0, colors)
    return child


def order(population):
    # order the solutions in the population from least number of conflicts to most number of conflicts
    smallest = 100
    ordered = list()
    hash = defaultdict(list)
    for i in range (0, len(population)):
        num = getNumConflicts(population[i])
        if num < smallest:
            smallest = num
        hash[num].append(population[i])
    for key in hash.keys():
        for each_pop in hash[key]:
            ordered.append(each_pop)
    return ordered


def choose(dec):
    rank = dec*10
    if rank>95:
        return 1
    else:
        chance = random.randint(0, 100)
        if chance>95:
            return 1
    return 0


def crossover(p1, p2):
    # to create new coloring to the left of the crossover point - p1 coloring, to the right - p2 coloring
    crossoverPoint = random.randint(0, len(p1.keys()))
    newColoring = dict()
    for node in p1.keys():
        if node < crossoverPoint:
            newColoring[node] = p1[node]
        else:
            newColoring[node] = p2[node]
    return newColoring


def nextGen(population, colors):
    # create next generation of solutions
    newPop = list()
    while (len(newPop) < len(population)):
        p1, p2 = -1, -1
        while p1 == -1 or p2 == -1:
            ind1, ind2 = random.sample(range(0, len(population)), 2)
            # the fewer the number of conflicts, the higher the chance each solution will be chosen to form
            # a next generation solution
            if (choose(len(population)-float(ind1)/len(population))) and (choose(len(population)-float(ind2)/len(population))):
                p1 = ind1
                p2 = ind2
        chance = random.randint(0, 100)
        parent1 = population[p1]
        parent2 = population[p2]
        if chance>95: # crossover probability
            child = crossover(parent1, parent2)
            child = mutate(child, colors)
            newPop.append(child)
        else:
            newPop.append(parent1)
            newPop.append(parent2)
    return newPop


def runGraphColoring(population, colors):
    population = order(population) # orders population from least to most number of unhappy edges
    newPopulation = nextGen(population, colors) # generates a new population
    return newPopulation # returned population


def getInitialPopulation(initialColors):
    # get random population
    # size of population should be experimented with
    population = list()
    for i in range(0,50):
        solution = dict()
        for key in graph.keys():
            color = random.randrange(0,initialColors)
            solution[key] = color
        population.append(solution)
    return population


start = time.time()
conf = 9999999
initialColors = 11
population = getInitialPopulation(initialColors)
conf = getNumConflicts(population[0])
while (conf>0):
    initialColors = 11
    newPopulation = runGraphColoring(population, initialColors)
    newPopulation = order(newPopulation) # orders new population from least to most # of unhappy edges
    newConf = getNumConflicts(newPopulation[0])
    population = newPopulation
    if newConf < conf: # for testing purposes
        conf = newConf
        print conf
    #if newConf == 0:
print population[0]
print time.time() - start










