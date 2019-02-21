import GenerateBinaryDataSet
import ClassicalMutationBinary
import ClassicalCrossoverBinary
import MapGenerator
import CalculateFitnessBinary
import TournamentSelection
import NextGenerationSelection
import BestSolutionSelection
import time
from tqdm import tqdm

populationSize = 100
numberOfCities = 10
distanceBetweenCities = 100
selectionPercentage = 40
selectionReturnPercentage = 100
mutationProbability = 1 / numberOfCities


def johnHollandGa():
    tspMap = MapGenerator.generateMap(numberOfCities, distanceBetweenCities)
    candidateSolutions = generateBinaryPopulation()
    candidateSolutionsWithFitness = calculateFitness(candidateSolutions, tspMap)
    originalBestSolution = BestSolutionSelection.findBestSolution(candidateSolutionsWithFitness)[1]

    for i in tqdm(range(50)):
        bestSolutions = parentSelection(candidateSolutionsWithFitness)
        childSolutions = applyCrossover(bestSolutions)
        mutatedSolutions = applyMutation(childSolutions)
        mutatedSolutionsWithFitness = calculateFitness(mutatedSolutions, tspMap)
        parentSolutionWithFitness = calculateFitness(bestSolutions, tspMap)
        candidateSolutionsWithFitness = nextGenerationSelection(mutatedSolutionsWithFitness, parentSolutionWithFitness)
    time.sleep(1)
    finalBestSolution = BestSolutionSelection.findBestSolution(candidateSolutionsWithFitness)[1]
    print(originalBestSolution)
    print(finalBestSolution)
    mutationEfficiency = (originalBestSolution/finalBestSolution)*100
    print("New Solution is: " + str(int(mutationEfficiency)) + "% faster than the original fastest route")
    exampleSolution = BestSolutionSelection.findBestSolution(candidateSolutionsWithFitness)[0]
    print(exampleSolution)


def generateBinaryPopulation():
    candidateSolutions = GenerateBinaryDataSet.generatePopulation(numberOfCities, populationSize)
    return candidateSolutions


def calculateFitness(population, tspMap):
    populationWithFitness = CalculateFitnessBinary.calculateFitness(population, tspMap)
    return populationWithFitness


def parentSelection(population):
    selectedParents = TournamentSelection.tournamentSelection(population, selectionPercentage,
                                                              selectionReturnPercentage)
    return selectedParents


def applyCrossover(population):
    childPopulation = ClassicalCrossoverBinary.runCrossover(population)
    return childPopulation


def applyMutation(population):
    mutatedPopulation = ClassicalMutationBinary.runMutation(population, mutationProbability)
    return mutatedPopulation


def nextGenerationSelection(mutatedPopulation, parentPopulation):
    nextGeneration = NextGenerationSelection.selectNextGeneration(mutatedPopulation, parentPopulation)
    return nextGeneration


johnHollandGa()
