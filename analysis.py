#! /usr/bin/env python3

import chess
import chess.pgn
import itertools
from statistics import mean
import os


def pgnProcess(pgn, event):

    def pairwise(iterable):
        # pairwise('ABCDEFG') --> AB BC CD DE EF FG
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)

    output = {event: {}}
    count = 0
    while True:

        game = chess.pgn.read_game(f)
        if not game:
            break

        count += 1
        output[event][str(count)] = dict()
        print(count)

        w = game.headers['White']
        b = game.headers['Black']

        evals = []

        if sum(1 for _ in game.mainline()) < 10:
            continue  # skip games shorter than 10 ply

        for node in itertools.islice(game.mainline(), 200):  # no analysis after ply 200
            if node.board().is_game_over():
                continue  # no eval for mate played
            evals.append(max(min(node.eval().white(), chess.engine.Cp(1000)), chess.engine.Cp(-1000)).score())  # blunders above 1000 don't count

        evals[0] = 35  # initial eval is 0 but should not be

        def difference(n, evals):
            a, b = evals
            if n % 2 != 0:
                return max((a - b), 0)
            return max((b - a), 0)

        cpls = []
        for n, pair in enumerate(pairwise(evals)):
            cpls.append(difference(n, pair))

        black_evals = cpls[::2]
        white_evals = cpls[1::2]
        output[event][str(count)][w] = ('w', mean(white_evals))
        output[event][str(count)][b] = ('b', mean(black_evals))
    return output


full_output = []

events = os.listdir('./analysed_pgns')
for event in events:
    print(event)
    f = open(f'analysed_pgns/{event}')
    event_output = pgnProcess(f, event)
    full_output.append(event_output)
print(full_output)
