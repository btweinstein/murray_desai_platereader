import argparse as ap
import re
import sys
import os

######### Definitions from previous file so everything is one place #######
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import skimage as ski
import skimage.io
import seaborn as sns # I use seaborn for plotting as it makes things easier to understand
sns.set_context('poster', font_scale = 1.25)

LOWERCASE_TO_INT = 96

class PlateReader_Experiment():

    def __init__(self, excel_path, table_position, f_low_position, f_high_position, high_dna_concentration=10,
                 well_rows = 8, well_columns=12):
        self.excel_path = excel_path
        self.column_str = table_position[0].lower() # Always lower case for consistency
        self.row = table_position[1]

        self.well_rows = well_rows
        self.well_columns = well_columns

        self.f_low_position = f_low_position
        self.f_high_position = f_high_position
        self.high_dna_concentration = high_dna_concentration

    def get_table(self):
        column_int = ord(self.column_str) - LOWERCASE_TO_INT # Converts characters into int

        # Excel starts at 1 indexing, so adjust both by one (python starts at zero)
        column_int -= 1
        row = self.row - 1

        # Import the excel file...always import the correct # of rows & columns
        excel_table = pd.read_excel(self.excel_path, header=None)
        # If the user was a potato and did not label all of their columns, this will not work correctly.
        # Nor if they did not label all of their rows. So make them do both.

        # Import the desired table
        table = excel_table.iloc[row:(row+self.well_rows), column_int:(column_int+self.well_columns)]

        # Label the table nicely
        columns = np.arange(1, self.well_columns + 1)
        rows = np.arange(1, self.well_rows + 1) + LOWERCASE_TO_INT
        row_names = [chr(z).upper() for z in rows]

        table.columns = columns
        table.index = row_names

        return table

    def get_concentration(self):
        """Returns concentration in units of ng/uL"""
        table = self.get_table()

        f_low = table.loc[self.f_low_position[0], self.f_low_position[1]]
        f_high = table.loc[self.f_high_position[0], self.f_high_position[1]]

        conc = ((table - f_low)/(f_high - f_low))*self.high_dna_concentration

        return conc

    def plot_table_as_heatmap(self, intensity_min = 10**4, intensity_max = 10**9):
        table = self.get_table()
        # Numpy does not like dealing with NaN unless things are floats evidently.
        table_values = np.array(table.values, dtype=np.float64)
        # Since we will probably plot this with a log scale, let us set all NaN values to 1.
        table_values[np.isnan(table_values)] = 1

        # Do the plotting
        ski.io.imshow(table_values, norm=LogNorm(), cmap='cubehelix', interpolation='None')
        plt.clim(intensity_min, intensity_max)
        plt.grid(False)

        # Label the axis ticks so that they look like a plate

        ytick_positions = np.arange(0, self.well_rows)
        ytick_labels = ytick_positions + 1
        # We actually want the ytick labels to be letters
        ytick_labels = [chr(z + LOWERCASE_TO_INT).upper() for z in ytick_labels]

        plt.yticks(ytick_positions, ytick_labels)

        xtick_positions = np.arange(0, self.well_columns)
        xtick_labels = xtick_positions + 1

        plt.xticks(xtick_positions, xtick_labels)


if __name__=='__main__':

    ######### Parsing the input

    parser = ap.ArgumentParser(description='Converts plate reader fluorescence measurements into DNA concentrations.')
    parser.add_argument('filename', help='The path to the desired excel file.')
    parser.add_argument('-t', '--table_position', help = 'Column then row in the excel file (default A1) of the upper left corner of the table')
    parser.add_argument('-s1', '--standard_1_position', help = 'Position of standard 1 (low fluorescence) on the 96 well plate (default A1)')
    parser.add_argument('-s2', '--standard_2_position', help = 'Position of standard 2 (high fluorescence) on the 96 well plate (default B1)')

    parsed_info = parser.parse_args()

    # Now parse the inputs
    file_name = parsed_info.filename
    table_position_str = parsed_info.table_position
    if table_position_str is None:
        table_position_str = 'A1'
    low_fluor_position_str = parsed_info.standard_1_position
    if low_fluor_position_str is None:
        low_fluor_position_str = 'A1'
    high_fluor_position_str = parsed_info.standard_2_position
    if high_fluor_position_str is None:
        high_fluor_position_str = 'B1'


    # Parse the strings

    def get_string_then_digits(input_string):
        match = re.match(r"([a-z]+)([0-9]+)", input_string , re.I)
        items = None
        if match:
            items = match.groups()
            # Convert second piece to number
            items = list(items)
            items[1] = int(items[1])
        return items


    table_position = get_string_then_digits(table_position_str)
    if len(table_position[0]) > 1:
        print 'pls organize ur excel file, y r u in AA'
        sys.exit(1)

    low_fluor_position = get_string_then_digits(low_fluor_position_str)
    high_fluor_position = get_string_then_digits(high_fluor_position_str)

    experiment = PlateReader_Experiment(file_name, table_position, low_fluor_position, high_fluor_position)
    conc = experiment.get_concentration()


    filename_without_extension = os.path.split(file_name)[0]
    output_filename = filename_without_extension + '/conc_' + table_position_str

    conc.to_csv(output_filename + '.csv', sep='\t', header=False, index=False)

    def float_formatter(input_float):
        return str(round(input_float, 2))

    conc.to_html(output_filename + '.html', float_format=float_formatter)