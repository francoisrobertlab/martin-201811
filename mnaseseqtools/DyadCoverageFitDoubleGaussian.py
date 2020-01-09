import logging

import click
from lmfit.models import GaussianModel, ConstantModel
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seqtools.SplitBed as sb


@click.command()
@click.option('--samples', '-s', type=click.Path(exists=True), default='samples.txt', show_default=True,
              help='Sample names listed one sample name by line.')
@click.option('--components', '-c', is_flag=True,
              help='Shows fit components and initial fit in plot.')
@click.option('--gaussian', '-g', is_flag=True,
              help='Shows gaussian components scaled with the constant component.')
@click.option('--verbose', '-v', is_flag=True,
              help='Shows fit report.')
@click.option('-c1', type=float, default=None,
              help='Center of first gaussian. Defaults to minus a quater of maximum index')
@click.option('--cmin1', '-cm1', type=float, default=None,
              help='Minimum value for center of first gaussian. Defaults to unbounded')
@click.option('--cmax1', '-cM1', type=float, default=None,
              help='Maximum value for center of first gaussian. Defaults to unbounded')
@click.option('-a1', type=float, default=None,
              help='Amplitude of first gaussian. Defaults to maximum relative frequency')
@click.option('--amin1', '-am1', type=float, default=None,
              help='Minimum amplitude of first gaussian. Defaults to unbounded')
@click.option('-s1', type=float, default=None,
              help='Width (sigma) of first gaussian. Defaults to a fifth of maximum index')
@click.option('--smin1', '-sm1', type=float, default=None,
              help='Minimum width (sigma) of first gaussian. Defaults unbounded')
@click.option('-c2', type=float, default=None,
              help='Center of second gaussian. Defaults to plus a quater of maximum index')
@click.option('--cmin2', '-cm2', type=float, default=None,
              help='Minimum value for center of second gaussian. Defaults to unbounded')
@click.option('--cmax2', '-cM2', type=float, default=None,
              help='Maximum value for center of second gaussian. Defaults to unbounded')
@click.option('-a2', type=float, default=None,
              help='Amplitude of second gaussian. Defaults to maximum relative frequency')
@click.option('--amin2', '-am2', type=float, default=None,
              help='Minimum amplitude of second gaussian. Defaults to unbounded')
@click.option('-s2', type=float, default=None,
              help='Width (sigma) of second gaussian. Defaults to a fifth of maximum index')
@click.option('--smin2', '-sm2', type=float, default=None,
              help='Minimum width (sigma) of second gaussian. Defaults to unbounded')
@click.option('--index', '-i', type=int, default=None,
              help='Index of sample to process in samples file.')
def main(samples, components, gaussian, verbose, c1, cmin1, cmax1, a1, amin1, s1, smin1, c2, cmin2, cmax2, a2, amin2, s2, smin2, index):
    '''Fits double gaussian curve to dyad coverage.'''
    logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    sample_names = pd.read_csv(samples, header=None, sep='\t', comment='#')[0]
    if index != None:
        sample_names = [sample_names[index]]
    for sample in sample_names:
        fit_double_gaussian(sample, components, gaussian, verbose, c1, cmin1, cmax1, a1, amin1, s1, smin1, c2, cmin2, cmax2, a2, amin2, s2, smin2)
        splits = sb.splits(sample)
        for split in splits:
            fit_double_gaussian(sample, components, gaussian, verbose, c1, cmin1, cmax1, a1, amin1, s1, smin1, c2, cmin2, cmax2, a2, amin2, s2, smin2)
           

def fit_double_gaussian(sample, components, gaussian, verbose, c1, cmin1, cmax1, a1, amin1, s1, smin1, c2, cmin2, cmax2, a2, amin2, s2, smin2):
    '''Fits double gaussian curve to dyad coverage for a single sample.'''
    print ('Fits double gaussian curve to dyad coverage of sample {}'.format(sample))
    input = sample + '-dyad.txt'
    dyads = pd.read_csv(input, sep='\t', index_col=0, comment='#')
    x = dyads.index.values
    y = dyads['Relative Frequency'].values
    if not a1:
        a1 = dyads['Relative Frequency'].max() * 50
    if not c1:
        c1 = -dyads.index.max() / 4
    if not s1:
        s1 = dyads.index.max() / 5
    if not a2:
        a2 = dyads['Relative Frequency'].max() * 50
    if not c2:
        c2 = dyads.index.max() / 4
    if not s2:
        s2 = dyads.index.max() / 5
    plt.plot(dyads.index.values, dyads['Relative Frequency'].values, color='red')
    plt.xlabel('Position relative to dyad (bp)')
    plt.ylabel('Relative Frequency')
    plt.title(sample)
    plot_output = sample + '-dyad-double-gaussian.png'
    try:
        constant = ConstantModel(prefix='c_')
        pars = constant.make_params()
        pars['c_c'].set(value=dyads['Relative Frequency'].min(), min=0.0, max=dyads['Relative Frequency'].max())
        gauss1 = GaussianModel(prefix='g1_')
        pars.update(gauss1.make_params())
        pars['g1_center'].set(value=c1, min=cmin1, max=cmax1)
        pars['g1_sigma'].set(value=s1, min=smin1)
        pars['g1_amplitude'].set(value=a1, min=amin1)
        gauss2 = GaussianModel(prefix='g2_')
        pars.update(gauss2.make_params())
        pars['g2_center'].set(value=c2, min=cmin2, max=cmax2)
        pars['g2_sigma'].set(value=s2, min=smin2)
        pars['g2_amplitude'].set(value=a2, min=amin2)
        mod = constant + gauss1 + gauss2
        init = mod.eval(pars, x=x)
        out = mod.fit(y, pars, x=x)
        if components:
            plt.plot(x, init, 'b--', label='Initial fit')
        if verbose:
            print(out.fit_report(min_correl=0.5))
        plt.plot(x, out.best_fit, 'b-', label='Best fit')
        if gaussian:
            comps = out.eval_components(x=x)
            constant_y = comps['c_']
            plt.plot(x, [yv + constant_y for yv in comps['g1_']], 'm--', label='Gaussian 1')
            plt.plot(x, [yv + constant_y for yv in comps['g2_']], 'y--', label='Gaussian 2')
        if components:
            comps = out.eval_components(x=x)
            plt.plot(x, np.repeat(comps['c_'], len(x)), 'g--', label='Constant component')
            plt.plot(x, comps['g1_'], 'm--', label='Gaussian component 1')
            plt.plot(x, comps['g2_'], 'k--', label='Gaussian component 2')
    except Exception as e:
        logging.warning('could not fit double gaussian curve to sample {}'.format(sample), e)
    if components:
        plt.legend(loc='lower right')
    plt.savefig(plot_output)


if __name__ == '__main__':
    main()
