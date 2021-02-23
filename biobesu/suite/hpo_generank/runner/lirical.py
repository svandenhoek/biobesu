#!/user/bin/env python3

from subprocess import call
from os import listdir
from re import search
from biobesu.helper import validate
from biobesu.helper.generic import create_dir
from biobesu.suite.hpo_generank.helper.converters import write_benchmarkdata_to_phenopackets

def main(parser):
    args = __parse_command_line(parser)
    try:
        phenopackets_dir = __generate_phenopacket_files(args)
        lirical_output_dir = __run_lirical(args, phenopackets_dir)
        __digest_lirical_output(args, lirical_output_dir)
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
    phenopackets_dir = create_dir(args.output + "phenopackets/")
    write_benchmarkdata_to_phenopackets(args.input, phenopackets_dir, args.hpo)
    return phenopackets_dir


def __run_lirical(args, phenopackets_dir):
    lirical_output_dir = create_dir(args.output + "lirical_output/")

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


def __digest_lirical_output(args, lirical_output_dir):
    lirical_extraction_file = args.output + "lirical_output_extraction.tsv"
    file_writer = open(lirical_extraction_file, 'x')  # Requires creating a new file.
    file_writer.write("id\tgene_aliases")

    for file in listdir(lirical_output_dir):
        file_id = file.strip(".tsv").split('/')[-1]

        # Write id column.
        file_writer.write("\n" + file_id + "\t")

        # Create/write genes column.
        genes = __extract_genes_from_lirical_data(open(lirical_output_dir + file))
        file_writer.write(','.join(genes))

    file_writer.flush()
    file_writer.close()

    return lirical_extraction_file


def __extract_genes_from_lirical_data(file_data):
    genes = []
    header = True

    # Goes through all files (test cases).
    for line in file_data:
        # Skip lirical lines.
        if line.startswith('!'):
            continue

        # Skip header.
        if header:
            header = False
            continue

        gene_alias = search(r'\t[\w, ]+; ([\w]+)', line)
        if gene_alias is not None:
            genes.append(gene_alias[1])

    return genes
