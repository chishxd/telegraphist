import threading
import time

from rich.console import Console

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
    global current_input

    listener_thread = threading.Thread(target=start_listening, args=(handle_new_char,))
    listener_thread.daemon = True

    listener_thread.start()
    console = Console()

    try:
        while True:
            CURSOR_UP_TOP = "\x1b[H"
            print(CURSOR_UP_TOP, end="")

            display_text = f"Your Transmission:\n> {current_input}"
            ui_panel = Panel(display_text, title="Telegraph Console")

            console.print(ui_panel)

            time.sleep(0.05)

    except KeyboardInterrupt:
        console.clear()
        console.print("\n[bold red] Game Ended![/bold red]")
