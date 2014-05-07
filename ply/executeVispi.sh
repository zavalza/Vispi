#!/bin/bash
make clean
python vispi.py $1 > debugOutput
rm tempMain.cpp
make
sudo ./vispi