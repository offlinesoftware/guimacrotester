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
                # 'Record macro' button
                self.record_macro_action = QAction(
                    # QIcon(Paths.icon("plus.png")), 
                    "Record macro",
                    self
                )
                self.record_macro_action.setStatusTip("Record a sequence of inputs")
                self.record_macro_action.triggered.connect(self.parent().record_macro)
                self.addAction(self.record_macro_action)

                # 'Play macro' button
                self.play_macro_action = QAction(
                    # QIcon(Paths.icon("plus.png")), 
                    "Play macro",
                    self
                )
                self.play_macro_action.setStatusTip("Play back the recorded sequence of inputs")
                self.play_macro_action.triggered.connect(self.parent().play_macro)
                self.play_macro_action.setEnabled(False)
                self.addAction(self.play_macro_action)

                self.delay_checkbox = QCheckBox("Delay:")
                
                self.delay_checkbox.stateChanged.connect(self.on_state_changed)
                self.delay_checkbox.setEnabled(False)
                self.addWidget(self.delay_checkbox)
                
                self.delay_spin = QDoubleSpinBox()
                self.delay_spin.setRange(0, 10.0)
                self.delay_spin.setDecimals(1)
                self.delay_spin.setSingleStep(0.1)
                self.delay_spin.setFixedWidth(70)
                self.delay_spin.setEnabled(False)
                self.addWidget(self.delay_spin)
                
            case 2:
                # 'Add new screen' button
                self.add_screen_action = QAction(
                    # QIcon(Paths.icon("ui-tab--plus.png")), 
                    "Add new screen",
                    self
                )
                self.add_screen_action.setStatusTip("Add a new group of screen co-ordinates")
                self.add_screen_action.triggered.connect(self.parent().add_screen)
                self.addAction(self.add_screen_action)

            case _:
                if Paths.debug:
                    print("Attempt to construct undefined toolbar:", tb_num)

    def on_state_changed(self, state):
        if state == Qt.CheckState.Checked.value:
            self.delay_spin.setEnabled(True)
        else:
            self.delay_spin.setEnabled(False)