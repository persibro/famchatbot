import threading
from random import randint
from time import sleep


class GuessTheNumber(threading.Thread):

    def __init__(self, upper_limit, chat_id, _bot):
        threading.Thread.__init__(self)
        self.chat_id = chat_id
        self._bot = _bot
        self.timer = 30.0
        self.turns = 0
        self.guessed_right = False
        if upper_limit != "":
            self.upper_limit = upper_limit
        else:
            self.upper_limit = 100

    def run(self):

        self.random_number = randint(0, self.upper_limit)
        self._bot.sendMessage(self.chat_id,
                              "Number generated! Guess with /guess")

        while self.timer >= 0 and self.turns < 10:
            sleep(.5)
            self.timer -= .5

        if self.guessed_right:
            return
        elif self.turns >= 10:
            self._bot.sendMessage(self.chat_id,
                                  "Sorry, out of turns!")
        elif self.timer <= 0 and not self.guessed_right:
            self._bot.sendMessage(self.chat_id,
                                  "Times up!")

    def guess(self, guess):
        try:
            guess = int(guess)
            if guess == self.random_number:
                self._bot.sendMessage(self.chat_id,
                                      "Correct!")
                self.guessed_right = True
                self.timer = 0

            elif guess > self.random_number:
                if self.turns < 9:
                    self._bot.sendMessage(self.chat_id,
                                          "Smaller than %d" % guess)

            elif guess < self.random_number:
                if self.turns < 9:
                    self._bot.sendMessage(self.chat_id,
                                          "Larger than %d" % guess)

            if not self.guessed_right:
                self.timer_refresh()

            self.turns += 1

        except:
            self._bot.sendMessage(self.chat_id,
                                  "invalid input bruh")

    def timer_refresh(self):
        self.timer = 30
