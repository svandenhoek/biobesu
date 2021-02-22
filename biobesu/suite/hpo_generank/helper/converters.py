#!/user/bin/env python3

from datetime import datetime
from biobesu.helper.reader import read_hpo_obo


def write_benchmarkdata_to_phenopackets(input_file, output_dir, hpo_obo_file):
    phenotype_dict = read_hpo_obo(hpo_obo_file)

    # Digests the benchmark cases.
    for i, line in enumerate(open(input_file)):
        # Skips first line (header).
        if i == 0:
            continue

        # Splits the columns.
        line = line.rstrip().split('\t')

        # Retrieve converted data.
        output_string = convert_benchmarkdata_linesplit_to_phenopackets(line, phenotype_dict)

        # Write output.
        file_writer = open(output_dir + line[0] + '.json', 'w')
        file_writer.write(output_string)
        file_writer.flush()
        file_writer.close()


def convert_benchmarkdata_linesplit_to_phenopackets(line, phenotype_dict):
    # Writes opening bracket.
    output_string = '{'

    # Convert row id to phenopackets.
    output_string += '\n\t"id": "' + line[0] + '",' + \
                     '\n\t"phenotypic_features": ['

    # Retrieves the phenotypes.
    phenotypes = line[2].split(',')

    # Converts phenotypes phenopackets.
    for i, phenotype in enumerate(phenotypes):
        output_string += '{' \
                         '\n\t\t"type": {' \
                         '\n\t\t\t"id": "' + phenotype + '",' + \
                         '\n\t\t\t"label": "' + phenotype_dict[phenotype] + '"' + \
                         '\n\t\t}' \
                         '\n\t}'
        if i < len(phenotypes)-1:
            output_string += ', '

    # Closing bracket for phenotypicFeatures.
    output_string += '],'

    # Add metadata.
    output_string += '\n\t"meta_data": {' \
                     '\n\t\t"created": "' + str(datetime.now()) + '",' + \
                     '\n\t\t"created_by": "biobesu",' \
                     '\n\t\t"resources": [{' \
                     '\n\t\t\t"id": "hp",' \
                     '\n\t\t\t"name": "Human Phenotype Ontology",' \
                     '\n\t\t\t"namespacePrefix": "HP",' \
                     '\n\t\t\t"url": "http://purl.obolibrary.org/obo/hp.owl",' \
                     '\n\t\t\t"version": "2018-03-08",' \
                     '\n\t\t\t"iriPrefix": "http://purl.obolibrary.org/obo/HP_"' \
                     '\n\t\t}]' \
                     '\n\t}'

    # Writes closing bracket.
    output_string += '\n}'

    return output_string
