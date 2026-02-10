# This Python file uses the following encoding: utf-8
import sys
from about_dialog import AboutDialog
from screen_tree import ScreenTree
from clickThings import *
from paths import Paths
from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QApplication, QCheckBox, 
    QMainWindow, QStatusBar, QToolBar, QInputDialog
)

class Toolbar(QToolBar):
    def __init__(self, parent, tb_num):
        super(Toolbar, self).__init__(parent)
        self.setIconSize(QSize(16, 16))
        match tb_num:
            case 1:
                add_screen_action = QAction(
                    # QIcon(Paths.icon("ui-tab--plus.png")), 
                    "Add new screen",
                    self
                )
                add_screen_action.setStatusTip("Add a new grouping of screen co-ordinates")
                add_screen_action.triggered.connect(self.parent().add_screen)
                self.addAction(add_screen_action)
            
            case _:
                print("Attempt to construct undefined toolbar:", tb_num)


class MainWindow(QMainWindow):
    """GUI Macro Tester main window class

    Attributes:
        tree (ScreenTree): QTreeWidget to show the loaded screen co-ordinate data.
        tb1 (Toolbar): QToolbar to add and remove screen co-ordinate data.
        tb2 (Toolbar): Not yet implemented
    """


    def __init__(self, parent=None):
        """Constructor"""

        super().__init__(parent)
        self.setWindowTitle("GUI Macro Tester")
        self.setFixedSize(500, 750)

        self.tree = ScreenTree()

        self.setCentralWidget(self.tree)

        # Toolbars
        tb1 = Toolbar(self, 1)
        self.addToolBar(tb1)
        tb2 = Toolbar(self, 2)

        self.createMenus()


    def createMenus(self):
        '''
        # Go button
        button_action = QAction(QIcon("bug.png"), "&New program", self)
        button_action.setStatusTip("Run current script")
        button_action.triggered.connect(self.go_button_clicked)
        # button_action.setCheckable(True)
        # button_action.setShortcut(QKeySequence("Ctrl+p"))
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        # Debug button
        button_action2 = QAction(QIcon("bug.png"), "Hide for 2 s", self)
        button_action2.setStatusTip("Click to hide main window")
        button_action2.triggered.connect(self.detect_position)
        # button_action2.setCheckable(True)
        toolbar.addAction(button_action2)

        # Resolution label
        resolution = str(screenWidth) + " x " + str(screenHeight)
        toolbar.addWidget(QLabel(resolution))
        # toolbar.addWidget(QCheckBox())
        '''
        

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
    
    #
    # Member functions
    #
    

    def add_screen(self):
        screen_name, ok = QInputDialog.getText(self, 'Enter screen name', 'Name of new screen:')
        if ok and screen_name:
            self.tree.new_screen(screen_name)
    
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
