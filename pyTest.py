import DisplacementMutation
import ExchangeMutation
import SimpleInversionMutation
import InsertionMutation
import InversionMutation
import ScrambleMutation
import AlternatingPositionCrossover
import CycleCrossover
import MaximalPreservativeCrossover
import OrderBasedCrossover
import OrderCrossover
import PartialMappingCrossover
import PositionBasedCrossover

mutationProbability = 1

population = [['1', '2', '3', '4', '5'], ['1', '2', '3', '4', '5'], ['5', '4', '3', '2', '1'],
              ['5', '4', '3', '2', '1']]

def testAlternatingPositionCrossoverReturnsValidSolution():
    validSolution = ['5', '4', '3', '2', '1']
    testPopulation = AlternatingPositionCrossover.alternatingPositionCrossover(population)
    assert len(testPopulation[0]) == len(validSolution) and set(testPopulation[1]) == set(validSolution)

def testCycleCrossoverReturnsValidSolution():
    validSolution = ['5', '4', '3', '2', '1']
    testPopulation = CycleCrossover.cycleCrossover(population)
    assert len(testPopulation[0]) == len(validSolution) and set(testPopulation[1]) == set(validSolution)

def testMaximalPreservativeCrossoverReturnsValidSolution():
    validSolution = ['5', '4', '3', '2', '1']
    testPopulation = MaximalPreservativeCrossover.maximalPreservativeCrossover(population)
    assert len(testPopulation[0]) == len(validSolution) and set(testPopulation[1]) == set(validSolution)

def testOrderBasedCrossoverReturnsValidSolution():
    validSolution = ['5', '4', '3', '2', '1']
    testPopulation = OrderBasedCrossover.orderBasedCrossover(population)
    assert len(testPopulation[0]) == len(validSolution) and set(testPopulation[1]) == set(validSolution)

def testOrderCrossoverReturnsValidSolution():
    validSolution = ['5', '4', '3', '2', '1']
    testPopulation = OrderCrossover.orderCrossover(population)
    assert len(testPopulation[0]) == len(validSolution) and set(testPopulation[1]) == set(validSolution)

def testPartialMappingCrossoverReturnsValidSolution():
    validSolution = ['5', '4', '3', '2', '1']
    testPopulation = PartialMappingCrossover.partiallyMappedCrossover(population)
    assert len(testPopulation[0]) == len(validSolution) and set(testPopulation[1]) == set(validSolution)

def testPositionBasedCrossoverReturnsValidSolution():
    validSolution = ['5', '4', '3', '2', '1']
    testPopulation = PositionBasedCrossover.positionBasedCrossover(population)
    assert len(testPopulation[0]) == len(validSolution) and set(testPopulation[1]) == set(validSolution)

def testDisplacementMutationReturnsValidSolution():
    validSolution = ['5', '4', '3', '2', '1']
    testPopulation = DisplacementMutation.displacementMutation(population, mutationProbability)
    assert len(testPopulation[0]) == len(validSolution) and set(testPopulation[1]) == set(validSolution)

def testExchangeMutationReturnsValidSolution():
    validSolution = ['5', '4', '3', '2', '1']
    testPopulation = ExchangeMutation.exchangeMutation(population, mutationProbability)
    assert len(testPopulation[0]) == len(validSolution) and set(testPopulation[1]) == set(validSolution)

def testSimpleInversionMutationReturnsValidSolution():
    validSolution = ['5', '4', '3', '2', '1']
    testPopulation = SimpleInversionMutation.simpleInversionMutation(population, mutationProbability)
    assert len(testPopulation[0]) == len(validSolution) and set(testPopulation[1]) == set(validSolution)

def testInversionMutationReturnsValidSolution():
    validSolution = ['5', '4', '3', '2', '1']
    testPopulation = InversionMutation.inversionMutation(population, mutationProbability)
    assert len(testPopulation[0]) == len(validSolution) and set(testPopulation[1]) == set(validSolution)

def testInsertionMutationReturnsValidSolution():
    validSolution = ['5', '4', '3', '2', '1']
    testPopulation = InsertionMutation.insertionMutation(population, mutationProbability)
    assert len(testPopulation[0]) == len(validSolution) and set(testPopulation[1]) == set(validSolution)

def testScrambleMutationReturnsValidSolution():
    validSolution = ['5', '4', '3', '2', '1']
    testPopulation = ScrambleMutation.scrambleMutation(population, mutationProbability)
    assert len(testPopulation[0]) == len(validSolution) and set(testPopulation[1]) == set(validSolution)