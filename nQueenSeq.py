import numpy as np
import sys
import random

nQueens = 8
#POPULATION = int(sys.argv[1])
#MUTATE = float(sys.argv[2])
POPULATION = 1000
MUTATE = .001


maxFitness = (nQueens * (nQueens - 1))//2
maxFitnessFound = False

class QueenPosition:
	def __init__(self):
		self.sequence = None
		self.fitness = 0
	def setSequence(self, val):
		self.sequence = val
	def setFitness(self, fitness):
		self.fitness = fitness
	def getAttr(self):
		return {'sequence':sequence, 'fitness':fitness}

def fitness(chromosome = None):
	clashes = 0;
	row_col_clashes = abs(nQueens - len(np.unique(chromosome)))
	clashes += row_col_clashes

	for i in range(nQueens):
		for j in range(nQueens):
			if ( i != j):
				dx = abs(i-j)
				dy = abs(chromosome[i] - chromosome[j])
				if(dx == dy):
					clashes += 1
	return maxFitness - clashes	


def generateChromosome():
	init_generation = np.random.permutation(nQueens)
	return init_generation

def generatePopulation(population_size = 100):
    global maxFitnessFound
    POPULATION = population_size
    population = [QueenPosition() for i in range(population_size)]
    for i in range(population_size):
        population[i].setSequence(generateChromosome())
        population[i].setFitness(fitness(population[i].sequence))
        if population[i].fitness == maxFitness:
            maxFitnessFound = True
            return population
    return population

def getParent(avgFitness):
    parent1, parent2 = None, None
    while True:
        parent = [x for x in population if x.fitness >= avgFitness]
        p1 = np.random.randint(len(parent))
        parent1 = parent[p1]
        p2 = np.random.randint(len(parent))
        parent2 = parent[p2]
        while parent1 == parent2:
            p2 = np.random.randint(len(parent))
            parent2 = parent[p2]    
        return parent1, parent2

def crossover(parent1, parent2):
    c = random.randint(0, nQueens-1)
    child = QueenPosition()
    child.sequence = []
    p1s = np.array(parent1.sequence)
    child.sequence.extend(parent1.sequence[0:c])
    child.sequence.extend(parent2.sequence[c:])
    return child

def mutate(child):
	c = np.random.randint(nQueens)
	child.sequence[c] = np.random.randint(nQueens)
	return child

def geneticAlgo(avgFitness):
    global maxFitnessFound
    newpopulation = []
    for i in range(len(population)):
        parent1, parent2 = getParent(avgFitness)
        child = crossover(parent1, parent2)
        uniqueGene = len(np.unique(child.sequence))
        if uniqueGene < nQueens and (uniqueGene/(nQueens * 100)) < MUTATE:
            child = mutate(child)
        child.setFitness(fitness(child.sequence))
        newpopulation.append(child)
        if child.fitness == maxFitness:
            maxFitnessFound = True
            return newpopulation
            break
    return newpopulation

if __name__ == "__main__":
    iteration = 0
    population = generatePopulation(POPULATION)
    while maxFitnessFound == False:
        avgFitness = np.mean([x.fitness for x in population])
        iteration +=1
        population = geneticAlgo(avgFitness)   
    
    for each in population:
        if each.fitness == maxFitness:
            print (each.sequence)
            break