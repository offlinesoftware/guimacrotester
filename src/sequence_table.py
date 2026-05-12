from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView

class SequenceTable(QTableWidget):
    def __init__(self, parent):
        super(SequenceTable, self).__init__(parent)
        self.parent = parent
        self.headers = ["Type", "x", "y", "Button", "Pressed", "Key", "Char"]
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setDragEnabled(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)   # or MultiSelection if you want Ctrl-click multi-row
        
    
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
        mac = []
        for r in range(self.rowCount()):
            row_dict = {}
            for c, header in enumerate(h.lower() for h in self.headers):
                item = self.item(r, c)
                row_dict[header] = item.text() if item else ""
            print(row_dict)
            mac.append(row_dict)
        
        self.parent.input_controller.macro = mac