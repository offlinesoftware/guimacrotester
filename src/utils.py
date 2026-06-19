from paths import Paths

from PySide6.QtGui import QIcon
from PySide6.QtCore import QObject

class Utils(QObject):
    # Constructor
    def __init__(self, parent=None):
        super().__init__(parent)

    # Button action builder
    def create_action(self, text, slot, enabled, tip, icon=None):
        act = self.addAction(QIcon(Paths.icon(icon)) if icon else QIcon(), text, slot)
        act.setStatusTip(tip)
        act.setEnabled(enabled)
        return act

