help([[
For detailed instructions, go to:
    https://github.com/francoisrobertlab/mnase-201908

This module sets the following environment variables:
    CHEC_BASE: directory containing MNase-seq source code
    CHEC_PATH: directory containing MNase-seq analysis tools in python
    CHEC_VENV: directory containing MNase-seq's virtual environment for python

This module loads the following modules and their requirements:
    - python/3.7.4
    - bwa/0.7.17
    - samtools/1.9
    - bedtools/2.27.1
    - kentutils/20180716
    - r/3.6.0
]])

whatis("Version: 1.0.0")
whatis("Keywords: MNase-seq, Utility")
whatis("URL: https://github.com/francoisrobertlab/mnase-201908")
whatis("Description: MNase-seq analysis for Celia Jeronimo data")

always_load("nixpkgs/16.09")
always_load("gcc/7.3.0")
always_load("python/3.7.4")
always_load("bwa/0.7.17")
always_load("samtools/1.9")
always_load("bedtools/2.27.1")
always_load("kentutils/20180716")
always_load("r/3.6.0")
always_load("vap")

local base = "~/projects/def-robertf/mnase-201908"
prepend_path("PATH", pathJoin(base,"bash"))
prepend_path("PATH", pathJoin(base,"venv/bin"))
setenv("MNASE_BASE", base)
setenv("MNASE_PATH", pathJoin(base,"mnaseseqtools"))
setenv("MNASE_VENV", pathJoin(base,"venv/bin"))
