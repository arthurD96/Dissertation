import random


def runMutation(population, mutationProbability):
    mutatedPopulation = []

    if random.random() < mutationProbability:
        for i in range(0, len(population)):
            currentSolution = population[i]

            firstAlleleToSwap = random.randint(0, len(currentSolution)-1)
            secondAlleleToSwap = random.randint(0, len(currentSolution)-1)

            # ensure the alleles are different
            while firstAlleleToSwap == secondAlleleToSwap:
                secondAlleleToSwap = random.randint(0, len(currentSolution) - 1)

            # Exchange Mutation Banzhaf 1990
            mutatedSolution = currentSolution[:]

            mutatedSolution[firstAlleleToSwap] = currentSolution[secondAlleleToSwap]
            mutatedSolution[secondAlleleToSwap] = currentSolution[firstAlleleToSwap]

            mutatedPopulation.append(mutatedSolution)

        return mutatedPopulation

    else:
        return population

