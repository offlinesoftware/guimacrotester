from paths import Paths
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView

class SequenceTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.headers = ["Type", "x", "y", "dx", "dy", "Button", "Pressed", "Key", "Char"]
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setDragEnabled(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)   # or MultiSelection if you want Ctrl-click multi-row
        
        self.setColumnWidth(3, 50)
        self.setColumnWidth(4, 50)

        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)


    def populate_table(self):
        
        mac = self.parent.input_controller.macro
        self.setRowCount(len(mac))
        
        self.clearContents()

        for row, entry in enumerate(mac):
            for key, val in entry.items():
                for col, header in enumerate(self.headers):
                    if header.lower() == key:
                        self.setItem(row, col, QTableWidgetItem(str(val)))
    
    def to_macro(self):
        if Paths.debug: print("\nMacro extracted from table:")
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
        
        self.parent.input_controller.macro = mac
    
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
    
    def move_down(self):
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
