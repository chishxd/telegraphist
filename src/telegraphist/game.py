import threading
import time

from playsound3 import playsound
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

feedback_message: str = ""


def display_title_screen() -> None:
    console = Console()
    console.clear()

    title_art = """
  _______ _            _______   _                            _     _     _   
 |__   __| |          |__   __| | |                          | |   (_)   | |  
    | |  | |__   ___     | | ___| | ___  __ _ _ __ __ _ _ __ | |__  _ ___| |_ 
    | |  | '_ \ / _ \    | |/ _ \ |/ _ \/ _` | '__/ _` | '_ \| '_ \| / __| __|
    | |  | | | |  __/    | |  __/ |  __/ (_| | | | (_| | |_) | | | | \__ \ |_ 
    |_|  |_| |_|\___|    |_|\___|_|\___|\__, |_|  \__,_| .__/|_| |_|_|___/\__|
                                         __/ |         | |                    
                                        |___/          |_|                    
"""

    console.print(f"[bold cyan]{title_art}[/bold cyan]", justify="center")

    input("\n \n" + " " * 40 + "Press Enter to Start Transmission...")


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
    global current_input, player_input_for_letter, current_letter_index, feedback_message

    display_title_screen()

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

            if current_letter_index >= len(target_word):
                console.print(Panel(f"Correct: '{target_word[-1]}'", border_style="yellow"))
                console.print(Panel("[bold green]You won![/bold green]", border_style="green"))
                break

            current_char = target_word[current_letter_index]
            correct_morse = MORSE_CODE_DICT[current_char]

            cheat_sheet = f"Transmit '{current_char}': [bold cyan]{correct_morse}[/bold cyan]"
            transmission_panel = Panel(
                f"{cheat_sheet}\n\nYour Input: {player_input_for_letter}",
                title="Telegraph Console",
                border_style="cyan",
            )

            console.print(transmission_panel)

            if feedback_message:
                console.print(Panel(feedback_message, border_style="yellow"))
                feedback_message = ""

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
    global current_input, player_input_for_letter, current_letter_index, feedback_message

    current_level_data = levels[current_level_index]
    target_word = current_level_data["word"]

    if current_letter_index >= len(target_word):
        return

    current_char = target_word[current_letter_index]
    correct_morse = MORSE_CODE_DICT[current_char]

    with input_lock:
        if current_input:
            player_input_for_letter += current_input
            current_input = ""

        if player_input_for_letter == correct_morse:
            # TODO: Add success sound
            playsound("src/telegraphist/sfx/success.wav", block=False)
            current_letter_index += 1
            player_input_for_letter = ""
            feedback_message = f"Correct: '{current_char}'"

        elif not correct_morse.startswith(player_input_for_letter):
            # TODO: Add error sound and visual feedback
            playsound("src/telegraphist/sfx/error.wav", block=False)
            feedback_message = "[bold red]Wrong Code![/bold red]"
            player_input_for_letter = ""
