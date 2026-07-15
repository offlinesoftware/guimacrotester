from PySide6.QtWidgets import QApplication, QStyle

class Paths:

    debug = False

    # Can't load contents from style() until after QApplication exists
    icon_dict = {}

    @classmethod
    def load_icons(cls):
        style = QApplication.style()

        cls.icon_dict = {
            "up_arrow":         style.standardIcon(QStyle.StandardPixmap.SP_ArrowUp),
            "down_arrow":       style.standardIcon(QStyle.StandardPixmap.SP_ArrowDown),
            "up_triangle":      style.standardIcon(QStyle.StandardPixmap.SP_TitleBarShadeButton),
            "down_triangle":    style.standardIcon(QStyle.StandardPixmap.SP_TitleBarUnshadeButton),
            "open_seq":         style.standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton),
            "save_seq":         style.standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton),
            "open_mac":         style.standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon),
            "save_mac":         style.standardIcon(QStyle.StandardPixmap.SP_DriveFDIcon),
            "record":           style.standardIcon(QStyle.StandardPixmap.SP_DialogNoButton),
            "play":             style.standardIcon(QStyle.StandardPixmap.SP_MediaPlay),
            "delete":            style.standardIcon(QStyle.StandardPixmap.SP_DialogResetButton),
            "clear":           style.standardIcon(QStyle.StandardPixmap.SP_DialogDiscardButton),
            "question":         style.standardIcon(QStyle.StandardPixmap.SP_MessageBoxQuestion)
        }
        
    @classmethod
    def get(cls, name):
        return cls.icon_dict[name]

    # For external icons imported with resources.qrc
    #@classmethod
    def icon(filename):
        return f":/icons/{filename}"