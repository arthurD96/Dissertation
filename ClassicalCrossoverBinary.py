import random


def runCrossover(population):
    childPopulation = []

    for i in range(1, len(population)):
        parentOne = ''.join(population[i - 1])
        parentTwo = ''.join(population[i])

        # John Hollands classic crossover

        crossoverBit = random.randint(0, len(parentOne))

        childOneString = parentOne[:crossoverBit] + parentTwo[crossoverBit:]
        childTwoString = parentTwo[:crossoverBit] + parentOne[crossoverBit:]
        childStrings = [childOneString, childTwoString]

        for string in childStrings:
            allele = ''
            child = []
            for j in range(1, len(string) + 1):
                allele += string[j - 1]
                if j % 3 == 0:
                    child.append(allele)
                    allele = ''
            childPopulation.append(child)

    return childPopulation
