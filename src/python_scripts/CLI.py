import argparse
import sys

parser = argparse.ArgumentParser(description="print hello")

parser.add_argument(
    'fname',
    type=str,
    help="Enter your first name"
)

parser.add_argument(
    '-ln',
    '--last_name',
    type=str,
    help="Enter your last name"
)
args = parser.parse_args()

frist_name = args.fname
last_name = args.last_name if args.last_name else ''

print("Hello {0} {1}".format(args.fname, args.last_name))
