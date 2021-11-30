#! /usr/bin/env python3

import chess
import chess.pgn
import itertools
from statistics import mean
import os
import csv


def pgnProcess(pgn, event):

    def pairwise(iterable):
        # pairwise('ABCDEFG') --> AB BC CD DE EF FG
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)

    output = []
    count = 0
    while True:

        game = chess.pgn.read_game(f)
        if not game:
            break

        count += 1

        w = game.headers['White']
        b = game.headers['Black']
        year = event.split('_')[2][:4]
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
        output.append([event, year, count, w, mean(white_evals), len(white_evals), b, mean(black_evals), len(black_evals), mean(white_evals) + mean(black_evals)])
        print('!', event, len(output))
    return output


full_output = []
headers = ['Event', 'Year', 'Game Number', 'White Player', 'White ACPL', 'White Num Moves', 'Black Player', 'Black ACPL', 'Black Num Moves', 'Combined ACPL']

events = os.listdir('./analysed_pgns')
for event in events:
    # print(event)
    with open(f'analysed_pgns/{event}') as f:
        event_outputs = pgnProcess(f, event)
    for output in event_outputs:
        full_output.append(output)

with open('analysis.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(full_output)
