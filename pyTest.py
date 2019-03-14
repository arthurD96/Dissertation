import DisplacementMutation
import ExchangeMutation
import SimpleInversionMutation
import InsertionMutation
import InversionMutation
import ScrambleMutation

mutationProbability = 1

population = [['1', '2', '3', '4', '5'], ['1', '2', '3', '4', '5'], ['5', '4', '3', '2', '1'],
              ['5', '4', '3', '2', '1']]


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