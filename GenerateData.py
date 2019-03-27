import random


def generatePopulationMatrix(numberOfCities, populationSize):
    population = []
    for i in range(populationSize):
        tour = random.sample(range(1, numberOfCities + 1), numberOfCities)
        solution = convertTourToMatrix(tour)
        population.append(solution)
    return population


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


def convertMatrixToTour(solution):
    tour = [None] * len(solution)
    for i, row in enumerate(solution):
        count = 0
        if row[0] is None:
            continue
        else:
            for allele in row:
                if allele == 1:
                    count += 1
                else:
                    continue
            index = len(solution) - count - 1
            tour[index] = i + 1
    return tour
