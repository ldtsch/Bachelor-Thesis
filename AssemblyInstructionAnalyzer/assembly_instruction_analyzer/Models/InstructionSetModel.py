import re

class InstructionSetModel:

    # create properties

    @property
    def Name(self):
        return self._name

    @Name.setter
    def Name(self, value):
        self._name = value

    @property
    def Filepath(self):
        return self._filepath

    @Filepath.setter
    def Filepath(self, value):
        self._filepath = value

    @property
    def ArgumentCondition(self):
        return self._argumentCondition

    @ArgumentCondition.setter
    def ArgumentCondition(self, value):
        self._argumentCondition = value

    @property
    def IsSIMD(self):
        return self._isSimd

    @IsSIMD.setter
    def IsSIMD(self, value):
        self._isSimd = value

    @property
    def IsDataLoadStore(self):
        return self._isDataLoadStore

    @IsDataLoadStore.setter
    def IsDataLoadStore(self, value):
        self._isDataLoadStore = value

    @property
    def IsFP(self):
        return self._isFP

    @IsFP.setter
    def IsFP(self, value):
        self._isFP = value

    # our list of instruction definition objects
    @property
    def InstructionDefinitions(self):
        return self._instructionDefinitions

    @InstructionDefinitions.setter
    def InstructionDefinitions(self, value):
        self._instructionDefinitions = value

    # the number of matches
    @property
    def NumberOfMatches(self):
        return self._numberOfMatches

    def __init__(self, name, filepath):
        self._name = name
        self._filepath = filepath
        self._numberOfMatches = 0
        self._instructionDefinitions = []
        self._argumentCondition = None
        self._isSimd = False
        self._isDataLoadStore = False
        self._isFP = False

    def AddInstructionDefinition(self, definition):
        self._instructionDefinitions.append(definition)

    def IncrementIfContains(self, disassembledInstruction):
        # First check if condition holds, if not we can return right away
        if not re.match(self._argumentCondition, disassembledInstruction.Arguments):
            return False
        # Then check the rest
        # Increment both the set's number of matches and the instruction's number of matches
        for defn in self._instructionDefinitions:
            if str.upper(disassembledInstruction.InstructionCode) == str.upper(defn.InstructionCode):
                self._numberOfMatches += 1
                defn.NumberOfMatches += 1
                return True
        return False

    # Debug method
    def PrintInstructions(self):
        print(self.Name)
        print(self.Filepath)
        for defn in self._instructionDefinitions:
            print(defn.InstructionCode + ": " + defn.Description)
