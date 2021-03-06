# -*- coding: utf-8 -*-
"""
Bot commands list:
blackppldice - Clicky clack
diceroll - Roll dices
8ball - Roll that Magic 8-Ball
goteem - GOT EEM! 👌🏿
rekt - Someone got REKTD! (takes optional <int> argument)
guessthenumber - Start a round of number guessing
roundofdice - Start a round of clicky clack
"""

import telepot
from pprint import pprint
from sys import argv, stdout, path
from os import system

path.insert(0, "extensions")

### Start extensions includes here ###
from eightball import eightball
from cannedresponses import cannedresponses
from rekt import rekt
import guessing_game
import dicegame
from diceroll import diceroll

try:
    bottoken = argv[1]
except IndexError:
    print "\nUsage: %s <bottoken>\n" % argv[0]
    exit()

run_counter = 0
current_threads = {}


def inc_message(msg):
    parsed_command = ""
    chat_id = msg["chat"]["id"]
    chat_id_key = str(chat_id)

    # initialize dict for chat_id if there isn't one already
    if chat_id_key not in current_threads.keys():
        current_threads[str(chat_id)] = {}

    # See if a command is sent
    if msg["text"][0] == "/":

        try:
            parsed_command = msg["text"][1:msg["text"].index('@')]
        except ValueError:
            try:
                parsed_command = msg["text"][1:msg["text"].index(' ')]
            except ValueError:
                parsed_command = msg["text"][1:]

    # Start of commands
    if parsed_command == "blackppldice":

        bot.sendMessage(chat_id,
                        "*%s* rolled %s" % (msg["from"]["first_name"], diceroll("3d6", False)),
                        "Markdown")

    elif parsed_command == "diceroll" and arg_extract(msg["text"]) == "":

        bot.sendMessage(chat_id,
                        "*%s* rolled %s" % (msg["from"]["first_name"], diceroll("d6", False)),
                        "Markdown")

    elif parsed_command == "diceroll" and arg_extract(msg["text"]):

        bot.sendMessage(chat_id,
                        "*%s* rolled %s" % (msg["from"]["first_name"], diceroll(arg_extract(msg["text"]), True)),
                        "Markdown")

    elif parsed_command == "8ball":

        bot.sendMessage(chat_id,
                        eightball(msg["from"]["first_name"], arg_extract(msg["text"])),
                        "Markdown")

    elif parsed_command == "goteem":

        bot.sendVideo(chat_id,
                      open('static/goteem.mp4', 'rb'))

    elif parsed_command == "rekt":

        try:
            argument = int(arg_extract(msg["text"]))
        except:
            argument = 4

        bot.sendMessage(chat_id,
                        rekt(argument))

    # Commands for number guessing game #

    elif parsed_command == "guessthenumber":

        try:
            if current_threads[chat_id_key]["guessinggame"].isAlive():
                bot.sendMessage(chat_id,
                                "Finish the current game first!")
            else:
                _newguessgame = guessing_game.GuessTheNumber("", chat_id, bot)
                current_threads[chat_id_key]["guessinggame"] = _newguessgame
                _newguessgame.start()
        except KeyError:
            _newguessgame = guessing_game.GuessTheNumber("", chat_id, bot)
            current_threads[chat_id_key]["guessinggame"] = _newguessgame
            _newguessgame.start()

    elif parsed_command == "guess" and current_threads[chat_id_key]["guessinggame"].isAlive():
        player_guess = arg_extract(msg["text"])
        current_threads[chat_id_key]["guessinggame"].guess(player_guess)

    # Commands for dice game #

    elif parsed_command == "roundofdice":
        try:
            if current_threads[chat_id_key]["dicegame"].isAlive():
                bot.sendMessage(chat_id,
                                "Finish the current game first!")
            else:
                _newdicegame = dicegame.DiceGame(chat_id, bot)
                current_threads[chat_id_key]["dicegame"] = _newdicegame
                _newdicegame.start()
        except KeyError:
            _newdicegame = dicegame.DiceGame(chat_id, bot)
            current_threads[chat_id_key]["dicegame"] = _newdicegame
            _newdicegame.start()

    elif parsed_command == "joindicegame" and current_threads[chat_id_key]["dicegame"].isAlive():
        current_threads[chat_id_key]["dicegame"].join(msg["from"])

    elif parsed_command == "rolldice" and current_threads[chat_id_key]["dicegame"].isAlive():
        current_threads[chat_id_key]["dicegame"].roll(msg["from"])

    elif parsed_command == "start" and current_threads[chat_id_key]["dicegame"].isAlive():
        current_threads[chat_id_key]["dicegame"].start_game()

    else:
        bot.sendMessage(chat_id,
                        cannedresponses())

    # Session run counter
    global run_counter
    run_counter += 1
    stdout.write('\r')
    stdout.write('Bot usage this session: %06d' % run_counter)
    stdout.flush()

    # pprint(msg) # print out message JSON for debugging


def arg_extract(some_string):
    try:
        argument = some_string[some_string.index(' ') + 1:]
        return argument
    except ValueError:
        return ""


if __name__ == '__main__':
    system("clear")
    bot = telepot.Bot(bottoken)
    bot.message_loop(inc_message, relax=.5)
    while True:
        nada = raw_input("Press enter to end script!\n")
        exit()
