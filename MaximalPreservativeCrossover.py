import random


def maximalPreservativeCrossover(population):
    childPopulation = []
    for i in range(0, len(population), 2):
        try:
            parentOne = population[i]
            parentTwo = population[i + 1]
        except IndexError:
            parentOne = population[i]
            parentTwo = population[0]

        if len(parentOne) < 10:
            crossoverOne = random.randint(0, len(parentOne) - 1)
            crossoverTwo = random.randint(crossoverOne + 1, len(parentOne))
        else:
            crossoverOne = random.randint(0, len(parentOne) - 10)
            crossoverTwo = random.randint(crossoverOne + 1, len(parentOne))
            if crossoverTwo - crossoverOne < 10:
                crossoverTwo = crossoverOne + 10
            elif crossoverTwo - crossoverOne > len(parentOne) / 2:
                crossoverTwo = crossoverOne + (len(parentOne) / 2)

        childOne = ([None] * crossoverOne) + parentTwo[crossoverOne:crossoverTwo] + (
                [None] * (len(parentOne) - crossoverTwo))
        childTwo = ([None] * crossoverOne) + parentOne[crossoverOne:crossoverTwo] + (
                [None] * (len(parentOne) - crossoverTwo))

        children = [childOne, childTwo]
        parents = [parentOne, parentTwo]
        for j in range(len(children)):
            child = children[j]
            parent = parents[j]
            for city in parent:
                if city not in child:
                    index = child.index(None)
                    child[index] = city
        childPopulation.append(childOne)
        childPopulation.append(childTwo)
    return childPopulation
