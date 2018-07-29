import numpy

class fiducial:
    def __init__(self, dataVals):
        self.xPosition = dataVals[0]
        self.yPosition = dataVals[1]
        self.stage1OffsetX = dataVals[2]
        self.stage1OffsetY = dataVals[3]
        self.stage2offsetX = dataVals[4]
        self.stage2offsetY = dataVals[5]

class fiducials:
    def __init__(self, fiducialList):
        self.xPositionList = [item.xPosition for item in fiducialList]
        self.yPositionList = [item.yPosition for item in fiducialList]
        print(len(self.xPositionList))
        self.xOffsetsStage1 = [item.stage1OffsetX for item in fiducialList]
        self.yOffsetsStage1 = [item.stage1OffsetY for item in fiducialList]
        print(len(self.yOffsetsStage1))
        self.xOffsetsStage2 = [item.stage2offsetX for item in fiducialList]
        self.yOffsetsStage2 = [item.stage2offsetY for item in fiducialList]

        fitOffsetX = [numpy.polyfit(self.xPositionList, self.xOffsetsStage1, 3), numpy.polyfit(self.xPositionList, self.xOffsetsStage2, 3)]
        fitOffsetY = [numpy.polyfit(self.xPositionList, self.yOffsetsStage1, 3), numpy.polyfit(self.xPositionList, self.yOffsetsStage2, 3)]

        self.predictedXOffsetsStage1 = [numpy.polyval(fitOffsetX[0], x) for x in self.xPositionList]
        self.predictedYOffsetsStage1 = [numpy.polyval(fitOffsetY[0], x) for x in self.xPositionList]
        self.predictedXOffsetsStage2 = [numpy.polyval(fitOffsetX[1], x) for x in self.xPositionList]
        self.predictedYOffsetsStage2 = [numpy.polyval(fitOffsetY[1], x) for x in self.xPositionList]
