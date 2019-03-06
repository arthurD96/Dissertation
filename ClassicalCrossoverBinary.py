import random

def runCrossover(population):
    childPopulation = []
    numberOfBits = len(population[0][0])

    for i in range(0, len(population), 2):
        try:
            parentOne = ''.join(population[i])
            parentTwo = ''.join(population[i + 1])
        except IndexError:
            parentOne = ''.join(population[i])
            parentTwo = ''.join(population[0])

        crossoverBit = random.randint(1, len(parentOne)-1)

        childOne = parentOne[:crossoverBit] + parentTwo[crossoverBit:]
        childTwo = parentTwo[:crossoverBit] + parentOne[crossoverBit:]
        children = [childOne, childTwo]

        for string in children:
            child = [string[i:i + numberOfBits] for i in range(0, len(string), numberOfBits)]
            childPopulation.append(child)

    return childPopulation





