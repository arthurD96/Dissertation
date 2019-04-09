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
import MatrixOperators
import Replacement
import tspDatabase

numberOfCities = 30
populationSize = 8000
childPopulationSizePercentage = 30
generationalGapPercentage = 20
mutationProbability = 0.001

representation = 'Path'
representations = {'Binary': BinaryOperators, 'Path': PathOperators, 'Matrix': MatrixOperators}

selectionType = ''
tournamentSize = 1
selectionParameters = {'Roulette': None, 'Tournament': tournamentSize}

'''
Crossover Key: 
Binary - (Classical Binary)
Path - (Maximal Preservative, Partially Mapped, Position Based, Order, Order Based, Alternating Position, Cycle)
Matrix - (Union , Intersection)
'''

crossoverType = ''

'''
Mutation Key: 
Binary = (Classical) 
Path and Matrix = (Displacement, Exchange, Insertion, Inversion, Scramble, Simple Inversion)
'''

mutationType = ''

terminationType = ''

iterations = 100
convergenceNumber = 10
reductionPercentage = 99.6
terminationParameters = {'Iteration': iterations, 'Reduction': reductionPercentage, 'Convergence': convergenceNumber}

fitnessFunction = {'Binary': CalculateFitness.calculateFitnessBinary, 'Path': CalculateFitness.calculateFitnessPath,
                   'Matrix': CalculateFitness.calculateFitnessMatrix}

cityCords = MapGenerator.generateMap(numberOfCities)

algorithmDict = {'Path': 'Pa', 'Binary': 'Bi', 'Matrix': 'Ma', 'Tournament': 'To', 'Roulette': 'Ro',
                 'Maximal Preservative': 'MPPa', 'Partially Mapped': 'PMPa', 'Position Based': 'PBPa',
                 'Order': 'OrPa', 'Order Based': 'OBPa', 'Alternating Position': 'APPa', 'Cycle': 'CyPa',
                 'Classical': 'ClBi', 'Intersection': 'IsMa', 'Union': 'UnMa', 'Displacement': 'DiPa',
                 'Exchange': 'ExPa', 'Insertion': 'IsPa', 'Inversion': 'IvPa', 'Scramble': 'ScPa',
                 'Simple Inversion': 'SIPa', 'Convergence': 'Co', 'Reduction': 'Re', 'Iteration': 'It'}


