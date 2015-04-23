import numpy as np
import pandas as pd

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