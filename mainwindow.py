# This Python file uses the following encoding: utf-8
import sys
import pyautogui as pag
from clickThings import *
from paths import Paths
from util import load_default
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence, QPixmap
from PySide6.QtWidgets import (QApplication, QCheckBox, QTreeWidget, QDialog, QDialogButtonBox,
    QLabel, QMainWindow, QStatusBar, QToolBar, QInputDialog, QTreeWidgetItem, QVBoxLayout
)

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

class MainWindow(QMainWindow):
    """GUI Macro Tester main window class"""

    def __init__(self, parent=None):
        """Constructor"""

        super().__init__(parent)
        self.setWindowTitle("GUI Macro Tester")
        self.setFixedSize(500, 750)

        # Screen co-ordinates tree
        self.tree = QTreeWidget(self)
        self.tree.setColumnCount(2)
        self.tree.setColumnWidth(0, 350)
        self.tree.setHeaderLabels(["Screen area", "Position"])
        treedata = load_default()
        self.populateTree(treedata)

        self.setCentralWidget(self.tree)

        self.createMenus()


    def populateTree(self, data):
        """
        Populate tree view from JSON data
        
        :param data: Dict generated from JSON file
        """
        screens = []
        for k, v in data.items():
            screen = QTreeWidgetItem([k])
            for area in v:
                for areaName, coords in area.items():
                    pos = str(coords[0]) + ", " + str(coords[1])
                    name = QTreeWidgetItem([areaName, pos])
                    screen.addChild(name)
            screens.append(screen)
        self.tree.insertTopLevelItems(0, screens)


    def createMenus(self):
        """Create menus and toolbars"""

        # Toolbar
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        # Go button
        button_action = QAction(QIcon("bug.png"), "&New program", self)
        button_action.setStatusTip("Run current script")
        button_action.triggered.connect(self.go_button_clicked)
        # button_action.setCheckable(True)
        # button_action.setShortcut(QKeySequence("Ctrl+p"))
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        # Debug button
        button_action2 = QAction(QIcon("bug.png"), "Your &button2", self)
        button_action2.setStatusTip("This is your button2")
        button_action2.triggered.connect(self.detect_position)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)

        # Resolution label
        resolution = str(screenWidth) + " x " + str(screenHeight)
        toolbar.addWidget(QLabel(resolution))
        toolbar.addWidget(QCheckBox())

        # Bit at the bottom for tooltips
        self.setStatusBar(QStatusBar(self))

        # Menu bar
        menu = self.menuBar()
        
        # tag::menuFile[]
        file_menu = self.menuBar().addMenu("&File")

        open_file_action = QAction(
            QIcon(Paths.icon("disk--arrow.png")),
            "Open file...",
            self,
        )
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction(
            QIcon(Paths.icon("disk--pencil.png")),
            "Save sequence as...",
            self,
        )
        save_file_action.setStatusTip("Save current sequence to file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)
        # end::menuFile[]
        
        # tag::menuHelp[]
        help_menu = self.menuBar().addMenu("&Help")

        about_action = QAction(
            QIcon(Paths.icon("question.png")),
            "About GUI Macro Tester",
            self,
        )
        about_action.setStatusTip(
            "Find out more about GUI Macro Tester"
        )  # Hungry!
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        # end::menuHelp[]

    def about(self):
        dlg = AboutDialog()
        dlg.exec()

    # end::menuHelpfn[]

    # tag::menuFilefnOpen[]
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "",
            "Hypertext Markup Language (*.htm *.html);;"
            "All files (*.*)",
        )

        if filename:
            with open(filename, "r") as f:
                html = f.read()

            self.browser.setHtml(html)
            self.urlbar.setText(filename)

    # end::menuFilefnOpen[]

    # tag::menuFilefnSave[]
    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Page As",
            "",
            "Hypertext Markup Language (*.htm *.html);;"
            "All files (*.*)",
        )

        if filename:
            # Define callback method to handle the write.
            def writer(html):
                with open(filename, "w") as f:
                    f.write(html)

            self.browser.page().toHtml(writer)

    # end::menuFilefnSave[]   
    
    def toolbar_button_clicked(self, s):
        """Debug function for button click"""

        print("click", s)


    def go_button_clicked(self):
        """
        Execute current macro sequence
        """
        
        program_name, ok = QInputDialog.getText(self, 'Enter progam name', 'Name of new program:')
        if ok and program_name:
            new_program(program_name)

    
    def detect_position(self):
        self.hide()
        sleep(2)
        self.show()


# Run the application
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.setStyleSheet("""
        QWidget {
            font-size: 16px;

        }

    """)
    window.show()

    sys.exit(app.exec())
