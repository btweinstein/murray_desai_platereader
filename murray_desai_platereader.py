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

    def __init__(self, excel_path, column_str, row, well_rows = 8, well_columns=12):
        self.excel_path = excel_path
        self.column_str = column_str.lower() # Always lower case for consistency
        self.row = row

        self.well_rows = well_rows
        self.well_columns = well_columns

    def get_table(self):
        column_int = ord(self.column_str) - LOWERCASE_TO_INT # Converts characters into int
        row = 2

        # Excel starts at 1 indexing, so adjust both by one (python starts at zero)
        column_int -= 1
        row -= 1

        # Import the excel file
        excel_table = pd.read_excel(self.excel_path, header=None)
        # Import the desired table
        table = excel_table.iloc[row:(row+self.well_rows), column_int:(column_int+self.well_columns)]

        # Label the table nicely
        columns = np.arange(1, self.well_columns + 1)
        rows = np.arange(1, self.well_rows + 1) + LOWERCASE_TO_INT
        row_names = [chr(z).upper() for z in rows]

        table.columns = columns
        table.index = row_names

        return table

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

