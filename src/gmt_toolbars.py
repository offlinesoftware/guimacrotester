from paths import Paths
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QToolBar, QCheckBox, QDoubleSpinBox, QWidget, QSizePolicy
)

# Toolbars for GUI Macro Tester
# (not intended for reuse)
class Toolbar(QToolBar):

    # Constructor
    def __init__(self, parent, tb_instance):
        super().__init__(parent)
        self.setIconSize(QSize(16, 16))
        self.setMovable(False)
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        
        if tb_instance == "top_horizontal":
            self.build_top_tb()
        
        elif tb_instance == "left_vertical":
            self.build_left_tb()

        elif Paths.debug:
            print("Attempt to construct undefined toolbar:", tb_instance)
    

    # Top horizontal toolbar
    def build_top_tb(self):
        
        # 'Record sequence' button
        self.record_sequence_action = self.create_action(
            text="Record sequence", slot=self.parent().record_sequence,
            enabled=True,           tip="Record a sequence of inputs",
            icon="control-record.png"
        )

        # Reduce misclicks
        self.addSeparator()

        # 'Play sequence' button
        self.play_sequence_action = self.create_action(
            text="Play sequence",   slot=self.parent().play_sequence,
            enabled=False,          tip="Play back the recorded sequence of inputs",
            icon="control.png"
        )

        # Separate play button from delay checkbox
        self.add_spacer()

        # Spinbox for delay value
        self.delay_spin = QDoubleSpinBox(
            value=100,      minimum=0,  maximum=1000, 
            singleStep=50,  decimals=0
        )
        self.delay_spin.setEnabled(False)
        self.delay_spin.setFixedWidth(100)

        # Checkbox to toggle use of delay value
        self.delay_checkbox = self.create_checkbox(
            text="Delay (ms) :",    checked=True,
            enabled=False,          slot=self.delay_spin.setEnabled
        )
        self.addWidget(self.delay_checkbox)

        # Draw spinbox after checkbox but need to declare it before 
        # because of checkbox slot is self.delay_spin.setEnabled
        self.addWidget(self.delay_spin)

        # Separate mouse return checkbox from delay spinbox
        self.add_spacer()

        # Checkbox for mouse return
        self.return_checkbox = self.create_checkbox(
            text="Return mouse cursor after execution", 
            checked=True,   enabled=False
        )
        self.addWidget(self.return_checkbox)

        # End of toolbar
        self.addSeparator()
            
    
    # Left horizontal toolbar
    def build_left_tb(self):

        self.setOrientation(Qt.Vertical)
        self.add_spacer()
        self.setFixedHeight(600)

        # Sequence editor 'Clear table' button
        self.clear_table_action = self.create_action(
            text="Clear sequence",  slot=self.parent().clear_table,
            enabled=False,          tip="Clear the current sequence shown in the top table"
        )

        # Sequence editor 'Move up' button
        self.move_up_action = self.create_action(
            text="Move up", slot=self.parent().sequence_table.move_up,
            enabled=False,  tip="Move one row of the input sequence table upwards"
        )

        # Move down button
        self.move_down_action = self.create_action(
            text="Move down",   slot=self.parent().sequence_table.move_down,
            enabled=False,      tip="Move one row of the input sequence table downwards"
        )

        # Spacing between top and bottom controls
        self.add_spacer()
        self.addSeparator()
        self.add_spacer()
        
        # Macro-sequence 'Move up' button
        self.ms_up_action = self.create_action(
            text = "Move up",   slot=self.parent().ms_table.move_up,
            enabled=False,      tip="Move one row of the macro-sequence table upwards"
        )

        # Macro-sequence Move Down button
        self.ms_down_action = self.create_action(
            text="Move down",   slot=self.parent().ms_table.move_down,
            enabled=False,      tip="Move one row of the macro-sequence table downwards"
        )

        self.add_spacer()

        # Play macro-sequence button
        self.play_ms_action = self.create_action(
            text="PLAY\nMACRO\nSEQUENCE",   slot=self.parent().play_ms,
            enabled=False,      tip="Play back all inputs in the macro-sequence"
        )
        big_button = self.widgetForAction(self.play_ms_action)
        big_button.setStyleSheet('''
            border: 1px solid gray;
            padding: 2px;
            font: bold;
        '''
        )


    # Button action builder
    def create_action(self, text, slot, enabled, tip, icon=None):
        act = self.addAction(QIcon(Paths.icon(icon)) if icon else QIcon(), text, slot)
        act.setStatusTip(tip)
        act.setEnabled(enabled)
        return act
    

    # Checkbox builder
    def create_checkbox(self, text, checked, enabled, slot=None):
        cb = QCheckBox(text)
        cb.setChecked(checked)
        cb.setEnabled(enabled)
        if slot:
            cb.stateChanged.connect(slot)
        return cb


    # Spacer builder
    def add_spacer(self):
        spcr = QWidget()
        if self.orientation() == Qt.Horizontal:
            spcr.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        else:
            spcr.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.addWidget(spcr)
