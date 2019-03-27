import random
import sys


def runMutation(mutation, population, mutationProbability):
    if mutation != 'ClBi':
        print(mutation + ' is not a valid binary mutation')
        sys.exit()
    mutatedPopulation = []

    for i in range(0, len(population)):
        currentSolution = population[i]
        mutatedSolution = []

        for allele in currentSolution:
            mutatedAllele = ""
            for bit in allele:
                if random.random() < mutationProbability:
                    if bit == "0":
                        bit = "1"
                        mutatedAllele = mutatedAllele + bit
                    else:
                        bit = "0"
                        mutatedAllele = mutatedAllele + bit
                else:
                    mutatedAllele = mutatedAllele + bit

            mutatedSolution.append(mutatedAllele)
        mutatedPopulation.append(mutatedSolution)

    return mutatedPopulation


def runCrossover(crossover, population):
    if crossover != 'ClBi':
        print(crossover + ' is not a valid binary crossover')
        sys.exit()
    childPopulation = []
    numberOfBits = len(population[0][0])

    for i in range(0, len(population), 2):
        try:
            parentOne = ''.join(population[i])
            parentTwo = ''.join(population[i + 1])
        except IndexError:
            parentOne = ''.join(population[i])
            parentTwo = ''.join(population[0])

        crossoverBit = random.randint(1, len(parentOne) - 1)

        childOne = parentOne[:crossoverBit] + parentTwo[crossoverBit:]
        childTwo = parentTwo[:crossoverBit] + parentOne[crossoverBit:]
        children = [childOne, childTwo]

        for string in children:
            child = [string[i:i + numberOfBits] for i in range(0, len(string), numberOfBits)]
            childPopulation.append(child)
    return childPopulation


def runRepair(population):
    numberOfCities = len(population[0])
    binaryLength = len("{0:b}".format(numberOfCities))
    validPopulation = []
    exampleSolution = []

    for j in range(1, numberOfCities + 1):
        city = bin(j)[2:].zfill(binaryLength)
        exampleSolution.append(city)
    setExample = frozenset(exampleSolution)

    for solution in population:
        validCities = [x for x in solution if x in setExample]
        validCities = list(dict.fromkeys(validCities))
        missingCities = [x for x in setExample if x not in solution]
        missingCities = list(missingCities)
        validCities.extend(missingCities)
        validPopulation.append(validCities)

    return validPopulation
