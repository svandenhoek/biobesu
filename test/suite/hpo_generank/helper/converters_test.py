#!/user/bin/env python3

import pytest
from re import sub
from biobesu.suite.hpo_generank.helper.converters import convert_benchmarkdata_linesplit_to_phenopackets


def test_benchmark_linesplit_to_phenopacket():
    input_string = ['1', 'A1BG', 'HP:0001234,HP:0004321']

    # Removed from expected (before "created_by" line): '\n\t\t"created": <current_time>,' \
    expected_output = '{' \
                      '\n\t"id": "1",' \
                      '\n\t"phenotypic_features": [{' \
                      '\n\t\t"type": {' \
                      '\n\t\t\t"id": "HP:0001234",' \
                      '\n\t\t\t"label": "Hitchhiker thumb"' \
                      '\n\t\t}' \
                      '\n\t}, {' \
                      '\n\t\t"type": {' \
                      '\n\t\t\t"id": "HP:0004321",' \
                      '\n\t\t\t"label": "Bladder fistula"' \
                      '\n\t\t}' \
                      '\n\t}],' \
                      '\n\t"meta_data": {' \
                      '\n\t\t"created_by": "biobesu",' \
                      '\n\t\t"resources": [{' \
                      '\n\t\t\t"id": "hp",' \
                      '\n\t\t\t"name": "Human Phenotype Ontology",' \
                      '\n\t\t\t"namespacePrefix": "HP",' \
                      '\n\t\t\t"url": "http://purl.obolibrary.org/obo/hp.owl",' \
                      '\n\t\t\t"version": "2018-03-08",' \
                      '\n\t\t\t"iriPrefix": "http://purl.obolibrary.org/obo/HP_"' \
                      '\n\t\t}]' \
                      '\n\t}' \
                      '\n}'

    # Simple simulation for retrieved data from a `hp.obo` file.
    phenotypes_dict = {"HP:0001234": "Hitchhiker thumb",
                       "HP:0004321": "Bladder fistula"}

    actual_output = convert_benchmarkdata_linesplit_to_phenopackets(input_string, phenotypes_dict)
    # Removes creation date for easier validation.
    # Date format: 2021-02-22 13:49:00.795222
    actual_output = sub(r'\t\t"created": "[0-9\- :.]+",\n', '', actual_output)

    assert actual_output == expected_output
