from operator import itemgetter


def selectNextGeneration(mutatedPopulation, parentPopulation):
    bestSolutions = []
    populationSize = len(mutatedPopulation)
    parentPopulation.extend(mutatedPopulation)
    sortedPopulation = sorted(parentPopulation, key=itemgetter(1))
    for i in range(0, populationSize):
        bestSolutions.append(sortedPopulation[i])
    return bestSolutions
