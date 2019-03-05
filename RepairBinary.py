def runRepair(population):
    numberOfCities = len(population[0])
    binaryLength = len("{0:b}".format(numberOfCities))
    validPopulation = []
    exampleSolution = []

    for j in range(1, numberOfCities + 1):
        city = bin(j)[2:].zfill(binaryLength)
        print(city)
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
