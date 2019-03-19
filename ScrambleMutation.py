import random


def scrambleMutation(population, mutationProbability):
    for i in range(0, len(population)):
        if random.random() < mutationProbability:
            currentSolution = population[i]
            lengthOfSubTour = random.randint(2, len(currentSolution) - 1)
            startPoint = random.randint(0, len(currentSolution) - lengthOfSubTour)
            subTour = currentSolution[startPoint:startPoint + lengthOfSubTour]
            random.shuffle(subTour)
            mutatedTour = currentSolution[:startPoint] + currentSolution[startPoint + lengthOfSubTour:]
            mutatedTour[startPoint:startPoint] = subTour
            population[i] = mutatedTour
    return population
