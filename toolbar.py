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

                # 'Add new position' button
                add_position_action = QAction(
                    # QIcon(Paths.icon("plus.png")), 
                    "Add new position",
                    self
                )
                add_position_action.setStatusTip("Add the co-ordinates of a position to the selected screen group")
                add_position_action.triggered.connect(self.parent().add_position)
                self.addAction(add_position_action)

            case _:
                print("Attempt to construct undefined toolbar:", tb_num)
