#!/user/bin/env python3

from biobesu.helper.generic import retrieve_entry_point


def main(parser):
    # Adds suite-specific command line.
    parser.add_argument("runner", help="the tool to be ran")

    # Processes command line.
    args, unknown_args = parser.parse_known_args()

    # Load available runners.
    runners = retrieve_entry_point('biobesu_hpo_generank')

    # Run selected runner.
    runners[args.runner](parser)
