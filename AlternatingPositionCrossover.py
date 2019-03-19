import random

def alternatingPositionCrossover(population):
    childPopulation = []
    for i in range(0, len(population), 2):
        try:
            parentOne = population[i]
            parentTwo = population[i + 1]
        except IndexError:
            parentOne = population[i]
            parentTwo = population[0]
        parentListOne = []
        parentListTwo = []
        for j in range(len(parentOne)):
            parentListOne.append(parentOne[j])
            parentListOne.append(parentTwo[j])
            parentListTwo.append(parentTwo[j])
            parentListTwo.append(parentOne[j])
        childOne = []
        childTwo = []
        for city in range(len(parentListOne)):
            if parentListOne[city] not in childOne:
                childOne.append(parentListOne[city])
            if parentListTwo[city] not in childTwo:
                childTwo.append(parentListTwo[city])
        childPopulation.append(childOne)
        childPopulation.append(childTwo)
    return childPopulation


