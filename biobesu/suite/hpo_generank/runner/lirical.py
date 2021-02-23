#!/user/bin/env python3

from subprocess import call
from os import listdir
from re import search
from biobesu.helper import validate
from biobesu.helper.generic import create_dir
from biobesu.suite.hpo_generank.helper.converters import write_benchmarkdata_to_phenopackets
from biobesu.suite.hpo_generank.helper.converters import retrieve_gene_aliases_dict
from biobesu.suite.hpo_generank.helper.converters import convert_gene_aliases_to_symbol


def main(parser):
    args = __parse_command_line(parser)
    try:
        phenopackets_dir = __generate_phenopacket_files(args)
        lirical_output_dir = __run_lirical(args, phenopackets_dir)
        lirical_gene_aliases = __digest_lirical_output(args, lirical_output_dir)
        lirical_output_gene_symbols, missing = __digest_lirical_gene_aliases_file(args, lirical_gene_aliases)
        print("Aliases without a symbol: " + ','.join(missing))
    except FileExistsError as e:
        print("\nAn output file/directory already exists: " + e.filename + "\nExiting...")


def __parse_command_line(parser):
    # Adds runner-specific command line.
    parser.add_argument("--jar", required=True, help="location of LIRICAL .jar file")
    parser.add_argument("--hpo", required=True, help="hpo.obo file")
    parser.add_argument("--input", required=True, help="input tsv benchmark file")
    parser.add_argument("--output", required=True, help="directory to write output to")
    parser.add_argument("--lirical_data", required=True, help="directory to write output to")

    # Processes command line.
    try:
        args = parser.parse_args()
        validate.file(args.input, ".tsv")
        validate.file(args.hpo, ".obo")
        validate.file(args.jar, ".jar")
        args.output = validate.directory(args.output)

        args.lirical_data = validate.directory(args.lirical_data)
        validate.file(args.lirical_data + "Homo_sapiens_gene_info.gz")
        validate.file(args.lirical_data + "hp.obo")
        validate.file(args.lirical_data + "mim2gene_medgen")
        validate.file(args.lirical_data + "phenotype.hpoa")
    except OSError as e:
        parser.error(e)

    return args


def __generate_phenopacket_files(args):
    phenopackets_dir = create_dir(args.output + "phenopackets/")
    write_benchmarkdata_to_phenopackets(args.input, phenopackets_dir, args.hpo)
    return phenopackets_dir


def __run_lirical(args, phenopackets_dir):
    lirical_output_dir = create_dir(args.output + "lirical_output/")

    # Run tool for each input file.
    for file in listdir(phenopackets_dir):
        file_path = phenopackets_dir + file
        file_id = file.strip(".json").split('/')[-1]
        call("java -jar " + args.jar + " phenopacket -p " + file_path + " -o " + lirical_output_dir + " -x " + file_id +
             " -d " + args.lirical_data + " --tsv", shell=True)

    return lirical_output_dir


def __digest_lirical_output(args, lirical_output_dir):
    lirical_extraction_file = args.output + "lirical_output_extraction.tsv"
    with open(lirical_extraction_file, 'x') as file_writer:  # Requires creating a new file.
        # Writer header.
        file_writer.write("id\tgene_aliases")

        # Process input files.
        for file in listdir(lirical_output_dir):
            file_id = file.strip(".tsv").split('/')[-1]

            # Write id column.
            file_writer.write("\n" + file_id + "\t")

            # Create/write genes column.
            with open(lirical_output_dir + file) as input_file:
                genes = __extract_genes_from_lirical_data(input_file)
                file_writer.write(','.join(genes))

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


def __digest_lirical_gene_aliases_file(args, lirical_gene_aliases):
    # Dict containing {alias:symbol}
    alias_conversion_dict = retrieve_gene_aliases_dict(args.lirical_data + "Homo_sapiens_gene_info.gz")
    # Set for collecting aliases without a symbol.
    all_missing = set()

    # Prepare output file.
    lirical_output_gene_symbols = args.output + "lirical_output_gene_symbols.tsv"

    with open(lirical_output_gene_symbols, 'x') as file_writer:  # Requires creating a new file.
        # Write header.
        file_writer.write("id\tgene_symbols\n")

        # Process input file.
        with open(lirical_gene_aliases) as file_reader:
            for i, line in enumerate(file_reader):
                # Skip header.
                if i == 0:
                    continue

                # Process line.
                line = line.split('\t')
                converted_genes, missing = convert_gene_aliases_to_symbol(alias_conversion_dict, line[1].split(','))

                # Digest results.
                file_writer.write(line[0] + '\t' + ','.join(converted_genes) + '\n')
                all_missing.update(missing)

    return lirical_output_gene_symbols, missing
