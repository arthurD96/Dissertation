import pytest
import TournamentSelection
import RouletteSelection

populationWithFitness = [[['010', '100', '101', '001', '011'], 10], [['100', '011', '010', '001', '101'], 12],
                         [['101', '010', '001', '100', '011'], 14], [['011', '001', '101', '010', '100'], 16]]

population = [['010', '100', '101', '001', '011'], ['100', '011', '010', '001', '101'],
              ['101', '010', '001', '100', '011'], ['011', '001', '101', '010', '100']]


def testWinningPopulationSizeTournamentSelection():
    selectionPercentage = 50
    winningPopulationPercentage = 25
    testPopulation = TournamentSelection.tournamentSelection(populationWithFitness, selectionPercentage,
                                                             winningPopulationPercentage)
    assert len(testPopulation) == 1


def testBestPopulationReturnedTournamentSelection():
    selectionPercentage = 100
    winningPopulationPercentage = 25
    testPopulation = TournamentSelection.tournamentSelection(populationWithFitness, selectionPercentage,
                                                             winningPopulationPercentage)
    assert testPopulation[0] == ['010', '100', '101', '001', '011']


def testWinningPopulationSizeRouletteSelection():
    winninPopulationPercentage = 50
    testPopulation = RouletteSelection.rouletteSelection(populationWithFitness, winninPopulationPercentage)

    assert len(testPopulation) == 2


def testValidPopulationRouletteSelection():
    winninPopulationPercentage = 25
    testPopulation = RouletteSelection.rouletteSelection(populationWithFitness, winninPopulationPercentage)
    assert testPopulation[0] in population


def testValidPopulationTournamentSelection():
    winninPopulationPercentage = 50
    selectionPercentage = 50
    testPopulation = TournamentSelection.tournamentSelection(populationWithFitness,selectionPercentage ,winninPopulationPercentage)
    assert testPopulation[1] in population
