# -*- coding: utf-8 -*-
"""
Bot commands list:
blackppldice - Clicky clack
8ball - Roll that Magic 8-Ball
goteem - GOT EEM! 👌🏿
"""

import telepot
from pprint import pprint
from random import randint
from sys import argv, stdout, path
from os import system

path.insert(0, "extensions")

### Start extensions includes here ###
from eightball import eightball
from cannedresponses import cannedresponses
from rekt import rekt

try:
    bottoken = argv[1]
except IndexError:
    print "\nUsage: %s <bottoken>\n" % argv[0]
    exit()

run_counter = 0


def inc_message(msg):
    parsed_command = ""
    chat_id = msg["chat"]["id"]

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
                        "*%s* rolled %s, %s, %s" % (msg["from"]["first_name"], randint(1, 6), randint(1, 6), randint(1, 6)),
                        "Markdown")

    elif parsed_command == "8ball":

        bot.sendMessage(chat_id,
                        eightball(msg["from"]["first_name"], arg_extract(msg["text"])),
                        "Markdown")

    elif parsed_command == "goteem":

        bot.sendVideo(chat_id,
                      open('static/goteem.mp4', 'rb'))

    elif parsed_command == "rekt":

        bot.sendMessage(chat_id,
                        rekt())

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
