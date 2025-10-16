import threading
import time

from rich.console import Console
from rich.control import Control

# from rich.live import Live
from rich.panel import Panel

from src.telegraphist.input import start_listening
from src.telegraphist.levels import levels

# from src.telegraphist.levels import levels
from src.telegraphist.morse_code import MORSE_CODE_DICT

current_input = ""
input_lock = threading.Lock()


def handle_new_char(char: str) -> None:
    """Handles space key press to morse code

    Adds . or - to current input box according to user's duration to hold a space bar

    Args:
        char (str): The symbol translated from user input, either . or -
    """
    global current_input
    with input_lock:
        current_input += char


def start_game() -> None:
    """Event to render the game UI

    Handles positioning of cursor, it's visibility and ensures clearing terminal before and after the game.
    """
    global current_input, player_input_for_letter, current_letter_index

    listener_thread = threading.Thread(target=start_listening, args=(handle_new_char,))
    listener_thread.daemon = True
    listener_thread.start()

    console = Console()

    try:
        console.control(Control.show_cursor(False))
        console.clear()

        while True:
            current_level_data = levels[current_level_index]
            target_word = current_level_data["word"]

            game_loop()
            console.control(Control.home())

            current_char = target_word[current_letter_index]
            correct_morse = MORSE_CODE_DICT[current_char]

            cheat_sheet = f"Transmit '{current_char}': [bold cyan]{correct_morse}[/bold cyan]"
            transmission_panel = Panel(
                f"{cheat_sheet}\n\nYour Input: {player_input_for_letter}",
                title="Telegraph Console",
                border_style="cyan",
            )

            console.print(transmission_panel)
            if player_input_for_letter == correct_morse:
                # TODO: Add success sound
                current_letter_index += 1
                player_input_for_letter = ""
                if current_letter_index >= len(target_word):
                    console.print("[bold green] You won! [/bold green]")
                    break

            elif not correct_morse.startswith(player_input_for_letter):
                # TODO: Add error sound and visual feedback
                player_input_for_letter = ""

            time.sleep(0.05)

    except KeyboardInterrupt:
        pass

    finally:
        console.control(Control.show_cursor(True))
        console.print("[bold red]Transmission Ended.[/bold red]")


current_level_index = 0
current_letter_index = 0
player_input_for_letter = ""


def game_loop() -> None:
    """Handles core logic of each level

    This function checks for the value of current level and forwards that data to UI
    """
    global current_input, player_input_for_letter, current_letter_index

    with input_lock:
        if current_input:
            player_input_for_letter += current_input
            current_input = ""
