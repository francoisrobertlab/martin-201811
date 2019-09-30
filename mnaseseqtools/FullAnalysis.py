import logging
import os

import PrepareGenomeCoverage
import click
import pandas as pd
import seqtools.Bam2Bed
import seqtools.DownloadSample
import seqtools.GenomeCoverage
import seqtools.MergeSampleBed
import seqtools.RunBwa
import seqtools.SplitBed


@click.command()
@click.option('--samples', '-s', type=click.Path(exists=True), default='samples.txt',
              help='Sample names listed one sample name by line.'
              ' An SRR id can be provided (tab-separated) to download the FASTQ file automatically, otherwise FASTQ file must be provided.')
@click.option('--merge', '-m', type=click.Path(), default='merge.txt',
              help='Merge name if first columns and sample names to merge on following columns - tab delimited.')
@click.option('--fasta', '-f', type=click.Path(exists=True), default='sacCer3.fa',
              help='FASTA file used for alignment.')
@click.option('--sizes', '-S', type=click.Path(exists=True), default='sacCer3.chrom.sizes',
              help='Size of chromosomes.')
@click.option('--threads', '-t', default=1,
              help='Number of threads used to process data per sample.')
@click.option('--splitLength', type=int, default=None,
              help='Split reads in bins by their length.')
@click.option('--splitMinLength', default=100,
              help='Split reads minimum length.')
@click.option('--splitMaxLength', default=500,
              help='Split reads maximum length.')
def main(samples, merge, fasta, sizes, threads, splitlength, splitminlength, splitmaxlength):
    '''Analyse Martin et al. data from November 2018 in Genetics.'''
    logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    RunBwa.bwa_index(fasta)
    sample_columns = pd.read_csv(samples, header=None, sep='\t', comment='#')
    for index, columns in sample_columns.iterrows():
        sample = columns[0]
        fastq = columns[1] if len(columns) > 1 else None
        srr = columns[2] if len(columns) > 2 else None
        analyse(sample, fastq, srr, fasta, sizes, splitlength, splitminlength, splitmaxlength, threads)
    merge_columns = pd.read_csv(merge, header=None, sep='\t', comment='#')
    for index, columns in merge_columns.iterrows():
        sample = columns[0]
        samples_to_merge = columns[1:] if len(columns) > 1 else None
        MergeSampleBed.merge_samples(sample, samples_to_merge)
        analyse_merged(sample, sizes, splitlength, splitminlength, splitmaxlength)


def analyse(sample, fastq, srr, fasta, sizes, splitlength, splitminlength, splitmaxlength, threads=None):
    '''Analyse a single sample.'''
    try:
        print ('Analyse sample {}'.format(sample))
        DownloadSample.download(sample, fastq, srr)
        RunBwa.align(sample, fastq, fasta, threads)
        Bam2Bed.bam_to_bed(sample, threads)
        if splitlength is not None:
            SplitBed.split_bed(sample, splitlength, splitminlength, splitmaxlength)
        PrepareGenomeCoverage.prepare_genome_coverage(sample, sizes)
        GenomeCoverage.genome_coverage(sample, sizes)
    except Exception as e:
        logging.exception('Could not analyse sample {}'.format(sample))
        raise e


def analyse_merged(sample, sizes, splitlength, splitminlength, splitmaxlength):
    '''Compute coverage of a single sample.'''
    print ('Analyse sample {}'.format(sample))
    try:
        if splitlength is not None:
            SplitBed.split_bed(sample, splitlength, splitminlength, splitmaxlength)
        PrepareGenomeCoverage.prepare_genome_coverage(sample, sizes)
        GenomeCoverage.genome_coverage(sample, sizes)
    except Exception as e:
        logging.exception('Could not analyse sample {}'.format(sample))
        raise e


if __name__ == '__main__':
    main()
