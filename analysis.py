#! /usr/bin/env python3

import chess.pgn
import itertools
from statistics import mean

f = open('analysed_pgns/lichess_study_1894-chess-world-championship-steinitz-lasker_by_Lichess_2021.11.29.pgn')


output = {}


def pgnProcess(pgn):

   def pairwise(iterable):
        # pairwise('ABCDEFG') --> AB BC CD DE EF FG
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)

    count = 0
    while True:
        count += 1
        print(count)
        game = chess.pgn.read_game(f)
        if not game:
            break
        w = game.headers['White']
        b = game.headers['Black']

        evals = []
        for node in game.mainline():
            evals.append(min(node.eval().white().score(mate_score=1000), 1000))  # blunders above 1000 don't count

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
        print(mean(white_evals))
        print(mean(black_evals))
