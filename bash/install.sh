#!/bin/bash

VENV="$HOME/mnaseseqtools-robertf-venv"

if [ "$1" == "clean" ]
then
    echo "Removing python virtual environment at $VENV"
    rm -R "$VENV"
fi
if [ ! -d "$VENV" ]
then
    echo "Creating python virtual environment at $VENV"
    python3 -m venv "$VENV"
fi
echo "Updating python libraries"
pip uninstall -y MNaseSeqTools
pip uninstall -y SeqTools
pip install git+https://git@github.com/francoisrobertlab/mnaseseqtools.git
