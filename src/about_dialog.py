from paths import Paths
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        QBtn = QDialogButtonBox.StandardButton.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setWindowTitle("About GUI Macro Tester")
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        title = QLabel("GUI Macro Tester")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)

        logo = QLabel()
        logo.setPixmap(QPixmap(Paths.icon("tw.png")))
        layout.addWidget(logo)

        layout.addWidget(QLabel("github.com/offlinesoftware"))
        layout.addWidget(QLabel("Copyright 2026 Thomas Walker"))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(
                Qt.AlignmentFlag.AlignHCenter
            )

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)