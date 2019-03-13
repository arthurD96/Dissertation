def convertRouteToXY(solution, cityCords):
    solution[0].append(solution[0][0])
    xySolution = []
    for i in range(0, len(solution[0])):
        cityInt = int(solution[0][i], 2)
        xySolution.append(cityCords[cityInt - 1])
    return xySolution
