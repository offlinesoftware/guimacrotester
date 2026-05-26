import time
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

    def on_move(self, x, y):
        # print('Pointer moved to {0}'.format((x, y)))
        pass

    def on_click(self, x, y, button, pressed):
        # Button class is not serializable so save as string
        m_click = {"type": "click", "x": x, "y": y, "button": str(button), "pressed": pressed}
        self.macro.append(m_click)

    def on_scroll(self, x, y, dx, dy):
        m_scroll = {"type": "scroll", "x": x, "y": y, "dx": dx, "dy": dy}
        self.macro.append(m_scroll)

    def on_press(self, key):
        keypress = {"type": "keypress", "key": str(key)}
        if hasattr(key, 'char'):
            keypress["char"] = key.char
        self.macro.append(keypress)

    def on_release(self, key):
        release = {"type": "release", "key": str(key)}
        if hasattr(key, 'char'):
            release["char"] = key.char
        self.macro.append(release)

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
        self.parent.sequence_table.populate_table()
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
        start = time.perf_counter()
        if Paths.debug: print("\nPlaying macro of length", len(self.macro))
        return_position = self.mouse_controller.position
        if Paths.debug:
            print('Return position is {0}'.format(return_position))
        for inpt in self.macro:

            if self.parent.tb1.delay_checkbox.isChecked():
                time.sleep(self.parent.tb1.delay_spin.value() / 1000)
            match inpt["type"]:
                case "keypress":
                    if Paths.debug: print("Pressing key: ", inpt['key'])
                    self.kb_controller.press(self.deserialize_key(inpt['key']))

                case "release":
                    if Paths.debug: print("Releasing key: ", inpt['key'])
                    self.kb_controller.release(self.deserialize_key(inpt["key"]))
        
                case "click":
                    self.mouse_controller.position = (int(inpt["x"]), int(inpt["y"]))
                    # Mouse 'Button' class is stored as string, so needs converting back
                    if inpt["pressed"]:
                        if Paths.debug: print(inpt['button'], " down at: ", inpt['x'], inpt['y'])
                        self.mouse_controller.press(mouse.Button[inpt["button"].split(".")[1]])
                    else:
                        if Paths.debug: print(inpt['button'], " up at: ", inpt['x'], inpt['y'])
                        self.mouse_controller.release(mouse.Button[inpt["button"].split(".")[1]])

                case "scroll":
                    if Paths.debug: print("Scrolling by: ", inpt['x'], inpt['y'])
                    self.mouse_controller.scroll(inpt['dx'], inpt['dy'])
        if Paths.debug:
            end = time.perf_counter()
            print(f"Execution time: {end - start:.6f} seconds")
        if self.parent.tb1.return_checkbox.isChecked():
            self.mouse_controller.position = return_position

    