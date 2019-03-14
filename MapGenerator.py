import random


def generateMap(numberOfCities):
    maxDistance = 1000
    xCord = [random.randrange(1, maxDistance + 1, 1) for _ in range(numberOfCities)]
    yCord = [random.randrange(1, maxDistance + 1, 1) for _ in range(numberOfCities)]
    xyCords = list(zip(xCord, yCord))
    duplicates = True
    while duplicates:
        if len(xyCords) == len(set(xyCords)):
            duplicates = False
        else:
            s = set()
            any(x in s or s.add(x) for x in xyCords)
            s = set()
            duplicates1 = set(x for x in xyCords if x in s or s.add(x))
            duplicates1 = list(duplicates1)
            for i in range(len(duplicates1)):
                newX = duplicates1[i][0]
                newY = duplicates1[i][1]
                if newX == maxDistance and newY == maxDistance:
                    newX = 0
                    newY = 0
                elif newX == maxDistance:
                    newY += 1
                else:
                    newX += 1
                newXy = (newX, newY)
                xyCords.remove(duplicates1[i])
                xyCords.append(newXy)

    return xyCords

