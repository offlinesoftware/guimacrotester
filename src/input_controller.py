from time import sleep
from paths import Paths
from pynput import keyboard, mouse

class InputController():

    def __init__(self, parent=None):
        self.parent = parent

        self.kb_listener = keyboard.Listener(
            on_press = self.on_press,
            on_release = self.on_release)
        self.kb_controller = keyboard.Controller()

        self.mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)
        self.mouse_controller = mouse.Controller()

        self.macro = []

    def on_move(x, y):
        # print('Pointer moved to {0}'.format((x, y)))
        pass

    def on_click(self, x, y, button, pressed):
        # Button class is not serializable so save as string
        m_click = {"type": "click", "x": x, "y": y, "button": str(button), "pressed": pressed}
        self.macro.append(m_click)
        if Paths.debug: 
            print(m_click)

    def on_scroll(self, x, y, dx, dy):
        m_scroll = {"type": "scroll", "x": x, "y": y, "dx": dx, "dy": dy}
        self.macro.append(m_scroll)
        if Paths.debug: 
            print(m_scroll)

    def on_press(self, key):
        keypress = {"type": "keypress", "key": str(key)}
        if hasattr(key, 'char'):
            keypress["char"] = key.char
        self.macro.append(keypress)
        if Paths.debug: 
            print(keypress)

    def on_release(self, key):
        release = {"type": "release", "key": str(key)}
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
        # What if we hold down 'Stop recording' the press keys before releasing it?
        if Paths.debug:
            print("\nMacro of length:", len(self.macro))
            print(self.macro)

    def deserialize_key(self, value: str):
        # Case 1: Special key like "Key.enter"
        if value.startswith("Key."):
            name = value.split(".")[1]
            return keyboard.Key[name]

        # Case 2: Single character key like "a"
        if len(value) == 1:
            return keyboard.KeyCode.from_char(value)

        return value.strip("'")
    
    def play(self):
        for inpt in self.macro:
            print(inpt)
            sleep(self.parent.tb1.delay_spin.value())
            match inpt["type"]:
                case "keypress":
                    self.kb_controller.press(self.deserialize_key(inpt["key"]))

                case "release":
                    self.kb_controller.release(self.deserialize_key(inpt["key"]))
        
                case "click":
                    self.mouse_controller.position = (inpt["x"], inpt["y"])
                    # Mouse 'Button' class is stored as string, so needs converting back
                    if inpt["pressed"]:
                        self.mouse_controller.press(mouse.Button[inpt["button"].split(".")[1]])
                    else:
                        self.mouse_controller.release(mouse.Button[inpt["button"].split(".")[1]])
