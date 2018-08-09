import numpy
import os
import matplotlib
import matplotlib.pyplot as pyplot
import clearingFunction
import largeFiducialsClass

class TapeCallibration:
    def __init__(self, folderName):
        self.serialNumber = folderName[-2:]
        self.callibrationData = []

        dataFolders = [dI for dI in os.listdir('fullReportData/' + folderName) if os.path.isdir(os.path.join('fullReportData/' + folderName, dI))]

        for folder in dataFolders:
            self.callibrationData.append(self.loadCallibrationDataFromFile('fullReportData/' + folderName + '/' + folder))

        numberOfFiducials = len(self.callibrationData[0][1])
        numberOfDataSets = len(self.callibrationData)

        xPos = [[item[1][i][0]*10**6 for item in self.callibrationData] for i in range(numberOfFiducials)]
        yPos = [[item[1][i][1]*10**6 for item in self.callibrationData] for i in range(numberOfFiducials)]

        self.rmsPos = [[numpy.std(xPos[i]), numpy.std(yPos[i])] for i in range(numberOfFiducials)]
        self.means = [[numpy.mean(xPos[i]), numpy.mean(yPos[i])] for i in range(numberOfFiducials)]
        self.spreads = [[[xPos[i][j] - self.means[i][0], yPos[i][j] - self.means[i][1]] for i in range(numberOfFiducials)] for j in range(numberOfDataSets)]
        self.CAD = self.callibrationData[0][0]

        self.largeFiducialObjects = [largeFiducialsClass.largeFiducialDataSet(item) for item in self.callibrationData]

        for item in self.rmsPos:
            print(item)

        for dataSet in self.callibrationData:
            print()
            for part in dataSet:
                print()
                for item in part:
                    print(item)

    def loadCallibrationDataFromFile(self, dataFolder):
        dataFile = open(dataFolder + "/Measurement Report.txt", 'r')

        CAD = []
        measuredPositions = []

        gotCAD = False
        gotPos = False
        loadingCAD = False
        loadingPos = False
        loadData = False
        reading = True

        while reading:
            loadedLine = dataFile.readline()

            if loadData:
                if loadedLine[0] == '-':
                    if loadingPos:
                        reading = False

                    loadData = False
                    loadingCAD = False
                    loadingPos = False
                elif loadingCAD:
                    splitLine = loadedLine.split('=')
                    CAD.append([float(splitLine[1][:-3]), float(splitLine[2])])
                elif loadingPos:
                    splitLine = loadedLine.split('=')
                    measuredPositions.append([float(splitLine[1][:-2]), float(splitLine[2])])
            elif loadedLine[:3] == 'CAD':
                loadingCAD = True
            elif loadedLine[:18] == 'Measured positions':
                loadingPos = True
            elif (loadedLine[0] == '-') and (loadingCAD or loadingPos):
                loadData = True


        dataFile.close()
        return [CAD, measuredPositions]

    def plotRMSasFunctionOfXCAD(self, coordinate):
        horizontal = [item[0] for item in self.CAD]

        if coordinate == 'Y':
            vertical = [item[1] for item in self.rmsPos]
        else:
            vertical = [item[0] for item in self.rmsPos]

        pyplot.xlabel("XCAD/meters")
        pyplot.ylabel(coordinate + " rms position/micrometers")
        pyplot.plot(horizontal, vertical, 'k.')

        pyplot.show()

    def plotSelect(self):
        notDone = True

        while notDone:
            clearingFunction.clear()
            print('Tape ' + self.serialNumber)
            print('Select a plot.')
            print('0: Y rms offsets as function of CADX')
            print('1: X rms offsets as function of CADX')
            print('2: Y histogram of rms offsets')
            print('3: X histogram of rms offsets')
            print('4: Y spreads about mean as function of XCAD')
            print('5: X spreads about mean as function of XCAD')
            print('6: Y spreads about mean histogram')
            print('7: X spreads about mean histogram')
            print('8: look at individual offsets')
            print("Input 'back' to go back.")

            userInput = str(input())

            if userInput == 'back':
                notDone = False
            elif userInput == '0':
                self.plotRMSasFunctionOfXCAD('Y')
            elif userInput == '1':
                self.plotRMSasFunctionOfXCAD('X')
            elif userInput == '2':
                self.plotHistogram('Y')
            elif userInput == '3':
                self.plotHistogram('X')
            elif userInput == '4':
                self.plotSpreads('Y')
            elif userInput == '5':
                self.plotSpreads('X')
            elif userInput == '6':
                self.plotHistogramOfSpreads('Y')
            elif userInput == '7':
                self.plotHistogramOfSpreads('X')
            elif userInput == '8':
                self.pickDataSetToPlot()

    def plotHistogram(self, coordinate):
        if coordinate == 'Y':
            histData = [item[1] for item in self.rmsPos]
        else:
            histData = [item[0] for item in self.rmsPos]

        pyplot.xlabel(coordinate + ' rms position/micrometers')
        pyplot.ylabel('Normalised density')
        pyplot.hist(histData, density = True)
        pyplot.show()

    def plotSpreads(self, coordinate):
        horizontal = [item[0] for item in self.CAD]

        if coordinate == 'Y':
            coordIndex = 1
        else:
            coordIndex = 0

        pyplot.xlabel("XCAD/meters")
        pyplot.ylabel(coordinate + " spread about mean position/micrometers")
        for dataSet in self.spreads:
            pyplot.plot(horizontal, [point[coordIndex] for point in dataSet], 'k.')

        pyplot.show()

    def plotHistogramOfSpreads(self, coordinate):
        dataList = []
        if coordinate == 'Y':
            coordIndex = 1
        else:
            coordIndex = 0

        for dataSet in self.spreads:
            dataList += [point[coordIndex] for point in dataSet]

        pyplot.xlabel(coordinate + ' difference from mean position/micrometers')
        pyplot.ylabel('Normalised density')
        pyplot.hist(dataList, density = True)
        pyplot.show()

    def pickDataSetToPlot(self):
        numberOfDataSets = len(self.largeFiducialObjects)

        notDone = True

        while notDone:
            clearingFunction.clear()
            print('Input the index of data set of interest.')
            print('This number cannot be larger than: ' + str(numberOfDataSets))
            print("Input 'back' to go back")

            userInput = str(input())
            if userInput == 'back':
                notDone = False
            else:
                self.largeFiducialObjects[int(userInput)].plotMenu()
