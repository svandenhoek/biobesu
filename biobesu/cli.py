#!/user/bin/env python3

from argparse import ArgumentParser
from biobesu.helper.generic import retrieve_entry_point


def main():
    # Defines global command line.
    parser = ArgumentParser()
    parser.add_argument("suite", help="the type of job to execute")

    # Processes command line.
    args, unknown_args = parser.parse_known_args()

    # Load available suites.
    suites = retrieve_entry_point('biobesu_suites')

    # Run selected suite.
    suites[args.suite](parser)
