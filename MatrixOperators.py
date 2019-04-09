import random
import sys
import PathOperators


def convertTourToMatrix(tour):
    solution = []
    numberOfCities = len(tour)
    for i in range(1, numberOfCities + 1):
        row = []
        for j in range(1, numberOfCities + 1):
            indexI = tour.index(i)
            indexJ = tour.index(j)
            if indexI < indexJ:
                row.append(1)
            else:
                row.append(0)
        solution.append(row)
    return solution


def convertMatrixToTour(tour):
    solution = [None] * len(tour)
    for i, row in enumerate(tour):
        count = 0
        if row[0] is None:
            continue
        else:
            for allele in row:
                if allele == 1:
                    count += 1
                else:
                    continue
            index = len(tour) - count - 1
            solution[index] = i + 1
    return solution


def intersectionCrossover(numberOfCities, parentOne, parentTwo):
    parentsZip = zip(parentOne, parentTwo)
    child = []
    for item in list(parentsZip):
        if item[0] == item[1]:
            child.append(item[0])
        else:
            child.append([None] * len(item[0]))
    tourChild = convertMatrixToTour(child)
    completeTour = random.sample(range(1, numberOfCities + 1), numberOfCities)
    for city in completeTour:
        if city not in tourChild:
            index = tourChild.index(None)
            tourChild[index] = city
    matrixChild = convertTourToMatrix(tourChild)
    return matrixChild


def unionCrossover(numberOfCities, parentOne, parentTwo):
    subLength = int(numberOfCities / 2)
    child = parentOne.copy()
    for i in range(numberOfCities):
        for j in range(numberOfCities):
            if i < subLength and j < subLength:
                child[i][j] = parentOne[i][j]
            elif i >= subLength and j >= subLength:
                child[i][j] = parentTwo[i][j]
            elif i < subLength:
                child[i][j] = 1
            else:
                child[i][j] = 0
    return child


crossovers = {'Intersection': intersectionCrossover, 'Union': unionCrossover}


def runCrossover(crossover, population):
    childPopulation = []
    numberOfCities = len(population[0])
    crossoverFunction = crossovers.get(crossover)
    if crossoverFunction:
        for i in range(0, len(population), 2):
            try:
                parentOne = population[i]
                parentTwo = population[i + 1]
            except IndexError:
                parentOne = population[i]
                parentTwo = population[0]
            child = crossoverFunction(numberOfCities, parentOne, parentTwo)
            childPopulation.append(child)
    else:
        print(str(crossover) + ' is not a valid Matrix crossover')
        sys.exit()
    return childPopulation


def runMutation(mutation, population, mutationProbability):
    populationPath = []
    for tour in population:
        tourPath = convertMatrixToTour(tour)
        populationPath.append(tourPath)
    childPopulationPath = PathOperators.runMutation(mutation, populationPath, mutationProbability)
    for i, tour in enumerate(childPopulationPath):
        population[i] = convertTourToMatrix(tour)
    return population
