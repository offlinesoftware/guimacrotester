# This Python file uses the following encoding: utf-8
import sys
from about_dialog import AboutDialog
from screen_tree import ScreenTree
from toolbar import Toolbar
from input_controller import InputController
# from clickThings import *
from paths import Paths
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QApplication,
    QMainWindow, QStatusBar, QInputDialog, QFileDialog
)

#:
#  name: MainWindow
#  description: Instance of QMainWindow
#  attributes:
#    tb1: top toolbar
#    tb2: left side toolbar
#  constructor:
#    params: implicit only

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        """Constructor"""

        super().__init__(parent)
        self.setWindowTitle("GUI Macro Tester")
        self.setFixedSize(500, 750)

        self.tree = ScreenTree()

        self.setCentralWidget(self.tree)

        # Toolbars
        self.tb1 = Toolbar(self, 1)
        self.addToolBar(self.tb1)
        self.tb2 = Toolbar(self, 2)
        self.addToolBar(Qt.LeftToolBarArea, self.tb2)

        self.createMenus()

        self.input_controller = InputController(parent=self)

    def createMenus(self):

        # Bit at the bottom for tooltips
        self.setStatusBar(QStatusBar(self))

        # Menu bar
        menu = self.menuBar()
        
        file_menu = self.menuBar().addMenu("&File")

        open_file_action = QAction(
            QIcon(Paths.icon("disk--arrow.png")),
            "Open file...",
            self,
        )
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction(
            QIcon(Paths.icon("disk--pencil.png")),
            "Save sequence as...",
            self,
        )
        save_file_action.setStatusTip("Save current sequence to file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        help_menu = self.menuBar().addMenu("&Help")

        about_action = QAction(
            QIcon(Paths.icon("question.png")),
            "About GUI Macro Tester",
            self,
        )
        about_action.setStatusTip(
            "Find out more about GUI Macro Tester"
        )  # Hungry!
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)


    def about(self):
        dlg = AboutDialog()
        dlg.exec()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "",
            "JavaSript Object Notation (*.json);;"
            "All files (*.*)",
        )

        if filename:
            with open(filename, "r") as f:
                html = f.read()

            self.browser.setHtml(html)
            self.urlbar.setText(filename)


    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Page As",
            "",
            "Hypertext Markup Language (*.htm *.html);;"
            "All files (*.*)",
        )

        if filename:
            # Define callback method to handle the write.
            def writer(html):
                with open(filename, "w") as f:
                    f.write(html)

            self.browser.page().toHtml(writer)

    
    #
    # Member functions
    #
    
    def add_screen(self):
        screen_name, ok = QInputDialog.getText(self, 'Enter screen name', 'Name of new screen:')
        if ok and screen_name:
            self.tree.new_screen(screen_name)

    def record_macro(self):
        if self.input_controller.kb_listener.running:
            self.input_controller.stop()
            self.tb1.play_macro_action.setEnabled(True)
            self.tb1.delay_checkbox.setEnabled(True)
            self.tb1.delay_checkbox.setChecked(True)
        else:
            self.input_controller.start()
    
    #:
    #  name: play_macro
    #  description: This is an example zensical comment
    #  params:
    #    self: the MainWindow object
    #  returns: nothing (needn't always bother stating this)

    def play_macro(self):
        self.tb1.record_macro_action.setEnabled(False)
        self.input_controller.play()
        self.tb1.record_macro_action.setEnabled(True)
    

# Run the application
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.setStyleSheet("""
        QWidget {
            font-size: 16px;

        }
        QCheckBox {
            padding-left: 5px;
            padding-right: 2px;
        }

    """)
    window.show()

    sys.exit(app.exec())
