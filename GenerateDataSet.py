import random
import sys
import MatrixOperators


def generatePopulation(representation, tourSize, populationSize):
    if representation == 'Binary':
        population = generatePopulationBinary(tourSize, populationSize)
        return population
    elif representation == 'Path':
        population = generatePopulationPath(tourSize, populationSize)
        return population
    elif representation == 'Matrix':
        population = generatePopulationMatrix(tourSize, populationSize)
        return population
    else:
        print(representation + ' is not a valid representation')
        sys.exit()


def generatePopulationBinary(tourSize, populationSize):
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


def generatePopulationPath(tourSize, populationSize):
    population = []

    for i in range(0, populationSize):
        tour = random.sample(range(1, tourSize + 1), tourSize)
        population.append(tour)

    return population


def generatePopulationMatrix(tourSize, populationSize):
    population = []
    for i in range(populationSize):
        tour = random.sample(range(1, tourSize + 1), tourSize)
        solution = MatrixOperators.convertTourToMatrix(tour)
        population.append(solution)
    return population

