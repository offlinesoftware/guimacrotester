from paths import Paths
from pynput import keyboard, mouse

class InputController():
    def on_move(x, y):
        # print('Pointer moved to {0}'.format((x, y)))
        pass

    def on_click(self, x, y, button, pressed):
        m_click = {"type": "click", "x": x, "y": y, "button": button, "pressed": pressed}
        self.macro.append(m_click)
        if Paths.debug: 
            print(m_click)

    def on_scroll(self, x, y, dx, dy):
        m_scroll = {"type": "scroll", "x": x, "y": y, "dx": dx, "dy": dy}
        self.macro.append(m_scroll)
        if Paths.debug: 
            print(m_scroll)

    def on_press(self, key):
        keypress = {"type": "keypress", "key": key}
        if hasattr(key, 'char'):
            keypress["char"] = key.char
        self.macro.append(keypress)
        if Paths.debug: 
            print(keypress)

    def on_release(self, key):
        release = {"type": "release", "key": key}
        if hasattr(key, 'char'):
            release["char"] = key.char
        self.macro.append(release)
        if Paths.debug: 
            print(release)

    def start(self):
        if Paths.debug:
            print("\nStarting new macro")
        self.macro = []

        self.kb_listener = keyboard.Listener(
            on_press = self.on_press,
            on_release = self.on_release)
        self.kb_listener.start()

        self.mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)
        self.mouse_listener.start()
    
    def stop(self):
        self.kb_listener.stop()
        self.mouse_listener.stop()
        # Remove click and release of 'Stop recording' button
        self.macro = self.macro[:-2]
        if Paths.debug:
            print("\nMacro of length:", len(self.macro))
            print(self.macro)

    def __init__(self):
        super().__init__()

        self.kb_listener = keyboard.Listener(
        on_press = self.on_press,
        on_release = self.on_release)

        self.mouse_listener = mouse.Listener(
        on_move=self.on_move,
        on_click=self.on_click,
        on_scroll=self.on_scroll)
