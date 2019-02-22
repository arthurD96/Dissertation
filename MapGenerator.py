import random
import matplotlib.pyplot as plt


def main():
    numberOfCities = 100
    maxDistance = 1000
    map = generateMap(numberOfCities, maxDistance)
    print(map)


def generateMap(numberOfCities, maxDistance):
    xCord = [random.randrange(1, maxDistance + 1, 1) for _ in range(numberOfCities)]
    yCord = [random.randrange(1, maxDistance + 1, 1) for _ in range(numberOfCities)]
    n = list(range(1, numberOfCities + 1))
    xyCord = list(zip(xCord, yCord))
    duplicates = True
    while duplicates:
        if len(xyCord) == len(set(xyCord)):
            duplicates = False
        else:
            s = set()
            any(x in s or s.add(x) for x in xyCord)
            s = set()
            duplicates1 = set(x for x in xyCord if x in s or s.add(x))
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
                xyCord.remove(duplicates1[i])
                xyCord.append(newXy)
    unzippedXy = list(zip(*xyCord))
    xCord = unzippedXy[0]
    yCord = unzippedXy[1]
    plt.scatter(xCord, yCord)
    plt.show()
    return xyCord


main()
