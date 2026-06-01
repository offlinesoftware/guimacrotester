from paths import Paths
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget

class MacroSequenceList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setDragDropMode(QListWidget.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)
        self.macro_list = []
    
    def import_current_seq(self, seq_name):

        self.parent.sequence_table.to_macro()
        mac = self.parent.input_controller.macro
        self.macro_list.append(mac)
        self.parent.ms_list.addItem(seq_name + ": " + str(mac))