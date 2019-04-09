import random
import sys
from collections import deque


def maximalPreservativeCrossover(numberOfCities, parentOne, parentTwo):
    if numberOfCities < 10:
        crossoverOne = random.randint(0, numberOfCities - 1)
        crossoverTwo = random.randint(crossoverOne + 1, numberOfCities)
    else:
        crossoverOne = random.randint(0, numberOfCities - 10)
        crossoverTwo = random.randint(crossoverOne + 1, numberOfCities)
        if crossoverTwo - crossoverOne < 10:
            crossoverTwo = crossoverOne + 10
        elif crossoverTwo - crossoverOne > numberOfCities / 2:
            crossoverTwo = crossoverOne + (numberOfCities / 2)
        crossoverTwo = int(crossoverTwo)
    childOne = ([None] * crossoverOne) + parentTwo[crossoverOne:crossoverTwo] + (
            [None] * (numberOfCities - crossoverTwo))
    childTwo = ([None] * crossoverOne) + parentOne[crossoverOne:crossoverTwo] + (
            [None] * (numberOfCities - crossoverTwo))

    children = [childOne, childTwo]
    parents = [parentOne, parentTwo]
    for j in range(len(children)):
        child = children[j]
        parent = parents[j]
        for city in parent:
            if city not in child:
                index = child.index(None)
                child[index] = city
    return children


def partiallyMappedCrossover(numberOfCities, parentOne, parentTwo):
    crossoverOne = random.randint(0, numberOfCities - 1)
    crossoverTwo = random.randint(0, numberOfCities - 1)

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
            [None] * (numberOfCities - crossoverTwo))
    childTwo = ([None] * crossoverOne) + parentOne[crossoverOne:crossoverTwo] + (
            [None] * (numberOfCities - crossoverTwo))

    childOne = partiallyMappedMapping(childOne, parentOne, map, revMap)
    childTwo = partiallyMappedMapping(childTwo, parentTwo, revMap, map)
    children = [childOne, childTwo]
    return children


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


def positionBasedCrossover(numberOfCities, parentOne, parentTwo):
    indexes = list(range(0, numberOfCities))
    numberOfIndexes = random.randint(0, numberOfCities)
    indexes = random.sample(indexes, numberOfIndexes)
    childOne = [None] * numberOfCities
    childTwo = [None] * numberOfCities
    parents = [parentOne, parentTwo]
    children = [childOne, childTwo]
    for index in indexes:
        childOne[index] = parentTwo[index]
        childTwo[index] = parentOne[index]
    for counter in range(2):
        for city in parents[counter]:
            if city not in children[counter]:
                index = children[counter].index(None)
                children[counter][index] = city
    return children


def orderCrossover(numberOfCities, parentOne, parentTwo):
    crossoverOne = random.randint(0, numberOfCities)
    crossoverTwo = random.randint(0, numberOfCities)

    while crossoverOne == crossoverTwo:
        crossoverTwo = random.randint(1, numberOfCities - 1)

    if crossoverOne > crossoverTwo:
        crossoverOne, crossoverTwo = crossoverTwo, crossoverOne

    childOne = ([None] * crossoverOne) + parentOne[crossoverOne:crossoverTwo] + (
            [None] * (numberOfCities - crossoverTwo))
    childTwo = ([None] * crossoverOne) + parentTwo[crossoverOne:crossoverTwo] + (
            [None] * (numberOfCities - crossoverTwo))
    order = deque(list(range(numberOfCities)))
    order.rotate(-crossoverTwo)
    children = [childOne, childTwo]
    parents = [parentTwo, parentOne]
    for child in children:
        index = children.index(child)
        for i in range(len(order)):
            if None not in child:
                break
            else:
                notPlaced = True
                j = i
                childIndex = order[j]
                while notPlaced and j < len(order):
                    parentIndex = order[j]
                    if parents[index][parentIndex] not in child:
                        child[childIndex] = parents[index][parentIndex]
                        notPlaced = False
                    else:
                        j += 1
    return children


