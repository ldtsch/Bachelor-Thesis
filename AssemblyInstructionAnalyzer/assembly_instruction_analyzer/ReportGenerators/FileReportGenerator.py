import os
from datetime import datetime
import pandas as pd
from assembly_instruction_analyzer.ReportGenerators.AbstractReportGenerator import AbstractReportGenerator

class FileReportGenerator(AbstractReportGenerator):

    def GenerateReport(self):
        # To prepare, create a saving location
        dirname = "fr_" + self._analyzerModel.ObjdumpName + "_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.mkdir(dirname)
        print("Saving analysis to " + dirname)
        self.__generateCountFile(dirname)
        self.__generateInstructionSetStatistics(dirname)


    def __generateCountFile(self, dirname):
        with open(dirname + '/counts.csv', 'w') as f:
            f.write("TotalCount; InstructionCount; LabelCount; BranchCount; ReturnCount; UnmatchedCount\n") 
            f.write(str(self._analyzerModel.TotalCount) + "; " + str(self._analyzerModel.InstructionCount) + "; " + str(self._analyzerModel.LabelCount) + "; " + str(self._analyzerModel.BranchCount) + "; " + str(self._analyzerModel.ReturnCount) + "; " + str(self._analyzerModel.UnmatchedCount))
            f.close()

    def __generateInstructionSetStatistics(self, dirname):
        #first df: number of matches for all instruction sets
        df = pd.DataFrame(data=([x.Name, x.NumberOfMatches, x.IsSIMD, x.IsDataLoadStore, x.IsFP] for x in self.AnalyzerModel.InstructionSets), columns=['Name', 'Number of Matches', 'IsSIMD', 'IsDataLoadStore', 'IsFP'])
        df.to_csv(dirname + "/instruction_sets.csv", index=False, sep=";")

        # Third plots: The most used instructions for each set
        for iset in self.AnalyzerModel.InstructionSets:
            d = dict()
            # Sort instructions by number of matches and then filter the 10 most used
            instructions = sorted(iset.InstructionDefinitions, key=lambda x: x.NumberOfMatches, reverse=True)
            for x in range(0, min(20, len(iset.InstructionDefinitions))):
                if(instructions[x].NumberOfMatches == 0):
                    break
                d.update({instructions[x].InstructionCode: instructions[x].NumberOfMatches})

            # if empty dictionary -> keep going since ggplot will break
            if not d:
                continue
            df2 = pd.DataFrame(list(d.items()), columns = [
                'Instruction Code',
                'Number of matches'
            ])
            df2.to_csv(dirname + "/instructions_" + iset.Name + ".csv", index=False, sep=";")