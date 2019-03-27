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
import tspDatabase

numberOfCities = 50
populationSize = 8000
childPopulationSizePercentage = 30
generationalGapPercentage = 20
mutationProbability = 0.001

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

crossoverType = 'PMPa'

'''
Mutation Key: 
ClBi = Classical Binary 
DiPa = Displacement Path, ExPa = Exchange Path, IsPa = Insertion Path, IvPa = Inversion Path, ScPa = Scramble Path, 
SIPa = Simple Inversion Path
'''

mutationType = 'IsPa'

'Termination Key: It = Iteration, Re = Reduction, Co = Convergence'

terminationType = 'Co'
iterations = 100
convergenceNumber = 50
reductionPercentage = 99.6
terminationParameters = {'It': iterations, 'Re': reductionPercentage, 'Co': convergenceNumber}

fitnessFunction = {'Bi': CalculateFitness.calculateFitnessBinary, 'Pa': CalculateFitness.calculateFitnessPath}
cityCords = MapGenerator.generateMap(numberOfCities)


def optimiseAlgorithm():
    global generationalGapPercentage
    global populationSize
    global mutationProbability
    global childPopulationSizePercentage
    childPopulationSizePercentage = 30
    mutationProbability = 0.001
    populationSize = 8000
    generationalGapPercentage = 20

    optimalPopulation = GenerateDataSet.generatePopulation(representation, numberOfCities, populationSize)
    mutationProbability = optimiseMutationProbability(optimalPopulation)
    childPopulationSizePercentage = optimiseChildPopulationSize(optimalPopulation)
    generationalGapPercentage = optimiseGenerationalGap(optimalPopulation)
    populationSize = optimisePopulationSize()
    finalPopulation = GenerateDataSet.generatePopulation(representation, numberOfCities, populationSize)
    singleAlgorithm(finalPopulation)


def optimisePopulationSize():
    global populationSize
    optimalPopulationSize = 0
    currentAlgorithmEfficiency = 0
    count = 0
    populationSizes = [5000, 10000, 18000, 25000, 50000, 100000]

    for size in populationSizes:
        populationSize = size
        population = GenerateDataSet.generatePopulation(representation, numberOfCities, populationSize)
        algorithmEfficiency = singleAlgorithm(population)
        if algorithmEfficiency > currentAlgorithmEfficiency:
            currentAlgorithmEfficiency = algorithmEfficiency
            optimalPopulationSize = size
            count = 0
        elif algorithmEfficiency == currentAlgorithmEfficiency:
            return optimalPopulationSize
        else:
            count += 1
            if count >= 3:
                return optimalPopulationSize
    return optimalPopulationSize


def optimiseChildPopulationSize(population):
    global childPopulationSizePercentage
    optimalChildPopulationSize = 0
    currentAlgorithmEfficiency = 0
    count = 0

    for size in range(5, 105, 10):
        childPopulationSizePercentage = size
        algorithmEfficiency = singleAlgorithm(population)
        if algorithmEfficiency > currentAlgorithmEfficiency:
            currentAlgorithmEfficiency = algorithmEfficiency
            optimalChildPopulationSize = size
            count = 0
        elif algorithmEfficiency == currentAlgorithmEfficiency:
            return optimalChildPopulationSize
        else:
            count += 1
            if count >= 4:
                return optimalChildPopulationSize
    return optimalChildPopulationSize


def optimiseGenerationalGap(population):
    global generationalGapPercentage
    optimalGenerationalGapPercentage = 0
    currentAlgorithmEfficiency = 0
    count = 0

    for generationalGap in range(5, 105, 10):
        generationalGapPercentage = generationalGap
        algorithmEfficiency = singleAlgorithm(population)
        if algorithmEfficiency > currentAlgorithmEfficiency:
            currentAlgorithmEfficiency = algorithmEfficiency
            optimalGenerationalGapPercentage = generationalGapPercentage
            count = 0
        elif algorithmEfficiency == currentAlgorithmEfficiency:
            return optimalGenerationalGapPercentage
        else:
            count += 1
            if count >= 4:
                return optimiseGenerationalGap()

    return optimalGenerationalGapPercentage


