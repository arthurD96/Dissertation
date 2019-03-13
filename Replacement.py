import random
from operator import itemgetter


def generationalReplacement(population, children, generationalGapPercentage, returnPercentage):
    generationalGap = int((generationalGapPercentage / 100) * len(population))

    if generationalGap > len(children):
        generationalGap = len(children)

    sortedPopulation = sorted(population, key=itemgetter(1))
    sortedPopulation = sortedPopulation[:-generationalGap]

    sortedChildren = sorted(children, key=itemgetter(1))
    sortedChildren = sortedChildren[:generationalGap]

    sortedPopulation.extend(sortedChildren)
    sortedPopulation = sorted(sortedPopulation, key=itemgetter(1))

    returnNumber = int((returnPercentage / 100) * len(population))
    random.shuffle(sortedPopulation)
    newGeneration = sortedPopulation[:returnNumber]
    return newGeneration
