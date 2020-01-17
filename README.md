# register-data-augmentation

Simple data augmentation scripts for text classification

## Quickstart

Generate a variant of `example-data/fincore-train-sample.tsv` containing
the last 512 basic tokens of each text:

    python3 augment.py --last-tokens 512 \
        example-data/fincore-train-sample.tsv \
	> fincore-train-extra.tsv

## Example data

`example-data/fincore-train-sample.tsv` was sampled from
[FinCORE](https://github.com/TurkuNLP/fincore) training data with

    shuf FinCORE/data/train.tsv | head -n 100 \
        > example-data/fincore-train-sample.tsv
