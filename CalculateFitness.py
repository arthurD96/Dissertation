import math


def calculateFitnessBinary(population, cityCords):
    populationWithFitness = []
    for solution in population:
        solution.append(solution[0])
        fitness = 0
        for i in range(1, len(solution)):
            cityTo = int(solution[i], 2)
            cityFrom = int(solution[i - 1], 2)
            distanceX = abs(cityCords[cityTo - 1][0] - cityCords[cityFrom - 1][0])
            distanceY = abs(cityCords[cityTo - 1][1] - cityCords[cityFrom - 1][1])
            fitness += math.sqrt((distanceX ** 2) + (distanceY ** 2))
        del solution[-1]
        populationWithFitness.append([solution, fitness])
    return populationWithFitness


def calculateFitnessPath(population, cityCords):
    populationWithFitness = []
    for solution in population:
        solution.append(solution[0])
        fitness = 0
        for i in range(1, len(solution)):
            cityTo = int(solution[i])
            cityFrom = int(solution[i - 1])
            distanceX = abs(cityCords[cityTo - 1][0] - cityCords[cityFrom - 1][0])
            distanceY = abs(cityCords[cityTo - 1][1] - cityCords[cityFrom - 1][1])
            fitness += math.sqrt((distanceX ** 2) + (distanceY ** 2))
        del solution[-1]
        populationWithFitness.append([solution, fitness])
    return populationWithFitness
