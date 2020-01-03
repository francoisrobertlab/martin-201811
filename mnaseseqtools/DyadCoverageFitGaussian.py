import logging
from scipy.optimize import curve_fit

import click
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seqtools.SplitBed as sb


@click.command()
@click.option('--samples', '-s', type=click.Path(exists=True), default='samples.txt',
              help='Sample names listed one sample name by line.')
@click.option('--index', '-i', type=int, default=None,
              help='Index of sample to process in samples file.')
def main(samples, index):
    '''Fits gaussian curve to dyad coverage.'''
    logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    sample_names = pd.read_csv(samples, header=None, sep='\t', comment='#')[0]
    if index != None:
        sample_names = [sample_names[index]]
    for sample in sample_names:
        fit_gaussian(sample)
        splits = sb.splits(sample)
        for split in splits:
            fit_gaussian(split)


def fit_gaussian(sample):
    '''Fits gaussian curve to dyad coverage for a single sample.'''
    print ('Fits gaussian curve to dyad coverage of sample {}'.format(sample))
    input = sample + '-dyad.txt'
    dyads = pd.read_csv(input, sep='\t', comment='#')
    plt.plot(dyads.index.values, dyads['Relative Frequency'].values, color='red')
    plt.xlabel('Position relative to dyad (bp)')
    plt.ylabel('Relative Frequency')
    plt.title(sample)
    plot_output = sample + '-dyad-gaussian.png'
    try:
        init_vals = [dyads['Relative Frequency'].max(), 0.0, dyads.index.max() / 2]
        best_vals, covar = curve_fit(gaussian, dyads.index.values, dyads['Relative Frequency'].values, p0=init_vals)
        plt.plot(dyads.index.values, gaussian(dyads.index.values, *best_vals), color='grey')
        plt.savefig(plot_output)
    except Exception as e:
        logging.warning('could not fit gaussian curve to sample {}'.format(sample), e)
    plt.clf()


def gaussian(x, amp, cen, wid):
    return amp * np.exp(-(x - cen) ** 2 / (2.0 * wid ** 2.0))


if __name__ == '__main__':
    main()
