import random


def tournamentSelection(population, selectionPercentage, winningPopulationPercentage):
    winningPopulation = []

    winningPopulationFloat = float(winningPopulationPercentage) / 100
    winningPopulationSize = winningPopulationFloat * float(len(population))

    percentageFloat = float(selectionPercentage) / 100
    tournamentSize = percentageFloat * float(len(population))

    for i in range(0, int(winningPopulationSize)):
        tournamentPool = []
        bestCandidate = [[], 0]
        selectedCompetitors = random.sample(range(len(population)), int(tournamentSize))
        for j in range(0, len(selectedCompetitors)):
            tournamentPool.append(population[selectedCompetitors[j]])
        for candidate in tournamentPool:
            if bestCandidate[1] == 0:
                bestCandidate = candidate
            elif candidate[1] < bestCandidate[1]:
                bestCandidate = candidate
        winningPopulation.append(bestCandidate[0])
    return winningPopulation
