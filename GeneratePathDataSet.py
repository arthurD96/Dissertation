import random

def generatePopulation(tourSize, populationSize):
    population = []

    for i in range(0, populationSize):
        tour = random.sample(range(1, tourSize+1), tourSize)
        population.append(tour)

    return population




