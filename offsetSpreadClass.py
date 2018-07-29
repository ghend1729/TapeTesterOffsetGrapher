import matplotlib
import matplotlib.pyplot as pyplot
import numpy

class spreadStorer:
    XCad = []
    offsets = []
    means = []
    spreads = []

    def __init__(self, offsetsSide1, offsetsSide2):
        self.offsets = offsetsSide1 + offsetsSide2
        self.means = [numpy.mean(offsetSet) for offsetSet in self.offsets]
        self.spreads = [[offset - self.means[i] for offset in self.offsets[i]] for i in range(len(self.offsets))]


class offsetSpreadAnalyse:
    def __init__(self, dataSets):
        lenSide1 = len(dataSets[0].fiducialsDataSide1.xPositionList)
        lenSide2 = len(dataSets[0].fiducialsDataSide2.xPositionList)
        self.numberOfDataSets = len(dataSets)
        self.XCad = dataSets[0].fiducialsDataSide1.xPositionList + dataSets[0].fiducialsDataSide2.xPositionList
        self.yOffsetsStage1 = spreadStorer([[item.fiducialsDataSide1.yOffsetsStage1[i] for item in dataSets] for i in range(lenSide1)], [[item.fiducialsDataSide2.yOffsetsStage1[i] for item in dataSets] for i in range(lenSide2)])
        self.yOffsetsStage2 = spreadStorer([[item.fiducialsDataSide1.yOffsetsStage2[i] for item in dataSets] for i in range(lenSide1)], [[item.fiducialsDataSide2.yOffsetsStage2[i] for item in dataSets] for i in range(lenSide2)])
        self.xOffsetsStage1 = spreadStorer([[item.fiducialsDataSide1.xOffsetsStage1[i] for item in dataSets] for i in range(lenSide1)], [[item.fiducialsDataSide2.xOffsetsStage1[i] for item in dataSets] for i in range(lenSide2)])
        self.xOffsetsStage2 = spreadStorer([[item.fiducialsDataSide1.xOffsetsStage2[i] for item in dataSets] for i in range(lenSide1)], [[item.fiducialsDataSide2.xOffsetsStage2[i] for item in dataSets] for i in range(lenSide2)])

        self.yOffsetsStage1HistorgramData = self.generateHistogramData(self.yOffsetsStage1)
        self.yOffsetsStage2HistorgramData = self.generateHistogramData(self.yOffsetsStage2)
        self.xOffsetsStage1HistorgramData = self.generateHistogramData(self.xOffsetsStage1)
        self.xOffsetsStage2HistorgramData = self.generateHistogramData(self.xOffsetsStage2)


    def generateHistogramData(self, spreadStorerObject):
        result = []

        for spreadSet in spreadStorerObject.spreads:
            result += spreadSet

        return result

    def graphDifferenceFromMeanAsFunctionOfXCad(self, coordinate):
        xData = self.XCad

        if coordinate == 'X':
            DataListStage1 = [[item[i]*10**6 for item in self.xOffsetsStage1.spreads] for i in range(self.numberOfDataSets)]
            DataListStage2 = [[item[i]*10**6 for item in self.xOffsetsStage2.spreads] for i in range(self.numberOfDataSets)]
        else:
            DataListStage1 = [[item[i]*10**6 for item in self.yOffsetsStage1.spreads] for i in range(self.numberOfDataSets)]
            DataListStage2 = [[item[i]*10**6 for item in self.yOffsetsStage2.spreads] for i in range(self.numberOfDataSets)]

        pyplot.subplot(211)
        pyplot.xlabel("X CAD position")
        pyplot.ylabel(coordinate + " offsets difference from mean (stage1)")
        for yData in DataListStage1:
            pyplot.plot(xData, yData, 'k.')


        pyplot.subplot(212)
        pyplot.xlabel("X CAD position")
        pyplot.ylabel(coordinate + " offsets difference from mean (stage2)")
        for yData in DataListStage2:
            pyplot.plot(xData, yData, 'k.')

        pyplot.show()
