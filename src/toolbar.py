from paths import Paths
from PySide6.QtGui import QAction
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QToolBar

class Toolbar(QToolBar):
    def __init__(self, parent, tb_num):
        super(Toolbar, self).__init__(parent)
        self.setIconSize(QSize(16, 16))
        match tb_num:
            case 1:
                # 'Add new screen' button
                self.add_screen_action = QAction(
                    # QIcon(Paths.icon("ui-tab--plus.png")), 
                    "Add new screen",
                    self
                )
                self.add_screen_action.setStatusTip("Add a new group of screen co-ordinates")
                self.add_screen_action.triggered.connect(self.parent().add_screen)
                self.addAction(self.add_screen_action)

                # 'Record macro' button
                self.record_macro_action = QAction(
                    # QIcon(Paths.icon("plus.png")), 
                    "Record macro",
                    self
                )
                self.record_macro_action.setStatusTip("Record a sequence of inputs")
                self.record_macro_action.triggered.connect(self.parent().record_macro)
                self.addAction(self.record_macro_action)

                # 'Play macro' button
                self.play_macro_action = QAction(
                    # QIcon(Paths.icon("plus.png")), 
                    "Play macro",
                    self
                )
                self.play_macro_action.setStatusTip("Play back the recorded sequence of inputs")
                self.play_macro_action.triggered.connect(self.parent().play_macro)
                self.play_macro_action.setEnabled(False)
                self.addAction(self.play_macro_action)


            case _:
                if Paths.debug:
                    print("Attempt to construct undefined toolbar:", tb_num)
