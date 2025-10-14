import time

from pynput import keyboard

DOT_DURATION: float = 0.2

press_time = None
key_down: bool = False


def on_press(key: keyboard.Key | keyboard.KeyCode | None) -> None:
    """Called by pynput on key press

    This function accespts a key from pynput, it's main purpose is to "hold" a key and not key firing

    Args:
        key (keyboard.Key | keyboard.KeyCode | None): The key pressed on Keyboard.
    """
    global key_down, press_time

    if key == keyboard.Key.space and not key_down:
        key_down = True
        press_time = time.time()


def on_release(key: keyboard.Key | keyboard.KeyCode | None):
    """This function is to be passed as a parameter for pynput

    This function accepts a key from pynput, calculate duration of the key being held and print result

    Args:
        key (keyboard.Key | keyboard.KeyCode | None): The Key recieved from keyboard input
    """

    global key_down, press_time

    if key == keyboard.Key.space and press_time is not None:
        duration = time.time() - press_time

        if duration < DOT_DURATION:
            print(".", end="", flush=True)
        else:
            print("-", end="", flush=True)

        press_time = None
        key_down = False
