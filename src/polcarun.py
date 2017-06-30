__doc__ = '''{f}: Python implementation of the online grammar compression algorithm OLCA.

Usage:
  {f} (comp | decomp) [options]
  
Options:
  -i FILE --input FILE              input file  [default: stdin]
  -o FILE --output FILE             output file [default: stdout]
  -e ENCODING --encoding ENCODING   open input/output by ENCODING for comp/decomp [default: binary]
                                    if ENCODING="binary", treat a byte as a single character 
                                    otherwise, treat a multi-byte encoded by ENCODING as a single character
'''.format(f=__file__)

import sys
import io
from docopt import docopt
from polca import compress, decompress

if __name__=='__main__':
  args = docopt(__doc__)
  if args['comp']:
    if args['--input'] == 'stdin':
      input = sys.stdin.buffer if args['--encoding'] == 'binary' else io.TextIOWrapper(sys.stdin.buffer, encoding=args['--encoding'])
    else:
      input = open(args['--input'], 'rb') if args['--encoding'] == 'binary' else open(args['--input'], 'r', encoding=args['--encoding'])
    output = sys.stdout if args['--output'] == 'stdout' else open(args['--output'], 'w')
    compress(input, output)
  else:
    input = sys.stdin if args['--input'] == 'stdin' else open(args['--input'], 'r')
    if args['--output'] == 'stdout':
      output = sys.stdout.buffer if args['--encoding'] == 'binary' else io.TextIOWrapper(sys.stdout.buffer, encoding=args['--encoding'])
    else:
      output = open(args['--output'], 'wb') if args['--encoding'] == 'binary' else open(args['--output'], 'w', encoding=args['--encoding'])
    decompress(input, output)