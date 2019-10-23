import logging
import os
import subprocess

import click
import pandas as pd


@click.command()
@click.option('--samples', '-s', type=click.Path(exists=True), default='samples-filter.txt',
              help='Tab-separated file containing '
              'the sample names with tag in the first column and '
              'the original sample names in the second column.')
@click.option('--annotations', '-a', type=click.Path(exists=True), default='annotations.bed',
              help='Keep reads for which their center is located on specified annotations.')
def main(samples, annotations):
    '''Keep only reads that intersects specified annotations.'''
    logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    sample_columns = pd.read_csv(samples, header=None, sep='\t', comment='#')
    annot_length = annotations_length(annotations)
    for index, columns in sample_columns.iterrows():
        tag = columns[0]
        sample = columns[1] if len(columns) > 1 else None
        intersect(sample, tag, annotations, annot_length)


def annotations_length(annotations):
    '''Find the length of an annotation'''
    with open(annotations, 'r') as infile:
        for line in infile:
            if not line.startswith('#'):
                return len(line.split('\t'))


def intersect(sample, tag, annotations, annot_length):
    '''Keep only reads that intersects specified annotations for a single sample.'''
    print ('Keep only reads that intersects specified annotations for sample {}'.format(sample))
    bed_raw = sample + '-raw.bed'
    bed_tag_raw = tag + '-raw.bed'
    bed_tmp = tag + '-tmp.bed'
    cmd = ['bedtools', 'intersect', '-a', annotations, '-b', bed_raw, '-wb']
    logging.debug('Running {}'.format(cmd))
    with open(bed_tmp, 'w') as outfile:
        subprocess.call(cmd, stdout=outfile)
    if not os.path.isfile(bed_tmp):
        raise AssertionError('Error when calling bedtools intersect for sample ' + sample)
    with open(bed_tmp, 'r') as infile, open(bed_tag_raw, 'w') as outfile:
        for line in infile:
            if line.startswith('#'):
                outfile.write(line)
            else:
                columns = line.split('\t')
                for i in range(annot_length, len(columns)):
                    outfile.write(columns[i])
                outfile.write('\n')
    os.remove(bed_tmp)
    

if __name__ == '__main__':
    main()
