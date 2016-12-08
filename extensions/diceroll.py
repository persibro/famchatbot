from random import randint

DICE_LIMIT = 1000


def input_parse(sumstr):

    rolls = []

    remove_spaces = [x for x in sumstr if x != " "]
    remove_spaces = "".join(remove_spaces)

    roll_directive = remove_spaces.split("+")

    for roll in roll_directive:

        rollsplitted = roll.split("d")

        if roll[0] != "d":  # Check to see if there is a number of dice specified (i.e. d6)

            if len(rollsplitted) == 2:

                try:
                    if int(rollsplitted[0]) <= DICE_LIMIT:
                        for x in xrange(int(rollsplitted[0])):
                            rolls.append(randint(1, int(rollsplitted[1])))
                except:
                    pass

            elif len(rollsplitted) == 1:

                try:
                    rolls.append(int(rollsplitted[0]))
                except:
                    pass

        elif roll[0] == "d":
            try:
                rolls.append(randint(1, int(rollsplitted[1])))
            except:
                pass

    return rolls


def diceroll(sumstr, show_total):

    rolls = input_parse(sumstr)

    compiled = ""

    for index, roll in enumerate(rolls):

        compiled += str(roll)

        if index < len(rolls) - 1:
            compiled += ", "
        else:
            if show_total:
                compiled += "\n - *Total*: " + str(sum(rolls)) + " -"

    return compiled


if __name__ == "__main__":

    while 1:

        userinput = raw_input("")

        if userinput == "x":
            exit()
        else:
            print diceroll(userinput)
