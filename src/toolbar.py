from paths import Paths
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QToolBar, QCheckBox, QDoubleSpinBox, QWidget, QSizePolicy

class Toolbar(QToolBar):

    # Constructor
    def __init__(self, parent, tb_num):
        super().__init__(parent)
        self.setIconSize(QSize(16, 16))
        
        match tb_num:
        
            # tb_num=1 sets up the top horizontal toolbar
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

                # Separate play button from delay checkbox
                self.addSeparator()

                # Spinbox for delay value
                self.delay_spin = QDoubleSpinBox()
                self.delay_spin.setRange(0, 1000)
                self.delay_spin.setDecimals(0)
                self.delay_spin.setSingleStep(50)
                self.delay_spin.setFixedWidth(100)
                self.delay_spin.setValue(100)
                self.delay_spin.setEnabled(False)
                
                # Checbox to toggle use of delay value
                self.delay_checkbox = QCheckBox("Delay (ms) :")
                self.delay_checkbox.stateChanged.connect(self.delay_state_changed)
                self.delay_checkbox.setChecked(True)
                self.delay_checkbox.setEnabled(False)
                self.addWidget(self.delay_checkbox)
                
                # Draw spinbox after checkbox but need to delare it before 
                # because of stateChanged.connect(self.delay_state_changed)
                self.addWidget(self.delay_spin)

                # Separate mouse return checkbox from delay spinbox
                self.addSeparator()

                # Checkbox for mouse return
                self.return_checkbox = QCheckBox("Return mouse cursor after execution")
                self.return_checkbox.setChecked(True)
                self.return_checkbox.setEnabled(False)
                self.addWidget(self.return_checkbox)
            

            # tb_num=2 sets up the left side vertical toolbar
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

                # Spacing between top and bottom controls
                spacer1 = QWidget()
                spacer1.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
                self.addWidget(spacer1)

                self.addSeparator()

                spacer2 = QWidget()
                spacer2.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
                self.addWidget(spacer2)

                # Macro-sequence Move Up button
                self.ms_up_action = QAction(
                    # QIcon(Paths.icon("ui-tab--plus.png")), 
                    "Move up",
                    self
                )
                self.ms_up_action.setStatusTip("Move one row of the macro-sequence table upwards")
                self.ms_up_action.triggered.connect(self.parent().ms_table.move_up)
                self.addAction(self.ms_up_action)

                # Macro-sequence Move Down button
                self.ms_down_action = QAction(
                    # QIcon(Paths.icon("ui-tab--plus.png")), 
                    "Move down",
                    self
                )
                self.ms_down_action.setStatusTip("Move one row of the macro-sequence table downwards")
                self.ms_down_action.triggered.connect(self.parent().ms_table.move_down)
                self.addAction(self.ms_down_action)

                self.setFixedHeight(500)
                
            case _:
                if Paths.debug:
                    print("Attempt to construct undefined toolbar:", tb_num)


    # Called when the delay checkbox is clicked
    def delay_state_changed(self, state):
        if state == Qt.CheckState.Checked.value:
            self.delay_spin.setEnabled(True)
        else:
            self.delay_spin.setEnabled(False)
            