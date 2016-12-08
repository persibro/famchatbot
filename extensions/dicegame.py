import threading
from time import sleep
from random import shuffle, randint
from collections import Counter
from operator import itemgetter


class DiceGame(threading.Thread):

    def __init__(self, chat_id, _bot):
        threading.Thread.__init__(self)
        self.game_open = True   # Open to new players
        self.players = {}
        self._bot = _bot
        self.roll_timer = 30.0
        self.lobby_timer = 30.0
        self.current_roller = ""
        self.chat_id = chat_id

    def run(self):

        self._bot.sendMessage(self.chat_id,
                              "Players have %d seconds to join the game! /joindicegame" % self.lobby_timer)

        # Wait in lobby for players
        while self.lobby_timer >= 0:
            self.lobby_timer -= .5
            sleep(.5)
        self.game_open = False
        playerlist = self.players.keys()
        shuffle(playerlist)

        self._bot.sendMessage(self.chat_id,
                              "Game closed! Time to roll!")

        # Roll session
        for player in playerlist:
            self.roll_timer = 30.0
            self.current_roller = str(player)
            self._bot.sendMessage(self.chat_id,
                                  "%s is up! /rolldice" % self.players[player][0])
            while self.roll_timer >= 0:
                self.roll_timer -= .5
                sleep(.5)

        self._bot.sendMessage(self.chat_id,
                              "Rolls completed!")

        # Print scores and announce winner
        self._bot.sendMessage(self.chat_id,
                              "*Scores:*\n%s" % self.winner_and_scores(),
                              "Markdown")

    def join(self, msg_from):

        user_id = str(msg_from["id"])

        if self.game_open:

            if user_id not in self.players.iterkeys():
                self.players[user_id] = [msg_from["first_name"], [], 0]
                self._bot.sendMessage(self.chat_id,
                                      "%s has joined the game!" % msg_from["first_name"])
            else:
                self._bot.sendMessage(self.chat_id,
                                      "%s already added!" % msg_from["first_name"])

    def start_game(self):
        self.lobby_timer = 0

    def roll(self, msg_from):

        user_id = str(msg_from["id"])
        rolls = []

        if user_id == self.current_roller:      # Roll only for the current person's turn
            for x in xrange(3):
                rolls.append(randint(1, 6))

            self._bot.sendMessage(self.chat_id,
                                  "*%s* rolled %s, %s, %s" % (msg_from["first_name"], rolls[0], rolls[1], rolls[2]),
                                  "Markdown")

            self.roll_timer = 30
            counted = Counter(rolls)

            # roll parse code
            if sorted(rolls) == [4, 5, 6]:
                self.players[user_id][1] = rolls
                self.players[user_id][2] = 13
                self.roll_timer = 0

            elif len(counted.most_common()) == 1:
                self.players[user_id][1] = rolls
                self.players[user_id][2] = 6 + counted.most_common()[0][0]
                self.roll_timer = 0

            elif len(counted.most_common()) == 2:
                self.players[user_id][1] = rolls
                self.players[user_id][2] = counted.most_common()[1][0]
                self.roll_timer = 0

            elif sorted(rolls) == [1, 2, 3]:
                self.players[user_id][1] = rolls
                self.roll_timer = 0

        else:
            self._bot.sendMessage(self.chat_id,
                                  "He, %s, it's not your turn!" % msg_from["first_name"])

    def winner_and_scores(self):
        # self.players[user_id] = [msg_from["first_name"], [], 0]

        return_string = ""

        if len(self.players.values()) > 1:
            ordered_list = sorted(self.players.values(), key=itemgetter(2), reverse=True)

            for player in ordered_list:
                return_string += "%s rolled %s, %s, %s\n" % (player[0], player[1][0], player[1][1], player[1][2])

        else:
            return_string += "%s rolled %s, %s, %s\n" % (self.players.values()[0][0], self.players.values()[0][1][0], self.players.values()[0][1][1], self.players.values()[0][1][2])

        return return_string
