from paths import Paths
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QToolBar, QCheckBox, QDoubleSpinBox

class Toolbar(QToolBar):
    def __init__(self, parent, tb_num):
        super(Toolbar, self).__init__(parent)
        self.setIconSize(QSize(16, 16))
        match tb_num:
            case 1:
                # 'Record sequence' button
                self.record_sequence_action = QAction(
                    # QIcon(Paths.icon("plus.png")), 
                    "Record sequence",
                    self
                )
                self.record_sequence_action.setStatusTip("Record a sequence of inputs")
                self.record_sequence_action.triggered.connect(self.parent().record_sequence)
                self.addAction(self.record_sequence_action)
                
                # 'Play sequence' button
                self.play_sequence_action = QAction(
                    # QIcon(Paths.icon("plus.png")), 
                    "Play sequence",
                    self
                )
                self.play_sequence_action.setStatusTip("Play back the recorded sequence of inputs")
                self.play_sequence_action.triggered.connect(self.parent().play_sequence)
                self.play_sequence_action.setEnabled(False)
                self.addAction(self.play_sequence_action)

                self.addSeparator()

                self.delay_spin = QDoubleSpinBox()
                self.delay_spin.setRange(0, 1000)
                self.delay_spin.setDecimals(0)
                self.delay_spin.setSingleStep(50)
                self.delay_spin.setFixedWidth(100)
                self.delay_spin.setValue(100)
                self.delay_spin.setEnabled(False)


                self.delay_checkbox = QCheckBox("Delay (ms) :")
                
                self.delay_checkbox.stateChanged.connect(self.on_state_changed)
                self.delay_checkbox.setChecked(True)
                self.delay_checkbox.setEnabled(False)
                self.addWidget(self.delay_checkbox)
                

                self.addWidget(self.delay_spin)

                self.addSeparator()
                self.return_checkbox = QCheckBox("Return mouse cursor after execution")
                self.return_checkbox.setChecked(True)
                self.return_checkbox.setEnabled(False)
                self.addWidget(self.return_checkbox)
                
            case 2:
                # 'Clear table' button
                self.clear_table_action = QAction(
                    # QIcon(Paths.icon("ui-tab--plus.png")), 
                    "Clear sequence",
                    self
                )
                self.clear_table_action.setStatusTip("Clear the current sequence shown in the top table")
                self.clear_table_action.triggered.connect(self.parent().clear_table)
                self.clear_table_action.setEnabled(False)
                self.addAction(self.clear_table_action)

                # Move up button
                self.move_up_action = QAction(
                    # QIcon(Paths.icon("ui-tab--plus.png")), 
                    "Move up",
                    self
                )
                self.move_up_action.setStatusTip("Move one row of the input sequence table upwards")
                self.move_up_action.triggered.connect(self.parent().sequence_table.move_up)
                self.addAction(self.move_up_action)

                # Move down button
                self.move_down_action = QAction(
                    # QIcon(Paths.icon("ui-tab--plus.png")), 
                    "Move down",
                    self
                )
                self.move_down_action.setStatusTip("Move one row of the input sequence table downwards")
                self.move_down_action.triggered.connect(self.parent().sequence_table.move_down)
                self.addAction(self.move_down_action)

            case _:
                if Paths.debug:
                    print("Attempt to construct undefined toolbar:", tb_num)

    def on_state_changed(self, state):
        if state == Qt.CheckState.Checked.value:
            self.delay_spin.setEnabled(True)
        else:
            self.delay_spin.setEnabled(False)