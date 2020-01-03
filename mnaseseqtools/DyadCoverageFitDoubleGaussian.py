import logging
from scipy.optimize import curve_fit

import click
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seqtools.SplitBed as sb


@click.command()
@click.option('--sample', '-s', default='sample',
              help='Sample name.')
@click.option('--amp1', type=float, default=None,
              help='Amplitude of first gaussian. Defaults to maximum relative frequency')
@click.option('--cen1', type=float, default=None,
              help='Center of first gaussian. Defaults to minus a quater of maximum index')
@click.option('--wid1', type=float, default=None,
              help='Width of first gaussian. Defaults to a fifth of maximum index')
@click.option('--amp2', type=float, default=None,
              help='Amplitude of second gaussian. Defaults to maximum relative frequency')
@click.option('--cen2', type=float, default=None,
              help='Center of second gaussian. Defaults to plus a quater of maximum index')
@click.option('--wid2', type=float, default=None,
              help='Width of second gaussian. Defaults to a fifth of maximum index')
def main(sample, amp1, cen1, wid1, amp2, cen2, wid2):
    '''Fits double gaussian curve to dyad coverage.'''
    logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    fit_double_gaussian(sample, amp1, cen1, wid1, amp2, cen2, wid2)
    splits = sb.splits(sample)
    for split in splits:
        fit_double_gaussian(sample, amp1, cen1, wid1, amp2, cen2, wid2)


def fit_double_gaussian(sample, amp1, cen1, wid1, amp2, cen2, wid2):
    '''Fits double gaussian curve to dyad coverage for a single sample.'''
    print ('Fits double gaussian curve to dyad coverage of sample {}'.format(sample))
    input = sample + '-dyad.txt'
    dyads = pd.read_csv(input, sep='\t', comment='#')
    if not amp1:
        amp1 = dyads['Relative Frequency'].max()
    if not cen1:
        cen1 = -dyads.index.max() / 4
    if not wid1:
        wid1 = dyads.index.max() / 5
    if not amp2:
        amp2 = dyads['Relative Frequency'].max()
    if not cen2:
        cen2 = dyads.index.max() / 4
    if not wid2:
        wid2 = dyads.index.max() / 5
    plt.plot(dyads.index.values, dyads['Relative Frequency'].values, color='red')
    plt.xlabel('Position relative to dyad (bp)')
    plt.ylabel('Relative Frequency')
    plt.title(sample)
    plot_output = sample + '-dyad-double-gaussian.png'
    try:
        init_vals = [amp1, cen1, wid1, amp2, cen2, wid2]
        best_vals, gaussian_covar = curve_fit(double_gaussian, dyads.index.values, dyads['Relative Frequency'].values, p0=init_vals)
        plt.plot(dyads.index.values, double_gaussian(dyads.index.values, *best_vals), color='grey')
        plt.savefig(plot_output)
    except Exception as e:
        logging.warning('could not fit double gaussian curve to sample {}'.format(sample), e)
    plt.clf()


def gaussian(x, amp, cen, wid):
    return amp * np.exp(-(x - cen) ** 2 / (2.0 * wid ** 2.0))


def double_gaussian(x, amp1, cen1, wid1, amp2, cen2, wid2):
    return gaussian(x, amp1, cen1, wid1) + gaussian(x, amp2, cen2, wid2)


if __name__ == '__main__':
    main()
