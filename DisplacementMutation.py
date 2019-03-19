import random


def displacementMutation(population, mutationProbability):
    for i in range(0,len(population)):
        if random.random() < mutationProbability:
            currentSolution = population[i]
            lengthOfSubTour = random.randint(1, len(currentSolution) - 1)
            removalPoint = random.randint(0, len(currentSolution) - lengthOfSubTour)
            insertionPoint = random.randint(0, len(currentSolution) - lengthOfSubTour)
            while removalPoint == insertionPoint:
                insertionPoint = random.randint(0, len(currentSolution) - lengthOfSubTour)
            subTour = currentSolution[removalPoint:removalPoint + lengthOfSubTour]
            fullTour = currentSolution[:removalPoint] + currentSolution[removalPoint + lengthOfSubTour:]
            fullTour[insertionPoint:insertionPoint] = subTour
            population[i] = fullTour
    return population
