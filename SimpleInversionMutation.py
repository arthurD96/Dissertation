import random


def simpleInversionMutation(population, mutationProbability):
    for i in range(0,len(population)):
        if random.random() < mutationProbability:
            currentSolution = population[i]
            lengthOfSubTour = random.randint(2, len(currentSolution) - 1)
            startPoint = random.randint(0, len(currentSolution) - lengthOfSubTour)
            revSubTour = currentSolution[startPoint:startPoint + lengthOfSubTour]
            revSubTour.reverse()
            mutatedTour = currentSolution[:startPoint] + currentSolution[startPoint + lengthOfSubTour:]
            mutatedTour[startPoint:startPoint] = revSubTour
            population[i] = mutatedTour
    return population
