# Since I want to add some nice-to-use properties like ratios etc. in this, this technically
# isn't a model but more like a C# view model, but I don't really care (and python neither)
# so whatever
from decimal import Decimal

class AnalyzerModel:
    def __init__(self):
        self._instructionSets = []
        self._disassembledInstructions = []
        self._unmatchedCount = 0
        self._totalCount = 0
        self._labelCount = 0
        self._instructionCount = 0
        self._returnCount = 0
        self._branchCount = 0
        self._unmatchedLines = []
        self._objdumpName = ""

    @property
    def ObjdumpName(self):
        return self._objdumpName

    @ObjdumpName.setter
    def ObjdumpName(self, value):
        self._objdumpName = value
        
    @property
    def InstructionSets(self):
        return self._instructionSets

    @InstructionSets.setter
    def InstructionSets(self, value):
        self._instructionSets = value

    @property
    def DisassembledInstructions(self):
        return self._disassembledInstructions

    @DisassembledInstructions.setter
    def DisassembledInstructions(self, value):
        self._disassembledInstructions = value

    @property
    def UnmatchedLines(self):
        return self._unmatchedLines

    @UnmatchedLines.setter
    def UnmatchedLines(self, value):
        self._unmatchedLines = value

    @property
    def UnmatchedCount(self):
        return self._unmatchedCount

    @UnmatchedCount.setter
    def UnmatchedCount(self, value):
        self._unmatchedCount = value

    @property
    def TotalCount(self):
        return self._totalCount

    @TotalCount.setter
    def TotalCount(self, value):
        self._totalCount = value

    @property
    def LabelCount(self):
        return self._labelCount

    @LabelCount.setter
    def LabelCount(self, value):
        self._labelCount = value

    @property
    def InstructionCount(self):
        return self._instructionCount

    @InstructionCount.setter
    def InstructionCount(self, value):
        self._instructionCount = value

    @property
    def ReturnCount(self):
        return self._returnCount

    @ReturnCount.setter
    def ReturnCount(self, value):
        self._returnCount = value

    @property
    def BranchCount(self):
        return self._branchCount

    @BranchCount.setter
    def BranchCount(self, value):
        self._branchCount = value

    # Here we go with the calculated properties
    @property
    def InstructionRatio(self):
        ratio = Decimal(100 * self._instructionCount / self._totalCount)
        return round(ratio, 2)

    @property
    def LabelRatio(self):
        ratio = Decimal(100 * self._labelCount / self._totalCount)
        return round(ratio, 2)

    @property
    def BranchRatio(self):
        ratio = Decimal(100 * self._branchCount / self._totalCount)
        return round(ratio, 2)

    @property
    def ReturnRatio(self):
        ratio = Decimal(100 * self._returnCount / self._totalCount)
        return round(ratio, 2)

    @property
    def UnmatchedRatio(self):
        ratio = Decimal(100 * self._unmatchedCount / self._totalCount)
        return round(ratio, 2)
