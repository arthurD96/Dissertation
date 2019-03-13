import time
from operator import itemgetter
from tqdm import tqdm

import matplotlib.pyplot as plt

import MapGenerator
import GenerateDataSet
import CalculateFitness
import ConvertRoute
import Selection
import BinaryOperators
import Replacement


def main():
    numberOfCities = 60
    populationSize = 300000
    maxDistance = 1000
    tournamentSizePercentage = 5
    childPopulationSizePercentage = 20
    mutationProbability = 1 / (numberOfCities * 5)
    generationalGapPercentage = 5
    generationalSizePercentage = 99.8
    population = GenerateDataSet.generatePopulationBinary(numberOfCities, populationSize)
    cityCords = MapGenerator.generateMap(numberOfCities, maxDistance)
    plotMap(cityCords)
    populationWithFitness = CalculateFitness.calculateFitnessBinary(population, cityCords)
    originalSolution = findBestSolution(populationWithFitness)
    duration = 0
    totalDuration = 0
    while len(populationWithFitness) > 1000:
        start = time.time()
        try:
            print(str(len(populationWithFitness)) + ': loop took ' + str(duration) + ' seconds for a total of ' + str(
                int(totalDuration / 60)) + ' minutes')
            childPopulation = Selection.rouletteSelection(populationWithFitness,
                                                          childPopulationSizePercentage)
            crossoverPopulation = BinaryOperators.runCrossover(childPopulation)
            mutatedPopulation = BinaryOperators.runMutation(crossoverPopulation, mutationProbability)
            repairedSolutions = BinaryOperators.runRepair(mutatedPopulation)
            childPopulationWithFitness = CalculateFitness.calculateFitnessBinary(repairedSolutions, cityCords)

            populationWithFitness = Replacement.generationalReplacement(populationWithFitness,
                                                                        childPopulationWithFitness,
                                                                        generationalGapPercentage,
                                                                        generationalSizePercentage)
            stop = time.time()
            duration = stop - start
            totalDuration += duration
        except IndexError:
            break

    originalXySolution = ConvertRoute.convertRouteToXY(originalSolution, cityCords)
    plotRoute(originalXySolution)
    finalSolution = findBestSolution(populationWithFitness)
    finalXySolution = ConvertRoute.convertRouteToXY(finalSolution, cityCords)
    plotRoute(finalXySolution)

    algorithmEfficiency = (originalSolution[1] / finalSolution[1]) * 100
    print("New Solution is: " + str(int(algorithmEfficiency) - 100) + "% faster than the original fastest route")


def plotRoute(xySolution):
    unzippedXy = list(zip(*xySolution))
    xCord = unzippedXy[0]
    yCord = unzippedXy[1]
    plt.plot(xCord, yCord)
    plt.show()


def plotMap(xyCords):
    unzippedXy = list(zip(*xyCords))
    xCord = unzippedXy[0]
    yCord = unzippedXy[1]
    plt.scatter(xCord, yCord)
    plt.show()


def findBestSolution(populationWithFitness):
    sortedPopulation = sorted(populationWithFitness, key=itemgetter(1))
    bestSolution = sortedPopulation[0]
    return bestSolution


main()
