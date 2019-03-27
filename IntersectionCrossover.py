import GenerateData
import random


def intersectionCrossover(population):
    childPopulation = []
    numberOfCities = len(population[0])
    for i in range(0, len(population), 2):
        try:
            parentOne = population[i]
            parentTwo = population[i + 1]
        except IndexError:
            parentOne = population[i]
            parentTwo = population[0]
        parentsZip = zip(parentOne, parentTwo)
        child = []
        for item in list(parentsZip):
            if item[0] == item[1]:
                child.append(item[0])
            else:
                child.append([None] * len(item[0]))
        tourChild = GenerateData.convertMatrixToTour(child)
        completeTour = random.sample(range(1, numberOfCities + 1), numberOfCities)
        for city in completeTour:
            if city not in tourChild:
                index = tourChild.index(None)
                tourChild[index] = city
        matrixChild = GenerateData.convertTourToMatrix(tourChild)
        childPopulation.append(matrixChild)
    return childPopulation

