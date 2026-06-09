from paths import Paths
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView

class SequenceTable(QTableWidget):

    # Constructor
    def __init__(self, parent=None, is_macro_sequence=False):
        super().__init__(parent)
        self.parent = parent

        if is_macro_sequence:
            self.headers = ["Name", "Sequence"]
        else:
            self.headers = ["Type", "x", "y", "dx", "dy", "Button", "Pressed", "Key", "Char"]
        
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setDragEnabled(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)   # or MultiSelection if you want Ctrl-click multi-row
        
        if is_macro_sequence:
            self.setColumnWidth(1, 700)
        else:
            self.setColumnWidth(3, 50)
            self.setColumnWidth(4, 50)

        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)


    # Populate upper sequence table with recorded sequence
    def populate_table(self):
        
        mac = self.parent.input_controller.sequence
        self.setRowCount(len(mac))
        
        self.clearContents()

        for row, entry in enumerate(mac):
            for key, val in entry.items():
                for col, header in enumerate(self.headers):
                    if header.lower() == key:
                        self.setItem(row, col, QTableWidgetItem(str(val)))
    

    # Read sequence from upper table and send back to input_controller
    def to_sequence(self):
        if Paths.debug: print("\nsequence extracted from table:")
        mac = []
        for r in range(self.rowCount()):
            row_dict = {}
            for c, header in enumerate(h.lower() for h in self.headers):
                item = self.item(r, c)
                row_dict[header] = item.text() if item else ""
            if row_dict['pressed'] == 'True': row_dict['pressed'] = True
            if row_dict['pressed'] == 'False': row_dict['pressed'] = False
            if Paths.debug: print(row_dict)
            mac.append(row_dict)
        
        self.parent.input_controller.sequence = mac
    

    # Move an input row up in the sequence table
    def move_up(self):
        if Paths.debug:
            print(self.selectedItems())
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
        if row >= self.rowCount():
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
    def import_current_seq(self, seq_name):
        self.parent.sequence_table.to_sequence()       
        row = self.rowCount()
        self.insertRow(row)
        self.setItem(row, 0, QTableWidgetItem(seq_name))
        self.setItem(row, 1, QTableWidgetItem(str(self.parent.input_controller.sequence)))
