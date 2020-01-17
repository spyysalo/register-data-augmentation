#!/usr/bin/env python3

import sys
import re


# Regex approximating BERT basic tokenization
TOKENIZATION_RE = re.compile(r'([^\W_]+|\s+|.)', flags=re.UNICODE)


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('-f', '--text-field', metavar='IDX', type=int, default=-1,
                    help='Index of text field (0-based, default last)')
    ap.add_argument('-l', '--last-tokens', metavar='N', type=int, default=None,
                    help='Output last N basic tokens of each text')
    ap.add_argument('file', nargs='+',
                    help='TSV file(s) with text')
    return ap


def process_text(text, options):
    if options.last_tokens:
        tokens = [t for t in TOKENIZATION_RE.split(text) if t]
        last_tokens, nonspace_count = [], 0
        for i in reversed(range(len(tokens))):
            if nonspace_count >= options.last_tokens:
                break
            last_tokens.append(tokens[i])
            if tokens[i] and not tokens[i].isspace():
                nonspace_count += 1
        text = ''.join(reversed(last_tokens))
    return text

        
def process(fn, options):
    with open(fn) as f:
        for ln, l in enumerate(f, start=1):
            l = l.rstrip('\n')
            fields = l.split('\t')
            try:
                text = fields[options.text_field]
            except IndexError:
                raise ValueError('failed to parse line {} in {}: {}'.format(
                    ln, fn, l))
            text = process_text(text, options)
            fields[options.text_field] = text
            print('\t'.join(fields))


def main(argv):
    args = argparser().parse_args(argv[1:])
    for fn in args.file:
        process(fn, args)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
