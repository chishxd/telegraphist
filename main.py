from src.telegraphist.game import start_game, analyse_word

# from src.telegraphist.input import start_listening


def main() -> None:
    data = analyse_word("SOS")
    print(data)


if __name__ == "__main__":
    main()
