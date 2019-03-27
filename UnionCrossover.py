import GenerateData


def unionCrossover(population):
    childPopulation = []
    numberOfCities = len(population[0])
    subLength = int(numberOfCities / 2)
    print(subLength)
    for i in range(0, len(population), 2):
        try:
            parentOne = population[i]
            parentTwo = population[i + 1]
        except IndexError:
            parentOne = population[i]
            parentTwo = population[0]

        child = parentOne.copy()

        for i in range(numberOfCities):
            for j in range(numberOfCities):
                if i < subLength and j < subLength:
                    child[i][j] = parentOne[i][j]
                elif i >= subLength and j >= subLength:
                    child[i][j] = parentTwo[i][j]
                elif i < subLength:
                    child[i][j] = 1
                else:
                    child[i][j] = 0
        childPopulation.append(child)

    return childPopulation

