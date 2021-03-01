#!/user/bin/env python3

from unittest.mock import patch
from unittest.mock import mock_open
from biobesu.helper import converters

gene_info_file = """NCBI Gene ID	Approved symbol
1	A1BG
2	A2M
3	A2MP1
9	NAT1
10	NAT2
11	NATP
"""


@patch("builtins.open", new_callable=mock_open, read_data=gene_info_file)
def test_id_to_symbol_single(mock_open):
    converter = converters.GeneConverter("path/to/file")

    input_data = '9'
    expected_output = 'NAT1'
    actual_output = converter.id_to_symbol(input_data)

    assert actual_output == expected_output


@patch("builtins.open", new_callable=mock_open, read_data=gene_info_file)
def test_id_to_symbol_list(mock_open):
    converter = converters.GeneConverter("/path/to/file")

    input_data = ['10', '3']
    expected_output = (['NAT2', 'A2MP1'], set())
    actual_output = converter.id_to_symbol(input_data)

    assert actual_output == expected_output


@patch("builtins.open", new_callable=mock_open, read_data=gene_info_file)
def test_id_to_symbol_list_with_missing(mock_open):
    converter = converters.GeneConverter("/path/to/file")

    input_data = ['10', '3', '14']
    expected_output = (['NAT2', 'A2MP1'], set(('14',)))
    actual_output = converter.id_to_symbol(input_data)

    assert actual_output == expected_output