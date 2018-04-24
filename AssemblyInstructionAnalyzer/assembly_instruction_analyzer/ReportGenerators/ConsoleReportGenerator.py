from decimal import Decimal
from assembly_instruction_analyzer.ReportGenerators.AbstractReportGenerator import AbstractReportGenerator
from assembly_instruction_analyzer.Models.DisassembledInstructionModel import Match

class ConsoleReportGenerator(AbstractReportGenerator):

    def GenerateReport(self):
        # This method generates a report and delivers it to the customer in console form
        # For now, let's just print some funny things
        print("\n\nALERT ALERT OBJDUMP REPORT INCOMING\n\n")
        print("Total number of instructions analyzed: " + str(self._analyzerModel.TotalCount))
        print("Of those, " + str(self._analyzerModel.InstructionCount) + " (" + str(self._analyzerModel.InstructionRatio) + "%) were instructions")
        print(str(self._analyzerModel.LabelCount) + "(" + str(self._analyzerModel.LabelRatio) + "%) were labels")
        print(str(self._analyzerModel.ReturnCount) + " (" + str(self._analyzerModel.ReturnRatio) + "%) were return statements")
        print(str(self._analyzerModel.BranchCount) + " (" + str(self._analyzerModel.BranchRatio) + "%) were branch statements")
        print(str(self._analyzerModel.UnmatchedCount) + " (" + str(self._analyzerModel.UnmatchedRatio) + "%) were unmatched statements")
        print("The distribution between instruction sets is as follows")
        for instrSet in self._analyzerModel.InstructionSets:
            percentage = str(round(Decimal(100 * instrSet.NumberOfMatches / self._analyzerModel.TotalCount), 2))
            print("For the instruction set " + instrSet.Name + ", we had " + str(instrSet.NumberOfMatches) + " (" + percentage + "%) matches")

        print("\nThe unmatched lines were the following:")
        for l in self._analyzerModel.UnmatchedLines:
            print(l)
        print("\nThe unmatched instructions were")
        noMatch = 0
        match = 0
        multiMatch = 0
        for di in list(filter(lambda x: x.IsInstruction, self._analyzerModel.DisassembledInstructions)):
            if di.Match == Match.NoMatch:
                print(di.InstructionCode + " " + di.Arguments)
                noMatch += 1
            if di.Match == Match.Match:
                match += 1
            if di.Match == Match.MultiMatch:
                multiMatch += 1

        print("\nWe had " + str(noMatch) + " no-matches, " + str(match) + " single matches and " + str(multiMatch) + " multi matches")
        
        # Most used instructions
        for iset in self.AnalyzerModel.InstructionSets:
            print("\nInstruction Set " + iset.Name)
            instructions = sorted(iset.InstructionDefinitions, key=lambda x: x.NumberOfMatches, reverse=True)
            for x in range(0, min(10, len(iset.InstructionDefinitions))):
                if(instructions[x].NumberOfMatches == 0):
                    break;
                print(instructions[x].InstructionCode + " " + str(instructions[x].NumberOfMatches))
                if x == 10:
                    break
        print("OBJDUMP REPORT OVER")
        