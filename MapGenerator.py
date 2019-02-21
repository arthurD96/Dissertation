import random


def generateMap(numberOfCities, maxDistance):
    tspMap = []

    for i in range(numberOfCities):
        tspDistances = []
        for j in range(numberOfCities):
            tspDistances.append('')
        tspMap.append(tspDistances)
    for i in range(0, numberOfCities):
        for j in range(0, numberOfCities):
            if i == j:
                tspMap[i][j] = 0
            elif tspMap[i][j] == '':
                distance = random.randint(1, maxDistance)
                tspMap[i][j] = distance
                tspMap[j][i] = distance
    return tspMap