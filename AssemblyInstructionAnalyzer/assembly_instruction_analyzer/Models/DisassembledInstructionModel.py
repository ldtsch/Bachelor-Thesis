from enum import Enum

# Model class for one disassembled instruction
class DisassembledInstructionModel:
    @property
    def IsInstruction(self):
        return self._isInstruction

    @IsInstruction.setter
    def IsInstruction(self, value):
        self._isInstruction = value
    
    @property
    def IsLabel(self):
        return self._isLabel

    @IsLabel.setter
    def IsLabel(self, value):
        self._isLabel = value

    @property
    def IsReturn(self):
        return self._isReturn

    @IsReturn.setter
    def IsReturn(self, value):
        self._isReturn = value

    @property
    def IsBranch(self):
        return self._isBranch

    @IsBranch.setter
    def IsBranch(self, value):
        self._isBranch = value

    @property
    def Label(self):
        if self._label is None:
            return ""
        return self._label

    @Label.setter
    def Label(self, value):
        # print("Label set: " + value)
        self._label = value

    @property
    def Opcode(self):
        if self._opcode is None:
            return ""
        return self._opcode

    @Opcode.setter
    def Opcode(self, value):
        # print("Opcode set: " + value)
        self._opcode = value

    @property
    def InstructionCode(self):
        if self._instructionCode is None:
            return ""
        return self._instructionCode

    @InstructionCode.setter
    def InstructionCode(self, value):
        # print("Instr Code set: " + value)
        self._instructionCode = value

    @property
    def Arguments(self):
        if self._arguments is None:
            return ""
        return self._arguments

    @Arguments.setter
    def Arguments(self, value):
        #        print("Arguments set: " + value)
        self._arguments = value

    @property
    def Match(self):
        return self._match

    @Match.setter
    def Match(self, value):
        self._match = value

    def __init__(self):
        self._isInstruction = False
        self._isLabel = False
        self._isReturn = False
        self._isBranch = False
        self._label = None
        self._opcode = None
        self._instructionCode = None
        self._arguments = None
        self._match = Match.NoMatch

class Match(Enum):
    NoMatch = 1
    Match = 2
    MultiMatch = 3
