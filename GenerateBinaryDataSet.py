import random


def generatePopulation(tourSize, populationSize):
    population = []
    binaryLength = len("{0:b}".format(tourSize))
    for i in range(populationSize):
        tour = []
        for j in range(1, tourSize + 1):
            city = bin(j)[2:].zfill(binaryLength)
            tour.append(city)
        random.shuffle(tour)
        population.append(tour)
    return population


