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
                add_screen_action = QAction(
                    # QIcon(Paths.icon("ui-tab--plus.png")), 
                    "Add new screen",
                    self
                )
                add_screen_action.setStatusTip("Add a new group of screen co-ordinates")
                add_screen_action.triggered.connect(self.parent().add_screen)
                self.addAction(add_screen_action)

                # 'Record macro' button
                record_macro_action = QAction(
                    # QIcon(Paths.icon("plus.png")), 
                    "Record macro",
                    self
                )
                record_macro_action.setStatusTip("Add the co-ordinates of a position to the selected screen group")
                record_macro_action.triggered.connect(self.parent().record_macro)
                self.addAction(record_macro_action)

            case _:
                if Paths.debug:
                    print("Attempt to construct undefined toolbar:", tb_num)
