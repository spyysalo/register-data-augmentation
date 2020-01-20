#!/usr/bin/env python3

# Special-purpose script for sampling documents from data where document
# boundaries are identified by a specifically formatted comment line.

import sys
import os
import re
import random
import gzip

from logging import warning


DOC_ID_RE = re.compile(r'###C:\d+ <urn:uuid:([0-9a-z-]+)>.*')


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('-e', '--encoding', default='UTF-8')
    ap.add_argument('-o', '--output-dir', default=None,
                    help='Output directory (default stdout)')
    ap.add_argument('ratio', type=float,
                    help='Ratio of documents to sample')
    ap.add_argument('file', nargs='+',
                    help='File(s) with documents')
    return ap


def sample_stream(f, fn, options):
    current_id, output_current, out = None, None, None
    for ln, l in enumerate(f, start=1):
        l = l.rstrip('\n')
        m = DOC_ID_RE.match(l)
        if m:
            current_id = m.group(1)
            if out is not None and out is not sys.stdout:
                out.close()
                out = None
            if random.random() > options.ratio:
                output_current = False
            else:
                output_current = True
                if not options.output_dir:
                    out = sys.stdout
                else:
                    out = open(os.path.join(options.output_dir,
                                            current_id + '.txt'), 'wt')
        if current_id is None:
            warning('Discarding text before first ID: {}'.format(l))
        elif output_current:
            print(l, file=out)


def sample(fn, options):
    if fn.endswith('.gz'):
        with gzip.open(fn, 'rt', encoding=options.encoding) as f:
            return sample_stream(f, fn, options)
    else:
        with open(fn) as f:
            return sample_stream(f, fn, options)

    
def main(argv):
    args = argparser().parse_args(argv[1:])
    for fn in args.file:
        sample(fn, args)
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
