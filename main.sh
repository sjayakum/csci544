#!/usr/bin/env bash

cd .

rm -rf nbmodel.txt
rm -rf nboutput.txt

python train_test_creator.py

python nblearn3.py train-text.txt train-labels.txt

python nbclassify3.py test-text.txt

python compare_results.py test-labels.txt nboutput.txt

