import random


def exchangeMutation(population, mutationProbability):
    for i in range(0,len(population)):
        if random.random() < mutationProbability:
            currentSolution = population[i]
            firstAlleleToSwap = random.randint(0, len(currentSolution) - 1)
            secondAlleleToSwap = random.randint(0, len(currentSolution) - 1)
            while firstAlleleToSwap == secondAlleleToSwap:
                secondAlleleToSwap = random.randint(0, len(currentSolution) - 1)
            firstAllele = currentSolution[firstAlleleToSwap]
            secondAllele = currentSolution[secondAlleleToSwap]
            currentSolution[firstAlleleToSwap] = secondAllele
            currentSolution[secondAlleleToSwap] = firstAllele
            population[i] = currentSolution
    return population
