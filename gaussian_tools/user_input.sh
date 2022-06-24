#!/bin/bash
echo "Enter Gaussian logfile name: "
echo "Filename entered: $1!"
echo "Enter image filename: "
python gaussian_fileparser.py -i $1 -o $2