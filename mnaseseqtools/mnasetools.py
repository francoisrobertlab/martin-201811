import click

from mnaseseqtools import DyadCoverage, DyadCoverageFitDoubleGaussian, DyadCoverageFitGaussian, FirstDyadPositionFinder, PrepareGenomeCoverage


@click.group()
def mnasetools():
    pass


mnasetools.add_command(DyadCoverage.dyadcov)
mnasetools.add_command(DyadCoverageFitGaussian.fitgaussian)
mnasetools.add_command(DyadCoverageFitDoubleGaussian.fitdoublegaussian)
mnasetools.add_command(FirstDyadPositionFinder.firstdyadposition)
mnasetools.add_command(PrepareGenomeCoverage.prepgenomecov)

if __name__ == '__main__':
   mnasetools()
