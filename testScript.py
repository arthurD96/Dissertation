import time
from operator import itemgetter
from tqdm import tqdm

import math
import sys
import csv

import MapGenerator
import GenerateDataSet
import CalculateFitness
import Selection
import BinaryOperators
import PathOperators
import Replacement
import Plotting

numberOfCities = 70
populationSize = 25000
childPopulationSizePercentage = 30
generationalGapPercentage = 20
mutationProbability = 0.01

'Representation Key: Bi = Binary, Pa = Path'

representation = 'Pa'
representations = {'Bi': BinaryOperators, 'Pa': PathOperators}

'Selection Key: To = Tournament, Ro = Roulette'

selectionType = 'Ro'
tournamentSize = 10
selectionParameters = {'Ro': None, 'To': tournamentSize}

'''
Crossover Key: 
Binary - (ClBi = Classical Binary)
Path - (MPPa = Maximal Preservative Path, PMPa = Partially Mapped Path, PBPa = Position Based Path, OrPa = Order Path,
OBPa = Order Based Path, APPa = Alternating Position Path, CyPa = Cycle Based Path)
'''

crossoverType = 'MPPa'

'''
Mutation Key: 
ClBi = Classical Binary 
DiPa = Displacement Path, ExPa = Exchange Path, IsPa = Insertion Path, IvPa = Inversion Path, ScPa = Scramble Path, 
SIPa = Simple Inversion Path
'''

mutationType = 'DiPa'

'Termination Key: It = Iteration, Re = Reduction, Co = Convergence'

terminationType = 'Co'
iterations = 100
convergenceNumber = 50
reductionPercentage = 99.99
terminationParameters = {'It': iterations, 'Re': reductionPercentage, 'Co': convergenceNumber}

fitnessFunction = {'Bi': CalculateFitness.calculateFitnessBinary, 'Pa': CalculateFitness.calculateFitnessPath}
cityCords = []


def main():
    global cityCords
    cityCords = MapGenerator.generateMap(numberOfCities)

    originalPopulation = GenerateDataSet.generatePopulation(representation, numberOfCities, populationSize)
    originalPopulationWithFitness = fitnessFunction[representation](originalPopulation, cityCords)
    originalSolution = findBestSolution(originalPopulationWithFitness)

    if terminationType == 'It':
        bestSolution = iterationTermination(originalPopulationWithFitness)
    elif terminationType == 'Re':
        bestSolution = reductionTermination(originalPopulationWithFitness)
    elif terminationType == 'Co':
        bestSolution = convergenceTermination(originalPopulationWithFitness)
    else:
        print(terminationType + ' is not a valid termination type')

    algorithmEfficiency = int((originalSolution[1] / bestSolution[1]) * 100) - 100
    print("New Solution is: " + str(algorithmEfficiency) + "% faster than the original fastest route")

    Plotting.plotMap(cityCords)
    Plotting.plotRoute(representation, originalSolution, cityCords)
    Plotting.plotRoute(representation, bestSolution, cityCords)
    addDataToCsv(originalSolution[0], bestSolution[0], algorithmEfficiency)


def iterationTermination(originalPopulationWithFitness):
    global reductionPercentage
    reductionPercentage = 100
    populationWithFitness = originalPopulationWithFitness
    for i in tqdm(range(iterations)):
        populationWithFitness = createNewGeneration(populationWithFitness)
    time.sleep(1)
    bestSolution = findBestSolution(populationWithFitness)
    return bestSolution


def reductionTermination(originalPopulationWithFitness):
    populationWithFitness = originalPopulationWithFitness
    count = 1
    totalDuration = 0
    print('Minute 0: Population size = ' + str(len(populationWithFitness)))
    while populationWithFitness:
        start = time.time()
        try:
            populationWithFitness = createNewGeneration(populationWithFitness)
            stop = time.time()
            duration = stop - start
            totalDuration += (duration / 60)
            if int(totalDuration) == count:
                print('Minute ' + str(count) + ': Population size = ' + str(len(populationWithFitness)))
                count += 1
            bestSolution = findBestSolution(populationWithFitness)
        except IndexError:
            break
    return bestSolution


def convergenceTermination(originalPopulationWithFitness):
    global reductionPercentage
    reductionPercentage = 100
    populationWithFitness = originalPopulationWithFitness
    count = 0
    currentBest = math.inf
    while count < convergenceNumber:
        populationWithFitness = createNewGeneration(populationWithFitness)
        bestSolution = findBestSolution(populationWithFitness)
        if bestSolution[1] < currentBest:
            currentBest = bestSolution[1]
            count = 0
            print('Current best fitness = ' + str(bestSolution[1]))
        else:
            count += 1
    return bestSolution


def createNewGeneration(populationWithFitness):
    if selectionType == 'Ro':
        childPopulation = Selection.rouletteSelection(populationWithFitness,
                                                      childPopulationSizePercentage)
    elif selectionType == 'To':
        childPopulation = Selection.tournamentSelection(populationWithFitness, tournamentSize,
                                                        childPopulationSizePercentage)
    else:
        print(selectionType + ' is not a valid selection method')
        sys.exit()

    childPopulation = representations[representation].runCrossover(crossoverType, childPopulation)
    childPopulation = representations[representation].runMutation(mutationType, childPopulation, mutationProbability)

    if representation == 'Bi':
        childPopulation = representations[representation].runRepair(childPopulation)

    childPopulationWithFitness = fitnessFunction[representation](childPopulation, cityCords)
    newGeneration = Replacement.generationalReplacement(populationWithFitness,
                                                        childPopulationWithFitness,
                                                        generationalGapPercentage,
                                                        reductionPercentage)
    return newGeneration


def findBestSolution(populationWithFitness):
    sortedPopulation = sorted(populationWithFitness, key=itemgetter(1))
    bestSolution = sortedPopulation[0]
    return bestSolution


def addDataToCsv(originalSolution, finalSolution, algorithmEfficiency):
    algorithm = selectionType + crossoverType + mutationType + terminationType
    selection = [selectionType, selectionParameters[selectionType]]
    termination = [terminationType, terminationParameters[terminationType]]

    with open('tspData.csv', 'a', newline='') as csvfile:
        wr = csv.writer(csvfile, delimiter=',')
        wr.writerow(
            [representation, numberOfCities, populationSize, childPopulationSizePercentage, generationalGapPercentage,
             mutationProbability, algorithm, selection, termination, cityCords, originalSolution, finalSolution,
             algorithmEfficiency])


main()
