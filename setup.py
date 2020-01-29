from setuptools import setup, find_packages

setup(
    name='MNaseSeqTools',
    version='0.1-SNAPSHOT',
    packages=find_packages(),
    author='Christian Poitras',
    author_email='christian.poitras@ircm.qc.ca',
    description='Tools to analyze MNase-seq data',
    keywords='bioinformatics, MNase-seq',
    url='https://github.com/francoisrobertlab/mnaseseqtools',
    license='GNU General Public License version 3',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License version 3'
    ],
    python_requires='>=3.7.4',
    install_requires=[
        'click>=7.0',
        'pandas>=0.25.3',
        'pyBigWig>=0.3.17',
        'matplotlib>=3.1.1',
        'scipy>=1.3.2',
        'lmfit>=1.0.0',
        'seqtools@http://github.com/francoisrobertlab/seqtools/tarball/master'
    ],
    entry_points={
        'console_scripts': [
            'dyadcov = mnaseseqtools.DyadCoverage:main',
            'fitdoublegaussian = mnaseseqtools.DyadCoverageFitDoubleGaussian:main',
            'fitgaussian = mnaseseqtools.DyadCoverageFitGaussian:main',
            'prepgenecov = mnaseseqtools.PrepareGenomeCoverage:main',
            'fullanalysis = mnaseseqtools.FullAnalysis:main'
        ]
    }
)
