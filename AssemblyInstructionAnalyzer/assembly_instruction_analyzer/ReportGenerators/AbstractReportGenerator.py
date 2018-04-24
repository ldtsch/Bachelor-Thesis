from abc import ABC, abstractmethod

class AbstractReportGenerator(ABC):

    @property
    def AnalyzerModel(self):
        return self._analyzerModel

    @AnalyzerModel.setter
    def AnalyzerModel(self, value):
        self._analyzerModel = value

    def __init__(self):
        self._analyzerModel = None

    @abstractmethod
    def GenerateReport(self):
        pass
