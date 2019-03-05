import random


def runMutation(population, mutationProbability):
    mutatedPopulation = []

    if random.random() < mutationProbability:
        for i in range(0, len(population)):

            currentSolution = population[i]
            mutationProbability = 1  # guarantees one mutation

            # sub tour has to exist and is smaller than the chromosome length
            lengthOfSubTour = random.randint(2, len(currentSolution) - 1)

            # start point has to be in solution and account for length of sub tour
            startPoint = random.randint(0, len(currentSolution) - lengthOfSubTour)

            # Simple inversion mutation Holland 1975 Grefenstette 1987
            if random.random() < mutationProbability:
                revSubTour = currentSolution[startPoint:startPoint + lengthOfSubTour]
                revSubTour.reverse()
                originalTour = currentSolution[:startPoint] + currentSolution[startPoint + lengthOfSubTour:]
                mutatedTour = originalTour[:]
                mutatedTour[startPoint:startPoint] = revSubTour
                mutatedPopulation.append(mutatedTour)

        return mutatedPopulation
    else:
        return population

