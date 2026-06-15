from PySide6.QtGui import QAction
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QToolBar, QCheckBox, QDoubleSpinBox,
    QWidget, QSizePolicy
)

class Toolbar(QToolBar):

    def __init__(self, name, config, parent=None):
        super().__init__(name, parent)
        self.setIconSize(QSize(16, 16))

        self._build(config)

    def _build(self, config):
        """
        Config is a dict describing what should go in the toolbar.
        """

        for item in config:

            if item == "separator":
                self.addSeparator()

            elif item == "spacer":
                spacer = QWidget()
                spacer.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
                self.addWidget(spacer)

            elif isinstance(item, QAction):
                self.addAction(item)

            elif item == "delay_controls":
                self._add_delay_controls()

            elif item == "return_checkbox":
                self._add_return_checkbox()

    def _add_delay_controls(self):
        self.delay_spin = QDoubleSpinBox()
        self.delay_spin.setRange(0, 1000)
        self.delay_spin.setDecimals(0)
        self.delay_spin.setSingleStep(50)
        self.delay_spin.setFixedWidth(100)
        self.delay_spin.setValue(100)
        self.delay_spin.setEnabled(False)

        self.delay_checkbox = QCheckBox("Delay (ms) :")
        self.delay_checkbox.setChecked(True)
        self.delay_checkbox.setEnabled(False)
        self.delay_checkbox.stateChanged.connect(self._delay_state_changed)

        self.addWidget(self.delay_checkbox)
        self.addWidget(self.delay_spin)

    def _add_return_checkbox(self):
        self.return_checkbox = QCheckBox(
            "Return mouse cursor after execution"
        )
        self.return_checkbox.setChecked(True)
        self.return_checkbox.setEnabled(False)
        self.addWidget(self.return_checkbox)

    def _delay_state_changed(self, state):
        self.delay_spin.setEnabled(
            state == Qt.CheckState.Checked.value
        )

'''
# Then in MainWindow:

def create_actions(self):
    self.record_sequence_action = QAction("Record sequence", self)
    self.record_sequence_action.setStatusTip("Record a sequence of inputs")
    self.record_sequence_action.triggered.connect(self.record_sequence)

    self.play_sequence_action = QAction("Play sequence", self)
    self.play_sequence_action.setStatusTip(
        "Play back the recorded sequence of inputs"
    )
    self.play_sequence_action.setEnabled(False)
    self.play_sequence_action.triggered.connect(self.play_sequence)

    self.clear_table_action = QAction("Clear sequence", self)
    self.clear_table_action.setEnabled(False)
    self.clear_table_action.triggered.connect(self.clear_table)

    self.move_up_action = QAction("Move up", self)
    self.move_up_action.triggered.connect(self.sequence_table.move_up)

    self.move_down_action = QAction("Move down", self)
    self.move_down_action.triggered.connect(self.sequence_table.move_down)

    self.ms_up_action = QAction("Move up", self)
    self.ms_up_action.triggered.connect(self.ms_table.move_up)

    self.ms_down_action = QAction("Move down", self)
    self.ms_down_action.triggered.connect(self.ms_table.move_down)


# Toolbar creation:

def create_toolbars(self):
    top_config = [
        self.record_sequence_action,
        self.play_sequence_action,
        "separator",
        "delay_controls",
        "separator",
        "return_checkbox",
    ]

    left_config = [
        self.clear_table_action,
        self.move_up_action,
        self.move_down_action,
        "spacer",
        "separator",
        "spacer",
        self.ms_up_action,
        self.ms_down_action,
    ]

    self.top_toolbar = Toolbar("Top", top_config, self)
    self.left_toolbar = Toolbar("Left", left_config, self)

    self.addToolBar(self.top_toolbar)
    self.addToolBar(Qt.LeftToolBarArea, self.left_toolbar)
'''