#!/user/bin/env python3

from biobesu.helper import validate

def main(parser):
    args = __parse_command_line(parser)


def __parse_command_line(parser):
    # Adds runner-specific command line.
    parser.add_argument("--input", required=True, help="input benchmark file")
    parser.add_argument("--hpo", required=True, help="hpo.obo file")
    parser.add_argument("--output", required=True, help="directory to write output to")

    # Processes command line.
    args = parser.parse_args()
    validate.file(parser, args.input, ".tsv")
    validate.file(parser, args.hpo, ".obo")
    args.output = validate.directory(parser, args.output)

    return args
