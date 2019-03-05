from operator import itemgetter

import matplotlib.pyplot as plt
import MapGenerator
import GenerateDataSet
import CalculateFitness
import ConvertRoute


def main():
    numberOfCities = 100
    populationSize = 1000
    maxDistance = 100
    population = GenerateDataSet.generatePopulationBinary(numberOfCities, populationSize)
    cityCords = MapGenerator.generateMap(numberOfCities, maxDistance)
    plotMap(cityCords)
    populationWithFitness = CalculateFitness.calculateFitnessBinary(population, cityCords)
    bestSolution = findBestSolution(populationWithFitness)
    print(bestSolution)
    xySolution = ConvertRoute.convertRouteToXY(bestSolution, cityCords)
    plotRoute(xySolution)


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
