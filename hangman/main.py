from __future__ import annotations # idk
from random import choice
from typing import Callable # i love typehinting
import json


with open("config.json") as file:
    cfg: dict = json.loads(file.read())


class Statistics:
    def __init__(self):
        self.won: int = 0
        self.lose: int = 0

    @property
    def total(self): return self.won + self.lose
    
    @property
    def winrate(self): return self.won / self.total

    def reset(self):
        self.won = 0
        self.lose = 0


class Options:
    def __init__(self):
        self.num_tries: int = 0
        self.words: list[str] = []
        self.endless: bool = False

    def load_cfg(self, cfg: dict):
        num_tries: int = cfg.get("num_tries", 5)
        endless: bool = cfg.get("endless", False)

        with open(cfg.get("words_file", "words.txt"), "r+") as __F:
            words: list[str] = __F.read().split("\n")
            if not any(words): words = ["jazz"]
            words.sort()
            words = list(filter(bool, words))

        self.endless = endless
        self.num_tries = num_tries
        self.words = words


class Game:
    def __init__(self):
        self.opts: Options = Options()
        self.stats: Statistics = Statistics()

        self.wrong: int = 0
        self.word: str = ""
        self.opened: dict[str, bool] = {}

        self.reset_opened()
        self.opts.load_cfg(cfg)

    @property
    def all_opened(self): return all(list(self.opened.values()))

    @property
    def out_of_tries(self): return self.wrong > self.opts.num_tries

    @property
    def complete(self): return (not self.out_of_tries) and (self.all_opened)

    @property
    def format_string(self): return ''.join(
            [
                (i if self.opened[i] else '_') 
                for i in self.word
            ]
        )

    def reset_opened(self):
        self.opened = {
            i: False for i in self.word
        }
        self.wrong = 0

    def set_word(self, new: str):
        self.word = new
        self.reset_opened()

    def try_letters(self, letters: str):
        if self.out_of_tries: return

        for i in letters:
            if i in self.opened: self.opened[i] = True
            else: self.wrong += 1


class Hangman(Game):
    def game(self):
        self.set_word(choice(self.opts.words))

        while (not self.all_opened) and (not self.out_of_tries):
            letters = input(
                f"word: {self.format_string} \n"
                f"tries left: {self.opts.num_tries - self.wrong} \n"
                "any ideas? (>=1 letters) > "
            )
            
            self.try_letters(letters)

        print(f"word was: {self.word}")
        if self.complete: self.stats.won += 1
        else: self.stats.lose += 1


    def start_one(self):
        self.game()
        if self.complete: print("you won!")

    def start_endless(self):
        while True:
            self.game()
            print(
                    "stats \n"
                    f"games: {self.stats.total} \n"
                    f"won: {self.stats.won} \n"
                    f"lose: {self.stats.lose} \n"
                    f"winrate: {self.stats.winrate}"
                )

    def start(self):
        if self.opts.endless: self.start_endless()
        else: self.start_one()


def main():
    h = Hangman()
    h.start()


if __name__ == "__main__": main()