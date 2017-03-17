#!/usr/bin/env bash

rm -rf hmmmodel.txt
rm -rf hmmoutput.txt

python3 hmmlearn.py catalan_corpus_train_tagged.txt
python3 hmmdecode.py catalan_corpus_dev_raw.txt
python3 grading_script.py catalan_corpus_dev_tagged.txt