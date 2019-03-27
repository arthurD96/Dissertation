import BinaryOperators
import Selection
import Replacement
import MatrixOperators
import GenerateDataSet

populationBinary = [['010', '100', '101', '001', '011'], ['100', '011', '010', '001', '101'],
                    ['101', '010', '001', '100', '011'], ['011', '001', '101', '010', '100']]

populationWithFitnessBinary = [[['010', '100', '101', '001', '011'], 10], [['100', '011', '010', '001', '101'], 12],
                               [['101', '010', '001', '100', '011'], 14], [['011', '001', '101', '010', '100'], 16]]

childrenWithFitnessBinary = [[['111', '100', '101', '001', '011'], 8], [['000', '001', '101', '010', '100'], 9]]

tour = [2, 3, 1, 4]

matrix = [[0, 0, 0, 1], [1, 0, 1, 1], [1, 0, 0, 1], [0, 0, 0, 0]]

populationMatrix = [[[0, 0, 0, 1], [1, 0, 1, 1], [1, 0, 0, 1], [0, 0, 0, 0]],
                    [[0, 0, 1, 1], [1, 0, 1, 1], [0, 0, 0, 0], [0, 0, 1, 0]]]


def testPopulationSizeReplacementReturn():
    testPopulation = Replacement.generationalReplacement(populationWithFitnessBinary, childrenWithFitnessBinary, 50, 75)
    assert len(testPopulation) == 3


def testParentInPopulationReplacement():
    testPopulation = Replacement.generationalReplacement(populationWithFitnessBinary, childrenWithFitnessBinary, 50,
                                                         100)
    assert [['010', '100', '101', '001', '011'], 10] in testPopulation


def testParentNotInPopulationReplacement():
    testPopulation = Replacement.generationalReplacement(populationWithFitnessBinary, childrenWithFitnessBinary, 50, 50)
    assert [['011', '001', '101', '010', '100'], 16] not in testPopulation


def testChildInPopulationReplacement():
    testPopulation = Replacement.generationalReplacement(populationWithFitnessBinary, childrenWithFitnessBinary, 50,
                                                         100)
    assert [['111', '100', '101', '001', '011'], 8] in testPopulation


# def testChildNotInPopulationReplacement():
#     testPopulation = Replacement.generationalReplacement(populationWithFitness, childrenWithFitness, 50, 50)
#     assert [['000', '001', '101', '010', '100'], 9] not in testPopulation


def testClassicalCrossoverPopulationSize():
    testPopulation = BinaryOperators.runCrossover('ClBi', populationBinary)
    assert len(testPopulation) == len(populationBinary)


def testClassicalCrossoverSolutionSize():
    testPopulation = BinaryOperators.runCrossover('ClBi', populationBinary)
    assert len(testPopulation[0]) == len(populationBinary[0])


def testClassicalCrossoverAlleleSize():
    testPopulation = BinaryOperators.runCrossover('ClBi', populationBinary)
    assert len(testPopulation[0][0]) == len(populationBinary[0][0])


def testClassicalMutationBinaryMutationRateOne():
    mutationProbability = 1
    testPopulation = BinaryOperators.runMutation('ClBi', populationBinary, mutationProbability)
    assert testPopulation == [['101', '011', '010', '110', '100'], ['011', '100', '101', '110', '010'],
                              ['010', '101', '110', '011', '100'], ['100', '110', '010', '101', '011']]


def testClasscicalMutationBinaryMutationRateZero():
    mutationProbability = 0
    testPopulation = BinaryOperators.runMutation('ClBi', populationBinary, mutationProbability)
    assert testPopulation == [['010', '100', '101', '001', '011'], ['100', '011', '010', '001', '101'],
                              ['101', '010', '001', '100', '011'], ['011', '001', '101', '010', '100']]


def testRepairBinaryOnValidSolution():
    testPopulation = BinaryOperators.runRepair(populationBinary)
    assert testPopulation == populationBinary


