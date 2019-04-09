import math
import sys
import csv
import time
import threading
from concurrent import futures
from operator import itemgetter
import queue
from tqdm import tqdm

import MapGenerator
import GenerateDataSet
import CalculateFitness
import Selection
import BinaryOperators
import PathOperators
import MatrixOperators
import Replacement
import Plotting
import tspDatabase

import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import tkinter as tk
from tkinter import ttk, IntVar

style.use("ggplot")
fontLarge = ("Courier", 14)
populationLock = threading.Lock()

numberOfCities = 0
populationSize = 0
childPopulationSizePercentage = 0
generationalGapPercentage = 0
mutationProbability = 0
xyCoords = [[], []]

representation = ''
representations = {'Binary': BinaryOperators, 'Path': PathOperators, 'Matrix': MatrixOperators}

selectionType = ''
tournamentSize = 0
selectionParameters = {'Roulette': None, 'Tournament': tournamentSize}

'''
Crossover Key: 
Binary - (ClBi = Classical Binary)
Path - (MPPa = Maximal Preservative Path, PMPa = Partially Mapped Path, PBPa = Position Based Path, OrPa = Order Path,
OBPa = Order Based Path, APPa = Alternating Position Path, CyPa = Cycle Based Path)
Matrix - (UnMa = Union Matrix, IsMa = Intersection Matrix)
'''

crossoverType = ''

'''
Mutation Key: 
ClBi = Classical Binary 
DiPa = Displacement Path, ExPa = Exchange Path, IsPa = Insertion Path, IvPa = Inversion Path, ScPa = Scramble Path, 
SIPa = Simple Inversion Path
'''

mutationType = ''

terminationType = ''
iterations = 0
convergenceNumber = 0
reductionPercentage = 0
terminationParameters = {'Iteration': iterations, 'Reduction': reductionPercentage, 'Convergence': convergenceNumber}

fitnessFunction = {'Binary': CalculateFitness.calculateFitnessBinary, 'Path': CalculateFitness.calculateFitnessPath,
                   'Matrix': CalculateFitness.calculateFitnessMatrix}

originalPopulation = []
originalPopulationWithFitness = []
originalSolution = []
bestSolution = []


