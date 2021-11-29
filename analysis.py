#! /usr/bin/env python3

import chess
import chess.pgn
import itertools
from statistics import mean


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

        w = game.headers['White']
        b = game.headers['Black']

        evals = []
        for node in game.mainline():
            evals.append(max(min(node.eval().white(), chess.engine.Cp(1000)), chess.engine.Cp(-1000)).score())  # blunders above 1000 don't count

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
        output[event][str(count)][w] = mean(white_evals)
        output[event][str(count)][b] = mean(black_evals)
    return output


event = 'lichess_study_1894-chess-world-championship-steinitz-lasker_by_Lichess_2021.11.29.pgn'
f = open(f'analysed_pgns/{event}')

output = pgnProcess(f, event)
print(output)
