import random


def insertionMutation(population, mutationProbability):
    for i in range(0, len(population)):
        if random.random() < mutationProbability:
            currentSolution = population[i]
            alleleToMove = random.randint(0, len(currentSolution) - 1)
            insertionPoint = random.randint(0, len(currentSolution) - 1)
            while alleleToMove == insertionPoint:
                insertionPoint = random.randint(0, len(currentSolution) - 1)
            removedCity = currentSolution[alleleToMove]
            del currentSolution[alleleToMove]
            currentSolution[insertionPoint:insertionPoint] = removedCity
            population[i] = currentSolution
    return population
