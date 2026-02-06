# This Python file uses the following encoding: utf-8
import sys
import pyautogui as pag
from clickThings import *
from util import load_default
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QApplication, QCheckBox, QTreeWidget,
    QLabel, QMainWindow, QStatusBar, QToolBar, QInputDialog, QTreeWidgetItem
)

class MainWindow(QMainWindow):
    """GUI Macro Tester main window class"""

    def __init__(self, parent=None):
        """Constructor"""

        super().__init__(parent)
        self.setWindowTitle("GUI Macro Tester")
        self.setFixedSize(500, 800)

        # Screen co-ordinates tree
        self.tree = QTreeWidget(self)
        self.tree.setColumnCount(2)
        self.tree.setColumnWidth(0, 350)
        self.tree.setHeaderLabels(["Screen area", "Position"])
        treedata = load_default()
        self.populateTree(treedata)

        self.setCentralWidget(self.tree)

        self.createMenus()


    def populateTree(self, data):
        """
        Populate tree view from JSON data
        
        :param data: Dict generated from JSON file
        """
        screens = []
        for k, v in data.items():
            screen = QTreeWidgetItem([k])
            for area in v:
                for areaName, coords in area.items():
                    pos = str(coords[0]) + ", " + str(coords[1])
                    name = QTreeWidgetItem([areaName, pos])
                    screen.addChild(name)
            screens.append(screen)
        self.tree.insertTopLevelItems(0, screens)


    def createMenus(self):
        """Create menus and toolbars"""

        # Toolbar
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        # Go button
        button_action = QAction(QIcon("bug.png"), "&New program", self)
        button_action.setStatusTip("Run current script")
        button_action.triggered.connect(self.go_button_clicked)
        button_action.setCheckable(True)
        button_action.setShortcut(QKeySequence("Ctrl+p"))
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        # Debug button
        button_action2 = QAction(QIcon("bug.png"), "Your &button2", self)
        button_action2.setStatusTip("This is your button2")
        button_action2.triggered.connect(self.detect_position)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)

        # Resolution label
        resolution = str(screenWidth) + " x " + str(screenHeight)
        toolbar.addWidget(QLabel(resolution))
        toolbar.addWidget(QCheckBox())

        # Bit at the bottom for tooltips
        self.setStatusBar(QStatusBar(self))

        # Menu bar
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addAction(button_action)
        file_menu.addSeparator()
        file_submenu = file_menu.addMenu("Submenu")
        file_submenu.addAction(button_action2)


    def toolbar_button_clicked(self, s):
        """Debug function for button click"""

        print("click", s)


    def go_button_clicked(self):
        """
        Execute current macro sequence
        """
        
        program_name, ok = QInputDialog.getText(self, 'Enter progam name', 'Name of new program:')
        if ok and program_name:
            new_program(program_name)

    
    def detect_position(self):
        """Debug function to show main window co-ordinates"""

        print(getattr(self, "pos")())


# Run the application
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()

    app.setStyleSheet("""
        QWidget {
            font-size: 16px;

        }

    """)
    window.show()

    sys.exit(app.exec())
