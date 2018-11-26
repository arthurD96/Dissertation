import random


def runMutation(population, mutationProbability):
    mutatedPopulation = []

    for i in range(0, len(population)):
        currentSolution = population[i]

        # John Hollands classic bit flip mutation
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

        # Repair Operation
        # Removing Duplicate solutions from the mutated chromosome
        noDuplicates = []

        for allele in mutatedSolution:
            if int(allele) == 0:
                continue
            elif allele not in noDuplicates:
                noDuplicates.append(allele)

        # Re-adding missing alleles
        setInitial = set(currentSolution)
        setNoDuplicates = set(noDuplicates)
        missing = list(sorted(setInitial - setNoDuplicates))
        missingAddedSolution = noDuplicates + missing
        validMutatedSolution = []

        # Remove newly created alleles that don't exist in original tour
        for allele in missingAddedSolution:
            if allele in currentSolution:
                validMutatedSolution.append(allele)

        mutatedPopulation.append(validMutatedSolution)

    return mutatedPopulation

