import random


def generatePopulationBinary(tourSize, populationSize):
    population = []
    binaryLength = len("{0:b}".format(tourSize))
    for i in range(populationSize):
        tour = []
        for j in range(1, tourSize + 1):
            city = bin(j)[2:].zfill(binaryLength)
            tour.append(city)
        random.shuffle(tour)
        tour.append(tour[0])
        population.append(tour)

    return population


def generatePopulationPath(tourSize, populationSize):
    population = []

    for i in range(0, populationSize):
        tour = random.sample(range(1, tourSize + 1), tourSize)
        tour.append(tour[0])
        population.append(tour)

    return population
