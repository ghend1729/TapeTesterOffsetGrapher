import matplotlib
import matplotlib.pyplot as pyplot
import numpy
import clearingFunction

class spreadStorer:
    XCad = []
    offsets = []
    means = []
    spreads = []

    def __init__(self, offsetsSide1, offsetsSide2, offsetPredictedSide1, offsetPredictedSide2):
        self.offsets = offsetsSide1 + offsetsSide2
        self.offsetsPredicted = offsetPredictedSide1 + offsetPredictedSide2
        self.means = [numpy.mean(offsetSet) for offsetSet in self.offsets]
        self.spreads = [[offset - self.means[i] for offset in self.offsets[i]] for i in range(len(self.offsets))]
        self.residuals = [[self.offsets[i][j] - self.offsetsPredicted[i][j] for j in range(len(self.offsets[i]))] for i in range(len(self.offsets))]


class offsetSpreadAnalyse:
    def __init__(self, dataSets):
        lenSide1 = len(dataSets[0].fiducialsDataSide1.xPositionList)
        lenSide2 = len(dataSets[0].fiducialsDataSide2.xPositionList)
        self.numberOfDataSets = len(dataSets)
        self.XCad = dataSets[0].fiducialsDataSide1.xPositionList + dataSets[0].fiducialsDataSide2.xPositionList
        self.yOffsetsStage1 = spreadStorer([[item.fiducialsDataSide1.yOffsetsStage1[i] for item in dataSets] for i in range(lenSide1)], [[item.fiducialsDataSide2.yOffsetsStage1[i] for item in dataSets] for i in range(lenSide2)], [[item.fiducialsDataSide1.predictedYOffsetsStage1[i] for item in dataSets] for i in range(lenSide1)], [[item.fiducialsDataSide2.predictedYOffsetsStage1[i] for item in dataSets] for i in range(lenSide2)])
        self.yOffsetsStage2 = spreadStorer([[item.fiducialsDataSide1.yOffsetsStage2[i] for item in dataSets] for i in range(lenSide1)], [[item.fiducialsDataSide2.yOffsetsStage2[i] for item in dataSets] for i in range(lenSide2)], [[item.fiducialsDataSide1.predictedYOffsetsStage2[i] for item in dataSets] for i in range(lenSide1)], [[item.fiducialsDataSide2.predictedYOffsetsStage2[i] for item in dataSets] for i in range(lenSide2)])
        self.xOffsetsStage1 = spreadStorer([[item.fiducialsDataSide1.xOffsetsStage1[i] for item in dataSets] for i in range(lenSide1)], [[item.fiducialsDataSide2.xOffsetsStage1[i] for item in dataSets] for i in range(lenSide2)], [[item.fiducialsDataSide1.predictedXOffsetsStage1[i] for item in dataSets] for i in range(lenSide1)], [[item.fiducialsDataSide2.predictedXOffsetsStage1[i] for item in dataSets] for i in range(lenSide2)])
        self.xOffsetsStage2 = spreadStorer([[item.fiducialsDataSide1.xOffsetsStage2[i] for item in dataSets] for i in range(lenSide1)], [[item.fiducialsDataSide2.xOffsetsStage2[i] for item in dataSets] for i in range(lenSide2)], [[item.fiducialsDataSide1.predictedXOffsetsStage2[i] for item in dataSets] for i in range(lenSide1)], [[item.fiducialsDataSide2.predictedXOffsetsStage2[i] for item in dataSets] for i in range(lenSide2)])

        self.yOffsetsStage1HistorgramData = self.generateHistogramData(self.yOffsetsStage1.spreads)
        self.yOffsetsStage2HistorgramData = self.generateHistogramData(self.yOffsetsStage2.spreads)
        self.xOffsetsStage1HistorgramData = self.generateHistogramData(self.xOffsetsStage1.spreads)
        self.xOffsetsStage2HistorgramData = self.generateHistogramData(self.xOffsetsStage2.spreads)
        self.yOffsetsResidStage1HistorgramData = self.generateHistogramData(self.yOffsetsStage1.residuals)
        self.yOffsetsResidStage2HistorgramData = self.generateHistogramData(self.yOffsetsStage2.residuals)
        self.xOffsetsResidStage1HistorgramData = self.generateHistogramData(self.xOffsetsStage1.residuals)
        self.xOffsetsResidStage2HistorgramData = self.generateHistogramData(self.xOffsetsStage2.residuals)

    def generateHistogramData(self, dataList):
        result = []

        for spreadSet in dataList:
            result += spreadSet

        return result

    def graphDifferenceFromMeanAsFunctionOfXCad(self, coordinate, useFitResid=False):
        xData = self.XCad

        if not useFitResid:
            graphLabel = " offsets spread "
            if coordinate == 'X':
                DataListStage1 = [[item[i]*10**6 for item in self.xOffsetsStage1.spreads] for i in range(self.numberOfDataSets)]
                DataListStage2 = [[item[i]*10**6 for item in self.xOffsetsStage2.spreads] for i in range(self.numberOfDataSets)]
            else:
                DataListStage1 = [[item[i]*10**6 for item in self.yOffsetsStage1.spreads] for i in range(self.numberOfDataSets)]
                DataListStage2 = [[item[i]*10**6 for item in self.yOffsetsStage2.spreads] for i in range(self.numberOfDataSets)]
        else:
            graphLabel = " offsets residuals "
            if coordinate == 'X':
                DataListStage1 = [[item[i]*10**6 for item in self.xOffsetsStage1.residuals] for i in range(self.numberOfDataSets)]
                DataListStage2 = [[item[i]*10**6 for item in self.xOffsetsStage2.residuals] for i in range(self.numberOfDataSets)]
            else:
                DataListStage1 = [[item[i]*10**6 for item in self.yOffsetsStage1.residuals] for i in range(self.numberOfDataSets)]
                DataListStage2 = [[item[i]*10**6 for item in self.yOffsetsStage2.residuals] for i in range(self.numberOfDataSets)]

        for item in DataListStage1:
            for i in range(len(item)):
                if abs(item[i]) > 100:
                    print("Residual from fit: " + str(item[i]) + " micrometers")
                    print("At CADX: " + str(xData[i]) + " meters")

        pyplot.subplot(211)
        pyplot.xlabel("X CAD position/meters")
        pyplot.ylabel(coordinate + graphLabel + "(stage1)/micrometers")
        for yData in DataListStage1:
            pyplot.plot(xData, yData, 'k.')


        pyplot.subplot(212)
        pyplot.xlabel("X CAD position/meters")
        pyplot.ylabel(coordinate + graphLabel + "(stage2)/micrometers")
        for yData in DataListStage2:
            pyplot.plot(xData, yData, 'k.')

        pyplot.show()

    def graphIndividualMune(self):
        notDone = True

        while notDone:
            clearingFunction.clear()

            print('----------Plot Individual spreads------------')
            print('Input the number for correct option.')
            print('0: Looks at the spreads in X offsets.')
            print('1: Looks at the spreads in Y offsets.')
            print('2: Looks at the residuals in X offsets.')
            print('3: Looks at the residuals in Y offsets.')
            print("Input 'back' to go back.")

            userInput = input()
            if userInput == '0':
                self.graphDifferenceFromMeanAsFunctionOfXCad('X')
            elif userInput == '1':
                self.graphDifferenceFromMeanAsFunctionOfXCad('Y')
            elif userInput == 'back':
                notDone = False
            elif userInput == '2':
                self.graphDifferenceFromMeanAsFunctionOfXCad('X', True)
            elif userInput == '3':
                self.graphDifferenceFromMeanAsFunctionOfXCad('Y', True)

    def plotHistogram(self, coordinate, useFitResid=False):
        if not useFitResid:
            graphLabel = " offsets spread "
            if coordinate == 'X':
                DataListStage1 = self.xOffsetsStage1HistorgramData
                DataListStage2 = self.xOffsetsStage2HistorgramData
            else:
                DataListStage1 = self.yOffsetsStage1HistorgramData
                DataListStage2 = self.yOffsetsStage2HistorgramData
        else:
            graphLabel = " offsets residuals "
            if coordinate == 'X':
                DataListStage1 = self.xOffsetsResidStage1HistorgramData
                DataListStage2 = self.xOffsetsResidStage2HistorgramData
            else:
                DataListStage1 = self.yOffsetsResidStage1HistorgramData
                DataListStage2 = self.yOffsetsResidStage2HistorgramData

        DataListStage1 = [item*10**6 for item in DataListStage1]
        DataListStage2 = [item*10**6 for item in DataListStage2]

        pyplot.subplot(211)
        pyplot.ylabel("Normalised Density")
        pyplot.xlabel(coordinate + graphLabel + "(stage1)/micrometers")
        pyplot.hist(DataListStage1, density = True)

        pyplot.subplot(212)
        pyplot.ylabel("Normalised Density")
        pyplot.xlabel(coordinate + graphLabel + "(stage2)/micrometers")
        pyplot.hist(DataListStage2, density = True)

        pyplot.show()

    def graphHistogramMenu(self):
        notDone = True

        while notDone:
            clearingFunction.clear()

            print('------------Histogram Plotting---------------')
            print('Input the number for correct option.')
            print('0: Looks at the spreads in X offsets.')
            print('1: Looks at the spreads in Y offsets.')
            print('2: Looks at the residuals in X offsets.')
            print('3: Looks at the residuals in Y offsets.')
            print("Input 'back' to go back.")

            userInput = input()
            if userInput == '0':
                self.plotHistogram('X')
            elif userInput == '1':
                self.plotHistogram('Y')
            elif userInput == '2':
                self.plotHistogram('X', True)
            elif userInput == '3':
                self.plotHistogram('Y', True)
            elif userInput == 'back':
                notDone = False
