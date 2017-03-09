#!/usr/bin/env bash

rm -rf hmmmodel.txt
rm -rf hmmoutput.txt

python hmmlearn.py catalan_corpus_train_tagged.txt
python hmmdecode.py catalan_corpus_dev_raw.txt
python grading_script.py