#!/user/bin/env python3

from biobesu.helper.converters import Converter
import gzip


class LiricalGeneAliasConverter(Converter):
    def __init__(self, omim2gene_file):
        self.gene_info_dict = self.__read_gene_info(omim2gene_file)

    def __read_gene_info(self, file_path):
        gene_info_dict = {}

        with gzip.open(file_path, 'rt') as file:
            for line in file:
                line = line.split('\t')
                gene_symbol = line[2]
                aliases = line[4]
                aliases = aliases.split('|')

                for alias in aliases:
                    gene_info_dict[alias] = gene_symbol

        return gene_info_dict

    def alias_to_gene_symbol(self, gene_aliases, include_na=False):
        return self.key_to_value(gene_aliases, self.gene_info_dict, include_na)


class LiricalOmimConverter(Converter):
    def __init__(self, omim2gene_file):
        self.omim_dict = self.__read_omim2gene(omim2gene_file)

    def __read_omim2gene(self, file_path):
        omim_dict = {}

        with open(file_path) as file:
            for line in file:
                line = line.split('\t')
                if line[1] != '-':
                    omim_dict[line[0]] = line[1]

        return omim_dict

    def omim_to_gene_id(self, omims, include_na=False):
        return self.key_to_value(omims, self.omim_dict, include_na)