class tspInterface(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "TSP Data Generator")

        mainFrame = ttk.Frame(self, padding="3 3 12 12")
        mainFrame.grid(column=0, row=0, sticky="nsew")
        mainFrame.grid_rowconfigure(0, weight=1)
        mainFrame.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MapGeneration, AlgorithmSelector, ProgressViewer):
            frame = F(mainFrame, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        self.showFrame(MapGeneration)

    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class MapGeneration(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.mapFigure = Figure(figsize=(5, 5), dpi=100)
        self.mapPlot = self.mapFigure.add_subplot(111)

        mainLabel = ttk.Label(self, text="Travelling Salesman Problem: Map Generator", font=fontLarge)
        mainLabel.grid(column=1, columnspan=3, row=0, sticky=tk.N + tk.W)

        numberOfCitiesLabel = ttk.Label(self, text="Number of Cities")
        numberOfCitiesLabel.grid(column=1, row=2, sticky=tk.N + tk.W)
        self.citiesInt = tk.StringVar()
        numberOfCitiesEntry = ttk.Entry(self, width=12, textvariable=self.citiesInt)
        numberOfCitiesEntry.grid(column=3, row=2, sticky=tk.N + tk.W)
        numberOfCitiesEntry.focus()
        generateButton = ttk.Button(self, text="Generate New Map", command=lambda: self.generateMap(controller))
        generateButton.grid(column=3, row=3, sticky=tk.N + tk.W)

        self.canvas = FigureCanvasTkAgg(self.mapFigure, self)
        self.canvas.get_tk_widget().grid(column=5, row=1, sticky=tk.N + tk.W)
        self.canvas._tkcanvas.grid(column=5, row=1, rowspan=20, sticky=tk.N + tk.W)
        self.canvas.draw()

        toolbarFrame = tk.Frame(self)
        toolbarFrame.grid(column=5, row=0, sticky=tk.N + tk.E)
        NavigationToolbar2Tk(self.canvas, toolbarFrame)

        for child in self.winfo_children():
            child.grid_configure(padx=10, pady=4)

    def generateMap(self, controller):
        global numberOfCities
        global xyCoords
        try:
            numberOfCities = int(self.citiesInt.get())
            xyCoords = MapGenerator.generateMap(numberOfCities)
            unzippedXy = list(zip(*xyCoords))
            self.mapPlot.clear()
            self.mapPlot.scatter(unzippedXy[0], unzippedXy[1], s=7)
            self.canvas.draw()
            acceptMapButton = ttk.Button(self, text="Accept Map",
                                         command=lambda: controller.showFrame(AlgorithmSelector))
            acceptMapButton.grid(column=3, row=4, sticky=tk.N + tk.W, padx=10, pady=4)
        except (ValueError, TypeError) as e:
            tk.messagebox.showinfo("Error", "Please enter a valid number of cities.\n" + str(e))


class AlgorithmSelector(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        returnToMapButton = ttk.Button(self, text="Return", command=lambda: controller.showFrame(MapGeneration))
        returnToMapButton.grid(column=0, row=0, sticky=tk.N + tk.W)

        mainLabel = ttk.Label(self, text="Travelling Salesman Problem: Algorithm Selection", font=fontLarge)
        mainLabel.grid(column=0, columnspan=2, row=1, sticky=tk.N + tk.W)

        representations = ["Path", "Binary", "Matrix"]
        self.representation = tk.StringVar()
        representationLabel = ttk.Label(self, text="Representation: ")
        representationLabel.grid(column=0, row=2, sticky=tk.N + tk.W)
        self.representationOption = ttk.OptionMenu(self, self.representation, representations[0], *representations)
        self.representationOption.grid(column=1, row=2, sticky=tk.N + tk.W)

        self.populationSize = tk.IntVar()
        self.populationSize.set(8000)
        populationLabel = ttk.Label(self, text="Population Size:")
        populationLabel.grid(column=0, row=3, sticky=tk.N + tk.W)
        self.populationEntry = ttk.Entry(self, textvariable=self.populationSize)
        self.populationEntry.grid(column=1, row=3, sticky=tk.N + tk.W)

        self.childPercentage = tk.IntVar()
        self.childPercentage.set(30)
        childPerecentageLabel = ttk.Label(self, text="Child Population Size (as %)")
        childPerecentageLabel.grid(column=0, row=4, sticky=tk.N + tk.W)
        self.childPopulationEntry = ttk.Entry(self, textvariable=self.childPercentage)
        self.childPopulationEntry.grid(column=1, row=4, sticky=tk.N + tk.W)

        self.generationGap = tk.IntVar()
        self.generationGap.set(15)
        generationGapLabel = ttk.Label(self, text="Generation Gap (as %)")
        generationGapLabel.grid(column=0, row=5, sticky=tk.N + tk.W)
        self.generationGapEntry = ttk.Entry(self, textvariable=self.generationGap)
        self.generationGapEntry.grid(column=1, row=5, sticky=tk.N + tk.W)

        self.mutationProbability = tk.StringVar()
        self.mutationProbability.set(0.001)
        mutationLabel = ttk.Label(self, text="Mutation Probability [0-1]")
        mutationLabel.grid(column=0, row=6, sticky=tk.N + tk.W)
        self.mutationEntry = ttk.Entry(self, textvariable=self.mutationProbability)
        self.mutationEntry.grid(column=1, row=6, sticky=tk.N + tk.W)

        selections = ["Roulette", "Tournament"]
        self.selection = tk.StringVar()
        selectionLabel = ttk.Label(self, text="Selection: ")
        selectionLabel.grid(column=0, row=7, sticky=tk.N + tk.W)
        self.selectionOption = ttk.OptionMenu(self, self.selection, selections[0], *selections)
        self.selectionOption.grid(column=1, row=7, sticky=tk.N + tk.W)

        terminations = ['Convergence', 'Reduction', 'Iteration']
        self.terminationType = tk.StringVar()
        terminationTypeLabel = ttk.Label(self, text="Termination Type:\t\t\t")
        terminationTypeLabel.grid(column=0, row=8, sticky=tk.N + tk.W)
        self.terminationOption = ttk.OptionMenu(self, self.terminationType, terminations[0], *terminations)
        self.terminationOption.grid(column=1, row=8, sticky=tk.N + tk.W)

        self.nextOptionsButton = ttk.Button(self, text="Next", command=lambda: self.nextOptions(controller))
        self.nextOptionsButton.grid(column=1, row=9, sticky=tk.N + tk.W)

        for child in self.winfo_children():
            child.grid_configure(padx=2, pady=4)

    def nextOptions(self, controller):
        self.nextOptionsButton.config(state=tk.DISABLED)
        self.representationOption.config(state=tk.DISABLED)
        self.populationEntry.config(state=tk.DISABLED)
        self.childPopulationEntry.config(state=tk.DISABLED)
        self.generationGapEntry.config(state=tk.DISABLED)
        self.mutationEntry.config(state=tk.DISABLED)
        self.selectionOption.config(state=tk.DISABLED)
        self.terminationOption.config(state=tk.DISABLED)

        mutations = ['Displacement', 'Exchange', 'Insertion', 'Inversion', 'Scramble', 'Simple Inversion']
        crossovers = ['Maximal Preservative', 'Partially Mapped', 'Position Based', 'Order', 'Order Based',
                      'Alternating Position', 'Cycle']

        if self.representation.get() == 'Binary':
            mutations = ['Classical']
            crossovers = ['Classical']
        elif self.representation.get() == 'Matrix':
            crossovers = ['Union', 'Intersection']

        if hasattr(self, 'mutationOption'):
            self.mutationOption.grid_forget()
            self.crossoverOption.grid_forget()

        self.mutationType = tk.StringVar()
        mutationTypeLabel = ttk.Label(self, text="Mutation Type:\t\t\t")
        mutationTypeLabel.grid(column=3, row=2, sticky=tk.N + tk.W)
        self.mutationOption = ttk.OptionMenu(self, self.mutationType, mutations[0], *mutations)
        self.mutationOption.grid(column=4, row=2, sticky=tk.N + tk.W)

        self.crossoverType = tk.StringVar()
        crossoverTypeLabel = ttk.Label(self, text="Crossover Type:\t\t\t")
        crossoverTypeLabel.grid(column=3, row=3, sticky=tk.N + tk.W)
        self.crossoverOption = ttk.OptionMenu(self, self.crossoverType, crossovers[0], *crossovers)
        self.crossoverOption.grid(column=4, row=3, sticky=tk.N + tk.W)

        self.tournamentSize = IntVar()
        self.tournamentSize.set(10)
        if hasattr(self, 'tournamentLabel'):
            self.tournamentLabel.grid_forget()
            self.tournamentEntry.grid_forget()

        self.selectionParam = tk.StringVar()
        if self.selection.get() == 'Tournament':
            selectionLabel = "Tournament Size (as %):"
            self.selectionParam.set(10)
        else:
            selectionLabel = "Roulette Selection:"
            self.selectionParam.set("N/A")

        self.tournamentLabel = ttk.Label(self, text=selectionLabel)
        self.tournamentLabel.grid(column=3, row=4, sticky=tk.N + tk.W)
        self.tournamentEntry = ttk.Entry(self, textvariable=self.selectionParam)
        self.tournamentEntry.grid(column=4, row=4, sticky=tk.N + tk.W)

        if hasattr(self, 'termParamLabel'):
            self.termParamLabel.grid_forget()

        termParamType = ''
        self.termParam = tk.StringVar()
        if self.terminationType.get() == 'Convergence':
            termParamType = 'Repeats for Convergence:'
            self.termParam.set(50)
        elif self.terminationType.get() == 'Reduction':
            termParamType = 'New Generation Size (as %):'
            self.termParam.set(99.9)
        elif self.terminationType.get() == 'Iteration':
            termParamType = 'Number of Iterations:'
            self.termParam.set(100)

        self.termParamLabel = ttk.Label(self, text=termParamType)
        self.termParamLabel.grid(column=3, row=5, sticky=tk.N + tk.W)
        self.termParamEntry = ttk.Entry(self, textvariable=self.termParam)
        self.termParamEntry.grid(column=4, row=5, sticky=tk.N + tk.W)

        runAlgorithmButton = ttk.Button(self, text="Run Algorithm",
                                        command=lambda: self.startAlgorithm(controller))
        runAlgorithmButton.grid(column=4, row=9, sticky=tk.N + tk.W)

        for child in self.winfo_children():
            child.grid_configure(padx=2, pady=4)

    def startAlgorithm(self, controller):
        global populationSize
        global childPopulationSizePercentage
        global generationalGapPercentage
        global mutationProbability
        global representation
        global selectionType
        global tournamentSize
        global crossoverType
        global mutationType
        global terminationType
        global iterations
        global reductionPercentage
        global convergenceNumber

        populationSize = self.populationSize.get()
        childPopulationSizePercentage = self.childPercentage.get()
        generationalGapPercentage = self.generationGap.get()
        mutationProbability = float(self.mutationProbability.get())
        representation = self.representation.get()
        selectionType = self.selection.get()
        tournamentSize = self.selectionParam.get()
        crossoverType = self.crossoverType.get()
        mutationType = self.mutationType.get()
        terminationType = self.terminationType.get()
        terminationParam = self.termParam.get()

        if terminationType == 'Convergence':
            convergenceNumber = terminationParam
        elif terminationType == 'Reduction':
            reductionPercentage = terminationParam
        elif terminationType == 'Iteration':
            iterations = terminationParam

        controller.showFrame(ProgressViewer)


class ProgressViewer(tk.Frame):
    def __init__(self, parent, controller):
        self.queue = None
        tk.Frame.__init__(self, parent)
        self.mapFigure = Figure(figsize=(5, 5), dpi=100)
        self.mapPlot = self.mapFigure.add_subplot(111)

        mainLabel = ttk.Label(self, text="Travelling Salesman Problem: Running Algorithm", font=fontLarge)
        mainLabel.grid(column=1, columnspan=3, row=0, sticky=tk.N + tk.W)

        algorithmLabel = ttk.Label(self, text="Algorithm Key: ")
        algorithmLabel.grid(column=1, row=2, sticky=tk.N + tk.W)

        originalSolutionLabel = ttk.Label(self, text="Original Solution Fitness: ")
        originalSolutionLabel.grid(column=1, row=3, sticky=tk.N + tk.W)

        self.bestSolutionLabel = ttk.Label(self, text="Best Fitness: ")
        self.bestSolutionLabel.grid(column=1, row=4, sticky=tk.N + tk.W)

        algorithmImprovementLabel = ttk.Label(self, text="Algorithm Improvement: ")
        algorithmImprovementLabel.grid(column=1, row=5, sticky=tk.N + tk.W)

        self.startButton = ttk.Button(self, text="Start", command=self.runAlgorithm)
        self.startButton.grid(column=1, row=6, sticky=tk.S + tk.W)

        finishButton = ttk.Button(self, text="Exit", command=controller.quit)
        finishButton.grid(column=2, row=20, sticky=tk.S + tk.W)

        self.canvas = FigureCanvasTkAgg(self.mapFigure, self)
        self.canvas.get_tk_widget().grid(column=5, row=1, sticky=tk.N + tk.W)
        self.canvas._tkcanvas.grid(column=5, row=0, rowspan=20, sticky=tk.N + tk.W)
        self.canvas.draw()

        toolbarFrame = tk.Frame(self)
        toolbarFrame.grid(column=5, row=21, sticky=tk.N + tk.W)
        NavigationToolbar2Tk(self.canvas, toolbarFrame)

        for child in self.winfo_children():
            child.grid_configure(padx=10, pady=4)

    def runAlgorithm(self):
        self.startButton.config(state=tk.DISABLED)
        self.queue = queue.Queue()
        ThreadedTask(self.queue).start()
        self.master.after(100, self.process_queue)

    def process_queue(self):
        try:
            msg = self.queue.get(0)
            if msg == "Original Solution":
                xyRoute = plotRoute(originalSolution)
                self.mapPlot.clear()
                self.mapPlot.plot(xyRoute[0],xyRoute[1])
                self.canvas.draw()
                self.master.after(100, self.process_queue)
            elif msg == "New Generation":
                xyRoute = plotRoute(bestSolution)
                self.mapPlot.clear()
                self.mapPlot.plot(xyRoute[0], xyRoute[1])
                self.canvas.draw()
                self.master.after(100, self.process_queue)

        except queue.Empty:
            self.master.after(100, self.process_queue)


class ThreadedTask(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        global originalPopulationWithFitness
        global originalSolution
        global originalPopulation
        originalPopulation = GenerateDataSet.generatePopulation(representation, numberOfCities, populationSize)
        originalPopulationWithFitness = fitnessFunction[representation](originalPopulation, xyCoords)
        originalSolution = self.findBestSolution(originalPopulationWithFitness)
        self.queue.put("Original Solution")

        if terminationType == 'Iteration':
            self.iterationTermination()
        elif terminationType == 'Reduction':
            self.reductionTermination()
        elif terminationType == 'Convergence':
            self.convergenceTermination()

        print(bestSolution)
        print(originalSolution)
        algorithmEfficiency = int((originalSolution[1] / bestSolution[1]) * 100) - 100


        # addDataToCsv(originalSolution[0], bestSolution[0], algorithmEfficiency)
        # updateDBfromCsv()




    def iterationTermination(self):
        global reductionPercentage
        reductionPercentage = 100
        populationWithFitness = originalPopulationWithFitness
        for i in range(iterations):
            populationWithFitness = self.createNewGeneration(populationWithFitness)
            self.queue.put("New Generation")
        bestSolution = self.findBestSolution(populationWithFitness)
        return bestSolution


    def reductionTermination(self):
        populationWithFitness = originalPopulationWithFitness
        count = len(populationWithFitness)
        while populationWithFitness:
            roundedPopulationCount = int(math.ceil(len(populationWithFitness) / 1000.0)) * 1000
            try:
                populationWithFitness = self.createNewGeneration(populationWithFitness)

                if roundedPopulationCount == count:
                    print('Population size = ' + str(count))
                    count -= 1000
                elif roundedPopulationCount < count:
                    count = roundedPopulationCount
                bestSolution = self.findBestSolution(populationWithFitness)
            except IndexError:
                break



    def convergenceTermination(self):
        global reductionPercentage
        global bestSolution
        reductionPercentage = 100
        populationWithFitness = originalPopulationWithFitness
        count = 0
        currentBest = math.inf
        while count < int(convergenceNumber):
            print(count)
            populationWithFitness = self.createNewGeneration(populationWithFitness)
            bestSolution = self.findBestSolution(populationWithFitness)

            if bestSolution[1] < currentBest:
                currentBest = bestSolution[1]
                count = 0
                self.queue.put("New Generation")
            else:
                count += 1
                self.queue.put("New Generation")


    def createNewGeneration(self, populationWithFitness):
        if selectionType == 'Roulette':
            childPopulation = Selection.rouletteSelection(populationWithFitness,
                                                          childPopulationSizePercentage)
        elif selectionType == 'Tournament':
            childPopulation = Selection.tournamentSelection(populationWithFitness, tournamentSize,
                                                            childPopulationSizePercentage)
        childPopulation = representations[representation].runCrossover(crossoverType, childPopulation)
        childPopulation = representations[representation].runMutation(mutationType, childPopulation, mutationProbability)
        if representation == 'Binary':
            childPopulation = representations[representation].runRepair(childPopulation)
        childPopulationWithFitness = fitnessFunction[representation](childPopulation, xyCoords)
        newGeneration = Replacement.generationalReplacement(populationWithFitness,
                                                            childPopulationWithFitness,
                                                            generationalGapPercentage,
                                                            reductionPercentage)
        return newGeneration


    def findBestSolution(self, populationWithFitness):
        sortedPopulation = sorted(populationWithFitness, key=itemgetter(1))
        bestSolution = sortedPopulation[0]
        return bestSolution

def plotRoute(solution):
    global representation
    global xyCoords
    if representation == 'Matrix':
        solution[0] = MatrixOperators.convertMatrixToTour(solution[0])
        representation = 'Path'
    solution[0].append(solution[0][0])
    xySolution = []
    for i in range(0, len(solution[0])):
        if representation == 'Binary':
            cityInt = int(solution[0][i], 2)
        elif representation == 'Path':
            cityInt = int(solution[0][i])
        else:
            print(representation + ': is not a valid representation')
            sys.exit()
        xySolution.append(xyCoords[cityInt - 1])

    unzippedXy = list(zip(*xySolution))
    return unzippedXy




app = tspInterface()
app.eval('tk::PlaceWindow %s center' % app.winfo_pathname(app.winfo_id()))
app.mainloop()
