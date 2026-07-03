# This Python file uses the following encoding: utf-8

''' GUI MACRO TESTER MAIN CLASS
Compile with:
pyinstaller -F -w --clean --paths=src src/main.py

Resources file built from .qrc using:
pyside6-rcc resources.qrc -o src/resources.py
'''
import resources

# Project imports
from about_dialog import AboutDialog
from input_controller import InputController
from ms_table import MacroSeqTable
from sequence_table import SequenceTable
from paths import Paths
from gmt_toolbars import Toolbar

# External imports
import sys, json, ast
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QKeySequence
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
    QMainWindow, QStatusBar, QInputDialog, QFileDialog, QMessageBox
)

class MainWindow(QMainWindow):

    # Constructor
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Main window config
        self.titles = {
            "normal":       "GUI Macro Tester", 
            "recording":    "GUI Macro Tester    RECORDING"
        }

        Paths.load_icons()

        self.setWindowTitle(self.titles["normal"])
        self.setFixedSize(1000, 700)
        self.setWindowIcon(QIcon(Paths.icon("tw.png")))
        self.flash_timer = QTimer()
        self.flash_timer.timeout.connect(self.flash_title)

        # Set up central VBox widget
        container = QWidget()
        self.sequence_table = SequenceTable(self)
        self.ms_table = MacroSeqTable(self)
        
        self.add_to_ms_button = QPushButton(" Add to macro-sequence")
        self.add_to_ms_button.clicked.connect(self.add_seq_to_ms)
        self.add_to_ms_button.setIcon(Paths.get("down_triangle"))
        self.add_to_ms_button.setEnabled(False)
        
        centralVBox = QVBoxLayout(container)

        centralVBox.addWidget(self.sequence_table)
        centralVBox.addWidget(self.add_to_ms_button)
        centralVBox.addWidget(self.ms_table)
        self.setCentralWidget(container)

        # Toolbars
        self.top_toolbar = Toolbar(self, "top_horizontal")
        self.addToolBar(self.top_toolbar)
        self.left_toolbar = Toolbar(self, "left_vertical")
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.left_toolbar)
        self.createMenus()

        # Initialise Pynput
        self.input_controller = InputController(self)
        self.input_controller.populate_sequence.connect(
            self.sequence_table.populate_table
        )


    # Alternate the title of the windowfr
    def flash_title(self):
        if self.windowTitle() == self.titles["normal"]:
            self.setWindowTitle(self.titles["recording"])
        else:
            self.setWindowTitle(self.titles["normal"])

    # Copy current sequence into the macro-sequence
    def add_seq_to_ms(self):
        sequence_name, ok = QInputDialog.getText(self, 'Enter sequence name', 'Name of new sequence:')
        if ok and sequence_name:
            self.ms_table.import_current_seq(sequence_name)
            self.set_ms_available(True)


    # Set up status bar and menu bar
    def createMenus(self):

        # Bit at the bottom for tooltips
        self.setStatusBar(QStatusBar(self))

        # Menu bar
        menu = self.menuBar()

        # > File menu        
        file_menu = menu.addMenu("&File")

        # > > Open sequence file
        self.open_file_action = self.menu_action(
            menu=file_menu,         text="Open sequence...", 
            slot=self.open_file,    tip="Load an input sequence from a TWS file",
            enabled=True,           icon="open_seq"
        )

        # > > Save sequence file
        self.save_file_action = self.menu_action(
            menu=file_menu,         text="Save sequence as...", 
            slot=self.save_file,    tip="Save current sequence to file",
            enabled=False,          icon="save_seq"
        )

        # > > Macro-sequence bits
        file_menu.addSeparator()

        # > > Open macro-sequence
        self.open_ms_action = self.menu_action(
            menu=file_menu,         text="Open macro-sequence...", 
            slot=self.open_macro,   tip="Load a macro-sequence from a TWM file",
            enabled=True,           icon="open_mac"
        )

        # > > Save macro-sequence
        self.save_ms_action = self.menu_action(
            menu=file_menu,         text="Save macro-sequence as...", 
            slot=self.save_macro,   tip="Save current macro-sequence to file",
            enabled=False,          icon="save_mac"
        )

        # > Help menu
        help_menu = self.menuBar().addMenu("&Help")

        # > > About 
        self.about_action = self.menu_action(
            menu=help_menu,     text="About GUI Macro Tester", 
            slot=self.about,    tip="Find out more about GUI Macro Tester",
            enabled=True,       icon="question"
        )


    # Menu button action builder
    def menu_action(self, menu, text, slot, tip, enabled, icon=None):
        # ma = menu.addAction(QIcon(Paths.icon(icon)) if icon else QIcon(), text, slot)
        ma = menu.addAction(QIcon(Paths.get(icon)) if icon else QIcon(), text, slot)
        ma.setStatusTip(tip)
        ma.setEnabled(enabled)
        return ma

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
            self.set_sequence_available(True)


    # Load macro-sequence file from disk
    def open_macro(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "",
            "TW Sequence (*.twm);;"
            "All files (*.*)",
        )
        if filename:
            with open(filename, "r") as f:
                self.ms_table.populate_table(json.load(f))
            

    # Store currently loaded sequence as JSON file
    def save_file(self):
        if Paths.debug:
            print("\nEntering save_file")
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
                    self.top_toolbar.record_sequence_action.setText("Record sequence")
    
    
    # Store macro-sequence as JSON file
    def save_macro(self):
        if Paths.debug:
            print("\nEntering save_macro")
        
        macList = []
        for r in range(self.ms_table.rowCount()):
            name = self.ms_table.item(r, 0).text()
            seq = ast.literal_eval(self.ms_table.item(r, 1).text())
            macList.append([name, seq])
        
        if len(macList) == 0:
            if Paths.debug: print("No macro-sequence to save")
            return
        
        else:
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Save Macro-Sequence As",
                "",
                "TW Macro-Sequence (*.twm);;"
                "All files (*.*)",
            )

            if filename:
                with open(filename, "w") as f:
                    json.dump(macList, f)

    
    # Remove all entries in sequence table
    def clear_table(self):
        result = QMessageBox.question(
            self,
            "Confirm clear",
            "Really clear the current sequence?",
            QMessageBox.Ok | QMessageBox.Cancel
        )
        if result == QMessageBox.Ok:
            if Paths.debug: print("Clearing the current sequence")
            self.sequence_table.clearContents()
            self.set_sequence_available(False)
        elif result == QMessageBox.Cancel:
            if Paths.debug:
                print("Cancelled clearing the sequence")
            return
    

    # Remove the currently selected row of the macro-sequence table
    def delete_ms_row(self):
        self.ms_table.removeRow(self.ms_table.currentRow())
        if self.ms_table.rowCount() == 0:
            self.set_ms_available(False)
    

    # Enable or disable GUI elements based on whether a sequence is available
    def set_sequence_available(self, is_available):
        for widget in [
            # Menu bar
            self.save_file_action,

            # Top toolbar
            self.top_toolbar.play_sequence_action, self.top_toolbar.delay_checkbox, 
            self.top_toolbar.delay_spin, self.top_toolbar.return_checkbox,

            # Left toolbar
            self.left_toolbar.clear_table_action, self.left_toolbar.move_up_action, self.left_toolbar.move_down_action, 

            # Central VBox
            self.add_to_ms_button
        ]: widget.setEnabled(is_available)
        if is_available:
            self.top_toolbar.delay_spin.setEnabled(self.top_toolbar.delay_checkbox.isChecked())
        else:
            self.top_toolbar.record_sequence_action.setText("Record sequence")


    # Enable or disable GUI elements based on whether a macro-sequence is available
    def set_ms_available(self, is_available):
        for widget in [
            # Menu bar
            self.save_ms_action,

            # Top toolbar
            self.top_toolbar.delay_checkbox, self.top_toolbar.delay_spin, self.top_toolbar.return_checkbox,

            # Left toolbar
            self.left_toolbar.ms_up_action, self.left_toolbar.ms_down_action, 
            self.left_toolbar.play_ms_action, self.left_toolbar.delete_ms_row_action
        ]: widget.setEnabled(is_available)


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
        if self.top_toolbar.record_sequence_action.text().endswith('*'):
            if not self.okay_to_clear_sequence():
                return
        
        # Stop recording
        if self.input_controller.kb_listener.running:
            self.input_controller.stop()
            if len(self.input_controller.sequence) > 0:
                self.set_sequence_available(True)
                self.top_toolbar.record_sequence_action.setText("Record sequence*")
            else:
                self.top_toolbar.record_sequence_action.setText("Record sequence")
            self.top_toolbar.record_sequence_action.setStatusTip("Record a sequence of inputs")
            self.flash_timer.stop()
            self.setWindowTitle(self.titles["normal"])
        
        # Start recording
        else:
            self.flash_timer.start(500)
            self.sequence_table.clearContents()
            self.set_sequence_available(False)
            self.input_controller.start()
            self.top_toolbar.record_sequence_action.setText("Stop Recording")
            self.top_toolbar.record_sequence_action.setStatusTip("Finish recording the sequence of inputs")
    

    # Replay the currently loaded sequence
    def play_sequence(self):
        self.sequence_table.to_sequence()
        self.top_toolbar.record_sequence_action.setEnabled(False)
        self.input_controller.play(
            use_delay = self.top_toolbar.delay_checkbox.isChecked(), 
            delay_value = self.top_toolbar.delay_spin.value(), 
            return_mouse = self.top_toolbar.return_checkbox.isChecked()
        )
        self.top_toolbar.record_sequence_action.setEnabled(True)

    
    # Replace the entire macro-sequence
    def play_ms(self):
        self.top_toolbar.record_sequence_action.setEnabled(False)
        
        for r in range(self.ms_table.rowCount()):
            mac = ast.literal_eval(self.ms_table.item(r, 1).text())
            self.window().input_controller.sequence = mac    
            self.input_controller.play(
                use_delay = self.top_toolbar.delay_checkbox.isChecked(), 
                delay_value = self.top_toolbar.delay_spin.value(), 
                return_mouse = self.top_toolbar.return_checkbox.isChecked()
            )
        
        self.top_toolbar.record_sequence_action.setEnabled(True)
    

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
        
        QToolButton {
            min-width: 150px;
        }

    """)
    
    window.show()
    sys.exit(app.exec())
