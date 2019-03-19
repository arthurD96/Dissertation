import random

def partiallyMappedCrossover(population):
    childPopulation = []
    for i in range(0, len(population), 2):
        try:
            parentOne = population[i]
            parentTwo = population[i + 1]
        except IndexError:
            parentOne = population[i]
            parentTwo = population[0]

        crossoverOne = random.randint(0, len(parentOne))
        crossoverTwo = random.randint(0, len(parentOne))

        while crossoverOne == crossoverTwo:
            crossoverTwo = random.randint(1, len(parentOne) - 1)

        if crossoverOne > crossoverTwo:
            crossoverOne, crossoverTwo = crossoverTwo, crossoverOne

        map = []
        revMap = []
        for j in range(crossoverOne, crossoverTwo):
            link = [parentOne[j], parentTwo[j]]
            map.append(link)
            link = [parentTwo[j], parentOne[j]]
            revMap.append(link)
        for j in range(crossoverOne, crossoverTwo):
            link = [parentTwo[j], parentOne[j]]
            map.append(link)
            link = [parentOne[j], parentTwo[j]]
            revMap.append(link)

        childOne = ([None] * crossoverOne) + parentTwo[crossoverOne:crossoverTwo] + (
                [None] * (len(parentOne) - crossoverTwo))
        childTwo = ([None] * crossoverOne) + parentOne[crossoverOne:crossoverTwo] + (
                [None] * (len(parentOne) - crossoverTwo))

        childOne = partiallyMappedMapping(childOne, parentOne, map, revMap)
        childTwo = partiallyMappedMapping(childTwo, parentTwo, revMap, map)

        childPopulation.append(childOne)
        childPopulation.append(childTwo)
    return childPopulation


def partiallyMappedMapping(child, parent, map, revMap):
    for k in range(len(child)):
        if child[k] is None:
            city = parent[k]
            if city not in child:
                child[k] = city
            else:
                while city in child:
                    for a in map:
                        if city == a[0]:
                            if a[1] in child:
                                for b in revMap:
                                    if city == b[0]:
                                        city = b[1]
                                        break
                            else:
                                city = a[1]
                                break
                child[k] = city
    return child


