import logging
import math
from numpy import mean
import sys

import click
import pandas as pd
import pyBigWig as pbw
import seqtools.SplitBed as sb
import statistics

POSITIVE_STRAND = '+'
NEGATIVE_STRAND = '-'


@click.command()
@click.option('--samples', '-s', type=click.Path(exists=True), default='samples.txt',
              help='Sample names listed one sample name by line.')
@click.option('--genes', '-g', type=click.Path(exists=True), default='genes.txt',
              help='Genes information with format <spacer text> <chromosome> <Gene Name> <TSS> <Strand> <TES> <Dyad Position>.')
@click.option('--maxd', '-d', type=int, default=100,
              help='Maximum distance from dyad.')
@click.option('--smoothing', '-S', type=int, default=None,
              help='Smooth the signal by averaging on smoothing window.')
@click.option('--index', '-i', type=int, default=None,
              help='Index of sample to process in samples file.')
def main(samples, genes, maxd, smoothing, index):
    '''Finds the distribution of ditances between fragments and dyad.'''
    logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    genes_info = pd.read_csv(genes, sep='\t', comment='#')
    genes_info = genes_info.loc[genes_info[genes_info.columns[6]] != -1]
    sample_names = pd.read_csv(samples, header=None, sep='\t', comment='#')[0]
    if index != None:
        sample_names = [sample_names[index]]
    for sample in sample_names:
        dyad_coverage(sample, genes_info, maxd, smoothing)
        splits = sb.splits(sample)
        for split in splits:
            dyad_coverage(split, genes_info, maxd, smoothing)


def dyad_coverage(sample, genes, maxd, smoothing=None):
    '''Finds the distribution of ditances between fragments and dyad for a single sample.'''
    print ('Finds the distribution of ditances between fragments and dyad of sample {}'.format(sample))
    bw = pbw.open(sample + '-cov.bw')
    distances = [[] for i in range(0, maxd * 2 + 1)]
    for index, columns in genes.iterrows():
        chromosome = columns[1]
        max_end = bw.chroms(chromosome)
        if not max_end:
            max_end = 0
        negative = columns[4] == NEGATIVE_STRAND
        theo_start = int(columns[6]) - maxd
        start = max(theo_start, 0)
        end = min(int(columns[6]) + maxd + 1, max_end)
        distance = signal(bw, chromosome, start, end, smoothing) if end > start else []
        if negative:
            distance.reverse()
        for i in range(0, maxd * 2 + 1):
            distance_index = i - (start - theo_start)
            value = distance[distance_index] if distance_index in range(0, len(distance)) else 0
            distances[i].append(value if value and not math.isnan(value) else 0)
    for i in range(0, maxd * 2 + 1):
        genes['dyad position ' + str(i - maxd)] = distances[i]
    output = sample + '-dyad.txt'
    genes.to_csv(output, sep='\t', index=False)


def signal(bw, chromosome, start, end, smoothing=None):
    '''Returns signal from bigWig'''
    max_end = bw.chroms(chromosome)
    if not max_end:
        return []
    if smoothing:
        return [statistics.mean(bw.values(chromosome, max(i - smoothing, 0), min(i + smoothing, max_end))) for i in range(start, end)]
    else:
        return bw.values(chromosome, start, end)


if __name__ == '__main__':
    main()
