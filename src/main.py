# This Python file uses the following encoding: utf-8
import sys, json
from about_dialog import AboutDialog
from sequence_table import SequenceTable
from toolbar import Toolbar
from input_controller import InputController
# from clickThings import *
from paths import Paths
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
    QMainWindow, QStatusBar, QInputDialog, QFileDialog, QMessageBox
)

class MainWindow(QMainWindow):

    # Constructor
    def __init__(self, parent=None):

        super().__init__(parent)
        # Main Window config
        self.setWindowTitle("GUI Macro Tester")
        self.setFixedSize(970, 700)
        self.setWindowIcon(QIcon(Paths.icon("tw.png")))

        # Set up central VBox widget
        container = QWidget()
        self.sequence_table = SequenceTable(self)
        self.ms_table = SequenceTable(self, True)
        
        self.add_to_ms_button = QPushButton("Add to macro-sequence")
        self.add_to_ms_button.clicked.connect(self.add_seq_to_ms)
        self.add_to_ms_button.setIcon(QIcon(Paths.icon("arrow-090.png")))
        self.add_to_ms_button.setEnabled(False)
        
        centralVBox = QVBoxLayout(container)

        centralVBox.addWidget(self.sequence_table)
        centralVBox.addWidget(self.add_to_ms_button)
        centralVBox.addWidget(self.ms_table)
        self.setCentralWidget(container)

        # Toolbars
        self.tb1 = Toolbar(self, 1)
        self.addToolBar(self.tb1)
        self.tb2 = Toolbar(self, 2)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.tb2) 

        self.createMenus()

        self.input_controller = InputController(parent=self)


    # Copy current sequence into the macro-sequence
    def add_seq_to_ms(self):
        sequence_name, ok = QInputDialog.getText(self, 'Enter sequence name', 'Name of new sequence:')
        if ok and sequence_name:
            self.ms_table.import_current_seq(sequence_name)


    # Set up status bar and menu bar
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
            "About GUI sequence Tester",
            self,
        )
        about_action.setStatusTip(
            "Find out more about GUI sequence Tester"
        )
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)


    # Executes class imported from about_dialogue.py
    def about(self):
        dlg = AboutDialog()
        dlg.exec()


    # Load sequence file from disk
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
                self.input_controller.sequence = json.load(f)
            self.sequence_table.populate_table()
            self.tb1.play_sequence_action.setEnabled(True)
            self.tb1.delay_checkbox.setEnabled(True)
            self.tb1.delay_checkbox.setChecked(True)
            

    # Store currently loaded sequence as JSON file
    def save_file(self):
        if Paths.debug: print("\nEntering save_file")
        mac = self.input_controller.sequence
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

    
    # Remove all entries in sequence table
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
    
    # Enable or disable GUI elements based on whether a sequence is available
    def set_sequence_available(self, is_available):
        if is_available:
            self.tb1.play_sequence_action.setEnabled(True)
            self.tb1.delay_checkbox.setEnabled(True)
            self.tb1.return_checkbox.setEnabled(True)
            self.tb2.clear_table_action.setEnabled(True)
            self.add_to_ms_button.setEnabled(True)
        else:
            self.tb1.play_sequence_action.setEnabled(False)
            self.tb1.delay_checkbox.setEnabled(False)
            self.tb1.return_checkbox.setEnabled(False)
            self.tb2.clear_table_action.setEnabled(False)
            self.tb1.record_sequence_action.setText("Record sequence")
            self.add_to_ms_button(False)

    # Show ok/cancel dialog when about to discard an unsaved sequence
    def okay_to_clear_sequence(self):
        result = QMessageBox.question(
            None,
            "Discard current sequence?",
            "The current sequence has not been saved. Okay to proceed?",
            QMessageBox.Ok | QMessageBox.Cancel
        )
        return True if result == QMessageBox.Ok else False

    # Capture keyboard and mouse inputs and save to sequence table
    def record_sequence(self):
        if self.tb1.record_sequence_action.text().endswith('*'):
            if not self.okay_to_clear_sequence():
                return
            
        if self.input_controller.kb_listener.running:
            self.input_controller.stop()
            if len(self.input_controller.sequence) > 0:
                self.set_sequence_available(True)
                self.tb1.record_sequence_action.setText("Record sequence*")
            self.tb1.record_sequence_action.setStatusTip("Record a sequence of inputs")
        else:
            self.input_controller.start()
            self.tb1.record_sequence_action.setText("Stop Recording")
            self.tb1.record_sequence_action.setStatusTip("Finish recording the sequence of inputs")
    
    # Replay the currently loaded sequence
    def play_sequence(self):
        self.sequence_table.to_sequence()
        self.tb1.record_sequence_action.setEnabled(False)
        self.input_controller.play()
        self.tb1.record_sequence_action.setEnabled(True)
    

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
