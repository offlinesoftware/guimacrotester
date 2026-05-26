# This Python file uses the following encoding: utf-8
import sys, json
from about_dialog import AboutDialog
from screen_tree import ScreenTree
from sequence_table import SequenceTable
from toolbar import Toolbar
from input_controller import InputController
# from clickThings import *
from paths import Paths
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
    QMainWindow, QStatusBar, QInputDialog, QFileDialog, QMessageBox
)

class MainWindow(QMainWindow):

    # Constructor
    def __init__(self, parent=None):
        # Constructor

        super().__init__(parent)
        self.setWindowTitle("GUI Macro Tester")
        self.setFixedSize(960, 700)

        self.tree = ScreenTree()
        container = QWidget()
        self.sequence_table = SequenceTable(self)
        centralVBox = QVBoxLayout(container)

        centralVBox.addWidget(self.sequence_table)
        centralVBox.addWidget(self.tree)
        self.setCentralWidget(container)

        # Toolbars
        self.tb1 = Toolbar(self, 1)
        self.addToolBar(self.tb1)
        self.tb2 = Toolbar(self, 2)
        # Qt.LeftToolBarArea works fine but PyLance whinges about it
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.tb2) 

        self.createMenus()

        self.input_controller = InputController(parent=self)

    
    def createMenus(self):

        # Bit at the bottom for tooltips
        self.setStatusBar(QStatusBar(self))

        # Menu bar
        menu = self.menuBar()

        # > File menu        
        file_menu = self.menuBar().addMenu("&File")

        # > > Open file
        open_file_action = QAction(
            QIcon(Paths.icon("disk--arrow.png")),
            "Open file...",
            self,
        )
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        # > > Save file
        save_file_action = QAction(
            QIcon(Paths.icon("disk--pencil.png")),
            "Save sequence as...",
            self,
        )
        save_file_action.setStatusTip("Save current sequence to file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        # > Help menu
        help_menu = self.menuBar().addMenu("&Help")

        # > > About 
        about_action = QAction(
            QIcon(Paths.icon("question.png")),
            "About GUI Macro Tester",
            self,
        )
        about_action.setStatusTip(
            "Find out more about GUI Macro Tester"
        )
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
            "TW Sequence (*.tws);;"
            "All files (*.*)",
        )

        if filename:
            with open(filename, "r") as f:
                self.input_controller.macro = json.load(f)
            self.sequence_table.populate_table()
            self.tb1.play_macro_action.setEnabled(True)
            self.tb1.delay_checkbox.setEnabled(True)
            self.tb1.delay_checkbox.setChecked(True)
            

    # Store currently loaded macro as JSON file
    def save_file(self):
        if Paths.debug: print("\nEntering save_file")
        mac = self.input_controller.macro
        if len(mac) == 0:
            if Paths.debug: print("No sequence to save")
            return
        else:
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Save Sequence As",
                "",
                "TW Sequence (*.tws);;"
                "All files (*.*)",
            )

            if filename:
                with open(filename, "w") as f:
                    json.dump(mac, f)


    def add_screen(self):
        screen_name, ok = QInputDialog.getText(self, 'Enter screen name', 'Name of new screen:')
        if ok and screen_name:
            self.tree.new_screen(screen_name)
    
    def clear_table(self):
        result = QMessageBox.question(
            self,
            "Confirm clear",
            "Really clear the current sequence?",
            QMessageBox.Ok | QMessageBox.Cancel
        )
        if result == QMessageBox.Ok:
            print("Clearing the current sequence")
            self.sequence_table.clearContents()
            self.set_sequence_available(False)
        elif result == QMessageBox.Cancel:
            if Paths.debug:
                print("Cancelled clearing the sequence")
            return
    
    def set_sequence_available(self, is_available):
        if is_available:
            self.tb1.play_macro_action.setEnabled(True)
            self.tb1.delay_checkbox.setEnabled(True)
            self.tb1.return_checkbox.setEnabled(True)
            self.tb2.clear_table_action.setEnabled(True)
        else:
            self.tb1.play_macro_action.setEnabled(False)
            self.tb1.delay_checkbox.setEnabled(False)
            self.tb1.return_checkbox.setEnabled(False)
            self.tb2.clear_table_action.setEnabled(False)
            self.tb1.record_macro_action.setText("Record macro")

    def record_macro(self):
        if self.input_controller.kb_listener.running:
            self.input_controller.stop()
            if len(self.input_controller.macro) > 0:
                self.set_sequence_available(True)
                self.tb1.record_macro_action.setText("Record macro*")
            self.tb1.record_macro_action.setStatusTip("Record a sequence of inputs")
        else:
            self.input_controller.start()
            self.tb1.record_macro_action.setText("Stop Recording")
            self.tb1.record_macro_action.setStatusTip("Finish recording the sequence of inputs")
    
    # Replay the currently loaded macro
    def play_macro(self):
        self.sequence_table.to_macro()
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
