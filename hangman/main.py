from __future__ import annotations # idk
from random import choice
from typing import Callable # i love typehinting


TRIES: int = 5 # you can edit this
WORDS: list[str] = ["jazz"]


try:
    with open("words.txt", "r") as file:
        WORDS = file.read().split("\n")

except FileNotFoundError as e:
    print(f"no words.txt found in directory \n[{e}]")


WORDS.sort()
WORDS = list(filter(bool, WORDS)) # remove empty lines if present


def main():
    word: str = choice(WORDS).lower()
    wrong: int = 0
    opened: dict[str, bool] = {i: False for i in word}

    # checks
    is_outoftries: Callable[[], bool] = lambda: not (wrong <= TRIES)
    is_allopened: Callable[[], bool] = lambda: all(list(opened.values()))

    while  not is_allopened() and not is_outoftries():
        __WS: str = "".join([(i if opened[i] else '_') for i in word]) # word format string
        letters: str = input(f"tries: {TRIES - wrong} \nword: {__WS} \nany ideas? (>=1 letter(s))> ").lower()

        if letters == "*": # quit
            print("you can't do that!")
            break

        for i in letters:
            if i in word: opened[i] = True
            else: wrong += 1

    print(f"the word was: {word}")
    if is_allopened(): print("you won!")


if __name__ == "__main__": main()