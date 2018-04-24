from setuptools import setup

setup(name='assembly_instruction_analyzer',
      version='0.1.0',
      packages=['assembly_instruction_analyzer'],
      entry_points={
          'console_scripts': [
              'assembly_instruction_analyzer = assembly_instruction_analyzer.__main__:main'
          ]
      },)
