import json
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu
from PySide6.QtGui import QAction

class ScreenTree(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(2)
        self.setColumnWidth(0, 350)
        self.setHeaderLabels(["Screen area", "Position"])
        self.load_data()
        self.populate()
    
    def load_data(self, file='default.json'):
        with open(file) as json_file:
            self.data = json.load(json_file)

    def populate(self):
        """
        Populate tree view from JSON data
        
        :param data: Dict generated from JSON file
        """
        screens = []
        for k, v in self.data.items():
            screen = QTreeWidgetItem([k])
            for area in v:
                for areaName, coords in area.items():
                    pos = str(coords[0]) + ", " + str(coords[1])
                    name = QTreeWidgetItem([areaName, pos])
                    screen.addChild(name)
            
            screens.append(screen)
        self.insertTopLevelItems(0, screens)
        self.itemClicked.connect(self.onItemClicked)

    def new_screen(self, name):
        self.data[name] = []
        self.clear()
        self.populate()

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)

        action1 = QAction('Action 1', self)
        action2 = QAction('Action 2', self)

        context_menu.addAction(action1)
        context_menu.addAction(action2)

        context_menu.exec(event.globalPos())

    def onItemClicked(self, it, col):
        print(it, col, it.text(col))