def optimiseMutationProbability(population):
    global mutationProbability
    optimalMutationProbability = 0
    currentAlgorithmEfficiency = 0
    mutations = [0, 0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1]

    for probability in mutations:
        mutationProbability = probability
        algorithmEfficiency = singleAlgorithm(population)
        if algorithmEfficiency > currentAlgorithmEfficiency:
            currentAlgorithmEfficiency = algorithmEfficiency
            optimalMutationProbability = mutationProbability
    return optimalMutationProbability


def singleAlgorithm(originalPopulation):
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

    # Plotting.plotMap(cityCords)
    # Plotting.plotRoute(representation, originalSolution, cityCords)
    # Plotting.plotRoute(representation, bestSolution, cityCords)
    addDataToCsv(originalSolution[0], bestSolution[0], algorithmEfficiency)
    updateDBfromCsv()

    return algorithmEfficiency


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
    count = len(populationWithFitness)
    while populationWithFitness:
        roundedPopulationCount = int(math.ceil(len(populationWithFitness) / 1000.0)) * 1000
        try:
            populationWithFitness = createNewGeneration(populationWithFitness)

            if roundedPopulationCount == count:
                print('Population size = ' + str(count))
                count -= 1000
            elif roundedPopulationCount < count:
                count = roundedPopulationCount
                print('Population size = ' + str(count))
            bestSolution = findBestSolution(populationWithFitness)
        except IndexError:
            break
    print('Best Fitness = ' + str(bestSolution[1]))
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
    algorithm = selectionType + crossoverType + mutationType + terminationType + str(numberOfCities)
    selection = [selectionType, selectionParameters[selectionType]]
    termination = [terminationType, terminationParameters[terminationType]]
    checked = False

    with open('tspData.csv', 'a', newline='') as csvFile:
        wr = csv.writer(csvFile, delimiter=',')
        wr.writerow(
            [representation, numberOfCities, populationSize, childPopulationSizePercentage, generationalGapPercentage,
             mutationProbability, algorithm, selection, termination, cityCords, originalSolution, finalSolution,
             algorithmEfficiency, checked])
    csvFile.close()


def updateDBfromCsv():
    csvData = readUncheckedCsvData()
    conn, cursor = tspDatabase.connectToSQL()
    for row in csvData:
        markCsvRowAsChecked(row)
        algorithm = row[6]
        exists = tspDatabase.checkAlgorithmExists(algorithm, cursor)
        if exists:
            improved = tspDatabase.checkForAlgorithmImprovement(row, algorithm, cursor)
            if improved:
                tspDatabase.replaceResults(row, cursor)
                print(algorithm + ' improved')
            else:
                continue
        else:
            tspDatabase.insertResults(row, cursor)
            print(algorithm + ' added')
    tspDatabase.disconnectFromSQL(conn)


def readUncheckedCsvData():
    csvData = []
    with open('tspData.csv') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if row[13] == 'False':
                csvData.append(row)
    csvFile.close()
    return csvData


def markCsvRowAsChecked(rowToCheck):
    rowsToWrite = []
    with open('tspData.csv') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            if row == rowToCheck:
                row[13] = 'TRUE'
            rowsToWrite.append(row)

    with open('tspData.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        for row in rowsToWrite:
            writer.writerow(row)


def generateDataPath():
    global mutationType
    global crossoverType
    global numberOfCities
    global terminationType
    global cityCords
    crossovers = ['PMPa', 'PBPa', 'OrPa', 'OBPa', 'APPa', 'CyPa', 'MPPa']
    mutations = ['ExPa', 'IsPa', 'IvPa', 'ScPa', 'SIPa', 'DiPa']
    cities = [30, 50, 70, 100, 60, 80, 90, 40, 10, 20]
    terminations = ['Co', 'Re', 'It']

    for terminationType in terminations:
        for numberOfCities in cities:
            cityCords = MapGenerator.generateMap(numberOfCities)
            for mutationType in mutations:
                for crossoverType in crossovers:

                    try:
                        algorithm = selectionType + crossoverType + mutationType + terminationType + str(numberOfCities)
                        conn, cursor = tspDatabase.connectToSQL()
                        exists = tspDatabase.checkAlgorithmExists(algorithm, cursor)
                        if exists:
                            continue
                        else:
                            optimiseAlgorithm()
                    except:
                        continue


generateDataPath()
