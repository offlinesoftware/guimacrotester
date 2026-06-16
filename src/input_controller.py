import time
from paths import Paths
from pynput import keyboard, mouse
from PySide6.QtCore import QObject, Signal

# Inherit from QObject to make use of Signal()
class InputController(QObject):

    # Signals go before the constructor
    populate_sequence = Signal()

    # Constructor
    def __init__(self, parent=None):
        super().__init__(parent)    
        

        self.kb_listener = keyboard.Listener(
            on_press = self.on_press,
            on_release = self.on_release)
        self.kb_controller = keyboard.Controller()

        self.mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)
        self.mouse_controller = mouse.Controller()

        self.sequence = []

    
    # Don't record changes in mouse position
    def on_move(self, x, y):
        # print('Pointer moved to {0}'.format((x, y)))
        pass

    # Button class is not serializable so save as string
    def on_click(self, x, y, button, pressed):
        m_click = {"type": "click", "x": x, "y": y, "button": str(button), "pressed": pressed}
        self.sequence.append(m_click)

    # Capture mousewheel scroll events
    def on_scroll(self, x, y, dx, dy):
        m_scroll = {"type": "scroll", "x": x, "y": y, "dx": dx, "dy": dy}
        self.sequence.append(m_scroll)

    # Press of keyboard buttons (not mouse clicks)
    def on_press(self, key):
        keypress = {"type": "keypress", "key": str(key)}
        if hasattr(key, 'char'):
            keypress["char"] = key.char
        self.sequence.append(keypress)

    # Release of keyboard buttons (not mouse clicks)
    def on_release(self, key):
        release = {"type": "release", "key": str(key)}
        if hasattr(key, 'char'):
            release["char"] = key.char
        self.sequence.append(release)


    # Triggered by 'Record sequence' button
    def start(self):
        if Paths.debug:
            print("\nStarting new sequence")
        self.sequence = []

        self.kb_listener = keyboard.Listener(
            on_press = self.on_press,
            on_release = self.on_release)
        self.kb_listener.start()

        self.mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)
        self.mouse_listener.start()
    

    # Triggered by 'Record sequence' button (when already recording)
    def stop(self):
        self.kb_listener.stop()
        self.mouse_listener.stop()
        # Remove click and release of 'Stop recording' button
        self.sequence = self.sequence[:-2]
        # What if we hold down 'Stop recording' the press keys before releasing it?
        self.populate_sequence.emit()
        if Paths.debug:
            print("\nsequence of length:", len(self.sequence))
            print(self.sequence)


    # Recreate keyboard events that have been recorded as strings
    def deserialize_key(self, value: str):
        # Case 1: Special key like "Key.enter"
        
        if value.startswith("Key."):
            name = value.split(".")[1]
            return keyboard.Key[name]

        # Case 2: Single character key like "a"
        if len(value) == 1:
            return keyboard.KeyCode.from_char(value)

        return value.strip("'")
    
    
    # Play back recorded sequence of inputs
    def play(self, use_delay: bool, delay_value: int, return_mouse: bool):
        start = time.perf_counter()
        if Paths.debug: print("\nPlaying sequence of length", len(self.sequence))
        return_position = self.mouse_controller.position
        if Paths.debug:
            print('Return position is {0}'.format(return_position))
            print("use_delay:", use_delay)
        for inpt in self.sequence:

            if use_delay:
                time.sleep(delay_value / 1000)
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
        if return_mouse:
            self.mouse_controller.position = return_position
