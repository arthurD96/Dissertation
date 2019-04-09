import random
import math
import numpy as np


def tournamentSelection(population, selectionPercentage, winningPopulationPercentage):
    winningPopulation = []

    winningPopulationFloat = float(winningPopulationPercentage) / 100
    winningPopulationSize = winningPopulationFloat * float(len(population))

    percentageFloat = float(selectionPercentage) / 100
    tournamentSize = percentageFloat * float(len(population))
    populationArray = np.array(population)
    for i in range(0, int(winningPopulationSize)):
        selectedCompetitors = populationArray[np.random.choice(len(population), math.ceil(tournamentSize))]
        bestCandidate = min(selectedCompetitors, key=lambda x: x[1])
        winningPopulation.append(bestCandidate[0])
    return winningPopulation


def rouletteSelection(population, winningPopulationPercentage):
    winningPopulation = []
    populationWithCumulativeFitness = []
    selectedCompetitors = []
    cumulativeFitness = 0
    totalFitness = 0

    for solution in population:
        totalFitness += solution[1]

    for solution in population:
        minimisation = (1 - (solution[1] / totalFitness)) / (len(population) - 1)
        cumulativeFitness += minimisation
        solutionWithCumulativeFitness = [solution[0], cumulativeFitness]
        populationWithCumulativeFitness.append(solutionWithCumulativeFitness)

    winningPopulationFloat = float(winningPopulationPercentage) / 100
    winningPopulationSize = int(winningPopulationFloat * float(len(population)))

    for i in range(winningPopulationSize):
        selectedCompetitors.append(random.random())
        selectedCompetitors.sort()

    competitorNumber = 0
    solutionNumber = 0
    while competitorNumber != len(selectedCompetitors):

        if selectedCompetitors[competitorNumber] < populationWithCumulativeFitness[solutionNumber][1]:
            winningPopulation.append(populationWithCumulativeFitness[solutionNumber][0])
            competitorNumber += 1
        else:

            solutionNumber += 1
    return winningPopulation
