import random
from collections import deque


def orderCrossover(population):
    childPopulation = []
    for i in range(0, len(population), 2):
        try:
            parentOne = population[i]
            parentTwo = population[i + 1]
        except IndexError:
            parentOne = population[i]
            parentTwo = population[0]

        crossoverOne = random.randint(0, len(parentOne))
        crossoverTwo = random.randint(0, len(parentOne))

        while crossoverOne == crossoverTwo:
            crossoverTwo = random.randint(1, len(parentOne) - 1)

        if crossoverOne > crossoverTwo:
            crossoverOne, crossoverTwo = crossoverTwo, crossoverOne

        childOne = ([None] * crossoverOne) + parentOne[crossoverOne:crossoverTwo] + (
                [None] * (len(parentOne) - crossoverTwo))
        childTwo = ([None] * crossoverOne) + parentTwo[crossoverOne:crossoverTwo] + (
                [None] * (len(parentOne) - crossoverTwo))
        order = deque(list(range(len(parentOne))))
        order.rotate(-crossoverTwo)
        children = [childOne, childTwo]
        parents = [parentTwo, parentOne]
        for child in children:
            index = children.index(child)
            for i in range(len(order)):
                if None not in child:
                    childPopulation.append(child)
                    break
                else:
                    notPlaced = True
                    j = i
                    childIndex = order[j]
                    while notPlaced and j < len(order):
                        parentIndex = order[j]
                        if parents[index][parentIndex] not in child:
                            child[childIndex] = parents[index][parentIndex]
                            notPlaced = False
                        else:
                            j += 1
    return childPopulation

