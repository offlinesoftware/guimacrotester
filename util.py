import json

# The `Qt` namespace has a lot of attributes to customize
# widgets. See: http://doc.qt.io/qt-6/qt.html
# label.setAlignment(Qt.AlignmentFlag.AlignCenter)

# Set the central widget of the Window. Widget will expand
# to take up all the space in the window by default.

def load_default():
    with open('default.json') as json_file:
        return json.load(json_file)
