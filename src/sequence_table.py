from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView

class SequenceTable(QTableWidget):
    def __init__(self, parent):
        super(SequenceTable, self).__init__(parent)
        self.parent = parent
        self.headers = ["Type", "x", "y", "Button", "Pressed", "Key", "Char"]
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    
    def populate_table(self):
        
        mac = self.parent.input_controller.macro
        self.setRowCount(len(mac))
        
        self.clearContents()

        for row, entry in enumerate(mac):
            for key, val in entry.items():
                for col, header in enumerate(self.headers):
                    if header.lower() == key:
                        self.setItem(row, col, QTableWidgetItem(str(val)))
