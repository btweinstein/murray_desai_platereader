import murray_desai_platereader as mdp
import argparse as ap
import re

parser = ap.ArgumentParser(description='Converts plate reader fluorescence measurements into DNA concentrations.')
parser.add_argument('filename', help='The path to the desired excel file.')
parser.add_argument('-t', '--table_position', help = 'Column then row in the excel file (default A1) of the upper left corner of the table')
parser.add_argument('-s1', '--standard_1_position', help = 'Position of standard 1 (low fluorescence) on the 96 well plate (default A1)')
parser.add_argument('-s2', '--standard_2_position', help = 'Position of standard 2 (high fluorescence) on the 96 well plate (default B1)')

parsed_info = parser.parse_args()

print parsed_info

# Now parse the inputs
file_name = parsed_info.filename

table_position = parsed_info.table_position
if table_position is None:
    table_position = 'A1'
low_fluor_position = parsed_info.standard_1_position
if low_fluor_position is None:
    low_fluor_position = 'A1'
high_fluor_position = parsed_info.standard_2_position
if high_fluor_position is None:
    high_fluor_position = 'B1'


# Parse the strings

match = re.match(r"([a-z]+)([0-9]+)", 'foofo21', re.I)
if match:
    items = match.groups()

print table_position

#experiment = mdp.PlateReader_Experiment(file_name, table_position, low_fluor_position, high_fluor_position, **kwargs)
#conc = experiment.get_concentration()