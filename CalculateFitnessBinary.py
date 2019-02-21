def calculateFitness(population, tspMap):
    populationWithFitness = []
    for solution in population:
        fitness = 0
        for i in range(1, len(solution)):
            fitness += tspMap[int(solution[i - 1], 2) - 1][int(solution[i], 2) - 1]
        populationWithFitness.append([solution, fitness])
    return populationWithFitness

# def convertBinaryToInt(binaryPopulation):
#     intPopulation = []
#     for solution in binaryPopulation:
#         intSolution = []
#         for binaryCity in solution:
#             intCity = int(binaryCity, 2)
#             intSolution.append(intCity)
#         intPopulation.append(intSolution)
#     return intPopulation
#
