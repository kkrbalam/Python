import argparse

parser = argparse.ArgumentParser(description="Demo")
parser.add_argument('--verbose', action='store_true', help='verbose flag')
args = parser.parse_args()

if args.verbose:
    print 'Verbose mode on'
else:
    print 'Not so verbose'