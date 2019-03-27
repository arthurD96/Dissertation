import pytest
import IntersectionCrossover
import GenerateData
import UnionCrossover

tour = [2, 3, 1, 4]
matrix = [[0, 0, 0, 1], [1, 0, 1, 1], [1, 0, 0, 1], [0, 0, 0, 0]]
population = [[[0, 0, 0, 1], [1, 0, 1, 1], [1, 0, 0, 1], [0, 0, 0, 0]],
              [[0, 0, 1, 1], [1, 0, 1, 1], [0, 0, 0, 0], [0, 0, 1, 0]]]


def testGenerateDataReturnsPopulationSize():
    numberOfCities = 10
    populationSize = 7
    population = GenerateData.generatePopulationMatrix(numberOfCities, populationSize)
    assert len(population) == 7


def testGenerateDataReturnsSolutionSize():
    numberOfCities = 10
    populationSize = 7
    population = GenerateData.generatePopulationMatrix(numberOfCities, populationSize)
    assert len(population[0]) == 10


def testConvertMatrixToTourReturnsCorrectTour():
    testTour = GenerateData.convertMatrixToTour(matrix)
    assert testTour == tour


def testConvertTourToMatrixReturnsCorrectMatrix():
    testMatrix = GenerateData.convertTourToMatrix(tour)
    assert testMatrix == matrix


def testIntersectionCrossoverReturnsValidSolutionLength():
    validSolution = [[0, 0, 0, 1], [1, 0, 1, 1], [1, 0, 0, 1], [0, 0, 0, 0]]
    testPopulation = IntersectionCrossover.intersectionCrossover(population)
    assert len(testPopulation[0]) == len(validSolution)

def testIntersectionCrossoverReturnsValidSolution():
    testPopulation = IntersectionCrossover.intersectionCrossover(population)
    count = 0
    numberOfCities = 4
    sumOfOnes = (numberOfCities*(numberOfCities-1))/2
    for row in testPopulation[0]:
        for item in row:
            if item == 1:
                count += 1
    assert count == sumOfOnes

def testUnionCrossoverReturnsValidSolutionLength():
    validSolution = [[0, 0, 0, 1], [1, 0, 1, 1], [1, 0, 0, 1], [0, 0, 0, 0]]
    testPopulation = UnionCrossover.unionCrossover(population)
    assert len(testPopulation[0]) == len(validSolution)

def testUnionCrossoverReturnsValidSolution():
    testPopulation = UnionCrossover.unionCrossover(population)
    count = 0
    numberOfCities = 4
    sumOfOnes = (numberOfCities*(numberOfCities-1))/2
    for row in testPopulation[0]:
        for item in row:
            if item == 1:
                count += 1
    assert count == sumOfOnes