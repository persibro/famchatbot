from random import shuffle, randint

canned_responses = [
    "I don't care.",
    "So what?",
    "Cool?"
]


def cannedresponses():
    shuffle(canned_responses)
    return canned_responses[randint(0, len(canned_responses) - 1)]
