import random


def orderBasedCrossover(population):
    childPopulation = []
    for i in range(0, len(population), 2):
        try:
            parentOne = population[i]
            parentTwo = population[i + 1]
        except IndexError:
            parentOne = population[i]
            parentTwo = population[0]
        indexes = list(range(0, len(parentOne)))
        numberOfIndexes = random.randint(0, len(parentOne))
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
        childPopulation.append(children[0])
        childPopulation.append(children[1])

    return childPopulation

