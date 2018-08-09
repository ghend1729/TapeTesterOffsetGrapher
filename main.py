import os
import numpy
import matplotlib
import matplotlib.pyplot as pyplot
from clearingFunction import *
import fullDataSetClass
import offsetSpreadClass
import TapeCallibrationClass

tapeCalObjects = [TapeCallibrationClass.TapeCallibration(item) for item in os.listdir('fullReportData')]

dataSetFileNames = os.listdir("DataSetFiles")

print("Data files found:")

#i stores the index of the file name without a tick number.
i = 0

for j, item in enumerate(dataSetFileNames):
    print(item)
    if len(item) < 15:
        i = j

numberedFiles = dataSetFileNames[:i] + dataSetFileNames[(i+1):]

numberedFiles = sorted(numberedFiles, key = lambda fileName: int(fileName[10:-5]))

timeOrderedFiles = [dataSetFileNames[i]] + numberedFiles

dataSets = [fullDataSetClass.fullDataSet("DataSetFiles/" + fileName) for fileName in timeOrderedFiles]
offsetSpreadAnalyseObject = offsetSpreadClass.offsetSpreadAnalyse(dataSets)

largeFiducialResidHistY = []
largeFiducialResidHistX = []

for fiducialDataSet in tapeCalObjects[1].largeFiducialObjects:
    largeFiducialResidHistY += [item[1]*10**6 for item in fiducialDataSet.residualsCombined]
    largeFiducialResidHistX += [item[0]*10**6 for item in fiducialDataSet.residualsCombined]

def mainMenu():
    notDone = True

    while notDone:
        clear()
        print('------------------Main Menu------------------')
        print('Input the number for correct option.')
        print("To exit just input 'exit'.")
        print('0: Look at graphs for a particular data file.')
        print('1: Look at spread in offset for each fiducial')
        print('individually.')
        print('2: Show a histogram offets for spread around')
        print('3: Graph mean offset.')
        print('4: Look at large fiducial data')
        print('5: plot all residuals for large fiducial fits')
        print('6: plot histogram for large fiducial residuals')
        print('7: hidden data dump')
        print('their mean.')

        userInput = str(input())
        if userInput == 'exit':
            notDone = False
            clear()
        elif userInput == '0':
            graphParticularDataFile()
        elif userInput == '1':
            offsetSpreadAnalyseObject.graphIndividualMune()
        elif userInput == '2':
            offsetSpreadAnalyseObject.graphHistogramMenu()
        elif userInput[0] == '3':
            graphMeanOffset('stage ' + userInput[2], userInput[4])
        elif userInput == '4':
            selectTape()
        elif userInput == '5':
            masterResidualPlotsLargeFiducials()
        elif userInput == '6':
            plotLargeFidResidHist()
        elif userInput == '7':
            dataDump()


def graphParticularDataFile():
    notDone = True

    while notDone:
        clear()
        print('---------Graph particular Data File----------')
        print('Input the number for the file you want to see.')
        print("Input 'back' to go back.")
        for i in range(len(dataSets)):
            print(str(i) + ': ' + dataSets[i].dataFileName)

        userInput = str(input())
        if userInput == 'back':
            notDone = False
        else:
            dataSets[int(userInput)].runPlottingLoop()

def graphMeanOffset(stage, coordinate):
    if coordinate == 'Y':
        if stage == 'stage 1':
            vertical = [numpy.mean(item.fiducialsDataSide1.yOffsetsStage1 + item.fiducialsDataSide2.yOffsetsStage1) for item in dataSets]
        else:
            vertical = [numpy.mean(item.fiducialsDataSide1.yOffsetsStage2 + item.fiducialsDataSide2.yOffsetsStage2) for item in dataSets]
    else:
        if stage == 'stage 1':
            vertical = [numpy.mean(item.fiducialsDataSide1.xOffsetsStage1 + item.fiducialsDataSide2.xOffsetsStage1) for item in dataSets]
        else:
            vertical = [numpy.mean(item.fiducialsDataSide1.xOffsetsStage2 + item.fiducialsDataSide2.xOffsetsStage2) for item in dataSets]


    vertical = [item*10**6 for item in vertical]

    pyplot.xlabel("Scan number")
    pyplot.ylabel("Mean offset/micrometers")
    pyplot.plot(vertical)

    pyplot.show()

def dataDump():
    xCad = dataSets[2].fiducialsDataSide1.xPositionList + dataSets[2].fiducialsDataSide2.xPositionList
    offsetDataX = dataSets[2].fiducialsDataSide1.xOffsetsStage1 + dataSets[2].fiducialsDataSide2.xOffsetsStage1
    offsetDataY = dataSets[2].fiducialsDataSide1.yOffsetsStage1 + dataSets[2].fiducialsDataSide2.yOffsetsStage1
    dataCombined = [[xCad[i], offsetDataX[i], offsetDataY[i]] for i in range(len(xCad))]
    for item in dataCombined:
        print(item)

def selectTape():
    notDone = True
    while notDone:
        clear()
        print('-----------------Select Tape-----------------')
        for i, tape in enumerate(tapeCalObjects):
            print(str(i) + ': tape ' + tape.serialNumber)
        print("Input 'back' to go back.")

        userInput = str(input())
        if userInput == 'back':
            notDone = False
        else:
            tapeCalObjects[int(userInput)].plotSelect()


def masterResidualPlotsLargeFiducials():
    pyplot.subplot(211)
    pyplot.xlabel('CADX/meters')
    pyplot.ylabel('Y residuals/micrometers')
    for tape in tapeCalObjects:
        for fiducialDataSet in tape.largeFiducialObjects:
            fiducialDataSet.plotResiduals('Y')

    pyplot.subplot(212)
    pyplot.xlabel('CADX/meters')
    pyplot.ylabel('X residuals/micrometers')
    for tape in tapeCalObjects:
        for fiducialDataSet in tape.largeFiducialObjects:
            fiducialDataSet.plotResiduals('X')

    pyplot.show()

def plotLargeFidResidHist():
    pyplot.subplot(211)
    pyplot.xlabel('Y residual/micrometers')
    pyplot.ylabel('Normalised density')
    pyplot.hist(largeFiducialResidHistY, density = True)

    pyplot.subplot(212)
    pyplot.xlabel('X residual/micrometers')
    pyplot.ylabel('Normalised density')
    pyplot.hist(largeFiducialResidHistX, density = True)

    pyplot.show()

mainMenu()
