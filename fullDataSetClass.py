import matplotlib
import matplotlib.pyplot as pyplot
import csv
import fiducialClasses
import clearingFunction

class fullDataSet:
    def __init__(self, fileName):
        print("loading data...")

        fiducialsSide1 = []
        fiducialsSide2 = []

        with open(fileName) as csvfile:
            self.dataFileName = fileName[13:]
            rawData = csv.reader(csvfile)
            dataValues = []
            for row in rawData:
                row = row[:-1]
                dataValues = [float(value) for value in row]
                print(dataValues)

                if dataValues[1] < 0.05:
                    fiducialsSide1.append(fiducialClasses.fiducial(dataValues))
                else:
                    fiducialsSide2.append(fiducialClasses.fiducial(dataValues))

        self.fiducialsDataSide1 = fiducialClasses.fiducials(fiducialsSide1)
        self.fiducialsDataSide2 = fiducialClasses.fiducials(fiducialsSide2)

        print("Load complete.")

    def runPlottingLoop(self):
        #Menu for running plotting options
        notDone = True
        while notDone:
            clearingFunction.clear()
            print("Data file: " + self.dataFileName)
            print("Input the number for desired plot (details below).")
            print("0: Plot stage 1 y offsets as function of CAD x position")
            print("1: Plot stage 2 y offsets as function of CAD x position")
            print("2: Plot stage 1 x offsets as function of CAD x position")
            print("3: Plot stage 2 x offsets as function of CAD x position")
            print("4: Plot stage 1 offsets y against x offsets")
            print("5: Plot stage 2 offsets y against x offsets")
            print("6: Plot stage 1 y offsets residuals as function of CAD x position")
            print("7: Plot stage 2 y offsets residuals as function of CAD x position")
            print("8: Plot stage 1 x offsets residuals as function of CAD x position")
            print("9: Plot stage 2 x offsets residuals as function of CAD x position")
            print("Input 'back' to go back.")

            userInput = str(input())
            if userInput == "0":
                self.plotOffsets('stage 1', 'Y')
            elif userInput == "1":
                self.plotOffsets('stage 2', 'Y')
            elif userInput == "2":
                self.plotOffsets('stage 1', 'X')
            elif userInput == "3":
                self.plotOffsets('stage 2', 'X')
            elif userInput == '4':
                self.plotOffsetAgainstOffset('stage 1')
            elif userInput == '5':
                self.plotOffsetAgainstOffset('stage 2')
            elif userInput == "6":
                self.plotResiduals('stage 1', 'Y')
            elif userInput == "7":
                self.plotResiduals('stage 2', 'Y')
            elif userInput == "8":
                self.plotResiduals('stage 1', 'X')
            elif userInput == "9":
                self.plotResiduals('stage 2', 'X')
            elif userInput == "back":
                notDone = False
            else:
                print("Invalid input!")

    def plotOffsets(self, stage, coordinate):
        horizontalSide1 = self.fiducialsDataSide1.xPositionList
        horizontalSide2 = self.fiducialsDataSide2.xPositionList

        if coordinate == 'Y':
            if stage == 'stage 1':
                verticalSide1 = self.fiducialsDataSide1.yOffsetsStage1
                verticalSide2 = self.fiducialsDataSide2.yOffsetsStage1
                predVerticalSide1 = self.fiducialsDataSide1.predictedYOffsetsStage1
                predVerticalSide2 = self.fiducialsDataSide2.predictedYOffsetsStage1
            else:
                verticalSide1 = self.fiducialsDataSide1.yOffsetsStage2
                verticalSide2 = self.fiducialsDataSide2.yOffsetsStage2
                predVerticalSide1 = self.fiducialsDataSide1.predictedYOffsetsStage2
                predVerticalSide2 = self.fiducialsDataSide2.predictedYOffsetsStage2
        else:
            if stage == 'stage 1':
                verticalSide1 = self.fiducialsDataSide1.xOffsetsStage1
                verticalSide2 = self.fiducialsDataSide2.xOffsetsStage1
                predVerticalSide1 = self.fiducialsDataSide1.predictedXOffsetsStage1
                predVerticalSide2 = self.fiducialsDataSide2.predictedXOffsetsStage1
            else:
                verticalSide1 = self.fiducialsDataSide1.xOffsetsStage2
                verticalSide2 = self.fiducialsDataSide2.xOffsetsStage2
                predVerticalSide1 = self.fiducialsDataSide1.predictedXOffsetsStage2
                predVerticalSide2 = self.fiducialsDataSide2.predictedXOffsetsStage2

        verticalSide1 = [item*10**6 for item in verticalSide1]
        verticalSide2 = [item*10**6 for item in verticalSide2]
        predVerticalSide1 = [item*10**6 for item in predVerticalSide1]
        predVerticalSide2 = [item*10**6 for item in predVerticalSide2]

        pyplot.subplot(211)
        pyplot.xlabel("X CAD position/meters")
        pyplot.ylabel(coordinate + " offsets (low Y)/micrometers")
        pyplot.plot(horizontalSide1, verticalSide1, 'k.')
        pyplot.plot(horizontalSide1, predVerticalSide1)

        pyplot.subplot(212)
        pyplot.xlabel("X CAD position/meters")
        pyplot.ylabel(coordinate + " offsets (high Y)/micrometers")
        pyplot.plot(horizontalSide2, verticalSide2, 'k.')
        pyplot.plot(horizontalSide2, predVerticalSide2)

        pyplot.show()

    def plotOffsetAgainstOffset(self, stage):
        if stage == '1':
            horizontalSide1 = self.fiducialsDataSide1.xOffsetsStage1
            verticalSide1 = self.fiducialsDataSide1.yOffsetsStage1
            horizontalSide2 = self.fiducialsDataSide2.xOffsetsStage1
            verticalSide2 = self.fiducialsDataSide2.yOffsetsStage1
        else:
            horizontalSide1 = self.fiducialsDataSide1.xOffsetsStage2
            verticalSide1 = self.fiducialsDataSide1.yOffsetsStage2
            horizontalSide2 = self.fiducialsDataSide2.xOffsetsStage2
            verticalSide2 = self.fiducialsDataSide2.yOffsetsStage2

        verticalSide1 = [item*10**6 for item in verticalSide1]
        verticalSide2 = [item*10**6 for item in verticalSide2]

        pyplot.subplot(211)
        pyplot.xlabel("X offsets (low Y)/micrometers")
        pyplot.ylabel("Y offsets (low Y)/micrometers")
        pyplot.plot(horizontalSide1, verticalSide1, 'k.')

        pyplot.subplot(212)
        pyplot.xlabel("X offsets (high Y)/micrometers")
        pyplot.ylabel("Y offsets (high Y)/micrometers")
        pyplot.plot(horizontalSide2, verticalSide2, 'k.')

        pyplot.show()

    def plotResiduals(self, stage, coordinate):
        horizontalSide1 = self.fiducialsDataSide1.xPositionList
        horizontalSide2 = self.fiducialsDataSide2.xPositionList

        if coordinate == 'Y':
            if stage == 'stage 1':
                verticalSide1 = self.fiducialsDataSide1.yOffsetsStage1
                verticalSide2 = self.fiducialsDataSide2.yOffsetsStage1
                predVerticalSide1 = self.fiducialsDataSide1.predictedYOffsetsStage1
                predVerticalSide2 = self.fiducialsDataSide2.predictedYOffsetsStage1
            else:
                verticalSide1 = self.fiducialsDataSide1.yOffsetsStage2
                verticalSide2 = self.fiducialsDataSide2.yOffsetsStage2
                predVerticalSide1 = self.fiducialsDataSide1.predictedYOffsetsStage2
                predVerticalSide2 = self.fiducialsDataSide2.predictedYOffsetsStage2
        else:
            if stage == 'stage 1':
                verticalSide1 = self.fiducialsDataSide1.xOffsetsStage1
                verticalSide2 = self.fiducialsDataSide2.xOffsetsStage1
                predVerticalSide1 = self.fiducialsDataSide1.predictedXOffsetsStage1
                predVerticalSide2 = self.fiducialsDataSide2.predictedXOffsetsStage1
            else:
                verticalSide1 = self.fiducialsDataSide1.xOffsetsStage2
                verticalSide2 = self.fiducialsDataSide2.xOffsetsStage2
                predVerticalSide1 = self.fiducialsDataSide1.predictedXOffsetsStage2
                predVerticalSide2 = self.fiducialsDataSide2.predictedXOffsetsStage2

        verticalSide1 = [verticalSide1[i] - predVerticalSide1[i] for i in range(len(verticalSide1))]
        verticalSide2 = [verticalSide2[i] - predVerticalSide2[i] for i in range(len(verticalSide2))]

        verticalSide1 = [item*10**6 for item in verticalSide1]
        verticalSide2 = [item*10**6 for item in verticalSide2]

        pyplot.subplot(211)
        pyplot.xlabel("X CAD position/meters")
        pyplot.ylabel(coordinate + " offsets residuals (low Y)/micrometers")
        pyplot.plot(horizontalSide1, verticalSide1, 'k.')

        pyplot.subplot(212)
        pyplot.xlabel("X CAD position/meters")
        pyplot.ylabel(coordinate + " offsets residuals (high Y)/micrometers")
        pyplot.plot(horizontalSide2, verticalSide2, 'k.')

        pyplot.show()
