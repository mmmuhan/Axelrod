"""A script to run the Axelrod tournament.

The code for strategies is present in `axelrod/strategies`.
"""

from __future__ import division

import argparse
import time

import numpy

import matplotlib.pyplot as plt

import axelrod


def run_tournament(turns, repetitions, exclude_basic, exclude_strategies, exclude_cheating, exclude_all):
    """Main function for running Axelrod tournaments."""
    graphs_to_plot = {}

    init_strategies = lambda S: [s() for s in S]
    if not exclude_basic:
        graphs_to_plot['basic_results.png'] = init_strategies(axelrod.basic_strategies)
    if not exclude_strategies:
        graphs_to_plot['results.png'] = init_strategies(axelrod.strategies)
    if not exclude_cheating:
        graphs_to_plot['cheating_results.png'] = init_strategies(axelrod.cheating_strategies)
    if not exclude_all:
        graphs_to_plot['all_results.png'] = init_strategies(axelrod.all_strategies)

    for plot in graphs_to_plot:
        if len(graphs_to_plot[plot]) != 1:

            tournament = axelrod.Tournament(
                players=graphs_to_plot[plot],
                turns=turns,
                repetitions=repetitions)

            # This is where the actual tournament takes place.
            results = tournament.play()

            # # Save the scores from this tournament to a CSV file.
            csv = results.csv()
            fname = plot.replace('.png', '.csv')
            with open('./assets/' + fname, 'w') as f:
                f.write(csv)

            # Save plots with the scores.
            plt.boxplot([s / (turns * (len(results.ranking) - 1)) for s in results.scores[results.ranking]])
            plt.xticks(range(1, len(results.ranked_names) + 2), [str(n) for n in results.ranked_names], rotation=90)
            plt.title('Mean score per stage game over {} rounds repeated {} times ({} strategies)'.format(turns, repetitions, len(results.ranking)))
            plt.savefig('./assets/' + plot, bbox_inches='tight')
            plt.clf()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='show verbose messages')
    parser.add_argument('-t', '--turns', type=int, default=200, help='turns per pair')
    parser.add_argument('-r', '--repetitions', type=int, default=50, help='round-robin repetitions')
    parser.add_argument('--xb', action='store_true', help='exlude basic strategies plot')
    parser.add_argument('--xs', action='store_true', help='exlude ordinary strategies plot')
    parser.add_argument('--xc', action='store_true', help='exclude cheating strategies plot')
    parser.add_argument('--xa', action='store_true', help='exclude combined strategies plot')
    args = parser.parse_args()

    t0 = time.time()

    if args.verbose:
        print 'Starting tournament with ' + str(args.repetitions) + ' round robins of ' + str(args.turns) + ' turns per pair.'
        print 'Basics strategies plot: ' + str(not args.xb)
        print 'Ordinary strategies plot: ' + str(not args.xs)
        print 'Cheating strategies plot: ' + str(not args.xc)
        print 'Combined strategies plot: ' + str(not args.xa)
    run_tournament(args.turns, args.repetitions, args.xb, args.xs, args.xc, args.xa)

    dt = time.time() - t0
    print "Finished in %.1fs" % dt
