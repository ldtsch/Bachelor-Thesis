# Model class to store the definition of one instruction
class InstructionDefinitionModel:
    @property
    def InstructionCode(self):
        return self._instructionCode

    @InstructionCode.setter
    def InstructionCode(self, value):
        self._instructionCode = value

    @property
    def Description(self):
        return self._description

    @Description.setter
    def Description(self, value):
        self._description = value

    @property
    def NumberOfMatches(self):
        return self._numberOfMatches

    @NumberOfMatches.setter
    def NumberOfMatches(self, value):
        self._numberOfMatches = value

    def __init__(self):
        self._instructionCode = None
        self._description = None
        self._numberOfMatches = 0
