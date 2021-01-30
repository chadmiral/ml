#!/bin/sh

column -s, -t < data/labels.csv | less -#2 -N -S
