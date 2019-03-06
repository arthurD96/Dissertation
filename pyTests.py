import ClassicalCrossoverBinary
import ClassicalMutationBinary
import RepairBinary
import pytest

population = [['010', '100', '101', '001', '011'], ['100', '011', '010', '001', '101'],
              ['101', '010', '001', '100', '011'], ['011', '001', '101', '010', '100']]


def testClassicalCrossoverPopulationSize():
    testPopulation = ClassicalCrossoverBinary.runCrossover(population)
    assert len(testPopulation) == len(population)


def testClassicalCrossoverSolutionSize():
    testPopulation = ClassicalCrossoverBinary.runCrossover(population)
    assert len(testPopulation[0]) == len(population[0])


def testClassicalCrossoverAlleleSize():
    testPopulation = ClassicalCrossoverBinary.runCrossover(population)
    assert len(testPopulation[0][0]) == len(population[0][0])


def testClassicalMutationBinaryMutationRateOne():
    mutationProbability = 1
    testPopulation = ClassicalMutationBinary.runMutation(population, mutationProbability)
    assert testPopulation == [['101', '011', '010', '110', '100'], ['011', '100', '101', '110', '010'],
                              ['010', '101', '110', '011', '100'], ['100', '110', '010', '101', '011']]


def testClasscicalMutationBinaryMutationRateZero():
    mutationProbability = 0
    testPopulation = ClassicalMutationBinary.runMutation(population, mutationProbability)
    assert testPopulation == [['010', '100', '101', '001', '011'], ['100', '011', '010', '001', '101'],
                              ['101', '010', '001', '100', '011'], ['011', '001', '101', '010', '100']]


def testRepairBinaryOnValidSolution():
    testPopulation = RepairBinary.runRepair(population)
    assert testPopulation == population


def testRepairBinaryOnNonValidSolution():
    invalidPopulation = [['001', '010', '000', '011', '101']]
    testPopulation = RepairBinary.runRepair(invalidPopulation)
    correctPopulation = [['001', '010', '011', '101', '100']]
    assert testPopulation == correctPopulation
