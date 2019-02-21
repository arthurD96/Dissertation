import random


def runCrossover(population):
    numberOfBits = len(population[0][0])
    childPopulation = []
    validChildPopulation = []
    i = 1
    for j in range(0, int(len(population)/2)):
        parentOne = ''.join(population[i - 1])
        parentTwo = ''.join(population[i])

        # John Hollands classic crossover

        crossoverBit = random.randint(1, len(parentOne))

        childOneString = parentOne[:crossoverBit] + parentTwo[crossoverBit:]
        childTwoString = parentTwo[:crossoverBit] + parentOne[crossoverBit:]
        childStrings = [childOneString, childTwoString]

        for string in childStrings:
            allele = ''
            child = []
            for k in range(1, len(string) + 1):
                allele += string[k - 1]
                if k % numberOfBits == 0:
                    child.append(allele)
                    allele = ''
            childPopulation.append(child)

    i += 2
    for child in childPopulation:
        noDuplicates = []

        for allele in child:
            if int(allele) == 0:
                continue
            elif allele not in noDuplicates:
                noDuplicates.append(allele)

        # Re-adding missing alleles
        setInitial = set(population[0])
        setNoDuplicates = set(noDuplicates)
        missing = list(sorted(setInitial - setNoDuplicates))
        missingAddedSolution = noDuplicates + missing
        validMutatedSolution = []

        # Remove newly created alleles that don't exist in original tour
        for allele in missingAddedSolution:
            if allele in population[0]:
                validMutatedSolution.append(allele)

        validChildPopulation.append(validMutatedSolution)
    return validChildPopulation
