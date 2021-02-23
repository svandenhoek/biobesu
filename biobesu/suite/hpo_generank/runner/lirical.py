#!/user/bin/env python3

from os import makedirs
from subprocess import call
from os import listdir
from biobesu.helper import validate
from biobesu.suite.hpo_generank.helper.converters import write_benchmarkdata_to_phenopackets

def main(parser):
    args = __parse_command_line(parser)
    try:
        phenopackets_dir = __generate_phenopacket_files(args)
        lirical_output_dir = __run_lirical(args, phenopackets_dir)
    except FileExistsError as e:
        print("\nAn output file/directory already exists: " + e.filename + "\nExiting...")


def __parse_command_line(parser):
    # Adds runner-specific command line.
    parser.add_argument("--jar", required=True, help="location of LIRICAL .jar file")
    parser.add_argument("--hpo", required=True, help="hpo.obo file")
    parser.add_argument("--input", required=True, help="input tsv benchmark file")
    parser.add_argument("--output", required=True, help="directory to write output to")

    parser.add_argument("--lirical_data", help="directory to write output to")
    parser.add_argument("--lirical_exomiser", help="directory to write output to")

    # Processes command line.
    try:
        args = parser.parse_args()
        validate.file(args.input, ".tsv")
        validate.file(args.hpo, ".obo")
        validate.file(args.jar, ".jar")
        args.output = validate.directory(args.output)

        if args.lirical_data is not None:
            args.lirical_data = validate.directory(args.lirical_data)
            validate.file(args.lirical_data + "Homo_sapiens_gene_info.gz")
            validate.file(args.lirical_data + "hp.obo")
            validate.file(args.lirical_data + "mim2gene_medgen")
            validate.file(args.lirical_data + "phenotype.hpoa")
        if args.lirical_exomiser is not None:
            validate.directory(args.lirical_exomiser)
    except OSError as e:
        parser.error(e)

    return args


def __generate_phenopacket_files(args):
    phenopackets_dir = args.output + "phenopackets/"
    makedirs(phenopackets_dir, exist_ok=False)
    write_benchmarkdata_to_phenopackets(args.input, phenopackets_dir, args.hpo)
    return phenopackets_dir


def __run_lirical(args, phenopackets_dir):
    # Prepares output directory.
    lirical_output_dir = args.output + "lirical_output/"
    makedirs(lirical_output_dir, exist_ok=False)

    # Digests optional arguments.
    optional_arguments = ""
    if args.lirical_data is not None:
        optional_arguments += " -d " + args.lirical_data
    if args.lirical_exomiser is not None:
        optional_arguments += " -e " + args.lirical_exomiser

    # Run tool for each input file.
    for file in listdir(phenopackets_dir):
        file_path = phenopackets_dir + file
        file_id = file.strip(".json").split('/')[-1]
        call("java -jar " + args.jar + " phenopacket -p " + file_path + " -o " + lirical_output_dir + " -x " + file_id +
             " --tsv" + optional_arguments, shell=True)

    return lirical_output_dir
