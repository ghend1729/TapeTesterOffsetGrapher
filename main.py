import os
from clearingFunction import *
import fullDataSetClass
import offsetSpreadClass

dataSets = [fullDataSetClass.fullDataSet("DataSetFiles/" + fileName) for fileName in os.listdir("DataSetFiles")]
offsetSpreadAnalyseObject = offsetSpreadClass.offsetSpreadAnalyse(dataSets)

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
        print('their mean.')

        userInput = input()
        if userInput == 'exit':
            notDone = False
        elif userInput == '0':
            graphParticularDataFile()
        elif userInput == '1':
            offsetSpreadAnalyseObject.graphDifferenceFromMeanAsFunctionOfXCad('Y')

def graphParticularDataFile():
    notDone = True

    while notDone:
        clear()
        print('---------Graph particular Data File----------')
        print('Input the number for the file you want to see.')
        print("Input 'back' to go back.")
        for i in range(len(dataSets)):
            print(str(i) + ': ' + dataSets[i].dataFileName)

        userInput = input()
        if userInput == 'back':
            notDone = False
        else:
            dataSets[int(userInput)].runPlottingLoop()

mainMenu()
