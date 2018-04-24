# We need to parse .csv files, so import the necessary packages
import csv
import re
from assembly_instruction_analyzer.Models.InstructionSetModel import InstructionSetModel
from assembly_instruction_analyzer.Models.InstructionDefinitionModel import InstructionDefinitionModel
from assembly_instruction_analyzer.Models.DisassembledInstructionModel import DisassembledInstructionModel
from assembly_instruction_analyzer.Models.DisassembledInstructionModel import Match
from assembly_instruction_analyzer.Models.AnalyzerModel import AnalyzerModel

class Analyzer:
    
    @property
    def AnalyzerModel(self):
        return self._analyzerModel

    @AnalyzerModel.setter
    def AnalyzerModel(self, value):
        self._analyzerModel = value

    @property
    def ReportGenerator(self):
        return self._reportGenerator

    @ReportGenerator.setter
    def ReportGenerator(self, value):
        self._reportGenerator = value

    def __init__(self, reportGenerator):
        self._analyzerModel = AnalyzerModel()
        self._reportGenerator = reportGenerator

    # This method should load a definition file with the given name
    # and store the instructions in our dictionary for later use.
    # The instruction set definition needs to contain a regex for the
    # condition at the first line
    def LoadInstructionSet(self, name, filepath, isSimd, isDataLoadStore, isFP):
        print("Loading Instruction Set with name " + name + " at path " + filepath)
        with open(filepath, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            instrSet = InstructionSetModel(name, filepath)
            instrSet.IsSIMD = isSimd
            instrSet.IsDataLoadStore = isDataLoadStore
            instrSet.IsFP = isFP
            # Get the condition Regex
            regex = next(reader)
            instrSet.ArgumentCondition = regex[0]
            # Read instructions from csv and add to model
            for row in reader:
                instrDefn = InstructionDefinitionModel()
                instrDefn.InstructionCode = row[0]
                # instrDefn.Description = row[1] # don't need that I believe
                instrSet.AddInstructionDefinition(instrDefn)

            self._analyzerModel.InstructionSets.append(instrSet)

    def LoadObjdumpFile(self, name, filepath):
        """    We expect a standard objdump file generated with options
                objdump -d --no-show-raw-insn
                that should be in the format
                <space><space>OPCODE:<tab>Instruction<tab>Arguments
        """
        print("Loading Objdump file with name " + name + " at path " + filepath)
        self._analyzerModel.ObjdumpName = name
        with open(filepath, 'r') as f:
            content = f.readlines()
            content = [x.strip() for x in content]  # remove whitespaces etc
            for line in content:
                self.__analyzeObjdumpLine(line)

    def __analyzeObjdumpLine(self, line):
        # Check if blank line or "...", which for some reason objdump likes to generate
        if re.match("^\s*$", line) or re.match("^\.*$", line):
            return

        match = DisassembledInstructionModel()

        self._analyzerModel.TotalCount += 1

        # Check if label: a label has a ":" as last character
        # other than that, no special things so not sure if this is enough
        instr = re.match("(.*):$", line)
        if instr:
            match.IsLabel = True
            match.Label = instr.group(1)
            self._analyzerModel.DisassembledInstructions.append(match)
            self._analyzerModel.LabelCount += 1
            return

        # filter for branch and return instructions
        instr = re.match(".([A-Fa-f0-9]*):\tret", line)
        if instr:
            match.IsReturn = True
            self._analyzerModel.DisassembledInstructions.append(match)
            self._analyzerModel.ReturnCount += 1
            return
        
        # Branch: check for match of all (?) possible branch conditions, according to manual
        instr = re.match("([A-Fa-f0-9]*):[\t\s](cbn?z|tbn?z|b.?(eq|ne|cs|hs|cc|lo|mi|pl|vs|vc|hi|ls|ge|lt|gt|le|al)?).*", line)
        if instr:
            match.IsBranch = True
            self._analyzerModel.DisassembledInstructions.append(match)
            self._analyzerModel.BranchCount += 1
            return

        # Check if instruction:
        # OPCODE:<tab/space>Instruction<tab/space>Arguments
        # Regex explanation:
        # ([A-Fa-f0-9]*) the opcode, match for hex number
        # ([A-Za-z0-9]*) the instruction, can contain any char or number
        # (.*) optional: match any character as argument (registers, offsets, and so on)
        instr = re.match("([A-Fa-f0-9]*):[\t\s]([A-Za-z0-9]*)[\t\s]?(.*)", line)
        if instr:
            match.IsInstruction = True
            match.Opcode = instr.group(1)
            match.InstructionCode = instr.group(2)
            match.Arguments = instr.group(3)
            self._analyzerModel.DisassembledInstructions.append(match)
            self._analyzerModel.InstructionCount += 1
            return

        # If we don't have a match, we do nothing but
        # I'll rather have all of them in a list
        # to see whether we're correct
        self._analyzerModel.UnmatchedCount += 1
        self._analyzerModel.UnmatchedLines.append(line)

    # This method launches the analysis and does some weird stuff
    # to try to get some decent results
    def ExecuteAnalysis(self):
        # For each instruction from our objdump:
        for entry in self._analyzerModel.DisassembledInstructions:
            # If we have a label, continue (for now)
            if not entry.IsInstruction:
                continue
            # #1: Loop through the instruction set definitions and count
            for instrSet in self._analyzerModel.InstructionSets:
                match = instrSet.IncrementIfContains(entry)
                # Here we set whether the instruction matches any instr sets
                # or multiple if applicable
                if match and entry.Match == Match.NoMatch:
                    entry.Match = Match.Match
                elif match and entry.Match == Match.Match:
                    entry.Match = Match.MultiMatch

        # When we're done with this, generate a report
        self._reportGenerator.AnalyzerModel = self._analyzerModel
        self._reportGenerator.GenerateReport()
