#!/user/bin/env python3

from biobesu.helper import validate
import requests


class Converter:
    @staticmethod
    def key_to_value(keys, conversion_dict, include_na=False):
        if type(keys) is list:
            values = []
            missing = set()
            for key in keys:
                try:
                    values.append(conversion_dict[key])
                except KeyError:
                    if include_na:
                        values.append('NA')
                    missing.add(key)

            return values, missing

        else:
            try:
                return conversion_dict[keys]
            except KeyError:
                return None


class GeneConverter(Converter):
    """
    If existing file is used, assumes it was downloaded through this class previously. Watch out with a manually
    downloaded file!

    """
    # Download URL (ordered by gene ID).
    download_file = 'https://www.genenames.org/cgi-bin/download/custom?col=gd_pub_eg_id&col=gd_app_sym' \
                    '&status=Approved&status=Entry%20Withdrawn&hgnc_dbtag=on&order_by=gd_pub_eg_id' \
                    '&format=text&submit=submit'

    # Expected file name.
    file_name = 'gene_ids_symbols.tsv'

    # Expected header format.
    expected_file_header = "NCBI Gene ID\tApproved symbol"

    def __init__(self, gene_file_dir):
        # The file location that needs to be loaded.
        self.gene_file = gene_file_dir + self.file_name

        # Downloads info file if not yet present in dir.
        try:
            validate.file(self.gene_file, expected_extension='.tsv')
        except OSError:
            self.__download_info_file()

        # Defines dictionaries for fast retrieval.
        self.id_by_symbol = {}
        self.symbol_by_id = {}

        # Retrieves data.
        self.__read_file()

    def __download_info_file(self):
        with requests.get(self.download_file, allow_redirects=True) as r:
            with open(self.gene_file, 'x') as file_writer:
                file_writer.write(r.content.decode('utf-8'))

    def __read_file(self):
        # Goes through the file.
        for counter, line in enumerate(open(self.gene_file)):
            # Validates if all expected columns are present and in expected order.
            if counter == 0 and line.rstrip() != self.expected_file_header:
                raise Exception("Unexpected gene info file header.\nExpected: {0}\nActual: {1}"
                                .format(self.expected_file_header, line))

            # Processes items.
            if counter > 0:
                line = line.rstrip().split("\t")

                # Ensures all items are of equal length after splitting.
                while len(line) < 2:
                    line.append('')

                # Clearer usage of data.
                gene_id = line[0]
                gene_symbol = line[1]

                # Adds gene to dict.
                if gene_id != '':
                    if self.id_by_symbol.get(gene_symbol) is not None:
                        raise Exception("The symbol {} was already assigned to {}".format(gene_symbol, gene_id))
                    self.id_by_symbol[gene_symbol] = gene_id
                    self.symbol_by_id[gene_id] = gene_symbol

    def id_to_symbol(self, gene_ids, include_na=False):
        return self.key_to_value(gene_ids, self.symbol_by_id, include_na)

    def symbol_to_id(self, gene_symbols, include_na=False):
        return self.key_to_value(gene_symbols, self.id_by_symbol, include_na)