#!/user/bin/env python3

from os import mkdir
from os.path import isdir
from biobesu.helper import validate
from biobesu.suite.hpo_generank.helper.converters import write_benchmarkdata_to_phenopackets

def main(parser):
    args = __parse_command_line(parser)
    __generate_phenopacket_files(args)


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


def __generate_phenopacket_files(args):
    phenopackets_dir = args.output + "/phenopackets/"

    # Skips creating phenopackets if dir already exists.
    if isdir(phenopackets_dir):
        print("Phenopackets subdirectory found, skipping conversion of benchmark data.")
        return

    mkdir(phenopackets_dir)
    write_benchmarkdata_to_phenopackets(args.input, phenopackets_dir, args.hpo)