def orderBasedCrossover(numberOfCities, parentOne, parentTwo):
    indexes = list(range(0, numberOfCities))
    numberOfIndexes = random.randint(0, numberOfCities)
    indexes = random.sample(indexes, numberOfIndexes)
    parents = [parentOne, parentTwo]
    children = [parentOne.copy(), parentTwo.copy()]
    for counter in range(len(parents)):
        cities = []
        if counter == 0:
            childIndex = 0
            parentIndex = 1
        else:
            childIndex = 1
            parentIndex = 0
        for index in indexes:
            cities.append(parents[parentIndex][index])
        for city in cities:
            if city in children[childIndex]:
                cityIndex = children[childIndex].index(city)
                children[childIndex][cityIndex] = None
        count = 0
        for j in range(len(children[childIndex])):
            if children[childIndex][j] is None:
                children[childIndex][j] = cities[count]
                count += 1
    return children


def alternatingPositionCrossover(numberOfCities, parentOne, parentTwo):
    parentListOne = []
    parentListTwo = []
    for j in range(numberOfCities):
        parentListOne.append(parentOne[j])
        parentListOne.append(parentTwo[j])
        parentListTwo.append(parentTwo[j])
        parentListTwo.append(parentOne[j])
    childOne = []
    childTwo = []
    children = [childOne, childTwo]
    for city in range(len(parentListOne)):
        if parentListOne[city] not in childOne:
            childOne.append(parentListOne[city])
        if parentListTwo[city] not in childTwo:
            childTwo.append(parentListTwo[city])
    return children


def cycleCrossover(numberOfCities, parentOne, parentTwo):
    relationMap = dict(zip(parentOne, parentTwo))
    keys = list(relationMap.keys())
    childOne = [None] * numberOfCities
    childTwo = [None] * numberOfCities
    parents = [parentOne, parentTwo]
    children = [childOne, childTwo]
    count = 0
    while keys:

        start = keys[0]
        current = relationMap[start]
        cycle = []
        while current not in cycle:
            cycle.append(current)
            current = relationMap[current]
            keys.remove(current)
        for item in cycle:
            index = parents[count].index(item)
            childOne[index] = item
            if count == 0:
                index = parents[1].index(item)
                childTwo[index] = item
            else:
                index = parents[0].index(item)
                childTwo[index] = item
        if count == 0:
            count = 1
        else:
            count = 0
    return children


def displacementMutation(solutionToMutate):
    lengthOfSubTour = random.randint(1, len(solutionToMutate) - 1)
    removalPoint = random.randint(0, len(solutionToMutate) - lengthOfSubTour)
    insertionPoint = random.randint(0, len(solutionToMutate) - lengthOfSubTour)
    while removalPoint == insertionPoint:
        insertionPoint = random.randint(0, len(solutionToMutate) - lengthOfSubTour)
    subTour = solutionToMutate[removalPoint:removalPoint + lengthOfSubTour]
    fullTour = solutionToMutate[:removalPoint] + solutionToMutate[removalPoint + lengthOfSubTour:]
    fullTour[insertionPoint:insertionPoint] = subTour
    return fullTour


def exchangeMutation(solutionToMutate):
    firstAlleleToSwap = random.randint(0, len(solutionToMutate) - 1)
    secondAlleleToSwap = random.randint(0, len(solutionToMutate) - 1)
    while firstAlleleToSwap == secondAlleleToSwap:
        secondAlleleToSwap = random.randint(0, len(solutionToMutate) - 1)
    firstAllele = solutionToMutate[firstAlleleToSwap]
    secondAllele = solutionToMutate[secondAlleleToSwap]
    solutionToMutate[firstAlleleToSwap] = secondAllele
    solutionToMutate[secondAlleleToSwap] = firstAllele
    return solutionToMutate