def optimiseAlgorithm():
    global generationalGapPercentage
    global populationSize
    global mutationProbability
    global childPopulationSizePercentage
    childPopulationSizePercentage = 30
    mutationProbability = 0.0001
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
    populationSizes = [5000, 10000, 18000, 25000, 50000]

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
    populationSizes = [5, 10, 15, 20, 50]
    optimalChildPopulationSize = 0
    currentAlgorithmEfficiency = 0
    count = 0

    for childPopulationSizePercentage in populationSizes:
        algorithmEfficiency = singleAlgorithm(population)
        if algorithmEfficiency > currentAlgorithmEfficiency:
            currentAlgorithmEfficiency = algorithmEfficiency
            optimalChildPopulationSize = childPopulationSizePercentage
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
    generationalGaps = [1, 5, 10, 15, 20]
    optimalGenerationalGapPercentage = 0
    currentAlgorithmEfficiency = 0
    count = 0

    for generationalGapPercentage in generationalGaps:
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
                return optimalGenerationalGapPercentage

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

    if terminationType == 'Iteration':
        bestSolution = iterationTermination(originalPopulationWithFitness)
    elif terminationType == 'Reduction':
        bestSolution = reductionTermination(originalPopulationWithFitness)
    elif terminationType == 'Convergence':
        bestSolution = convergenceTermination(originalPopulationWithFitness)
    else:
        print(terminationType + ' is not a valid termination type')

    algorithmEfficiency = int((originalSolution[1] / bestSolution[1]) * 100) - 100
    print("New Solution is: " + str(algorithmEfficiency) + "% faster than the original fastest route")

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
    if selectionType == 'Roulette':
        childPopulation = Selection.rouletteSelection(populationWithFitness,
                                                      childPopulationSizePercentage)
    elif selectionType == 'Tournament':
        childPopulation = Selection.tournamentSelection(populationWithFitness, tournamentSize,
                                                        childPopulationSizePercentage)
    else:
        print(selectionType + ' is not a valid selection method')
        sys.exit()
    childPopulation = representations[representation].runCrossover(crossoverType, childPopulation)
    childPopulation = representations[representation].runMutation(mutationType, childPopulation, mutationProbability)

    if representation == 'Binary':
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
    checked = False
    algorithmKey = algorithmDict[selectionType] + algorithmDict[crossoverType] + algorithmDict[mutationType] + \
                   algorithmDict[terminationType] + str(numberOfCities)
    selectionKey = [algorithmDict[selectionType], selectionParameters[selectionType]]
    terminationKey = [algorithmDict[terminationType], terminationParameters[terminationType]]
    with open('tspData.csv', 'a', newline='') as csvFile:
        wr = csv.writer(csvFile, delimiter=',')
        wr.writerow(
            [algorithmDict[representation], numberOfCities, populationSize, childPopulationSizePercentage, generationalGapPercentage,
             mutationProbability, algorithmKey, selectionKey, terminationKey, cityCords, originalSolution,
             finalSolution,
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
        try:
            reader = csv.reader(csvFile)
            for row in reader:
                if row[13] == 'False':
                    csvData.append(row)
        except IndexError:
            print(row)
            sys.exit()
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
    global representation
    global selectionType
    representation = 'Path'
    crossovers = ['Maximal Preservative', 'Partially Mapped', 'Position Based', 'Order', 'Order Based',
                  'Alternating Position', 'Cycle']
    mutations = ['Displacement', 'Exchange', 'Insertion', 'Inversion', 'Scramble', 'Simple Inversion']
    cities = [30, 50, 70, 100]
    terminations = ['Convergence', 'Reduction', 'Iteration']
    selections = ['Tournament', 'Roulette']

    for terminationType in terminations:
        for selectionType in selections:
            for numberOfCities in cities:
                cityCords = MapGenerator.generateMap(numberOfCities)
                for mutationType in mutations:
                    for crossoverType in crossovers:

                        try:
                            algorithmKey = algorithmDict[selectionType] + algorithmDict[crossoverType] + algorithmDict[
                                mutationType] + \
                                           algorithmDict[terminationType] + str(numberOfCities)
                            conn, cursor = tspDatabase.connectToSQL()
                            exists = tspDatabase.checkAlgorithmExists(algorithmKey, cursor)
                            if exists:
                                print(algorithmKey + ' Exists already')
                                continue
                            else:
                                print('Optimising ' + algorithmKey)
                                optimiseAlgorithm()
                        except Exception as e:
                            print(e)
                            continue


def generateDataBinary():
    global mutationType
    global crossoverType
    global numberOfCities
    global terminationType
    global cityCords
    global representation
    global selectionType
    representation = 'Binary'
    crossovers = ['Classical']
    mutations = ['Classical']
    cities = [30, 50, 70, 100]
    terminations = ['Convergence', 'Reduction', 'Iteration']
    selections = ['Tournament', 'Roulette']

    for terminationType in terminations:
        for selectionType in selections:
            for numberOfCities in cities:
                cityCords = MapGenerator.generateMap(numberOfCities)
                for mutationType in mutations:
                    for crossoverType in crossovers:

                        try:
                            algorithmKey = algorithmDict[selectionType] + algorithmDict[crossoverType] + algorithmDict[
                                mutationType] + \
                                           algorithmDict[terminationType] + str(numberOfCities)
                            conn, cursor = tspDatabase.connectToSQL()
                            exists = tspDatabase.checkAlgorithmExists(algorithmKey, cursor)
                            if exists:
                                print(algorithmKey + ' Exists already')
                                continue
                            else:
                                print('Optimising ' + algorithmKey)
                                optimiseAlgorithm()
                        except Exception as e:
                            print(e)
                            continue


def generateDataMatrix():
    global mutationType
    global crossoverType
    global numberOfCities
    global terminationType
    global cityCords
    global representation
    global selectionType
    representation = 'Matrix'
    crossovers = ['Union', 'Intersection']
    mutations = ['Displacement', 'Exchange', 'Insertion', 'Inversion', 'Scramble', 'Simple Inversion']
    cities = [30, 50, 70, 100]
    terminations = ['Convergence', 'Reduction', 'Iteration']
    selections = ['Tournament', 'Roulette']

    for terminationType in terminations:
        for selectionType in selections:
            for numberOfCities in cities:
                cityCords = MapGenerator.generateMap(numberOfCities)
                for mutationType in mutations:
                    for crossoverType in crossovers:

                        try:
                            algorithmKey = algorithmDict[selectionType] + algorithmDict[crossoverType] + algorithmDict[
                                mutationType] + \
                                           algorithmDict[terminationType] + str(numberOfCities)
                            conn, cursor = tspDatabase.connectToSQL()
                            exists = tspDatabase.checkAlgorithmExists(algorithmKey, cursor)
                            if exists:
                                print(algorithmKey + ' Exists already')
                                continue
                            else:
                                print('Optimising ' + algorithmKey)
                                optimiseAlgorithm()
                        except Exception as e:
                            print(e)
                            continue


def generateData():
    generateDataBinary()
    generateDataPath()
    generateDataMatrix()


generateData()
