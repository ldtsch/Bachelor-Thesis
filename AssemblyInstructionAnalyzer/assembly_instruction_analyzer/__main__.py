import sys
import os
import argparse
from assembly_instruction_analyzer.Analyzer import Analyzer
from assembly_instruction_analyzer.ReportGenerators.ConsoleReportGenerator import ConsoleReportGenerator
#from assembly_instruction_analyzer.ReportGenerators.GraphicalReportGenerator import GraphicalReportGenerator
from assembly_instruction_analyzer.ReportGenerators.FileReportGenerator import FileReportGenerator

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('--objdump', '-o', help="The objdump file to analyze", type=argparse.FileType('r', encoding='UTF-8'), 
                     required=True)

    args = parser.parse_args()

    path = os.path.dirname(__file__)
    filepath_data = os.path.join(path, '../instructions/aarch64_data_instructions.csv')
    filepath_general = os.path.join(path, '../instructions/aarch64_general_instructions.csv')
    filepath_fp = os.path.join(path, '../instructions/aarch64_fp_instructions.csv')
#    filepath_neon_scalar = os.path.join(path, '../instructions/neon_scalar_instructions.csv')
#    filepath_neon_vector = os.path.join(path, '../instructions/neon_vector_instructions.csv')
    filepath_neon = os.path.join(path, '../instructions/neon_instructions.csv')
    filepath_sve = os.path.join(path, '../instructions/sve_instructions.csv')
    filepath_objdump = args.objdump.name

    reportGenerator = FileReportGenerator()
    analyzer = Analyzer(reportGenerator)
    analyzer.LoadInstructionSet('AArch64 Data', filepath_data, False, True, False)
    analyzer.LoadInstructionSet('AArch64 General', filepath_general, False, False, False)
    analyzer.LoadInstructionSet('AArch64 FP', filepath_fp, False, False, True)
    analyzer.LoadInstructionSet('Neon', filepath_neon, True, False, True)
#    analyzer.LoadInstructionSet('Neon Scalar', filepath_neon_scalar, True, False)
#    analyzer.LoadInstructionSet('Neon Vector', filepath_neon_vector, True, False)
    analyzer.LoadInstructionSet('SVE', filepath_sve, True, False, True)

    analyzer.LoadObjdumpFile(os.path.basename(filepath_objdump), filepath_objdump)
    analyzer.ExecuteAnalysis()


if __name__ == "__main__":
    main()
