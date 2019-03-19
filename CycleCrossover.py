import random


def cycleCrossover(population):
    childPopulation = []
    for i in range(0, len(population), 2):
        try:
            parentOne = population[i]
            parentTwo = population[i + 1]
        except IndexError:
            parentOne = population[i]
            parentTwo = population[0]
        relationMap = dict(zip(parentOne, parentTwo))
        keys = list(relationMap.keys())
        childOne = [None] * len(parentOne)
        childTwo = [None] * len(parentTwo)
        count = 0
        while keys:

            start = keys[0]
            current = relationMap[start]
            cycle = []
            while current not in cycle:
                cycle.append(current)
                current = relationMap[current]
                keys.remove(current)
            for item in cycle:
                index = population[count].index(item)
                childOne[index] = item
                if count == 0:
                    index = population[1].index(item)
                    childTwo[index] = item
                else:
                    index = population[0].index(item)
                    childTwo[index] = item
            if count == 0:
                count = 1
            else:
                count = 0
        childPopulation.append(childOne)
        childPopulation.append(childTwo)
    return childPopulation
