import random


def runMutation(population, mutationProbability):
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



