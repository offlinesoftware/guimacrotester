import pprint
from paths import Paths
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView

class MacroSeqTable(QTableWidget):

    # Constructor
    def __init__(self, parent=None):
        super().__init__(parent)
        self.headers = ["Name", "Sequence"]
        
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setDragEnabled(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)   # or MultiSelection if you want Ctrl-click multi-row
        self.setColumnWidth(0, 400)
        self.setColumnWidth(1, 400)

        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)
    
    
    # Populate macro-sequence table with from twm file
    def populate_table(self, ms):
        '''
        for n, row in enumerate(ms):
            print("\nRow:", n)
            print("Name:", row[0])
            print("Sequence:", row[1])
        '''
        for row in ms:
            row_number = self.rowCount()
            self.insertRow(row_number)
            self.setItem(row_number, 0, QTableWidgetItem(row[0]))
            self.setItem(row_number, 1, QTableWidgetItem(str(row[1])))
        self.window().set_ms_available(True)
            

    # Move an input row up in the sequence table
    def move_up(self):
        row = self.currentRow()
        if row <= 0:
            return  # already at top, nothing to do

        col_count = self.columnCount()

        # Swap each cell with the one above it
        for col in range(col_count):
            current_item = self.takeItem(row, col)
            above_item = self.takeItem(row - 1, col)

            self.setItem(row - 1, col, current_item)
            self.setItem(row, col, above_item)

        # Move selection to the new row
        self.selectRow(row - 1)


    # Move an input row down in the sequence table
    def move_down(self):
        if not self.selectedItems():
            return
        row = self.currentRow()
        if row >= self.rowCount() - 1:
            return  # already at bottom, nothing to do

        col_count = self.columnCount()

        # Swap each cell with the one above it
        for col in range(col_count):
            current_item = self.takeItem(row, col)
            below_item = self.takeItem(row + 1, col)

            self.setItem(row + 1, col, current_item)
            self.setItem(row, col, below_item)

        # Move selection to the new row
        self.selectRow(row + 1)


    # Import the sequence from the upper table to one row of the macro-sequence
    def import_current_seq(self, seq_name, from_file=None):
        self.window().sequence_table.to_sequence()       
        row = self.rowCount()
        self.insertRow(row)
        self.setItem(row, 0, QTableWidgetItem(seq_name))
        self.setItem(row, 1, QTableWidgetItem(str(self.window().input_controller.sequence)))
