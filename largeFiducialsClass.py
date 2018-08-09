import numpy
import matplotlib
import matplotlib.pyplot as pyplot
import clearingFunction

class largeFiducialsPositionList:
    def __init__(self, dataSet):
        self.Pos = dataSet

    def __add__(self, other):
        numOfPoints = len(self.Pos)
        newPositionList = [[self.Pos[i][0] + other.Pos[i][0], self.Pos[i][1] + other.Pos[i][1]] for i in range(numOfPoints)]
        return largeFiducialsPositionList(newPositionList)

    def __sub__(self, other):
        numOfPoints = len(self.Pos)
        newPositionList = [[self.Pos[i][0] - other.Pos[i][0], self.Pos[i][1] - other.Pos[i][1]] for i in range(numOfPoints)]
        return largeFiducialsPositionList(newPositionList)

class largeFiducialDataSet:
    def __init__(self, dataSet):
        self.CAD = largeFiducialsPositionList(dataSet[0])
        self.realPos = largeFiducialsPositionList(dataSet[1])
        self.offsets = self.realPos - self.CAD
        self.CADX = [item[0] for item in self.CAD.Pos]
        self.CADXLowY = []
        self.CADXHighY = []
        self.offsetsLowY = []
        self.offsetsHighY = []

        for i in range(len(self.CADX)):
            if self.CAD.Pos[i][1] < 0.05:
                self.CADXLowY.append(self.CADX[i])
                self.offsetsLowY.append(self.offsets.Pos[i])
            else:
                self.CADXHighY.append(self.CADX[i])
                self.offsetsHighY.append(self.offsets.Pos[i])

        self.fitLowY = [numpy.polyfit(self.CADXLowY, [item[0] for item in self.offsetsLowY], 1), numpy.polyfit(self.CADXLowY, [item[1] for item in self.offsetsLowY], 3)]
        self.fitHighY = [numpy.polyfit(self.CADXHighY, [item[0] for item in self.offsetsHighY], 1), numpy.polyfit(self.CADXHighY, [item[1] for item in self.offsetsHighY], 3)]

        self.predOffsetLowY = [[numpy.polyval(self.fitLowY[0], x), numpy.polyval(self.fitLowY[1], x)] for x in self.CADXLowY]
        self.predOffsetHighY = [[numpy.polyval(self.fitHighY[0], x), numpy.polyval(self.fitHighY[1], x)] for x in self.CADXHighY]

        self.residualsLowY = largeFiducialsPositionList(self.offsetsLowY) - largeFiducialsPositionList(self.predOffsetLowY)
        self.residualsHighY = largeFiducialsPositionList(self.offsetsHighY) - largeFiducialsPositionList(self.predOffsetHighY)
        self.residualsCombined = self.residualsLowY.Pos + self.residualsHighY.Pos
        self.CADXCombined = self.CADXLowY + self.CADXHighY

    def plotOffsets(self, coordinate):
        if coordinate == 'Y':
            yDataLowY = [item[1]*10**6 for item in self.offsetsLowY]
            yDataHighY = [item[1]*10**6 for item in self.offsetsHighY]
            yDataPredLowY = [item[1]*10**6 for item in self.predOffsetLowY]
            yDataPredHighY = [item[1]*10**6 for item in self.predOffsetHighY]
        else:
            yDataLowY = [item[0]*10**6 for item in self.offsetsLowY]
            yDataHighY = [item[0]*10**6 for item in self.offsetsHighY]
            yDataPredLowY = [item[0]*10**6 for item in self.predOffsetLowY]
            yDataPredHighY = [item[0]*10**6 for item in self.predOffsetHighY]

        pyplot.subplot(211)
        pyplot.xlabel('CADX/meters')
        pyplot.ylabel(coordinate + ' offsets(Low Y)/micrometers')
        pyplot.plot(self.CADXLowY, yDataLowY, 'k.')
        pyplot.plot(self.CADXLowY, yDataPredLowY)

        pyplot.subplot(212)
        pyplot.xlabel('CADX/meters')
        pyplot.ylabel(coordinate + ' offsets(High Y)/micrometers')
        pyplot.plot(self.CADXLowY, yDataHighY, 'k.')
        pyplot.plot(self.CADXHighY, yDataPredHighY)

        pyplot.show()

    def plotMenu(self):
        notDone = True

        while notDone:
            clearingFunction.clear()
            print('0: plot Y')
            print('1: plot X')
            print("Input 'back' to go back")

            userInput = str(input())
            if userInput == '0':
                self.plotOffsets('Y')
            elif userInput == '1':
                self.plotOffsets('X')
            elif userInput == 'back':
                notDone = False

    def plotResiduals(self, coordinate):
        if coordinate == 'Y':
            yData = [item[1]*10**6 for item in self.residualsCombined]
        else:
            yData = [item[0]*10**6 for item in self.residualsCombined]

        pyplot.plot(self.CADXCombined, yData, 'k.')
