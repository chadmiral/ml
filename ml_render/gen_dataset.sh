#!/bin/sh

rm ./data/labels.csv
rm ./data/judkins_box/*.png
blender --background --python blender_dataset_gen.py