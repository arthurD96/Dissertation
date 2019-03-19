import random


def positionBasedCrossover(population):
    childPopulation = []
    for i in range(0, len(population), 2):
        try:
            parentOne = population[i]
            parentTwo = population[i + 1]
        except IndexError:
            parentOne = population[i]
            parentTwo = population[0]
        indexes = list(range(0, len(parentOne)))
        numberOfIndexes = random.randint(0, len(parentOne))
        indexes = random.sample(indexes, numberOfIndexes)
        childOne = [None] * len(parentOne)
        childTwo = [None] * len(parentTwo)
        parents = [parentOne, parentTwo]
        children = [childOne, childTwo]
        for index in indexes:
            childOne[index] = parentTwo[index]
            childTwo[index] = parentOne[index]
        for counter in range(2):
            for city in parents[counter]:
                if city not in children[counter]:
                    index = children[counter].index(None)
                    children[counter][index] = city
        childPopulation.append(childOne)
        childPopulation.append(childTwo)
    return childPopulation



