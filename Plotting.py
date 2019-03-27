import matplotlib.pyplot as plt
import sys
import MatrixOperators


def plotRoute(representation, solution, cityCords):
    if representation == 'Ma':
        solution[0] = MatrixOperators.convertMatrixToTour(solution[0])
        representation = 'Pa'
    solution[0].append(solution[0][0])
    xySolution = []
    for i in range(0, len(solution[0])):
        if representation == 'Bi':
            cityInt = int(solution[0][i], 2)
        elif representation == 'Pa':
            cityInt = int(solution[0][i])
        else:
            print(representation + ': is not a valid representation')
            sys.exit()
        xySolution.append(cityCords[cityInt - 1])

    unzippedXy = list(zip(*xySolution))
    xCord = unzippedXy[0]
    yCord = unzippedXy[1]
    plt.plot(xCord, yCord)
    plt.show()


def plotMap(cityCords):
    unzippedXy = list(zip(*cityCords))
    xCord = unzippedXy[0]
    yCord = unzippedXy[1]
    plt.scatter(xCord, yCord)
    plt.show()
