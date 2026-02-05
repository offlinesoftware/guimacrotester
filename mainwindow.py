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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GUI Macro Tester")
        # label = QLabel(str(screenWidth) + " x " + str(screenHeight))

        self.setFixedSize(500, 800)

        ''''
        table = QTableWidget()
        table.setRowCount(20)
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Screen", "Area Name", "Position"])
        '''

        self.tree = QTreeWidget(self)
        self.tree.setColumnCount(2)
        self.tree.setColumnWidth(0, 350)
        self.tree.setHeaderLabels(["Screen area", "Position"])
        treedata = load_default()
        self.populateTree(treedata)

        # The `Qt` namespace has a lot of attributes to customize
        # widgets. See: http://doc.qt.io/qt-6/qt.html
        # label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(self.tree)

        self.createMenus()

    def populateTree(self, data):
        screens = []
        for k, v in data.items():
            screen = QTreeWidgetItem([k])
            for area in v:
                for areaName, coords in area.items():
                    pos = str(coords[0]) + ", " + str(coords[1])
                    name = QTreeWidgetItem([areaName, pos])
                    screen.addChild(name)
            screens.append(screen)

        '''
        items = []
        for key, values in data.items():
            item = QTreeWidgetItem([key])
            for value in values:
                print(value)
                print(type(value))
                ext = value.values()
                child = QTreeWidgetItem([value, ext])
                item.addChild(child)
            items.append(item)

        tree.insertTopLevelItems(0, items)
        '''
        self.tree.insertTopLevelItems(0, screens)

    def createMenus(self):

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
        print("click", s)

    def go_button_clicked(self):
        program_name, ok = QInputDialog.getText(self, 'Enter progam name', 'Name of new program:')
        if ok and program_name:
            new_program(program_name)

    def detect_position(self):
        print(getattr(self, "pos")())




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