def insertionMutation(solutionToMutate):
    alleleToMove = random.randint(0, len(solutionToMutate) - 1)
    insertionPoint = random.randint(0, len(solutionToMutate) - 1)
    while alleleToMove == insertionPoint:
        insertionPoint = random.randint(0, len(solutionToMutate) - 1)
    removedCity = solutionToMutate[alleleToMove]
    del solutionToMutate[alleleToMove]
    solutionToMutate.insert(insertionPoint, removedCity)
    return solutionToMutate


def inversionMutation(solutionToMutate):
    lengthOfSubTour = random.randint(1, len(solutionToMutate) - 1)
    removalPoint = random.randint(0, len(solutionToMutate) - lengthOfSubTour)
    insertionPoint = random.randint(0, len(solutionToMutate) - lengthOfSubTour)

    while removalPoint == insertionPoint:
        insertionPoint = random.randint(0, len(solutionToMutate) - lengthOfSubTour)
    subTour = solutionToMutate[removalPoint:removalPoint + lengthOfSubTour]
    subTour.reverse()
    fullTour = solutionToMutate[:removalPoint] + solutionToMutate[removalPoint + lengthOfSubTour:]
    fullTour[insertionPoint:insertionPoint] = subTour
    return fullTour


def scrambleMutation(solutionToMutate):
    lengthOfSubTour = random.randint(2, len(solutionToMutate) - 1)
    startPoint = random.randint(0, len(solutionToMutate) - lengthOfSubTour)
    subTour = solutionToMutate[startPoint:startPoint + lengthOfSubTour]
    random.shuffle(subTour)
    mutatedTour = solutionToMutate[:startPoint] + solutionToMutate[startPoint + lengthOfSubTour:]
    mutatedTour[startPoint:startPoint] = subTour
    return mutatedTour


def simpleInversionMutation(solutionToMutate):
    lengthOfSubTour = random.randint(2, len(solutionToMutate) - 1)
    startPoint = random.randint(0, len(solutionToMutate) - lengthOfSubTour)
    revSubTour = solutionToMutate[startPoint:startPoint + lengthOfSubTour]
    revSubTour.reverse()
    mutatedTour = solutionToMutate[:startPoint] + solutionToMutate[startPoint + lengthOfSubTour:]
    mutatedTour[startPoint:startPoint] = revSubTour
    return mutatedTour


crossovers = {
    'Maximal Preservative': maximalPreservativeCrossover, 'Partially Mapped': partiallyMappedCrossover,
    'Position Based': positionBasedCrossover,
    'Order': orderCrossover, 'Order Based': orderBasedCrossover, 'Alternating Position': alternatingPositionCrossover,
    'Cycle': cycleCrossover
}


mutations = {
    'Displacement': displacementMutation, 'Exchange': exchangeMutation, 'Insertion': insertionMutation,
    'Inversion': inversionMutation,
    'Scramble': scrambleMutation, 'Simple Inversion': simpleInversionMutation
}


def runCrossover(crossover, population):
    childPopulation = []
    numberOfCities = len(population[0])
    crossoverFunction = crossovers.get(crossover)
    if crossoverFunction:
        for i in range(0, len(population), 2):
            try:
                parentOne = population[i]
                parentTwo = population[i + 1]
            except IndexError:
                parentOne = population[i]
                parentTwo = population[0]

            children = crossoverFunction(numberOfCities, parentOne, parentTwo)
            children[0] = list(filter(None, children[0]))
            children[1] = list(filter(None, children[1]))
            childPopulation.extend(children)
    else:
        print(str(crossover) + ' is not a valid Path crossover')
        sys.exit()

    return childPopulation


def runMutation(mutation, population, mutationProbability):
    mutationFunction = mutations.get(mutation)
    if mutationFunction:
        for i in range(0, len(population)):
            if random.random() < mutationProbability:
                population[i] = mutationFunction(population[i])
    else:
        print(str(mutation) + ' is not a valid Path mutation')
        sys.exit()
    return population
