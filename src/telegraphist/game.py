import threading
import time

from rich.console import Console
from rich.control import Control

# from rich.live import Live
from rich.panel import Panel

from src.telegraphist.input import start_listening

current_input = ""
input_lock = threading.Lock()


def handle_new_char(char: str) -> None:
    global current_input
    with input_lock:
        current_input += char


def start_game() -> None:
    global current_input, CURSOR_TO_HOME, HIDE_CURSOR, SHOW_CURSOR, CLEAR_SCREEN

    listener_thread = threading.Thread(target=start_listening, args=(handle_new_char,))
    listener_thread.daemon = True

    listener_thread.start()
    console = Console()

    console.control(Control.show_cursor(False))
    console.clear()
    try:
        while True:
            console.control(Control.home())

            display_text = f"Your Transmission:\n> {current_input}"
            ui_panel = Panel(display_text, title="Telegraph Console")
            ui_panel = Panel(display_text, title="Telegraph Console")

            console.print(ui_panel)

            time.sleep(0.05)

    except KeyboardInterrupt:
        pass

    finally:
        console.control(Control.show_cursor(True))
        console.print("[bold red]Transmission Ended.[/bold red]")
