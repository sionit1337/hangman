from __future__ import annotations
from random import choice


TRIES: int = 5
WORDS: list[str] = ["jazz"]


try:
    with open("words.txt", "r") as file:
        WORDS = file.read().split("\n")

except FileNotFoundError as e:
    print(f"no words.txt found in directory \n[{e}]")


WORDS.sort()
WORDS = list(filter(bool, WORDS))


def main():
    word: str = choice(WORDS).lower()
    wrong: int = 0
    opened: dict[str, bool] = {i: False for i in word}

    while  (not all(list(opened.values()))) and (wrong <= TRIES):
        __WS: str = "".join([(i if opened[i] else '_') for i in word])
        letters: str = input(f"tries: {TRIES - wrong} \nword: {__WS} \nany ideas? (>=1 letter(s))> ").lower()
        if letters == "*":
            print("you can't do that!")
            break

        for i in letters:
            if i in word: opened[i] = True
            else: wrong += 1

    print(f"the word was: {word}")
    if all(list(opened.values())): print("you won!")


if __name__ == "__main__": main()