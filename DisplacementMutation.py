import random


def runMutation(population, mutationProbability):
    mutatedPopulation = []

    if random.random() < mutationProbability:
        for i in range(0, len(population)):
            currentSolution = population[i]
            mutationProbability = 1  # guarantees one mutation

            # sub tour has to exist and is smaller than the chromosome length
            lengthOfSubTour = random.randint(1, len(currentSolution) - 1)

            # removal point has to be in solution and account for length of sub tour
            removalPoint = random.randint(0, len(currentSolution) - lengthOfSubTour)

            # insertion point can start at index 0 and has to exist in the solution length after sub tour is removed
            insertionPoint = random.randint(0, len(currentSolution) - lengthOfSubTour)

            # Michalewicz Displacement Mutation
            if random.random() < mutationProbability:
                subTour = currentSolution[removalPoint:removalPoint + lengthOfSubTour]

                originalTour = currentSolution[:removalPoint] + currentSolution[removalPoint + lengthOfSubTour:]

                mutatedTour = originalTour[:]
                mutatedTour[insertionPoint:insertionPoint] = subTour

            mutatedPopulation.append(mutatedTour)

        return mutatedPopulation

    else:
        return population

