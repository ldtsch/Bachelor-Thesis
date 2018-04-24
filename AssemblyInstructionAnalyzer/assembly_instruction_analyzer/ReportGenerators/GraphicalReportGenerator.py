import os
from datetime import datetime
from plotnine import *
from plotnine.data import *
import pandas as pd
from assembly_instruction_analyzer.ReportGenerators.AbstractReportGenerator import AbstractReportGenerator

class GraphicalReportGenerator(AbstractReportGenerator):

    def GenerateReport(self):
        
        # To prepare, create a saving location
        dirname = "graphreport_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.mkdir(dirname)

        # First, let's generate a plot comparing the respective instruction sets with each other
        # Therefore, let's create a dataframe in the format
        #           instruction count
        # set name        ..
        df = pd.DataFrame(data=([x.Name, x.NumberOfMatches] for x in self.AnalyzerModel.InstructionSets), columns=['Name', 'Number of Matches'])
        plot = ggplot(df, aes(x='Name', y='Number of Matches')) + geom_bar(stat='identity', fill='steelblue') \
                    + xlab("Instruction set name") \
                    + ylab("Number of matches") \
                    + ggtitle("Number of instructions used for each instruction set") \
                    + geom_text(aes(label='Number of Matches'), nudge_y=1)
        plot.save(dirname + "/plot_is_comparison.png", width=25, height=15, units='cm')
        # print(plot)

        # Second plot: Compare Simd instruction sets
        df = pd.DataFrame(data=([x.Name, x.NumberOfMatches] for x in filter(lambda r: r.IsSIMD is True, self.AnalyzerModel.InstructionSets)), columns=['Name', 'Number of Matches'])
        plot = ggplot(df, aes(x='Name', y='Number of Matches')) + geom_bar(stat='identity', fill='steelblue') \
                    + xlab("Instruction set name") \
                    + ylab("Number of instructions") \
                    + ggtitle("Number of instructions used for each instruction set") \
                    + geom_text(aes(label='Number of Matches'), nudge_y=1)
        plot.save(dirname + "/plot_is_comparison_simd.png", width=25, height=15, units='cm')

        # Third plot: Exclude data load/store operations
        df = pd.DataFrame(data=([x.Name, x.NumberOfMatches] for x in filter(lambda r: r.IsDataLoadStore is False, self.AnalyzerModel.InstructionSets)), columns=['Name', 'Number of Matches'])
        plot = ggplot(df, aes(x='Name', y='Number of Matches')) + geom_bar(stat='identity', fill='steelblue') \
                    + xlab("Instruction set name") \
                    + ylab("Number of instructions") \
                    + ggtitle("Number of instructions used for each instruction set") \
                    + geom_text(aes(label='Number of Matches'), nudge_y=1)
        plot.save(dirname + "/plot_is_comparison_nodataloadstore.png", width=25, height=15, units='cm')

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
            df = pd.DataFrame(list(d.items()), columns = [
                'Instruction Code',
                'Number of matches'
            ])
            #print(df)
            plot =  ggplot(df, aes(x='Instruction Code', y='Number of matches'))  \
                    + geom_bar(stat='identity', fill='steelblue') \
                    + xlab("Instruction codes") \
                    + ylab("Number of matches") \
                    + ggtitle("Most used instructions for instruction set " + iset.Name) \
                    + geom_text(aes(label='Number of Matches'), nudge_y=1)
            plot.save(dirname + "/plot_" + iset.Name + ".png", width=25, height=15, units='cm')
            # print(plot)

        df = pd.DataFrame(data=([x.Name, x.NumberOfMatches] for x in filter(lambda r: r.IsFP is True, self.AnalyzerModel.InstructionSets)), columns=['Name', 'Number of Matches'])
        plot = ggplot(df, aes(x='Name', y='Number of Matches')) + geom_bar(stat='identity', fill='steelblue') \
                    + xlab("Instruction set name") \
                    + ylab("Number of instructions") \
                    + ggtitle("Number of instructions used for each instruction set") \
                    + geom_text(aes(label='Number of Matches'), nudge_y=1)
        plot.save(dirname + "/plot_is_comparison_fp.png", width=25, height=15, units='cm')