def testRepairBinaryOnNonValidSolution():
    invalidPopulation = [['001', '010', '000', '011', '101']]
    testPopulation = BinaryOperators.runRepair(invalidPopulation)
    correctPopulation = [['001', '010', '011', '101', '100']]
    assert testPopulation == correctPopulation


def testWinningPopulationSizeTournamentSelection():
    selectionPercentage = 50
    winningPopulationPercentage = 25
    testPopulation = Selection.tournamentSelection(populationWithFitnessBinary, selectionPercentage,
                                                   winningPopulationPercentage)
    assert len(testPopulation) == 1


def testBestPopulationReturnedTournamentSelection():
    selectionPercentage = 100
    winningPopulationPercentage = 25
    testPopulation = Selection.tournamentSelection(populationWithFitnessBinary, selectionPercentage,
                                                   winningPopulationPercentage)
    assert testPopulation[0] == ['010', '100', '101', '001', '011']


def testWinningPopulationSizeRouletteSelection():
    winninPopulationPercentage = 50
    testPopulation = Selection.rouletteSelection(populationWithFitnessBinary, winninPopulationPercentage)

    assert len(testPopulation) == 2


def testValidPopulationRouletteSelection():
    winninPopulationPercentage = 25
    testPopulation = Selection.rouletteSelection(populationWithFitnessBinary, winninPopulationPercentage)
    assert testPopulation[0] in populationBinary


def testValidPopulationTournamentSelection():
    winninPopulationPercentage = 50
    selectionPercentage = 50
    testPopulation = Selection.tournamentSelection(populationWithFitnessBinary, selectionPercentage,
                                                   winninPopulationPercentage)
    assert testPopulation[1] in populationBinary


def testGenerateDataReturnsPopulationSize():
    numberOfCities = 10
    populationSize = 7
    population = GenerateDataSet.generatePopulationMatrix(numberOfCities, populationSize)
    assert len(population) == 7


def testGenerateDataReturnsSolutionSize():
    numberOfCities = 10
    populationSize = 7
    population = GenerateDataSet.generatePopulationMatrix(numberOfCities, populationSize)
    assert len(population[0]) == 10


def testConvertMatrixToTourReturnsCorrectTour():
    testTour = MatrixOperators.convertMatrixToTour(matrix)
    assert testTour == tour


def testConvertTourToMatrixReturnsCorrectMatrix():
    testMatrix = MatrixOperators.convertTourToMatrix(tour)
    assert testMatrix == matrix


def testIntersectionCrossoverReturnsValidSolutionLength():
    validSolution = [[0, 0, 0, 1], [1, 0, 1, 1], [1, 0, 0, 1], [0, 0, 0, 0]]
    numberOfCities = 4
    testPopulation = MatrixOperators.intersectionCrossover(numberOfCities, populationMatrix[0], populationMatrix[1])
    assert len(testPopulation[0]) == len(validSolution)


def testIntersectionCrossoverReturnsValidSolution():
    numberOfCities = 4
    testPopulation = MatrixOperators.intersectionCrossover(numberOfCities, populationMatrix[0], populationMatrix[1])
    count = 0
    numberOfCities = 4
    sumOfOnes = (numberOfCities * (numberOfCities - 1)) / 2
    for row in testPopulation:
        for item in row:
            if item == 1:
                count += 1
    assert count == sumOfOnes


def testUnionCrossoverReturnsValidSolutionLength():
    numberOfCities = 4
    validSolution = [[0, 0, 0, 1], [1, 0, 1, 1], [1, 0, 0, 1], [0, 0, 0, 0]]
    testPopulation = MatrixOperators.unionCrossover(numberOfCities, populationMatrix[0], populationMatrix[1])
    assert len(testPopulation[0]) == len(validSolution)


def testUnionCrossoverReturnsValidSolution():
    numberOfCities = 4
    testPopulation = MatrixOperators.unionCrossover(numberOfCities, populationMatrix[0], populationMatrix[1])
    count = 0
    numberOfCities = 4
    sumOfOnes = (numberOfCities * (numberOfCities - 1)) / 2
    for row in testPopulation:
        for item in row:
            if item == 1:
                count += 1
    assert count == sumOfOnes
